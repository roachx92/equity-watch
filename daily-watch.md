# Daily "What's New" equity watch

The self-contained operational procedure the scheduled routine runs each weekday. It applies **Section A + E** (standing rules & honest limits) and **Section F** (the "Latest Updates" workflow) of the framework to this repo's `tickers/<TICKER>/news.md` layout. It does NOT restate the rules — the binding source is the framework files under `framework/`.

**First, establish today's date** from the session's current-date context (do not guess or infer it from memory/training data). Use that exact date throughout this run: as the anchor for "since the last dated entry" / "last ~48h" news searches, as the date stamped on every log entry and every source citation, and in the commit message (`daily watch: <today's date>`) and the run summary.

## Order of authority
Read and apply, in this order of authority:

1. **`framework/standing-rules.md`** (Sections A + E) — BINDING on every step and every sentence you produce: search before answering anything time-sensitive; ground claims in primary/reputable sources and cite them; never fabricate (if unverifiable or a source is inaccessible, say so); date every point-in-time figure; separate contracted/backlog from recognized revenue; label fact vs estimate vs opinion; give the honest counterweight; not financial advice. If anything below appears to conflict with this, Section A wins. **Exception — scope it correctly:** Section A's "Diligence depth — EXHAUSTIVE BY DEFAULT" subsection is explicitly scoped (in its own text) to full report construction (triggered by "run the framework on [TICKER]"), NOT to this daily "Latest Updates" scan — do not apply exhaustive/iterate-until-dry searching here (see `framework/news-check.md` §A).
2. **`framework/latest-updates-workflow.md`** (Section F) — the analytical procedure for this task, including its §18 Tripwire/Edge assessment step and **§F.1, the canonical Recent News Log entry format** (the single source of truth for how a news item gets stored; this file does not restate it).
3. **`framework/news-check.md`** — the shared research method (§A: parallel sub-agents, source quality, first-run window) and run-summary format (§B). Both the daily watch and ad-hoc "what's new" checks use it.
4. **This file** — the operational checklist that applies Section F to this repo's file layout (which tickers to read, when to commit, and the run's ordering). The three spec files above own the *how*; this file owns the *sequence*.

These are small, purpose-scoped files — read them directly. If any framework file is missing from the checkout, STOP and report it rather than proceeding on a remembered version.

## Research method
Use the agentic **parallel research sub-agent** method defined in **[`framework/news-check.md`](framework/news-check.md) §A**. **Determine today's watch-list first:** enumerate the **ticker folders** under `tickers/` (e.g. `ls tickers/`) — that directory *is* the watch-list; every subfolder is a watched ticker, its folder name is the symbol, and its state lives in `tickers/<TICKER>/news.md`. There is no separate roster to keep in sync, and adding a ticker is "drop in a folder with a news.md." Skip any folder without a `news.md` (a half-created ticker) rather than failing the run — and say so in the run summary. Dispatch **one sub-agent per ticker folder found, all in parallel** in a single dispatch. `news-check.md` §A also carries the self-contained sub-agent prompt requirements, the source-quality guidance, and the first-run (~14-day) window. Do not restate them here.

## Task
For every ticker folder under `tickers/` (the watch-list enumerated in the Research method step above):

1. **Dispatch one sub-agent per ticker folder, all in parallel** (via the Task/Agent tool), one per ticker, per the Research method (`news-check.md` §A). Each one reads its own ticker's `news.md` (noting Edge, numbered Tripwires, thesis context) and does the research pass, reporting back full-detail dated findings (not condensed) assessed against that ticker's actual Tripwires/Edge.
2. **Wait for all of them to complete, then synthesize.**
3. **Categorize** each material event the sub-agents found against the framework sections (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Use a short `[TAG]`.
4. **Assess against the Tripwire and Edge — MANDATORY** (per Section F step 4):
   - **Tripwire:** does the event match, or move materially toward, any numbered tripwire? If yes → tag `[TRIPWIRE]`, name which trigger fired and how close to its threshold, and state the pre-committed action (exit / re-underwrite). This is the highest-priority finding — surface it at the TOP of the run summary, not buried.
   - **Edge:** does the event support or undermine the variant view? Tag `[EDGE+]` (corroborates) or `[EDGE−]` (consensus was right / edge eroding). An accumulation of `[EDGE−]` items means the differentiated thesis is failing even if no single tripwire fired — say so.
5. **Append full-detail, dated items** to that ticker's `news.md` `## Recent News Log` per the canonical entry format in **[`framework/latest-updates-workflow.md`](framework/latest-updates-workflow.md) §F.1** — the single source of truth for how a news item gets stored (where it goes, the format string, the full-detail and one-entry-per-event rules, source linking, and the no-placeholder rule). Read and apply it directly; it is not restated here.
6. **Produce the run summary** — the chat digest in the canonical §B format
   (`framework/news-check.md`), TRIPWIRES FIRST, including the conditional
   per-ticker Edge & Tripwires recap. This same digest is both your chat output
   and the body of the summary file in the next step.
7. **Write the summary file** — write the digest to `summaries/<today>.md`,
   prefixed with a YAML frontmatter block, then the verbatim §B digest body:

       ---
       date: <today>
       tickers_checked: <count of ticker folders under tickers/ scanned this run>
       tripwires_fired: <count of [TRIPWIRE] hits this run>
       edge_shifts: <count of [EDGE+]/[EDGE−] items this run>
       ---
       <the §B digest, exactly as produced in step 6>

   Write this file **every run**, even when nothing material was found (the body
   then carries the §B "nothing material" content and the counts are `0`) — it is
   the daily heartbeat that drives the Discord post. Do not restate the §B format
   here; `framework/news-check.md` §B is its single source.
8. **Commit & push** the updated `news.md` files **and** `summaries/<today>.md` with
   a message `daily watch: <today's date>`. Because the summary file is new every
   run, this commit always happens (unlike before, when it was skipped on a
   no-change day). The push triggers the Discord notification Action.

## Run summary (the agent's output each day)
Produce the chat digest in the **canonical format defined in [`framework/news-check.md`](framework/news-check.md) §B** — TRIPWIRES FIRST, then edge shifts, then per-ticker headline+digest items, then the conditional Edge & Tripwires recap. That file is the single source of truth for this format and is shared with the ad-hoc "what's new / latest on [ticker]" workflow (`framework/latest-updates-workflow.md` step 7); do not restate it here. Run it across all tickers checked this run. The same digest is persisted verbatim (with a frontmatter counts block) to `summaries/<today>.md` in step 7 above; a GitHub Action posts that file to Discord on push. The digest format remains defined only in `framework/news-check.md` §B.

Rules: apply **all** of `framework/standing-rules.md` (Sections A + E) to every step above — do not work from a remembered summary. If any framework file under `framework/` is missing from the checkout, STOP and report it.
