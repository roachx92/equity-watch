# Dispatcher Discord notification — design

**Date:** 2026-07-18
**Status:** approved (design), pending implementation

## Goal

`.github/workflows/dispatcher.yml` runs every weekday morning (~09:30 ET) — a
deterministic, Claude-free Python pre-filter (`scripts/dispatch.py`) that decides
which watched tickers warrant a paid earnings-digest / what's-new run and fires
them via `gh workflow run`. Today its only output is a per-ticker decision table
written to the Actions job summary, which nobody sees unless they open the run.

**We want a Discord notification of the dispatcher results on every run** — a
daily heartbeat that confirms the cron fired and shows the full per-ticker
decision table.

## Decisions (locked)

- **Trigger:** post on **every** run (heartbeat), including quiet "nothing
  dispatched" mornings. Confirms the cron fired.
- **Content:** the **full per-ticker decision table** — the same Markdown table
  `dispatch.py` already renders to the Actions job summary.
- **Channel / webhook:** a **dedicated** Discord channel, delivered via a new
  GitHub Actions secret `DISCORD_DISPATCHER_WEBHOOK` (a single webhook URL).
  Rationale: the dispatcher table is repo-wide, not per-ticker, so it does not
  belong in any ticker's channel. The per-ticker `.secrets/discord-webhooks.json`
  map (rebuilt in CI from the `DISCORD_WEBHOOKS_JSON` secret) is keyed by ticker
  symbol; overloading it with a reserved non-ticker key would muddy that
  contract. A separate single-URL secret is cleaner.

## Non-goals

- No change to the per-ticker `.secrets/discord-webhooks.json` contract or the
  `.secrets/*.example.json` template — those stay per-ticker.
- No condensed/summary message format — the full table is the payload.
- No change to what the dispatcher *decides* or dispatches.

## Architecture (Approach A — dedicated script + `if: always()` step)

The dispatcher is a Claude-free deterministic job, so the notification is plain
Python + a workflow step (not `claude-code-action`). It mirrors the existing
`scripts/notify_discord_ticker.py`, reusing `scripts/discord_common.py`.

### 1. `scripts/notify_discord_dispatch.py` (new, stdlib-only)

Posts the dispatcher decision table to the dispatcher Discord channel.

- **Inputs (argparse):**
  - `--summary-file PATH` — file holding the rendered Markdown table (written by
    `dispatch.py`, see §2).
  - `--date YYYY-MM-DD` — the run date, shown in the embed title.
  - `--status STATUS` — the workflow job status (`success` / `failure` /
    `cancelled`), from `${{ job.status }}`; colors the header embed.
  - `--webhook URL` — override; defaults to the `DISCORD_DISPATCHER_WEBHOOK`
    environment variable.
  - `--dry-run` — print payloads, do not post.
- **Behavior:**
  - Webhook resolution: `--webhook` else `DISCORD_DISPATCHER_WEBHOOK` env. If
    **unset/empty → skip gracefully** (print a notice to stderr, `return 0`),
    exactly like `notify_discord_ticker.py`. Never fails the workflow over a
    missing webhook.
  - Header embed: title `Dispatcher — <date>` (date omitted if not given);
    color **green `0x2ECC71`** when status is `success`, **red `0xD9342B`**
    otherwise.
  - Body: read `--summary-file`. If present and non-empty → post the header embed
    then the table, `chunk()`-ed to Discord's limit via `discord_common.chunk`,
    `post`-ed via `discord_common.post` with the same 0.6s inter-message spacing
    as the per-ticker poster. If the summary file is **missing or empty** (the
    dispatch step crashed before writing it) → post the header embed + a short
    fallback body: `⚠️ Dispatcher run did not produce a summary (status:
    <status>). See the Actions run logs.`
  - UTF-8 stdout/stderr reconfigure guard (same as `notify_discord_ticker.py`),
    for consistency.

### 2. `scripts/dispatch.py` (one addition)

