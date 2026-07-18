import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import summarize_counts as sc  # noqa: E402

# Unified diff adding two log entries: one TRIPWIRE, one EDGE− (U+2212 minus).
DIFF = """diff --git a/tickers/ABC/news.md b/tickers/ABC/news.md
--- a/tickers/ABC/news.md
+++ b/tickers/ABC/news.md
@@ -25,0 +26,2 @@
+- 2026-07-18 — [Risks] [TRIPWIRE #1 — fired] — **bad**. d → i. Source: [R](https://r.co) (x).
+- 2026-07-18 — [Sentiment] [EDGE−] — **shift**. d → i. Source: [R](https://r.co) (x).
"""


def test_added_lines_strips_headers():
    added = sc.added_lines(DIFF)
    assert "TRIPWIRE" in added
    assert "+++ b/tickers" not in added
    assert "diff --git" not in added


def test_derive_counts_counts_tags():
    counts = sc.derive_counts(DIFF, news_file_count=5)
    assert counts == {"tickers_checked": 5, "tripwires_fired": 1, "edge_shifts": 1}


def test_derive_counts_edge_ascii_and_unicode_minus():
    diff = "+ [EDGE+] a\n+ [EDGE−] b\n+ [EDGE-] c\n"
    assert sc.derive_counts(diff, 1)["edge_shifts"] == 3


def test_derive_counts_zero_when_no_additions():
    assert sc.derive_counts("", 3) == {"tickers_checked": 3, "tripwires_fired": 0, "edge_shifts": 0}


def test_render_and_split_roundtrip(tmp_path):
    front = sc.render_frontmatter("2026-07-18", {"tickers_checked": 5, "tripwires_fired": 1, "edge_shifts": 2})
    assert front.startswith("---\ndate: 2026-07-18\n")
    assert "tripwires_fired: 1" in front
    p = tmp_path / "s.md"
    p.write_text(front + "digest body\n", encoding="utf-8")
    meta, body = sc.split_summary(p)
    assert meta["date"] == "2026-07-18"
    assert meta["edge_shifts"] == "2"
    assert body == "digest body\n"


def _write_summary(tmp_path, date, counts, body="🚨 digest\n"):
    p = tmp_path / "summaries" / f"{date}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(sc.render_frontmatter(date, counts) + body, encoding="utf-8")
    return p


def _patch(monkeypatch, tmp_path, diff, n):
    monkeypatch.setattr(sc, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(sc, "git_news_diff", lambda root, base: diff)
    monkeypatch.setattr(sc, "news_files", lambda root=None: list(range(n)))


def test_main_writes_frontmatter_preserving_body(tmp_path, monkeypatch):
    _write_summary(tmp_path, "2026-07-18", {"tickers_checked": 0, "tripwires_fired": 0, "edge_shifts": 0})
    _patch(monkeypatch, tmp_path, DIFF, 5)
    assert sc.main(["--date", "2026-07-18"]) == 0
    text = (tmp_path / "summaries" / "2026-07-18.md").read_text(encoding="utf-8")
    assert "tripwires_fired: 1" in text
    assert "edge_shifts: 1" in text
    assert "🚨 digest" in text  # body preserved


def test_main_check_passes_when_counts_match(tmp_path, monkeypatch):
    _write_summary(tmp_path, "2026-07-18", {"tickers_checked": 5, "tripwires_fired": 1, "edge_shifts": 1})
    _patch(monkeypatch, tmp_path, DIFF, 5)
    assert sc.main(["--date", "2026-07-18", "--check"]) == 0


def test_main_check_fails_on_mismatch(tmp_path, monkeypatch):
    _write_summary(tmp_path, "2026-07-18", {"tickers_checked": 5, "tripwires_fired": 0, "edge_shifts": 0})
    _patch(monkeypatch, tmp_path, DIFF, 5)
    assert sc.main(["--date", "2026-07-18", "--check"]) == 1


def test_main_missing_file_returns_1(tmp_path, monkeypatch):
    _patch(monkeypatch, tmp_path, DIFF, 5)
    assert sc.main(["--date", "2026-07-18"]) == 1
