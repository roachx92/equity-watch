# Discord notification for the daily watch — design

_Status: approved for planning · 2026-07-15_

## Purpose

The daily "What's New" equity watch already ends each run by producing a **run
summary** — the `framework/news-check.md` §B chat digest (🚨 tripwires first,
then edge shifts, then per-ticker headline+digest items, then a conditional
Edge/Tripwire recap). Today that digest exists only as ephemeral output of the
routine session: nobody sees it unless they open the routine's chat.

This project makes that digest land reliably in a **Discord channel** every run.
The digest content is already written each day; the work is (a) persisting it to
a file and (b) delivering it to Discord as deterministic plumbing.

Non-goal: changing what the digest *says*. `news-check.md` §B remains the single
source of the digest format; this project persists and delivers it, it does not
restate or reformat it.

## Design decisions (locked)

1. **Content sent:** the **full** §B daily digest, every run.
2. **Delivery path:** the agent **materializes** the digest to a tracked file,
   commits it; a **GitHub Action** fires on push and posts to Discord. Delivery
   runs *outside* the LLM session, so a flaky session can't silently drop the
   post.
3. **Length handling:** the full digest often exceeds Discord's 2000-char
   message limit, so the poster **chunks** the body into ≤~1900-char messages on
   item/line boundaries, preceded by a colored **header embed**.
4. **Heartbeat:** **every weekday posts**, even a "nothing material" day, so
   silence is never ambiguous (a silent day would otherwise mean *either*
   nothing happened *or* the routine broke). A summary file is written every run.
5. **Credential:** the webhook URL is a GitHub Actions **secret**
   (`DISCORD_WEBHOOK_URL`), not a variable — it is a write credential.
6. **"Full run →" link target:** the committed summary file on github.com (zero
   site changes). Site-publish of `summaries/` is an explicit out-of-scope
   follow-on.

## Architecture

```
routine run  (LLM: research + assessment)
  └─ writes summaries/YYYY-MM-DD.md      ← frontmatter + verbatim §B digest body
  └─ git commit + push                    ← summary file + any ticker changes, one commit
        └─ .github/workflows/notify-discord.yml   (trigger: push, paths: summaries/**)
              └─ scripts/notify-discord.py         (plumbing: parse → embed → chunk → POST)
                    └─ Discord webhook  →  #channel
```

The split is the `docs/part-2-scripts-plan.md` dividing line: **the LLM produces
the digest (assessment); the script + Action deliver it (plumbing).**

## Components

### 1. Summary file — `summaries/YYYY-MM-DD.md`

Written by the routine agent as a step in `daily-watch.md`. Lightweight YAML
frontmatter (the deterministic contract the poster reads) followed by the
verbatim §B digest body:

```markdown
---
date: 2026-07-15
tickers_checked: 5
tripwires_fired: 1      # count of [TRIPWIRE] hits this run
edge_shifts: 2          # count of EDGE+/EDGE− items this run
---
🚨 TRIPWIRES
• **CIFR Tripwire #2 — early-warning.** Hashprice ↓18% WoW → margin test…

EDGE SHIFTS
• **AAOI — EDGE+.** 800G design win at a hyperscaler (2026-07-15).

PER-TICKER
2026-07-15 — [CATALYST] — **AAOI 800G win**. One-sentence digest → impact.
…

RECAP
CIFR: Edge & Tripwires — <condensed recap, since it had a hit>.
AAOI: unchanged — Edge and Tripwires as before.
```

- The frontmatter drives the header embed deterministically (color + counts
  line), so the poster never parses prose to learn whether a tripwire fired.
- The body is the §B digest **exactly as produced** — no reformatting.
- On a "nothing material" day the body still carries the §B "nothing material"
  content and `tripwires_fired: 0`, `edge_shifts: 0`; the file is still written
  (heartbeat).

**Field semantics.** `tripwires_fired` = count of `[TRIPWIRE]` hits across all
tickers this run; `edge_shifts` = count of `[EDGE+]`/`[EDGE−]` items;
`tickers_checked` = number of `tickers/*.md` scanned this run.

### 2. `daily-watch.md` — one new step

After "produce the run summary" (current step 7), add a step:

> Write that same run-summary digest to `summaries/<today>.md`, prefixed with the
> frontmatter block (`date`, `tickers_checked`, `tripwires_fired`,
> `edge_shifts`), and include the file in the commit. The digest format is the
> canonical §B format in `framework/news-check.md` — do not restate it here; the
> summary file body IS that digest.

Consequences:
- The commit step (current step 6) becomes **always-commits**, because a new
  summary file exists every run. The prior "commit only if a ticker changed"
  behavior is superseded — this is the intended daily heartbeat.
