---
name: deep-dive
description: >-
  Run a full-diligence equity deep-dive on a ticker in this equity-watch repo — the
  exhaustive, multi-sub-agent "run the framework" workflow that produces a dated
  18-section report under reports/<date>/<TICKER>.md and seeds the ticker's watch-list
  file. Use this whenever the user says "run the framework on <TICKER>", "do a full
  deep-dive / full diligence / full report on <ticker or company>", "deep dive <ticker>",
  "start watching <ticker>" (a new name needs its report built first), or otherwise asks
  for complete equity diligence on a stock — even if they don't say the word "framework".
  This is the heaviest of the three research entry points; for a lighter "what's new lately"
  news check on an already-covered name use the whats-new skill instead, and for breaking down
  one specific earnings call use the earnings-digest skill.
---

# Run the framework — full equity deep-dive

This skill is a **launcher**, not a rulebook. This repo is the master for the research
framework, and the binding rule (`CLAUDE.md`) is: **apply the framework files as written —
never restate the rules from memory.** Your job is to read the canonical files below,
orchestrate the work they define, and write the outputs to this repo's conventions. If any
framework file is missing from the checkout, STOP and report it rather than proceeding on a
remembered version.

## Step 0 — establish today's date
Take today's date from the session's current-date context (do **not** infer it from training
data). Use that exact date as the report folder, the report's `Date:` line, every point-in-time
figure's as-of stamp, and the commit message.

## Step 1 — read the canonical framework (in this order of authority)
Read these directly — they are small and purpose-scoped. Do not work from memory of them.
1. **`framework/standing-rules.md`** — Sections A + E. Binding on every sentence: search
   before asserting any time-sensitive fact, ground claims in primary sources and cite them,
   never fabricate, date every figure, separate contracted/backlog from recognized revenue,
   give the honest counterweight + pre-mortem. **Its "Diligence depth — EXHAUSTIVE BY DEFAULT"
   subsection applies here** (this IS a full report): read primary filings directly, diligence
   every counterparty, don't stop until searches go dry.
2. **`framework/deep-dive-template.md`** — Sections B0/B/C/D/G/H: the 18-section report standard (§B0, output architecture, is non-negotiable — model pinning, table mandate, exec-summary, depth floor),
   the Section D re-rate methodology, the Section G mandatory competitive-moat depth standard,
   and the **four hard-coded sub-agent prompt templates** (filing, counterparty, sector in §H;
   competitive-landscape in §G). Use those templates verbatim — fill the [BRACKETS], don't
   rewrite them.
3. **`reports/_template.md`** — the empty 18-section skeleton to copy from for the report file.

## Step 2 — dispatch the four mandatory sub-agents, in parallel
Per Section A and Section G/H: dispatch **four parallel research sub-agents in a single
dispatch** — **filing, counterparty, sector, and competitive-landscape** — each using its
hard-coded prompt template (fill [DATE], [COMPANY], [TICKER], [CORE TECH/PRODUCT]). **Pin every
sub-agent to Opus** (per standing-rules.md's model-pinning rule) — this is mandatory, not a
default to inherit; record the model used in the report's closing Methodology block. Each
sub-agent prompt is self-contained (sub-agents have no memory of this conversation). **Sub-agents
research only — they must NOT edit any files.** They run exhaustive, multi-pass web research and
report back dense, dated, source-linked, reliability-tiered findings. If the diligence-depth rule
wants more passes after the first synthesis (new material facts still surfacing), run them.

## Step 3 — synthesize and write the report
Wait for all four sub-agents, then synthesize their findings yourself (**this synthesis pass
runs on Opus** — per §B0.1 it is the most judgment-dense step in the framework) into
`reports/<today's-date>/<TICKER>.md`, copying the `reports/_template.md` skeleton and filling
**every section that applies** to Section B depth (§4/§5 together must satisfy the full Section G
competitive standard; §3 renders as **four separate typed re-rate tables**, per Section D; §8
must include the named pre-mortem; §18 must include the explicit **Edge** (variant view) and
**Tripwire** (falsification trigger + committed action)). **Apply §B0 in full** — it is
non-negotiable, not a style preference: the front-loaded executive summary (must stand alone,
not defer to §15), the 13-table mandate, the ~7,000-word depth floor, and the closing
Sources/Methodology/Caveats block with the model used. One dated snapshot per run — never
overwrite a prior date's file.

## Step 4 — seed / update the ticker's news.md
Each watched ticker is a **folder** under `tickers/`, named for the symbol, holding that
ticker's `news.md`; the `tickers/` directory **is** the watch-list. After the report is written:
- If `tickers/<TICKER>/news.md` does not exist, create the folder and the file, modeling an
  existing one (e.g. `tickers/CIFR/news.md`): frontmatter (`company`, `blurb` — these feed the
  homepage coverage grid via `hooks/coverage.py`), a one-paragraph thesis context, the **Edge**
  and **numbered Tripwires** derived **verbatim from the report's §18**, and an empty
  `## Recent News Log` seeded with the standard header note pointing at
  `framework/latest-updates-workflow.md` §F.1 (the canonical entry format — don't restate it).
- Set/refresh its `**Canonical deep-dive:**` line to link the new report file.
- The Edge/Tripwires in the ticker's news.md are the binding pre-committed triggers the daily
  watch and the whats-new skill assess against — mirror them faithfully, don't paraphrase away
  the specifics.
- A report without its ticker folder is invisible to the daily watch and the homepage build —
  this step is not optional for a new name.

## Step 5 — commit
Commit the new report and the created/updated ticker news.md with a clear message (e.g.
`deep-dive: <TICKER> full report <today's-date>`). Push only if the user asks or the repo's
routine expects it.

## Guardrails
- Not financial advice — informational research tooling only (per Section A). No unsolicited
  portfolio-fit / position-sizing commentary about the reader.
- Never fabricate a figure, source, or a precise market-share % — tier and hedge, say what
  couldn't be verified (Sections A + G).
- Reports are markdown in this repo. No `.docx`, no external sync.
