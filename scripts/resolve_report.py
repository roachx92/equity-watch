#!/usr/bin/env python3
"""Resolve each ticker's `**Canonical deep-dive:**` pointer against the newest
report on disk — the deterministic version of the glob-and-max rule the LLM
otherwise runs by hand every whats-new/earnings/deep-dive session (CLAUDE.md's
"resolve by glob, never by trust").

The pointer is a written cache and can go stale (a later re-run, a manual edit,
a race between sessions). This script is the single programmatic resolver:

    --check   (default) exit 1 if any news.md pointer != newest report. CI gate.
    --fix     rewrite the pointer link to the newest date, prose untouched.

It only ever rewrites the canonical pointer's own markdown — the backtick-coded
link `[`reports/<date>.md`](reports/<date>.md)` — never any other dated link in
the line (AAOI's line references an older snapshot in prose; that must survive).

Python 3 stdlib only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import latest_report_date, ticker_dirs  # noqa: E402

# The canonical pointer, and ONLY it: a backtick code-span label + link whose
# target is a dated report file. The prose form `[2026-07-14](reports/..)` (no
# backticks in the label) is deliberately not matched.
_CANON_POINTER = re.compile(
    r"\[`reports/(\d{4}-\d{2}-\d{2})\.md`\]\(reports/(\d{4}-\d{2}-\d{2})\.md\)"
)
_CANON_LINE = "**Canonical deep-dive:**"


def _pointer_date(news_text: str) -> tuple[str | None, int | None]:
    """Return (dated linked in the canonical pointer, line index) or (None, None)."""
    for i, line in enumerate(news_text.splitlines()):
        if line.startswith(_CANON_LINE):
            m = _CANON_POINTER.search(line)
            return (m.group(1) if m else None, i)
    return (None, None)


def _rewrite_pointer(line: str, newest: str) -> str:
    """Rewrite only the canonical pointer link in `line` to `newest`."""
    return _CANON_POINTER.sub(
        lambda _m: f"[`reports/{newest}.md`](reports/{newest}.md)", line, count=1
    )


def check(root: Path | None = None):
    """Yield (sym, pointer_date, newest_date, status) for every ticker."""
    rows = []
    for d in ticker_dirs(root):
        news = d / "news.md"
        if not news.is_file():
            continue  # half-created ticker — lint_news_structure.py owns that
        pointer, _ = _pointer_date(news.read_text(encoding="utf-8"))
        newest = latest_report_date(d)
        if newest is None:
            status = "no-reports"
        elif pointer is None:
            status = "no-pointer"
        elif pointer == newest:
            status = "ok"
        else:
            status = "drift"
        rows.append((d.name, pointer, newest, status))
    return rows


def fix(root: Path | None = None) -> list[str]:
    """Rewrite stale pointers to the newest report. Return the syms fixed."""
    fixed = []
    for d in ticker_dirs(root):
        news = d / "news.md"
        if not news.is_file():
            continue
        text = news.read_text(encoding="utf-8")
        pointer, _ = _pointer_date(text)
        newest = latest_report_date(d)
        if newest is None or pointer is None or pointer == newest:
            continue
        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if line.startswith(_CANON_LINE):
                lines[i] = _rewrite_pointer(line, newest)
                break
        news.write_text("".join(lines), encoding="utf-8")
        fixed.append(d.name)
    return fixed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report drift, exit 1 if any (default)")
    mode.add_argument("--fix", action="store_true", help="rewrite stale pointers to newest report")
    args = ap.parse_args(argv)

    if args.fix:
        fixed = fix()
        if fixed:
            print("fixed pointer for: " + ", ".join(fixed))
        else:
            print("all pointers already current")
        return 0

    rows = check()
    drift = [r for r in rows if r[3] == "drift"]
    for sym, pointer, newest, status in rows:
        if status == "drift":
            print(f"DRIFT  {sym}: pointer={pointer} newest={newest}")
        elif status in ("no-pointer", "no-reports"):
            print(f"WARN   {sym}: {status}")
    if drift:
        print(f"\n{len(drift)} stale pointer(s) — run `resolve_report.py --fix`", file=sys.stderr)
        return 1
    print(f"OK     {len(rows)} ticker(s), all pointers current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
