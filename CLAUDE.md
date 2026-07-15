# CLAUDE.md — equity-watch

## What this is
A live monitoring repo for a daily "What's New" equity watch. A Claude Code Remote Routine runs each weekday, reads `daily-watch.md`, dispatches one research sub-agent per ticker, assesses findings against each ticker's pre-committed **Edge** and **Tripwires**, and commits dated entries to `tickers/*.md`. The repo holds the lightweight monitoring state **and** the full deep-dive reports (markdown under `reports/<YYYY-MM-DD>/<TICKER>.md`); the repo is published as a MkDocs Material GitHub Pages site.

## Canonical-source rule
- This repo is the **master** for the research framework. Apply the framework files as written — **never restate the rules from memory**.
- Deep-dive reports are **markdown in this repo** (`reports/<YYYY-MM-DD>/<TICKER>.md`), applying the framework; they are published via GitHub Pages (see `docs/part-2-scripts-plan.md`). No `.docx`, no external sync.

## File map
- `framework/standing-rules.md` — Sections A + E. Standing rules and honest limits; apply to EVERY response.
- `framework/latest-updates-workflow.md` — Section F. The "what's new" analytical procedure (with §16 Tripwire/Edge assessment).
- `framework/deep-dive-template.md` — Sections B, C, D, G, H. The full-diligence report standard + the four mandatory sub-agent prompt templates.
- `framework/news-check.md` — the single canonical spec shared by the daily watch and the "what's new" workflow: §A the agentic parallel-sub-agent research method (+ source-quality & first-run window), §B the run-summary chat-digest format.
- `daily-watch.md` — the operational procedure the routine runs (applies Sections A + F to this repo's layout).
- `tickers/{IBIDY,WYFI,LPKF}.md` — per-ticker state: thesis, Edge, numbered Tripwires, Recent News Log.
- `docs/part-2-scripts-plan.md` — planned migration of deterministic tasks to scripts.

## Section → file lookup
| Section | Lives in |
| --- | --- |
| A — Standing rules | `framework/standing-rules.md` |
| B — Full deep-dive template | `framework/deep-dive-template.md` |
| C — Catalyst / milestone tracking | `framework/deep-dive-template.md` |
| D — Re-rate mapping methodology | `framework/deep-dive-template.md` |
| E — Honest limits | `framework/standing-rules.md` |
| F — "Latest Updates" workflow | `framework/latest-updates-workflow.md` |
| G — Competitive-moat depth standard | `framework/deep-dive-template.md` |
| H — Filing/counterparty/sector templates | `framework/deep-dive-template.md` |

## Layering
Standing rules (always) → latest-updates workflow (the method) → `daily-watch.md` (launcher/ops) → `tickers/*.md` (state).

## Two entry points
- **Daily watch:** the routine reads `daily-watch.md`. Uses Sections A + F only.
- **Full deep-dive** ("run the framework on TICKER"): use `framework/deep-dive-template.md` with all four sub-agent templates, under `framework/standing-rules.md`.

_Not financial advice — informational research tooling only._
