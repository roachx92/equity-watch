# Markdown Framework Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the equity-watch markdown files to agentic-coding best practices — split the framework by purpose, merge the duplicated launcher files, add a `CLAUDE.md`, and stage the deterministic work for Part 2 — without breaking the live daily watch.

**Architecture:** Pure content relocation + de-duplication of markdown. The 212-line `Equity_Research_Framework.md` (Sections A–H) splits into three purpose-scoped files under `framework/`. `PROMPT.md` + `WORKFLOW.md` merge into one `daily-watch.md`. New `CLAUDE.md` orients agents; new `docs/part-2-scripts-plan.md` records deferred script work. The GitHub Actions YAML is repointed. No analytical rule is reworded — text is relocated, and the `awk` extraction and `cp`/`diff` sync disappear structurally.

**Tech Stack:** Markdown, GitHub Actions YAML, git. No runtime/build. Verification is `grep`/`diff`/`git`.

## Global Constraints

- **Preserve exact wording** of every standing rule and procedural instruction when relocating it. This is a reorganization, not a rewrite. The only permitted edits are: (a) changing which file a section lives in, (b) removing the `awk` extraction block, (c) removing the `cp`/`diff` sync discipline, (d) collapsing verbatim-duplicated prose to a single statement, (e) updating file-path references to the new layout.
- **Section letters (A/B/C/…) stay as headings** inside the split files so cross-references (`see Section G`, `Section B.3`, `§16`) keep resolving.
- **Do not edit ticker-file content** (`tickers/*.md`) — that is live monitoring state.
- **Do not change the analytical framework** — section semantics, the 16-section template, sub-agent templates, and rule text are untouched.
- Repo slug `roachx92/equity-watch` is correct — do not change it.
- Docs use kebab-case filenames; ticker files keep their symbol names; `README.md` / `CLAUDE.md` keep conventional caps.
- Work happens on branch `restructure-markdown-framework`. Commit after each task.
- Source line ranges below refer to `Equity_Research_Framework.md` as it exists at the start of this plan:
  A = 7–49, B = 52–79, C = 83–88, D = 92–106, E = 110–115, F = 119–134, G = 138–168, H = 172–208, changelog = 212.

---

### Task 1: Create `framework/standing-rules.md` (Sections A + E)

**Files:**
- Create: `framework/standing-rules.md`
- Source: `Equity_Research_Framework.md:7-49` (Section A), `Equity_Research_Framework.md:110-115` (Section E)

**Interfaces:**
- Produces: `framework/standing-rules.md` containing the `## A. Standing rules — apply to EVERY response` heading and the `## E. Honest limits — always in view` heading, with all sub-bullets verbatim. Referenced by `daily-watch.md` (Task 5), `CLAUDE.md` (Task 6), and the section-lookup table.

- [ ] **Step 1: Create the file**

Add a short title line, then paste Section A (lines 7–49) verbatim, then Section E (lines 110–115) verbatim. Structure:

```markdown
# Standing rules & honest limits

*Sections A and E of the equity research framework. These apply to EVERY response — the daily watch and every full report alike. Verbatim; relocated from the former single framework file.*

---

## A. Standing rules — apply to EVERY response
<... paste Equity_Research_Framework.md lines 7-49 body verbatim ...>

---

## E. Honest limits — always in view
<... paste Equity_Research_Framework.md lines 110-115 body verbatim ...>
```

- [ ] **Step 2: Verify no rule text was lost**

Run: `diff <(sed -n '9,49p;110,115p' Equity_Research_Framework.md) <(grep -A999 '### Sourcing' framework/standing-rules.md | sed '/^---$/,$d')` — inspect that every bullet from A's body and E's body is present. Simpler acceptance check:

Run: `grep -c '\- \[ \]' framework/standing-rules.md`
Expected: `30` (all 30 Section-A checkboxes; Section E uses plain `-` bullets, not checkboxes, so contributes 0). Cross-check against the source: `grep -c '\- \[ \]' <(sed -n '7,49p' Equity_Research_Framework.md)` must return the same number. If they differ, a bullet was dropped.

