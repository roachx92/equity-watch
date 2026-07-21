# Discord bot transport — design

**Date:** 2026-07-21
**Status:** approved (pending spec review)
**Branch:** `worktree-discord-bot`

## Problem

Per-ticker Discord posting uses one **webhook URL per channel**. A webhook URL embeds its own auth token, so the whole ticker→URL map is secret. That forces two copies — a gitignored local `.secrets/discord-webhooks.json` and a `DISCORD_WEBHOOKS_JSON` CI secret — with no alarm when they drift. That drift is exactly what caused an AAOI what's-new run to silently not post on 2026-07-21: the CI secret had been rewritten from a copy that diverged from the good local map, and because the post lives inside the (output-hidden) Claude agent step, the failure was invisible.

The class of bug is structural to webhooks, not a one-off. Every ticker added is another row to hand-sync into two stores.

## Goal

Move all Discord posting to a single **bot**, so the only secret is one rarely-changing bot token and the ticker→channel mapping becomes **non-secret, committed, and reviewed** — eliminating the drift class of bug entirely. Make a missing/broken mapping fail **loudly** in CI instead of vanishing.

## Decisions (locked)

| Decision | Choice |
| --- | --- |
| Cutover | **Hard replace** — bot is the only transport; webhook code removed |
| Channel map location | **Single committed JSON file** (`discord-channels.json`) |
| Channel creation | **Bot auto-creates** at onboarding time (not lazily at post time) |
| Dispatcher heartbeat | **Migrates to the bot** too; `DISCORD_DISPATCHER_WEBHOOK` retired |
| `_guild_id` / dispatcher channel | Reserved `_`-prefixed keys in the same `discord-channels.json` |
| Bot permissions | Send Messages + **Manage Channels** (already granted on the server) |

## Architecture

All posting goes through the Discord REST API:

```
POST https://discord.com/api/v10/channels/{channel_id}/messages
Authorization: Bot <DISCORD_BOT_TOKEN>
Content-Type: application/json
{ "content": "..." }  or  { "embeds": [ ... ] }
```

The message payloads (header embed + chunked content), the 1900-char chunking, and the 429 retry/backoff already implemented in `discord_common.py` are preserved. Only the transport changes: resolve a `channel_id` and send with the bot auth header, instead of POSTing a per-channel webhook URL.

### Single secret

- **`DISCORD_BOT_TOKEN`** — repo secret (and local env for ad-hoc runs). The only Discord secret in the system.
- Retired: `DISCORD_WEBHOOKS_JSON`, `DISCORD_DISPATCHER_WEBHOOK`.

### Committed channel map — `discord-channels.json` (repo root, committed)

```json
{
  "_comment": "Committed, non-secret. Channel/guild IDs are not sensitive. Single source of truth for ticker→Discord-channel routing. Onboard a ticker with scripts/onboard_discord_channel.py.",
  "_guild_id": "<guild snowflake>",
  "_dispatcher": "<dispatcher-channel snowflake>",
  "AAOI": "<channel snowflake>",
  "CIFR": "<channel snowflake>"
}
```

- Keys are ticker symbols (normalized upper-case), values are channel-ID snowflakes (strings).
- `_`-prefixed keys are reserved config, skipped by the ticker loader: `_comment` (docs), `_guild_id` (needed for auto-create), `_dispatcher` (heartbeat channel).
- Committed and reviewed in the same PR that onboards a ticker. **No second copy exists, so drift is impossible.**

## Components

### `discord_common.py` (modified)

- Keep `chunk(body, limit=1900)` unchanged.
- Replace `post(webhook_url, payload)` with a bot-transport post:
  - `post(channel_id, payload, token=None)` — token defaults to `os.environ["DISCORD_BOT_TOKEN"]`; POSTs to the channel-messages endpoint with the bot auth header; keeps the existing 429 `Retry-After` loop and the real User-Agent header.
- Add a small `create_channel(guild_id, name, token=None)` helper (POST `/guilds/{guild_id}/channels`, type 0 text) returning the new channel_id — used only by the onboard helper.
- Add `load_channels(path)` / channel-map helpers (normalize keys, skip `_`-prefixed) — or a tiny `channelmap.py` module if it keeps `discord_common` focused. One parser only (mirror the "never grow a second tag parser" rule from `audit_report.py`).

### `notify_discord_ticker.py` (modified)

- Resolve `ticker → channel_id` from committed `discord-channels.json` (default `--config` path points at the committed file, not `.secrets/`).
- Post via `discord_common.post(channel_id, msg)`.
- Embed header (`build_header`), `--kind {whats-new,earnings-digest,audit}`, `--date`, `--tripwire-fired`, `--text-file`, `--dry-run` all unchanged in behavior.
- New `--require-channel` flag: when set (CI uses it), a missing channel_id is a **hard error** (non-zero exit, clear message). Without it (local ad-hoc runs), a missing channel_id still skips gracefully as today.
- Empty-body skip unchanged.

