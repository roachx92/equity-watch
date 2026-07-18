"""Build-time generator for the homepage Coverage grid.

The watch-list is the `tickers/*/` directory glob (see CLAUDE.md) — one folder
per ticker, each holding a `news.md`. The homepage coverage cards must be
derived from it — not hand-maintained — or they drift stale exactly when a
ticker is added or a deep-dive is generated.

This mkdocs hook scans the assembled docs tree and exposes the card data to the
`web/overrides/home.html` template as `config.extra.coverage_cards`. One card per
`tickers/<SYM>/news.md`, auto-linked to the latest
`tickers/<SYM>/reports/<YYYY-MM-DD>.md`.
Per-card prose (`company`, `blurb`) lives in each news.md's YAML front matter,
so it sits next to the thesis rather than in the template.

Note the symbol comes from the *parent directory* name, not the filename — every
news.md is called `news.md`. A folder without a news.md is skipped rather than
crashing the build, so a half-created ticker folder can't take the site down.

Runs wherever the site is built — `web/scripts/build.sh`, `web/scripts/serve.sh`,
and the GitHub Pages deploy — since all of them invoke mkdocs.
"""

from __future__ import annotations

import glob
import os
import re

import yaml

_DATE_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
_FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _front_matter(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else {}


def _latest_report(ticker_dir: str, sym: str) -> str | None:
    """Newest `tickers/<SYM>/reports/<date>.md` as a site path, or None if none."""
    reports_dir = os.path.join(ticker_dir, "reports")
    dates = []
    if os.path.isdir(reports_dir):
        for entry in os.listdir(reports_dir):
            match = _DATE_FILE.match(entry)
            if match:
                dates.append(match.group(1))
    if not dates:
        return None
    return f"tickers/{sym}/reports/{max(dates)}/"  # ISO dates sort lexically


def on_config(config):
    docs_dir = config["docs_dir"]

    cards = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "tickers", "*", "news.md"))):
        ticker_dir = os.path.dirname(path)
        sym = os.path.basename(ticker_dir)
        meta = _front_matter(path)
        cards.append(
            {
                "sym": sym,
                "company": meta.get("company", ""),
                "blurb": meta.get("blurb", ""),
                "monitor": f"tickers/{sym}/news/",
                "report": _latest_report(ticker_dir, sym),
            }
        )

    config["extra"]["coverage_cards"] = cards
    return config
