"""Tests for scripts/crossref.py — offline, built on tmp_path ticker fixtures.

The invariant worth guarding is what this tool refuses to do: it surfaces an
event as a *candidate* for a slug-peer to assess, and never copies an entry or
its assessment across tickers (sector-lens.md §K.5 — impact is per-ticker and
signed).
"""
import sys
import pathlib

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import crossref  # noqa: E402

NEWS = """---
company: "{name}"
blurb: "b"
---
# {sym}

## Sector lens
{lens}

## Recent News Log
{entries}
"""


def _mk(root, sym, slugs, entries):
    d = root / "tickers" / sym
    d.mkdir(parents=True)
    lens = "\n".join(f"- **`{s}` — sole.** Channels: **demand**." for s in slugs)
    (d / "news.md").write_text(
        NEWS.format(name=f"{sym} Co", sym=sym, lens=lens, entries="\n".join(entries)),
        encoding="utf-8")
    return d


def _entry(date, slug, headline):
    tag = f"[Sector/{slug}]" if slug else "[Financials]"
    return f"- {date} — {tag} — **{headline}**. detail -> impact. Source: [X](http://x) ({date})."


@pytest.fixture
def corpus(tmp_path, monkeypatch):
    """Two ai-optics peers; one has an event the other lacks, one is shared."""
    _mk(tmp_path, "COHR", ["ai-optics"], [
        _entry("2026-07-29", "ai-optics", "Microsoft FY26 Q4 capex 41.0B up 70 percent"),
        _entry("2026-07-28", "ai-optics", "Innolight prices Hong Kong IPO at HKD 980 raising 53.4B"),
    ])
    _mk(tmp_path, "AAOI", ["ai-optics", "catv-broadband"], [
        _entry("2026-07-28", "ai-optics", "Zhongji InnoLight prices Hong Kong offering at HKD 980 raising"),
    ])
    _mk(tmp_path, "MSTR", ["btc-treasury"], [])
    monkeypatch.setattr(crossref, "ticker_dirs",
                        lambda root=None: sorted((tmp_path / "tickers").iterdir()))
    return tmp_path


def test_index_captures_slugs_and_entries(corpus):
    idx = crossref.index()
    assert idx["COHR"]["slugs"] == ["ai-optics"]
    assert idx["COHR"]["count"] == 2
    assert idx["COHR"]["newest"] == "2026-07-29"


def test_peers_only_includes_shared_slugs(corpus):
    p = crossref.peers(crossref.index())
    assert p["ai-optics"] == ["AAOI", "COHR"]
    assert "btc-treasury" not in p     # MSTR is alone
    assert "catv-broadband" not in p   # AAOI is alone in it


def test_gap_surfaces_peer_event_this_ticker_lacks(corpus):
    rows = crossref.gaps_for("AAOI", crossref.index())
    dates = [r["date"] for r in rows]
    assert "2026-07-29" in dates      # COHR's Microsoft entry
    assert "2026-07-28" not in dates  # AAOI already has that date+slug


def test_gap_records_which_peer_logged_it(corpus):
    rows = crossref.gaps_for("AAOI", crossref.index())
    row = next(r for r in rows if r["date"] == "2026-07-29")
    assert row["logged_by"] == ["COHR"]
    assert row["slug"] == "ai-optics"


def test_gap_flags_whether_ticker_was_active_that_day(corpus):
    """A date with no entry at all is stronger evidence of a miss."""
    rows = crossref.gaps_for("AAOI", crossref.index())
    row = next(r for r in rows if r["date"] == "2026-07-29")
    assert row["ticker_active_that_day"] is False


def test_gaps_never_carry_an_assessment(corpus):
    """§K.5: the peer's sign must not travel with the event."""
    rows = crossref.gaps_for("AAOI", crossref.index())
    for r in rows:
        assert set(r) == {"slug", "date", "headline", "logged_by", "ticker_active_that_day"}
        assert "verdict" not in r and "tags" not in r


def test_no_gaps_for_a_ticker_with_no_slug_peer(corpus):
    assert crossref.gaps_for("MSTR", crossref.index()) == []


def test_unknown_ticker_returns_empty(corpus):
    assert crossref.gaps_for("NOPE", crossref.index()) == []


def test_duplicates_detects_the_same_event_under_two_tickers(corpus):
    dups = crossref.duplicates(crossref.index())
    assert len(dups) == 1
    d = dups[0]
    assert d["tickers"] == ["AAOI", "COHR"]
    assert d["date"] == "2026-07-28"
    assert d["similarity"] >= crossref.DUP_THRESHOLD


def test_duplicates_ignores_unrelated_entries_on_the_same_day(tmp_path, monkeypatch):
    _mk(tmp_path, "AAA", ["s"], [_entry("2026-07-28", "s", "Alpha ships widget factory in Texas")])
    _mk(tmp_path, "BBB", ["s"], [_entry("2026-07-28", "s", "Beta refinances convertible notes due 2030")])
    monkeypatch.setattr(crossref, "ticker_dirs",
                        lambda root=None: sorted((tmp_path / "tickers").iterdir()))
    assert crossref.duplicates(crossref.index()) == []


def test_similarity_is_symmetric_and_bounded():
    a, b = "Innolight prices Hong Kong IPO at HKD 980", "Zhongji InnoLight prices Hong Kong offering HKD 980"
    s = crossref._similarity(a, b)
    assert s == crossref._similarity(b, a)
    assert 0.0 <= s <= 1.0
    assert s >= crossref.DUP_THRESHOLD


def test_similarity_ignores_stopwords_and_quarter_labels():
    assert crossref._similarity("the a of to in Q1", "the a of to in Q2") == 0.0


def test_headline_extraction_takes_the_bold_span():
    line = "- 2026-07-29 — [Sector/ai-optics] — **The headline here**. Then detail."
    assert crossref._headline(line) == "The headline here"


def test_entries_without_a_sector_tag_are_indexed_but_never_fan_out(tmp_path, monkeypatch):
    """A company-specific entry is not a sector candidate for a peer."""
    _mk(tmp_path, "AAA", ["s"], [_entry("2026-07-28", None, "AAA files an 8-K on its own refinancing")])
    _mk(tmp_path, "BBB", ["s"], [])
    monkeypatch.setattr(crossref, "ticker_dirs",
                        lambda root=None: sorted((tmp_path / "tickers").iterdir()))
    idx = crossref.index()
    assert idx["AAA"]["count"] == 1
    assert crossref.gaps_for("BBB", idx) == []
