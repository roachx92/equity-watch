"""Tests for scripts/tripwire_check.py — offline; `facts.facts` is monkeypatched.

The three guards that stop this from becoming a shadow pre-commitment are what
these tests are really for:
  1. a hedged threshold near its boundary must return INCONCLUSIVE, not a verdict
  2. `context` items are reported, never evaluated
  3. a trigger with no evaluable clauses reports MANUAL, never "clean"
"""
import sys
import pathlib

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import tripwire_check as tc  # noqa: E402

FY_END = "2026-06-30"


@pytest.fixture
def wired(monkeypatch):
    def go(val, *, instantaneous=False, start="2025-07-01", end=FY_END):
        row = {
            "start": None if instantaneous else start,
            "end": end,
            "val": val,
            "form": "10-K",
            "filed": "2026-08-20",
            "accession": "0000820318-26-000099",
            "instantaneous": instantaneous,
        }
        monkeypatch.setattr(tc, "facts", lambda t, tag: ([row], "USD"))
        monkeypatch.setattr(tc, "select", lambda rows, **kw: rows)
    return go


def _clause(**kw):
    base = {"id": "ocf", "label": "OCF below ~$300M", "tag": "ocf",
            "period": "annual", "op": "<", "threshold": 300_000_000, "hedged": False}
    base.update(kw)
    return base


def test_fires_when_threshold_is_breached(wired):
    wired(250_000_000)
    r = tc.evaluate_clause("COHR", _clause(), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.FIRES


def test_does_not_fire_when_clear(wired):
    wired(633_600_000)
    r = tc.evaluate_clause("COHR", _clause(), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.NOT_FIRED


def test_hedged_threshold_near_boundary_is_inconclusive(wired):
    """'roughly $300M' must not resolve FIRES at 299 and NOT-FIRE at 301."""
    wired(299_000_000)
    r = tc.evaluate_clause("COHR", _clause(hedged=True), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.INCONCLUSIVE
    assert "hedge band" in r["reason"]


def test_unhedged_threshold_near_boundary_is_decisive(wired):
    """An exact figure from a filing (inventory) gets a real verdict."""
    wired(299_000_000)
    r = tc.evaluate_clause("COHR", _clause(hedged=False), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.FIRES


def test_hedge_band_is_symmetric(wired):
    wired(301_000_000)
    r = tc.evaluate_clause("COHR", _clause(hedged=True), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.INCONCLUSIVE


def test_value_outside_hedge_band_still_decides(wired):
    wired(200_000_000)
    r = tc.evaluate_clause("COHR", _clause(hedged=True), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.FIRES


def test_unfiled_period_is_inconclusive_not_clean(monkeypatch):
    """Before the 10-K lands there is no fact; that must never read as 'clear'."""
    monkeypatch.setattr(tc, "facts", lambda t, tag: ([], "USD"))
    monkeypatch.setattr(tc, "select", lambda rows, **kw: rows)
    r = tc.evaluate_clause("COHR", _clause(), FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.INCONCLUSIVE
    assert "filed yet" in r["reason"].lower()


def test_result_carries_a_filing_citation(wired):
    wired(250_000_000)
    r = tc.evaluate_clause("COHR", _clause(), FY_END, tc.DEFAULT_HEDGE)
    assert r["accession"] == "0000820318-26-000099"
    assert r["form"] == "10-K"


def test_instant_clause_matches_balance_sheet_date(wired):
    wired(2_200_000_000, instantaneous=True)
    r = tc.evaluate_clause(
        "COHR",
        _clause(tag="inventory", period="instant", op=">=", threshold=2_126_823_000),
        FY_END, tc.DEFAULT_HEDGE)
    assert r["verdict"] == tc.FIRES


def test_combine_any_prefers_fires_then_inconclusive():
    assert tc.combine([{"verdict": tc.NOT_FIRED}, {"verdict": tc.FIRES}], "any") == tc.FIRES
    assert tc.combine([{"verdict": tc.NOT_FIRED}, {"verdict": tc.INCONCLUSIVE}], "any") == tc.INCONCLUSIVE
    assert tc.combine([{"verdict": tc.NOT_FIRED}, {"verdict": tc.NOT_FIRED}], "any") == tc.NOT_FIRED


def test_combine_all_requires_every_clause():
    assert tc.combine([{"verdict": tc.FIRES}, {"verdict": tc.FIRES}], "all") == tc.FIRES
    assert tc.combine([{"verdict": tc.FIRES}, {"verdict": tc.NOT_FIRED}], "all") == tc.NOT_FIRED


def test_no_clauses_reports_manual_never_clean():
    """COHR #2 (customer concentration) has no tagged concept — silence != clear."""
    assert tc.combine([], "manual") == tc.MANUAL
    assert tc.combine([], "any") == tc.MANUAL


def test_fiscal_year_bounds_for_june_year_end():
    start, end = tc.fy_bounds(2026, "06-30")
    assert end == "2026-06-30"
    assert start == "2025-07-01"


def test_fiscal_year_bounds_for_calendar_year_end():
    start, end = tc.fy_bounds(2026, "12-31")
    assert (start, end) == ("2026-01-01", "2026-12-31")


def test_missing_checks_file_is_not_an_error(monkeypatch, tmp_path):
    monkeypatch.setattr(tc, "repo_root", lambda: tmp_path)
    res = tc.run("NOPE")
    assert res["checks"] is None
    assert "not configured" in res["note"]


def test_real_cohr_checks_file_parses_and_is_labelled_derived():
    """The committed checks.json must state it is not the pre-commitment."""
    cfg = tc.load_checks("COHR")
    assert cfg is not None
    assert "NOT THE PRE-COMMITMENT" in cfg["_note"].upper()
    assert cfg["fiscal_year_end"] == "06-30"
    tw = {c["tripwire"] for c in cfg["checks"]}
    assert {1, 2} <= tw
    # #2 must be explicitly manual, never silently evaluable
    two = next(c for c in cfg["checks"] if c["tripwire"] == 2)
    assert two["fires_when"] == "manual"
    assert two["clauses"] == []


def test_cohr_inventory_threshold_matches_the_tripwire_text():
    """Guards the encoding against drifting from the prose it mirrors."""
    cfg = tc.load_checks("COHR")
    one = next(c for c in cfg["checks"] if c["tripwire"] == 1)
    inv = next(c for c in one["clauses"] if c["id"] == "inventory")
    assert inv["threshold"] == 2_126_823_000       # $2,126.8M in the trigger text
    assert "2,126.8" in one["quote"]
    ocf = next(c for c in one["clauses"] if c["id"] == "ocf")
    assert ocf["threshold"] == 300_000_000
    assert ocf["hedged"] is True                    # the trigger says "roughly"
