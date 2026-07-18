#!/usr/bin/env python3
"""Deterministic dispatcher for the equity-watch heavy workflows.

Runs on a schedule (see .github/workflows/dispatcher.yml). For each watched
ticker under tickers/*/ it decides — using cheap Finnhub calls and no Claude —
whether an earnings-digest and/or a what's-new scan is warranted, then fires the
existing heavy workflow via `gh workflow run`. See
docs/superpowers/specs/2026-07-18-dispatcher-triggers-design.md.

Python 3 stdlib only.
"""
import re
import json
from datetime import datetime, timedelta
from pathlib import Path


def material_headlines(news_items, keywords):
    """Keep Finnhub company-news items whose headline or summary contains a
    materiality keyword (case-insensitive, word-boundary). Returns a list of
    (headline, matched_keyword) tuples — the first matched keyword labels each."""
    matches = []
    for item in news_items:
        text = ((item.get("headline") or "") + " " + (item.get("summary") or "")).lower()
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text):
                matches.append((item.get("headline", ""), kw))
                break
    return matches


def should_scan_news(matched, last_scan, now, cap_hours=48):
    """Decide whether to fire a what's-new scan.

    matched   -- list from material_headlines (truthy iff any material item)
    last_scan -- tz-aware datetime of the previous scan dispatch, or None
    now       -- tz-aware datetime (UTC)
    Returns (should_fire, reason_str).
    """
    if not matched:
        return (False, "no material news")
    if last_scan is not None and (now - last_scan) < timedelta(hours=cap_hours):
        resume = last_scan + timedelta(hours=cap_hours)
        return (False, "rate-capped until " + resume.strftime("%Y-%m-%d %H:%MZ"))
    keyword = matched[0][1]
    return (True, 'keyword: "%s" (%d headline(s))' % (keyword, len(matched)))


def earnings_due(calendar_rows, today):
    """Return the most recent report date (YYYY-MM-DD str) in [today-1, today]
    from Finnhub earningsCalendar rows, or None. `today` is a date object."""
    window = {(today - timedelta(days=1)).isoformat(), today.isoformat()}
    dates = sorted({r.get("date") for r in calendar_rows if r.get("date") in window})
    return dates[-1] if dates else None


def quarter_already_logged(debrief_text, report_date):
    """True if the earnings debrief already covers the quarter reported on
    report_date. Dedup keys on the reporting date appearing in the debrief — the
    earnings-digest workflow stamps that date on the quarter heading. A missing or
    empty debrief means the quarter is not logged (dispatch)."""
    if not debrief_text:
        return False
    return report_date in debrief_text


def load_state(path):
    """Load the gate-state JSON. Missing or unparseable file -> {}."""
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(path, state):
    """Write the gate-state JSON, creating parent directories."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def _parse_dt(s):
    """Parse an isoformat datetime string; None/invalid -> None."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def list_tickers(tickers_dir):
    """Watch-list = subdirectories of tickers_dir that contain a news.md."""
    base = Path(tickers_dir)
    if not base.exists():
        return []
    return [p.name for p in base.iterdir() if p.is_dir() and (p / "news.md").exists()]


def read_debrief(tickers_dir, ticker):
    """Return tickers/<ticker>/earnings-debrief.md contents, or '' if absent."""
    p = Path(tickers_dir) / ticker / "earnings-debrief.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""
