import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import notify_discord_dispatch as ndd  # noqa: E402


def _write_summary(tmp_path, text):
    p = tmp_path / "summary.md"
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_build_header_green_on_success():
    embed = ndd.build_header(date="2026-07-18", status="success")
    assert embed["embeds"][0]["color"] == 0x2ECC71
    assert embed["embeds"][0]["title"] == "Dispatcher — 2026-07-18"


def test_build_header_red_on_failure():
    embed = ndd.build_header(date="2026-07-18", status="failure")
    assert embed["embeds"][0]["color"] == 0xD9342B


def test_build_header_red_on_unknown_status():
    embed = ndd.build_header(date="2026-07-18", status="cancelled")
    assert embed["embeds"][0]["color"] == 0xD9342B


def test_build_header_omits_date_when_none():
    embed = ndd.build_header(date=None, status="success")
    assert embed["embeds"][0]["title"] == "Dispatcher"


def test_read_summary_missing_returns_empty(tmp_path):
    assert ndd.read_summary(str(tmp_path / "nope.md")) == ""


def test_read_summary_reads_and_strips(tmp_path):
    path = _write_summary(tmp_path, "\n| Ticker | Earnings |\n| --- | --- |\n")
    assert ndd.read_summary(path) == "| Ticker | Earnings |\n| --- | --- |"


def test_main_skips_gracefully_when_webhook_unset(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("DISCORD_DISPATCHER_WEBHOOK", raising=False)
    summary = _write_summary(tmp_path, "| Ticker | Earnings | What's-new | Reason |")

    rc = ndd.main(["--summary-file", summary, "--date", "2026-07-18", "--status", "success"])

    assert rc == 0
    assert "no DISCORD_DISPATCHER_WEBHOOK" in capsys.readouterr().err


def test_main_dry_run_prints_header_and_table(tmp_path, capsys):
    summary = _write_summary(tmp_path, "| Ticker | Earnings |\n| --- | --- |\n| COHR | dispatched |")

    rc = ndd.main([
        "--summary-file", summary, "--date", "2026-07-18",
        "--status", "success", "--dry-run",
    ])

    assert rc == 0
    lines = [l for l in capsys.readouterr().out.strip().splitlines() if l]
    payloads = [json.loads(l) for l in lines]
    assert payloads[0]["embeds"][0]["title"] == "Dispatcher — 2026-07-18"
    assert payloads[0]["embeds"][0]["color"] == 0x2ECC71
    assert "| COHR | dispatched |" in payloads[1]["content"]


def test_main_fallback_body_when_summary_missing(tmp_path, capsys):
    rc = ndd.main([
        "--summary-file", str(tmp_path / "absent.md"), "--date", "2026-07-18",
        "--status", "failure", "--dry-run",
    ])

    assert rc == 0
    lines = [l for l in capsys.readouterr().out.strip().splitlines() if l]
    payloads = [json.loads(l) for l in lines]
    assert payloads[0]["embeds"][0]["color"] == 0xD9342B
    assert "did not produce a summary" in payloads[1]["content"]
    assert "failure" in payloads[1]["content"]
