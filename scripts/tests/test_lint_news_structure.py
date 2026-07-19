import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import lint_news_structure as lns  # noqa: E402

WELL_FORMED = """---
company: "ABC Co"
blurb: "does things"
---
# ABC

**Canonical deep-dive:** [`reports/2026-07-14.md`](reports/2026-07-14.md)

## Thesis context (one-paragraph)
para

## Edge
edge

## Sector lens
- **`ai-optics` — sole.** Channel: **demand**.

## Tripwires
1. t

## Recent News Log
- entry
"""


def _mk(root, sym, text=WELL_FORMED, with_news=True):
    d = root / "tickers" / sym
    d.mkdir(parents=True)
    if with_news:
        (d / "news.md").write_text(text, encoding="utf-8")
    return d


def test_well_formed_passes(tmp_path):
    _mk(tmp_path, "ABC")
    assert lns.main(["--root", str(tmp_path)]) == 0


def test_missing_news_md_flagged(tmp_path, capsys):
    _mk(tmp_path, "ABC")
    _mk(tmp_path, "ZZZ", with_news=False)  # half-created
    rc = lns.main(["--root", str(tmp_path)])
    assert rc == 1
    assert "ZZZ" in capsys.readouterr().out


def test_missing_section_flagged(tmp_path):
    text = WELL_FORMED.replace("## Tripwires\n1. t\n\n", "")
    d = _mk(tmp_path, "ABC", text=text)
    problems = lns.lint_news(d / "news.md")
    assert any("Tripwires" in p for p in problems)


def test_missing_front_matter_key_flagged(tmp_path):
    text = WELL_FORMED.replace('blurb: "does things"\n', "")
    d = _mk(tmp_path, "ABC", text=text)
    problems = lns.lint_news(d / "news.md")
    assert any("blurb" in p for p in problems)


def test_thesis_heading_with_suffix_accepted(tmp_path):
    # "## Thesis context (one-paragraph)" must satisfy "## Thesis context".
    d = _mk(tmp_path, "ABC")
    assert lns.lint_news(d / "news.md") == []


def test_missing_sector_lens_section_flagged(tmp_path, capsys):
    text = WELL_FORMED.replace(
        "## Sector lens\n- **`ai-optics` — sole.** Channel: **demand**.\n\n", "")
    _mk(tmp_path, "ABC", text=text)
    assert lns.main(["--root", str(tmp_path)]) == 1
    assert "Sector lens" in capsys.readouterr().out


def test_sector_lens_present_but_empty_flagged(tmp_path, capsys):
    """A heading with no membership bullet is the silent case: the section
    exists so a structure check passes, but the sector agent has nothing to
    search and the miss produces no entries."""
    text = WELL_FORMED.replace("- **`ai-optics` — sole.** Channel: **demand**.",
                               "*TBD — not yet assigned.*")
    _mk(tmp_path, "ABC", text=text)
    assert lns.main(["--root", str(tmp_path)]) == 1
    assert "no sector membership" in capsys.readouterr().out


def test_unknown_sector_slug_rejected(tmp_path, capsys):
    """Closed vocabulary: a typo'd slug would route the sector agent to no
    registry entry at all, so it fails rather than warning."""
    text = WELL_FORMED.replace("`ai-optics`", "`ai-optics-typo`")
    _mk(tmp_path, "ABC", text=text)
    assert lns.main(["--root", str(tmp_path)]) == 1
    assert "unknown sector" in capsys.readouterr().out
