"""Tests for scripts/facts.py — offline; `_get`/`resolve_cik` are monkeypatched.

The behaviour worth guarding is period **selection**: companyconcept reports the
same fiscal period many times (its own 10-K, then as a comparative in later
filings), so picking the wrong row silently yields a stale or restated number.
"""
import sys
import pathlib

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import facts  # noqa: E402


def _payload(rows, unit="USD"):
    return {"units": {unit: rows}}


@pytest.fixture
def wired(monkeypatch):
    def go(rows, unit="USD"):
        monkeypatch.setattr(facts, "resolve_cik", lambda t: 820318)
        monkeypatch.setattr(facts, "_get", lambda url, timeout=25: _payload(rows, unit))
    return go


def test_aliases_resolve_to_us_gaap_tags():
    assert facts.resolve_tag("inventory") == "InventoryNet"
    assert facts.resolve_tag("OCF") == "NetCashProvidedByUsedInOperatingActivities"
    assert facts.resolve_tag("capex") == "PaymentsToAcquirePropertyPlantAndEquipment"


def test_unknown_tag_passes_through_untouched():
    assert facts.resolve_tag("SomeCustomTag") == "SomeCustomTag"


def test_restatement_wins_latest_filed_for_same_period(wired):
    """Same period, two filings — the newer filing is the truth."""
    wired([
        {"start": None, "end": "2025-06-30", "val": 1_400_000_000,
         "form": "10-K", "filed": "2025-08-16", "accn": "OLD"},
        {"start": None, "end": "2025-06-30", "val": 1_437_636_000,
         "form": "10-Q", "filed": "2026-05-06", "accn": "NEW"},
    ])
    rows, unit = facts.facts("COHR", "inventory")
    assert len(rows) == 1
    assert rows[0]["val"] == 1_437_636_000
    assert rows[0]["accession"] == "NEW"
    assert unit == "USD"


def test_distinct_periods_are_both_kept(wired):
    wired([
        {"start": None, "end": "2025-06-30", "val": 1, "filed": "2025-08-16", "accn": "A"},
        {"start": None, "end": "2026-03-31", "val": 2, "filed": "2026-05-06", "accn": "B"},
    ])
    rows, _ = facts.facts("COHR", "inventory")
    assert [r["end"] for r in rows] == ["2026-03-31", "2025-06-30"]  # newest first


def test_rows_without_a_value_are_dropped(wired):
    wired([
        {"start": None, "end": "2026-03-31", "val": None, "filed": "2026-05-06", "accn": "A"},
        {"start": None, "end": "2025-06-30", "val": 5, "filed": "2025-08-16", "accn": "B"},
    ])
    rows, _ = facts.facts("COHR", "inventory")
    assert [r["val"] for r in rows] == [5]


def test_instantaneous_flag_distinguishes_stock_from_flow(wired):
    wired([
        {"start": None, "end": "2026-03-31", "val": 1, "filed": "2026-05-06", "accn": "A"},
        {"start": "2025-07-01", "end": "2026-03-31", "val": 2, "filed": "2026-05-06", "accn": "B"},
    ])
    rows, _ = facts.facts("COHR", "whatever")
    flags = {r["instantaneous"] for r in rows}
    assert flags == {True, False}


def test_months_spans():
    assert facts._months("2025-07-01", "2026-06-30") == 12
    assert facts._months("2025-07-01", "2025-09-30") == 3
    assert facts._months("2025-07-01", "2026-03-31") == 9


def test_annual_filter_keeps_only_year_length_durations(wired):
    wired([
        {"start": "2025-07-01", "end": "2026-06-30", "val": 1, "filed": "2026-08-01", "accn": "FY"},
        {"start": "2026-04-01", "end": "2026-06-30", "val": 2, "filed": "2026-08-01", "accn": "Q4"},
    ])
    rows, _ = facts.facts("COHR", "ocf")
    annual = facts.select(rows, annual=True)
    assert [r["accession"] for r in annual] == ["FY"]


def test_quarterly_filter_keeps_only_short_durations(wired):
    wired([
        {"start": "2025-07-01", "end": "2026-06-30", "val": 1, "filed": "2026-08-01", "accn": "FY"},
        {"start": "2026-04-01", "end": "2026-06-30", "val": 2, "filed": "2026-08-01", "accn": "Q4"},
    ])
    rows, _ = facts.facts("COHR", "ocf")
    q = facts.select(rows, quarterly=True)
    assert [r["accession"] for r in q] == ["Q4"]


def test_period_end_selects_an_exact_close(wired):
    wired([
        {"start": None, "end": "2026-06-30", "val": 1, "filed": "2026-08-01", "accn": "A"},
        {"start": None, "end": "2026-03-31", "val": 2, "filed": "2026-05-06", "accn": "B"},
    ])
    rows, _ = facts.facts("COHR", "inventory")
    got = facts.select(rows, period_end="2026-03-31")
    assert [r["accession"] for r in got] == ["B"]


def test_empty_units_returns_empty(wired):
    wired([])
    rows, unit = facts.facts("COHR", "inventory")
    assert rows == []
