# Part 2 — deterministic tasks → scripts (backlog)

Part 1 reorganized the markdown. Part 2 moves the remaining **deterministic** work out of prompts and into scripts, so the LLM is left to do research and assessment. Nothing here is built yet.

**Dividing line:** scripts do plumbing, validation, and sync; the LLM does research and assessment.

## Backlog

1. **Deep-dive reports → markdown-in-git, published via GitHub Pages.** *(Was: `.docx` → Google Drive sync — dropped.)* Reports live as `reports/<YYYY-MM-DD>/<TICKER>.md` (git is the source of truth) and the repo is published as a MkDocs Material site with a bespoke "Research Desk" homepage. No `.docx`, no Drive, no external auth. **Follow-on (deterministic, deferred):** a "latest report per ticker" resolver script so the ticker pointer updates itself instead of by hand.

2. **Ticker enumeration. — DONE.** The watch-list is derived from a `tickers/*.md` glob: `daily-watch.md` enumerates the directory at run start and dispatches one sub-agent per file found; the hardcoded name-lists and "four sub-agents" counts are gone, and CLAUDE.md/README point at the directory as the source of truth. Adding a ticker is now "drop in a file." *(Kept as a prose instruction to the agent — no script needed, since the routine already runs `ls tickers/`.)*

3. **Log-entry format validation.** A linter for the Recent News Log entry shape: `YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — **Headline**. … Source: <name(s)> (<date>).` Fails CI on malformed entries.

4. **Ticker-file structure lint.** Assert each `tickers/*.md` has the required sections: Thesis context, Edge, Tripwires, Recent News Log.

5. **Git commit/push plumbing.** The mechanical commit-and-push of changed ticker files (message `daily watch: <date>`), moved from prose instruction into a script step the agent invokes.

## Already captured in Part 1 (for the record)
- `awk` section-extraction — **eliminated** by splitting the framework into purpose-scoped files.
- `cp`/`diff` framework sync — **eliminated** by making this repo canonical.
