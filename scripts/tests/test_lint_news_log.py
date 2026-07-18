import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import lint_news_log as lnl  # noqa: E402

GOOD = ("- 2026-07-15 — [Catalysts] [EDGE+] — **Headline here**. detail → implication. "
        "Source: [Reuters](https://reuters.com/x) (15 Jul 2026).")
GOOD_RANGE = ("- 2026-07-09 to 2026-07-17 — [Sentiment/Valuation] — **Range entry**. "
              "d → i. Source: [X](https://x.com/a) (17 Jul 2026).")
BARE_SOURCE = ("- 2026-07-16 — [Catalysts] — **No link source**. d → i. "
               "Source: GlobeNewswire, Benzinga (16 Jul 2026).")


def test_valid_entry_no_problems_no_warnings():
    assert lint_entry_ok(GOOD)


def test_date_range_and_compound_tag_valid():
    assert lint_entry_ok(GOOD_RANGE)


def lint_entry_ok(line):
    problems, warnings = lnl.lint_entry(line)
    return problems == [] and warnings == []


def test_missing_arrow_is_hard_problem():
    line = "- 2026-07-15 — [Catalysts] — **H**. no implication clause. Source: [R](https://r.co/x) (x)."
    problems, _ = lnl.lint_entry(line)
    assert any("→" in p for p in problems)


def test_missing_tag_is_hard_problem():
    line = "- 2026-07-15 — **H**. d → i. Source: [R](https://r.co/x) (x)."
    problems, _ = lnl.lint_entry(line)
    assert any("FRAMEWORK-TAG" in p for p in problems)


def test_missing_bold_headline_is_hard_problem():
    line = "- 2026-07-15 — [Catalysts] — plain headline. d → i. Source: [R](https://r.co/x) (x)."
    problems, _ = lnl.lint_entry(line)
    assert any("Headline" in p for p in problems)


def test_bare_source_is_warning_not_problem():
    problems, warnings = lnl.lint_entry(BARE_SOURCE)
    assert problems == []
    assert warnings and "bare source" in warnings[0]


def test_log_entries_only_captures_bullets_in_section():
    text = (
        "## Edge\n- not a log entry, wrong section\n"
        "## Recent News Log\n"
        "*(Entry format: ...)*\n\n"
        f"{GOOD}\n{BARE_SOURCE}\n"
        "## Next\n- 2026-01-01 — [X] — after section\n"
    )
    entries = lnl.log_entries(text)
    assert len(entries) == 2
    assert all(line.startswith("- 2026-07") for _, line in entries)


def test_main_passes_on_valid_synthetic_tree(tmp_path, capsys):
    d = tmp_path / "tickers" / "ABC"
    d.mkdir(parents=True)
    (d / "news.md").write_text(
        f'---\ncompany: "x"\nblurb: "y"\n---\n## Recent News Log\n{GOOD}\n',
        encoding="utf-8",
    )
    assert lnl.main(["--root", str(tmp_path)]) == 0


def test_main_fails_on_malformed_entry(tmp_path):
    d = tmp_path / "tickers" / "ABC"
    d.mkdir(parents=True)
    bad = "- 2026-07-15 — [Catalysts] — plain no bold, no arrow. Source: [R](https://r.co) (x)."
    (d / "news.md").write_text(
        f'---\ncompany: "x"\nblurb: "y"\n---\n## Recent News Log\n{bad}\n', encoding="utf-8"
    )
    assert lnl.main(["--root", str(tmp_path)]) == 1
