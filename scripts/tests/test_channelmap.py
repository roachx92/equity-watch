import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import channelmap  # noqa: E402


def _write(tmp_path, mapping):
    p = tmp_path / "discord-channels.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return str(p)


def test_resolve_is_case_insensitive(tmp_path):
    cfg = _write(tmp_path, {"_guild_id": "1", "AAOI": "111", "cifr": "222"})
    assert channelmap.resolve("aaoi", cfg) == "111"
    assert channelmap.resolve("CIFR", cfg) == "222"


def test_resolve_missing_ticker_returns_none(tmp_path):
    cfg = _write(tmp_path, {"AAOI": "111"})
    assert channelmap.resolve("WYFI", cfg) is None


def test_resolve_skips_reserved_and_empty(tmp_path):
    cfg = _write(tmp_path, {"_dispatcher": "999", "AAOI": ""})
    assert channelmap.resolve("_dispatcher", cfg) is None
    assert channelmap.resolve("AAOI", cfg) is None


def test_guild_and_dispatcher(tmp_path):
    cfg = _write(tmp_path, {"_guild_id": "77", "_dispatcher": "88"})
    assert channelmap.guild_id(cfg) == "77"
    assert channelmap.dispatcher(cfg) == "88"


def test_load_missing_file_returns_empty(tmp_path):
    assert channelmap.load(str(tmp_path / "nope.json")) == {}


def test_write_channel_upserts_and_preserves_reserved(tmp_path):
    cfg = _write(tmp_path, {"_comment": "c", "_guild_id": "77", "CIFR": "222"})
    channelmap.write_channel("aaoi", "111", cfg)
    raw = json.loads(pathlib.Path(cfg).read_text(encoding="utf-8"))
    assert raw["_guild_id"] == "77"
    assert raw["AAOI"] == "111"
    assert raw["CIFR"] == "222"
    # ticker keys sorted; reserved keys stay ahead of tickers
    keys = list(raw)
    assert keys.index("_guild_id") < keys.index("AAOI")
    assert keys.index("AAOI") < keys.index("CIFR")
