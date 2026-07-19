#!/usr/bin/env python3
"""Post the deterministic dispatcher's decision table to a Discord channel.

Run as a step in .github/workflows/dispatcher.yml (if: always()) after
scripts/dispatch.py. Reads the rendered per-ticker decision table that dispatch.py
writes to a file and posts it — as a daily heartbeat — to a dedicated dispatcher
Discord channel. The webhook URL comes from the DISCORD_DISPATCHER_WEBHOOK repo
secret (a single URL, not the per-ticker map); if it is unset the step skips
gracefully, so the workflow stays green until the secret is configured.

Unlike the per-ticker poster (notify_discord_ticker.py), the dispatcher table is
repo-wide, so it has its own channel and its own single-URL secret.

Python 3 stdlib only.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from discord_common import chunk, post  # noqa: E402

WEBHOOK_ENV = "DISCORD_DISPATCHER_WEBHOOK"


def build_header(date, status, label="Dispatcher"):
    """Header embed: title `<label> — <date>` (date omitted if None),
    green when the job succeeded, red otherwise.

    `label` exists so the staleness audit's repo-wide sweep roll-up can share
    this poster and this channel (§J.5) without a third near-identical script.
    """
    title = label + (f" — {date}" if date else "")
    return {
        "embeds": [{
            "title": title,
            "color": 0x2ECC71 if status == "success" else 0xD9342B,
        }]
    }


def read_summary(path):
    """Return the dispatcher summary table from `path`, stripped. Missing file
    or empty content -> '' (the caller substitutes a fallback body)."""
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8").strip()


def main(argv=None):
    # Match the per-ticker poster: force UTF-8 stdio so an emoji-bearing body
    # cannot crash on a cp1252 console.
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
                    help="embed title prefix — the staleness-audit sweep shares this "
                         "channel and passes 'Staleness audit' (§J.5)")
    ap.add_argument("--webhook", default=None,
                    help=f"webhook URL override; defaults to the {WEBHOOK_ENV} env var")
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

    webhook = args.webhook or os.environ.get(WEBHOOK_ENV, "")
    if not webhook:
        print(
            f"[notify_discord_dispatch] no {WEBHOOK_ENV} configured — skipping post.",
            file=sys.stderr,
        )
        return 0

    for i, msg in enumerate(messages):
        post(webhook, msg)
        if i < len(messages) - 1:
            import time
            time.sleep(0.6)
    print(f"[notify_discord_dispatch] posted dispatcher summary to Discord ({len(messages)} message(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
