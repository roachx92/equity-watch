# equity-watch

Monitoring state for a daily "What's New" check on a set of equity-research names. A scheduled cloud agent runs each weekday morning, scans news for each ticker, assesses it against that ticker's **Edge** and **Tripwires**, and appends dated entries to the per-ticker Recent News Log.

- **`WORKFLOW.md`** — the self-contained daily workflow the agent runs.
- **`PROMPT.md`** — the exact prompt the scheduled routine executes.
- **`tickers/*.md`** — one watch-file per ticker: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.

The canonical, full deep-dive reports (18-section `.docx`) live locally outside this repo; this repo holds only the lightweight monitoring state so a cloud agent can read the Edge/Tripwire and commit news back. Fold any flagged items into the local `.docx` reports during a local session.

## Single source of truth & sync discipline
The **rules and workflow are NOT duplicated** here — they live in `Equity_Research_Framework.md`, which is a **byte-identical copy** of the canonical local framework (`…/research framework/Equity_Research_Framework.md`). `PROMPT.md` and `WORKFLOW.md` are thin launchers that *read and apply* Section A (standing rules) and Section F (workflow) from that file — they never restate the rules from memory, so the agent always obeys the real, current framework.

**When the local framework changes** (standing rules, Section F, or the §16 Tripwire/Edge concept), re-copy it into this repo and push, so the cloud agent stays in sync:
```
cp "<local>/research framework/Equity_Research_Framework.md" ./Equity_Research_Framework.md
git commit -am "sync framework" && git push
```
Drift is detectable at any time with a plain `diff` between this copy and the local canonical file — if they differ, the repo is stale. (The framework's own changelog line at the bottom of the file serves as the version stamp.)

Tickers watched: **IBIDY** (Ibiden 4062), **WYFI** (WhiteFiber), **LPKF** (LPKF Laser).

_Not financial advice — informational research tooling only._
