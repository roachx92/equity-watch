#!/usr/bin/env python3
"""Load and update the committed Discord channel map (discord-channels.json).

NON-SECRET: Discord channel/guild IDs are visible to anyone in the server, so
this file is committed — the single source of truth for ticker→channel routing,
replacing the old gitignored per-channel webhook map. Keys are ticker symbols
(normalized upper-case); values are channel-ID snowflake strings. Reserved
`_`-prefixed keys carry config: `_comment`, `_guild_id` (needed to auto-create
channels), `_dispatcher` (the dispatcher heartbeat channel). This is the ONLY
parser for the map — do not grow a second one.

Python 3 stdlib only.
"""
import json
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parents[1] / "discord-channels.json"


def load(path=DEFAULT_PATH):
    """Return the raw map dict (including `_`-keys). Missing file -> {}."""
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"discord-channels.json is not valid JSON ({path}): {exc}") from exc


def resolve(ticker, path=DEFAULT_PATH):
    """Return the channel_id string for `ticker` (case-insensitive), or None."""
    want = ticker.strip().upper()
    for k, v in load(path).items():
        if k.startswith("_"):
            continue
        if k.strip().upper() == want and v:
            return str(v)
    return None


def guild_id(path=DEFAULT_PATH):
    v = load(path).get("_guild_id")
    return str(v) if v else None


def dispatcher(path=DEFAULT_PATH):
    v = load(path).get("_dispatcher")
    return str(v) if v else None


def write_channel(ticker, channel_id, path=DEFAULT_PATH):
    """Upsert `ticker`->channel_id and write the file back, preserving `_`-keys
    (config first) and sorting ticker keys for a stable diff. Returns new dict."""
    raw = load(path)
    reserved = {k: v for k, v in raw.items() if k.startswith("_")}
    tickers = {k.strip().upper(): v for k, v in raw.items() if not k.startswith("_")}
    tickers[ticker.strip().upper()] = str(channel_id)
    ordered = {}
    for k in ("_comment", "_guild_id", "_dispatcher"):
        if k in reserved:
            ordered[k] = reserved[k]
    for k, v in reserved.items():
        ordered.setdefault(k, v)
    for k in sorted(tickers):
        ordered[k] = tickers[k]
    Path(path).write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ordered
