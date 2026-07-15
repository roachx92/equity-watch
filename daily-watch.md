# Daily "What's New" equity watch

The self-contained operational procedure the scheduled routine runs each weekday. It applies **Section A + E** (standing rules & honest limits) and **Section F** (the "Latest Updates" workflow) of the framework to this repo's `tickers/*.md` layout. It does NOT restate the rules — the binding source is the framework files under `framework/`.

**First, establish today's date** from the session's current-date context (do not guess or infer it from memory/training data). Use that exact date throughout this run: as the anchor for "since the last dated entry" / "last ~48h" news searches, as the date stamped on every log entry and every source citation, and in the commit message (`daily watch: <today's date>`) and the run summary.

## Order of authority
Read and apply, in this order of authority:

1. **`framework/standing-rules.md`** (Sections A + E) — BINDING on every step and every sentence you produce: search before answering anything time-sensitive; ground claims in primary/reputable sources and cite them; never fabricate (if unverifiable or a source is inaccessible, say so); date every point-in-time figure; separate contracted/backlog from recognized revenue; label fact vs estimate vs opinion; give the honest counterweight; not financial advice. If anything below appears to conflict with this, Section A wins. **Exception — scope it correctly:** Section A's "Diligence depth — EXHAUSTIVE BY DEFAULT" subsection is explicitly scoped (in its own text) to full report construction (triggered by "run the framework on [TICKER]"), NOT to this daily "Latest Updates" scan — do not apply exhaustive/iterate-until-dry searching here (see `framework/news-check.md` §A).
2. **`framework/latest-updates-workflow.md`** (Section F) and its §16 Tripwire/Edge assessment step — the analytical procedure for this task.
3. **`framework/news-check.md`** — the shared research method (§A: parallel sub-agents, source quality, first-run window) and run-summary format (§B). Both the daily watch and ad-hoc "what's new" checks use it.
4. **This file** — the operational checklist that applies Section F to this repo's file layout (how to read each ticker file, tag, append the news log, commit).

These are small, purpose-scoped files — read them directly. If any framework file is missing from the checkout, STOP and report it rather than proceeding on a remembered version.

## Research method
Use the agentic **parallel research sub-agent** method defined in **[`framework/news-check.md`](framework/news-check.md) §A** — for the daily watch, dispatch **one sub-agent per ticker (IBIDY, WYFI, LPKF), all in parallel** in a single dispatch. That file also carries the self-contained sub-agent prompt requirements, the source-quality guidance, and the first-run (~14-day) window. Do not restate it here.

## Task
For the tickers under `tickers/` (IBIDY, WYFI, LPKF):

1. **Dispatch the three sub-agents in parallel** (via the Task/Agent tool), one per ticker, per the Research method (`news-check.md` §A). Each one reads its own ticker file (noting Edge, numbered Tripwires, thesis context) and does the research pass, reporting back full-detail dated findings (not condensed) assessed against that ticker's actual Tripwires/Edge.
2. **Wait for all three to complete, then synthesize.**
3. **Categorize** each material event the sub-agents found against the framework sections (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Use a short `[TAG]`.
4. **Assess against the Tripwire and Edge — MANDATORY** (per Section F step 4):
   - **Tripwire:** does the event match, or move materially toward, any numbered tripwire? If yes → tag `[TRIPWIRE]`, name which trigger fired and how close to its threshold, and state the pre-committed action (exit / re-underwrite). This is the highest-priority finding — surface it at the TOP of the run summary, not buried.
   - **Edge:** does the event support or undermine the variant view? Tag `[EDGE+]` (corroborates) or `[EDGE−]` (consensus was right / edge eroding). An accumulation of `[EDGE−]` items means the differentiated thesis is failing even if no single tripwire fired — say so.
5. **Append full-detail, dated items** to that ticker file's `## Recent News Log`, most recent first. Do NOT compress to a vague one-liner — carry over the sub-agent's full substantive detail (exact figures, named counterparties/sources, deal terms) into the entry itself. One entry per distinct event — split a multi-fact disclosure (e.g. an earnings call covering several separate items) into separate entries, each independently categorized and tagged, rather than merging unrelated facts into one line. Lead the summary portion with a **bolded, one-line headline** so the entry is quickly scannable before the full detail. Format:
   `YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — **Headline**. Full detail of the event → impact/implication. Source: [Name1](URL1), [Name2](URL2) (<date>).`
   Each source is a markdown link to its direct URL (article/filing/press-release), not just a bare publication name — so the reader can click through and verify it themselves. If a source genuinely has no linkable URL (e.g. a paywalled terminal feed), write its name plain (no brackets) rather than fabricating or omitting it.
   Do NOT add "no news" placeholder entries. If a ticker's sub-agent found nothing material within window, leave that ticker's log unchanged.
6. **Commit & push** the updated ticker files with a message `daily watch: <today's date>` (only if something changed).
7. **Produce the run summary** — TRIPWIRES FIRST (see the Run summary section below).
8. **Per-ticker Edge & Tripwires recap — conditional on a hit** (see the Run summary section below).

## Run summary (the agent's output each day)
Produce the chat digest in the **canonical format defined in [`framework/news-check.md`](framework/news-check.md) §B** — TRIPWIRES FIRST, then edge shifts, then per-ticker headline+digest items, then the conditional Edge & Tripwires recap. That file is the single source of truth for this format and is shared with the ad-hoc "what's new / latest on [ticker]" workflow (`framework/latest-updates-workflow.md` step 7); do not restate it here. Run it across all tickers checked this run.

Rules: apply **all** of `framework/standing-rules.md` (Sections A + E) to every step above — do not work from a remembered summary. If any framework file under `framework/` is missing from the checkout, STOP and report it.