Run: `grep -c '^- ' framework/standing-rules.md` and confirm Section E's 4 limit bullets are present:
Run: `grep -F 'Reliable knowledge cutoff: end of January 2026' framework/standing-rules.md`
Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add framework/standing-rules.md
git commit -m "Add framework/standing-rules.md (Sections A + E)"
```

---

### Task 2: Create `framework/deep-dive-template.md` (Sections B, C, D, G, H + changelog)

**Files:**
- Create: `framework/deep-dive-template.md`
- Source: `Equity_Research_Framework.md` lines 52–79 (B), 83–88 (C), 92–106 (D), 138–168 (G), 172–208 (H), 212 (changelog)

**Interfaces:**
- Produces: `framework/deep-dive-template.md` carrying headings `## B.`, `## C.`, `## D.`, `## G.`, `## H.` verbatim, plus the "Standard adopted July 2026…" changelog line at the foot. Referenced by `CLAUDE.md`, the lookup table, and any "run the framework on TICKER" full-diligence request.

- [ ] **Step 1: Create the file**

Title line, then paste Sections B, C, D, G, H verbatim in that order (each keeps its `## X.` heading and any `---` separators between them), then the changelog line last. Structure:

```markdown
# Full deep-dive template & mandatory sub-agent prompts

*Sections B, C, D, G, H of the equity research framework — the full-diligence report standard and the four mandatory parallel sub-agent prompt templates. Verbatim; relocated from the former single framework file. Section A (standing rules) and Section E (honest limits) live in `standing-rules.md`; the daily "Latest Updates" workflow (Section F) lives in `latest-updates-workflow.md`.*

---

## B. Full deep-dive template — the standard sections
<... paste lines 54-79 body verbatim ...>

---

## C. Catalyst / milestone tracking — when watching a name
<... paste lines 85-88 body verbatim ...>

---

## D. Re-rate mapping — methodology (backs Section B.3)
<... paste lines 94-106 body verbatim ...>

---

## G. Competitive Moat & Landscape — MANDATORY depth standard (backs Section B.4–B.5)
<... paste lines 140-168 body verbatim ...>

---

## H. Filing, Counterparty & Sector — MANDATORY sub-agent templates (backs Section A)
<... paste lines 174-208 body verbatim ...>

---

*<... paste line 212 changelog verbatim ...>*
```

- [ ] **Step 2: Verify all five sections + templates survived**

Run: `for h in '## B.' '## C.' '## D.' '## G.' '## H.'; do grep -qF "$h" framework/deep-dive-template.md && echo "ok $h" || echo "MISSING $h"; done`
Expected: five `ok` lines, no `MISSING`.

Run: `grep -c 'Hard-coded sub-agent prompt template' framework/deep-dive-template.md`
Expected: `4` (competitive-moat, filing, counterparty, sector).

Run: `grep -F 'Standard adopted July 2026' framework/deep-dive-template.md`
Expected: one match (changelog preserved).

- [ ] **Step 3: Commit**

```bash
git add framework/deep-dive-template.md
git commit -m "Add framework/deep-dive-template.md (Sections B, C, D, G, H)"
```

---

### Task 3: Create `framework/latest-updates-workflow.md` (Section F)

**Files:**
- Create: `framework/latest-updates-workflow.md`
- Source: `Equity_Research_Framework.md:119-134` (Section F)

**Interfaces:**
- Produces: `framework/latest-updates-workflow.md` carrying the `## F. "Latest Updates" workflow` heading and its 6 numbered steps + §16 Tripwire/Edge assessment, verbatim. Referenced by `daily-watch.md` (Task 5) as the binding analytical procedure.

- [ ] **Step 1: Create the file**