- `news-check.md` §B is untouched (still the format's single source). A one-line
  pointer may be added there noting the digest is also persisted to
  `summaries/<date>.md`, but the format definition stays there and only there.

### 3. `.github/workflows/notify-discord.yml`

- Trigger: `on: push` with `branches: [main]` and `paths: ['summaries/**']` — a
  push touching only framework/ticker/docs files does not fire.
- Guard against double-posting: act only on summary files **added** in this push,
  computed via `git diff --name-only --diff-filter=A <before>..<after>` (scoped
  to `summaries/`). Re-pushes or edits of an existing summary do not re-notify.
  Handle the first-push all-zeros `before` SHA by falling back to `HEAD^` (or,
  if unavailable, the single latest `summaries/*.md`).
- `permissions: contents: read`.
- Passes `secrets.DISCORD_WEBHOOK_URL` to the poster via env.
- Builds the "Full run →" link with
  `${{ github.server_url }}/${{ github.repository }}/blob/${{ github.sha }}/summaries/<date>.md`
  (no hardcoded org/repo).

### 4. `scripts/notify-discord.py` — the poster

Python (not shell) for clean JSON assembly and chunking, consistent with the
existing `hooks/coverage.py`. Locally runnable and unit-testable.

Interface:
```
notify-discord.py <summary-file> [--file-url URL] [--dry-run]
env: DISCORD_WEBHOOK_URL   (required unless --dry-run)
```

Behavior:
1. Parse frontmatter (`date`, `tickers_checked`, `tripwires_fired`,
   `edge_shifts`) and split off the digest body.
2. Build a **header embed**: title `Daily Watch — <date>`; color **red
   (0xD9342B) if `tripwires_fired > 0`, else green (0x2ECC71)**; description = a
   counts line (`N tripwires · M edge shifts · K checked`) plus a masked
   `[Full run →](<file-url>)` link.
3. **Chunk** the body into ≤~1900-char segments split on line boundaries (never
   mid-line; prefer splitting between digest items). Preserve order.
4. POST the header embed first, then each body chunk as a plain-content message,
   in order. Sleep briefly between posts; on HTTP 429 respect `retry_after` and
   retry. Fail loudly (non-zero exit) if any post errors, so the Action surfaces
   it.
5. `--dry-run`: print each payload to stdout and post nothing (used by CI and
   local checks).

**Formatting note.** The §B digest body contains bold (`**…**`) and bullets,
which render in Discord plain-content messages; it does **not** contain masked
`[text](url)` source links (sources live in the ticker files, not the digest),
so no links are lost in the chunked body. Masked links are used only in the
header embed description, where Discord renders them.

### 5. One-time manual setup (already done)

1. Discord: channel → Integrations → Webhooks → New Webhook → copy URL.
2. GitHub: repo → Settings → Secrets and variables → Actions → **Secrets** tab →
   `DISCORD_WEBHOOK_URL`.

## Testing

- **Chunker (TDD):** pure function `chunk(body, limit) -> list[str]`. Unit-test
  first: never exceeds limit, never splits mid-line, reassembles to the original,
  handles a body already under the limit (1 chunk) and an empty body.
- **Header embed:** unit-test color selection (red when `tripwires_fired>0`, green
  otherwise) and the counts line from frontmatter fixtures.
- **Integration:** run `notify-discord.py summaries/2026-07-14.md` against a
  **throwaway test webhook** (a real past digest as fixture) and confirm the
  header + chunks land correctly in a test channel.
- **CI smoke:** a `--dry-run` invocation over a committed fixture summary asserts
  the script builds valid payloads without a live webhook.

## Documentation updates

- `daily-watch.md` — the new write-summary step (§2 above).
- `CLAUDE.md` — file map: add `summaries/` and the notify-discord flow; add
  `scripts/notify-discord.py` and `.github/workflows/notify-discord.yml`.
- `docs/part-2-scripts-plan.md` — record Discord notify as a completed
  deterministic-plumbing item.
- Optionally a one-line pointer in `news-check.md` §B noting the digest is
  persisted to `summaries/<date>.md` (format stays canonical there).

## Out of scope (optional follow-ons)

- Publishing `summaries/` to the MkDocs site as a "Run Log" section (would make
  the "Full run →" link a rendered page instead of the raw GitHub file).
- Role-ping / `@mention` on tripwire days.
- A "latest summary per channel" digest-of-digests or weekly roll-up.

## Open risks

- **Discord rate limits** on a very heavy day (many chunks): mitigated by
  inter-post sleep + 429 `retry_after` handling.
- **Frontmatter drift:** if the agent omits or mis-counts a frontmatter field,
  the header embed degrades (wrong color/counts) but the body still posts. The
  poster should default missing counts to `0` and a missing `date` to the
  filename stem rather than crashing.
```
