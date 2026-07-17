# News check — research method (§A) & run-summary format (§B)

*The single shared spec for a "what's new" news check on one or more tickers. Used by BOTH the scheduled daily watch (`daily-watch.md`, across its ticker set) and the ad-hoc "what's new / latest on [ticker]" workflow (`latest-updates-workflow.md`, Section F). **Single source of truth for (A) how to research the news and (B) how to report it in the chat digest — edit here only; the two workflows reference this file, they do not restate it.** Apply all of `standing-rules.md` (Sections A + E) throughout.*

> **The third spec — how a news item gets STORED** (the `## Recent News Log` entry format in a ticker's news.md) — lives in **[`latest-updates-workflow.md`](latest-updates-workflow.md) §F.1**, not here. The full split: **§A research it · §B report it (chat digest) · F.1 store it (ticker's news.md).** Each has exactly one home; both entry points use all three.

---

## A. Research method — parallel research sub-agents

Do not research single-threaded — use the agentic, multi-agent pattern whether it's the daily watch or a one-off "what's new" request. **This is the quality bar for getting new info on a stock: parallel research sub-agents, not a single quick search.**
- **Multiple tickers (daily watch):** dispatch **one sub-agent per ticker, all in parallel** in a single dispatch (via the Task/Agent tool).
- **Single ticker ("what's new on X"):** dispatch a thorough research pass on that one ticker — one dedicated sub-agent, or several in parallel split by research angle (e.g. filings/financing vs. product/competitive vs. sentiment/positioning) when the question warrants depth.

Each sub-agent runs a thorough, multi-query pass — no fixed query cap; **typically 6-10+ distinct searches**, following threads, using WebFetch on primary sources where accessible. **Sub-agents research only — they must NOT edit any files.** Wait for all sub-agents to finish, then the orchestrator synthesizes every report and does all file writes itself. This mirrors the framework's Section H multi-agent pattern (`deep-dive-template.md`).

Each sub-agent's prompt must be self-contained (it has no memory of the parent conversation) and must include:
1. Today's date and the ticker/company name.
2. An instruction to `Read tickers/<TICKER>/news.md` first (the ticker's news.md — one folder per ticker under `tickers/`, the folder name is the symbol) and quote its exact Edge and numbered Tripwires verbatim (not from memory or paraphrase).
3. The search window: since the last dated entry in that ticker's Recent News Log, or **~14 days back if the log is empty** (see First-run window below).
4. The Source-quality guidance below.
5. An explicit hunt-list: one line per numbered Tripwire plus the Edge's specific mechanism, so the sub-agent searches for what would actually break or confirm the thesis, not just generic company news.
6. A report-back format: every material dated item with exact date + source name **with its direct URL** (the actual article/filing/press-release link, not just a publication name) + **full substantive detail** (figures, named parties, terms — not a vague gloss), each assessed against that ticker's actual Tripwires/Edge. If a source has no directly linkable URL (e.g. a paywalled terminal feed), say so explicitly rather than omitting the link silently.

Do not iterate to exhaustion beyond that, do not chase every tangential source, and do not re-verify facts already settled in the ticker's news.md thesis context. If a sub-agent's search turns up nothing material, that's a valid, complete result — don't force a finding. *(This bounded scan is distinct from a full "run the framework" deep dive, which IS exhaustive per Section A's Diligence-depth rule.)*

### Source quality
Favor primary/reputable sources — SEC EDGAR filings (10-K/10-Q/8-K/6-K), company press releases and IR pages, wire services (PR Newswire, Business Wire, GlobeNewswire, Reuters, Bloomberg), and established sector trade press (e.g. DigiTimes, TrendForce for semis). Quote-aggregator/data-only pages (Yahoo Finance quote, Google Finance, Investing.com quote, Morningstar quote, TradingView symbol page, CNBC quote, stockanalysis.com) carry price data but rarely article content — don't treat them as a source for a news item; run follow-up queries narrowed to a specific event type (e.g. "<ticker> 8-K", "<ticker> press release") instead. When using WebSearch, pass `blocked_domains` for these quote-only sites if the tool supports it.

### First-run window
If a ticker's Recent News Log is empty (first-ever check), search back **~14 days**, not just ~48h — a tight window on day one silently misses material context (a financing, a contract, a filing) that predates the check. Once the log has at least one dated entry, revert to the tight "since the last dated entry" window for all subsequent runs.

---

## B. Run-summary output format

Produce a short chat-reply digest that **leads with the actual news items found** — so the reader sees what's worth recording in the log before any assessment — then gives the tripwire/edge assessment beneath. The full multi-paragraph detail lives in each ticker's `## Recent News Log` (in that **ticker's news.md** — `tickers/<TICKER>/news.md`), not the chat reply — EXCEPT the Tripwires/Edge-shifts bullets below, which each get one detailed line per hit, not just a bare list.

**Escalation override — a fired tripwire always leads.** If any `[TRIPWIRE]` fired this run, put its 🚨 callout at the very TOP of the reply, above the items list — a fired tripwire is the highest-priority output and must never be buried under routine news. Absent a fired tripwire, the items list leads. Either way, when a tripwire fires the digest headline must say so.

Order of the digest:

- **Per-ticker items — FIRST.** List every substantive item found this run, one per item, most recent first, as a **headline + one-sentence abridged digest** — a step up from headline-only, but still NOT the full multi-clause paragraph (that stays in the ticker's news.md Recent News Log). Format — **the `[FRAMEWORK-TAG]` goes at the END of the line**, so the headline and its impact read first:
  `YYYY-MM-DD — **Headline**. One-sentence abridged digest of what happened → brief impact. [TRIPWIRE #n / EDGE+ / EDGE− if applicable] [FRAMEWORK-TAG]`
  Keep the digest to one sentence per item. If nothing material was found for a ticker, write "nothing material" instead of a list.
- **🚨 TRIPWIRES:** one bullet per `[TRIPWIRE]` hit (across every ticker checked this run), format:
  `**<TICKER> Tripwire #n — <status, e.g. "live, unresolved" / "early-warning" / "checked, does not fire">.** <one clause: what happened, why it matters, and the next test/date if still pending>.`
  If a ticker had no tripwire activity, a one-line `<TICKER>: none` is enough — don't pad it. If nothing fired anywhere, just say "none."
- **Edge shifts:** one bullet per `[EDGE+]/[EDGE−]` item (group same-direction items for one ticker into a single bullet if there are several), format:
  `**<TICKER> — EDGE+ / EDGE− / EDGE live test.** <one clause: what the item was, with its dated anchor>.`
  Omit a ticker entirely here if it had no edge activity — don't pad with "none."
- **Per-ticker Edge & Tripwires recap — conditional on a hit:** if the ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, restate (condensed, taken from the ticker's news.md, not memory) its current Edge one-liner and its numbered Tripwires, so the reader sees what fired against what's being watched. If nothing fired for that ticker this run, skip the full recap and give one line instead: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`

For a single-ticker "what's new" request this collapses naturally to that one ticker; for the daily watch it runs across every ticker checked.

> The daily watch persists this exact digest to `summaries/<date>.md` (with a
> frontmatter counts block) so a GitHub Action can post it to Discord. That is a
> delivery concern only — this section remains the single source of the digest
> format; the summary file body **is** this digest, unmodified.
