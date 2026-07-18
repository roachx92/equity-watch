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
