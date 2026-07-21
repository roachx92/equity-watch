#!/usr/bin/env python3
"""Reconcile Discord channels with the watch-list.

Enumerate watched tickers (the `tickers/<T>/news.md` folders — the repo's
watch-list) and ensure each has a channel in the committed discord-channels.json,
creating any that are missing. Idempotent: a ticker that already has a channel_id
is skipped, so re-running is always safe. Run manually, or by the
`discord-channel-sync` workflow on push to `tickers/**`.

Requires DISCORD_BOT_TOKEN and a `_guild_id` in the map. Auto-created channels get
the DEFAULT (lowercased-ticker) name — CI can't invent a themed name; onboard a
themed name manually first (scripts/onboard_discord_channel.py --name …) and the
sync will then see it as already-mapped and leave it alone.

Python 3 stdlib only.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from onboard_discord_channel import ensure_channel  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def watched_tickers(repo_root=REPO_ROOT):
    """Ticker symbols from the watch-list: `tickers/<T>/news.md` folders.
    A folder counts only if it carries a news.md (the watch-list unit), so
    stray directories are ignored. Returns upper-cased symbols, sorted."""
    tickers_dir = Path(repo_root) / "tickers"
    return sorted(
        p.parent.name.strip().upper()
        for p in tickers_dir.glob("*/news.md")
    )


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Create Discord channels for any watched ticker missing one."
    )
    ap.add_argument("--config", default=None,
                    help="path to the committed channel map (default: <repo-root>/discord-channels.json)")
    ap.add_argument("--repo-root", default=str(REPO_ROOT),
                    help="repo root holding the tickers/ watch-list (default: this repo)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report which channels would be created, create nothing")
    args = ap.parse_args(argv)

    # Keep the map coupled to the watch-list it's reconciling: default --config to
    # the map inside --repo-root, so a non-default --repo-root can't silently read
    # tickers from one checkout while writing the map of another.
    config = args.config or str(Path(args.repo_root) / "discord-channels.json")

    tickers = watched_tickers(args.repo_root)
    provisioned = []
    try:
        for ticker in tickers:
            action, channel_id = ensure_channel(ticker, None, config, args.dry_run)
            if action != "already-mapped":
                provisioned.append((ticker, action, channel_id))
                suffix = f" ({channel_id})" if channel_id else ""
                print(f"[sync] {ticker}: {action}{suffix}")
    except ValueError as exc:
        print(f"[sync] {exc} — cannot create channels.", file=sys.stderr)
        return 1

    if not provisioned:
        print(f"[sync] all {len(tickers)} watched tickers already have channels — no-op.")
    else:
        verb = "to create" if args.dry_run else "created/adopted"
        print(f"[sync] {len(provisioned)} channel(s) {verb} of {len(tickers)} watched tickers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