```markdown
# "Latest Updates" workflow

*Section F of the equity research framework — the analytical procedure for "what's new / latest on [ticker]" checks, including the mandatory §16 Tripwire/Edge assessment. Verbatim; relocated from the former single framework file. Read alongside `standing-rules.md` (Sections A + E), which binds every step here.*

---

## F. "Latest Updates" workflow
<... paste Equity_Research_Framework.md lines 121-134 body verbatim ...>
```

- [ ] **Step 2: Verify the workflow steps survived**

Run: `grep -c 'Assess every event against the §16 Tripwire and Edge' framework/latest-updates-workflow.md`
Expected: `1`.

Run: `grep -Ec '^\s*[0-9]+\.' framework/latest-updates-workflow.md`
Expected: `6` (the six numbered workflow steps).

- [ ] **Step 3: Commit**

```bash
git add framework/latest-updates-workflow.md
git commit -m "Add framework/latest-updates-workflow.md (Section F)"
```

---

### Task 4: Verify full A–H coverage, then delete the old framework file

**Files:**
- Delete: `Equity_Research_Framework.md`

**Interfaces:**
- Consumes: the three files from Tasks 1–3.
- Produces: removal of the monolith. After this task, `grep -rl 'Equity_Research_Framework.md'` should return only files still to be edited in later tasks (`daily-watch` sources, README, YAML, the design/plan docs).

- [ ] **Step 1: Prove every section has a new home**

Run:
```bash
for s in 'A.' 'B.' 'C.' 'D.' 'E.' 'F.' 'G.' 'H.'; do \
  hits=$(grep -rlF "## $s" framework/ | wc -l | tr -d ' '); \
  echo "Section $s -> $hits file(s)"; done
```
Expected: every section reports `1 file(s)`. If any reports `0`, STOP — a section was dropped; fix the relevant Task before deleting.

- [ ] **Step 2: Delete the monolith**

```bash
git rm Equity_Research_Framework.md
```

- [ ] **Step 3: Verify**

Run: `test ! -f Equity_Research_Framework.md && echo removed`
Expected: `removed`.

- [ ] **Step 4: Commit**

```bash
git commit -m "Remove Equity_Research_Framework.md (split into framework/*)"
```

---

### Task 5: Merge `PROMPT.md` + `WORKFLOW.md` into `daily-watch.md`

**Files:**
- Create: `daily-watch.md`
- Delete: `PROMPT.md`, `WORKFLOW.md`
- Source: `PROMPT.md` (all), `WORKFLOW.md` (all)

**Interfaces:**
- Consumes: `framework/standing-rules.md`, `framework/latest-updates-workflow.md` (referenced by path in the "Order of authority" section).
- Produces: `daily-watch.md` — the single operational procedure the routine runs. Referenced by `.github/workflows/daily-watch.yml` (Task 8) and `CLAUDE.md` (Task 6).

**Assembly recipe.** `WORKFLOW.md` is the fuller operational checklist and is the base. Fold in the pieces unique to `PROMPT.md`, remove the `awk` block, and collapse every duplicated block to one statement. Assemble in this order:

1. **Title + purpose** — one line: "Daily 'What's New' equity-watch — the procedure the scheduled routine runs." (from `PROMPT.md:1-3` + `WORKFLOW.md:1-3`).
2. **Establish today's date** — paste `PROMPT.md:5` verbatim (the "establish today's date from the session's current-date context" paragraph).
3. **Order of authority** — replace the `awk`-extraction block (`PROMPT.md:7-13`) with direct reads. Write:
   > Read and apply, in this order of authority:
   > 1. **`framework/standing-rules.md`** (Sections A + E) — BINDING on every step and every sentence. If anything below conflicts with it, it wins. *Scope note (verbatim from source):* Section A's "Diligence depth — EXHAUSTIVE BY DEFAULT" subsection is scoped to full-report construction, NOT this daily scan — do not apply exhaustive/iterate-until-dry searching here (see the search-budget note in the Research method).
   > 2. **`framework/latest-updates-workflow.md`** (Section F) + its §16 Tripwire/Edge step — the analytical procedure for this task.
   > 3. This file — how to apply Section F to `tickers/*.md` (read each ticker file, tag, append the log, commit).
   >
   > These are small, purpose-scoped files — read them directly. If any is missing from the checkout, STOP and report it rather than proceeding from memory.
   (This preserves the intent of `PROMPT.md:15-18` and `WORKFLOW.md:5-7` without the `awk` commands and without the "don't read the whole 210-line file" token warning, which no longer applies.)
