# Daily "What's New" equity watch

The self-contained operational procedure the scheduled routine runs each weekday. It applies **Section A + E** (standing rules & honest limits) and **Section F** (the "Latest Updates" workflow) of the framework to this repo's `tickers/*.md` layout. It does NOT restate the rules — the binding source is the framework files under `framework/`.

**First, establish today's date** from the session's current-date context (do not guess or infer it from memory/training data). Use that exact date throughout this run: as the anchor for "since the last dated entry" / "last ~48h" news searches, as the date stamped on every log entry and every source citation, and in the commit message (`daily watch: <today's date>`) and the run summary.

## Order of authority
Read and apply, in this order of authority:

1. **`framework/standing-rules.md`** (Sections A + E) — BINDING on every step and every sentence you produce: search before answering anything time-sensitive; ground claims in primary/reputable sources and cite them; never fabricate (if unverifiable or a source is inaccessible, say so); date every point-in-time figure; separate contracted/backlog from recognized revenue; label fact vs estimate vs opinion; give the honest counterweight; not financial advice. If anything below appears to conflict with this, Section A wins. **Exception — scope it correctly:** Section A's "Diligence depth — EXHAUSTIVE BY DEFAULT" subsection is explicitly scoped (in its own text) to full report construction (triggered by "run the framework on [TICKER]"), NOT to this daily "Latest Updates" scan. See the search-budget notes below — do not apply exhaustive/iterate-until-dry searching here.
2. **`framework/latest-updates-workflow.md`** (Section F) and its §16 Tripwire/Edge assessment step — the analytical procedure for this task.
3. **This file** — the operational checklist that applies Section F to this repo's file layout (how to read each ticker file, tag, append the news log, commit).

These are small, purpose-scoped files — read them directly. If any framework file is missing from the checkout, STOP and report it rather than proceeding on a remembered version.

## Research method — parallel per-ticker sub-agents
Do not do this research single-threaded. Dispatch **one sub-agent per ticker (IBIDY, WYFI, LPKF), all in parallel** (via the Task/Agent tool, in a single dispatch), each running a thorough, multi-query research pass — no fixed query cap; typically 6-10+ distinct searches, following threads, using WebFetch on primary sources where accessible. Sub-agents research only — they must NOT edit any files. Wait for all sub-agents to finish, then the orchestrator synthesizes every report and does all file writes itself. This mirrors the framework's Section H multi-agent pattern, scaled to one agent per ticker instead of one per work-stream.

Each sub-agent's prompt must be self-contained (it has no memory of this conversation) and must include:
1. Today's date and the ticker/company name.
2. An instruction to `Read tickers/<TICKER>.md` first and quote its exact Edge and numbered Tripwires verbatim (not from memory or paraphrase).
3. The search window: since the last dated entry in that ticker's Recent News Log, or **~14 days back if the log is empty** (see First-run window below).
4. The Source-quality guidance below.
5. An explicit hunt-list: one line per numbered Tripwire plus the Edge's specific mechanism, so the sub-agent searches for what would actually break or confirm the thesis, not just generic company news.
6. A report-back format: every material dated item with exact date + source name/URL + **full substantive detail** (figures, named parties, terms — not a vague gloss), each assessed against that ticker's actual Tripwires/Edge.

Do not iterate to exhaustion beyond that, do not chase every tangential source, and do not re-verify facts already settled in the ticker file's thesis context. If a sub-agent's search turns up nothing material, that's a valid, complete result (see Section F step 6 / "if nothing turns up" below) — don't force a finding.

## Source quality
Favor primary/reputable sources — SEC EDGAR filings (10-K/10-Q/8-K/6-K), company press releases and IR pages, wire services (PR Newswire, Business Wire, GlobeNewswire, Reuters, Bloomberg), and established sector trade press (e.g. DigiTimes, TrendForce for semis). Quote-aggregator/data-only pages (Yahoo Finance quote, Google Finance, Investing.com quote, Morningstar quote, TradingView symbol page, CNBC quote, stockanalysis.com) carry price data but rarely article content — don't treat them as a source for a news item; run follow-up queries narrowed to a specific event type (e.g. "<ticker> 8-K", "<ticker> press release") instead. When using WebSearch, pass `blocked_domains` for these quote-only sites if the tool supports it.

## First-run window
If a ticker's Recent News Log is empty (first-ever check), search back **~14 days**, not just ~48h — a tight window on day one silently misses material context (a financing, a contract, a filing) that predates the daily cadence. Once the log has at least one dated entry, revert to the tight "since the last dated entry" window for all subsequent runs.