### `notify_discord_dispatch.py` (modified)

- Post the repo-wide roll-up to the `_dispatcher` channel via the bot, read from `discord-channels.json`.
- Keep `--summary-file`, `--date`, `--status`, `--label`, `--dry-run`. Replace the `--webhook`/`DISCORD_DISPATCHER_WEBHOOK` resolution with channel-id resolution (`_dispatcher`, overridable via `--channel`).
- Same graceful skip if `_dispatcher` is absent.

### `scripts/onboard_discord_channel.py` (new)

- `--ticker X [--name "AAOI Oracle"] [--dry-run]`.
- Idempotent:
  1. If `X` already has a channel_id in the map → no-op (report "already mapped").
  2. Else if a guild channel with the target name already exists → adopt its id into the map.
  3. Else create the channel via `create_channel(_guild_id, name)`.
- Naming: `--name` if provided (preserves themed names); otherwise defaults to the ticker symbol (e.g. `aaoi`).
- Writes the resolved channel_id back into `discord-channels.json` (stable key order, `_`-keys preserved), leaving it staged for the human to commit.
- Requires `DISCORD_BOT_TOKEN` and a `_guild_id` in the map.

### Workflows (modified) — `whats-new.yml`, `earnings-digest.yml`, `dispatcher.yml`, `audit.yml`

- Remove the "Materialize Discord webhook config" step and all `DISCORD_WEBHOOKS_JSON` / `DISCORD_DISPATCHER_WEBHOOK` env wiring. Add `DISCORD_BOT_TOKEN` where a poster runs.
- **Move the per-ticker Discord post out of the Claude agent prompt into a deterministic post-agent workflow step** (`whats-new.yml`, `earnings-digest.yml`): after the agent step, a step reads `whats-new-digest.md` / the digest file and runs `notify_discord_ticker.py --require-channel …`. The agent no longer runs the poster; the prompt drops that instruction. This makes the post's success/failure **visible in the job log** — the fix for the original bug's invisibility.
- `dispatcher.yml` / `audit.yml`: their existing `notify_discord_dispatch.py` / `notify_discord_ticker.py --kind audit` steps keep their structure, just repointed to the bot token + committed map.

### Cleanup (hard replace)

- Delete `.secrets/discord-webhooks.json` and `.secrets/discord-webhooks.example.json`.
- Remove every webhook-URL code path from the two posters and `discord_common`.
- Update `CLAUDE.md` file-map entries for `notify_discord_ticker.py`, `notify_discord_dispatch.py`, `discord_common.py`, `dispatch.py` to describe the bot model and the committed map; add the onboard helper.
- Update `docs/part-2-scripts-plan.md` references. Leave the historical `docs/superpowers/specs/2026-07-18-dispatcher-discord-notification-design.md` as-is (dated record).

## Data flow

**Onboard (human, once per ticker):**
`onboard_discord_channel.py --ticker COHR --name "Coherent Wizard"` → bot creates/adopts channel → writes id to `discord-channels.json` → human commits it in the ticker's onboarding PR.

**Post (CI, every run):**
agent writes digest file → deterministic workflow step runs `notify_discord_ticker.py --ticker T --require-channel --text-file …` → resolve id from committed map → bot posts → success/failure logged in the job.

## Error handling

- Missing `DISCORD_BOT_TOKEN`: poster errors clearly (CI) / skips with a message (local, no token) — mirrors current graceful-skip ethos but never silent in CI.
- Missing channel_id for a ticker: `--require-channel` → hard fail in CI; graceful skip locally.
- Non-429 HTTP error from Discord (e.g. 404 dead channel, 403 perms): raised, non-zero exit, surfaced by the deterministic step.
- 429: existing `Retry-After` backoff, up to 5 attempts.

## Security note

A bot token is broader than a post-only webhook: with Manage Channels it can create/edit channels across the guild. Accepted for this single-owner server (permission already granted). The token is the one secret to protect; the committed map carries no secrets.

## Testing (TDD, keep 161 baseline green)

- Rewrite `test_notify_discord_ticker.py`: mock the HTTP transport; assert channel resolution from a fixture map, embed header/title per `--kind`, chunking, `--require-channel` hard-fail vs graceful skip, empty-body skip.
- Rewrite `test_notify_discord_dispatch.py`: `_dispatcher` resolution, roll-up post, graceful skip when absent.
- New `test_onboard_discord_channel.py`: idempotency (already-mapped no-op, name-adopt, create-and-write-back), key-order/`_`-key preservation on write, dry-run.
- New coverage in a `discord_common` test for the bot `post` (auth header, endpoint, 429 loop) and `create_channel`.

## Out of scope

- Slash commands / interactive bot behavior. This bot is post-only + channel creation.
- Migrating historical webhook posts. Cutover is forward-only.
- Retro-theming existing channel names.
