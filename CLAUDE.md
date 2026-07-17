# CLAUDE.md — equity-watch

## What this is
A live monitoring repo for a daily "What's New" equity watch. A Claude Code Remote Routine runs each weekday, reads `daily-watch.md`, dispatches one research sub-agent per ticker, assesses findings against each ticker's pre-committed **Edge** and **Tripwires**, and commits dated entries to each ticker's `news.md`. The repo holds the lightweight monitoring state **and** the full deep-dive reports (markdown under `tickers/<TICKER>/reports/<YYYY-MM-DD>.md`); the repo is published as a MkDocs Material GitHub Pages site.

## Canonical-source rule
- This repo is the **master** for the research framework. Apply the framework files as written — **never restate the rules from memory**.
- Deep-dive reports are **markdown in this repo** (`tickers/<TICKER>/reports/<YYYY-MM-DD>.md`), applying the framework; they are published via GitHub Pages (see `docs/part-2-scripts-plan.md`). No `.docx`, no external sync.

## File map
- `framework/standing-rules.md` — Sections A + E. Standing rules and honest limits; apply to EVERY response.
- `framework/latest-updates-workflow.md` — Section F. The "what's new" analytical procedure (with §18 Tripwire/Edge assessment), **plus §F.1 — the canonical `## Recent News Log` entry format, single source of truth for how a news item gets stored in a ticker's news.md.**
- `framework/deep-dive-template.md` — Sections B0, B, C, D, G, H. The full-diligence report standard + the four mandatory sub-agent prompt templates.
- `framework/news-check.md` — the canonical spec shared by the daily watch and the "what's new" workflow: §A the agentic parallel-sub-agent research method (+ source-quality & first-run window), §B the run-summary chat-digest format.
- `framework/earnings-digest.md` — Section I. The earnings-call debrief procedure: three parallel sub-agents over the 8-K/EX-99.1, 10-Q, deck and call Q&A → a retail-readable breakdown (numbers · cash conversion · management's sector read cross-checked against peers · what was *dropped* from disclosure · the reaction decomposed from the sector tape) + assessment against thesis / re-rate drivers / risks / Edge + Tripwires + what to watch next. Output goes to `tickers/<TICKER>/earnings-debrief.md`; the call's discrete news items still go to the ticker's news.md per §F.1.

**News-check spec split — one home each, referenced never restated:** **research it** → `news-check.md` §A · **report it** (chat digest) → `news-check.md` §B · **store it** (log entry in the ticker's news.md) → `latest-updates-workflow.md` §F.1. Both entry points (daily watch and ad-hoc) apply all three identically.
- `daily-watch.md` — the operational procedure the routine runs (applies Sections A + F to this repo's layout).
- `tickers/<TICKER>/earnings-debrief.md` — per-ticker **earnings debrief log**: one prepended section per quarter (most recent first), written by `framework/earnings-digest.md`. Quarters are never overwritten — the accumulated history is how management's story is tracked across calls. **One deliberate exception:** the standing `## Guidance track record` table at the top is updated in place (row added when a guide is issued, outcome filled when that period reports) and is the prospective evidence base for the next deep-dive's §13 management assessment. Optional per ticker; absent until the first digest runs.
- `tickers/<TICKER>/news.md` — **the ticker's news.md**: per-ticker state (YAML front matter for the homepage grid, Canonical deep-dive link, thesis context, Edge, numbered Tripwires, Recent News Log). **The directory is the watch-list** — one **folder** per watched ticker, folder name = symbol; adding a ticker is "drop in a folder with a news.md," and there is no separate roster to update. A folder is the unit; the news.md is its state. The per-ticker folder exists so future per-ticker artifacts have a home without disturbing the watch-list glob.
- `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` — the ticker's **deep-dive report snapshots**, one dated file per full-framework run, written by `framework/deep-dive-template.md`. **Immutable once published** — never overwrite a prior date; a re-run drops a new dated file alongside. The newest date is the canonical deep-dive the news.md links; the homepage grid resolves it automatically (`hooks/coverage.py`). Absent until the first deep-dive runs.
- `summaries/<YYYY-MM-DD>.md` — per-run persisted copy of the §B run-summary
  digest (frontmatter counts + digest body), written by `daily-watch.md` each
  run. Consumed by the Discord notification Action; also the daily heartbeat.
- `scripts/notify_discord.py` — dependency-free poster: parses a summary file,
  builds a colored header embed, chunks the body under Discord's limit, POSTs to
  the `DISCORD_WEBHOOK_URL` webhook. Locally runnable with `--dry-run`.
- `.github/workflows/notify-discord.yml` — on push to `summaries/**`, posts each
  newly added summary to Discord via the poster.
- `docs/part-2-scripts-plan.md` — planned migration of deterministic tasks to scripts.

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
Standing rules (always) → latest-updates workflow (the method) → `daily-watch.md` (launcher/ops) → `tickers/<TICKER>/news.md` (state).

## Three entry points
- **Daily watch:** the routine reads `daily-watch.md`. Uses Sections A + F only.
- **Full deep-dive** ("run the framework on TICKER"): use `framework/deep-dive-template.md` with all four sub-agent templates, under `framework/standing-rules.md`. **Start from `framework/report-template.md`, apply §B0 (output architecture — non-negotiable), and run the orchestrator plus all four sub-agents on Opus.** Do not use a previously published report as the quality precedent — build against §B0 directly; the July 2026 audit found the whole corpus below the bar.
- **Earnings digest** ("earnings digest on TICKER", "break down TICKER's call"): use `framework/earnings-digest.md` (Section I), under `framework/standing-rules.md`. Presupposes a deep-dive and the ticker's Edge/Tripwires already exist — if they don't, build the report first. Three sub-agents, Opus-pinned. Writes the quarter's analysis to `tickers/<TICKER>/earnings-debrief.md` **and** the call's discrete news items to the ticker's news.md per §F.1.

## Git workflow — every worktree, every session
- **Never commit or push directly to `main`.** Work on a feature branch (any name; this repo's convention is `work/<date>-<slug>` or `<topic>`, e.g. `work/2026-07-16-earnings-digest`).
- **Commit freely as work progresses, but do NOT push or open a PR on every increment.** Pushing to the remote and opening a PR happen **only when the user explicitly asks** ("push", "open a PR", "push a PR"). Batch incremental edits locally until then — don't auto-PR each change.
- **When the user does ask to push/PR:** if the branch already has an open PR, push the new commits to the **same branch** (they land in that PR — don't open a duplicate). If that branch's PR was already merged (history diverged, common after a squash-merge), **rebase the branch onto `main` first**, then open a fresh PR.
- **Never merge a PR unless the user explicitly asks.** Even after pushing/opening a PR at the user's request, merging is a separate, explicit ask every time — the PR is the seam where the user reviews on GitHub before it lands in `main`.

_Not financial advice — informational research tooling only._
