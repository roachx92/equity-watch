#!/usr/bin/env python3
"""Lint every `## Recent News Log` entry against the invariants of the canonical
format — `framework/latest-updates-workflow.md` §F.1, which stays the single
source of truth. This file validates the *shape* §F.1 asserts; it does NOT
restate the format (and it checks that nobody else does either).

Structural invariants — hard failures (exit 1):
  1. leads with a date or date-range (`YYYY-MM-DD` [` to YYYY-MM-DD`]) then ` — `
  2. carries at least one `[FRAMEWORK-TAG]` bracket right after the date
  3. has a bold `**Headline**`
  4. states the implication — the mandatory `→` clause

Warning — printed, does NOT fail (exit stays 0):
  5. cites at least one linked source: `Source:` + at least one `[label](http…)`.
     Older entries predate the link requirement (bare `Source: GlobeNewswire`),
     so this is surfaced, not blocked, until a cleanup pass. Promote to a hard
     fail once the corpus is linked.

Real entries use compound tags (`[Sentiment/Valuation]`), status suffixes
(`[TRIPWIRE #4 — touched, not sustained]`), and date ranges — all valid here.

Repo invariant: the literal skeleton `YYYY-MM-DD — [FRAMEWORK-TAG]` must appear
only in §F.1 (no `_template`-style restatement leaks elsewhere).

Python 3 stdlib only. Exit 1 on any violation.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import news_files, repo_root  # noqa: E402

_LOG_HEADER = "## Recent News Log"
_ENTRY_LEAD = re.compile(r"^-\s+\d{4}-\d{2}-\d{2}(?:\s+to\s+\d{4}-\d{2}-\d{2})?\s+—\s+\[[^\]]+\]")
_ENTRY_BULLET = re.compile(r"^-\s+\d{4}-\d{2}-\d{2}")
_BOLD = re.compile(r"\*\*.+?\*\*")  # a bold span may itself contain *italic* emphasis
_LINK = re.compile(r"\]\(https?://")
_SKELETON = "YYYY-MM-DD — [FRAMEWORK-TAG]"
_CANONICAL_SPEC = "framework/latest-updates-workflow.md"


def log_entries(text: str) -> list[tuple[int, str]]:
    """(1-based line number, line) for each bullet in the Recent News Log section."""
    lines = text.splitlines()
    out, in_section = [], False
    for i, line in enumerate(lines, start=1):
        if line.startswith("## "):
            in_section = line.strip() == _LOG_HEADER
            continue
        if in_section and _ENTRY_BULLET.match(line):
            out.append((i, line))
    return out


def lint_entry(line: str) -> tuple[list[str], list[str]]:
    """(hard problems, warnings) for one entry line — both empty = fully valid."""
    problems = []
    if not _ENTRY_LEAD.match(line):
        problems.append("must lead with `DATE[ to DATE] — [FRAMEWORK-TAG]`")
    if not _BOLD.search(line):
        problems.append("missing bold **Headline**")
    if "→" not in line:
        problems.append("missing the mandatory `→` implication clause")
    warnings = []
    if "Source:" not in line or not _LINK.search(line):
        warnings.append("bare source, no linked citation (`Source:` + [label](http…))")
    return problems, warnings


def _restatement_leaks(root: Path) -> list[str]:
    """Markdown files (other than §F.1) that restate the literal format skeleton."""
    leaks = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        if rel == _CANONICAL_SPEC or "/.claude/" in f"/{rel}" or rel.startswith(".claude/"):
            continue
        try:
            if _SKELETON in md.read_text(encoding="utf-8"):
                leaks.append(rel)
        except (OSError, UnicodeDecodeError):
            continue
    return leaks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--root", default=None, help="repo root (default: auto)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else repo_root()

    violations, warnings = 0, 0
    for news in news_files(root):
        rel = news.relative_to(root).as_posix()
        text = news.read_text(encoding="utf-8")
        for lineno, line in log_entries(text):
            problems, warns = lint_entry(line)
            for problem in problems:
                print(f"{rel}:{lineno}: {problem}")
                violations += 1
            for warn in warns:
                print(f"{rel}:{lineno}: WARN {warn}")
                warnings += 1

    for leak in _restatement_leaks(root):
        print(f"{leak}: restates the §F.1 format skeleton — reference §F.1, do not copy it")
        violations += 1

    if warnings:
        print(f"{warnings} warning(s) (non-blocking)")
    if violations:
        print(f"\n{violations} log-format violation(s)", file=sys.stderr)
        return 1
    print("OK  all Recent News Log entries structurally valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
