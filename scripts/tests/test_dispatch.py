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
    assert reason == "rate-capped until 2026-07-20 03:30Z"


def test_should_scan_news_fires_after_48h():
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    last = now - timedelta(hours=49)
    matched = [("Wins contract", "contract")]
    should, _ = dispatch.should_scan_news(matched, last, now)
    assert should is True


from datetime import date


def test_earnings_due_returns_recent_report_in_window():
    rows = [{"date": "2026-07-17", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 18)) == "2026-07-17"


def test_earnings_due_returns_today_report():
    rows = [{"date": "2026-07-18", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 18)) == "2026-07-18"


def test_earnings_due_ignores_reports_outside_window():
    # Just past the look-back edge (today-5) and far in the future are both out.
    rows = [{"date": "2026-07-13", "symbol": "COHR"}, {"date": "2026-11-05", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 18)) is None


def test_earnings_due_catches_friday_amc_on_monday():
    # The gap this look-back fixes: a Friday-after-market report (2026-07-17,
    # a Friday) caught by Monday's run (2026-07-20). A bare [today-1, today]
    # window {Sun, Mon} would miss it.
    rows = [{"date": "2026-07-17", "symbol": "COHR"}]
    assert dispatch.earnings_due(rows, date(2026, 7, 20)) == "2026-07-17"


def test_earnings_due_window_lower_bound_inclusive():
    # today-LOOKBACK is inside the window; today-(LOOKBACK+1) is not.
    today = date(2026, 7, 18)
    edge = (today - timedelta(days=dispatch.EARNINGS_LOOKBACK_DAYS)).isoformat()
    beyond = (today - timedelta(days=dispatch.EARNINGS_LOOKBACK_DAYS + 1)).isoformat()
    assert dispatch.earnings_due([{"date": edge}], today) == edge
    assert dispatch.earnings_due([{"date": beyond}], today) is None


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


def test_quarter_already_logged_ignores_date_outside_heading():
    # The report date appears only in non-heading lines (methodology / deep-dive
    # link) — must NOT count as logged. The prior quarter's heading date must.
    debrief = (
        "## Q1 2026 — reported 2026-05-07 (after close)\n\n"
        "Sources retrieved and digest written 2026-07-17.\n"
        "Canonical deep-dive: reports/2026-07-17.md\n"
    )
    assert dispatch.quarter_already_logged(debrief, "2026-07-17") is False
    assert dispatch.quarter_already_logged(debrief, "2026-05-07") is True


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
    (tmp_path / "COHR" / "earnings-debrief.md").write_text(
        "## Q4 FY2026 — reported 2026-07-17\n\nNumbers...\n", encoding="utf-8")
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


def test_run_dispatch_failure_marks_failed_and_does_not_arm_cap(tmp_path):
    tdir = _make_tickers(tmp_path, ["AAOI"])
    client = _FakeClient(news={"AAOI": [{"headline": "AAOI wins contract"}]})
    now = datetime(2026, 7, 18, 13, 30, tzinfo=UTC)
    state = {}
    rows = dispatch.run(tdir, client, state, now, dispatch.DEFAULT_KEYWORDS,
                        dispatch=lambda wf, t, dry_run=False: False)
    assert rows[0][2] == "dispatch-failed"
    assert state == {}  # 48h cap must NOT be armed when the dispatch failed


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


def test_render_summary_escapes_pipe_in_reason():
    rows = [("AAOI", "—", "skipped", "news error: bad|value")]
    out = dispatch.render_summary(rows)
    assert "bad\\|value" in out


def test_write_summary_file_writes_table_and_creates_parent(tmp_path):
    target = tmp_path / "nested" / "summary.md"
    dispatch.write_summary_file(str(target), "| Ticker | Earnings |\n| --- | --- |")
    assert target.read_text(encoding="utf-8") == "| Ticker | Earnings |\n| --- | --- |"


def test_dispatch_workflow_dry_run_returns_true_without_calling():
    assert dispatch.dispatch_workflow("whats-new.yml", "AAOI", dry_run=True) is True


def test_dispatch_workflow_returns_false_on_nonzero_exit(monkeypatch):
    class _Result:
        returncode = 1
        stderr = "gh: not authenticated"
    monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Result())
    assert dispatch.dispatch_workflow("whats-new.yml", "AAOI") is False


def test_dispatch_workflow_returns_true_on_zero_exit(monkeypatch):
    class _Result:
        returncode = 0
        stderr = ""
    monkeypatch.setattr(dispatch.subprocess, "run", lambda *a, **k: _Result())
    assert dispatch.dispatch_workflow("whats-new.yml", "AAOI") is True
