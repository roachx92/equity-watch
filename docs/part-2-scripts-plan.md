# Part 2 — deterministic tasks → scripts (backlog)

Part 1 reorganized the markdown. Part 2 moves the remaining **deterministic** work out of prompts and into scripts, so the LLM is left to do research and assessment. Nothing here is built yet.

**Dividing line:** scripts do plumbing, validation, and sync; the LLM does research and assessment.

## Backlog

1. **Deep-dive `.docx` → Google Drive sync** *(new requirement).* Publish/update the full reports to a Drive folder when a report is created or updated. Decide at build time: Google Drive MCP vs. a Drive-API / `rclone` script; one-way publish vs. two-way; folder layout (one folder per ticker vs. flat). Trigger: report save, or a manual/scheduled push.

2. **Ticker enumeration.** Derive the watch-list from a `tickers/*.md` glob instead of the hardcoded IBIDY/WYFI/LPKF lists in `daily-watch.md`. Adding a ticker becomes "drop in a file."

3. **Log-entry format validation.** A linter for the Recent News Log entry shape: `YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — **Headline**. … Source: <name(s)> (<date>).` Fails CI on malformed entries.

4. **Ticker-file structure lint.** Assert each `tickers/*.md` has the required sections: Thesis context, Edge, Tripwires, Recent News Log.

5. **Git commit/push plumbing.** The mechanical commit-and-push of changed ticker files (message `daily watch: <date>`), moved from prose instruction into a script step the agent invokes.

## Already captured in Part 1 (for the record)
- `awk` section-extraction — **eliminated** by splitting the framework into purpose-scoped files.
- `cp`/`diff` framework sync — **eliminated** by making this repo canonical.
