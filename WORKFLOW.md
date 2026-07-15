# Daily "What's New" Workflow (operational checklist)

This is the operational checklist for the daily agent. It applies **Section F** of `Equity_Research_Framework.md` to this repo's file layout. It does NOT restate the rules — the binding source is the framework file:

- **Standing rules** = `Equity_Research_Framework.md` **Section A** (search first; cite primary sources; never fabricate; date every figure; contracted vs recognized; honest counterweight; not financial advice). Apply them to every step below. If this checklist ever conflicts with Section A, **Section A wins**.
- **Workflow procedure** = `Equity_Research_Framework.md` **Section F** + its §16 Tripwire/Edge step. The steps below are just how to execute that against `tickers/*.md`.
- **Token budget:** don't `Read` the whole framework file — extract just Sections A and F (see `PROMPT.md` for the exact commands). Sections B–E, G, H are full-diligence-only content and are not needed here.
- **Research method — parallel per-ticker sub-agents.** This is no longer a single-threaded 1-2-query scan. Dispatch **one sub-agent per ticker, all in parallel** (via the Task/Agent tool, in a single dispatch), each running a thorough, multi-query research pass — no fixed query cap; typically 6-10+ distinct searches, following threads, using WebFetch on primary sources where accessible. Sub-agents research only — they must NOT edit any files. Wait for all sub-agents to finish, then the orchestrator synthesizes every report and does all file writes itself. This mirrors the framework's Section H multi-agent pattern, scaled to one agent per ticker instead of one per work-stream.

  Each sub-agent's prompt must be self-contained (it has no memory of anything above) and must include:
  1. Today's date and the ticker/company name.
  2. An instruction to `Read` `tickers/<TICKER>.md` first and quote its exact Edge and numbered Tripwires verbatim (not from memory or paraphrase).
  3. The search window: since the last dated entry in that ticker's Recent News Log, or **~14 days back if the log is empty** (see First-run window below).
  4. The Source-quality guidance below.
  5. An explicit hunt-list: one line per numbered Tripwire plus the Edge's specific mechanism, so the sub-agent searches for what would actually break or confirm the thesis, not just generic company news.
  6. A report-back format: every material dated item with exact date + source name/URL + **full substantive detail** (figures, named parties, terms — not a vague gloss), each assessed against that ticker's actual Tripwires/Edge.

- **Source quality:** favor primary/reputable sources — SEC EDGAR filings (10-K/10-Q/8-K/6-K), company press releases and IR pages, wire services (PR Newswire, Business Wire, GlobeNewswire, Reuters, Bloomberg), and established sector trade press (e.g. DigiTimes, TrendForce for semis). Quote-aggregator/data-only pages (Yahoo Finance quote, Google Finance, Investing.com quote, Morningstar quote, TradingView symbol page, CNBC quote, stockanalysis.com) carry price data but rarely article content — don't treat them as a source for a news item; run follow-up queries narrowed to a specific event type instead. When using WebSearch, pass `blocked_domains` for these quote-only sites if the tool supports it.
- **First-run window:** if a ticker's Recent News Log is empty (first-ever check), search back **~14 days**, not just ~48h — a tight window on day one silently misses material context (a financing, a contract, a filing) that predates the daily cadence. Once the log has at least one dated entry, revert to the tight "since the last dated entry" window for all subsequent runs.

For EACH ticker file under `tickers/` (IBIDY, WYFI, LPKF):

1. **Dispatch the three sub-agents in parallel**, one per ticker, per the Research method above. Each one reads its own ticker file (noting Edge, numbered Tripwires, thesis context) and does the research pass.
2. **Categorize** each material event the sub-agents found against the framework sections (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Use a short `[TAG]`.
3. **Assess against the Tripwire and Edge — MANDATORY:**
   - **Tripwire:** does the event match, or move materially toward, any numbered tripwire? If yes → tag `[TRIPWIRE]`, name which trigger fired and how close to its threshold, and state the pre-committed action (exit / re-underwrite). This is the highest-priority finding — surface it at the TOP of the run summary, not buried.
   - **Edge:** does the event support or undermine the variant view? Tag `[EDGE+]` (corroborates) or `[EDGE−]` (consensus was right / edge eroding). An accumulation of `[EDGE−]` items means the differentiated thesis is failing even if no single tripwire fired — say so.
4. **Append full-detail, dated items** to that ticker file's `## Recent News Log`, most recent first. Do NOT compress to a vague one-liner — carry over the sub-agent's full substantive detail (exact figures, named counterparties/sources, deal terms) into the entry itself. One entry per distinct event — split a multi-fact disclosure (e.g. an earnings call covering several separate items) into separate entries, each independently categorized and tagged, rather than merging unrelated facts into one line. Lead the summary portion with a **bolded, one-line headline** so the entry is quickly scannable before the full detail. Format:
   `YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — **Headline**. Full detail of the event → impact/implication. Source: <name(s)> (<date>).`
   Do NOT add "no news" placeholder entries. If a ticker's sub-agent found nothing material within window, leave that ticker's log unchanged.
5. **Commit & push** the updated ticker files with a message like `daily watch: YYYY-MM-DD` (only if something changed).

## Run summary (the agent's output each day)
Produce a short digest, TRIPWIRES FIRST. The full multi-paragraph detail lives in each ticker's Recent News Log (step 4), not the chat reply — EXCEPT the Tripwires/Edge-shifts bullets below, which each get one detailed line per hit, not just a bare list:
- **🚨 TRIPWIRES:** one bullet per `[TRIPWIRE]` hit across all tickers, format:
  `**<TICKER> Tripwire #n — <status, e.g. "live, unresolved" / "early-warning" / "checked, does not fire">.** <one clause: what happened, why it matters, and the next test/date if still pending>.`
  If a ticker had no tripwire activity this run, a one-line `<TICKER>: none` is enough — don't pad it. If nothing fired anywhere, just say "none."
- **Edge shifts:** one bullet per `[EDGE+]/[EDGE−]` item (group same-direction items for one ticker into a single bullet if there are several), format:
  `**<TICKER> — EDGE+ / EDGE− / EDGE live test.** <one clause: what the item was, with its dated anchor>.`
  Omit a ticker entirely here if it had no edge activity — don't pad with "none."
- **Per-ticker:** list every substantive item found this run as a **headline-only** line, one per item, most recent first — do NOT repeat the full summary/impact text here (that stays in the ticker file). Format:
  `YYYY-MM-DD — [FRAMEWORK-TAG] — **Headline**. [TRIPWIRE #n / EDGE+ / EDGE− if applicable]`
  If nothing material was found for a ticker, write "nothing material" instead of a list.
- **Per-ticker Edge & Tripwires recap — conditional on a hit:** if the ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, restate (condensed, taken from the ticker file, not memory) its current Edge one-liner and its numbered Tripwires, so the reader sees what fired against what's being watched. If nothing fired for that ticker this run, skip the full recap and give one line instead: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`
- If a tripwire fired, the digest headline must say so.

Rules: apply **all** of `Equity_Research_Framework.md` Section A to every step above — do not work from a remembered summary. If `Equity_Research_Framework.md` is missing from the checkout, STOP and report it.
