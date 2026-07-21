# Discord Bot Transport Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace per-channel Discord webhooks with a single bot token + a committed, non-secret ticker→channel_id map, eliminating the local/CI map drift that silently dropped posts.

**Architecture:** All Discord posting moves to the bot REST API (`POST /channels/{id}/messages` with `Authorization: Bot <token>`). The ticker→channel_id routing becomes a committed `discord-channels.json` (channel/guild IDs aren't secret). A new `channelmap.py` owns map I/O; `discord_common.py` owns the bot HTTP. Two posters and a new onboarding helper consume them. The per-ticker post moves out of the hidden Claude agent prompt into a deterministic, visible workflow step.

**Tech Stack:** Python 3 stdlib only (`urllib`, `json`, `argparse`), pytest, GitHub Actions YAML.

## Global Constraints

- **Python 3 stdlib only** — no third-party imports in any script (matches the existing `scripts/` convention).
- **One map parser only** — all reads/writes of `discord-channels.json` go through `channelmap.py`. Never add a second parser (mirrors the `audit_report.py` "never grow a second tag parser" rule).
- **Keep the baseline green** — `python3 -m pytest scripts/tests/ -q` is 161 passing at the start; every task ends green.
- **Commit style** — feature branch `worktree-discord-bot` (already checked out). Never push/PR unless the user asks. Commit message trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **Real IDs (already fetched, live):** guild `1526854603008905276`; channels — AAOI `1527764579940044811`, CIFR `1527758659910631597`, COHR `1528137183716835370`, IBIDY `1528072153063489636`, IREN `1528091636700024842`, LPKF `1527758892858085488`, WYFI `1528877273573359626`.
- **Embed contract unchanged** — per-ticker embed title `"<TICKER> — <Kind> (<date>)"`, green `0x2ECC71` / red `0xD9342B`; dispatcher title `"<label> — <date>"`. Chunk limit 1900. 429 `Retry-After` backoff, 5 attempts.

---

### Task 1: `channelmap.py` — committed channel-map module

**Files:**
- Create: `scripts/channelmap.py`
- Test: `scripts/tests/test_channelmap.py`

**Interfaces:**
- Consumes: nothing (stdlib only).
- Produces:
  - `DEFAULT_PATH` — `Path` to the repo-root `discord-channels.json`.
  - `load(path=DEFAULT_PATH) -> dict` — raw map incl. `_`-keys; missing file → `{}`.
  - `resolve(ticker, path=DEFAULT_PATH) -> str | None` — channel_id for ticker (case-insensitive), skipping `_`-keys and empty values.
  - `guild_id(path=DEFAULT_PATH) -> str | None`.
  - `dispatcher(path=DEFAULT_PATH) -> str | None`.
  - `write_channel(ticker, channel_id, path=DEFAULT_PATH) -> dict` — upsert ticker→id, preserve `_`-keys, sort ticker keys, write pretty JSON + trailing newline.

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_channelmap.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_channelmap.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'channelmap'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/channelmap.py`:

```python
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
    return json.loads(p.read_text(encoding="utf-8"))


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest scripts/tests/test_channelmap.py -q`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/channelmap.py scripts/tests/test_channelmap.py
git commit -m "Add channelmap.py: committed Discord channel-map parser

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `discord_common.py` — bot transport

**Files:**
- Modify: `scripts/discord_common.py` (replace `post`; keep `chunk`; add `create_channel`, `list_channels`)
- Test: `scripts/tests/test_discord_common.py` (new)

**Interfaces:**
- Consumes: `DISCORD_BOT_TOKEN` env (or explicit `token=` arg).
- Produces:
  - `chunk(body, limit=1900) -> list[str]` (unchanged).
  - `post(channel_id, payload, token=None) -> dict` — POST message; returns created-message dict.
  - `create_channel(guild_id, name, token=None) -> str` — create text channel, return new id.
  - `list_channels(guild_id, token=None) -> list[dict]` — the guild's channels.
  - `API`, `TOKEN_ENV = "DISCORD_BOT_TOKEN"`.

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_discord_common.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_discord_common.py -q`
Expected: FAIL — `AttributeError: module 'discord_common' has no attribute 'create_channel'` (and `post` signature mismatch).

- [ ] **Step 3: Write minimal implementation**

Replace the entire contents of `scripts/discord_common.py` with:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_discord_common.py -q`
Expected: PASS (5 tests).

Then confirm the two poster modules still IMPORT (their `from discord_common import chunk, post` line still resolves — signatures change but names exist), and the whole suite is still green except the two poster test files (which Tasks 3–4 rewrite; they may still pass here since none of them actually call `post`):

Run: `python3 -m pytest scripts/tests/ -q`
Expected: PASS — 166 (161 + channelmap 6 = 167, minus none; discord_common 5 new → 172). Exact count is not important; **no failures**. If `test_notify_discord_ticker.py` or `test_notify_discord_dispatch.py` fail here, note it — Tasks 3–4 replace them; do not patch around it now.

- [ ] **Step 5: Commit**

```bash
git add scripts/discord_common.py scripts/tests/test_discord_common.py
git commit -m "discord_common: switch transport from webhooks to bot REST API

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `notify_discord_ticker.py` — bot post + `--require-channel`

**Files:**
- Modify: `scripts/notify_discord_ticker.py`
- Test: `scripts/tests/test_notify_discord_ticker.py` (rewrite)

**Interfaces:**
- Consumes: `channelmap.resolve`, `channelmap.DEFAULT_PATH`, `discord_common.post`, `discord_common.chunk`.
- Produces: unchanged CLI except `--config` now points to the channel map and a new `--require-channel` flag. `build_header(ticker, tripwire_fired, kind, date)` and `KIND_LABELS` unchanged.

- [ ] **Step 1: Write the failing test**

Replace the entire contents of `scripts/tests/test_notify_discord_ticker.py` with:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_notify_discord_ticker.py -q`
Expected: FAIL — `test_posts_to_resolved_channel` references `ndt.time` and `ndt.post` with the new signature; `--require-channel` is unknown to argparse.

- [ ] **Step 3: Write minimal implementation**

Replace the entire contents of `scripts/notify_discord_ticker.py` with:

```python
#!/usr/bin/env python3
"""Post a per-ticker digest (whats-new, earnings-digest or staleness audit) to Discord.

Resolves the ticker's channel_id from the committed discord-channels.json and
posts the digest via the Discord bot (single DISCORD_BOT_TOKEN). Both run types
post to the same per-ticker channel, so the embed title names which kind of run
produced it. In CI, pass --require-channel so an unmapped ticker fails loudly
instead of skipping silently.

Python 3 stdlib only.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channelmap  # noqa: E402
from discord_common import chunk, post  # noqa: E402

KIND_LABELS = {
    "whats-new": "What's New",
    "earnings-digest": "Earnings Digest",
    "audit": "Staleness Audit",
}


def build_header(ticker, tripwire_fired, kind, date):
    label = KIND_LABELS.get(kind, kind)
    title = f"{ticker} — {label}" + (f" ({date})" if date else "")
    return {
        "embeds": [{
            "title": title,
            "color": 0xD9342B if tripwire_fired else 0x2ECC71,
        }]
    }


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Post a whats-new/earnings-digest/audit chat digest to a ticker's Discord channel."
    )
    ap.add_argument("--ticker", required=True, help="ticker symbol, e.g. LPKF")
    ap.add_argument("--kind", required=True, choices=sorted(KIND_LABELS),
                    help="which run produced this digest — titles the Discord embed")
    ap.add_argument("--date", default=None, help="the run's date (YYYY-MM-DD), shown in the embed title")
    ap.add_argument("--text-file", default=None, help="file with the chat digest; reads stdin if omitted")
    ap.add_argument("--tripwire-fired", action="store_true", help="mark the header embed red")
    ap.add_argument("--config", default=str(channelmap.DEFAULT_PATH),
                    help=f"path to the committed channel map (default: {channelmap.DEFAULT_PATH})")
    ap.add_argument("--require-channel", action="store_true",
                    help="fail (non-zero) if the ticker has no channel_id — CI passes this so a "
                         "missing mapping is loud, not a silent skip")
    ap.add_argument("--dry-run", action="store_true", help="print payloads, do not post")
    args = ap.parse_args(argv)

    ticker = args.ticker.strip().upper()
    body = (
        Path(args.text_file).read_text(encoding="utf-8") if args.text_file else sys.stdin.read()
    ).strip()

    if not body:
        print(f"[notify_discord_ticker] empty digest for {ticker} — nothing to post.", file=sys.stderr)
        return 0

    channel_id = channelmap.resolve(ticker, args.config)

    messages = [build_header(ticker, args.tripwire_fired, args.kind, args.date)]
    messages += [{"content": c} for c in chunk(body)]

    if args.dry_run:
        for msg in messages:
            print(json.dumps(msg, ensure_ascii=False))
        return 0

    if not channel_id:
        note = f"[notify_discord_ticker] no Discord channel mapped for {ticker} in {args.config}"
        if args.require_channel:
            print(note + " — failing (--require-channel).", file=sys.stderr)
            return 1
        print(note + " — skipping post.", file=sys.stderr)
        return 0

    for i, msg in enumerate(messages):
        post(channel_id, msg)
        if i < len(messages) - 1:
            time.sleep(0.6)
    print(f"[notify_discord_ticker] posted {ticker} digest to Discord ({len(messages)} message(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_notify_discord_ticker.py -q`
Expected: PASS (11 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/notify_discord_ticker.py scripts/tests/test_notify_discord_ticker.py
git commit -m "notify_discord_ticker: post via bot + channel map; add --require-channel

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: `notify_discord_dispatch.py` — bot post to `_dispatcher`

**Files:**
- Modify: `scripts/notify_discord_dispatch.py`
- Test: `scripts/tests/test_notify_discord_dispatch.py` (rewrite the webhook-specific tests)

**Interfaces:**
- Consumes: `channelmap.dispatcher`, `channelmap.DEFAULT_PATH`, `discord_common.post`, `discord_common.chunk`.
- Produces: same CLI minus `--webhook`; adds `--channel` (override) and `--config`. `build_header`, `read_summary` unchanged.

- [ ] **Step 1: Write the failing test**

Replace the entire contents of `scripts/tests/test_notify_discord_dispatch.py` with:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_notify_discord_dispatch.py -q`
Expected: FAIL — `--config` unknown, `ndd.post` old signature, `ndd.time` missing.

- [ ] **Step 3: Write minimal implementation**

Replace the entire contents of `scripts/notify_discord_dispatch.py` with:

```python
#!/usr/bin/env python3
"""Post the deterministic dispatcher's decision table to a Discord channel.

Run as an if: always() step after scripts/dispatch.py. Reads the rendered
per-ticker decision table and posts it — as a heartbeat — to the dispatcher
channel resolved from the committed discord-channels.json (`_dispatcher`) via the
Discord bot (DISCORD_BOT_TOKEN). Skips gracefully if no dispatcher channel is
configured, so the workflow stays green until it is.

The staleness audit's repo-wide sweep shares this poster and channel via --label.

Python 3 stdlib only.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channelmap  # noqa: E402
from discord_common import chunk, post  # noqa: E402


def build_header(date, status, label="Dispatcher"):
    """Header embed: title `<label> — <date>` (date omitted if None), green when
    the job succeeded, red otherwise."""
    title = label + (f" — {date}" if date else "")
    return {
        "embeds": [{
            "title": title,
            "color": 0x2ECC71 if status == "success" else 0xD9342B,
        }]
    }


def read_summary(path):
    """Return the summary table from `path`, stripped. Missing/empty -> ''."""
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8").strip()


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Post the dispatcher decision table to the dispatcher Discord channel."
    )
    ap.add_argument("--summary-file", required=True,
                    help="path to the rendered decision table written by dispatch.py")
    ap.add_argument("--date", default=None, help="run date (YYYY-MM-DD), shown in the embed title")
    ap.add_argument("--status", default="", help="workflow job status (success/failure/…)")
    ap.add_argument("--label", default="Dispatcher",
                    help="embed title prefix — the staleness-audit sweep passes 'Staleness audit'")
    ap.add_argument("--config", default=str(channelmap.DEFAULT_PATH),
                    help=f"path to the committed channel map (default: {channelmap.DEFAULT_PATH})")
    ap.add_argument("--channel", default=None,
                    help="dispatcher channel_id override; defaults to `_dispatcher` in the map")
    ap.add_argument("--dry-run", action="store_true", help="print payloads, do not post")
    args = ap.parse_args(argv)

    body = read_summary(args.summary_file)
    if not body:
        body = (
            f"⚠️ {args.label} run did not produce a summary "
            f"(status: {args.status or 'unknown'}). See the Actions run logs."
        )

    messages = [build_header(args.date, args.status, args.label)]
    messages += [{"content": c} for c in chunk(body)]

    if args.dry_run:
        for msg in messages:
            print(json.dumps(msg, ensure_ascii=False))
        return 0

    channel_id = args.channel or channelmap.dispatcher(args.config)
    if not channel_id:
        print(
            f"[notify_discord_dispatch] no _dispatcher channel configured in {args.config} — skipping post.",
            file=sys.stderr,
        )
        return 0

    for i, msg in enumerate(messages):
        post(channel_id, msg)
        if i < len(messages) - 1:
            time.sleep(0.6)
    print(f"[notify_discord_dispatch] posted dispatcher summary to Discord ({len(messages)} message(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_notify_discord_dispatch.py -q`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/notify_discord_dispatch.py scripts/tests/test_notify_discord_dispatch.py
git commit -m "notify_discord_dispatch: post via bot to _dispatcher channel

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: `onboard_discord_channel.py` — idempotent channel onboarding

**Files:**
- Create: `scripts/onboard_discord_channel.py`
- Test: `scripts/tests/test_onboard_discord_channel.py`

**Interfaces:**
- Consumes: `channelmap.resolve/guild_id/write_channel`, `discord_common.create_channel/list_channels`.
- Produces: CLI `--ticker X [--name ...] [--config ...] [--dry-run]`; `main(argv) -> int`.

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_onboard_discord_channel.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_onboard_discord_channel.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'onboard_discord_channel'`.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/onboard_discord_channel.py`:

```python
#!/usr/bin/env python3
"""Idempotently ensure a ticker has a Discord channel and record it in the map.

Run once when onboarding a ticker (the bot needs Manage Channels). Requires
DISCORD_BOT_TOKEN and a `_guild_id` in discord-channels.json. Order of operations:
  1. already mapped        -> no-op
  2. a guild channel with the target name exists -> adopt its id
  3. otherwise             -> create the channel
then write the id back to the committed map (leave it staged for a human commit).

Naming: --name preserves themed names (e.g. "AAOI Oracle"); default is the
lowercased ticker.

Python 3 stdlib only.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channelmap  # noqa: E402
from discord_common import create_channel, list_channels  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ensure a ticker's Discord channel exists and is mapped.")
    ap.add_argument("--ticker", required=True, help="ticker symbol, e.g. WYFI")
    ap.add_argument("--name", default=None, help="channel name (default: lowercased ticker)")
    ap.add_argument("--config", default=str(channelmap.DEFAULT_PATH),
                    help=f"path to the committed channel map (default: {channelmap.DEFAULT_PATH})")
    ap.add_argument("--dry-run", action="store_true", help="report intent, do not create or write")
    args = ap.parse_args(argv)

    ticker = args.ticker.strip().upper()

    existing = channelmap.resolve(ticker, args.config)
    if existing:
        print(f"[onboard] {ticker} already mapped to channel {existing} — no-op.")
        return 0

    gid = channelmap.guild_id(args.config)
    if not gid:
        print(f"[onboard] no _guild_id in {args.config} — cannot create a channel.", file=sys.stderr)
        return 1

    name = args.name or ticker.lower()

    if args.dry_run:
        print(f"[onboard] would ensure channel '{name}' in guild {gid} and map {ticker}.")
        return 0

    match = None
    for ch in list_channels(gid):
        if ch.get("name") == name and ch.get("type") == 0:
            match = str(ch["id"])
            break

    channel_id = match or create_channel(gid, name)
    channelmap.write_channel(ticker, channel_id, args.config)
    verb = "adopted" if match else "created"
    print(f"[onboard] {verb} channel '{name}' ({channel_id}); wrote {ticker} to {args.config}. Commit it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_onboard_discord_channel.py -q`
Expected: PASS (5 tests).

- [ ] **Step 5: Full suite + commit**

Run: `python3 -m pytest scripts/tests/ -q`
Expected: PASS, no failures.

```bash
git add scripts/onboard_discord_channel.py scripts/tests/test_onboard_discord_channel.py
git commit -m "Add onboard_discord_channel.py: idempotent channel onboarding + map write-back

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Committed `discord-channels.json` + remove webhook secrets

**Files:**
- Create: `discord-channels.json` (repo root)
- Delete: `.secrets/discord-webhooks.example.json` (tracked)
- Note: `.secrets/discord-webhooks.json` is gitignored (only in the main checkout) — not tracked here; the human removes it manually after cutover.

This task has no unit test (it's config data). Verification is a JSON-parse + a `channelmap.resolve` smoke check.

- [ ] **Step 1: Create the committed map with real IDs**

Create `discord-channels.json` at the repo root:

```json
{
  "_comment": "Committed, NON-SECRET: Discord channel/guild IDs are visible to anyone in the server. Single source of truth for ticker->channel routing (replaces the old gitignored webhook map). Onboard a ticker with scripts/onboard_discord_channel.py, then commit this file. Keys are ticker symbols; values are channel-ID snowflakes. _dispatcher is the dispatcher/audit heartbeat channel.",
  "_guild_id": "1526854603008905276",
  "AAOI": "1527764579940044811",
  "CIFR": "1527758659910631597",
  "COHR": "1528137183716835370",
  "IBIDY": "1528072153063489636",
  "IREN": "1528091636700024842",
  "LPKF": "1527758892858085488",
  "WYFI": "1528877273573359626"
}
```

(`_dispatcher` is intentionally absent — added in Task 8 once its channel id is obtained; until then `notify_discord_dispatch` skips gracefully.)

- [ ] **Step 2: Smoke-check it parses and resolves**

Run:
```bash
python3 -c "import sys; sys.path.insert(0,'scripts'); import channelmap as c; \
print('guild', c.guild_id('discord-channels.json')); \
print('AAOI', c.resolve('aaoi','discord-channels.json')); \
print('dispatcher', c.dispatcher('discord-channels.json'))"
```
Expected:
```
guild 1526854603008905276
AAOI 1527764579940044811
dispatcher None
```

- [ ] **Step 3: Delete the tracked webhook example**

Run: `git rm .secrets/discord-webhooks.example.json`
Expected: `rm '.secrets/discord-webhooks.example.json'`.

- [ ] **Step 4: Commit**

```bash
git add discord-channels.json
git commit -m "Add committed discord-channels.json; drop tracked webhook example

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: `whats-new.yml` + `earnings-digest.yml` — deterministic post step

**Files:**
- Modify: `.gitignore`
- Modify: `.github/workflows/whats-new.yml`
- Modify: `.github/workflows/earnings-digest.yml`

No unit test (workflow YAML). The stdlib has no `yaml`; validate with `actionlint` if present, else the grep assertions below.

**Key facts (verified):**
- The digest and pr-body files are already gitignored (`.gitignore` lines 22–25): `/whats-new-digest.md`, `/whats-new-pr-body.md`, `/earnings-digest-body.md`, `/earnings-digest-pr-body.md`. The earnings digest file is **`earnings-digest-body.md`** (NOT `-digest.md`).
- **whats-new.yml**: the WORKFLOW owns git — a `Commit, push, open & merge PR` step runs `git add -A`. Claude step is `Run what's-new check` (`id: claude`).
- **earnings-digest.yml**: the AGENT owns git — inside the prompt it runs `git checkout -b … && git add -A && git commit && git push && gh pr create` (it does NOT merge; a later step does). Claude step is `Run earnings digest` (`id: claude`), followed by `Summarize token usage` → `Append token usage… squash-merge` → `Rebuild the Pages site`.
- Because the agent runs `git add -A` in earnings-digest, the tripwire sentinel MUST be gitignored (a workflow-side `rm` can't run before the agent's own add). Gitignoring is used for BOTH workflows for consistency.

- [ ] **Step 1: Gitignore the sentinel files**

In `.gitignore`, right after the existing `/earnings-digest-pr-body.md` line, add:

```
/whats-new-tripwire.flag
/earnings-digest-tripwire.flag
```

Verify: `git check-ignore whats-new-tripwire.flag earnings-digest-tripwire.flag` → prints both paths.

- [ ] **Step 2: `whats-new.yml` — remove the Materialize step**

Delete this entire step (currently lines ~64–75):

```yaml
      - name: Materialize Discord webhook config
        env:
          WEBHOOKS_JSON: ${{ secrets.DISCORD_WEBHOOKS_JSON }}
        run: |
          set -euo pipefail
          if [ -n "${WEBHOOKS_JSON:-}" ]; then
            mkdir -p .secrets
            printf '%s' "$WEBHOOKS_JSON" > .secrets/discord-webhooks.json
            echo "Wrote .secrets/discord-webhooks.json from DISCORD_WEBHOOKS_JSON."
          else
            echo "DISCORD_WEBHOOKS_JSON not set — the Discord post will skip gracefully."
          fi
```

- [ ] **Step 3: `whats-new.yml` — drop the post instruction from the prompt, add a tripwire sentinel**

Replace the "Post the digest…" bullet (currently lines ~139–145):

```
              - Post the digest to the ticker's Discord channel (add --tripwire-fired only
                if a [TRIPWIRE] hit this run):
                  python scripts/notify_discord_ticker.py \
                    --ticker ${{ steps.meta.outputs.ticker }} --kind whats-new \
                    --date ${{ steps.meta.outputs.date }} --text-file whats-new-digest.md
                The poster exits 0 and skips if no webhook is configured for the ticker —
                that is expected, not an error.
```

with (the agent no longer posts — it only signals whether a tripwire fired; the sentinel is gitignored, so its own working tree stays clean of it):

```
              - Do NOT post to Discord — a later workflow step posts deterministically from
                whats-new-digest.md. Only signal a fired tripwire: if any [TRIPWIRE] hit this
                run, create an empty file `whats-new-tripwire.flag` in the repo root (it is
                gitignored); otherwise do not create it.
```

- [ ] **Step 4: `whats-new.yml` — add a deterministic post step after the Claude step**

Insert immediately AFTER the `Run what's-new check` step (before `Summarize token usage`):

```yaml
      - name: Post digest to Discord
        if: always()
        env:
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          TICKER: ${{ steps.meta.outputs.ticker }}
          DATE: ${{ steps.meta.outputs.date }}
        run: |
          set -uo pipefail
          if [ ! -s whats-new-digest.md ]; then
            echo "No whats-new-digest.md produced — nothing to post."
            exit 0
          fi
          FLAG=""
          [ -f whats-new-tripwire.flag ] && FLAG="--tripwire-fired"
          python3 scripts/notify_discord_ticker.py \
            --ticker "$TICKER" --kind whats-new --date "$DATE" \
            --text-file whats-new-digest.md --require-channel $FLAG
```

`--require-channel` makes an unmapped ticker fail this step visibly. No commit-step cleanup is needed — the sentinel is gitignored (Step 1), so `git add -A` won't stage it.

- [ ] **Step 5: `earnings-digest.yml` — remove the Materialize step**

Delete its `Materialize Discord webhook config` step (lines ~62–72), identical in shape to whats-new's.

- [ ] **Step 6: `earnings-digest.yml` — drop the post instruction from the prompt, add a sentinel**

Replace this bullet in the prompt (the "Post it to the ticker's Discord channel…" block):

```
              - Post it to the ticker's Discord channel (add --tripwire-fired only if a
                [TRIPWIRE] fired this run):
                  python scripts/notify_discord_ticker.py \
                    --ticker ${{ steps.meta.outputs.ticker }} --kind earnings-digest \
                    --date ${{ steps.meta.outputs.date }} --text-file earnings-digest-body.md
                The poster exits 0 and skips if no webhook is configured — that is expected.
```

with:

```
              - Do NOT post to Discord — a later workflow step posts deterministically from
                earnings-digest-body.md. Only signal a fired tripwire: if any [TRIPWIRE] fired
                this run, create an empty file `earnings-digest-tripwire.flag` in the repo root
                (it is gitignored, so your `git add -A` will not stage it); otherwise do not
                create it.
```

Also remove the now-stale `* a final line: "Full digest posted to Discord."` requirement from the PR-body bullet just below (the digest is still posted, just by a later step — leave the debrief link but drop that final line to avoid asserting an order the agent no longer controls). This is optional polish; if in doubt leave it.

- [ ] **Step 7: `earnings-digest.yml` — add a deterministic post step after the Claude step**

Insert immediately AFTER the `Run earnings digest` step (before `Summarize token usage`). The digest file is gitignored, so it survives in the working tree after the agent's own commit:

```yaml
      - name: Post digest to Discord
        if: always()
        env:
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          TICKER: ${{ steps.meta.outputs.ticker }}
          DATE: ${{ steps.meta.outputs.date }}
        run: |
          set -uo pipefail
          if [ ! -s earnings-digest-body.md ]; then
            echo "No earnings-digest-body.md produced — nothing to post."
            exit 0
          fi
          FLAG=""
          [ -f earnings-digest-tripwire.flag ] && FLAG="--tripwire-fired"
          python3 scripts/notify_discord_ticker.py \
            --ticker "$TICKER" --kind earnings-digest --date "$DATE" \
            --text-file earnings-digest-body.md --require-channel $FLAG
```

- [ ] **Step 8: Verify no webhook references remain and steps are wired**

Run:
```bash
grep -n "DISCORD_WEBHOOKS_JSON\|discord-webhooks\|Materialize Discord" .github/workflows/whats-new.yml .github/workflows/earnings-digest.yml || echo "clean: no webhook refs"
grep -c "Post digest to Discord" .github/workflows/whats-new.yml .github/workflows/earnings-digest.yml
grep -n "DISCORD_BOT_TOKEN\|--require-channel" .github/workflows/whats-new.yml .github/workflows/earnings-digest.yml
```
Expected: first prints `clean: no webhook refs`; second shows `1` for each file; third shows the bot token env and `--require-channel` in both.

If `actionlint` is installed: `actionlint .github/workflows/whats-new.yml .github/workflows/earnings-digest.yml` → no errors. If not, skip (note it).

- [ ] **Step 9: Commit**

```bash
git add .gitignore .github/workflows/whats-new.yml .github/workflows/earnings-digest.yml
git commit -m "whats-new/earnings-digest: deterministic bot post step, drop webhook materialize

Move the Discord post out of the hidden Claude prompt into a visible workflow
step (--require-channel makes a missing mapping loud). Agent only signals a
fired tripwire via a gitignored sentinel file.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: `dispatcher.yml` + `audit.yml` — repoint to the bot

**Files:**
- Modify: `.github/workflows/dispatcher.yml`
- Modify: `.github/workflows/audit.yml`
- Modify: `discord-channels.json` (add `_dispatcher`)

- [ ] **Step 1: Obtain the dispatcher channel id and add `_dispatcher`**

The dispatcher channel id is the channel the old `DISCORD_DISPATCHER_WEBHOOK` posted to. Obtain it once (either command works):

- From Discord: enable Developer Mode → right-click the dispatcher channel → Copy Channel ID.
- Or from the existing webhook secret value, if you still have the URL locally:
  ```bash
  curl -s "<DISCORD_DISPATCHER_WEBHOOK url>" -H 'User-Agent: x' | python3 -c "import sys,json;print(json.load(sys.stdin)['channel_id'])"
  ```

Add the resulting id to `discord-channels.json` as `_dispatcher` (place it right after `_guild_id`), e.g.:

```json
  "_guild_id": "1526854603008905276",
  "_dispatcher": "<dispatcher channel id>",
```

- [ ] **Step 2: `dispatcher.yml` — swap the webhook env for the bot token**

Replace (line ~67):

```yaml
          DISCORD_DISPATCHER_WEBHOOK: ${{ secrets.DISCORD_DISPATCHER_WEBHOOK }}
```

with:

```yaml
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
```

The `python3 scripts/notify_discord_dispatch.py --summary-file …` invocation needs no change — it now resolves `_dispatcher` from the committed map.

- [ ] **Step 3: `audit.yml` — remove Materialize, swap dispatcher env**

- Delete the `Materialize Discord webhook config` step (lines ~71–82).
- Add `DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}` to the env of every step that runs `audit_notify.py` or `notify_discord_dispatch.py` (the per-ticker audit posts go through `notify_discord_ticker.py --kind audit`, which now needs the bot token too).
- Replace the `DISCORD_DISPATCHER_WEBHOOK` env (line ~120) with `DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}`.

Read `audit.yml` around the `audit_notify.py` invocation to confirm which steps shell out to the posters, and put the bot-token env on each. The per-ticker audit poster should also gain `--require-channel` only if audit runs should hard-fail on an unmapped ticker; per spec, audit posting keeps the graceful-skip behavior (it sweeps quiet tickers that may legitimately lack a channel), so do NOT add `--require-channel` in audit.yml.

- [ ] **Step 4: Verify**

Run:
```bash
grep -rn "DISCORD_DISPATCHER_WEBHOOK\|DISCORD_WEBHOOKS_JSON\|Materialize Discord\|discord-webhooks" .github/workflows/ || echo "clean: no webhook refs in any workflow"
python3 -c "import sys; sys.path.insert(0,'scripts'); import channelmap as c; print('dispatcher', c.dispatcher('discord-channels.json'))"
```
Expected: `clean: no webhook refs in any workflow`; `dispatcher <id>` (non-None).

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/dispatcher.yml .github/workflows/audit.yml discord-channels.json
git commit -m "dispatcher/audit: post via bot to _dispatcher channel; retire dispatcher webhook

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: Docs — CLAUDE.md + scripts plan

**Files:**
- Modify: `CLAUDE.md` (file-map entries)
- Modify: `docs/part-2-scripts-plan.md`

- [ ] **Step 1: Update `CLAUDE.md` file-map entries**

Read `CLAUDE.md` and update these bullet descriptions to the bot model:
- `scripts/notify_discord_ticker.py` — now resolves the ticker's channel_id from the committed `discord-channels.json` and posts via the Discord bot (`DISCORD_BOT_TOKEN`); replace the `.secrets/discord-webhooks.json` / "skips if no webhook" language with "resolves from the committed channel map; `--require-channel` makes CI fail loudly on an unmapped ticker, otherwise skips gracefully."
- `scripts/dispatch.py` paragraph — the heartbeat now posts via the bot to the `_dispatcher` channel (no `DISCORD_DISPATCHER_WEBHOOK`).
- `scripts/notify_discord_dispatch.py` — posts via the bot to `_dispatcher`; drop the single-URL-secret language.
- Add two new file-map bullets: `scripts/channelmap.py` (the sole committed-channel-map parser) and `scripts/onboard_discord_channel.py` (idempotent channel onboarding), and `discord-channels.json` (committed, non-secret routing map).
- Replace any remaining mention of `.secrets/discord-webhooks.json` / `.example.json` with the committed map + `DISCORD_BOT_TOKEN` secret.

- [ ] **Step 2: Update `docs/part-2-scripts-plan.md`**

Read it and update the Discord-notification references from the webhook map to the bot + committed map. Keep the historical spec `docs/superpowers/specs/2026-07-18-dispatcher-discord-notification-design.md` unchanged (dated record).

- [ ] **Step 3: Verify no stale webhook references remain in docs**

Run:
```bash
grep -rn "discord-webhooks\|DISCORD_WEBHOOKS_JSON\|DISCORD_DISPATCHER_WEBHOOK" CLAUDE.md docs/part-2-scripts-plan.md || echo "clean"
```
Expected: `clean` (the dated 2026-07-18 spec may still reference the old secret — that's fine, it's history).

- [ ] **Step 4: Full suite + commit**

Run: `python3 -m pytest scripts/tests/ -q`
Expected: PASS, no failures.

```bash
git add CLAUDE.md docs/part-2-scripts-plan.md
git commit -m "docs: describe the Discord bot transport + committed channel map

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Post-implementation (human, outside this plan)

These require the live bot and are NOT automated here:

1. **Create the Discord application + bot**, invite it to the guild with **Send Messages + Manage Channels**, and set the `DISCORD_BOT_TOKEN` repo secret (`gh secret set DISCORD_BOT_TOKEN`). Also export it locally for ad-hoc runs.
2. **Fill `_dispatcher`** in `discord-channels.json` (Task 8 Step 1) if not already done.
3. **Smoke test**: `DISCORD_BOT_TOKEN=… python3 scripts/notify_discord_ticker.py --ticker AAOI --kind whats-new --date 2026-07-21 --text-file <some file> --dry-run` (dry-run first), then a real post to confirm the bot reaches the channel.
4. **Retire the old secrets**: delete `DISCORD_WEBHOOKS_JSON` and `DISCORD_DISPATCHER_WEBHOOK` repo secrets, and remove the local `.secrets/discord-webhooks.json`.
5. **Re-dispatch AAOI** what's-new to confirm the deterministic post step posts and is visible in the job log.
