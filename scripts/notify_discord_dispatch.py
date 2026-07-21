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
