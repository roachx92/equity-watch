"""Tests for scripts/prices.py — all offline; no test here touches the network.

The behaviour that actually matters is the `settled` flag. Two wrong closes have
reached the Recent News Log by treating an intraday reading as a close, so the
live-bar cases below are the point of this file, not filler.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import prices  # noqa: E402

# 2026-07-29 13:30 UTC — a US session open (09:30 America/New_York, EDT = -14400).
JUL29_OPEN = 1785331800
DAY = 86400
EDT = -14400


def _result(stamps, closes, *, market_time=None, period_end=None, gmtoffset=EDT, **series):
    """Build a minimal Yahoo chart result. Only the fields prices.py reads."""
    meta = {"gmtoffset": gmtoffset, "currency": "USD", "fullExchangeName": "NYSE"}
    if market_time is not None:
        meta["regularMarketTime"] = market_time
    if period_end is not None:
        meta["currentTradingPeriod"] = {"regular": {"end": period_end}}
    quote = {"close": list(closes)}
    for key, vals in series.items():
        quote[key] = list(vals)
    quote.setdefault("open", [None] * len(closes))
    quote.setdefault("high", [None] * len(closes))
    quote.setdefault("low", [None] * len(closes))
    quote.setdefault("volume", [None] * len(closes))
    return {"meta": meta, "timestamp": list(stamps), "indicators": {"quote": [quote]}}


def test_symbol_override_maps_foreign_listing():
    # LPKF's folder name is the company; Yahoo wants the Xetra listing.
    assert prices.yahoo_symbol("LPKF") == "LPK.DE"
    assert prices.yahoo_symbol("lpkf") == "LPK.DE"


def test_symbol_defaults_to_the_ticker():
    assert prices.yahoo_symbol("COHR") == "COHR"
    assert prices.yahoo_symbol("cohr") == "COHR"


def test_bar_is_settled_when_market_has_closed():
    # regularMarketTime past the session end => that day's bar is a real close.
    r = _result([JUL29_OPEN], [222.05], market_time=JUL29_OPEN + 23400, period_end=JUL29_OPEN + 23400)
    rows, _ = prices.bars(r)
    assert rows[0]["settled"] is True


def test_current_session_bar_is_unsettled_while_trading():
    # Mid-session: last trade is BEFORE the period end, and the bar is today's.
    r = _result([JUL29_OPEN], [246.23], market_time=JUL29_OPEN + 7200, period_end=JUL29_OPEN + 23400)
    rows, _ = prices.bars(r)
    assert rows[0]["settled"] is False


def test_prior_days_stay_settled_even_while_today_trades():
    """The live-session flag must not leak backwards onto finished sessions."""
    r = _result(
        [JUL29_OPEN - DAY, JUL29_OPEN],
        [222.05, 246.23],
        market_time=JUL29_OPEN + 7200,
        period_end=JUL29_OPEN + 23400,
    )
    rows, _ = prices.bars(r)
    assert [x["settled"] for x in rows] == [True, False]


def test_pct_is_computed_from_closes_not_supplied():
    """The whole point: percentages derive from bars, never from a headline."""
    r = _result([JUL29_OPEN - DAY, JUL29_OPEN], [271.31, 243.33])
    rows, _ = prices.bars(r)
    assert "pct" not in rows[0]  # nothing to chain from
    assert rows[1]["pct"] == (243.33 / 271.31 - 1) * 100.0


def test_null_closes_are_dropped_not_zeroed():
    """Holidays/halts come back as null; a 0.0 close would fabricate a -100% move."""
    r = _result([JUL29_OPEN - DAY, JUL29_OPEN], [None, 243.33])
    rows, _ = prices.bars(r)
    assert len(rows) == 1
    assert rows[0]["close"] == 243.33


def test_dates_use_exchange_local_time_not_utc():
    """A Xetra bar opens 09:00 CEST = 07:00 UTC; naive UTC handling still lands on
    the same day here, but an exchange east of UTC would not, so shift explicitly."""
    # 2026-07-29 07:00 UTC, gmtoffset +7200 (CEST) -> local 09:00 on the 29th.
    stamp = 1785308400
    r = _result([stamp], [14.20], gmtoffset=7200)
    rows, _ = prices.bars(r)
    assert rows[0]["date"] == "2026-07-29"


def test_render_flags_the_unsettled_bar_loudly():
    r = _result(
        [JUL29_OPEN - DAY, JUL29_OPEN],
        [222.05, 246.23],
        market_time=JUL29_OPEN + 7200,
        period_end=JUL29_OPEN + 23400,
    )
    rows, meta = prices.bars(r)
    out = prices.render("COHR", rows, meta, None)
    assert "UNSETTLED" in out
    # and the warning block, so a reader pasting this into news.md sees why
    assert "never write it" in out.lower()


def test_render_summary_spans_settled_bars_only():
    r = _result(
        [JUL29_OPEN - DAY, JUL29_OPEN],
        [222.05, 246.23],
        market_time=JUL29_OPEN + 7200,
        period_end=JUL29_OPEN + 23400,
    )
    rows, meta = prices.bars(r)
    out = prices.render("COHR", rows, meta, None)
    # Only one settled bar => no misleading "settled range" line spanning the live one.
    assert "246.23)" not in out


def test_empty_result_renders_without_crashing():
    rows, meta = prices.bars(_result([], []))
    assert rows == []
    assert "no bars" in prices.render("COHR", rows, meta, None)
