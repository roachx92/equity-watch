# "Latest Updates" workflow

*Section F of the equity research framework — the analytical procedure for "what's new / latest on [ticker]" checks, including the mandatory §18 Tripwire/Edge assessment. Verbatim; relocated from the former single framework file. Read alongside `standing-rules.md` (Sections A + E), which binds every step here.*

> **Numbering note (July 2026 audit).** The Edge/Tripwire pre-investment checklist lives in the deep-dive's **Final thoughts & conclusion** section. That is **§18** in the current template (which grew to 18 sections); reports published **before the July 2026 gold-standard audit carry the same checklist at §16**, and the ticker news.md files correctly cite §16 against those existing reports. Follow the section *name*, not the number, when they disagree.

---

## F. "Latest Updates" workflow

*Triggered by requests like "latest on [ticker]," "what's new with X," "any updates on X."*

1. **Check whether a full framework report already exists** for the ticker (`tickers/<TICKER>/reports/<YYYY-MM-DD>.md`, with the Edge/Tripwires mirrored into the ticker's news.md at `tickers/<TICKER>/news.md`).
   - If not: **build the full report first** (per `deep-dive-template.md`, written as a dated markdown report at `tickers/<TICKER>/reports/<YYYY-MM-DD>.md`), create the ticker's folder and news.md, derive the §18 Edge/Tripwires into it, then continue.
2. **Search for recent news/events** tied to the stock since the last dated entry in the ticker's Recent News Log (or since report creation, if this is the first check) — using the agentic **parallel research sub-agent** method in [`news-check.md`](news-check.md) §A (self-contained sub-agent prompts, source-quality guidance, first-run ~14-day window). Don't research single-threaded — dispatch a thorough sub-agent pass on the ticker (or several in parallel split by research angle) for the same search quality the daily watch uses.
3. **Categorize each event against the framework's own sections** — Business model, Catalysts, Re-rate drivers, Moat/Competition, Technological moat/competing tech, Secular positioning, Financials/Capital stack, Risks/Concentration/Geopolitics, Bull/Base/Bear, Bottleneck fit, Sentiment, Asymmetry, Management/Insider activity, Valuation multiples, Investment thesis — to gauge which part of the thesis it actually touches.
4. **Assess every event against the §18 Tripwire and Edge — MANDATORY.** For each piece of news, explicitly ask:
   - **Does it trip the Tripwire?** Does the event match (or move materially toward) any of the pre-committed exit/re-underwrite triggers named in the ticker's Edge/Tripwires (in the ticker's news.md, `tickers/<TICKER>/news.md`, restated verbatim from the deep-dive report's §18)? If yes, this is the highest-priority finding: **flag it prominently at the top of the chat reply AND in the Recent News Log entry**, tag the entry **[TRIPWIRE]**, state which specific trigger fired and how close it is to the stated threshold, and note the pre-committed action (exit / re-underwrite). Never bury a tripwire event inside a routine news list.
   - **Does it strengthen or weaken the Edge?** Does the event support or undermine the differentiated/variant view the thesis rests on (§18 "Your edge")? Tag it **[EDGE+]** if it corroborates the variant view, **[EDGE−]** if it cuts against it (i.e., consensus was right and your edge is eroding). An accumulation of EDGE− items means the differentiated thesis is failing even if no single tripwire has fired — say so explicitly.
   - If the ticker's news.md has no §18 Tripwire/Edge on file yet, **derive them first** (per §18, from the deep-dive report) before assessing, and note that you did.
5. **If there's substantive, dated news:** append it to the ticker's `## Recent News Log` per **§F.1 below — the canonical entry format**. Do not restate or paraphrase that spec here or anywhere else; apply it as written.
6. **If nothing substantial turns up:** say so in the chat reply — do **not** add a placeholder or "no news" entry to the ticker's news.md. Keep the log clean. (Still state explicitly that you checked the news against the Tripwire and Edge and nothing fired — a clean check is itself a useful, reassuring result.)
7. **End with a run summary.** Produce the chat-reply digest in the **canonical format defined in [`news-check.md`](news-check.md) §B** — the same format the scheduled daily watch produces, so a one-off check and the automated run read identically (just scoped to the ticker(s) asked about).

*Note: this presupposes a full deep-dive report (and therefore the ticker's news.md §18 Edge/Tripwires) already exists — see step 1. If starting fresh without it, build the report first and derive the Edge/Tripwires, then continue.*

---

## F.1 Recent News Log — canonical entry format (SINGLE SOURCE OF TRUTH)

*The one authoritative spec for **how a news item gets written into a ticker's news.md**. **Both** entry points use it verbatim — the scheduled daily watch (`daily-watch.md` step 5) and the ad-hoc "what's new" check (Section F step 5 above). **Edit here only.** The other files reference this section; they do not restate it. (Companion specs live in [`news-check.md`](news-check.md): §A how to research the news, §B how to report it in the chat digest. This section covers the third thing — how it gets stored.)*

### Where it goes

- **Append to the `## Recent News Log` in the ticker's news.md — `tickers/<TICKER>/news.md` — most recent first.** Each watched ticker is a **folder** under `tickers/`, named for the symbol, holding that ticker's `news.md` (thesis context, Edge, numbered Tripwires, and the living log). The folder is the unit of the watch-list; the news.md is its state.
- **Never to the deep-dive report.** `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` is a dated point-in-time snapshot and is immutable once published; ongoing news accumulates **only** in the ticker's news.md.
- **Never add "no news" placeholder entries.** If a ticker's research pass found nothing material within the window, leave that ticker's log unchanged. A clean check gets reported in the chat digest, not written to the file.

### Format

```
YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — **Headline**. Full detail of the event → impact/implication. Source: [Name1](URL1), [Name2](URL2) (<date>).
```

- **`YYYY-MM-DD`** — the event's date, not the run date.
- **`[FRAMEWORK-TAG]`** — the framework section the event actually touches (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Short tag.
- **`[TRIPWIRE]` / `[EDGE+]` / `[EDGE−]`** — per the mandatory assessment in step 4 above. Include only when one applies.
- **Headline** — bolded, one line, leads the summary portion so the entry is scannable before the full detail.

### Content rules

- **Full detail — do NOT compress to a vague one-liner.** Carry the research pass's full substantive detail *into the entry itself*: exact figures, named counterparties, named sources, deal terms. The log entry must stand on its own without the reader going back to the source; a gloss like "reported strong results" is a failure of this rule.
- **One entry per distinct event.** Split a multi-fact disclosure — an earnings call covering several separate items, say — into **separate entries**, each independently dated, categorized, and tagged. Never merge unrelated facts into one line to save space.
- **State the implication, not just the fact.** The `→ impact/implication` clause is mandatory: what this does to the thesis.

### Sources

- **Every source is a markdown link to its direct URL** — the actual article, filing, or press release, so the reader can click through and verify it themselves. A bare publication name is not a citation.
- **No linkable URL** (e.g. a paywalled terminal feed): write the name plain, without brackets, and say so — never fabricate a URL, and never drop the attribution silently.
- Multiple sources are comma-separated; the trailing `(<date>)` is the publication date.

### Tripwire escalation

If any entry carries `[TRIPWIRE]`, it must **also** surface at the top of the chat digest as a headline callout (per [`news-check.md`](news-check.md) §B) — naming which numbered trigger fired, how close it sits to its stated threshold, and the pre-committed action (exit / re-underwrite). Never let a tripwire exist only inside the log, and never bury it in a routine news list.
