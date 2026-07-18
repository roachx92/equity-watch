# Deterministic Dispatcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a scheduled, deterministic dispatcher that fires the existing `earnings-digest.yml` and `whats-new.yml` workflows only when warranted — earnings the morning after a Finnhub-calendar report, what's-new via a cheap keyword+48h-cap news gate.

**Architecture:** One new scheduled workflow (`.github/workflows/dispatcher.yml`) runs a deterministic Python script (`scripts/dispatch.py`, no Claude). The script globs `tickers/*/`, queries Finnhub for earnings dates and company news, and calls `gh workflow run <file> -f ticker=<T>` for the tickers that qualify. All analytical behaviour of the two heavy workflows is unchanged — the dispatcher only triggers them.

**Tech Stack:** Python 3 standard library only (`urllib`, `json`, `argparse`, `subprocess`, `datetime`, `pathlib`, `re`). Pytest for tests. GitHub Actions (`schedule` cron, `actions/cache` for gate state, `gh` CLI for dispatch). Finnhub free-tier REST API.

## Global Constraints

- **Stdlib only** in `scripts/dispatch.py` — no third-party packages (matches `scripts/notify_discord_ticker.py`). HTTP via `urllib.request`.
- **No type annotations in code** — the existing scripts use none; follow that. Document types in docstrings.
- **Python 3.9 compatible** (local dev runs 3.9.6). Store/parse datetimes as `isoformat()` with `+00:00` offset (not a `Z` suffix — 3.9's `fromisoformat` rejects `Z`).
- **Never commit dispatcher state to `main`** — gate state lives only in the Actions cache.
- **Dispatch via `gh workflow run`** (a `workflow_dispatch`), driven by `GITHUB_TOKEN` with `actions: write`. This is the recursion-guard exception GitHub documents and is already proven in-repo (`earnings-digest.yml` calls `gh workflow run pages.yml`).
- **Per-ticker isolation** — one ticker's API error must never sink the whole run; catch per ticker and record the error in the summary.
- **No silent drops** — every ticker's outcome + reason goes to the Actions job summary.
- Test command throughout: `python3 -m pytest scripts/tests/test_dispatch.py -v`.

---

### Task 1: News-gate decision logic

Creates `scripts/dispatch.py` with the two pure functions that decide whether a what's-new scan is warranted. Pure — no I/O, no network — so they are the fully-tested core.

**Files:**
- Create: `scripts/dispatch.py`
- Create: `scripts/tests/test_dispatch.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `material_headlines(news_items, keywords) -> list of (headline_str, matched_keyword_str)` — one tuple per news item whose `headline`+`summary` contains a keyword (case-insensitive, word-boundary); first matched keyword wins.
  - `should_scan_news(matched, last_scan, now, cap_hours=48) -> (bool, reason_str)` — `matched` is the list from `material_headlines`; `last_scan` is a tz-aware `datetime` or `None`; `now` is tz-aware `datetime`.

- [ ] **Step 1: Write the failing tests**

```python
# scripts/tests/test_dispatch.py
import sys
import pathlib
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import dispatch  # noqa: E402

UTC = timezone.utc


def _news(headline, summary=""):
    return {"headline": headline, "summary": summary}


def test_material_headlines_matches_keyword_case_insensitive():
    items = [_news("Company wins big CONTRACT with hyperscaler")]
    matched = dispatch.material_headlines(items, ["contract", "guidance"])
    assert matched == [("Company wins big CONTRACT with hyperscaler", "contract")]


def test_material_headlines_ignores_routine_headlines():
    items = [_news("Why the stock rose 4% today"), _news("3 stocks to watch")]
    assert dispatch.material_headlines(items, ["contract", "guidance", "earnings"]) == []


def test_material_headlines_matches_on_word_boundary_only():
    # "sec" must not match inside "second"; "SEC probe" must match.
    assert dispatch.material_headlines([_news("A second look")], ["sec"]) == []
    assert dispatch.material_headlines([_news("SEC opens probe")], ["sec"]) == [("SEC opens probe", "sec")]


def test_material_headlines_searches_summary_too():
    items = [_news("Update", summary="management issued fresh guidance")]
    assert dispatch.material_headlines(items, ["guidance"]) == [("Update", "guidance")]


def test_should_scan_news_fires_when_material_and_never_scanned():
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    matched = [("Wins contract", "contract"), ("Raises guidance", "guidance")]
    should, reason = dispatch.should_scan_news(matched, None, now)
    assert should is True
    assert reason == 'keyword: "contract" (2 headline(s))'


def test_should_scan_news_skips_when_no_material_news():
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    should, reason = dispatch.should_scan_news([], None, now)
    assert should is False
    assert reason == "no material news"


def test_should_scan_news_rate_caps_within_48h():
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    last = now - timedelta(hours=10)
    matched = [("Wins contract", "contract")]
    should, reason = dispatch.should_scan_news(matched, last, now)
    assert should is False
    assert reason == "rate-capped until 2026-07-19 13:30Z"


def test_should_scan_news_fires_after_48h():
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    last = now - timedelta(hours=49)
    matched = [("Wins contract", "contract")]
    should, _ = dispatch.should_scan_news(matched, last, now)
    assert should is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'dispatch'` (file not yet created).

- [ ] **Step 3: Create `scripts/dispatch.py` with the two functions**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: PASS (8 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/dispatch.py scripts/tests/test_dispatch.py
git commit -m "feat(dispatch): news-gate materiality + 48h-cap decision logic"
```

---

### Task 2: Earnings decision logic

Adds the two pure functions that decide whether an earnings digest is due, with repo-read dedup.

**Files:**
- Modify: `scripts/dispatch.py`
- Modify: `scripts/tests/test_dispatch.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `earnings_due(calendar_rows, today) -> report_date_str or None` — `calendar_rows` are Finnhub `earningsCalendar` dicts (each with a `date` key); `today` is a `date`. Returns the most recent report date in `[today-1, today]`, else `None`.
  - `quarter_already_logged(debrief_text, report_date) -> bool` — True iff `report_date` appears in the debrief text (dedup key; empty text → False).

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_dispatch.py`:

```python
from datetime import date


def test_earnings_due_returns_recent_report_in_window():
    rows = [{"date": "2026-07-17", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 18)) == "2026-07-17"


def test_earnings_due_returns_today_report():
    rows = [{"date": "2026-07-18", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 18)) == "2026-07-18"


def test_earnings_due_ignores_reports_outside_window():
    rows = [{"date": "2026-07-15", "symbol": "COHR"}, {"date": "2026-11-05", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 18)) is None


def test_earnings_due_empty_calendar_is_none():
    assert dispatch.earnings_due([], date(2026, 7, 18)) is None


def test_quarter_already_logged_true_when_date_present():
    debrief = "## Q4 FY2026 — reported 2026-07-17\n\nNumbers...\n"
    assert dispatch.quarter_already_logged(debrief, "2026-07-17") is True


def test_quarter_already_logged_false_when_absent():
    debrief = "## Q3 FY2026 — reported 2026-04-30\n"
    assert dispatch.quarter_already_logged(debrief, "2026-07-17") is False


def test_quarter_already_logged_false_when_debrief_empty():
    assert dispatch.quarter_already_logged("", "2026-07-17") is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: FAIL — `AttributeError: module 'dispatch' has no attribute 'earnings_due'`.

- [ ] **Step 3: Add the functions to `scripts/dispatch.py`**

Append after `should_scan_news`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: PASS (15 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/dispatch.py scripts/tests/test_dispatch.py
git commit -m "feat(dispatch): earnings-due detection + repo-read quarter dedup"
```

---

### Task 3: State persistence + filesystem helpers

Adds gate-state load/save, the datetime parser, and the ticker/debrief filesystem readers.

**Files:**
- Modify: `scripts/dispatch.py`
- Modify: `scripts/tests/test_dispatch.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `load_state(path) -> dict` — returns `{}` for a missing or unparseable file.
  - `save_state(path, state) -> None` — writes pretty JSON, creating parent dirs.
  - `_parse_dt(s) -> datetime or None` — parses an isoformat string; `None`/invalid → `None`.
  - `list_tickers(tickers_dir) -> list[str]` — subdirectory names that contain a `news.md`.
  - `read_debrief(tickers_dir, ticker) -> str` — `earnings-debrief.md` contents, or `""` if absent.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_dispatch.py`:

```python
def test_load_state_missing_file_returns_empty(tmp_path):
    assert dispatch.load_state(str(tmp_path / "nope.json")) == {}


def test_save_then_load_state_roundtrips(tmp_path):
    path = str(tmp_path / "state" / "state.json")
    dispatch.save_state(path, {"AAOI": {"last_news_scan": "2026-07-18T13:30:00+00:00"}})
    assert dispatch.load_state(path) == {"AAOI": {"last_news_scan": "2026-07-18T13:30:00+00:00"}}


def test_load_state_bad_json_returns_empty(tmp_path):
    p = tmp_path / "state.json"
    p.write_text("{not json", encoding="utf-8")
    assert dispatch.load_state(str(p)) == {}


def test_parse_dt_roundtrips_utc():
    dt = dispatch._parse_dt("2026-07-18T13:30:00+00:00")
    assert dt.year == 2026 and dt.utcoffset() == timedelta(0)


def test_parse_dt_none_and_garbage_return_none():
    assert dispatch._parse_dt(None) is None
    assert dispatch._parse_dt("not-a-date") is None


def test_list_tickers_only_dirs_with_news_md(tmp_path):
    (tmp_path / "AAOI").mkdir()
    (tmp_path / "AAOI" / "news.md").write_text("x", encoding="utf-8")
    (tmp_path / "EMPTY").mkdir()  # no news.md
    (tmp_path / "loose.txt").write_text("x", encoding="utf-8")
    assert dispatch.list_tickers(str(tmp_path)) == ["AAOI"]


def test_read_debrief_absent_returns_empty(tmp_path):
    (tmp_path / "AAOI").mkdir()
    assert dispatch.read_debrief(str(tmp_path), "AAOI") == ""


def test_read_debrief_returns_contents(tmp_path):
    (tmp_path / "AAOI").mkdir()
    (tmp_path / "AAOI" / "earnings-debrief.md").write_text("debrief body", encoding="utf-8")
    assert dispatch.read_debrief(str(tmp_path), "AAOI") == "debrief body"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: FAIL — `AttributeError: module 'dispatch' has no attribute 'load_state'`.

- [ ] **Step 3: Add the helpers to `scripts/dispatch.py`**

Add these imports to the top of the file (below the existing `import re`):

```python
import json
from datetime import datetime
from pathlib import Path
```

Append these functions after `quarter_already_logged`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: PASS (23 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/dispatch.py scripts/tests/test_dispatch.py
git commit -m "feat(dispatch): gate-state persistence + fs helpers"
```

---

### Task 4: Finnhub client

A thin `urllib` wrapper over the two Finnhub endpoints, with an injectable opener so tests never hit the network.

**Files:**
- Modify: `scripts/dispatch.py`
- Modify: `scripts/tests/test_dispatch.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `FinnhubClient(api_key, opener=None)` — `opener` defaults to `urllib.request.urlopen`; tests inject a fake.
    - `.earnings_calendar(symbol, frm, to) -> list` — the `earningsCalendar` array (`[]` on unexpected shape).
    - `.company_news(symbol, frm, to) -> list` — the news array (`[]` on unexpected shape).

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_dispatch.py`:

```python
import json as _json


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload.encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _fake_opener(state):
    def opener(req, timeout=None):
        state["url"] = req.full_url
        return _FakeResp(state["payload"])
    return opener


def test_earnings_calendar_parses_and_passes_symbol():
    state = {"payload": _json.dumps({"earningsCalendar": [{"date": "2026-07-17", "symbol": "COHR"}]})}
    client = dispatch.FinnhubClient("KEY", opener=_fake_opener(state))
    rows = client.earnings_calendar("COHR", "2026-07-17", "2026-07-18")
    assert rows == [{"date": "2026-07-17", "symbol": "COHR"}]
    assert "symbol=COHR" in state["url"]
    assert "/calendar/earnings" in state["url"]


def test_earnings_calendar_unexpected_shape_returns_empty():
    state = {"payload": _json.dumps([])}  # not a dict
    client = dispatch.FinnhubClient("KEY", opener=_fake_opener(state))
    assert client.earnings_calendar("COHR", "2026-07-17", "2026-07-18") == []


def test_company_news_parses_list():
    state = {"payload": _json.dumps([{"headline": "Wins contract"}])}
    client = dispatch.FinnhubClient("KEY", opener=_fake_opener(state))
    news = client.company_news("AAOI", "2026-07-15", "2026-07-18")
    assert news == [{"headline": "Wins contract"}]
    assert "/company-news" in state["url"]


def test_company_news_unexpected_shape_returns_empty():
    state = {"payload": _json.dumps({"error": "nope"})}  # not a list
    client = dispatch.FinnhubClient("KEY", opener=_fake_opener(state))
    assert client.company_news("AAOI", "2026-07-15", "2026-07-18") == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: FAIL — `AttributeError: module 'dispatch' has no attribute 'FinnhubClient'`.

- [ ] **Step 3: Add the client to `scripts/dispatch.py`**

Add these imports to the top of the file:

```python
import urllib.parse
import urllib.request
```

Append after `read_debrief`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: PASS (27 tests total).

- [ ] **Step 5: Commit**

```bash
git add scripts/dispatch.py scripts/tests/test_dispatch.py
git commit -m "feat(dispatch): Finnhub client with injectable opener"
```

---

### Task 5: Orchestration, summary, and CLI

Wires the pieces into `run()` (the per-ticker decision loop), `render_summary()`, `dispatch_workflow()`, `DEFAULT_KEYWORDS`, and `main()`. `run()` takes an injected client and an injected `dispatch` callable, so the loop is fully testable with no network and no `gh`.

**Files:**
- Modify: `scripts/dispatch.py`
- Modify: `scripts/tests/test_dispatch.py`

**Interfaces:**
- Consumes: `material_headlines`, `should_scan_news`, `earnings_due`, `quarter_already_logged`, `_parse_dt`, `list_tickers`, `read_debrief`, `FinnhubClient`, `load_state`, `save_state`.
- Produces:
  - `dispatch_workflow(workflow_file, ticker, dry_run=False) -> bool` — runs `gh workflow run <file> -f ticker=<T>`; `dry_run` skips the call and returns True.
  - `run(tickers_dir, client, state, now, keywords, dispatch=dispatch_workflow, dry_run=False) -> list of (ticker, earnings_cell, news_cell, reason)` — mutates `state` in place on a fired scan (unless `dry_run`).
  - `render_summary(rows) -> str` — Markdown table.
  - `DEFAULT_KEYWORDS` — list of materiality keywords.
  - `main(argv=None) -> int`.

- [ ] **Step 1: Write the failing tests**

Append to `scripts/tests/test_dispatch.py`:

```python
class _FakeClient:
    def __init__(self, earnings=None, news=None):
        self._earnings = earnings or {}
        self._news = news or {}

    def earnings_calendar(self, symbol, frm, to):
        return self._earnings.get(symbol, [])

    def company_news(self, symbol, frm, to):
        return self._news.get(symbol, [])


def _make_tickers(tmp_path, names):
    for n in names:
        (tmp_path / n).mkdir()
        (tmp_path / n / "news.md").write_text("state", encoding="utf-8")
    return str(tmp_path)


def test_run_dispatches_whats_new_on_material_news(tmp_path):
    tdir = _make_tickers(tmp_path, ["AAOI"])
    client = _FakeClient(news={"AAOI": [{"headline": "AAOI wins hyperscaler contract"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    fired = []
    rows = dispatch.run(tdir, client, {}, now, dispatch.DEFAULT_KEYWORDS,
                        dispatch=lambda wf, t, dry_run=False: fired.append((wf, t)) or True)
    assert ("whats-new.yml", "AAOI") in fired
    assert rows[0][2] == "dispatched"


def test_run_dispatches_earnings_when_quarter_new(tmp_path):
    tdir = _make_tickers(tmp_path, ["COHR"])
    client = _FakeClient(earnings={"COHR": [{"date": "2026-07-17", "symbol": "COHR"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    fired = []
    dispatch.run(tdir, client, {}, now, dispatch.DEFAULT_KEYWORDS,
                 dispatch=lambda wf, t, dry_run=False: fired.append((wf, t)) or True)
    assert ("earnings-digest.yml", "COHR") in fired


def test_run_skips_earnings_when_quarter_already_logged(tmp_path):
    tdir = _make_tickers(tmp_path, ["COHR"])
    (tmp_path / "COHR" / "earnings-debrief.md").write_text("reported 2026-07-17", encoding="utf-8")
    client = _FakeClient(earnings={"COHR": [{"date": "2026-07-17", "symbol": "COHR"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    fired = []
    dispatch.run(tdir, client, {}, now, dispatch.DEFAULT_KEYWORDS,
                 dispatch=lambda wf, t, dry_run=False: fired.append((wf, t)) or True)
    assert fired == []


def test_run_rate_caps_and_records_state(tmp_path):
    tdir = _make_tickers(tmp_path, ["AAOI"])
    client = _FakeClient(news={"AAOI": [{"headline": "AAOI guidance raised"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    state = {"AAOI": {"last_news_scan": (now - timedelta(hours=5)).isoformat()}}
    fired = []
    rows = dispatch.run(tdir, client, state, now, dispatch.DEFAULT_KEYWORDS,
                        dispatch=lambda wf, t, dry_run=False: fired.append((wf, t)) or True)
    assert fired == []
    assert "rate-capped" in rows[0][3]


def test_run_updates_state_on_fire(tmp_path):
    tdir = _make_tickers(tmp_path, ["AAOI"])
    client = _FakeClient(news={"AAOI": [{"headline": "AAOI wins contract"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    state = {}
    dispatch.run(tdir, client, state, now, dispatch.DEFAULT_KEYWORDS,
                 dispatch=lambda wf, t, dry_run=False: True)
    assert state["AAOI"]["last_news_scan"] == now.isoformat()


def test_run_dry_run_does_not_mutate_state(tmp_path):
    tdir = _make_tickers(tmp_path, ["AAOI"])
    client = _FakeClient(news={"AAOI": [{"headline": "AAOI wins contract"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    state = {}
    dispatch.run(tdir, client, state, now, dispatch.DEFAULT_KEYWORDS,
                 dispatch=lambda wf, t, dry_run=False: True, dry_run=True)
    assert state == {}


def test_run_isolates_per_ticker_errors(tmp_path):
    tdir = _make_tickers(tmp_path, ["AAOI", "BOOM"])

    class _Boom(_FakeClient):
        def company_news(self, symbol, frm, to):
            if symbol == "BOOM":
                raise RuntimeError("api down")
            return super().company_news(symbol, frm, to)

    client = _Boom(news={"AAOI": [{"headline": "AAOI wins contract"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    fired = []
    rows = dispatch.run(tdir, client, {}, now, dispatch.DEFAULT_KEYWORDS,
                        dispatch=lambda wf, t, dry_run=False: fired.append((wf, t)) or True)
    assert ("whats-new.yml", "AAOI") in fired          # AAOI still processed
    boom_row = [r for r in rows if r[0] == "BOOM"][0]
    assert "news error" in boom_row[3]


def test_render_summary_has_header_and_rows():
    rows = [("AAOI", "—", "dispatched", 'keyword: "contract" (1 headline(s))')]
    out = dispatch.render_summary(rows)
    assert "| Ticker | Earnings | What's-new | Reason |" in out
    assert "| AAOI | — | dispatched |" in out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: FAIL — `AttributeError: module 'dispatch' has no attribute 'DEFAULT_KEYWORDS'`.

- [ ] **Step 3: Add orchestration to `scripts/dispatch.py`**

Add these imports to the top of the file:

```python
import argparse
import os
import subprocess
import sys
from datetime import timezone
```

Append after the `FinnhubClient` class:

```python
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
                dispatch("earnings-digest.yml", ticker, dry_run)
                earnings_cell = "dispatched"
                reasons.append("earnings reported %s" % report_date)
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
                dispatch("whats-new.yml", ticker, dry_run)
                news_cell = "dispatched"
                if not dry_run:
                    state.setdefault(ticker, {})["last_news_scan"] = now.isoformat()
            elif matched:
                news_cell = "skipped"
        except Exception as exc:  # noqa: BLE001
            reasons.append("news error: %s" % exc)

        rows.append((ticker, earnings_cell, news_cell, "; ".join(reasons)))
    return rows


def render_summary(rows):
    """Render the decision rows as a Markdown table for the Actions summary."""
    lines = ["| Ticker | Earnings | What's-new | Reason |",
             "| --- | --- | --- | --- |"]
    for ticker, earnings_cell, news_cell, reason in rows:
        lines.append("| %s | %s | %s | %s |" % (ticker, earnings_cell, news_cell, reason))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic equity-watch dispatcher.")
    ap.add_argument("--tickers-dir", default="tickers")
    ap.add_argument("--state-file", default=".dispatch-state/state.json")
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
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as fh:
            fh.write("## Dispatcher run (%s)\n\n%s\n" % (now.date().isoformat(), summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: PASS (35 tests total).

- [ ] **Step 5: Smoke-test the CLI wiring locally**

Run: `FINNHUB_API_KEY=dummy python3 scripts/dispatch.py --dry-run --tickers-dir tickers`
Expected: prints a Markdown table with a row per ticker. (Rows will show `news error`/`earnings error` because `dummy` is rejected by Finnhub — that is the per-ticker isolation working, not a crash. Exit code 0.)

- [ ] **Step 6: Commit**

```bash
git add scripts/dispatch.py scripts/tests/test_dispatch.py
git commit -m "feat(dispatch): orchestration loop, summary, and CLI"
```

---

### Task 6: Scheduled workflow + gitignore + docs

Adds the GitHub Actions workflow that runs the dispatcher on a cron, wires the Actions-cache state, ignores the local state dir, and documents the required secret.

**Files:**
- Create: `.github/workflows/dispatcher.yml`
- Modify: `.gitignore`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add the state dir to `.gitignore`**

Append to `.gitignore`:

```
# Dispatcher gate-state (lives only in the Actions cache; never committed)
.dispatch-state/
```

- [ ] **Step 2: Create `.github/workflows/dispatcher.yml`**

```yaml
name: Dispatcher (deterministic triggers)

# Runs a deterministic Python pre-filter (scripts/dispatch.py, NO Claude) on a
# weekday-morning cron. For each watched ticker under tickers/*/ it decides,
# using cheap Finnhub calls, whether an earnings-digest and/or a what's-new scan
# is warranted, then fires the existing heavy workflow via `gh workflow run`.
# Earnings: dispatched the morning after a Finnhub-calendar report, deduped by
# reading tickers/<T>/earnings-debrief.md. What's-new: a keyword-filtered news
# gate with a 48h per-ticker rate cap; gate state lives in the Actions cache
# (never committed to main). See
# docs/superpowers/specs/2026-07-18-dispatcher-triggers-design.md.

on:
  schedule:
    - cron: '30 13 * * 1-5'   # ~09:30 ET, weekdays; catches prior-day AMC + same-morning BMO
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Print the decision table without dispatching or saving state'
        type: boolean
        default: false

permissions:
  contents: read
  actions: write            # required for `gh workflow run` to dispatch the heavy workflows

concurrency:
  group: dispatcher
  cancel-in-progress: false

jobs:
  dispatch:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Restore gate state
        uses: actions/cache/restore@v4
        with:
          path: .dispatch-state
          key: dispatch-state-v1-${{ github.run_id }}
          restore-keys: |
            dispatch-state-v1-

      - name: Run dispatcher
        env:
          FINNHUB_API_KEY: ${{ secrets.FINNHUB_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          set -euo pipefail
          python3 scripts/dispatch.py ${{ inputs.dry_run && '--dry-run' || '' }}

      - name: Save gate state
        if: always()
        uses: actions/cache/save@v4
        with:
          path: .dispatch-state
          key: dispatch-state-v1-${{ github.run_id }}
```

- [ ] **Step 3: Validate the workflow YAML parses**

Run: `python3 -c "import yaml, sys; yaml.safe_load(open('.github/workflows/dispatcher.yml')); print('yaml ok')"`
Expected: `yaml ok`. (If `yaml` is unavailable locally, instead run `gh workflow list` after pushing, or `actionlint .github/workflows/dispatcher.yml` if installed.)

- [ ] **Step 4: Document the new secret in `CLAUDE.md`**

In `CLAUDE.md`, under the File map, add a bullet after the `scripts/notify_discord_ticker.py` entry:

```markdown
- `scripts/dispatch.py` + `.github/workflows/dispatcher.yml` — the **deterministic dispatcher**: a scheduled (weekday-morning cron), Claude-free Python pre-filter that decides which watched tickers warrant a paid run and fires the existing `earnings-digest.yml` / `whats-new.yml` via `gh workflow run`. **Earnings** dispatch the morning after a Finnhub earnings-calendar report, deduped by reading `tickers/<T>/earnings-debrief.md` (so a state loss can never double-digest a quarter); the two foreign names (IBIDY, LPKF) fall through to manual dispatch. **What's-new** dispatch on a keyword-filtered Finnhub company-news gate with a 48h per-ticker rate cap; the gate's only state (`last_news_scan` per ticker) lives in the **Actions cache**, never committed to `main`. Requires a `FINNHUB_API_KEY` repo secret (free tier). Every run writes a per-ticker dispatch/skip table to the Actions job summary.
```

- [ ] **Step 5: Run the full test suite one final time**

Run: `python3 -m pytest scripts/tests/test_dispatch.py -v`
Expected: PASS (35 tests).

- [ ] **Step 6: Commit**

```bash
git add .github/workflows/dispatcher.yml .gitignore CLAUDE.md
git commit -m "feat(dispatch): scheduled dispatcher workflow + docs"
```

---

## Post-implementation (manual, out of band)

These are not code steps — they are the human handoff to make the dispatcher live:

1. **Provision the secret:** `gh secret set FINNHUB_API_KEY` (free key from finnhub.io). Without it the workflow exits 1 with a clear message.
2. **Shakedown:** trigger `dispatcher.yml` manually with `dry_run: true` and confirm the job-summary table looks right (correct tickers, sensible reasons, foreign names showing "no calendar report") before trusting the cron.
3. **First real run:** trigger once with `dry_run: false`, confirm it dispatches only what you'd expect, then let the cron take over.

## Notes for the implementer

- **All functions live in one module** (`scripts/dispatch.py`) — this matches the house pattern (`notify_discord_ticker.py` is likewise one module). Later tasks *modify* the file created in Task 1; add imports at the top as each task calls for them (duplicate `import` lines are harmless, but keep them consolidated at the top).
- **The em-dash** in `run()` and `render_summary` (`"—"`) is a literal UTF-8 character — the codebase already uses em-dashes (e.g. the Discord embed titles in `notify_discord_ticker.py`). Keep the file UTF-8.
- **`inputs.dry_run` on a `schedule` trigger** is empty, so `${{ inputs.dry_run && '--dry-run' || '' }}` correctly yields `''` on the cron path and `--dry-run` only when a human ticks the box.
- **Do not** add third-party deps or a `requirements.txt` for the script — it is stdlib only. `actions/setup-python` is used only to pin a predictable interpreter.
```

