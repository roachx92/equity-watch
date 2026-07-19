#!/usr/bin/env python3
"""Decide what the staleness audit should *say*, and post it (Section J.5).

Split from `audit_report.py` on purpose. The audit computation must stay
**stateless and idempotent** — the deep-dive refresh path re-runs it live to
build a provenance block, so it may never depend on or write history. Noise
control does need history (don't re-nag the same verdict for ~30 days), so it
lives here, in the reporting layer, exactly as §J.5 requires: separate how often
the audit *runs* from how often it *speaks*.

Reads `audit_report.py --json`, decides per ticker whether this verdict is worth
a message, posts the ones that are to their own channels via
`notify_discord_ticker.py`, and writes a roll-up for the sweep's channel.

Suppression rules:
  * Silent when CLEAN and nothing forced a notify.
  * A verdict already reported within the window is suppressed — UNLESS it
    **escalated** (CLEAN → ESCALATE → REFRESH → RE-UNDERWRITE), which always
    speaks.
  * State lives in the Actions cache and is evictable by design. Eviction costs
    at worst one duplicate nudge, which is the right way to be wrong.

Python 3 stdlib only.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent

#: Ascending severity. A move *up* this ladder always speaks, even inside the
#: suppression window — that is the whole point of the exception.
SEVERITY = ["CLEAN", "ESCALATE", "REFRESH", "RE-UNDERWRITE", "NOT-COVERED"]

DEFAULT_WINDOW_DAYS = 30


def _rank(verdict: str) -> int:
    return SEVERITY.index(verdict) if verdict in SEVERITY else 0


def load_state(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # A corrupt cache must never fail the audit; worst case we re-nag once.
        return {}


def should_notify(result: dict, prior: dict | None, today: date,
                  window_days: int = DEFAULT_WINDOW_DAYS) -> tuple[bool, str]:
    """(post?, why) for one ticker's result against what was last reported."""
    if not result.get("notify"):
        return False, "clean and nothing forced a notify"

    if prior is None:
        return True, "first report of this verdict"

    if _rank(result["verdict"]) > _rank(prior.get("verdict", "CLEAN")):
        return True, f"escalated from {prior.get('verdict')}"

    if result["verdict"] != prior.get("verdict"):
        return True, f"verdict changed from {prior.get('verdict')}"

    try:
        last = datetime.strptime(prior["last_posted"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return True, "no usable last-posted date on record"

    if today - last >= timedelta(days=window_days):
        return True, f"window elapsed ({(today - last).days}d)"

    return False, f"same verdict, re-nag suppressed ({(today - last).days}d ago)"


def render_ticker_message(r: dict) -> str:
    """The per-ticker Discord body: verdict, dated evidence, exact command."""
    lines = [f"**{r['ticker']} — {r['verdict']}**", ""]
    for ev in r.get("evidence", []):
        lines.append(f"· {ev}")
    if r.get("work_streams"):
        lines.append("")
        lines.append(f"**Work order:** {', '.join(r['work_streams'])}")
    if r.get("escalation_question"):
        lines.append("")
        lines.append(f"**Judgment needed:** {r['escalation_question']}")
    if r.get("drift"):
        lines.append("")
        lines.append(f"⚠ Canonical link says {r['drift']['linked']}, "
                     f"latest on disk is {r['drift']['latest']}")

    lines.append("")
    verdict = r["verdict"]
    if verdict in ("REFRESH", "RE-UNDERWRITE", "ESCALATE"):
        # §J.1: the audit recommends, a human dispatches. Give the exact command
        # so the decision is an approval, not an investigation.
        lines.append(f"**Run:** `/deep-dive {r['ticker']}`")
        if r.get("baseline"):
            lines.append(f"_The re-run will re-derive this audit against baseline "
                         f"{r['baseline']} and record it in the report's provenance "
                         f"block. Edge/Tripwires in news.md are not touched until you "
                         f"promote them._")
    elif verdict == "NOT-COVERED":
        lines.append(f"**Run:** `/deep-dive {r['ticker']}` — no report to audit against.")
    return "\n".join(lines)


def render_rollup(results: list[dict], decisions: dict, today: date) -> str:
    """Repo-wide table for the sweep channel. Written even when silent (§J.5)."""
    lines = [f"Staleness audit — {today}", ""]
    width = max((len(r["ticker"]) for r in results), default=6)
    for r in results:
        post, why = decisions[r["ticker"]]
        mark = "!" if r.get("notify") else " "
        note = "posted" if post else why
        lines.append(f"{mark} {r['ticker']:<{width}}  {r['verdict']:<14}  {note}")
    posted = sum(1 for p, _ in decisions.values() if p)
    lines += ["", f"{len(results)} audited · {posted} posted · "
                  f"{sum(1 for r in results if r['verdict'] == 'CLEAN')} clean"]
    return "\n".join(lines)


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", required=True,
                    help="path to `audit_report.py --json` output")
    ap.add_argument("--state", default=".audit-state/seen.json",
                    help="cache-backed record of what was last reported per ticker")
    ap.add_argument("--rollup-file", default=".audit-state/summary.md",
                    help="where to write the repo-wide table (always written)")
    ap.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    ap.add_argument("--today", default=None, help="override today (tests)")
    ap.add_argument("--dry-run", action="store_true",
                    help="decide and render, but do not post or write state")
    args = ap.parse_args(argv)

    today = (datetime.strptime(args.today, "%Y-%m-%d").date() if args.today
             else date.today())
    results = json.loads(Path(args.results).read_text(encoding="utf-8"))
    state_path = Path(args.state)
    state = load_state(state_path)

    decisions = {}
    for r in results:
        decisions[r["ticker"]] = should_notify(
            r, state.get(r["ticker"]), today, args.window_days)

    for r in results:
        post, why = decisions[r["ticker"]]
        if not post:
            print(f"[audit_notify] {r['ticker']}: silent — {why}")
            continue

        body = render_ticker_message(r)
        cmd = [sys.executable, str(HERE / "notify_discord_ticker.py"),
               "--ticker", r["ticker"], "--kind", "audit",
               "--date", today.isoformat()]
        # Red embed for the verdicts that mean a trigger actually tripped.
        if r["verdict"] == "RE-UNDERWRITE":
            cmd.append("--tripwire-fired")
        if args.dry_run:
            cmd.append("--dry-run")
        proc = subprocess.run(cmd, input=body, text=True, encoding="utf-8")
        if proc.returncode != 0:
            print(f"[audit_notify] {r['ticker']}: poster exited "
                  f"{proc.returncode}", file=sys.stderr)
        else:
            print(f"[audit_notify] {r['ticker']}: posted — {why}")
            if not args.dry_run:
                state[r["ticker"]] = {"verdict": r["verdict"],
                                      "last_posted": today.isoformat()}

    rollup = render_rollup(results, decisions, today)
    rollup_path = Path(args.rollup_file)
    if not args.dry_run:
        rollup_path.parent.mkdir(parents=True, exist_ok=True)
        rollup_path.write_text(rollup + "\n", encoding="utf-8")
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True),
                              encoding="utf-8")
    print()
    print(rollup)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
