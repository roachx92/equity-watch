import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import notify_discord_ticker as ndt  # noqa: E402


def _write_config(tmp_path, mapping):
    p = tmp_path / "discord-webhooks.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return str(p)


def test_load_webhooks_normalizes_keys_to_upper(tmp_path):
    cfg = _write_config(tmp_path, {"lpkf": "https://example.com/hook1", "CIFR": "https://example.com/hook2"})
    webhooks = ndt.load_webhooks(cfg)
    assert webhooks["LPKF"] == "https://example.com/hook1"
    assert webhooks["CIFR"] == "https://example.com/hook2"


def test_load_webhooks_missing_file_returns_empty(tmp_path):
    assert ndt.load_webhooks(str(tmp_path / "does-not-exist.json")) == {}


def test_load_webhooks_drops_empty_values(tmp_path):
    cfg = _write_config(tmp_path, {"AAOI": "", "WYFI": "https://example.com/hook3"})
    webhooks = ndt.load_webhooks(cfg)
    assert "AAOI" not in webhooks
    assert webhooks["WYFI"] == "https://example.com/hook3"


def test_build_header_color_red_on_tripwire():
    embed = ndt.build_header("LPKF", tripwire_fired=True)
    assert embed["embeds"][0]["color"] == 0xD9342B
    assert embed["embeds"][0]["title"] == "LPKF — What's New"


def test_build_header_color_green_when_clean():
    embed = ndt.build_header("LPKF", tripwire_fired=False)
    assert embed["embeds"][0]["color"] == 0x2ECC71


def test_main_skips_gracefully_when_ticker_not_configured(tmp_path, capsys):
    cfg = _write_config(tmp_path, {"CIFR": "https://example.com/hook"})
    text_file = tmp_path / "digest.txt"
    text_file.write_text("some digest body", encoding="utf-8")

    rc = ndt.main(["--ticker", "LPKF", "--text-file", str(text_file), "--config", cfg])

    assert rc == 0
    captured = capsys.readouterr()
    assert "no Discord webhook configured for LPKF" in captured.err


def test_main_empty_digest_is_a_noop(tmp_path, capsys):
    cfg = _write_config(tmp_path, {"LPKF": "https://example.com/hook"})
    text_file = tmp_path / "digest.txt"
    text_file.write_text("   \n  ", encoding="utf-8")

    rc = ndt.main(["--ticker", "LPKF", "--text-file", str(text_file), "--config", cfg])

    assert rc == 0
    captured = capsys.readouterr()
    assert "empty digest" in captured.err


def test_main_dry_run_prints_payloads_without_posting(tmp_path, capsys):
    cfg = _write_config(tmp_path, {"LPKF": "https://example.com/hook"})
    text_file = tmp_path / "digest.txt"
    text_file.write_text("line one\nline two", encoding="utf-8")

    rc = ndt.main(["--ticker", "lpkf", "--text-file", str(text_file), "--config", cfg, "--dry-run"])

    assert rc == 0
    lines = [l for l in capsys.readouterr().out.strip().splitlines() if l]
    payloads = [json.loads(l) for l in lines]
    assert payloads[0]["embeds"][0]["title"] == "LPKF — What's New"
    assert payloads[1]["content"] == "line one\nline two"
