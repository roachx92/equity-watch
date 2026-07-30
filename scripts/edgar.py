#!/usr/bin/env python3
"""SEC filing index for a watched ticker — stdlib only, no API key.

Why this exists: research passes kept reporting "EDGAR returned HTTP 403, so the
filing-absence claim rests on aggregator indices, not a direct check." That
caveat appeared twice in the 2026-07-29 COHR run alone, on the two Tripwires
(#1 cash conversion, #2 customer concentration) that *resolve on filings*.

EDGAR was never blocking us. `data.sec.gov` returns 403 only when the request
carries **no User-Agent**; the SEC's fair-access policy asks callers to identify
themselves, and an unidentified request is refused. Send any UA and it answers
normally. So the fix is a header, not a workaround, and the whole class of
"couldn't verify from primary source" caveat goes away.

Set `EDGAR_IDENTITY` to "Name email@example.com" per the SEC's stated policy.
There is no signup and no key.

For rich XBRL work (parsed statements, typed objects) an `edgartools` MCP server
is configured in `.mcp.json` for interactive sessions. This module deliberately
stays stdlib so it also runs inside the GitHub Actions workflows, which invoke
`scripts/` with no pip install step.

Usage:
    python scripts/edgar.py COHR                      # recent filings
    python scripts/edgar.py COHR --since 2026-07-27   # did anything file in the window?
    python scripts/edgar.py COHR --forms 8-K,10-Q,10-K
    python scripts/edgar.py COHR --json

Not financial advice — informational research tooling only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
_FILING_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/{doc}"

#: The SEC asks callers to identify themselves. An unidentified request is the
#: documented cause of the 403s this module exists to stop hitting.
_FALLBACK_UA = "equity-watch (https://github.com/roachx92/equity-watch)"

#: Watch-list tickers with no SEC filing history, so a "no filings" result is
#: correctly reported as "not an SEC filer" rather than an empty window.
NON_SEC_FILERS = {
    "LPKF": "German (Xetra: LPK) - files with the Bundesanzeiger, not EDGAR",
}


class EdgarError(RuntimeError):
    """Fetch or resolution failure, with a message safe to show a human."""


def identity() -> str:
    return os.environ.get("EDGAR_IDENTITY") or _FALLBACK_UA


def _get(url: str, timeout: int = 25):
    req = urllib.request.Request(url, headers={"User-Agent": identity()})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            raise EdgarError(
                "SEC returned 403 - the request was not identified. Set EDGAR_IDENTITY "
                "to 'Your Name your@email.com' (no signup, no API key)."
            ) from exc
        if exc.code == 404:
            raise EdgarError(f"SEC returned 404 for {url}") from exc
        raise EdgarError(f"SEC returned HTTP {exc.code} for {url}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise EdgarError(f"network error reaching SEC - {exc}") from exc
    except json.JSONDecodeError as exc:
        raise EdgarError(f"malformed JSON from {url}") from exc


def resolve_cik(ticker: str) -> int:
    """Map a ticker symbol to its SEC CIK."""
    ticker = ticker.upper()
    data = _get(_TICKERS_URL)
    # Shape: {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
    for row in data.values():
        if str(row.get("ticker", "")).upper() == ticker:
            return int(row["cik_str"])
    raise EdgarError(
        f"{ticker}: no CIK on SEC's ticker index - it may not be an SEC filer "
        f"(foreign listings often are not)."
    )


def filings(ticker: str, since: str | None = None, forms: list[str] | None = None,
            limit: int = 40) -> tuple[list[dict], dict]:
    """Return (filings, company_meta), most recent first."""
    cik = resolve_cik(ticker)
    sub = _get(_SUBMISSIONS.format(cik=cik))
    recent = (sub.get("filings") or {}).get("recent") or {}

    cols = ("filingDate", "form", "accessionNumber", "primaryDocument",
            "reportDate", "primaryDocDescription")
    series = {c: recent.get(c) or [] for c in cols}
    n = len(series["filingDate"])

    wanted = {f.strip().upper() for f in forms} if forms else None
    out: list[dict] = []
    for i in range(n):
        date = series["filingDate"][i]
        form = series["form"][i]
        if since and date < since:
            continue
        if wanted and form.upper() not in wanted:
            continue
        acc = series["accessionNumber"][i] or ""
        doc = series["primaryDocument"][i] or ""
        out.append({
            "date": date,
            "form": form,
            "accession": acc,
            "report_date": series["reportDate"][i] if series["reportDate"] else None,
            "description": series["primaryDocDescription"][i] if series["primaryDocDescription"] else None,
            "url": _FILING_URL.format(cik=cik, acc_nodash=acc.replace("-", ""), doc=doc) if acc and doc else None,
        })
        if len(out) >= limit:
            break

    meta = {
        "cik": cik,
        "name": sub.get("name"),
        "sic_description": sub.get("sicDescription"),
        "fiscal_year_end": sub.get("fiscalYearEnd"),
        "exchanges": sub.get("exchanges"),
    }
    return out, meta


def render(ticker: str, rows: list[dict], meta: dict, since: str | None) -> str:
    head = f"{ticker} | {meta.get('name')} (CIK {meta.get('cik')})"
    lines = [head, ""]
    if not rows:
        window = f" on/after {since}" if since else ""
        lines.append(f"No filings{window}. Verified directly against data.sec.gov "
                     f"(not an aggregator index).")
        return "\n".join(lines)
    lines.append(f"{'filed':<12}{'form':<14}{'period':<12}accession")
    lines.append("-" * 66)
    for r in rows:
        lines.append(f"{r['date']:<12}{r['form']:<14}{(r['report_date'] or ''):<12}{r['accession']}")
    if since:
        lines += ["", f"{len(rows)} filing(s) on/after {since}."]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="SEC filing index for a watched ticker (stdlib only, no API key).")
    ap.add_argument("ticker")
    ap.add_argument("--since", help="Only filings on/after this YYYY-MM-DD")
    ap.add_argument("--forms", help="Comma-separated form filter, e.g. 8-K,10-Q,10-K,4")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    tk = args.ticker.upper()
    if tk in NON_SEC_FILERS:
        msg = f"{tk}: not an SEC filer - {NON_SEC_FILERS[tk]}"
        if args.json:
            print(json.dumps({"ticker": tk, "sec_filer": False, "reason": NON_SEC_FILERS[tk]}, indent=2))
        else:
            print(msg)
        return 0

    forms = args.forms.split(",") if args.forms else None
    try:
        rows, meta = filings(tk, since=args.since, forms=forms, limit=args.limit)
    except EdgarError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"ticker": tk, "sec_filer": True, **meta, "filings": rows}, indent=2))
    else:
        print(render(tk, rows, meta, args.since))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
