import pathlib
import sys
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import audit_notify as an  # noqa: E402

TODAY = date(2026, 7, 19)


def _r(ticker="TST", verdict="ESCALATE", notify=True, **kw):
    base = {"ticker": ticker, "verdict": verdict, "notify": notify,
            "evidence": ["something dated"], "work_streams": [], "drift": None}
    base.update(kw)
    return base


# --- suppression ------------------------------------------------------------

def test_clean_and_unforced_is_silent(tmp_path):
    post, why = an.should_notify(_r(verdict="CLEAN", notify=False), None, TODAY)
    assert post is False
    assert "clean" in why


def test_first_sighting_posts(tmp_path):
    post, _ = an.should_notify(_r(), None, TODAY)
    assert post is True


def test_same_verdict_inside_window_is_suppressed():
    prior = {"verdict": "ESCALATE", "last_posted": "2026-07-10"}
    post, why = an.should_notify(_r(verdict="ESCALATE"), prior, TODAY)
    assert post is False
    assert "suppressed" in why


def test_same_verdict_after_window_speaks_again():
    prior = {"verdict": "ESCALATE", "last_posted": "2026-06-01"}
    post, why = an.should_notify(_r(verdict="ESCALATE"), prior, TODAY)
    assert post is True
    assert "window elapsed" in why


def test_escalation_always_breaks_suppression():
    """The exception that makes the window safe: getting worse always speaks."""
    prior = {"verdict": "ESCALATE", "last_posted": "2026-07-18"}  # yesterday
    post, why = an.should_notify(_r(verdict="RE-UNDERWRITE"), prior, TODAY)
    assert post is True
    assert "escalated" in why


def test_de_escalation_still_reports_the_change():
    prior = {"verdict": "RE-UNDERWRITE", "last_posted": "2026-07-18"}
    post, why = an.should_notify(_r(verdict="REFRESH"), prior, TODAY)
    assert post is True
    assert "changed" in why


def test_early_warning_forces_a_post_on_a_clean_verdict():
    """§J.5: verdict and notification are separate outputs."""
    post, _ = an.should_notify(_r(verdict="CLEAN", notify=True), None, TODAY)
    assert post is True


def test_corrupt_state_does_not_crash(tmp_path):
    p = tmp_path / "seen.json"
    p.write_text("{not json", encoding="utf-8")
    assert an.load_state(p) == {}


def test_unusable_last_posted_date_speaks_rather_than_swallowing():
    prior = {"verdict": "ESCALATE"}  # no last_posted at all
    post, why = an.should_notify(_r(), prior, TODAY)
    assert post is True
    assert "no usable" in why


# --- message content --------------------------------------------------------

def test_message_carries_verdict_evidence_and_the_exact_command():
    body = an.render_ticker_message(
        _r(ticker="CIFR", verdict="REFRESH", baseline="2026-07-15",
           evidence=["2 quarters reported since 2026-07-15"],
           work_streams=["filing", "sector"]))
    assert "CIFR — REFRESH" in body
    assert "2 quarters reported since 2026-07-15" in body
    assert "/deep-dive CIFR" in body
    assert "filing, sector" in body


def test_message_states_that_tripwires_are_not_touched():
    """The reader must know a re-run does not silently rewrite their triggers."""
    body = an.render_ticker_message(_r(verdict="RE-UNDERWRITE", baseline="2026-01-01"))
    assert "not touched until you promote them" in body


def test_escalate_message_carries_the_judgment_question():
    body = an.render_ticker_message(
        _r(verdict="ESCALATE", escalation_question="Falsified or merely pressured?"))
    assert "Falsified or merely pressured?" in body


def test_rollup_is_written_even_for_a_fully_clean_run():
    results = [_r(ticker="AAA", verdict="CLEAN", notify=False)]
    decisions = {"AAA": (False, "clean and nothing forced a notify")}
    out = an.render_rollup(results, decisions, TODAY)
    assert "AAA" in out and "CLEAN" in out
    assert "1 audited · 0 posted · 1 clean" in out
