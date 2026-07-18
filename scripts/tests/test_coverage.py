import importlib.util
import pathlib

# Load the mkdocs hook web/hooks/coverage.py by explicit path, under a unique
# module name so it can't collide with the PyPI `coverage` tool. The hook itself
# puts scripts/ on sys.path on import (to reach tickerlib).
_HOOK = pathlib.Path(__file__).resolve().parents[2] / "web" / "hooks" / "coverage.py"
_spec = importlib.util.spec_from_file_location("coverage_hook", _HOOK)
coverage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(coverage)


def _make_docs(root, sym, company, blurb, reports=()):
    """Build a minimal assembled-docs tree: docs/tickers/<sym>/news.md (+reports)."""
    d = root / "tickers" / sym
    d.mkdir(parents=True)
    (d / "news.md").write_text(
        f'---\ncompany: "{company}"\nblurb: "{blurb}"\n---\n# {sym}\n',
        encoding="utf-8",
    )
    if reports:
        (d / "reports").mkdir()
        for date in reports:
            (d / "reports" / f"{date}.md").write_text("x", encoding="utf-8")
    return root


def _run(docs_dir):
    config = {"docs_dir": str(docs_dir), "extra": {}}
    coverage.on_config(config)
    return config["extra"]["coverage_cards"]


def test_card_carries_front_matter_and_latest_report(tmp_path):
    _make_docs(tmp_path, "AAOI", "Applied Optoelectronics · NASDAQ", "an optics story",
               reports=("2026-07-14", "2026-07-17"))
    cards = _run(tmp_path)
    assert cards == [{
        "sym": "AAOI",
        "company": "Applied Optoelectronics · NASDAQ",
        "blurb": "an optics story",
        "monitor": "tickers/AAOI/news/",
        "report": "tickers/AAOI/reports/2026-07-17/",   # newest of the two
    }]


def test_card_report_is_none_when_no_reports(tmp_path):
    _make_docs(tmp_path, "WYFI", "Wyfi Corp", "no reports yet")
    cards = _run(tmp_path)
    assert cards[0]["report"] is None
    assert cards[0]["company"] == "Wyfi Corp"


def test_multiple_tickers_sorted_by_symbol(tmp_path):
    _make_docs(tmp_path, "ZZZ", "Zzz Inc", "z")
    _make_docs(tmp_path, "AAA", "Aaa Inc", "a")
    cards = _run(tmp_path)
    assert [c["sym"] for c in cards] == ["AAA", "ZZZ"]


def test_folder_without_news_md_is_skipped(tmp_path):
    _make_docs(tmp_path, "AAA", "Aaa Inc", "a")
    (tmp_path / "tickers" / "EMPTY").mkdir()  # no news.md
    cards = _run(tmp_path)
    assert [c["sym"] for c in cards] == ["AAA"]
