import io
import json
import sys
import pathlib
import urllib.error

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import discord_common as dc  # noqa: E402


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def _capture(monkeypatch, body=b"{}"):
    calls = {}

    def fake_urlopen(req, *a, **k):
        calls["url"] = req.full_url
        calls["method"] = req.get_method()
        calls["headers"] = dict(req.header_items())
        calls["data"] = req.data
        return _Resp(body)

    monkeypatch.setattr(dc.urllib.request, "urlopen", fake_urlopen)
    return calls


def test_post_hits_channel_endpoint_with_bot_auth(monkeypatch):
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "tok123")
    calls = _capture(monkeypatch, body=b'{"id": "555"}')
    out = dc.post("42", {"content": "hi"})
    assert out == {"id": "555"}
    assert calls["url"] == "https://discord.com/api/v10/channels/42/messages"
    assert calls["method"] == "POST"
    # header keys are capitalized by urllib
    assert calls["headers"]["Authorization"] == "Bot tok123"
    assert json.loads(calls["data"]) == {"content": "hi"}


def test_create_channel_returns_new_id(monkeypatch):
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "tok123")
    calls = _capture(monkeypatch, body=b'{"id": "999", "name": "aaoi"}')
    new_id = dc.create_channel("77", "aaoi")
    assert new_id == "999"
    assert calls["url"] == "https://discord.com/api/v10/guilds/77/channels"
    assert json.loads(calls["data"]) == {"name": "aaoi", "type": 0}


def test_list_channels_is_a_get(monkeypatch):
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "tok123")
    calls = _capture(monkeypatch, body=b'[{"id":"1","name":"aaoi","type":0}]')
    chans = dc.list_channels("77")
    assert chans[0]["name"] == "aaoi"
    assert calls["method"] == "GET"
    assert calls["data"] is None


def test_missing_token_raises(monkeypatch):
    monkeypatch.delenv("DISCORD_BOT_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        dc.post("42", {"content": "hi"})


def test_chunk_splits_long_body():
    body = "\n".join(["x" * 100] * 40)  # 4000+ chars
    parts = dc.chunk(body, limit=1900)
    assert len(parts) >= 2
    assert all(len(p) <= 1900 for p in parts)
