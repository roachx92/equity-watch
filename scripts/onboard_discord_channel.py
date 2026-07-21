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


def _slug(name):
    """Approximate Discord's channel-name slugification for matching: lowercase,
    collapse whitespace runs to single hyphens, strip surrounding whitespace."""
    return "-".join(name.strip().lower().split())


def ensure_channel(ticker, name=None, config=channelmap.DEFAULT_PATH, dry_run=False):
    """Idempotently ensure `ticker` has a channel in the committed map.

    Returns (action, channel_id) where action is one of:
      'already-mapped' — the ticker already had a channel_id (channel_id returned)
      'would-create'   — dry-run: a channel would be created (channel_id None)
      'adopted'        — an existing guild channel matched by slug was mapped
      'created'        — a new channel was created and mapped
    Raises ValueError if the ticker is unmapped and no `_guild_id` is configured.
    Reused by both the onboard CLI and sync_discord_channels.py.
    """
    ticker = ticker.strip().upper()

    existing = channelmap.resolve(ticker, config)
    if existing:
        return ("already-mapped", existing)

    gid = channelmap.guild_id(config)
    if not gid:
        raise ValueError(f"no _guild_id in {config}")

    name = name or ticker.lower()

    if dry_run:
        return ("would-create", None)

    match = None
    target = _slug(name)
    for ch in list_channels(gid):
        if ch.get("type") == 0 and _slug(ch.get("name", "")) == target:
            match = str(ch["id"])
            break

    channel_id = match or create_channel(gid, name)
    channelmap.write_channel(ticker, channel_id, config)
    return (("adopted" if match else "created"), channel_id)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ensure a ticker's Discord channel exists and is mapped.")
    ap.add_argument("--ticker", required=True, help="ticker symbol, e.g. WYFI")
    ap.add_argument("--name", default=None, help="channel name (default: lowercased ticker)")
    ap.add_argument("--config", default=str(channelmap.DEFAULT_PATH),
                    help=f"path to the committed channel map (default: {channelmap.DEFAULT_PATH})")
    ap.add_argument("--dry-run", action="store_true", help="report intent, do not create or write")
    args = ap.parse_args(argv)

    ticker = args.ticker.strip().upper()
    name = args.name or ticker.lower()

    try:
        action, channel_id = ensure_channel(ticker, args.name, args.config, args.dry_run)
    except ValueError as exc:
        print(f"[onboard] {exc} — cannot create a channel.", file=sys.stderr)
        return 1

    if action == "already-mapped":
        print(f"[onboard] {ticker} already mapped to channel {channel_id} — no-op.")
    elif action == "would-create":
        gid = channelmap.guild_id(args.config)
        print(f"[onboard] would ensure channel '{name}' in guild {gid} and map {ticker}.")
    else:
        print(f"[onboard] {action} channel '{name}' ({channel_id}); wrote {ticker} to {args.config}. Commit it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
