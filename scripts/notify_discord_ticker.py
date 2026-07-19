#!/usr/bin/env python3
"""Post a per-ticker digest (whats-new, earnings-digest or staleness audit) to Discord.

Run locally at the end of a /whats-new or /earnings-digest <TICKER> session (not
CI-triggered — ad-hoc runs aren't pushed to GitHub on every check, so there's no
push event to hang a GitHub Action off of). Looks up TICKER in a local, gitignored
webhook-URL config and posts the digest text to that channel. Both run types post
to the same per-ticker channel, so the embed title always names which kind of run
produced it — otherwise the two are indistinguishable in the Discord feed.

Python 3 stdlib only.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from discord_common import chunk, post  # noqa: E402

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / ".secrets" / "discord-webhooks.json"

KIND_LABELS = {
    "whats-new": "What's New",
    "earnings-digest": "Earnings Digest",
    "audit": "Staleness Audit",
}


def load_webhooks(config_path):
    path = Path(config_path)
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    # normalize keys to upper-case ticker symbols
    return {k.strip().upper(): v for k, v in raw.items() if v}


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
    # The digest is emoji-heavy; Windows consoles default to a codec (cp1252)
    # that can't print it. Force UTF-8 stdout/stderr so local runs don't crash.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Post a whats-new or earnings-digest chat digest to a ticker's Discord webhook."
    )
    ap.add_argument("--ticker", required=True, help="ticker symbol, e.g. LPKF")
    ap.add_argument(
        "--kind",
        required=True,
        choices=sorted(KIND_LABELS),
        help="which run produced this digest — titles the Discord embed so the two are "
             "distinguishable in the feed (both post to the same per-ticker channel)",
    )
    ap.add_argument(
        "--date",
        default=None,
        help="the run's date (YYYY-MM-DD, from the session's current-date context — "
             "not inferred), shown in the embed title",
    )
    ap.add_argument(
        "--text-file",
        default=None,
        help="path to a file containing the chat digest; reads stdin if omitted",
    )
    ap.add_argument(
        "--tripwire-fired",
        action="store_true",
        help="mark the header embed red (a Tripwire fired this run)",
    )
    ap.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help=f"path to the webhook-URL config JSON (default: {DEFAULT_CONFIG})",
    )
    ap.add_argument("--dry-run", action="store_true", help="print payloads, do not post")
    args = ap.parse_args(argv)

    ticker = args.ticker.strip().upper()
    body = (
        Path(args.text_file).read_text(encoding="utf-8")
        if args.text_file
        else sys.stdin.read()
    ).strip()

    if not body:
        print(f"[notify_discord_ticker] empty digest for {ticker} — nothing to post.", file=sys.stderr)
        return 0

    webhooks = load_webhooks(args.config)
    webhook = webhooks.get(ticker)

    messages = [build_header(ticker, args.tripwire_fired, args.kind, args.date)]
    messages += [{"content": c} for c in chunk(body)]

    if args.dry_run:
        for msg in messages:
            print(json.dumps(msg, ensure_ascii=False))
        return 0

    if not webhook:
        # Not configured — skip gracefully, don't fail the /whats-new run over it.
        print(
            f"[notify_discord_ticker] no Discord webhook configured for {ticker} "
            f"in {args.config} — skipping post.",
            file=sys.stderr,
        )
        return 0

    for i, msg in enumerate(messages):
        post(webhook, msg)
        if i < len(messages) - 1:
            import time
            time.sleep(0.6)
    print(f"[notify_discord_ticker] posted {ticker} digest to Discord ({len(messages)} message(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
