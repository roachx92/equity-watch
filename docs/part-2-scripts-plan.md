# Part 2 — deterministic tasks → scripts (backlog)

Part 1 reorganized the markdown. Part 2 moves the remaining **deterministic** work out of prompts and into scripts, so the LLM is left to do research and assessment. **As of 2026-07-18 the Part 2 backlog is built** (items 1 follow-on, 3, 4) — see each item below and `.github/workflows/lint.yml`. Items 5 and 7 (git-commit plumbing, summary-count stamper) were **dropped** when the scheduled daily-watch/summaries pipeline was retired (PR #29). Part 3 (deferred efficiency backlog) is captured at the bottom, not built.

**Dividing line:** scripts do plumbing, validation, and sync; the LLM does research and assessment.

## Backlog

1. **Deep-dive reports → markdown-in-git, published via GitHub Pages.** *(Was: `.docx` → Google Drive sync — dropped.)* Reports live as `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` (git is the source of truth) and the repo is published as a MkDocs Material site with a bespoke "Research Desk" homepage. No `.docx`, no Drive, no external auth. **Follow-on — DONE.** `scripts/resolve_report.py` resolves each ticker's newest report by glob-and-max (shared logic in `scripts/tickerlib.py`, cross-checked against `web/hooks/coverage.py`): `--check` fails CI on a stale `**Canonical deep-dive:**` pointer, `--fix` rewrites only the pointer link (never surrounding prose) so it self-heals. Runs in CI (`.github/workflows/lint.yml`) and on demand.

2. **Ticker enumeration. — DONE.** The watch-list is derived from a `tickers/*/` folder glob (each holding a `news.md`): the per-ticker workflows and the site build enumerate the directory; the hardcoded name-lists and "four sub-agents" counts are gone, and CLAUDE.md/README point at the directory as the source of truth. Adding a ticker is now "drop in a folder with a news.md." *(Kept as a prose instruction to the agent — no script needed, since a workflow just runs `ls tickers/`.)*

3. **Log-entry format validation. — DONE.** `scripts/lint_news_log.py` validates each Recent News Log entry against the invariants of `framework/latest-updates-workflow.md` §F.1 (the authority — the linter references it, does not encode a second copy) and also fails if the literal format skeleton is restated outside §F.1. **Hard-fails** (CI) on the structural invariants: date/range lead, ≥1 `[FRAMEWORK-TAG]`, bold `**Headline**`, the `→` implication clause. The "≥1 linked source" rule is a **non-blocking warning** for now — the legacy corpus predates link enforcement (20 bare-source entries across AAOI/WYFI/IBIDY/LPKF); promote it to a hard fail after a cleanup pass links them.

4. **Ticker news.md structure lint. — DONE.** `scripts/lint_news_structure.py` asserts each `tickers/*/news.md` has the required sections (Thesis context, Edge, Tripwires, Recent News Log) and the front-matter `company`/`blurb` the coverage grid depends on, **and** fails on any `tickers/*/` folder with no `news.md` (a half-created ticker that both the per-ticker workflows and `web/hooks/coverage.py` skip silently). CI gate via `.github/workflows/lint.yml`.

5. **Git commit/push plumbing. — DROPPED.** *(Was: `scripts/commit_watch.py` staging `tickers/*/news.md` + `summaries/<date>.md` and committing `daily watch: <date>`.)* Superseded when the scheduled daily-watch/summaries pipeline was retired (PR #29): git is now owned per-ticker by the `whats-new`/`earnings-digest` GitHub Actions workflows (commit on a feature branch → PR → squash-merge), so a standalone commit script has no caller.

7. **Summary-count stamper. — DROPPED.** *(Was: `scripts/summarize_counts.py` stamping `tickers_checked`/`tripwires_fired`/`edge_shifts` onto `summaries/<date>.md`.)* Superseded with the `summaries/<date>.md` run-digest itself when the all-ticker daily watch was retired (PR #29); the per-ticker digest carries no aggregate count block.

6. **Discord notification of the per-ticker digest. — DONE.** At the end of a
   `whats-new.yml` or `earnings-digest.yml` run, `scripts/notify_discord_ticker.py`
   posts the §B chat digest (colored header embed + chunked body) to that ticker's
   Discord channel, resolved from the committed `discord-channels.json` map
   (`scripts/channelmap.py`) and posted via the Discord bot (single `DISCORD_BOT_TOKEN`
   repo secret — no more per-channel webhooks). Runs as a deterministic workflow step,
   not inside the Claude agent prompt — the dividing-line pattern in action.

*(Superseded, July 2026 — dropped: the scheduled all-ticker daily watch and its
`summaries/<date>.md` → push-triggered Discord pipeline. The pipeline is now per-ticker,
on-demand only; item 6 above reflects the surviving per-ticker poster.)*

## Part 3 — deferred efficiency backlog

Surfaced by the 2026-07-18 pipeline-efficiency review. **Not built** — captured here so
they aren't lost. Bucket 1 (scripts/determinism) is the work above; these are the rest.

### 3a. DRY the docs & code
The dividing-line refactor cut *awk/sync*, but the launchers still restate shared rules,
and the scripts duplicate helpers. Consolidating reduces drift and per-run context load.
- **Prose restated across files:** glob-newest-report rule (6×: `CLAUDE.md`, `latest-updates-workflow.md`, `earnings-digest.md`, and the whats-new/earnings/deep-dive SKILLs); "sub-agents research only, don't edit files" (5×); "confirm covered else build the deep-dive first" (4×); "read news.md, quote Edge/Tripwires verbatim" (4×); the date-setup Step 0 (4×); the Discord Step 6 block near-verbatim in the whats-new and earnings-digest SKILLs. Candidate: a single referenced block per rule, launchers link not restate.
- **Code duplicated:** two front-matter parsers (`web/hooks/coverage.py` PyYAML vs the new stdlib `tickerlib.front_matter`); `web/scripts/build.sh` and `serve.sh` duplicate the site-assembly block; `coverage._latest_report` vs `tickerlib.latest_report_date` (a cross-check test guards them — unify once safe to import across the `scripts/` ↔ `web/hooks/` boundary).

### 3b. Runtime token/$ cost
Highest raw savings, highest risk — touches the framework's deliberate quality mandate.
- **Opus pinned on every node** of deep-dive (orchestrator + 4 sub-agents) and earnings (3), including mechanical sub-tasks — no lighter tier. The framework is emphatic that a weaker model degrades synthesis invisibly, so any tiering must be scoped to demonstrably-mechanical sub-tasks only, and measured.
- **whats-new re-runs the full research pass** with no same-day dedup: back-to-back whats-new runs on the same ticker each re-glob, re-read news.md, re-derive the hunt-list, and dispatch a fresh 6–10-search pass over the same window. Candidate: a same-day short-circuit keyed off the last log entry's timestamp.
- **No cross-run source cache** — every run re-fetches primary sources; the only memory is the append-only log.

### 3c. Human toil
- Collapse the store→notify tail of an ad-hoc run into one command (the whats-new / earnings-digest SKILLs currently hand-invoke `notify_discord_ticker.py` as a separate step after writing the log; the write and the poster could be one wrapper).

## Already captured in Part 1 (for the record)
- `awk` section-extraction — **eliminated** by splitting the framework into purpose-scoped files.
- `cp`/`diff` framework sync — **eliminated** by making this repo canonical.
