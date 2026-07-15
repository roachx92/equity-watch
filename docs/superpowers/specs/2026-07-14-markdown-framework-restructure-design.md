# Design: Restructure the equity-watch markdown framework

**Date:** 2026-07-14
**Status:** Approved (design phase)
**Scope:** Part 1 of a two-part initiative. Part 1 = reorganize the markdown files to agentic-coding best practices. Part 2 (planned here, built later) = move deterministic tasks out of prompts into scripts.

---

## 1. Context

`equity-watch` (`roachx92/equity-watch`) is a **live, in-production** monitoring system. A Claude Code Remote Routine runs every weekday morning, reads the launcher prompt, dispatches one research sub-agent per ticker, assesses findings against each ticker's pre-committed **Edge** and **Tripwires**, and commits dated entries back to `tickers/*.md`. A disabled GitHub Actions cron (`workflow_dispatch` only) is kept for manual runs.

The repo today is entirely markdown:

| File | Role |
| --- | --- |
| `README.md` | Human-facing intro + sync discipline |
| `Equity_Research_Framework.md` (212 lines) | The analytical "brain": Sections A–H (standing rules, 16-section deep-dive template, methodologies, the daily-watch procedure, and mandatory sub-agent templates) |
| `PROMPT.md` | The exact prompt the scheduled routine runs |
| `WORKFLOW.md` | Operational checklist applying Section F to the repo layout |
| `tickers/{IBIDY,WYFI,LPKF}.md` | Per-ticker monitoring state (thesis, Edge, Tripwires, Recent News Log) |
| `.github/workflows/daily-watch.yml` | CI (cron disabled; manual dispatch); invokes `claude-code-action` reading `PROMPT.md` |

### Problems this design fixes

1. **Duplication between `PROMPT.md` and `WORKFLOW.md`.** The parallel-sub-agent research method, source-quality guidance, first-run window, and run-summary format are each stated twice, near-verbatim. They will drift.
2. **No `CLAUDE.md`.** Nothing gives an agent (or a new human contributor) persistent orientation to the repo, its layering, or its rules.
3. **Deterministic hacks embedded in reasoning prompts.** An `awk` section-extraction block in `PROMPT.md`; a manual `cp` + `diff` sync discipline for the framework file; hardcoded ticker lists in three files.
4. **One file mixes two jobs.** `Equity_Research_Framework.md` carries both the full-diligence deep-dive standard (B–E, G, H) and the daily-watch procedure (F). The daily watch needs only A + F — which is *why* the brittle `awk` extraction exists.
5. **External source of truth.** The framework file was maintained as a "byte-identical copy" of a local canonical file, drift-detectable only by a manual `diff`.

### Decisions taken during brainstorming

1. **This repo becomes canonical** for the framework. The local `.docx` deep-dive reports become downstream consumers. The `cp`/`diff` sync discipline is removed.
2. **Split the framework file by purpose**, eliminating the `awk` hack structurally.
3. **Merge `PROMPT.md` + `WORKFLOW.md`** into one canonical daily-watch procedure, removing a hop and all cross-file duplication.
4. **New requirement:** the full deep-dive `.docx` reports should sync to **Google Drive**. Planned in Part 2 (not built during this pass); Drive becomes the reports' home/distribution point.
5. `roachx92/equity-watch` is the correct repo slug (verified) — no change needed there.

---

## 2. Target structure

```
CLAUDE.md                            NEW  — agent + human orientation
README.md                            KEEP — rewrite the sync section
framework/
  standing-rules.md                  ← Section A (+ Section E "honest limits")
  deep-dive-template.md              ← Sections B, C, D, G, H
  latest-updates-workflow.md         ← Section F
daily-watch.md                       ← PROMPT.md + WORKFLOW.md merged
tickers/{IBIDY,WYFI,LPKF}.md         KEEP — unchanged (live state)
docs/part-2-scripts-plan.md          NEW  — deterministic-tasks → scripts backlog
docs/superpowers/specs/2026-07-14-*  this design doc
.github/workflows/daily-watch.yml    EDIT — point at daily-watch.md; drop awk mention
```

**Deleted:** `Equity_Research_Framework.md`, `PROMPT.md`, `WORKFLOW.md`. All their content moves into the files above — nothing is lost.

### Cross-reference strategy

The framework's sections cross-reference each other densely by letter (`see Section G`, `Section B.3`, `§16`). To keep every reference resolving with minimal churn:

- **Section letters (A/B/C/…) are preserved as headings inside the split files.** Splitting changes which *file* a section lives in, not its label.
- `CLAUDE.md` carries a **section → file lookup table** so an agent can find "Section G" without scanning.

---

## 3. Per-file content plan

