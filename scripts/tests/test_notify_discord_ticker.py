import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import notify_discord_ticker as ndt  # noqa: E402


def _cfg(tmp_path, mapping):
    p = tmp_path / "discord-channels.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return str(p)


def test_build_header_color_red_on_tripwire():
    embed = ndt.build_header("LPKF", tripwire_fired=True, kind="whats-new", date="2026-07-17")
    assert embed["embeds"][0]["color"] == 0xD9342B
    assert embed["embeds"][0]["title"] == "LPKF — What's New (2026-07-17)"


def test_build_header_color_green_when_clean():
    embed = ndt.build_header("LPKF", tripwire_fired=False, kind="whats-new", date="2026-07-17")
    assert embed["embeds"][0]["color"] == 0x2ECC71


def test_build_header_earnings_digest_title():
    embed = ndt.build_header("CIFR", tripwire_fired=False, kind="earnings-digest", date="2026-07-17")
    assert embed["embeds"][0]["title"] == "CIFR — Earnings Digest (2026-07-17)"


def test_build_header_omits_date_when_none():
    embed = ndt.build_header("CIFR", tripwire_fired=False, kind="earnings-digest", date=None)
    assert embed["embeds"][0]["title"] == "CIFR — Earnings Digest"


def test_unmapped_ticker_skips_gracefully_by_default(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"CIFR": "222"})
    tf = tmp_path / "d.txt"; tf.write_text("body", encoding="utf-8")
    rc = ndt.main(["--ticker", "LPKF", "--kind", "whats-new", "--text-file", str(tf), "--config", cfg])
    assert rc == 0
    assert "no Discord channel mapped for LPKF" in capsys.readouterr().err


def test_unmapped_ticker_fails_hard_with_require_channel(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"CIFR": "222"})
    tf = tmp_path / "d.txt"; tf.write_text("body", encoding="utf-8")
    rc = ndt.main(["--ticker", "LPKF", "--kind", "whats-new", "--text-file", str(tf),
                   "--config", cfg, "--require-channel"])
    assert rc == 1
    assert "failing (--require-channel)" in capsys.readouterr().err


def test_empty_digest_is_a_noop(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"LPKF": "111"})
    tf = tmp_path / "d.txt"; tf.write_text("  \n ", encoding="utf-8")
    rc = ndt.main(["--ticker", "LPKF", "--kind", "whats-new", "--text-file", str(tf), "--config", cfg])
    assert rc == 0
    assert "empty digest" in capsys.readouterr().err


def test_dry_run_prints_payloads_without_posting(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"LPKF": "111"})
    tf = tmp_path / "d.txt"; tf.write_text("line one\nline two", encoding="utf-8")
    rc = ndt.main(["--ticker", "lpkf", "--kind", "whats-new", "--date", "2026-07-17",
                   "--text-file", str(tf), "--config", cfg, "--dry-run"])
    assert rc == 0
    payloads = [json.loads(l) for l in capsys.readouterr().out.strip().splitlines() if l]
    assert payloads[0]["embeds"][0]["title"] == "LPKF — What's New (2026-07-17)"
    assert payloads[1]["content"] == "line one\nline two"


def test_posts_to_resolved_channel(tmp_path, monkeypatch):
    cfg = _cfg(tmp_path, {"LPKF": "111"})
    tf = tmp_path / "d.txt"; tf.write_text("hello", encoding="utf-8")
    sent = []
    monkeypatch.setattr(ndt, "post", lambda channel_id, msg: sent.append((channel_id, msg)))
    monkeypatch.setattr(ndt.time, "sleep", lambda *_a, **_k: None)
    rc = ndt.main(["--ticker", "LPKF", "--kind", "whats-new", "--text-file", str(tf), "--config", cfg])
    assert rc == 0
    assert sent[0][0] == "111"                       # header to channel 111
    assert sent[-1][1]["content"] == "hello"


def test_rejects_invalid_kind(tmp_path):
    cfg = _cfg(tmp_path, {"LPKF": "111"})
    tf = tmp_path / "d.txt"; tf.write_text("body", encoding="utf-8")
    try:
        ndt.main(["--ticker", "LPKF", "--kind", "nope", "--text-file", str(tf), "--config", cfg])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code != 0
