# Part 2 — deterministic tasks → scripts (backlog)

Part 1 reorganized the markdown. Part 2 moves the remaining **deterministic** work out of prompts and into scripts, so the LLM is left to do research and assessment. Nothing here is built yet.

**Dividing line:** scripts do plumbing, validation, and sync; the LLM does research and assessment.

## Backlog

1. **Deep-dive reports → markdown-in-git, published via GitHub Pages.** *(Was: `.docx` → Google Drive sync — dropped.)* Reports live as `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` (git is the source of truth) and the repo is published as a MkDocs Material site with a bespoke "Research Desk" homepage. No `.docx`, no Drive, no external auth. **Follow-on (deterministic, deferred):** a "latest report per ticker" resolver script so the ticker pointer updates itself instead of by hand.

2. **Ticker enumeration. — DONE.** The watch-list is derived from a `tickers/*/` folder glob (each holding a `news.md`): the per-ticker workflows and the site build enumerate the directory; the hardcoded name-lists and "four sub-agents" counts are gone, and CLAUDE.md/README point at the directory as the source of truth. Adding a ticker is now "drop in a folder with a news.md." *(Kept as a prose instruction to the agent — no script needed, since a workflow just runs `ls tickers/`.)*

3. **Log-entry format validation.** A linter for the Recent News Log entry shape, validating against the canonical spec in `framework/latest-updates-workflow.md` §F.1 (which is the authority — the linter must not encode a second copy of the format). Fails CI on malformed entries. Worth also asserting the rules that drift silently: every entry carries at least one linked source, and no `_template`-style restatement of the format reappears outside §F.1.

4. **Ticker news.md structure lint.** Assert each `tickers/*/news.md` has the required sections: Thesis context, Edge, Tripwires, Recent News Log — plus the YAML front matter (`company`, `blurb`) the homepage coverage grid depends on. Also flag a `tickers/*/` folder with no `news.md`: both the per-ticker workflows and `web/hooks/coverage.py` skip it silently, so a half-created ticker goes unwatched without erroring.

5. **Git commit/push plumbing.** The mechanical commit-and-push of changed ticker news.md files, moved from prose instruction into a script step the agent invokes.

6. **Discord notification of the per-ticker digest. — DONE.** At the end of a `/whats-new`
   or `/earnings-digest <TICKER>` run, `scripts/notify_discord_ticker.py` posts the §B
   chat digest (colored header embed + chunked body) to that ticker's Discord webhook,
   looked up in `.secrets/discord-webhooks.json`. Runs locally in-session — deterministic
   plumbing outside the LLM's assessment, the dividing-line pattern in action.

*(Superseded, July 2026 — dropped: the scheduled all-ticker daily watch and its
`summaries/<date>.md` → push-triggered Discord pipeline. The pipeline is now per-ticker,
on-demand only; item 6 above reflects the surviving per-ticker poster.)*

## Already captured in Part 1 (for the record)
- `awk` section-extraction — **eliminated** by splitting the framework into purpose-scoped files.
- `cp`/`diff` framework sync — **eliminated** by making this repo canonical.
