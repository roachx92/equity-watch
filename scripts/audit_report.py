#!/usr/bin/env python3
"""Staleness audit — the deterministic tier (Section J).

Answers one question per ticker: has the world moved far enough since the dated
deep-dive report that the report should be revisited? Computes only what can be
derived from the repo, then either clears the ticker or escalates it to the
bounded judgment (LLM) pass. That escalation gate is what makes this cheap
enough to run on every push.

This tier **clears or escalates — it does not conclude**. That is the whole
two-tier design, and the boundary is load-bearing:

  CLEAN          — nothing to do. Record the check.
  REFRESH        — facts stale (quarters reported, age + unincorporated items).
                   Pure counting, no judgment, so this tier may issue it.
  RE-UNDERWRITE  — a tripwire tag *explicitly says* `fires`. A prior run already
                   made that assessment against the pre-committed trigger, so
                   this tier is relaying a determination, not inferring one.
  ESCALATE       — pressure accumulated, but deciding what it *means* needs the
                   judgment tier. Never a final answer.

`[EDGE−]` accumulation routes to ESCALATE, not RE-UNDERWRITE, and the live
corpus shows why. Both of CIFR's `[EDGE−]` entries say in their own text that
the Edge's *core* was corroborated — one states "The Edge's skeptical core is
corroborated, not weakened" — because that Edge is two-sided ("either the
bullish variant … or the bearish variant … pick a side"), so an item can cut
against one branch while confirming the thesis. Counting the tags says
"disconfirmation accumulated"; only reading them says whether the Edge is
*pressured* or *falsified*, and only the Step 4b diff against a freshly
re-derived §18 proves it actually changed. A count is a proxy for pressure —
never evidence of change.

PATCH is deliberately absent: it requires the judgment tier's contradiction
check ("was this claim wrong *when written*?"), which no script can answer.

Two properties this file must keep, because other things depend on them:

  * **Stateless and idempotent.** Every signal is recomputed from repo state on
    each run and nothing is written back. The deep-dive re-run path calls this
    live to build a report's provenance block (the audit's own outputs are
    ephemeral by design), so a second invocation must agree with the first.
  * **No second tag parser.** Polarity comes from `tickerlib.parse_assessment_tags`,
    the same classifier the linter uses. A private copy here would drift and
    silently re-acquire the false-positive bug this tier exists to avoid —
    `[TRIPWIRE #4 — reaffirmed, does not fire]` must never read as fired.

Exit status is about *hygiene*, not staleness: a stale report is a decision for
a human, not a failure. Only canonical-link drift exits non-zero.

Python 3 stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import (  # noqa: E402
    canonical_report_date,
    entry_date,
    latest_report_date,
    log_entries,
    parse_assessment_tags,
    ticker_dirs,
)

#: A report older than this stops being coverable by a targeted work order:
#: "no logged news in area X" is a proxy for "X is current", and the proxy
#: decays. Past the horizon a refresh re-runs all four work-streams. Judgment
#: number, tuned with use — not derived.
STALENESS_HORIZON_DAYS = 180

#: Fires REFRESH on its own. Two reported quarters is enough for the business to
#: have moved in ways the report predates.
QUARTERS_FOR_REFRESH = 2

#: With unincorporated items present, this much age routes to REFRESH.
AGE_FOR_REFRESH_DAYS = 90

#: Accumulated disconfirmation worth a human/LLM look. §F states that an
#: accumulation of EDGE− means the differentiated thesis is failing even with no
#: tripwire fired — but the tag is binary while an Edge can be two-sided, so this
#: threshold escalates for judgment rather than concluding.
EDGE_NEG_FOR_ESCALATION = 2

#: Framework tag fragment → the sub-agent work-stream that owns it. Used only to
#: *suggest* a work order; the vocabulary is open and has drifted, so the
#: judgment tier owns the real mapping (Section J). Lowercase substring match.
WORK_STREAM_HINTS = (
    ("financial", "filing"),
    ("capital stack", "filing"),
    ("management", "filing"),
    ("insider", "filing"),
    ("risk", "counterparty"),
    ("concentration", "counterparty"),
    ("counterparty", "counterparty"),
    ("moat", "competitive-landscape"),
    ("competition", "competitive-landscape"),
    ("tech moat", "competitive-landscape"),
    ("sentiment", "sector"),
    ("catalyst", "sector"),
    ("secular", "sector"),
    ("valuation", "sector"),
)


def _days_between(iso_start: str, today: date) -> int:
    return (today - datetime.strptime(iso_start, "%Y-%m-%d").date()).days


def _quarters_since(debrief: Path, baseline: str) -> int:
    """Count `## <period> — reported <date>` headings dated after the baseline."""
    if not debrief.is_file():
        return 0
    count = 0
    for line in debrief.read_text(encoding="utf-8").splitlines():
        if not line.startswith("## "):
            continue
        for token in line.replace("—", " ").split():
            token = token.strip("()[],")
            if len(token) == 10 and token[4] == "-" and token > baseline:
                count += 1
                break
    return count


def _work_streams(tags: list[str]) -> list[str]:
    """Suggested agent set for the framework tags on the stale entries."""
    found = []
    for tag in tags:
        low = tag.lower()
        for fragment, stream in WORK_STREAM_HINTS:
            if fragment in low and stream not in found:
                found.append(stream)
    return sorted(found)


def audit_ticker(ticker_dir: Path, today: date, baseline: str | None = None) -> dict:
    """Every deterministic signal for one ticker, plus the routed verdict."""
    symbol = ticker_dir.name
    news = ticker_dir / "news.md"
    result: dict = {"ticker": symbol, "verdict": "CLEAN", "notify": False,
                    "evidence": [], "work_streams": [], "drift": None}

    if not news.is_file():
        result.update(verdict="NOT-COVERED", notify=True,
                      evidence=["no news.md — invisible to every workflow"])
        return result

    text = news.read_text(encoding="utf-8")
    on_disk = latest_report_date(ticker_dir)
    if on_disk is None:
        result.update(verdict="NOT-COVERED", notify=True,
                      evidence=["no dated report — nothing to audit against"])
        return result

    # The link is a written pointer and can go stale; the glob is the resolver
    # (CLAUDE.md). Disagreement is a real hygiene error, not a staleness signal.
    linked = canonical_report_date(text)
    if linked and linked != on_disk:
        result["drift"] = {"linked": linked, "latest": on_disk}

    # A pinned baseline is not necessarily the report's own date. Keep the two
    # distinguishable: the evidence strings get quoted into a report's
    # provenance block, so "the report is 199d old" must not be asserted about
    # a date the caller supplied.
    base = baseline or on_disk
    pinned = baseline is not None and baseline != on_disk
    result["baseline"] = base
    result["baseline_source"] = "pinned" if pinned else "latest-report"
    result["latest_report"] = on_disk
    age = _days_between(base, today)
    result["age_days"] = age
    span = (f"{age}d of history since pinned baseline {base}" if pinned
            else f"report is {age}d old")

    fired: list[int | None] = []
    early: list[int | None] = []
    edge_neg = edge_pos = 0
    stale_tags: list[str] = []
    unincorporated = 0

    for _, line in log_entries(text):
        when = entry_date(line)
        if when is None or when <= base:
            continue
        unincorporated += 1
        # Framework tag is the first bracket after the date — used for the
        # work-order hint only.
        if "[" in line:
            head = line.split("[", 1)[1].split("]", 1)[0]
            stale_tags.append(head)
        for tag in parse_assessment_tags(line):
            if tag["kind"] == "EDGE":
                if tag["polarity"] == "negative":
                    edge_neg += 1
                elif tag["polarity"] == "positive":
                    edge_pos += 1
            elif tag["polarity"] == "fired":
                fired.append(tag["number"])
            elif tag["polarity"] == "early-warning":
                early.append(tag["number"])

    quarters = _quarters_since(ticker_dir / "earnings-debrief.md", base)
    result.update(unincorporated=unincorporated, edge_neg=edge_neg,
                  edge_pos=edge_pos, quarters_since=quarters,
                  tripwires_fired=fired, tripwires_early_warning=early)

    ev = result["evidence"]

    # --- routing -----------------------------------------------------------
    if fired:
        names = ", ".join(f"#{n}" if n else "#?" for n in fired)
        ev.append(f"tripwire {names} FIRED since {base} — pre-committed action is due")
        result["verdict"] = "RE-UNDERWRITE"
    elif edge_neg >= EDGE_NEG_FOR_ESCALATION:
        ev.append(f"{edge_neg} [EDGE−] since {base} (vs {edge_pos} [EDGE+]) — "
                  "disconfirmation accumulating; judgment tier must read the "
                  "entries and decide pressured vs. falsified (a count cannot)")
        result["verdict"] = "ESCALATE"
        result["escalation_question"] = (
            "Is the Edge genuinely falsified, or merely pressured? Read each "
            "[EDGE−] entry in full — a two-sided Edge can be corroborated at its "
            "core by an item that cuts against one of its branches."
        )
    elif quarters >= QUARTERS_FOR_REFRESH:
        ev.append(f"{quarters} quarters reported since {base}, absent from the report")
        result["verdict"] = "REFRESH"
    elif age >= AGE_FOR_REFRESH_DAYS and unincorporated:
        ev.append(f"{span} with {unincorporated} unincorporated items")
        result["verdict"] = "REFRESH"

    # early-warning never escalates the route, but always breaks the silence
    if early:
        names = ", ".join(f"#{n}" if n else "#?" for n in early)
        ev.append(f"tripwire {names} early-warning — approaching, not tripped")

    if result["verdict"] == "REFRESH":
        if age >= STALENESS_HORIZON_DAYS:
            result["work_streams"] = ["filing", "counterparty", "sector",
                                      "competitive-landscape"]
            ev.append(f"past the {STALENESS_HORIZON_DAYS}d staleness horizon — "
                      "absence of logged news no longer evidences currency; all four run")
        else:
            result["work_streams"] = _work_streams(stale_tags)

    result["notify"] = bool(result["verdict"] != "CLEAN" or early)
    return result


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:  # pragma: no cover - very old Python
            pass

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ticker", help="audit one symbol instead of the watch-list")
    ap.add_argument("--baseline", metavar="YYYY-MM-DD",
                    help="pin the comparison date instead of the latest report "
                         "on disk — required by the refresh path, which must ask "
                         "'what happened since the report I am replacing?'")
    ap.add_argument("--today", metavar="YYYY-MM-DD", help="override today (tests)")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    today = (datetime.strptime(args.today, "%Y-%m-%d").date() if args.today
             else date.today())

    dirs = ticker_dirs()
    if args.ticker:
        dirs = [d for d in dirs if d.name.upper() == args.ticker.upper()]
        if not dirs:
            print(f"no such ticker: {args.ticker}", file=sys.stderr)
            return 2

    results = [audit_ticker(d, today, args.baseline) for d in dirs]

    if args.as_json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Staleness audit — {today}")
        if args.baseline:
            print(f"⚠ BASELINE PINNED to {args.baseline} — ages and evidence below are "
                  "measured from that date, NOT from each report's own date.")
        print()
        width = max((len(r["ticker"]) for r in results), default=6)
        for r in results:
            bell = "!" if r["notify"] else " "
            age = f"{r.get('age_days', '?')}d"
            mark = "*" if r.get("baseline_source") == "pinned" else " "
            print(f"{bell} {r['ticker']:<{width}}  {r['verdict']:<14} {age:>6}"
                  f"  base {r.get('baseline', '—')}{mark}")
            for line in r["evidence"]:
                print(f"    · {line}")
            if r["work_streams"]:
                print(f"    → dispatch: {', '.join(r['work_streams'])}")
            if r["drift"]:
                print(f"    ⚠ canonical link says {r['drift']['linked']}, "
                      f"latest on disk is {r['drift']['latest']}")
        posted = sum(1 for r in results if r["notify"])
        print(f"\n{len(results)} audited · {posted} would notify · "
              f"{sum(1 for r in results if r['verdict'] == 'CLEAN')} clean")

    # Staleness is a decision, not a failure. Only hygiene fails the build.
    return 1 if any(r["drift"] for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