4. **Research method — parallel per-ticker sub-agents** — state ONCE. Use `WORKFLOW.md:8-16` (the fuller version with the 6-point self-contained-prompt requirements list). Drop the near-identical `PROMPT.md:19-22` restatement.
5. **Source quality** — state ONCE, from `WORKFLOW.md:18` (identical to `PROMPT.md:24-25`).
6. **First-run window** — state ONCE, from `WORKFLOW.md:19` (identical to `PROMPT.md:27-28`).
7. **Task (numbered steps)** — merge `PROMPT.md:30-39` (Task 1–7) with `WORKFLOW.md:21-31` (per-ticker steps 1–5). Keep the fuller wording of each step; the two lists describe the same procedure (dispatch → categorize → assess Tripwire/Edge → append full-detail dated log entries most-recent-first with bolded headline → commit & push). Include `PROMPT.md`'s step 6 (run summary) and step 7 (conditional per-ticker recap) as pointers to the Run-summary section below.
8. **Run summary format** — state ONCE, from `WORKFLOW.md:33-45` (the detailed version: tripwires-first bullet format, edge-shifts format, per-ticker headline + one-sentence digest, conditional Edge/Tripwire recap). Drop the duplicated `PROMPT.md:36-37`.
9. **Closing rule** — from `WORKFLOW.md:47`: apply all of `framework/standing-rules.md` to every step; do not work from a remembered summary; if the framework files are missing, STOP and report.

- [ ] **Step 1: Write `daily-watch.md`** following the assembly recipe above. Every instruction from both source files must land in exactly one place.

- [ ] **Step 2: Coverage check — no instruction dropped in the merge**

Confirm each of these strings (one representative phrase per required instruction) appears exactly once in `daily-watch.md`:
```bash
for p in \
  'establish today' \
  'one sub-agent per ticker' \
  'quote its exact Edge and numbered Tripwires' \
  '~14 days back' \
  'SEC EDGAR' \
  'does not fire' \
  'bolded, one-line headline' \
  'TRIPWIRES FIRST' \
  'unchanged — Edge and Tripwires as before' \
  'commit'; do \
  n=$(grep -Fic "$p" daily-watch.md); echo "$n  $p"; done
```
Expected: each phrase count ≥ 1. Any `0` means that instruction was lost — restore it.

- [ ] **Step 3: Confirm the awk block is gone**

Run: `grep -c 'awk' daily-watch.md`
Expected: `0`.

- [ ] **Step 4: Delete the two source files**

```bash
git rm PROMPT.md WORKFLOW.md
```

- [ ] **Step 5: Commit**

```bash
git add daily-watch.md
git commit -m "Merge PROMPT.md + WORKFLOW.md into daily-watch.md; drop awk extraction"
```

---

### Task 6: Create `CLAUDE.md`

**Files:**
- Create: `CLAUDE.md`

**Interfaces:**
- Consumes: the file names produced by Tasks 1–5.
- Produces: `CLAUDE.md` at repo root — persistent orientation with the section→file lookup table.

- [ ] **Step 1: Write the file**

