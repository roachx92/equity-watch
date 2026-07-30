#!/usr/bin/env python3
"""Evaluate the NUMERIC half of a ticker's Tripwires against XBRL — stdlib only.

**This computes; it does not decide.** The prose Tripwires in `news.md` are the
binding pre-commitment (`standing-rules.md`, "The pre-committed Edge &
Tripwires"). A `tickers/<T>/checks.json` encodes only the machine-checkable
numeric clauses so the audit's deterministic tier can produce a value with a
filing citation, instead of a model reading a figure out of a press release.
If the encoding and the prose ever disagree, **the prose wins and the
disagreement is the finding.**

Three things keep this from quietly becoming the source of truth:

1. **Hedged thresholds return INCONCLUSIVE, not a verdict.** COHR's #1 says
   "below *roughly* $300M". A run that answers `FIRES` at $299M and
   `DOES NOT FIRE` at $301M has invented a precision the human never committed
   to. Inside the hedge band (default 5%) the result is `INCONCLUSIVE` and
   routes to the judgment tier, which is what the prose actually implies.
2. **`context` clauses are reported, never evaluated.** Where a trigger's text
   is ambiguous about whether something is a condition, it is recorded as
   context so the script cannot invent a condition nobody committed to.
3. **A trigger with no evaluable clauses reports `MANUAL`, never `CLEAN`.**
   COHR's #2 turns on customer concentration, which is a narrative footnote and
   carries no us-gaap tag. Silence there must not read as "checked and clear."

Verdicts map onto the closed vocabulary in `latest-updates-workflow.md` §F.1:
    FIRES         -> [TRIPWIRE #n - fires]
    DOES NOT FIRE -> [TRIPWIRE #n - does not fire]
    INCONCLUSIVE  -> judgment tier (hedge band, or the period has not been filed)
    MANUAL        -> not machine-checkable at all; a human must read the filing

Usage:
    python scripts/tripwire_check.py COHR
    python scripts/tripwire_check.py COHR --json
    python scripts/tripwire_check.py --all

Not financial advice — informational research tooling only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edgar import EdgarError  # noqa: E402
from facts import facts, select  # noqa: E402
from tickerlib import repo_root, ticker_dirs  # noqa: E402

DEFAULT_HEDGE = 0.05

FIRES, NOT_FIRED, INCONCLUSIVE, MANUAL = "FIRES", "DOES NOT FIRE", "INCONCLUSIVE", "MANUAL"

_OPS = {
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
}


class CheckError(RuntimeError):
    pass


def checks_path(ticker: str) -> Path:
    return repo_root() / "tickers" / ticker.upper() / "checks.json"


def load_checks(ticker: str) -> dict | None:
    p = checks_path(ticker)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CheckError(f"{ticker}: checks.json is not valid JSON — {exc}") from exc


def fy_bounds(fiscal_year: int, fiscal_year_end: str) -> tuple[str, str]:
    """(start, end) ISO dates for a fiscal year labelled by its END year."""
    mm, dd = (int(x) for x in fiscal_year_end.split("-"))
    end = f"{fiscal_year:04d}-{mm:02d}-{dd:02d}"
    start_year = fiscal_year - 1 if (mm, dd) != (12, 31) else fiscal_year
    start_mm, start_dd = (1, 1) if (mm, dd) == (12, 31) else (mm % 12 + 1, 1)
    return f"{start_year:04d}-{start_mm:02d}-{start_dd:02d}", end


def _pick(rows: list[dict], period: str, fy_end: str) -> dict | None:
    """Choose the fact matching the clause's period shape and fiscal-year end."""
    if period == "instant":
        exact = [r for r in rows if r["instantaneous"] and r["end"] == fy_end]
        return exact[0] if exact else None
    annual = select(rows, annual=True)
    exact = [r for r in annual if r["end"] == fy_end and not r["instantaneous"]]
    return exact[0] if exact else None


def evaluate_clause(ticker: str, clause: dict, fy_end: str, hedge: float) -> dict:
    tag = clause["tag"]
    try:
        rows, unit = facts(ticker, tag)
    except EdgarError as exc:
        return {**_clause_stub(clause), "verdict": INCONCLUSIVE, "reason": str(exc)}

    fact = _pick(rows, clause.get("period", "annual"), fy_end)
    if fact is None:
        return {
            **_clause_stub(clause),
            "verdict": INCONCLUSIVE,
            "reason": f"no {clause.get('period','annual')} fact ending {fy_end} filed yet",
        }

    val, thr, op = fact["val"], clause["threshold"], clause["op"]
    hit = _OPS[op](val, thr)
    band = abs(thr) * (hedge if clause.get("hedged") else 0.0)
    inside_band = band > 0 and abs(val - thr) <= band

    if inside_band:
        verdict = INCONCLUSIVE
        reason = (f"within the +/-{hedge:.0%} hedge band of a threshold the trigger "
                  f"states as approximate - a judgment call, not arithmetic")
    else:
        verdict = FIRES if hit else NOT_FIRED
        reason = f"{val:,} {op} {thr:,} is {hit}"

    return {
        **_clause_stub(clause),
        "verdict": verdict,
        "reason": reason,
        "value": val,
        "unit": unit,
        "period": fact["end"] if fact["instantaneous"] else f"{fact['start']} -> {fact['end']}",
        "form": fact["form"],
        "filed": fact["filed"],
        "accession": fact["accession"],
        "distance_pct": round((val - thr) / thr * 100, 2) if thr else None,
    }


