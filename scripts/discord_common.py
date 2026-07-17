"""Shared Discord-webhook posting helpers — stdlib only.

Used by both notify_discord.py (the daily-watch summary poster, CI-triggered)
and notify_discord_ticker.py (the ad-hoc per-ticker poster, run locally at
the end of a /whats-new session).
"""
import json
import time
import urllib.error
import urllib.request


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


def post(webhook_url, payload):
    data = json.dumps(payload).encode("utf-8")
    # Discord (via Cloudflare) 403s the default Python-urllib UA; send a real one.
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "equity-watch-notifier/1.0 (+https://github.com/roachx92/equity-watch)",
        },
    )
    for _ in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                time.sleep(float(exc.headers.get("Retry-After", "1")))
                continue
            raise
    raise RuntimeError("Discord POST failed after retries (HTTP 429)")
