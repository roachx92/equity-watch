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
