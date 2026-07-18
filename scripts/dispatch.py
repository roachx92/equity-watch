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
from datetime import timedelta


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