## Task
For the tickers under `tickers/` (IBIDY, WYFI, LPKF):

1. **Dispatch the three sub-agents in parallel** (via the Task/Agent tool), one per ticker, per the Research method above. Each one reads its own ticker file (noting Edge, numbered Tripwires, thesis context) and does the research pass, reporting back full-detail dated findings (not condensed) assessed against that ticker's actual Tripwires/Edge.
2. **Wait for all three to complete, then synthesize.**
3. **Categorize** each material event the sub-agents found against the framework sections (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Use a short `[TAG]`.
4. **Assess against the Tripwire and Edge — MANDATORY** (per Section F step 4):
   - **Tripwire:** does the event match, or move materially toward, any numbered tripwire? If yes → tag `[TRIPWIRE]`, name which trigger fired and how close to its threshold, and state the pre-committed action (exit / re-underwrite). This is the highest-priority finding — surface it at the TOP of the run summary, not buried.
   - **Edge:** does the event support or undermine the variant view? Tag `[EDGE+]` (corroborates) or `[EDGE−]` (consensus was right / edge eroding). An accumulation of `[EDGE−]` items means the differentiated thesis is failing even if no single tripwire fired — say so.
5. **Append full-detail, dated items** to that ticker file's `## Recent News Log`, most recent first. Do NOT compress to a vague one-liner — carry over the sub-agent's full substantive detail (exact figures, named counterparties/sources, deal terms) into the entry itself. One entry per distinct event — split a multi-fact disclosure (e.g. an earnings call covering several separate items) into separate entries, each independently categorized and tagged, rather than merging unrelated facts into one line. Lead the summary portion with a **bolded, one-line headline** so the entry is quickly scannable before the full detail. Format:
   `YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — **Headline**. Full detail of the event → impact/implication. Source: <name(s)> (<date>).`
   Do NOT add "no news" placeholder entries. If a ticker's sub-agent found nothing material within window, leave that ticker's log unchanged.
6. **Commit & push** the updated ticker files with a message `daily watch: <today's date>` (only if something changed).
7. **Produce the run summary** — TRIPWIRES FIRST (see the Run summary section below).
8. **Per-ticker Edge & Tripwires recap — conditional on a hit** (see the Run summary section below).

## Run summary (the agent's output each day)
Produce a short digest, TRIPWIRES FIRST. The full multi-paragraph detail lives in each ticker's Recent News Log (step 5), not the chat reply — EXCEPT the Tripwires/Edge-shifts bullets below, which each get one detailed line per hit, not just a bare list:
- **🚨 TRIPWIRES:** one bullet per `[TRIPWIRE]` hit across all tickers, format:
  `**<TICKER> Tripwire #n — <status, e.g. "live, unresolved" / "early-warning" / "checked, does not fire">.** <one clause: what happened, why it matters, and the next test/date if still pending>.`
  If a ticker had no tripwire activity this run, a one-line `<TICKER>: none` is enough — don't pad it. If nothing fired anywhere, just say "none."
- **Edge shifts:** one bullet per `[EDGE+]/[EDGE−]` item (group same-direction items for one ticker into a single bullet if there are several), format:
  `**<TICKER> — EDGE+ / EDGE− / EDGE live test.** <one clause: what the item was, with its dated anchor>.`
  Omit a ticker entirely here if it had no edge activity — don't pad with "none."
- **Per-ticker:** list every substantive item found this run, one per item, most recent first, as a **headline + one-sentence abridged digest** — a step up from headline-only, but still NOT the full multi-clause paragraph (that stays in the ticker file). Format:
  `YYYY-MM-DD — [FRAMEWORK-TAG] — **Headline**. One-sentence abridged digest of what happened → brief impact. [TRIPWIRE #n / EDGE+ / EDGE− if applicable]`
  Keep the digest to one sentence per item. If nothing material was found for a ticker, write "nothing material" instead of a list.
- **Per-ticker Edge & Tripwires recap — conditional on a hit:** if the ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, restate (condensed, taken from the ticker file, not memory) its current Edge one-liner and its numbered Tripwires, so the reader sees what fired against what's being watched. If nothing fired for that ticker this run, skip the full recap and give one line instead: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`
- If a tripwire fired, the digest headline must say so.

Rules: apply **all** of `framework/standing-rules.md` (Sections A + E) to every step above — do not work from a remembered summary. If any framework file under `framework/` is missing from the checkout, STOP and report it.
