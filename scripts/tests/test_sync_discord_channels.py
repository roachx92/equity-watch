import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import sync_discord_channels as sync  # noqa: E402
import onboard_discord_channel as onb  # noqa: E402


def _repo(tmp_path, tickers):
    """Build a fake repo root with tickers/<T>/news.md folders (plus one noise
    folder with no news.md that must be ignored)."""
    for t in tickers:
        d = tmp_path / "tickers" / t
        d.mkdir(parents=True)
        (d / "news.md").write_text("# " + t, encoding="utf-8")
    noise = tmp_path / "tickers" / "NOTATICKER"
    noise.mkdir(parents=True)
    return str(tmp_path)


def _cfg(tmp_path, mapping):
    p = tmp_path / "discord-channels.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return str(p)


def test_watched_tickers_globs_folders_uppercased_sorted(tmp_path):
    root = _repo(tmp_path, ["cifr", "AAOI"])
    assert sync.watched_tickers(root) == ["AAOI", "CIFR"]  # NOTATICKER (no news.md) excluded


def test_sync_creates_only_missing(tmp_path, monkeypatch, capsys):
    root = _repo(tmp_path, ["AAOI", "WYFI"])
    cfg = _cfg(tmp_path, {"_guild_id": "77", "AAOI": "111"})
    monkeypatch.setattr(onb, "list_channels", lambda gid, token=None: [])
    monkeypatch.setattr(onb, "create_channel", lambda gid, name, token=None: "999")

    rc = sync.main(["--config", cfg, "--repo-root", root])
    assert rc == 0
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert raw["AAOI"] == "111"          # untouched
    assert raw["WYFI"] == "999"          # created
    out = capsys.readouterr().out
    assert "WYFI" in out and "created" in out
    assert "AAOI" not in out             # already-mapped tickers are not reported


def test_sync_all_mapped_is_noop(tmp_path, monkeypatch, capsys):
    root = _repo(tmp_path, ["AAOI"])
    cfg = _cfg(tmp_path, {"_guild_id": "77", "AAOI": "111"})
    monkeypatch.setattr(onb, "list_channels",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not list")))
    monkeypatch.setattr(onb, "create_channel",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not create")))

    rc = sync.main(["--config", cfg, "--repo-root", root])
    assert rc == 0
    assert "already have channels" in capsys.readouterr().out


def test_sync_dry_run_writes_nothing(tmp_path, monkeypatch, capsys):
    root = _repo(tmp_path, ["WYFI"])
    cfg = _cfg(tmp_path, {"_guild_id": "77"})
    monkeypatch.setattr(onb, "list_channels",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not list")))
    monkeypatch.setattr(onb, "create_channel",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not create")))

    rc = sync.main(["--config", cfg, "--repo-root", root, "--dry-run"])
    assert rc == 0
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert "WYFI" not in raw
    assert "would-create" in capsys.readouterr().out


def test_sync_missing_guild_fails_loud(tmp_path, capsys):
    root = _repo(tmp_path, ["WYFI"])
    cfg = _cfg(tmp_path, {"AAOI": "111"})  # no _guild_id, WYFI unmapped
    rc = sync.main(["--config", cfg, "--repo-root", root])
    assert rc == 1
    assert "no _guild_id" in capsys.readouterr().err
