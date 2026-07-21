import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import notify_discord_dispatch as ndd  # noqa: E402


def _cfg(tmp_path, mapping):
    p = tmp_path / "discord-channels.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return str(p)


def test_build_header_green_on_success():
    embed = ndd.build_header("2026-07-20", "success", "Dispatcher")
    assert embed["embeds"][0]["color"] == 0x2ECC71
    assert embed["embeds"][0]["title"] == "Dispatcher — 2026-07-20"


def test_build_header_red_on_failure_and_label():
    embed = ndd.build_header(None, "failure", "Staleness audit")
    assert embed["embeds"][0]["color"] == 0xD9342B
    assert embed["embeds"][0]["title"] == "Staleness audit"


def test_missing_summary_uses_fallback_body(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"_dispatcher": "88"})
    rc = ndd.main(["--summary-file", str(tmp_path / "nope.md"), "--status", "failure",
                   "--config", cfg, "--dry-run"])
    assert rc == 0
    payloads = [json.loads(l) for l in capsys.readouterr().out.strip().splitlines() if l]
    assert "did not produce a summary" in payloads[1]["content"]


def test_skips_when_no_dispatcher_channel(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"AAOI": "111"})
    sf = tmp_path / "s.md"; sf.write_text("table", encoding="utf-8")
    rc = ndd.main(["--summary-file", str(sf), "--status", "success", "--config", cfg])
    assert rc == 0
    assert "no _dispatcher channel configured" in capsys.readouterr().err


def test_posts_to_dispatcher_channel(tmp_path, monkeypatch):
    cfg = _cfg(tmp_path, {"_dispatcher": "88"})
    sf = tmp_path / "s.md"; sf.write_text("the table", encoding="utf-8")
    sent = []
    monkeypatch.setattr(ndd, "post", lambda channel_id, msg: sent.append((channel_id, msg)))
    monkeypatch.setattr(ndd.time, "sleep", lambda *_a, **_k: None)
    rc = ndd.main(["--summary-file", str(sf), "--status", "success", "--config", cfg])
    assert rc == 0
    assert sent[0][0] == "88"
    assert sent[-1][1]["content"] == "the table"
