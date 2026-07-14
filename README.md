# equity-watch

Monitoring state for a daily "What's New" check on a set of equity-research names. A scheduled cloud agent runs each weekday morning, scans news for each ticker, assesses it against that ticker's **Edge** and **Tripwires**, and appends dated entries to the per-ticker Recent News Log.

- **`WORKFLOW.md`** — the self-contained daily workflow the agent runs.
- **`PROMPT.md`** — the exact prompt the scheduled routine executes.
- **`tickers/*.md`** — one watch-file per ticker: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.

The canonical, full deep-dive reports (18-section `.docx`) live locally outside this repo; this repo holds only the lightweight monitoring state so a cloud agent can read the Edge/Tripwire and commit news back. Fold any flagged items into the local `.docx` reports during a local session.

Tickers watched: **IBIDY** (Ibiden 4062), **WYFI** (WhiteFiber), **LPKF** (LPKF Laser).

_Not financial advice — informational research tooling only._
