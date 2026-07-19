import pathlib
import sys
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import audit_report as ar  # noqa: E402

TODAY = date(2026, 7, 19)

_HEADER = """---
company: "T Co"
blurb: "b"
---
# T

**Canonical deep-dive:** [report](reports/{canonical}.md)

Edge: something variant.

## Recent News Log

Tag `[TRIPWIRE #n — fires]` / `[EDGE+]` / `[EDGE−]` only when it applies.

"""


def _mk(root, sym="TST", reports=("2026-01-10",), entries=(), canonical=None,
        quarters=()):
    """A ticker folder. `entries` are raw log lines; `quarters` are debrief dates."""
    d = root / "tickers" / sym
    d.mkdir(parents=True)
    body = _HEADER.format(canonical=canonical or (reports[-1] if reports else "x"))
    body += "\n".join(entries)
    (d / "news.md").write_text(body, encoding="utf-8")
    if reports:
        (d / "reports").mkdir()
        for r in reports:
            (d / "reports" / f"{r}.md").write_text("x", encoding="utf-8")
    if quarters:
        (d / "earnings-debrief.md").write_text(
            "\n".join(f"## FY26 Q{i} — reported {q}" for i, q in enumerate(quarters, 1)),
            encoding="utf-8",
        )
    return d


def _entry(when, tag="[Financials/Capital stack]", extra=""):
    return f"- {when} — {tag} **Thing happened**. Detail → impact. {extra}"


# --- routing ---------------------------------------------------------------

def test_fired_tripwire_routes_to_reunderwrite(tmp_path):
    d = _mk(tmp_path, entries=[_entry("2026-02-01", extra="[TRIPWIRE #2 — fires]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["verdict"] == "RE-UNDERWRITE"
    assert r["tripwires_fired"] == [2]
    assert r["notify"] is True


def test_two_edge_negatives_route_to_reunderwrite(tmp_path):
    d = _mk(tmp_path, entries=[_entry("2026-02-01", extra="[EDGE−]"),
                               _entry("2026-02-02", extra="[EDGE−]")])
    assert ar.audit_ticker(d, TODAY)["verdict"] == "RE-UNDERWRITE"


def test_one_edge_negative_does_not_escalate(tmp_path):
    d = _mk(tmp_path, reports=("2026-07-10",),
            entries=[_entry("2026-07-12", extra="[EDGE−]")])
    assert ar.audit_ticker(d, TODAY)["verdict"] == "CLEAN"


def test_two_quarters_route_to_refresh(tmp_path):
    d = _mk(tmp_path, reports=("2026-07-10",),
            quarters=("2026-07-12", "2026-07-15"))
    assert ar.audit_ticker(d, TODAY)["verdict"] == "REFRESH"


# --- the false-positive guard this tier exists for -------------------------

def test_does_not_fire_is_not_a_fire(tmp_path):
    # Recent report on purpose: age/unincorporated would otherwise route to
    # REFRESH on their own and mask what this test is actually asserting.
    d = _mk(tmp_path, reports=("2026-07-10",), entries=[
        _entry("2026-07-12", extra="[TRIPWIRE #4 — reaffirmed, does not fire]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["tripwires_fired"] == []
    assert r["verdict"] == "CLEAN"
    assert r["notify"] is False, "a checked-and-not-fired tripwire is silent"


def test_touched_not_sustained_is_not_a_fire(tmp_path):
    d = _mk(tmp_path, entries=[
        _entry("2026-02-01", extra="[TRIPWIRE #4 — touched, not sustained]")])
    assert ar.audit_ticker(d, TODAY)["tripwires_fired"] == []


def test_log_header_boilerplate_is_not_an_entry(tmp_path):
    """The header note documents the tag format and contains the word 'fires'."""
    d = _mk(tmp_path, entries=[])
    r = ar.audit_ticker(d, TODAY)
    assert r["unincorporated"] == 0
    assert r["tripwires_fired"] == []


# --- early-warning: alerts, never escalates (Section J decision) -----------

def test_early_warning_stays_clean_but_forces_notify(tmp_path):
    d = _mk(tmp_path, reports=("2026-07-10",), entries=[
        _entry("2026-07-12", extra="[TRIPWIRE #3 — early-warning, closing in]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["verdict"] == "CLEAN", "early-warning must not escalate the route"
    assert r["notify"] is True, "…but must break the silent-when-CLEAN rule"
    assert r["tripwires_early_warning"] == [3]


def test_early_warning_rides_along_on_an_independent_verdict(tmp_path):
    d = _mk(tmp_path, entries=[
        _entry("2026-02-01", extra="[EDGE−]"), _entry("2026-02-02", extra="[EDGE−]"),
        _entry("2026-02-03", extra="[TRIPWIRE #1 — early-warning]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["verdict"] == "RE-UNDERWRITE"
    assert any("early-warning" in e for e in r["evidence"])


# --- ordering inversion: the failure that reads as "all clear" -------------

def test_baseline_pins_the_comparison_date(tmp_path):
    """With a newer report on disk the default baseline hides everything."""
    d = _mk(tmp_path, reports=("2026-01-10", "2026-07-19"),
            entries=[_entry("2026-02-01", extra="[TRIPWIRE #2 — fires]")],
            canonical="2026-07-19")
    assert ar.audit_ticker(d, TODAY)["verdict"] == "CLEAN"
    pinned = ar.audit_ticker(d, TODAY, baseline="2026-01-10")
    assert pinned["verdict"] == "RE-UNDERWRITE"
    assert pinned["tripwires_fired"] == [2]


def test_idempotent(tmp_path):
    d = _mk(tmp_path, entries=[_entry("2026-02-01", extra="[EDGE−]")])
    assert ar.audit_ticker(d, TODAY) == ar.audit_ticker(d, TODAY)


# --- work order ------------------------------------------------------------

def test_work_streams_derived_from_framework_tags(tmp_path):
    d = _mk(tmp_path, reports=("2026-04-01",), entries=[
        _entry("2026-04-10", tag="[Moat/Competition]"),
        _entry("2026-04-11", tag="[Financials/Capital stack]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["verdict"] == "REFRESH"
    assert r["work_streams"] == ["competitive-landscape", "filing"]


def test_past_horizon_dispatches_all_four(tmp_path):
    d = _mk(tmp_path, reports=("2025-12-01",),
            entries=[_entry("2026-01-05", tag="[Moat/Competition]")])
    r = ar.audit_ticker(d, TODAY)
    assert len(r["work_streams"]) == 4
    assert any("horizon" in e for e in r["evidence"])


# --- hygiene ---------------------------------------------------------------

def test_canonical_link_drift_is_reported(tmp_path):
    d = _mk(tmp_path, reports=("2026-01-10", "2026-07-01"), canonical="2026-01-10")
    r = ar.audit_ticker(d, TODAY)
    assert r["drift"] == {"linked": "2026-01-10", "latest": "2026-07-01"}


def test_missing_news_or_report_is_not_covered(tmp_path):
    d = tmp_path / "tickers" / "GAP"
    d.mkdir(parents=True)
    assert ar.audit_ticker(d, TODAY)["verdict"] == "NOT-COVERED"
