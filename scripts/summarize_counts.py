#!/usr/bin/env python3
"""Stamp the frontmatter counts on `summaries/<date>.md` from ground truth,
instead of the LLM hand-deriving them (and re-deriving the tripwire signal up to
four times per run). The tag written into the news.md log entry becomes the
single source for the count.

Counts:
  tickers_checked  = number of `tickers/<SYM>/news.md` files.
  tripwires_fired  = `[TRIPWIRE…]` tags in log lines *added this run*.
  edge_shifts      = `[EDGE+]` / `[EDGE−]` tags in log lines added this run.

"Added this run" = added (`+`) lines under `tickers/*/news.md` in `git diff`
against the base (default HEAD) — i.e. everything appended but not yet committed.

    --check    exit 1 if the file's existing counts disagree with derived.
    --dry-run  print the frontmatter block that would be written; write nothing.
    (default)  rewrite the frontmatter block in place, body untouched.

Python 3 stdlib only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import news_files, repo_root  # noqa: E402

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)
_TRIPWIRE = re.compile(r"\[TRIPWIRE")
_EDGE = re.compile(r"\[EDGE[+−-]")  # EDGE+ , EDGE− (U+2212), EDGE-
_COUNT_KEYS = ("tickers_checked", "tripwires_fired", "edge_shifts")


def added_lines(diff_text: str) -> str:
    """The added (`+`) content of a unified diff, minus the `+++` file headers."""
    return "\n".join(
        ln[1:] for ln in diff_text.splitlines() if ln.startswith("+") and not ln.startswith("+++")
    )


def derive_counts(diff_text: str, news_file_count: int) -> dict:
    added = added_lines(diff_text)
    return {
        "tickers_checked": news_file_count,
        "tripwires_fired": len(_TRIPWIRE.findall(added)),
        "edge_shifts": len(_EDGE.findall(added)),
    }


def git_news_diff(root: Path, base: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), "diff", "--unified=0", base, "--", "tickers/*/news.md"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def render_frontmatter(date: str, counts: dict) -> str:
    return (
        "---\n"
        f"date: {date}\n"
        f"tickers_checked: {counts['tickers_checked']}\n"
        f"tripwires_fired: {counts['tripwires_fired']}\n"
        f"edge_shifts: {counts['edge_shifts']}\n"
        "---\n"
    )


def split_summary(path: Path) -> tuple[dict, str]:
    """(existing frontmatter dict, body) for a summary file."""
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.split("#", 1)[0].strip()
    return meta, m.group(2)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--date", required=True, help="summary date (YYYY-MM-DD)")
    ap.add_argument("--base", default="HEAD", help="git diff base (default HEAD)")
    ap.add_argument("--check", action="store_true", help="verify existing counts, exit 1 on mismatch")
    ap.add_argument("--dry-run", action="store_true", help="print the frontmatter, write nothing")
    args = ap.parse_args(argv)

    root = repo_root()
    diff = git_news_diff(root, args.base)
    counts = derive_counts(diff, len(news_files(root)))

    summary = root / "summaries" / f"{args.date}.md"
    if not summary.is_file():
        print(f"{summary} does not exist", file=sys.stderr)
        return 1
    meta, body = split_summary(summary)

    if args.check:
        mism = [k for k in _COUNT_KEYS if str(counts[k]) != meta.get(k, "")]
        if mism:
            for k in mism:
                print(f"MISMATCH {k}: file={meta.get(k, '∅')} derived={counts[k]}")
            return 1
        print("OK  frontmatter counts match derived")
        return 0

    front = render_frontmatter(meta.get("date", args.date), counts)
    if args.dry_run:
        print(front, end="")
        return 0
    summary.write_text(front + body, encoding="utf-8")
    print(f"stamped {summary.relative_to(root).as_posix()}: "
          f"{counts['tickers_checked']} checked · {counts['tripwires_fired']} tripwire(s) · "
          f"{counts['edge_shifts']} edge shift(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
