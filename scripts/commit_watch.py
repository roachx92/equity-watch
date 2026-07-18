#!/usr/bin/env python3
"""Commit and push the daily-watch outputs — the mechanical git step, moved out
of the daily-watch prose into a script the agent invokes.

Stages the changed `tickers/*/news.md` files plus `summaries/<date>.md`, commits
with the canonical message `daily watch: <date>`, and pushes (the push is what
triggers the Discord notification Action).

    --date <YYYY-MM-DD>   required — the run date (commit message + summary file)
    --no-push             commit only, do not push
    --dry-run             print the staged files + message, run no git

Python 3 stdlib only.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import repo_root  # noqa: E402


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout


def staged_targets(root: Path, date: str) -> list[str]:
    """Pathspecs to stage: the news.md files and this run's summary file."""
    targets = ["tickers/*/news.md"]
    summary = f"summaries/{date}.md"
    if (root / summary).is_file():
        targets.append(summary)
    return targets


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--date", required=True, help="run date (YYYY-MM-DD)")
    ap.add_argument("--no-push", action="store_true", help="commit only, do not push")
    ap.add_argument("--dry-run", action="store_true", help="print plan, run no git")
    args = ap.parse_args(argv)

    root = repo_root()
    targets = staged_targets(root, args.date)
    message = f"daily watch: {args.date}"

    if args.dry_run:
        print(f"would stage:   {' '.join(targets)}")
        print(f"would commit:  {message}")
        print("would push:    " + ("no (--no-push)" if args.no_push else "yes"))
        # Show what actually differs so a dry run is informative.
        changed = _git(root, "status", "--porcelain", "--", *targets).strip()
        print("current changes:\n" + (changed or "  (none)"))
        return 0

    _git(root, "add", "--", *targets)
    if not _git(root, "diff", "--cached", "--name-only").strip():
        print("nothing staged — no watch outputs changed; skipping commit")
        return 0
    _git(root, "commit", "-m", message)
    print(f"committed: {message}")
    if not args.no_push:
        _git(root, "push")
        print("pushed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
