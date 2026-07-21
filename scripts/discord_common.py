"""Shared Discord bot-transport helpers — stdlib only.

Posts via a Discord bot (single DISCORD_BOT_TOKEN) to a channel by ID, replacing
the old per-channel webhook URLs. Used by notify_discord_ticker.py,
notify_discord_dispatch.py and onboard_discord_channel.py. Channel/guild IDs are
resolved from the committed map by channelmap.py; this module only speaks HTTP.
"""
import json
import os
import time
import urllib.error
import urllib.request

API = "https://discord.com/api/v10"
TOKEN_ENV = "DISCORD_BOT_TOKEN"
USER_AGENT = "equity-watch-notifier/1.0 (+https://github.com/roachx92/equity-watch)"


def chunk(body, limit=1900):
    chunks, cur = [], ""
    for line in body.split("\n"):
        while len(line) > limit:            # a single over-long line: hard split
            if cur:
                chunks.append(cur)
                cur = ""
            chunks.append(line[:limit])
            line = line[limit:]
        candidate = line if not cur else cur + "\n" + line
        if len(candidate) <= limit:
            cur = candidate
        else:
            chunks.append(cur)
            cur = line
    if cur:
        chunks.append(cur)
    return chunks


def _token(token):
    tok = token or os.environ.get(TOKEN_ENV, "")
    if not tok:
        raise RuntimeError(f"{TOKEN_ENV} not set")
    return tok


def _request(url, token, payload=None, method=None):
    """One Discord REST call with bot auth and a 429 Retry-After loop.
    payload=None -> GET (no body); otherwise POST JSON. Returns parsed JSON
    ({} / [] if the body is empty)."""
    method = method or ("GET" if payload is None else "POST")
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bot {_token(token)}", "User-Agent": USER_AGENT}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    for _ in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode("utf-8")
                return json.loads(text) if text.strip() else {}
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                time.sleep(float(exc.headers.get("Retry-After", "1")))
                continue
            raise
    raise RuntimeError("Discord request failed after retries (HTTP 429)")


def post(channel_id, payload, token=None):
    """POST a message payload to channel_id. Returns the created-message dict."""
    return _request(f"{API}/channels/{channel_id}/messages", token, payload)


def create_channel(guild_id, name, token=None):
    """Create a text channel (type 0) named `name` in `guild_id`; return its id."""
    obj = _request(f"{API}/guilds/{guild_id}/channels", token, {"name": name, "type": 0})
    return str(obj["id"])


def list_channels(guild_id, token=None):
    """Return the guild's channels as a list of dicts."""
    return _request(f"{API}/guilds/{guild_id}/channels", token)
