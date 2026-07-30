#!/usr/bin/env python3
"""Cross-ticker coverage: what a slug-peer logged that this ticker has not.

**This surfaces candidates. It never copies an entry between tickers.** That
restraint is the whole design, and it comes straight from `sector-lens.md` §K.5:
impact is *per-ticker and signed*, so the same headline can be `[EDGE+]` for one
name and tripwire-adjacent for another. Copying an assessment across tickers
would be wrong. Surfacing the *event* so each ticker's own §18 assessment can run
is right.

The gap it closes is §K.0's stated failure mode — "an angle nobody searches
produces no entries, and an absence of entries reads exactly like nothing
happened." Today an unlogged event and an assessed-immaterial event are
indistinguishable. Measured on the corpus at the time of writing:

  - AAOI and COHR are both `ai-optics` and were **both researched 2026-07-29**,
    so staleness explains nothing. COHR logged the Microsoft/Meta capex prints;
    AAOI did not. AAOI logged Celestica Q2; COHR did not.
  - Innolight's HK IPO and the 2026-07-27 TrendForce CPO release were each
    researched **twice, independently**, for the two tickers within 48 hours —
    and the two records of the IPO captured *different* facts, so neither log is
    complete and neither reader can tell.

Two report modes:

  gaps        an event a slug-peer logged on a date this ticker has no entry for.
              A candidate to assess, NOT a conclusion that it was missed - the
              §K.6 materiality bar may have correctly excluded it.
  duplicates  the same event logged under two tickers, i.e. paid for twice.

Usage:
    python scripts/crossref.py --ticker AAOI
    python scripts/crossref.py --all
    python scripts/crossref.py --duplicates
    python scripts/crossref.py --all --json

Not financial advice — informational research tooling only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import entry_date, log_entries, sector_slugs, ticker_dirs  # noqa: E402

# Unlike the other scripts here, this one prints *corpus prose* — headlines that
# legitimately carry U+2212 (§F.1 mandates it for `[EDGE−]`), en-dashes and
# Chinese source names. Those cannot be ASCII-ised away, so make stdout carry
# them and degrade rather than crash on a cp1252 console.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - non-reconfigurable stream
        pass

_SECTOR_TAG = re.compile(r"\[Sector/([a-z0-9-]+)\]")
_HEADLINE = re.compile(r"\*\*(.+?)\*\*", re.DOTALL)

#: Token overlap above which two entries on the same date+slug are treated as
#: the same underlying event. Deliberately high: a false "duplicate" claim is
#: worse than missing one, because it invites deleting a real entry.
DUP_THRESHOLD = 0.45

_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "at",
    "from", "by", "its", "it", "as", "is", "are", "was", "were", "be", "been",
    "that", "this", "than", "but", "not", "no", "into", "over", "after", "up",
    "down", "new", "first", "per", "vs", "q1", "q2", "q3", "q4",
}


def _headline(line: str) -> str:
    m = _HEADLINE.search(line)
    return (m.group(1).strip() if m else line[:160]).replace("\n", " ")


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9.'-]{2,}", text.lower())
    return {w.strip(".'-") for w in words if w not in _STOP}


def _similarity(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def index(root: Path | None = None) -> dict:
    """Index every ticker's Recent News Log by (slug, date)."""
    out: dict[str, dict] = {}
    for d in sorted(ticker_dirs(root), key=lambda p: p.name):
        news = d / "news.md"
        if not news.exists():
            continue
        text = news.read_text(encoding="utf-8")
        entries = []
        for _, line in log_entries(text):
            date = entry_date(line)
            if not date:
                continue
            m = _SECTOR_TAG.search(line)
            entries.append({
                "date": date,
                "slug": m.group(1) if m else None,
                "headline": _headline(line),
            })
        out[d.name] = {
            "slugs": sector_slugs(text),
            "entries": entries,
            "newest": max((e["date"] for e in entries), default=None),
            "count": len(entries),
        }
    return out


def peers(idx: dict) -> dict[str, list[str]]:
    """slug -> tickers carrying it (only slugs with more than one member)."""
    by_slug: dict[str, list[str]] = {}
    for tk, rec in idx.items():
        for s in rec["slugs"]:
            by_slug.setdefault(s, []).append(tk)
    return {s: sorted(t) for s, t in by_slug.items() if len(t) > 1}


