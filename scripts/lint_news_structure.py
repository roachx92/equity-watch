#!/usr/bin/env python3
"""Lint the structure of every `tickers/<SYM>/news.md`, and flag any ticker
folder with no news.md at all.

A half-created `tickers/<SYM>/` folder (no news.md) is skipped *silently* by both
the daily watch and `web/hooks/coverage.py`, so the ticker goes unwatched and its
coverage card never appears — no error anywhere. This linter turns that silent
gap into a CI failure.

Each news.md must have:
  - YAML front matter with non-empty `company` and `blurb` (the homepage
    coverage grid reads these — `web/hooks/coverage.py`).
  - the sections `## Thesis context`, `## Edge`, `## Tripwires`,
    `## Recent News Log`.

Python 3 stdlib only. Exit 1 on any violation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tickerlib import front_matter, repo_root, ticker_dirs  # noqa: E402

_REQUIRED_FM = ("company", "blurb")
_REQUIRED_SECTIONS = (
    "## Thesis context",
    "## Edge",
    "## Tripwires",
    "## Recent News Log",
)


def lint_news(path: Path) -> list[str]:
    """Structural problems for one news.md (empty = valid)."""
    problems = []
    fm = front_matter(path)
    for key in _REQUIRED_FM:
        if not fm.get(key, "").strip():
            problems.append(f"front matter missing non-empty `{key}`")
    text = path.read_text(encoding="utf-8")
    heads = {ln.strip() for ln in text.splitlines() if ln.startswith("## ")}
    for section in _REQUIRED_SECTIONS:
        # startswith match so `## Thesis context (one-paragraph)` counts.
        if not any(h.startswith(section) for h in heads):
            problems.append(f"missing section `{section}`")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--root", default=None, help="repo root (default: auto)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else repo_root()

    violations = 0
    for d in ticker_dirs(root):
        news = d / "news.md"
        if not news.is_file():
            print(f"tickers/{d.name}/: no news.md — half-created ticker, silently unwatched")
            violations += 1
            continue
        rel = news.relative_to(root).as_posix()
        for problem in lint_news(news):
            print(f"{rel}: {problem}")
            violations += 1

    if violations:
        print(f"\n{violations} structure violation(s)", file=sys.stderr)
        return 1
    print("OK  all ticker news.md files well-formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
