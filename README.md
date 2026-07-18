# equity-watch

Monitoring state for on-demand, per-ticker equity research. Three workflows run against a watched name — a **what's-new** news scan, an **earnings-digest** call breakdown, and a full **deep-dive** — each assessing findings against that ticker's pre-committed **Edge** and **Tripwires** and appending dated entries to its Recent News Log.

- **`framework/`** — the analytical framework, split by purpose: `standing-rules.md` (Sections A + E), `latest-updates-workflow.md` (Section F — the "what's new" workflow), `deep-dive-template.md` (Sections B, C, D, G, H), `earnings-digest.md` (Section I), `news-check.md` (the shared news-check spec: §A agentic parallel-sub-agent research method, §B run-summary chat-digest format).
- **`tickers/<TICKER>/news.md`** — one folder per ticker, each holding that ticker's **news.md**: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.
- **`CLAUDE.md`** — orientation for agents working in the repo (file map + section lookup).

The full deep-dive reports are **markdown in git** at `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` and are published as a **GitHub Pages site** (see `docs/part-2-scripts-plan.md`). Each workflow reads the Edge/Tripwire and commits news back to the ticker's `news.md`; fold flagged items into the deep-dive reports during a local session.

## Single source of truth
This repo is the **canonical home of the research framework** (`framework/*.md`) **and of the deep-dive reports** (`tickers/*/reports/**`), applying the framework as written. The `framework/` files are read and applied verbatim — the rules are never restated from memory, so the agent always obeys the current framework.

Tickers watched: one folder per ticker under [`tickers/`](tickers/), each holding a `news.md` — that directory is the live watch-list (adding a ticker is "drop in a folder with a news.md"). See each ticker's news.md for its thesis, Edge, and Tripwires.

_Not financial advice — informational research tooling only._
