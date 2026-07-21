import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import onboard_discord_channel as onb  # noqa: E402


def _cfg(tmp_path, mapping):
    p = tmp_path / "discord-channels.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return str(p)


def test_already_mapped_is_noop(tmp_path, monkeypatch, capsys):
    cfg = _cfg(tmp_path, {"_guild_id": "77", "AAOI": "111"})
    monkeypatch.setattr(onb, "create_channel", lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not create")))
    monkeypatch.setattr(onb, "list_channels", lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not list")))
    rc = onb.main(["--ticker", "aaoi", "--config", cfg])
    assert rc == 0
    assert "already mapped" in capsys.readouterr().out


def test_missing_guild_errors(tmp_path, capsys):
    cfg = _cfg(tmp_path, {"AAOI": "111"})
    rc = onb.main(["--ticker", "WYFI", "--config", cfg])
    assert rc == 1
    assert "no _guild_id" in capsys.readouterr().err


def test_creates_and_writes_back(tmp_path, monkeypatch, capsys):
    cfg = _cfg(tmp_path, {"_guild_id": "77"})
    monkeypatch.setattr(onb, "list_channels", lambda gid, token=None: [])
    monkeypatch.setattr(onb, "create_channel", lambda gid, name, token=None: "999")
    rc = onb.main(["--ticker", "wyfi", "--name", "WYFI Warden", "--config", cfg])
    assert rc == 0
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert raw["WYFI"] == "999"
    assert "created" in capsys.readouterr().out


def test_adopts_existing_channel_by_name(tmp_path, monkeypatch, capsys):
    cfg = _cfg(tmp_path, {"_guild_id": "77"})
    monkeypatch.setattr(onb, "list_channels",
                        lambda gid, token=None: [{"id": "555", "name": "wyfi", "type": 0}])
    monkeypatch.setattr(onb, "create_channel",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("should adopt, not create")))
    rc = onb.main(["--ticker", "WYFI", "--config", cfg])   # default name == "wyfi"
    assert rc == 0
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert raw["WYFI"] == "555"
    assert "adopted" in capsys.readouterr().out


def test_dry_run_does_not_write(tmp_path, monkeypatch, capsys):
    cfg = _cfg(tmp_path, {"_guild_id": "77"})
    monkeypatch.setattr(onb, "list_channels", lambda *a, **k: (_ for _ in ()).throw(AssertionError()))
    monkeypatch.setattr(onb, "create_channel", lambda *a, **k: (_ for _ in ()).throw(AssertionError()))
    rc = onb.main(["--ticker", "WYFI", "--config", cfg, "--dry-run"])
    assert rc == 0
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert "WYFI" not in raw
    assert "would ensure" in capsys.readouterr().out


def test_adopts_themed_name_channel_via_slug(tmp_path, monkeypatch, capsys):
    cfg = _cfg(tmp_path, {"_guild_id": "77"})
    monkeypatch.setattr(onb, "list_channels",
                        lambda gid, token=None: [{"id": "555", "name": "wyfi-warden", "type": 0}])
    monkeypatch.setattr(onb, "create_channel",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("should adopt, not create")))
    rc = onb.main(["--ticker", "WYFI", "--name", "WYFI Warden", "--config", str(cfg)])
    assert rc == 0
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert raw["WYFI"] == "555"
    assert "adopted" in capsys.readouterr().out