```markdown
# CLAUDE.md — equity-watch

## What this is
A live monitoring repo for a daily "What's New" equity watch. A Claude Code Remote Routine runs each weekday, reads `daily-watch.md`, dispatches one research sub-agent per ticker, assesses findings against each ticker's pre-committed **Edge** and **Tripwires**, and commits dated entries to `tickers/*.md`. The repo holds lightweight monitoring state only; the full 18-section deep-dive reports (`.docx`) are downstream artifacts.

## Canonical-source rule
- This repo is the **master** for the research framework. Apply the framework files as written — **never restate the rules from memory**.
- The `.docx` deep-dive reports are **downstream** consumers of the framework and sync to Google Drive (planned; see `docs/part-2-scripts-plan.md`).

## File map
- `framework/standing-rules.md` — Sections A + E. Standing rules and honest limits; apply to EVERY response.
- `framework/latest-updates-workflow.md` — Section F. The "what's new" analytical procedure (with §16 Tripwire/Edge assessment).
- `framework/deep-dive-template.md` — Sections B, C, D, G, H. The full-diligence report standard + the four mandatory sub-agent prompt templates.
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
```

- [ ] **Step 2: Verify the lookup table is complete**

Run: `for s in A B C D E F G H; do grep -q "| $s —" CLAUDE.md && echo "ok $s" || echo "MISSING $s"; done`
Expected: eight `ok` lines.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "Add CLAUDE.md orientation + section->file lookup"
```

---

### Task 7: Rewrite `README.md` (canonical-source + file list)

**Files:**
- Modify: `README.md`

**Interfaces:**
- Produces: a `README.md` whose "single source of truth" section reflects repo-as-canonical, whose file list matches the new layout, and which states that `.docx` reports sync to Google Drive.

- [ ] **Step 1: Replace the file-list bullets (current lines 5–7)**

Replace:
```markdown
- **`WORKFLOW.md`** — the self-contained daily workflow the agent runs.
- **`PROMPT.md`** — the exact prompt the scheduled routine executes.
- **`tickers/*.md`** — one watch-file per ticker: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.
```
with:
```markdown
- **`daily-watch.md`** — the self-contained daily procedure the scheduled routine runs (merged launcher + workflow).
- **`framework/`** — the analytical framework, split by purpose: `standing-rules.md` (Sections A + E), `latest-updates-workflow.md` (Section F), `deep-dive-template.md` (Sections B, C, D, G, H).
- **`tickers/*.md`** — one watch-file per ticker: thesis context, Edge (variant view), numbered Tripwires (pre-committed exit triggers), and the Recent News Log.
- **`CLAUDE.md`** — orientation for agents working in the repo (file map + section lookup).
```

- [ ] **Step 2: Replace the "Single source of truth & sync discipline" section (current lines 9–19)**

Replace the paragraph beginning "The canonical, full deep-dive reports…" and the whole "## Single source of truth & sync discipline" block (through the `diff`/changelog paragraph and the fenced `cp`/`git` block) with:

```markdown
The full, 18-section deep-dive reports (`.docx`) live locally and **sync to Google Drive** (see `docs/part-2-scripts-plan.md`); this repo holds only the lightweight monitoring state so the cloud agent can read the Edge/Tripwire and commit news back. Fold any flagged items into the deep-dive reports during a local session.

## Single source of truth
This repo is the **canonical home of the research framework** (`framework/*.md`). The deep-dive `.docx` reports are downstream consumers of it, not the other way around. `daily-watch.md` and the `framework/` files are read and applied as written — the rules are never restated from memory, so the agent always obeys the current framework.
```

- [ ] **Step 3: Verify staleness is gone**

Run: `grep -Ec 'cp \"|byte-identical|WORKFLOW\.md|PROMPT\.md' README.md`
Expected: `0`.
Run: `grep -Fc 'Google Drive' README.md`
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "README: repo is canonical; drop cp/diff sync; note Drive sync + new layout"
```

---

### Task 8: Repoint `.github/workflows/daily-watch.yml`

**Files:**
- Modify: `.github/workflows/daily-watch.yml:39` (the "Then read and follow PROMPT.md" instruction inside the inline prompt)

**Interfaces:**
- Produces: a workflow whose prompt tells the agent to read `daily-watch.md`.

- [ ] **Step 1: Update the prompt text**

Replace:
```
            Then read and follow PROMPT.md in this repo exactly, end to end.
            It is self-contained and references Equity_Research_Framework.md
            and WORKFLOW.md in the same repo. This includes: scanning each
```
with:
```
            Then read and follow daily-watch.md in this repo exactly, end to
            end. It is self-contained and references the framework/ files in
            the same repo (standing-rules.md and latest-updates-workflow.md).
            This includes: scanning each
```

- [ ] **Step 2: Verify**

Run: `grep -Ec 'PROMPT\.md|WORKFLOW\.md|Equity_Research_Framework\.md' .github/workflows/daily-watch.yml`
Expected: `0`.
Run: `grep -Fc 'daily-watch.md' .github/workflows/daily-watch.yml`
Expected: `1`.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/daily-watch.yml
git commit -m "CI: point daily-watch prompt at daily-watch.md"
```

---

### Task 9: Create `docs/part-2-scripts-plan.md`

**Files:**
- Create: `docs/part-2-scripts-plan.md`

**Interfaces:**
- Produces: the Part-2 backlog referenced by `CLAUDE.md` and `README.md`.

- [ ] **Step 1: Write the file**

```markdown
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
```

- [ ] **Step 2: Verify**

Run: `grep -Fc 'Google Drive' docs/part-2-scripts-plan.md`
Expected: `1` (at minimum).

- [ ] **Step 3: Commit**

```bash
git add docs/part-2-scripts-plan.md
git commit -m "Add Part 2 scripts backlog (incl. Google Drive report sync)"
```

---

### Task 10: Final integrity sweep

**Files:** none created — verification only.

- [ ] **Step 1: No dangling references to deleted files**

Run:
```bash
grep -rEl 'Equity_Research_Framework\.md|(^|[^-])PROMPT\.md|WORKFLOW\.md' \
  --include='*.md' --include='*.yml' . \
  | grep -v 'docs/superpowers/'
```
Expected: no output. (The design/plan docs under `docs/superpowers/` legitimately mention the old names as history and are excluded.)

- [ ] **Step 2: Every framework section resolves to exactly one file**

Run:
```bash
for s in A B C D E F G H; do \
  n=$(grep -rlF "## $s." framework/ | wc -l | tr -d ' '); \
  echo "Section $s -> $n"; done
```
Expected: each section → `1`.

- [ ] **Step 3: Tree matches the target layout**

Run: `find . -name '*.md' -not -path './.git/*' -not -path './docs/superpowers/*' | sort`
Expected exactly:
```
./CLAUDE.md
./README.md
./daily-watch.md
./docs/part-2-scripts-plan.md
./framework/deep-dive-template.md
./framework/latest-updates-workflow.md
./framework/standing-rules.md
./tickers/IBIDY.md
./tickers/LPKF.md
./tickers/WYFI.md
```

- [ ] **Step 4: Ticker content untouched**

Run: `git diff main --stat -- tickers/`
Expected: no output (no ticker file changed on this branch).

- [ ] **Step 5: YAML still parses**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/daily-watch.yml')); print('yaml ok')"`
Expected: `yaml ok`.

- [ ] **Step 6: Commit any final touch-ups** (only if a prior step required a fix)

```bash
git add -A && git commit -m "Final integrity sweep for framework restructure" || echo "nothing to commit"
```

---

## Post-plan follow-ups (outside this repo — cannot be automated here)

1. **Update the Claude Code Remote Routine.** Its prompt currently references `PROMPT.md`; repoint it to `daily-watch.md`. The repo change alone will not update the scheduler.
2. **Part 2 execution.** Work `docs/part-2-scripts-plan.md` as a separate spec → plan → implementation cycle, starting with the Google Drive report sync.
