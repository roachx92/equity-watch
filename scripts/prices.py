#!/usr/bin/env python3
"""Settled daily price bars for a watched ticker — stdlib only, no API key.

Why this exists: the Recent News Log has twice recorded a wrong close, both
times because a research pass read a *percentage headline* ("down 7.99% today")
and chained it off the prior close. Those headlines are intraday snapshots
published mid-session and are routinely misdated by aggregators. On 2026-07-27
that produced a logged close of $259.58 for COHR against a settled close of
$271.31 — an $11.73 error that propagated into the drawdown and two-session
figures of the entry built on top of it.

So: never derive a close from a percentage. Read the settled bar, and compute
the percentage from the bars. That is the whole job.

Source is Yahoo's public chart endpoint (the same one `yfinance` wraps), reached
with `urllib` so this stays importable on a bare runner — every other script in
`scripts/` is stdlib-only and five workflows run them with no pip install step.

**The UNSETTLED marker is the point.** Yahoo returns a bar for the *current*
session while it is still trading. That bar is exactly the intraday reading that
caused both prior errors, so it is flagged loudly and excluded from `--json`
unless `--include-live` is passed. A bar marked UNSETTLED must never be written
to a news.md entry as a close.

Usage:
    python scripts/prices.py COHR                  # ~1mo of settled daily bars
    python scripts/prices.py COHR --range 3mo
    python scripts/prices.py COHR --since 2026-07-17
    python scripts/prices.py COHR --json
    python scripts/prices.py --all                 # latest settled close, every ticker

Not financial advice — informational research tooling only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import ticker_dirs  # noqa: E402

_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
_UA = "Mozilla/5.0 (compatible; equity-watch/1.0; +https://github.com/roachx92/equity-watch)"

#: Watch-list ticker -> Yahoo symbol, for names whose folder name is not the
#: Yahoo symbol. Folder names follow the research convention (LPKF is the
#: company); Yahoo wants the *listing*. Add a line here when a ticker's primary
#: listing is not a plain US one. LPKF trades Xetra: LPK (EUR) with an OTC ADR
#: (LPKFF, USD) — the Xetra line is primary, so that is what we quote.
SYMBOL_OVERRIDES = {
    "LPKF": "LPK.DE",
}


class PriceError(RuntimeError):
    """Fetch or parse failure, with a message safe to show a human."""


def yahoo_symbol(ticker: str) -> str:
    return SYMBOL_OVERRIDES.get(ticker.upper(), ticker.upper())


def fetch(ticker: str, rng: str = "1mo", timeout: int = 20) -> dict:
    """Return the parsed chart payload for `ticker`, or raise PriceError."""
    symbol = yahoo_symbol(ticker)
    url = f"{_CHART.format(symbol=symbol)}?interval=1d&range={rng}"
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise PriceError(
                f"{ticker}: Yahoo has no symbol {symbol!r}. If this is a foreign "
                f"listing, add its Yahoo symbol to SYMBOL_OVERRIDES in {Path(__file__).name}."
            ) from exc
        raise PriceError(f"{ticker}: HTTP {exc.code} fetching {symbol}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise PriceError(f"{ticker}: network error fetching {symbol} — {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PriceError(f"{ticker}: malformed JSON from Yahoo for {symbol}") from exc

    err = (payload.get("chart") or {}).get("error")
    if err:
        raise PriceError(f"{ticker}: Yahoo error — {err}")
    results = (payload.get("chart") or {}).get("result") or []
    if not results:
        raise PriceError(f"{ticker}: empty result for {symbol}")
    return results[0]


def _local_date(epoch: int, gmtoffset: int) -> str:
    """Exchange-local calendar date for a bar timestamp.

    Bars are stamped at the session open in UTC epoch. For a US listing the UTC
    date happens to match the local date, but that is a coincidence of the
    offset — for Xetra it is not guaranteed, so shift explicitly rather than
    relying on it.
    """
    return dt.datetime.fromtimestamp(epoch + gmtoffset, dt.UTC).strftime("%Y-%m-%d")


def bars(result: dict) -> tuple[list[dict], dict]:
    """Split a chart result into (bars, meta). Bars carry a `settled` flag."""
    meta = result.get("meta") or {}
    gmtoffset = int(meta.get("gmtoffset") or 0)
    stamps = result.get("timestamp") or []
    quote = ((result.get("indicators") or {}).get("quote") or [{}])[0]

    # A bar for the session currently trading is not a close. Identify it by
    # comparing against the exchange-local date of the last trade Yahoo reports.
    market_time = meta.get("regularMarketTime")
    live_date = _local_date(int(market_time), gmtoffset) if market_time else None
    period_end = ((meta.get("currentTradingPeriod") or {}).get("regular") or {}).get("end")
    market_open = bool(market_time and period_end and int(market_time) < int(period_end))

    out: list[dict] = []
    for i, stamp in enumerate(stamps):
        close = (quote.get("close") or [None] * len(stamps))[i]
        if close is None:
            continue  # holiday / halted / not yet printed
        date = _local_date(int(stamp), gmtoffset)
        out.append(
            {
                "date": date,
                "open": (quote.get("open") or [None] * len(stamps))[i],
                "high": (quote.get("high") or [None] * len(stamps))[i],
                "low": (quote.get("low") or [None] * len(stamps))[i],
                "close": close,
                "volume": (quote.get("volume") or [None] * len(stamps))[i],
                "settled": not (market_open and date == live_date),
            }
        )

    for prev, cur in zip(out, out[1:]):
        if prev["close"]:
            cur["pct"] = (cur["close"] / prev["close"] - 1) * 100.0
    return out, meta


def render(ticker: str, rows: list[dict], meta: dict, since: str | None) -> str:
    if since:
        rows = [r for r in rows if r["date"] >= since]
    if not rows:
        return f"{ticker}: no bars in range."

    cur = meta.get("currency") or "?"
    ex = meta.get("fullExchangeName") or meta.get("exchangeName") or "?"
    sym = yahoo_symbol(ticker)
    head = f"{ticker} ({sym} | {ex} | {cur})"

    lines = [head, "", f"{'date':<12}{'close':>11}{'chg':>10}{'volume':>14}  note", "-" * 60]
    for r in rows:
        pct = f"{r['pct']:+.2f}%" if "pct" in r else ""
        vol = f"{r['volume']:,}" if r.get("volume") else ""
        note = "" if r["settled"] else "UNSETTLED - session live, not a close"
        lines.append(f"{r['date']:<12}{r['close']:>11.2f}{pct:>10}{vol:>14}  {note}")

    settled = [r for r in rows if r["settled"]]
    if settled:
        first, last = settled[0], settled[-1]
        if first is not last and first["close"]:
            move = (last["close"] / first["close"] - 1) * 100.0
            lines += [
                "",
                f"Settled {first['date']} -> {last['date']}: "
                f"{first['close']:.2f} -> {last['close']:.2f} ({move:+.2f}%)",
            ]
    if any(not r["settled"] for r in rows):
        lines += [
            "",
            "!! The UNSETTLED bar is an intraday reading and WILL revise. Never write it",
            "!! to a news.md entry as a close - that is the exact error this script exists",
            "!! to prevent (see the 2026-07-27 correction in tickers/COHR/news.md).",
        ]
    return "\n".join(lines)


def watch_list() -> list[str]:
    return sorted(d.name for d in ticker_dirs())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Settled daily price bars for watched tickers (stdlib only, no API key).",
    )
    ap.add_argument("ticker", nargs="?", help="Watch-list ticker, e.g. COHR")
    ap.add_argument("--all", action="store_true", help="Latest settled close for every watched ticker")
    ap.add_argument("--range", default="1mo", help="Yahoo range: 5d, 1mo, 3mo, 6mo, 1y (default 1mo)")
    ap.add_argument("--since", help="Only show bars on/after this YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="Emit JSON (settled bars only unless --include-live)")
    ap.add_argument("--include-live", action="store_true", help="Include the unsettled current-session bar in --json")
    args = ap.parse_args(argv)

    if not args.ticker and not args.all:
        ap.error("give a TICKER or --all")

    if args.all:
        out, failures = {}, []
        for tk in watch_list():
            try:
                rows, meta = bars(fetch(tk, rng="5d"))
            except PriceError as exc:
                failures.append(str(exc))
                continue
            settled = [r for r in rows if r["settled"]]
            if settled:
                out[tk] = {
                    "symbol": yahoo_symbol(tk),
                    "currency": meta.get("currency"),
                    **{k: settled[-1][k] for k in ("date", "close") if k in settled[-1]},
                    "pct": round(settled[-1].get("pct", 0.0), 4) if "pct" in settled[-1] else None,
                }
        if args.json:
            print(json.dumps({"prices": out, "errors": failures}, indent=2))
        else:
            print(f"{'ticker':<8}{'date':<12}{'close':>11}{'chg':>10}  ccy")
            print("-" * 48)
            for tk, row in out.items():
                pct = f"{row['pct']:+.2f}%" if row.get("pct") is not None else ""
                print(f"{tk:<8}{row['date']:<12}{row['close']:>11.2f}{pct:>10}  {row.get('currency') or ''}")
            for f in failures:
                print(f"  ! {f}", file=sys.stderr)
        return 1 if failures and not out else 0

    try:
        rows, meta = bars(fetch(args.ticker, rng=args.range))
    except PriceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.since:
        rows = [r for r in rows if r["date"] >= args.since]
    if args.json:
        emit = rows if args.include_live else [r for r in rows if r["settled"]]
        print(json.dumps(
            {
                "ticker": args.ticker.upper(),
                "symbol": yahoo_symbol(args.ticker),
                "currency": meta.get("currency"),
                "exchange": meta.get("fullExchangeName") or meta.get("exchangeName"),
                "bars": emit,
            },
            indent=2,
        ))
    else:
        print(render(args.ticker.upper(), rows, meta, None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
