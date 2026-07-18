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