def gaps_for(ticker: str, idx: dict) -> list[dict]:
    """Events a slug-peer logged on a (slug, date) this ticker has nothing for."""
    ticker = ticker.upper()
    me = idx.get(ticker)
    if not me:
        return []
    shared = peers(idx)
    mine = {(e["slug"], e["date"]) for e in me["entries"]}
    my_dates = {e["date"] for e in me["entries"]}

    found: dict[tuple, dict] = {}
    for slug in me["slugs"]:
        for peer in shared.get(slug, []):
            if peer == ticker:
                continue
            for e in idx[peer]["entries"]:
                if e["slug"] != slug or (slug, e["date"]) in mine:
                    continue
                key = (slug, e["date"], e["headline"][:60])
                found.setdefault(key, {
                    "slug": slug,
                    "date": e["date"],
                    "headline": e["headline"],
                    "logged_by": [],
                    # A date this ticker logged *something* on is weaker evidence
                    # of a miss than one it has no entry for at all.
                    "ticker_active_that_day": e["date"] in my_dates,
                })["logged_by"].append(peer)

    rows = sorted(found.values(), key=lambda r: (r["date"], r["slug"]), reverse=True)
    for r in rows:
        r["logged_by"] = sorted(set(r["logged_by"]))
    return rows


def duplicates(idx: dict, threshold: float = DUP_THRESHOLD) -> list[dict]:
    """The same event logged under two tickers — researched and paid for twice."""
    buckets: dict[tuple, list[tuple[str, dict]]] = {}
    for tk, rec in idx.items():
        for e in rec["entries"]:
            if e["slug"]:
                buckets.setdefault((e["slug"], e["date"]), []).append((tk, e))

    out = []
    for (slug, date), items in buckets.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                (t1, e1), (t2, e2) = items[i], items[j]
                if t1 == t2:
                    continue
                score = _similarity(e1["headline"], e2["headline"])
                if score >= threshold:
                    out.append({
                        "slug": slug, "date": date, "similarity": round(score, 2),
                        "tickers": sorted([t1, t2]),
                        "headlines": {t1: e1["headline"], t2: e2["headline"]},
                    })
    return sorted(out, key=lambda r: (r["date"], -r["similarity"]), reverse=True)


def _trunc(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


def render_gaps(ticker: str, rows: list[dict], idx: dict) -> str:
    rec = idx.get(ticker.upper())
    if rec is None:
        return f"{ticker}: not a watched ticker."
    head = [f"{ticker.upper()} | cross-ticker coverage  (slugs: {', '.join(rec['slugs']) or 'none'};"
            f" {rec['count']} log entries, newest {rec['newest'] or '-'})", ""]
    if not rows:
        return "\n".join(head + ["No slug-peer logged anything this ticker lacks."])
    head.append("Candidates to ASSESS against this ticker's own Edge/Tripwires (K.5) -")
    head.append("not conclusions that anything was missed; the K.6 bar may exclude them.")
    head.append("")
    for r in rows:
        flag = "" if r["ticker_active_that_day"] else "  [no entry at all that day]"
        head.append(f"  {r['date']}  [{r['slug']}]  via {','.join(r['logged_by'])}{flag}")
        head.append(f"      {_trunc(r['headline'], 110)}")
    return "\n".join(head)


def render_dups(rows: list[dict]) -> str:
    if not rows:
        return "No duplicated sector research detected."
    out = [f"Duplicated sector research - the same event logged under two tickers ({len(rows)} pair(s)):", ""]
    for r in rows:
        out.append(f"  {r['date']}  [{r['slug']}]  {' + '.join(r['tickers'])}  (overlap {r['similarity']})")
        for tk in r["tickers"]:
            out.append(f"      {tk}: {_trunc(r['headlines'][tk], 100)}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Cross-ticker sector coverage: gaps and duplicated research.")
    ap.add_argument("--ticker")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--duplicates", action="store_true")
    ap.add_argument("--threshold", type=float, default=DUP_THRESHOLD)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not (args.ticker or args.all or args.duplicates):
        ap.error("give --ticker, --all, or --duplicates")

    idx = index()

    if args.duplicates and not (args.ticker or args.all):
        rows = duplicates(idx, args.threshold)
        print(json.dumps(rows, indent=2) if args.json else render_dups(rows))
        return 0

    targets = sorted(idx) if args.all else [args.ticker.upper()]
    payload = {}
    for tk in targets:
        payload[tk] = gaps_for(tk, idx)

    if args.json:
        out = {"gaps": payload}
        if args.duplicates:
            out["duplicates"] = duplicates(idx, args.threshold)
        print(json.dumps(out, indent=2))
        return 0

    for tk in targets:
        rows = payload[tk]
        if args.all and not rows:
            continue
        print(render_gaps(tk, rows, idx))
        print()
    if args.duplicates:
        print(render_dups(duplicates(idx, args.threshold)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
