# equity-watch

Monitoring state for a daily "What's New" check on a set of equity-research names. A scheduled cloud agent runs each weekday morning, scans news for each ticker, assesses it against that ticker's **Edge** and **Tripwires**, and appends dated entries to the per-ticker Recent News Log.

- **`daily-watch.md`** — the self-contained daily procedure the scheduled routine runs (merged launcher + workflow).
- **`framework/`** — the analytical framework, split by purpose: `standing-rules.md` (Sections A + E), `latest-updates-workflow.md` (Section F), `deep-dive-template.md` (Sections B, C, D, G, H), `run-summary-format.md` (the shared chat-digest format).
- **`tickers/*.md`** — one watch-file per ticker: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.
- **`CLAUDE.md`** — orientation for agents working in the repo (file map + section lookup).

The full deep-dive reports are **markdown in git** at `reports/<YYYY-MM-DD>/<TICKER>.md` and are published as a **GitHub Pages site** (see `docs/part-2-scripts-plan.md`). The cloud agent reads the Edge/Tripwire and commits news back to `tickers/*.md`; fold flagged items into the deep-dive reports during a local session.

## Single source of truth
This repo is the **canonical home of the research framework** (`framework/*.md`) **and of the deep-dive reports** (`reports/**`), applying the framework as written. `daily-watch.md` and the `framework/` files are read and applied verbatim — the rules are never restated from memory, so the agent always obeys the current framework.

Tickers watched: **IBIDY** (Ibiden 4062), **WYFI** (WhiteFiber), **LPKF** (LPKF Laser).

_Not financial advice — informational research tooling only._
