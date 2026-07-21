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
