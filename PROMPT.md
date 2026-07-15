# Daily routine prompt

You are running the daily "What's New" equity watch. Search for the latest — never answer present-day facts from memory. This repository has been cloned into your workspace.

**First, establish today's date** from the session's current-date context (do not guess or infer it from memory/training data). Use that exact date throughout this run: as the anchor for "since the last dated entry" / "last ~48h" news searches, as the date stamped on every log entry and every source citation, and in the commit message (`daily watch: <today's date>`) and the run summary.

## Order of authority — TOKEN-BUDGET NOTICE: extract, do not read the whole file
`Equity_Research_Framework.md` is a large, multi-purpose document (~210 lines) that also carries the mandatory sub-agent prompt templates for FULL diligence runs (Sections G, H) and the full 16-section report template (Section B) — none of that is needed for this daily scan. **Do not `Read` the whole file.** Instead, run these two extraction commands and treat ONLY their output as binding:

```
awk '/^## A\./{f=1} /^## B\./{f=0} f' Equity_Research_Framework.md
awk '/^## F\./{f=1} /^## G\./{f=0} f' Equity_Research_Framework.md
```

1. **The Section A output (Standing rules)** — BINDING, applies to every step and every sentence you produce: search before answering anything time-sensitive; ground claims in primary/reputable sources and cite them; never fabricate (if unverifiable or a source is inaccessible, say so); date every point-in-time figure; separate contracted/backlog from recognized revenue; label fact vs estimate vs opinion; give the honest counterweight; not financial advice. If anything below appears to conflict with this, Section A wins. **Exception — scope it correctly:** Section A's "Diligence depth — EXHAUSTIVE BY DEFAULT" subsection is explicitly scoped (in its own text) to full report construction (triggered by "run the framework on [TICKER]"), NOT to this daily "Latest Updates" scan. See the search-budget note below — do not apply exhaustive/iterate-until-dry searching here.
2. **The Section F output ("Latest Updates" workflow)** and its §16 Tripwire/Edge assessment step — the analytical procedure for this task.
3. **`WORKFLOW.md`** — the operational checklist that applies Section F to this repo's file layout (how to read each ticker file, tag, append the news log, commit).

## Research method — parallel per-ticker sub-agents
Do not do this research single-threaded. Dispatch **one sub-agent per ticker (IBIDY, WYFI, LPKF), all three in parallel, in a single dispatch**, via the Task/Agent tool. Each sub-agent runs a thorough, multi-query research pass — no fixed cap, typically 6-10+ distinct searches, following up on threads and using WebFetch on primary sources where accessible. Sub-agents research only; they must NOT edit any files. Wait for all three to complete, then synthesize their reports yourself and do all file writes.

Each sub-agent's prompt must be self-contained (it has no memory of this conversation) and must include: today's date; an instruction to `Read tickers/<TICKER>.md` first and quote its exact Edge and numbered Tripwires verbatim; the search window (since the last dated Recent News Log entry, or ~14 days back if empty — see First-run window below); the Source-quality guidance below; an explicit hunt-list of one line per numbered Tripwire plus the Edge's specific mechanism (search for what would actually break or confirm the thesis, not generic company news); and a report-back format requiring every material dated item with exact date, source name/URL, and **full substantive detail** (figures, named parties, terms — not a vague gloss), each assessed against that ticker's actual Tripwires/Edge. Do not iterate to exhaustion beyond that, do not chase every tangential source, and do not re-verify facts already settled in the ticker file's thesis context. If a sub-agent's search turns up nothing material, that's a valid, complete result (see Section F step 6 / "if nothing turns up" in WORKFLOW.md) — don't force a finding.

## Source quality
Favor primary/reputable sources: SEC EDGAR filings (10-K/10-Q/8-K/6-K), company press releases and IR pages, wire services (PR Newswire, Business Wire, GlobeNewswire, Reuters, Bloomberg), and established sector trade press. Quote-aggregator/data-only pages (Yahoo Finance quote, Google Finance, Investing.com quote, Morningstar quote, TradingView symbol page, CNBC quote, stockanalysis.com) carry price data but rarely article content — don't cite them as the source for a news item. If a WebSearch call returns mostly these, run the one follow-up allowed by the search budget narrowed to a specific event type (e.g. "<ticker> 8-K", "<ticker> press release").

## First-run window
If a ticker's Recent News Log is empty (first-ever check), search back **~14 days**, not just ~48h, so material context that predates the daily cadence isn't silently missed. Once the log has at least one dated entry, use the tight "since the last dated entry" window for all subsequent runs.

## Task
1. Dispatch three sub-agents in parallel (via the Task/Agent tool), one per ticker (IBIDY.md, WYFI.md, LPKF.md) — per the Research method above. Each reads its own ticker file and reports back full-detail dated findings (not condensed) assessed against that ticker's actual Tripwires/Edge.
2. Wait for all three to complete, then synthesize.
3. For each ticker, assess every material item the sub-agent found against the framework sections AND that ticker's Tripwires and Edge (per Section F step 4). Tag: `[TRIPWIRE]` (name which trigger + how close to threshold + pre-committed action), `[EDGE+]`/`[EDGE−]`.
4. Append full-detail, dated items to that ticker's `## Recent News Log` (most recent first, per WORKFLOW.md format) — carry over the sub-agent's exact figures, named parties, and terms, don't paraphrase down to a vague one-liner; one entry per distinct event; lead each entry's summary with a **bolded, one-line headline** for quick scanning. No "no news" placeholders.
5. If any file changed, commit all changes with message `daily watch: <today's date>` and push to the default branch.
6. End with a run summary, **TRIPWIRES FIRST**. The full multi-paragraph detail belongs in the ticker files (step 4), not the chat reply — EXCEPT the 🚨 Tripwires and Edge-shifts bullets, which each get one detailed line per hit (ticker + tripwire # + status word + a one-clause explanation of what happened / why it matters / next test date if pending — see WORKFLOW.md's Run summary section for the exact format), not just a bare list. After that, every substantive item per ticker as a headline + one-sentence abridged digest line: `YYYY-MM-DD — [FRAMEWORK-TAG] — **Headline**. One-sentence abridged digest → brief impact. [TRIPWIRE/EDGE± if applicable]` (one sentence only — the full multi-clause detail stays in the ticker file). If a tripwire fired, lead with it.
7. **Per-ticker Edge & Tripwires recap — conditional on a hit.** If that ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, include the full recap (a short restatement of its current Edge one-liner and its numbered Tripwires, taken verbatim/condensed from the ticker file — not from memory) so the reader sees exactly what fired against what's being watched. If the ticker had no such hit this run, replace the full recap with a single line: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`

Do not restate or paraphrase the standing rules from memory — apply them from the extracted `Equity_Research_Framework.md` sections as written. If that file is missing from the checkout, STOP and report it rather than proceeding on a remembered version.
