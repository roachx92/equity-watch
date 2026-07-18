# Part 2 — deterministic tasks → scripts (backlog)

Part 1 reorganized the markdown. Part 2 moves the remaining **deterministic** work out of prompts and into scripts, so the LLM is left to do research and assessment. **As of 2026-07-18 the Part 2 backlog is built** (items 1 follow-on, 3, 4, 5, plus a net-new count-stamper) — see each item below and `.github/workflows/lint.yml`. Part 3 (deferred efficiency backlog) is captured at the bottom, not built.

**Dividing line:** scripts do plumbing, validation, and sync; the LLM does research and assessment.

## Backlog

1. **Deep-dive reports → markdown-in-git, published via GitHub Pages.** *(Was: `.docx` → Google Drive sync — dropped.)* Reports live as `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` (git is the source of truth) and the repo is published as a MkDocs Material site with a bespoke "Research Desk" homepage. No `.docx`, no Drive, no external auth. **Follow-on — DONE.** `scripts/resolve_report.py` resolves each ticker's newest report by glob-and-max (shared logic in `scripts/tickerlib.py`, cross-checked against `web/hooks/coverage.py`): `--check` fails CI on a stale `**Canonical deep-dive:**` pointer, `--fix` rewrites only the pointer link (never surrounding prose) so it self-heals. Wired into `daily-watch.md` step 7b.

2. **Ticker enumeration. — DONE.** The watch-list is derived from a `tickers/*/` folder glob (each holding a `news.md`): `daily-watch.md` enumerates the directory at run start and dispatches one sub-agent per ticker folder found; the hardcoded name-lists and "four sub-agents" counts are gone, and CLAUDE.md/README point at the directory as the source of truth. Adding a ticker is now "drop in a folder with a news.md." *(Kept as a prose instruction to the agent — no script needed, since the routine already runs `ls tickers/`.)*

3. **Log-entry format validation. — DONE.** `scripts/lint_news_log.py` validates each Recent News Log entry against the invariants of `framework/latest-updates-workflow.md` §F.1 (the authority — the linter references it, does not encode a second copy) and also fails if the literal format skeleton is restated outside §F.1. **Hard-fails** (CI) on the structural invariants: date/range lead, ≥1 `[FRAMEWORK-TAG]`, bold `**Headline**`, the `→` implication clause. The "≥1 linked source" rule is a **non-blocking warning** for now — the legacy corpus predates link enforcement (20 bare-source entries across AAOI/WYFI/IBIDY/LPKF); promote it to a hard fail after a cleanup pass links them.

4. **Ticker news.md structure lint. — DONE.** `scripts/lint_news_structure.py` asserts each `tickers/*/news.md` has the required sections (Thesis context, Edge, Tripwires, Recent News Log) and the front-matter `company`/`blurb` the coverage grid depends on, **and** fails on any `tickers/*/` folder with no `news.md` (a half-created ticker that both the daily watch and `web/hooks/coverage.py` skip silently). CI gate via `.github/workflows/lint.yml`.

5. **Git commit/push plumbing. — DONE.** `scripts/commit_watch.py --date <date>` stages the changed `tickers/*/news.md` + `summaries/<date>.md`, commits `daily watch: <date>`, and pushes (`--no-push`/`--dry-run` for local use). Wired into `daily-watch.md` step 8.

7. **Summary-count stamper. — DONE (net-new, not in the original list).** `scripts/summarize_counts.py --date <date>` derives `tickers_checked`/`tripwires_fired`/`edge_shifts` from ground truth — the ticker count and the `[TRIPWIRE]`/`[EDGE±]` tags in the log lines added this run (`git diff`) — and stamps the summary frontmatter, replacing the LLM's hand-count and collapsing what was a 4× re-derivation of the tripwire signal to one source (the tag in the log entry). `--check` verifies; wired into `daily-watch.md` step 7a.

6. **Discord notification of the run summary. — DONE.** The daily watch writes
   its §B digest to `summaries/<date>.md`; `.github/workflows/notify-discord.yml`
   fires on push and `scripts/notify_discord.py` posts a colored header embed +
   chunked body to a Discord webhook (`DISCORD_WEBHOOK_URL` secret). Deterministic
   plumbing outside the LLM session — the dividing-line pattern in action.

## Part 3 — deferred efficiency backlog

Surfaced by the 2026-07-18 pipeline-efficiency review. **Not built** — captured here so
they aren't lost. Bucket 1 (scripts/determinism) is the work above; these are the rest.

### 3a. DRY the docs & code
The dividing-line refactor cut *awk/sync*, but the launchers still restate shared rules,
and the scripts duplicate helpers. Consolidating reduces drift and per-run context load.
- **Prose restated across files:** glob-newest-report rule (6×: `CLAUDE.md`, `latest-updates-workflow.md`, `earnings-digest.md`, and the whats-new/earnings/deep-dive SKILLs); "sub-agents research only, don't edit files" (5×); "confirm covered else build the deep-dive first" (4×); "read news.md, quote Edge/Tripwires verbatim" (4×); the date-setup Step 0 (4×); the Discord Step 6 block near-verbatim in the whats-new and earnings-digest SKILLs. Candidate: a single referenced block per rule, launchers link not restate.
- **Code duplicated:** two front-matter parsers (`notify_discord.py` hand-rolled vs `web/hooks/coverage.py` PyYAML vs the new stdlib `tickerlib.front_matter` — three now); Discord color constants + tripwire→red mapping copy-pasted across `notify_discord.py` and `notify_discord_ticker.py` instead of `discord_common.py`; `web/scripts/build.sh` and `serve.sh` duplicate the site-assembly block; `coverage._latest_report` vs `tickerlib.latest_report_date` (a cross-check test guards them — unify once safe to import across the `scripts/` ↔ `web/hooks/` boundary).

### 3b. Runtime token/$ cost
Highest raw savings, highest risk — touches the framework's deliberate quality mandate.
- **Opus pinned on every node** of deep-dive (orchestrator + 4 sub-agents) and earnings (3), including mechanical sub-tasks — no lighter tier. The framework is emphatic that a weaker model degrades synthesis invisibly, so any tiering must be scoped to demonstrably-mechanical sub-tasks only, and measured.
- **whats-new re-runs the daily-watch pipeline** with no same-day dedup: if the scheduled watch already covered a ticker hours earlier, an ad-hoc whats-new still re-globs, re-reads news.md, re-derives the hunt-list, and dispatches a fresh 6–10-search pass over the same window. Candidate: a same-day short-circuit keyed off the last log entry's timestamp.
- **No cross-run source cache** — every run re-fetches primary sources; the only memory is the append-only log.

### 3c. Human toil
- Collapse the store→commit→notify tail of an ad-hoc run into one command (the whats-new / earnings-digest SKILLs currently hand-invoke `notify_discord_ticker.py` as a separate step; `commit_watch.py` + the poster could be one wrapper).

## Already captured in Part 1 (for the record)
- `awk` section-extraction — **eliminated** by splitting the framework into purpose-scoped files.
- `cp`/`diff` framework sync — **eliminated** by making this repo canonical.
