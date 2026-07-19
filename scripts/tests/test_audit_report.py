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


def test_two_edge_negatives_escalate_rather_than_conclude(tmp_path):
    """A count is a proxy for pressure, never evidence the Edge changed.

    CIFR on the live corpus has two [EDGE−] entries whose own text says the
    Edge's core was corroborated -- a two-sided Edge can be confirmed at its
    core by an item cutting against one branch. Concluding RE-UNDERWRITE from
    the count alone produces a false positive on real data.
    """
    d = _mk(tmp_path, reports=("2026-07-10",),
            entries=[_entry("2026-07-12", extra="[EDGE−]"),
                     _entry("2026-07-13", extra="[EDGE−]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["verdict"] == "ESCALATE"
    assert r["notify"] is True
    assert "escalation_question" in r


def test_fired_tripwire_may_conclude_because_it_relays_an_assessment(tmp_path):
    """`fires` is a prior run's explicit call against the trigger, not an inference."""
    d = _mk(tmp_path, reports=("2026-07-10",),
            entries=[_entry("2026-07-12", extra="[TRIPWIRE #1 — fires]")])
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
    assert r["verdict"] == "ESCALATE"  # from the EDGE− pair, not the early-warning
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


def test_pinned_baseline_is_labelled_and_not_called_the_report_age(tmp_path):
    """A pinned baseline is the caller's date, not the report's.

    These evidence strings get quoted into a report's provenance block, so
    asserting "the report is Nd old" about a supplied date would put a false
    statement into the permanent record.
    """
    d = _mk(tmp_path, reports=("2026-07-18",),
            entries=[_entry("2026-03-01", tag="[Financials/Capital stack]")])
    real = ar.audit_ticker(d, TODAY)
    assert real["baseline_source"] == "latest-report"
    assert real["verdict"] == "CLEAN"  # 1-day-old report

    forced = ar.audit_ticker(d, TODAY, baseline="2026-01-01")
    assert forced["baseline_source"] == "pinned"
    assert forced["latest_report"] == "2026-07-18"
    assert not any("report is" in e for e in forced["evidence"]), \
        "must not assert the report's age from a caller-supplied baseline"
    assert any("pinned baseline" in e for e in forced["evidence"])


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


# --- tripwire expiry: dated windows, flagged-never-removed ------------------
#
# The trigger prose (verbatim from the report) carries only the `(n)` markers;
# expiry lives in its own `| # | Expires |` table below the prose, never as an
# inline annotation mid-sentence.

def _with_tripwires(root, prose, rows, **kw):
    """`prose` is the `(n) ...` blockquote text; `rows` is [(n, date_or_None), ...]."""
    d = _mk(root, **kw)
    news = d / "news.md"
    table = "\n\n| # | Expires |\n|---|---|\n" + "\n".join(
        f"| {n} | {date or ''} |" for n, date in rows)
    body = news.read_text(encoding="utf-8").replace(
        "## Recent News Log",
        "## Tripwires (pre-committed exit / re-underwrite triggers)\n"
        f"> {prose}" + table + "\n\n## Recent News Log")
    news.write_text(body, encoding="utf-8")
    return d


def test_expired_tripwire_escalates_and_notifies(tmp_path):
    d = _with_tripwires(tmp_path, "(1) first thing; (2) second thing.",
        [(1, "2026-06-30"), (2, "2027-06-30")], reports=("2026-07-10",))
    r = ar.audit_ticker(d, TODAY)  # today = 2026-07-19 > #1's window
    assert r["tripwires_expired"] == [1]
    assert r["verdict"] == "ESCALATE"
    assert r["notify"] is True
    assert any("EXPIRED" in e and "never silently" in e for e in r["evidence"])


def test_unexpired_tripwires_stay_silent(tmp_path):
    d = _with_tripwires(tmp_path, "(1) first thing; (2) second thing.",
        [(1, "2027-06-30"), (2, "2027-12-31")], reports=("2026-07-10",))
    r = ar.audit_ticker(d, TODAY)
    assert r["tripwires_expired"] == []
    assert r["verdict"] == "CLEAN"
    assert r["notify"] is False


def test_undated_tripwire_is_surfaced_not_guessed(tmp_path):
    d = _with_tripwires(tmp_path, "(1) dated thing; (2) undated thing.",
        [(1, "2027-06-30"), (2, None)], reports=("2026-07-10",))
    r = ar.audit_ticker(d, TODAY)
    assert r["tripwires_undated"] == [2]
    assert r["verdict"] == "CLEAN", "missing a date is hygiene, not staleness"
    assert any("no row" in e for e in r["evidence"])


def test_tripwire_with_no_table_row_at_all_is_also_undated(tmp_path):
    """A trigger the table simply omits is untracked, same as a blank cell."""
    d = _with_tripwires(tmp_path, "(1) dated thing; (2) forgotten thing.",
        [(1, "2027-06-30")], reports=("2026-07-10",))  # no row 2 at all
    r = ar.audit_ticker(d, TODAY)
    assert r["tripwires_undated"] == [2]


def test_fired_outranks_expired(tmp_path):
    d = _with_tripwires(tmp_path, "(1) old window; (2) live one.",
        [(1, "2026-06-30"), (2, "2027-12-31")], reports=("2026-07-10",),
        entries=[_entry("2026-07-12", extra="[TRIPWIRE #2 — fires]")])
    r = ar.audit_ticker(d, TODAY)
    assert r["verdict"] == "RE-UNDERWRITE"          # the fire wins the verdict
    assert r["tripwires_expired"] == [1]            # …but expiry still surfaces
    assert any("EXPIRED" in e for e in r["evidence"])


# --- hygiene ---------------------------------------------------------------

def test_canonical_link_drift_is_reported(tmp_path):
    d = _mk(tmp_path, reports=("2026-01-10", "2026-07-01"), canonical="2026-01-10")
    r = ar.audit_ticker(d, TODAY)
    assert r["drift"] == {"linked": "2026-01-10", "latest": "2026-07-01"}


def test_missing_news_or_report_is_not_covered(tmp_path):
    d = tmp_path / "tickers" / "GAP"
    d.mkdir(parents=True)
    assert ar.audit_ticker(d, TODAY)["verdict"] == "NOT-COVERED"
