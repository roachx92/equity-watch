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
