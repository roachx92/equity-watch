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
import sys
from pathlib import Path

# Reuse the deterministic watch-list helpers instead of re-implementing the
# front-matter parser and report-date glob here. scripts/ sits at the repo root
# (parents[2] of web/hooks/coverage.py); __file__-relative so it resolves under
# whatever cwd mkdocs runs the hook from. tickerlib is stdlib-only, so this hook
# no longer needs PyYAML.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import tickerlib  # noqa: E402


def _latest_report(ticker_dir: str, sym: str) -> str | None:
    """Newest `tickers/<SYM>/reports/<date>.md` as a site path, or None if none.

    Date-finding is delegated to tickerlib; this only formats the site URL.
    """
    date = tickerlib.latest_report_date(Path(ticker_dir))
    return f"tickers/{sym}/reports/{date}/" if date else None


def on_config(config):
    docs_dir = config["docs_dir"]

    cards = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "tickers", "*", "news.md"))):
        ticker_dir = os.path.dirname(path)
        sym = os.path.basename(ticker_dir)
        meta = tickerlib.front_matter(Path(path))
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