`main()` currently renders the table and writes it to stdout + `GITHUB_STEP_SUMMARY`.
Add: also write the rendered table to a `--summary-file` (default
`.dispatch-state/summary.md`) so the *separate* notify step can read the exact
same table. Written on both real and dry runs (the file is derived output, not
gate state). Parent dir created if needed (reuse the existing dir-creation
idiom). Existing stdout + step-summary behavior is unchanged.

### 3. `.github/workflows/dispatcher.yml` (new step)

After "Run dispatcher", add:

```yaml
      - name: Notify Discord
        if: always()
        env:
          DISCORD_DISPATCHER_WEBHOOK: ${{ secrets.DISCORD_DISPATCHER_WEBHOOK }}
        run: |
          set -euo pipefail
          python3 scripts/notify_discord_dispatch.py \
            --summary-file .dispatch-state/summary.md \
            --date "$(date -u +%Y-%m-%d)" \
            --status "${{ job.status }}"
```

- `if: always()` → posts every run (heartbeat) **and** even if the dispatch step
  failed (fallback body covers the crash case).
- The "Save gate state" step keeps its own `if: always()`; ordering: Run
  dispatcher → Notify Discord → Save gate state (or Notify after Save — either
  works; place Notify directly after Run dispatcher so the summary file is fresh).
- Header comment in the workflow updated to mention the Discord notification and
  the `DISCORD_DISPATCHER_WEBHOOK` secret.

### 4. Tests — `scripts/tests/test_notify_discord_dispatch.py` (new)

Follows the existing `test_notify_discord_ticker.py` conventions (import the
module, exercise pure helpers, use `--dry-run`/injected paths, no network):

- header embed color: `success` → green, `failure`/other → red.
- title formatting with and without `--date`.
- webhook unset → skips gracefully (`return 0`, no post attempted).
- summary file present → payloads include the table content, chunked.
- summary file missing/empty → fallback body payload is posted.
- `--dry-run` prints payloads and does not post.

### 5. Docs

- **CLAUDE.md** file map: add a bullet for `scripts/notify_discord_dispatch.py`
  next to the `scripts/dispatch.py` / dispatcher entry, noting it posts the
  decision table to a dedicated channel via the `DISCORD_DISPATCHER_WEBHOOK`
  repo secret and skips gracefully when unset.
- **`dispatcher.yml`** header comment: note the Discord heartbeat.
- No change to `.secrets/discord-webhooks.example.json` (per-ticker, unchanged).

## Manual step for the user (out of band)

1. Create a Discord webhook for the target channel (Channel → Integrations →
   Webhooks → New Webhook → Copy URL).
2. Add it as a repo secret:
   `gh secret set DISCORD_DISPATCHER_WEBHOOK` (paste the URL when prompted).

Until the secret exists, the notify step runs and skips gracefully — no failures.

## Data flow

```
cron (weekday 09:30 ET)
  └─ dispatch.py  ──renders table──▶ stdout + GITHUB_STEP_SUMMARY + .dispatch-state/summary.md
        └─ (Notify Discord step, if: always())
              notify_discord_dispatch.py
                ├─ webhook from DISCORD_DISPATCHER_WEBHOOK  (unset → skip, return 0)
                ├─ header embed (green=success / red=failure)  +  chunked table
                └─ POST via discord_common.post  ──▶ dispatcher Discord channel
```

## Risks / edge cases

- **Discord 2000-char limit:** the table can exceed it as the watch-list grows →
  handled by `discord_common.chunk`.
- **Dispatch step hard-crash (e.g. missing `FINNHUB_API_KEY`):** no summary file
  → fallback body posts under `if: always()` with a red embed, so a silent cron
  failure still pings.
- **Secret not yet configured:** graceful skip, workflow stays green.
- **Markdown table in Discord:** Discord does not render Markdown tables as
  tables; it shows the raw pipe-delimited text. Acceptable — it is still
  readable, and matches the "full table" decision. (If we later want prettier
  output, that is a separate formatting change, not in scope here.)
