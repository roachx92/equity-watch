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
