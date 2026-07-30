#!/usr/bin/env python3
"""XBRL company facts from SEC EDGAR — stdlib only, no API key.

Why this exists: a ticker's numeric Tripwires are assertions over tagged
financial-statement line items. COHR's #1 is the clearest case — *"full-year
operating cash flow below roughly $300M against ~$700M of capex, OR inventory
fails to decline from $2,126.8M."* Those three quantities are `us-gaap`
concepts. Today they get evaluated by a model reading prose out of a press
release, which is the wrong instrument for a numeric comparison and is how a
figure drifts.

This module returns the tagged value, the period it covers, and the accession
it was filed under, so a tripwire evaluation can cite a filing rather than a
recollection.

**Selection is the subtle part.** `companyconcept` returns the same period many
times — a fiscal year appears in its own 10-K and again as the comparative in
later filings. Rows are therefore keyed on (start, end) and the one with the
latest `filed` date wins, which is also what surfaces a **restatement**: if a
number changes, the newest filing is the truth and the old log entry is stale.

Usage:
    python scripts/facts.py COHR --tag InventoryNet
    python scripts/facts.py COHR --tag NetCashProvidedByUsedInOperatingActivities --annual
    python scripts/facts.py COHR --tag InventoryNet --json

Not financial advice — informational research tooling only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edgar import EdgarError, _get, resolve_cik  # noqa: E402

_CONCEPT = "https://data.sec.gov/api/xbrl/companyconcept/CIK{cik:010d}/{taxonomy}/{tag}.json"

#: Friendly aliases so a checks file and a CLI user need not memorise us-gaap
#: tag spellings. The right-hand side is the actual concept name.
ALIASES = {
    "inventory": "InventoryNet",
    "ocf": "NetCashProvidedByUsedInOperatingActivities",
    "operating_cash_flow": "NetCashProvidedByUsedInOperatingActivities",
    "capex": "PaymentsToAcquirePropertyPlantAndEquipment",
    "revenue": "RevenueFromContractWithCustomerExcludingAssessedTax",
    "cash": "CashAndCashEquivalentsAtCarryingValue",
}


def resolve_tag(tag: str) -> str:
    return ALIASES.get(tag.strip().lower(), tag)


def concept(ticker: str, tag: str, taxonomy: str = "us-gaap") -> dict:
    """Fetch one XBRL concept for `ticker`. Raises EdgarError."""
    tag = resolve_tag(tag)
    cik = resolve_cik(ticker)
    try:
        return _get(_CONCEPT.format(cik=cik, taxonomy=taxonomy, tag=tag))
    except EdgarError as exc:
        if "404" in str(exc):
            raise EdgarError(
                f"{ticker}: no us-gaap concept {tag!r} reported. Either the tag is "
                f"misspelled or this filer does not report it (custom extension tags "
                f"and text-only disclosures are not in companyconcept)."
            ) from exc
        raise


def facts(ticker: str, tag: str, taxonomy: str = "us-gaap") -> tuple[list[dict], str]:
    """Return (deduped facts newest-period-first, unit).

    One row per distinct (start, end) period, keeping the most recently *filed*
    value so restatements win over the original print.
    """
    payload = concept(ticker, tag, taxonomy)
    units = payload.get("units") or {}
    if not units:
        return [], ""
    unit = next(iter(units))

    best: dict[tuple, dict] = {}
    for row in units[unit]:
        end = row.get("end")
        if not end or row.get("val") is None:
            continue
        key = (row.get("start"), end)
        prior = best.get(key)
        if prior is None or (row.get("filed") or "") > (prior.get("filed") or ""):
            best[key] = row

    out = []
    for (start, end), row in best.items():
        out.append({
            "start": start,
            "end": end,
            "val": row["val"],
            "form": row.get("form"),
            "fy": row.get("fy"),
            "fp": row.get("fp"),
            "filed": row.get("filed"),
            "accession": row.get("accn"),
            "frame": row.get("frame"),
            "instantaneous": start is None,
        })
    out.sort(key=lambda r: (r["end"], r["start"] or ""), reverse=True)
    return out, unit


def _months(start: str, end: str) -> int:
    """Approximate month span of a duration fact, for annual/quarterly filtering."""
    sy, sm, sd = (int(x) for x in start.split("-"))
    ey, em, ed = (int(x) for x in end.split("-"))
    return (ey - sy) * 12 + (em - sm) + (1 if ed >= sd else 0)


def select(rows: list[dict], *, annual: bool = False, quarterly: bool = False,
           as_of: str | None = None, period_end: str | None = None) -> list[dict]:
    """Filter facts by period shape and date."""
    out = rows
    if period_end:
        out = [r for r in out if r["end"] == period_end]
    if as_of:
        out = [r for r in out if r["end"] <= as_of]
    if annual:
        out = [r for r in out if r["instantaneous"] or _months(r["start"], r["end"]) >= 11]
    if quarterly:
        out = [r for r in out if r["instantaneous"] or _months(r["start"], r["end"]) <= 4]
    return out


def latest(rows: list[dict]) -> dict | None:
    return rows[0] if rows else None


def _fmt(val, unit: str) -> str:
    if unit == "USD" and abs(val) >= 1_000_000:
        return f"{val/1_000_000:,.1f}M"
    return f"{val:,}"


def render(ticker: str, tag: str, rows: list[dict], unit: str, limit: int) -> str:
    if not rows:
        return f"{ticker}: no facts for {resolve_tag(tag)}."
    lines = [
        f"{ticker} | {resolve_tag(tag)} ({unit})",
        "",
        f"{'period':<26}{'value':>16}  {'form':<7}{'filed':<12}accession",
        "-" * 84,
    ]
    for r in rows[:limit]:
        period = r["end"] if r["instantaneous"] else f"{r['start']} -> {r['end']}"
        lines.append(
            f"{period:<26}{_fmt(r['val'], unit):>16}  "
            f"{str(r['form']):<7}{str(r['filed']):<12}{r['accession']}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="XBRL company facts from SEC EDGAR (stdlib only, no API key).")
    ap.add_argument("ticker")
    ap.add_argument("--tag", required=True,
                    help=f"us-gaap concept or alias ({', '.join(sorted(ALIASES))})")
    ap.add_argument("--taxonomy", default="us-gaap")
    ap.add_argument("--annual", action="store_true", help="Only ~annual duration facts")
    ap.add_argument("--quarterly", action="store_true", help="Only ~quarterly duration facts")
    ap.add_argument("--as-of", help="Only periods ending on/before YYYY-MM-DD")
    ap.add_argument("--period-end", help="Exact period end YYYY-MM-DD")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        rows, unit = facts(args.ticker, args.tag, args.taxonomy)
    except EdgarError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rows = select(rows, annual=args.annual, quarterly=args.quarterly,
                  as_of=args.as_of, period_end=args.period_end)
    if args.json:
        print(json.dumps({
            "ticker": args.ticker.upper(),
            "tag": resolve_tag(args.tag),
            "unit": unit,
            "facts": rows[:args.limit],
        }, indent=2))
    else:
        print(render(args.ticker.upper(), args.tag, rows, unit, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