### `framework/standing-rules.md`
Section A verbatim, plus Section E ("Honest limits — always in view") folded in. Rationale: both are explicitly "apply to every response / always in view." Folding E in means the daily watch (which currently extracts only A) also sees the knowledge-cutoff and no-live-data limits — a reasoning gain. **No rule text is reworded; text is only relocated.**

### `framework/deep-dive-template.md`
The full-diligence bundle: Section B (16-section report template), C (catalyst/milestone tracking), D (re-rate mapping methodology), G (competitive-moat depth standard + its sub-agent prompt template), H (filing/counterparty/sector sub-agent prompt templates). Section letters retained as headings.

### `framework/latest-updates-workflow.md`
Section F ("Latest Updates" workflow) verbatim, including its §16 Tripwire/Edge assessment step.

### `daily-watch.md` (merged `PROMPT.md` + `WORKFLOW.md`)
One canonical operational procedure the routine runs. Each concept stated **once**:
- **Order of authority** — read `framework/standing-rules.md` and `framework/latest-updates-workflow.md` **directly**. The `awk` extraction block is **deleted** (the files are already scoped). Still instructs: if the framework files are missing from the checkout, STOP and report rather than proceeding from memory.
- **Research method** — parallel per-ticker sub-agents (one per ticker, single dispatch, research-only, orchestrator synthesizes and does all writes). Stated once.
- **Source quality**, **first-run window**, **task steps (categorize → assess Tripwire/Edge → append log → commit/push)**, **run-summary format (tripwires first; per-ticker headline + one-sentence digest; conditional Edge/Tripwire recap)** — each stated once.

### `CLAUDE.md` (new)
Persistent orientation, concise:
- One-paragraph "what this is."
- File map + **section → file lookup table**.
- The layering: standing rules → workflow → launcher (`daily-watch.md`) → per-ticker state.
- The **canonical-source rule**: this repo is master for the framework; `.docx` deep-dive reports are downstream and sync to Google Drive (Part 2).
- The standing directive: **apply the framework files as written — never restate the rules from memory.**

### `README.md`
Rewrite the "Single source of truth & sync discipline" section: the repo is now canonical; the `cp`/`diff` discipline is removed. Add that the full deep-dive `.docx` reports live in / sync to Google Drive. Update the file list to the new layout. Keep the "not financial advice" disclaimer and the watched-tickers line.

### `.github/workflows/daily-watch.yml`
Update the inline prompt to point at `daily-watch.md` instead of `PROMPT.md`; drop any section-extraction/`awk` mention. Leave `workflow_dispatch`-only triggering and the `roachx92/equity-watch` reference unchanged.

---

## 4. `docs/part-2-scripts-plan.md` (planning artifact — nothing built in Part 1)

Catalogs deterministic work to move from prompts into scripts. Each item: trigger + sketch. The stated dividing line: **scripts do plumbing/validation/sync; the LLM does research and assessment.**

1. **Deep-dive `.docx` → Google Drive sync** *(new requirement)* — publish/update reports to a Drive folder when a report is created or updated. Options to evaluate: Google Drive MCP vs. a Drive-API / `rclone` script. Decide direction (one-way publish vs. two-way) and folder layout at build time.
2. **Ticker enumeration** — derive the watch-list from a `tickers/*.md` glob instead of the hardcoded IBIDY/WYFI/LPKF lists, so adding a ticker means dropping in a file.
3. **Log-entry format validation** — a linter for the `YYYY-MM-DD — [TAG] [TRIPWIRE/EDGE± if any] — **Headline**. … Source: …` entry shape.
4. **Ticker-file structure lint** — assert each ticker file has Thesis context / Edge / Tripwires / Recent News Log sections.
5. **Git commit/push plumbing** — the mechanical commit-and-push step.
6. **Already captured (for the record):** `awk` section-extraction → *eliminated by the framework split*; `cp`/`diff` framework sync → *eliminated by repo-becomes-canonical*.

---

## 5. Safety / keeping the live watch working

The daily routine runs off these files, so the implementation must:

1. **Preserve exact wording** of every standing rule and procedural instruction where it is relocated (relocations, not rewrites).
2. **Coverage check** before finishing: confirm the merged `daily-watch.md` contains every instruction the old `PROMPT.md` + `WORKFLOW.md` carried (an explicit item-by-item check, not a vibe).
3. **Update the CI YAML in the same change** so `daily-watch.yml` points at `daily-watch.md`.

### Out-of-band follow-up (cannot be done from this repo)

The real scheduler is a **Claude Code Remote Routine** configured outside this repo. Its prompt currently references `PROMPT.md` and must be updated to `daily-watch.md`. This design **flags** it; the repo change alone will not update the routine.

---

## 6. Explicitly out of scope (Part 1)

- Building any script (all of §4 is Part 2).
- Wiring up the Google Drive sync.
- Editing ticker-file *content* (the live monitoring state is left as-is).
- Changing the framework's analytical rules, section semantics, or the 16-section template. This is a reorganization, not a rewrite.
