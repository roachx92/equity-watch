"""Build-time generator for the homepage Coverage grid.

The watch-list is the `tickers/*.md` glob (see CLAUDE.md), so the homepage
coverage cards must be derived from it — not hand-maintained — or they drift
stale exactly when a ticker is added or a deep-dive is generated.

This mkdocs hook scans the assembled docs tree and exposes the card data to the
`overrides/home.html` template as `config.extra.coverage_cards`. One card per
`tickers/<SYM>.md`, auto-linked to the latest `reports/<YYYY-MM-DD>/<SYM>.md`.
Per-card prose (`company`, `blurb`) lives in each ticker file's YAML front
matter, so it sits next to the thesis rather than in the template.

Runs wherever the site is built — `scripts/build-site.sh`, `scripts/serve-site.sh`,
and the GitHub Pages deploy — since all of them invoke mkdocs.
"""

from __future__ import annotations

import glob
import os
import re

import yaml

_DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _front_matter(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else {}


def _latest_report(reports_dir: str, sym: str) -> str | None:
    """Newest `reports/<date>/<SYM>.md` as a site path, or None if none exist."""
    dates = []
    if os.path.isdir(reports_dir):
        for entry in os.listdir(reports_dir):
            if _DATE_DIR.match(entry) and os.path.isfile(
                os.path.join(reports_dir, entry, f"{sym}.md")
            ):
                dates.append(entry)
    if not dates:
        return None
    return f"reports/{max(dates)}/{sym}/"  # ISO dates sort lexically


def on_config(config):
    docs_dir = config["docs_dir"]
    reports_dir = os.path.join(docs_dir, "reports")

    cards = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "tickers", "*.md"))):
        sym = os.path.splitext(os.path.basename(path))[0]
        meta = _front_matter(path)
        cards.append(
            {
                "sym": sym,
                "company": meta.get("company", ""),
                "blurb": meta.get("blurb", ""),
                "monitor": f"tickers/{sym}/",
                "report": _latest_report(reports_dir, sym),
            }
        )

    config["extra"]["coverage_cards"] = cards
    return config
