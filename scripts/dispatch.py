#!/usr/bin/env python3
"""Deterministic dispatcher for the equity-watch heavy workflows.

Runs on a schedule (see .github/workflows/dispatcher.yml). For each watched
ticker under tickers/*/ it decides — using cheap Finnhub calls and no Claude —
whether an earnings-digest and/or a what's-new scan is warranted, then fires the
existing heavy workflow via `gh workflow run`. See
docs/superpowers/specs/2026-07-18-dispatcher-triggers-design.md.

Python 3 stdlib only.
"""
import argparse
import os
import re
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
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
    report_date. Dedup keys on the quarter HEADING the earnings-digest workflow
    writes — `## <FY period> — reported <YYYY-MM-DD>` (framework/earnings-digest.md
    §I.5) — not on the bare date appearing anywhere, because debriefs also carry
    that date in methodology lines, the deep-dive link, and guidance-table cells.
    A missing or empty debrief means the quarter is not logged (dispatch)."""
    if not debrief_text:
        return False
    pattern = r"(?m)^##\s.*\breported\s+" + re.escape(report_date) + r"\b"
    return re.search(pattern, debrief_text) is not None


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


class FinnhubClient:
    """Thin wrapper over the Finnhub free-tier REST API (stdlib urllib).

    `opener` defaults to urllib.request.urlopen; tests inject a fake that
    returns recorded fixtures, so the suite never touches the network.
    """
    BASE = "https://finnhub.io/api/v1"

    def __init__(self, api_key, opener=None):
        self._key = api_key
        self._opener = opener or urllib.request.urlopen

    def _get(self, path, params):
        url = self.BASE + path + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"X-Finnhub-Token": self._key})
        with self._opener(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def earnings_calendar(self, symbol, frm, to):
        data = self._get("/calendar/earnings", {"symbol": symbol, "from": frm, "to": to})
        return data.get("earningsCalendar", []) if isinstance(data, dict) else []

    def company_news(self, symbol, frm, to):
        data = self._get("/company-news", {"symbol": symbol, "from": frm, "to": to})
        return data if isinstance(data, list) else []


# Materiality keyword set — the coarse pre-filter that decides a headline is
# worth a paid Opus scan. Edit here to tune. Word-boundary, case-insensitive.
DEFAULT_KEYWORDS = [
    "earnings", "results", "guidance", "forecast", "outlook",
    "contract", "award", "deal", "offering", "dilution", "raise",
    "downgrade", "upgrade", "price target", "SEC", "8-K", "10-Q",
    "CEO", "CFO", "resign", "appoint", "merger", "acquire",
    "acquisition", "buyout", "halt", "recall", "lawsuit",
    "investigation", "bankruptcy",
]


def dispatch_workflow(workflow_file, ticker, dry_run=False):
    """Fire a workflow_dispatch for one ticker via the gh CLI. Returns True on
    success. dry_run prints nothing and skips the call (returns True)."""
    if dry_run:
        return True
    cmd = ["gh", "workflow", "run", workflow_file, "-f", "ticker=" + ticker]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write("dispatch failed for %s (%s): %s\n"
                         % (ticker, workflow_file, result.stderr.strip()))
        return False
    return True


def run(tickers_dir, client, state, now, keywords,
        dispatch=dispatch_workflow, dry_run=False):
    """Per-ticker decision loop. Mutates `state` in place when a scan fires
    (unless dry_run). Returns summary rows: (ticker, earnings_cell, news_cell, reason)."""
    today = now.date()
    rows = []
    for ticker in sorted(list_tickers(tickers_dir)):
        earnings_cell, news_cell, reasons = "—", "—", []

        # --- Earnings trigger (stateless, repo-read dedup) ---
        try:
            cal = client.earnings_calendar(
                ticker, (today - timedelta(days=1)).isoformat(), today.isoformat())
            report_date = earnings_due(cal, today)
            if report_date is None:
                reasons.append("no calendar report")
            elif quarter_already_logged(read_debrief(tickers_dir, ticker), report_date):
                earnings_cell = "skipped"
                reasons.append("quarter %s already logged" % report_date)
            else:
                ok = dispatch("earnings-digest.yml", ticker, dry_run)
                earnings_cell = "dispatched" if ok else "dispatch-failed"
                reasons.append(
                    ("earnings reported %s" % report_date) if ok
                    else ("earnings dispatch FAILED for %s" % report_date))
        except Exception as exc:  # noqa: BLE001 - one ticker must not sink the run
            reasons.append("earnings error: %s" % exc)

        # --- What's-new gate (keyword filter + 48h cap) ---
        try:
            last_scan = _parse_dt((state.get(ticker) or {}).get("last_news_scan"))
            frm = (last_scan.date() if last_scan else today - timedelta(days=3)).isoformat()
            news = client.company_news(ticker, frm, today.isoformat())
            matched = material_headlines(news, keywords)
            should, reason = should_scan_news(matched, last_scan, now)
            reasons.append(reason)
            if should:
                ok = dispatch("whats-new.yml", ticker, dry_run)
                if ok:
                    news_cell = "dispatched"
                    if not dry_run:
                        state.setdefault(ticker, {})["last_news_scan"] = now.isoformat()
                else:
                    news_cell = "dispatch-failed"
                    reasons.append("whats-new dispatch FAILED")
            elif matched:
                news_cell = "skipped"
        except Exception as exc:  # noqa: BLE001
            reasons.append("news error: %s" % exc)

        rows.append((ticker, earnings_cell, news_cell, "; ".join(reasons)))
    return rows


def render_summary(rows):
    """Render the decision rows as a Markdown table for the Actions summary.
    Cell values are escaped so a `|` in a reason (e.g. an exception message)
    cannot corrupt the table."""
    def _cell(value):
        return str(value).replace("|", "\\|")
    lines = ["| Ticker | Earnings | What's-new | Reason |",
             "| --- | --- | --- | --- |"]
    for ticker, earnings_cell, news_cell, reason in rows:
        lines.append("| %s | %s | %s | %s |"
                     % (_cell(ticker), _cell(earnings_cell), _cell(news_cell), _cell(reason)))
    return "\n".join(lines)


def write_summary_file(path, summary):
    """Write the rendered decision table to `path` (creating parents) so a
    separate workflow step (the Discord notifier) can read the exact same table.
    Derived output, not gate state — written on both real and dry runs."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(summary, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic equity-watch dispatcher.")
    ap.add_argument("--tickers-dir", default="tickers")
    ap.add_argument("--state-file", default=".dispatch-state/state.json")
    ap.add_argument("--summary-file", default=".dispatch-state/summary.md",
                    help="also write the rendered decision table here (for the Discord notifier)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the decision table without dispatching or saving state")
    args = ap.parse_args(argv)

    api_key = os.environ.get("FINNHUB_API_KEY", "")
    if not api_key:
        sys.stderr.write("FINNHUB_API_KEY not set — cannot run dispatcher.\n")
        return 1

    now = datetime.now(timezone.utc)
    client = FinnhubClient(api_key)
    state = load_state(args.state_file)
    rows = run(args.tickers_dir, client, state, now, DEFAULT_KEYWORDS, dry_run=args.dry_run)
    if not args.dry_run:
        save_state(args.state_file, state)

    summary = render_summary(rows)
    print(summary)
    write_summary_file(args.summary_file, summary)
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as fh:
            fh.write("## Dispatcher run (%s)\n\n%s\n" % (now.date().isoformat(), summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
