#!/usr/bin/env python3
"""Post a daily-watch summary file to a Discord webhook.

Reads summaries/<date>.md (frontmatter + §B digest body), builds a colored
header embed, chunks the body under Discord's message limit, and POSTs.
Python 3 stdlib only — runs on a bare GitHub Actions runner.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RED = 0xD9342B
GREEN = 0x2ECC71

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def parse_summary(path):
    text = Path(path).read_text(encoding="utf-8")
    meta_raw, body = {}, text
    m = _FRONTMATTER.match(text)
    if m:
        fm, body = m.group(1), m.group(2)
        for line in fm.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta_raw[key.strip()] = val.split("#", 1)[0].strip()

    def as_int(key):
        try:
            return int(meta_raw.get(key, 0))
        except ValueError:
            return 0

    meta = {
        "date": meta_raw.get("date") or Path(path).stem,
        "tickers_checked": as_int("tickers_checked"),
        "tripwires_fired": as_int("tripwires_fired"),
        "edge_shifts": as_int("edge_shifts"),
    }
    return meta, body.strip("\n")


def build_header_embed(meta, file_url=None):
    color = RED if meta["tripwires_fired"] > 0 else GREEN
    counts = (
        f'{meta["tripwires_fired"]} tripwire(s) · '
        f'{meta["edge_shifts"]} edge shift(s) · '
        f'{meta["tickers_checked"]} checked'
    )
    description = counts
    if file_url:
        description += f"\n[Full run →]({file_url})"
    return {
        "embeds": [{
            "title": f'Daily Watch — {meta["date"]}',
            "description": description,
            "color": color,
        }]
    }


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
    req = urllib.request.Request(
        webhook_url, data=data, headers={"Content-Type": "application/json"})
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


def main(argv=None):
    ap = argparse.ArgumentParser(description="Post a summary file to Discord.")
    ap.add_argument("summary", help="path to summaries/<date>.md")
    ap.add_argument("--file-url", default=None, help="URL for the 'Full run →' link")
    ap.add_argument("--dry-run", action="store_true", help="print payloads, do not post")
    args = ap.parse_args(argv)

    meta, body = parse_summary(args.summary)
    messages = [build_header_embed(meta, args.file_url)]
    messages += [{"content": c} for c in chunk(body)]

    if args.dry_run:
        for msg in messages:
            print(json.dumps(msg, ensure_ascii=False))
        return 0

    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("DISCORD_WEBHOOK_URL not set", file=sys.stderr)
        return 1

    for i, msg in enumerate(messages):
        post(webhook, msg)
        if i < len(messages) - 1:
            time.sleep(0.6)
    return 0


if __name__ == "__main__":
    sys.exit(main())
