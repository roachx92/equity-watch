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


def test_entry_date_single_date():
    assert tl.entry_date("- 2026-07-09 — [Tag] — **H**. x → y.") == "2026-07-09"


def test_entry_date_range_uses_the_end_date():
    """A range's content is 'as of' its later date — an entry that starts before
    a baseline but ends after it is post-baseline information, not pre-baseline.
    This is the CIFR case: '2026-07-09 to 2026-07-17' carrying an [EDGE−] was
    invisible to the staleness audit when keyed off the 7/9 start."""
    line = "- 2026-07-09 to 2026-07-17 — [Tag] — **H**. x → y. [EDGE−]"
    assert tl.entry_date(line) == "2026-07-17"


def test_entry_date_no_match_returns_none():
    assert tl.entry_date("not a bullet at all") is None


# --- sector lens (§K) -------------------------------------------------------

_SECTOR_DOC = """# T

## Edge
> variant view

## Sector lens
*Assigned per §K.1.*

- **`ai-optics` — sole.** Channels: **demand** and **supply**. Tripwire #3 is capex.
- **Deliberately excluded: industrial lasers.** No Tripwire turns on them.

## Tripwires
> (1) thing.
"""


def test_sector_slugs_reads_membership_bullets():
    assert tl.sector_slugs(_SECTOR_DOC) == ["ai-optics"]


def test_sector_slugs_ignores_exclusion_notes():
    """The 'deliberately excluded' / 'not a sector' notes explain what was
    considered and rejected -- they must not read as memberships."""
    assert "industrial" not in " ".join(tl.sector_slugs(_SECTOR_DOC))


def test_sector_slugs_handles_dual_membership_in_order():
    doc = _SECTOR_DOC.replace(
        "- **`ai-optics` — sole.** Channels: **demand** and **supply**. Tripwire #3 is capex.",
        "- **`ai-optics`.** Channels: **supply**.\n- **`catv-broadband`.** Channels: **demand**.")
    assert tl.sector_slugs(doc) == ["ai-optics", "catv-broadband"]


def test_sector_slugs_scoped_to_its_own_section():
    """A backticked slug quoted elsewhere in the file is not a membership."""
    doc = _SECTOR_DOC.replace("## Edge\n> variant view",
                              "## Edge\n- **`btc-mining`** is discussed here but not assigned.")
    assert tl.sector_slugs(doc) == ["ai-optics"]


def test_sector_slugs_absent_section_returns_empty():
    assert tl.sector_slugs("# T\n\n## Edge\n> x\n") == []


def test_every_live_ticker_has_a_known_sector():
    """The corpus itself must satisfy §K.1 -- at least one, all in-vocabulary."""
    for d in tl.ticker_dirs():
        news = d / "news.md"
        if not news.is_file():
            continue
        slugs = tl.sector_slugs(news.read_text(encoding="utf-8"))
        assert slugs, f"{d.name} has no sector assigned"
        for s in slugs:
            assert s in tl.SECTOR_SLUGS, f"{d.name}: unknown sector {s}"


def test_change_log_subsection_is_excluded_from_trigger_parsing():
    """§J.4's `### Change log` lives inside `## Tripwires` but is prose about
    past changes. It must be scoped out structurally, so a change-log line may
    contain a parenthesised in-sequence number without inventing a trigger."""
    doc = """# T

## Tripwires
- **(1)** first thing.
- **(2)** second thing.

| # | Expires |
|---|---|
| 1 | 2027-03-31 |
| 2 | 2027-06-30 |

### Change log
- **2026-07-19** — #2 sharpened. The prior bar (3) was not meaningful, and a
  successor trigger (4) was considered and rejected.

## Recent News Log
"""
    assert tl.tripwire_expiries(doc) == {1: "2027-03-31", 2: "2027-06-30"}