def _clause_stub(clause: dict) -> dict:
    return {
        "id": clause.get("id"),
        "label": clause.get("label"),
        "tag": clause.get("tag"),
        "threshold": clause.get("threshold"),
        "op": clause.get("op"),
        "hedged": bool(clause.get("hedged")),
    }


def fetch_context(ticker: str, item: dict, fy_end: str) -> dict:
    """Context is reported, never evaluated — see the module docstring."""
    out = {"id": item.get("id"), "label": item.get("label"), "note": item.get("note")}
    try:
        rows, unit = facts(ticker, item["tag"])
    except EdgarError as exc:
        return {**out, "value": None, "reason": str(exc)}
    fact = _pick(rows, item.get("period", "annual"), fy_end)
    if fact is None:
        return {**out, "value": None, "reason": f"no fact ending {fy_end} filed yet"}
    return {
        **out,
        "value": fact["val"],
        "unit": unit,
        "period": fact["end"] if fact["instantaneous"] else f"{fact['start']} -> {fact['end']}",
        "accession": fact["accession"],
    }


def combine(clause_results: list[dict], fires_when: str) -> str:
    if fires_when == "manual" or not clause_results:
        return MANUAL
    verdicts = [c["verdict"] for c in clause_results]
    if fires_when == "any":
        if FIRES in verdicts:
            return FIRES
        if INCONCLUSIVE in verdicts:
            return INCONCLUSIVE
        return NOT_FIRED
    # "all"
    if all(v == FIRES for v in verdicts):
        return FIRES
    if INCONCLUSIVE in verdicts:
        return INCONCLUSIVE
    return NOT_FIRED


def run(ticker: str, hedge: float = DEFAULT_HEDGE) -> dict:
    cfg = load_checks(ticker)
    if cfg is None:
        return {"ticker": ticker.upper(), "checks": None,
                "note": "no checks.json - numeric tripwire evaluation not configured"}

    fye = cfg.get("fiscal_year_end", "12-31")
    results = []
    for chk in cfg.get("checks", []):
        _, fy_end = fy_bounds(int(chk["fiscal_year"]), fye)
        clauses = [evaluate_clause(ticker, c, fy_end, hedge) for c in chk.get("clauses", [])]
        context = [fetch_context(ticker, c, fy_end) for c in chk.get("context", [])]
        results.append({
            "tripwire": chk["tripwire"],
            "name": chk.get("name"),
            "quote": chk.get("quote"),
            "fiscal_year": chk["fiscal_year"],
            "fiscal_year_end": fy_end,
            "verdict": combine(clauses, chk.get("fires_when", "any")),
            "clauses": clauses,
            "context": context,
        })
    return {"ticker": ticker.upper(), "fiscal_year_end": fye, "checks": results}


def _m(v, unit="USD"):
    if v is None:
        return "n/a"
    return f"${v/1_000_000:,.1f}M" if unit == "USD" else f"{v:,}"


def render(res: dict) -> str:
    if res.get("checks") is None:
        return f"{res['ticker']}: {res['note']}"
    lines = [f"{res['ticker']} | numeric tripwire checks",
             "(computed aid - the prose Tripwires in news.md remain binding)", ""]
    for c in res["checks"]:
        lines.append(f"Tripwire #{c['tripwire']} - {c['name']}  =>  {c['verdict']}")
        lines.append(f"  FY{c['fiscal_year']} (ends {c['fiscal_year_end']})")
        for cl in c["clauses"]:
            val = _m(cl.get("value"), cl.get("unit", "USD"))
            thr = _m(cl.get("threshold"))
            dist = f"  [{cl['distance_pct']:+.1f}% vs threshold]" if cl.get("distance_pct") is not None else ""
            lines.append(f"    - {cl['label']}")
            lines.append(f"        {cl['verdict']}: {val} {cl.get('op','')} {thr}{dist}")
            if cl.get("accession"):
                lines.append(f"        source: {cl['form']} {cl['accession']} filed {cl['filed']} ({cl['period']})")
            if cl["verdict"] in (INCONCLUSIVE, MANUAL):
                lines.append(f"        why: {cl.get('reason')}")
        for cx in c["context"]:
            lines.append(f"    ~ context (reported, not evaluated): {cx['label']}")
            lines.append(f"        {_m(cx.get('value'), cx.get('unit','USD'))}"
                         + (f"  [{cx.get('accession')}]" if cx.get("accession") else "")
                         + (f"  ({cx.get('reason')})" if cx.get("reason") else ""))
        if c["verdict"] == MANUAL:
            lines.append("    !! MANUAL - not machine-checkable; a human must read the filing.")
            lines.append("       Absence of a numeric result here is NOT 'checked and clear'.")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Evaluate the numeric half of a ticker's Tripwires against XBRL.")
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--hedge", type=float, default=DEFAULT_HEDGE,
                    help="Fractional band around a hedged threshold (default 0.05)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.ticker and not args.all:
        ap.error("give a TICKER or --all")

    targets = sorted(d.name for d in ticker_dirs()) if args.all else [args.ticker.upper()]
    out = []
    for tk in targets:
        try:
            out.append(run(tk, args.hedge))
        except CheckError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(out if args.all else out[0], indent=2))
    else:
        for res in out:
            if args.all and res.get("checks") is None:
                continue
            print(render(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
