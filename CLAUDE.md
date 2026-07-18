# CLAUDE.md — equity-watch

## What this is
A monitoring repo for on-demand, per-ticker equity research. Three workflows run against a watched ticker — a **what's-new** news scan, an **earnings-digest** call breakdown, and a full **deep-dive** — each dispatching research sub-agents, assessing findings against that ticker's pre-committed **Edge** and **Tripwires**, and committing dated entries to its `news.md`. The repo holds the lightweight monitoring state **and** the full deep-dive reports (markdown under `tickers/<TICKER>/reports/<YYYY-MM-DD>.md`); the repo is published as a MkDocs Material GitHub Pages site.

## Canonical-source rule
- This repo is the **master** for the research framework. Apply the framework files as written — **never restate the rules from memory**.
- Deep-dive reports are **markdown in this repo** (`tickers/<TICKER>/reports/<YYYY-MM-DD>.md`), applying the framework; they are published via GitHub Pages (see `docs/part-2-scripts-plan.md`). No `.docx`, no external sync.

## File map
- `framework/standing-rules.md` — Sections A + E. Standing rules and honest limits; apply to EVERY response.
- `framework/latest-updates-workflow.md` — Section F. The "what's new" analytical procedure (with §18 Tripwire/Edge assessment), **plus §F.1 — the canonical `## Recent News Log` entry format, single source of truth for how a news item gets stored in a ticker's news.md.**
- `framework/deep-dive-template.md` — Sections B0, B, C, D, G, H. The full-diligence report standard + the four mandatory sub-agent prompt templates.
- `framework/news-check.md` — the canonical spec for the "what's new" workflow: §A the agentic parallel-sub-agent research method (+ source-quality & first-run window), §B the run-summary chat-digest format.
- `framework/earnings-digest.md` — Section I. The earnings-call debrief procedure: three parallel sub-agents over the 8-K/EX-99.1, 10-Q, deck and call Q&A → a retail-readable breakdown (numbers · cash conversion · management's sector read cross-checked against peers · what was *dropped* from disclosure · the reaction decomposed from the sector tape) + assessment against thesis / re-rate drivers / risks / Edge + Tripwires + what to watch next. Output goes to `tickers/<TICKER>/earnings-debrief.md`; the call's discrete news items still go to the ticker's news.md per §F.1.

**News-check spec split — one home each, referenced never restated:** **research it** → `news-check.md` §A · **report it** (chat digest) → `news-check.md` §B · **store it** (log entry in the ticker's news.md) → `latest-updates-workflow.md` §F.1. The what's-new workflow applies all three.
- `tickers/<TICKER>/earnings-debrief.md` — per-ticker **earnings debrief log**: one prepended section per quarter (most recent first), written by `framework/earnings-digest.md`. Quarters are never overwritten — the accumulated history is how management's story is tracked across calls. **One deliberate exception:** the standing `## Guidance track record` table at the top is updated in place (row added when a guide is issued, outcome filled when that period reports) and is the prospective evidence base for the next deep-dive's §13 management assessment. Optional per ticker; absent until the first digest runs.
- `tickers/<TICKER>/news.md` — **the ticker's news.md**: per-ticker state (YAML front matter for the homepage grid, Canonical deep-dive link, thesis context, Edge, numbered Tripwires, Recent News Log). **The directory is the watch-list** — one **folder** per watched ticker, folder name = symbol; adding a ticker is "drop in a folder with a news.md," and there is no separate roster to update. A folder is the unit; the news.md is its state. The per-ticker folder exists so future per-ticker artifacts have a home without disturbing the watch-list glob.
- `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` — the ticker's **deep-dive report snapshots**, one dated file per full-framework run, written by `framework/deep-dive-template.md`. **Immutable once published** — never overwrite a prior date; a re-run drops a new dated file alongside. The newest date is the canonical deep-dive; the homepage grid resolves it automatically (`web/hooks/coverage.py`). Absent until the first deep-dive runs.
  **Resolving "the" report — always by glob, never by trust.** Any workflow that needs a ticker's deep-dive (deep-dive Step 4 seeding/refreshing news.md, whats-new/earnings-digest Step "confirm the ticker is covered," or any ad-hoc question about a ticker's report) globs `tickers/<TICKER>/reports/*.md`, sorts by date, and uses the newest — it does **not** assume the news.md `**Canonical deep-dive:**` line is current, since that line is a written pointer someone set at a point in time and can go stale (a later re-run, a manual edit, a race between sessions). If the glob's newest date disagrees with what the link says, that's real drift: use the glob result and refresh the link to match as part of the current run, don't silently propagate the stale one. This applies every time, not just right after a fresh deep-dive.
- `scripts/notify_discord_ticker.py` — the per-ticker Discord poster,
  run locally by both the `whats-new` and `earnings-digest` skills at the end of every
  `/whats-new <TICKER>` or `/earnings-digest <TICKER>` run (not push-triggered — an
  ad-hoc check isn't committed/pushed every time). Shares its chunking/POST logic with
  `scripts/discord_common.py`. **Both run types post to the same
  per-ticker channel**, so `--kind whats-new|earnings-digest` is mandatory and titles
  the embed `<TICKER> — What's New (<date>)` or `<TICKER> — Earnings Digest (<date>)`
  so the two are distinguishable in the Discord feed. Looks up the ticker in
  `.secrets/discord-webhooks.json` (local, gitignored — see
  `.secrets/discord-webhooks.example.json` for the template) and posts the chat digest
  to that ticker's channel; **skips gracefully, no error, if the ticker has no webhook
  configured.**
- `scripts/dispatch.py` + `.github/workflows/dispatcher.yml` — the **deterministic dispatcher**: a scheduled (weekday-morning cron), Claude-free Python pre-filter that decides which watched tickers warrant a paid run and fires the existing `earnings-digest.yml` / `whats-new.yml` via `gh workflow run`. **Earnings** dispatch the morning after a Finnhub earnings-calendar report, deduped by reading `tickers/<T>/earnings-debrief.md` (so a state loss can never double-digest a quarter); the two foreign names (IBIDY, LPKF) fall through to manual dispatch. **What's-new** dispatch on a keyword-filtered Finnhub company-news gate with a 48h per-ticker rate cap; the gate's only state (`last_news_scan` per ticker) lives in the **Actions cache**, never committed to `main`. Requires a `FINNHUB_API_KEY` repo secret (free tier). Every run writes a per-ticker dispatch/skip table to the Actions job summary.
- `docs/part-2-scripts-plan.md` — planned migration of deterministic tasks to scripts.
- `web/` — **all site build machinery in one place**: `mkdocs.yml`, the homepage `index.md`, `requirements.txt` (mkdocs deps), `overrides/` (theme templates), `stylesheets/`, `hooks/coverage.py` (build-time coverage-grid generator), and `scripts/build.sh` + `scripts/serve.sh`. The site's *content* is the research master at the repo root (`framework/`, `tickers/`); the build assembles it into `web/site_src/` and emits `web/site/` (both gitignored). Published to GitHub Pages by `.github/workflows/pages.yml`.

## Section → file lookup
| Section | Lives in |
| --- | --- |
| A — Standing rules | `framework/standing-rules.md` |
| B0 — Output architecture (non-negotiable) | `framework/deep-dive-template.md` |
| B — Full deep-dive template (18 sections) | `framework/deep-dive-template.md` |
| C — Catalyst / milestone tracking | `framework/deep-dive-template.md` |
| D — Re-rate mapping methodology | `framework/deep-dive-template.md` |
| E — Honest limits | `framework/standing-rules.md` |
| F — "Latest Updates" workflow | `framework/latest-updates-workflow.md` |
| G — Competitive-moat depth standard | `framework/deep-dive-template.md` |
| H — Filing/counterparty/sector templates | `framework/deep-dive-template.md` |
| I — Earnings digest workflow | `framework/earnings-digest.md` |

## Layering
Standing rules (always) → latest-updates workflow (the method) → `tickers/<TICKER>/news.md` (state).

## Three entry points
- **What's new** ("what's new on TICKER", "latest on TICKER"): use `framework/latest-updates-workflow.md` (Section F) with `framework/news-check.md`, under `framework/standing-rules.md`. The bounded, per-ticker news scan — appends to the ticker's Recent News Log and emits the §B digest.
- **Full deep-dive** ("run the framework on TICKER"): use `framework/deep-dive-template.md` with all four sub-agent templates, under `framework/standing-rules.md`. **Start from `framework/report-template.md`, apply §B0 (output architecture — non-negotiable), and run the orchestrator plus all four sub-agents on Opus.** Do not use a previously published report as the quality precedent — build against §B0 directly; the July 2026 audit found the whole corpus below the bar.
- **Earnings digest** ("earnings digest on TICKER", "break down TICKER's call"): use `framework/earnings-digest.md` (Section I), under `framework/standing-rules.md`. Presupposes a deep-dive and the ticker's Edge/Tripwires already exist — if they don't, build the report first. Three sub-agents, Opus-pinned. Writes the quarter's analysis to `tickers/<TICKER>/earnings-debrief.md` **and** the call's discrete news items to the ticker's news.md per §F.1.

## Git workflow — every worktree, every session
- **Never commit or push directly to `main`.** Work on a feature branch (any name; this repo's convention is `work/<date>-<slug>` or `<topic>`, e.g. `work/2026-07-16-earnings-digest`).
- **Commit freely as work progresses, but do NOT push or open a PR on every increment.** Pushing to the remote and opening a PR happen **only when the user explicitly asks** ("push", "open a PR", "push a PR"). Batch incremental edits locally until then — don't auto-PR each change.
- **When the user does ask to push/PR:** if the branch already has an open PR, push the new commits to the **same branch** (they land in that PR — don't open a duplicate). If that branch's PR was already merged (history diverged, common after a squash-merge), **rebase the branch onto `main` first**, then open a fresh PR.
- **Never merge a PR unless the user explicitly asks.** Even after pushing/opening a PR at the user's request, merging is a separate, explicit ask every time — the PR is the seam where the user reviews on GitHub before it lands in `main`.

_Not financial advice — informational research tooling only._
