# equity-watch

Monitoring state for a daily "What's New" check on a set of equity-research names. A scheduled cloud agent runs each weekday morning, scans news for each ticker, assesses it against that ticker's **Edge** and **Tripwires**, and appends dated entries to the per-ticker Recent News Log.

- **`daily-watch.md`** — the self-contained daily procedure the scheduled routine runs (merged launcher + workflow).
- **`framework/`** — the analytical framework, split by purpose: `standing-rules.md` (Sections A + E), `latest-updates-workflow.md` (Section F), `deep-dive-template.md` (Sections B, C, D, G, H).
- **`tickers/*.md`** — one watch-file per ticker: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.
- **`CLAUDE.md`** — orientation for agents working in the repo (file map + section lookup).

The full, 18-section deep-dive reports (`.docx`) live locally and **sync to Google Drive** (see `docs/part-2-scripts-plan.md`); this repo holds only the lightweight monitoring state so the cloud agent can read the Edge/Tripwire and commit news back. Fold any flagged items into the deep-dive reports during a local session.

## Single source of truth
This repo is the **canonical home of the research framework** (`framework/*.md`). The deep-dive `.docx` reports are downstream consumers of it, not the other way around. `daily-watch.md` and the `framework/` files are read and applied as written — the rules are never restated from memory, so the agent always obeys the current framework.

Tickers watched: **IBIDY** (Ibiden 4062), **WYFI** (WhiteFiber), **LPKF** (LPKF Laser).

_Not financial advice — informational research tooling only._
