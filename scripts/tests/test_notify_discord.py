import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import notify_discord as nd  # noqa: E402


SAMPLE = """---
date: 2026-07-15
tickers_checked: 5
tripwires_fired: 1      # count of [TRIPWIRE] hits this run
edge_shifts: 2          # count of EDGE+/EDGE- items this run
---
🚨 TRIPWIRES
• **CIFR Tripwire #2 — early-warning.** Hashprice down 18% WoW.

EDGE SHIFTS
• **AAOI — EDGE+.** 800G design win (2026-07-15).

PER-TICKER
2026-07-15 — [CATALYST] — **AAOI 800G win**. Digest → impact.
"""


def _write(tmp_path, text, name="2026-07-15.md"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_parse_summary_reads_frontmatter_and_body(tmp_path):
    meta, body = nd.parse_summary(_write(tmp_path, SAMPLE))
    assert meta["date"] == "2026-07-15"
    assert meta["tickers_checked"] == 5
    assert meta["tripwires_fired"] == 1
    assert meta["edge_shifts"] == 2
    assert body.startswith("🚨 TRIPWIRES")
    assert "---" not in body


def test_parse_missing_fields_default_zero_and_date_from_stem(tmp_path):
    text = "---\ntickers_checked: 3\n---\nnothing material\n"
    meta, body = nd.parse_summary(_write(tmp_path, text, "2026-07-16.md"))
    assert meta["date"] == "2026-07-16"       # from filename stem
    assert meta["tripwires_fired"] == 0        # missing → 0
    assert meta["edge_shifts"] == 0
    assert meta["tickers_checked"] == 3
    assert body == "nothing material"


def test_embed_color_red_on_tripwire():
    embed = nd.build_header_embed(
        {"date": "2026-07-15", "tickers_checked": 5,
         "tripwires_fired": 1, "edge_shifts": 2})
    assert embed["embeds"][0]["color"] == nd.RED


def test_embed_color_green_when_no_tripwire():
    embed = nd.build_header_embed(
        {"date": "2026-07-15", "tickers_checked": 5,
         "tripwires_fired": 0, "edge_shifts": 0})
    assert embed["embeds"][0]["color"] == nd.GREEN


def test_embed_counts_line_and_link():
    embed = nd.build_header_embed(
        {"date": "2026-07-15", "tickers_checked": 5,
         "tripwires_fired": 1, "edge_shifts": 2},
        file_url="https://example.com/s.md")
    desc = embed["embeds"][0]["description"]
    assert "1 tripwire" in desc and "2 edge" in desc and "5 checked" in desc
    assert "[Full run →](https://example.com/s.md)" in desc


def test_chunk_never_exceeds_limit():
    body = "\n".join(f"line {i} " + "x" * 50 for i in range(200))
    for c in nd.chunk(body, limit=200):
        assert len(c) <= 200


def test_chunk_reassembles_when_no_line_exceeds_limit():
    body = "\n".join(f"line {i}" for i in range(50))
    assert "\n".join(nd.chunk(body, limit=100)) == body


def test_chunk_empty_body_returns_empty_list():
    assert nd.chunk("", limit=1900) == []


def test_chunk_short_body_is_single_chunk():
    assert nd.chunk("hello\nworld", limit=1900) == ["hello\nworld"]
