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
  6. stays within §F.1's ~1,200-character ceiling. **Scoped to entries dated on
     or after LENGTH_RULE_FROM**, because §F.1's length rule is explicitly
     forward-looking: the log is a dated record of what was known when, and
     existing entries are never rewritten to match a later format revision.
     Without that scoping the warning would flood on historical entries nobody
     is permitted to fix.

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
from tickerlib import (  # noqa: E402
    entry_date,
    log_entries,
    news_files,
    parse_assessment_tags,
    repo_root,
)

#: §F.1's length ceiling. Not a hard limit — an entry that genuinely needs 1,300
#: characters is fine; one that needs 4,000 is the research pass pasted in rather
#: than distilled, and that is what this catches.
LENGTH_CEILING = 1200

#: The date §F.1's length rule was adopted. Entries dated before this predate the
#: rule and are historical record — never rewritten (§F.1), so never warned about.
LENGTH_RULE_FROM = "2026-07-29"

_LOG_HEADER = "## Recent News Log"
_ENTRY_LEAD = re.compile(r"^-\s+\d{4}-\d{2}-\d{2}(?:\s+to\s+\d{4}-\d{2}-\d{2})?\s+—\s+\[[^\]]+\]")
_ENTRY_BULLET = re.compile(r"^-\s+\d{4}-\d{2}-\d{2}")
_BOLD = re.compile(r"\*\*.+?\*\*")  # a bold span may itself contain *italic* emphasis
_LINK = re.compile(r"\]\(https?://")
_SKELETON = "YYYY-MM-DD — [FRAMEWORK-TAG]"
_CANONICAL_SPEC = "framework/latest-updates-workflow.md"


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

    when = entry_date(line)
    if when and when >= LENGTH_RULE_FROM and len(line) > LENGTH_CEILING:
        warnings.append(
            f"{len(line)} chars — over §F.1's ~{LENGTH_CEILING}-char ceiling. "
            "Cut broad-market colour, prose on tripwires this item does not "
            "move, and commentary on prior entries; keep the figures that "
            "change the assessment and the → clause"
        )

    # Assessment-tag grammar (§F.1). Polarity drives the staleness audit's
    # routing, so an unclassifiable tag is a hard failure: silently treating it
    # as either fired or not-fired would misroute an expensive decision.
    for tag in parse_assessment_tags(line):
        if tag["polarity"] is None:
            problems.append(
                f"unrecognised assessment tag {tag['raw']} — §F.1 defines "
                f"[EDGE+] / [EDGE−] / [EDGE~] and [TRIPWIRE #n — fires|early-warning|does not fire]"
            )
        elif tag["legacy"]:
            warnings.append(f"legacy tag spelling {tag['raw']} — canonicalise per §F.1")
        if tag["kind"] == "TRIPWIRE" and tag["number"] is None:
            problems.append(f"tripwire tag {tag['raw']} missing its `#n` — which trigger?")
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
    # Findings quote em-dashes, §, and U+2212 from the entries themselves;
    # a cp1252 console would mojibake them (or crash on write).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

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
