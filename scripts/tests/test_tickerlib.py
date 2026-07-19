import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import tickerlib as tl  # noqa: E402


def _mk_ticker(root, sym, news=True, reports=()):
    d = root / "tickers" / sym
    d.mkdir(parents=True)
    if news:
        (d / "news.md").write_text(
            f'---\ncompany: "{sym} Co"\nblurb: "b"\n---\n# {sym}\n', encoding="utf-8"
        )
    if reports:
        (d / "reports").mkdir()
        for date in reports:
            (d / "reports" / f"{date}.md").write_text("x", encoding="utf-8")
    return d


def test_front_matter_parses_quoted_values(tmp_path):
    d = _mk_ticker(tmp_path, "ABC")
    fm = tl.front_matter(d / "news.md")
    assert fm["company"] == "ABC Co"
    assert fm["blurb"] == "b"


def test_front_matter_absent_returns_empty(tmp_path):
    p = tmp_path / "x.md"
    p.write_text("# no front matter\n", encoding="utf-8")
    assert tl.front_matter(p) == {}


def test_latest_report_date_picks_newest(tmp_path):
    d = _mk_ticker(tmp_path, "ABC", reports=("2026-07-14", "2026-07-17", "2026-01-02"))
    assert tl.latest_report_date(d) == "2026-07-17"


def test_latest_report_date_none_when_no_reports(tmp_path):
    d = _mk_ticker(tmp_path, "ABC")
    assert tl.latest_report_date(d) is None


def test_latest_report_ignores_non_date_files(tmp_path):
    d = _mk_ticker(tmp_path, "ABC", reports=("2026-07-14",))
    (d / "reports" / "notes.md").write_text("x", encoding="utf-8")
    assert tl.latest_report_date(d) == "2026-07-14"


def test_news_files_skips_folder_without_news(tmp_path):
    _mk_ticker(tmp_path, "ABC")
    _mk_ticker(tmp_path, "ZZZ", news=False)  # half-created
    files = tl.news_files(tmp_path)
    assert [f.parent.name for f in files] == ["ABC"]


def test_ticker_dirs_includes_half_created(tmp_path):
    _mk_ticker(tmp_path, "ABC")
    _mk_ticker(tmp_path, "ZZZ", news=False)
    assert [d.name for d in tl.ticker_dirs(tmp_path)] == ["ABC", "ZZZ"]


# --- assessment-tag grammar (§F.1) ----------------------------------------
# Polarity drives the staleness audit's routing, so the negative cases below
# are the load-bearing ones: a tripwire whose text says it did NOT fire must
# never classify as fired, or it dispatches an expensive re-underwrite.

def _tag(raw):
    line = f"- 2026-01-01 — [Sentiment] — **H**. detail → impact. Source: x. {raw}"
    tags = tl.parse_assessment_tags(line)
    assert len(tags) == 1, f"expected exactly one tag from {raw!r}, got {tags}"
    return tags[0]


def test_tripwire_does_not_fire_is_not_fired():
    t = _tag("[TRIPWIRE #4 — reaffirmed, does not fire]")
    assert t["polarity"] == "not-fired"
    assert t["number"] == 4


def test_tripwire_touched_not_sustained_is_not_fired():
    t = _tag("[TRIPWIRE #4 — touched, not sustained]")
    assert t["polarity"] == "not-fired"


def test_tripwire_fires_is_fired():
    assert _tag("[TRIPWIRE #2 — fires]")["polarity"] == "fired"


def test_tripwire_early_warning():
    assert _tag("[TRIPWIRE #3 — early-warning, management-downplayed]")["polarity"] == "early-warning"


def test_tripwire_live_unresolved_is_early_warning_not_fired():
    t = _tag("[TRIPWIRE #1 — live, unresolved]")
    assert t["polarity"] == "early-warning"
    assert t["legacy"] is True


def test_unrecognised_tripwire_status_is_none_not_fired():
    """Unclassifiable must be None so callers surface it, never assume a fire."""
    assert _tag("[TRIPWIRE #9 — something novel]")["polarity"] is None


def test_bare_tripwire_has_no_polarity_or_number():
    t = _tag("[TRIPWIRE]")
    assert t["polarity"] is None and t["number"] is None


def test_edge_signs_and_unicode_minus():
    assert _tag("[EDGE+]")["polarity"] == "positive"
    minus = _tag("[EDGE−]")          # U+2212, canonical
    assert minus["polarity"] == "negative" and minus["legacy"] is False
    ascii_minus = _tag("[EDGE-]")          # accepted, flagged
    assert ascii_minus["polarity"] == "negative" and ascii_minus["legacy"] is True


def test_edge_live_test_is_legacy_neutral_not_negative():
    """Legacy-only. Neutral routes to nothing, so it must not count toward the
    audit's >=2 EDGE- re-underwrite threshold, and must flag for canonicalising
    -- F.1 edges are binary."""
    t = _tag("[EDGE — live test, unresolved]")
    assert t["polarity"] == "neutral"
    assert t["legacy"] is True


def test_edge_qualifier_parses_but_is_legacy():
    """F.1 drops qualifiers: nuance belongs in the entry body, not the tag."""
    t = _tag("[EDGE+, tangential]")
    assert t["polarity"] == "positive"
    assert t["legacy"] is True


def test_multiple_tags_on_one_line():
    line = "- 2026-01-01 — [Tag] — **H**. x → y. [TRIPWIRE #1 — fires] [EDGE−]"
    got = {(t["kind"], t["polarity"]) for t in tl.parse_assessment_tags(line)}
    assert got == {("TRIPWIRE", "fired"), ("EDGE", "negative")}
