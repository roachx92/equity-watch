# "Latest Updates" workflow

*Section F of the equity research framework — the analytical procedure for "what's new / latest on [ticker]" checks, including the mandatory §16 Tripwire/Edge assessment. Verbatim; relocated from the former single framework file. Read alongside `standing-rules.md` (Sections A + E), which binds every step here.*

---

## F. "Latest Updates" workflow

*Triggered by requests like "latest on [ticker]," "what's new with X," "any updates on X."*

1. **Check whether a full framework report (Section B) already exists** for the ticker.
   - If not: **build the full report first** (Section B template, exported as the standard report artifact), then continue.
2. **Search for recent news/events** tied to the stock since the last update (or since report creation, if this is the first check).
3. **Categorize each event against the framework's own sections** — Business model, Catalysts, Re-rate drivers, Moat/Competition, Technological moat/competing tech, Secular positioning, Financials/Capital stack, Risks/Concentration/Geopolitics, Bull/Base/Bear, Bottleneck fit, Sentiment, Asymmetry, Management/Insider activity, Valuation multiples, Investment thesis — to gauge which part of the thesis it actually touches.
4. **Assess every event against the §16 Tripwire and Edge — MANDATORY.** For each piece of news, explicitly ask:
   - **Does it trip the Tripwire?** Does the event match (or move materially toward) any of the pre-committed exit/re-underwrite triggers named in the report's §16? If yes, this is the highest-priority finding: **flag it prominently at the top of the chat reply AND in the report**, tag the entry **[TRIPWIRE]**, state which specific trigger fired and how close it is to the stated threshold, and note the pre-committed action (exit / re-underwrite). Never bury a tripwire event inside a routine news list.
   - **Does it strengthen or weaken the Edge?** Does the event support or undermine the differentiated/variant view the thesis rests on (§16 "Your edge")? Tag it **[EDGE+]** if it corroborates the variant view, **[EDGE−]** if it cuts against it (i.e., consensus was right and your edge is eroding). An accumulation of EDGE− items means the differentiated thesis is failing even if no single tripwire has fired — say so explicitly.
   - If the report predates the §16 Tripwire/Edge additions and has none on file, **derive them first** (per §16) before assessing, and note that you did.
5. **If there's substantive, dated news:** add or append a **"Recent News"** section to the report. Each entry: **date** + brief summary + **[framework category tag]** + any **[TRIPWIRE]/[EDGE+]/[EDGE−]** tag + impact/implications commentary. Most recent first. If any entry is a **[TRIPWIRE]**, also surface it in the chat reply as a headline callout, not just inside the document.
6. **If nothing substantial turns up:** say so in the chat reply — do **not** add a placeholder or "no news" entry to the report itself. Keep the document clean. (Still state explicitly that you checked the news against the Tripwire and Edge and nothing fired — a clean check is itself a useful, reassuring result.)

7. **End with a run summary — same format as the daily watch.** The chat reply for a "what's new" request uses the identical structure the scheduled daily watch produces (so a one-off check and the automated run read the same way), just scoped to the ticker(s) asked about. **TRIPWIRES FIRST.** The full multi-paragraph detail lives in the report's Recent News section (step 5), not the chat reply — EXCEPT the Tripwires/Edge-shifts bullets below, which each get one detailed line per hit:
   - **🚨 TRIPWIRES:** one bullet per `[TRIPWIRE]` hit, format:
     `**<TICKER> Tripwire #n — <status, e.g. "live, unresolved" / "early-warning" / "checked, does not fire">.** <one clause: what happened, why it matters, and the next test/date if still pending>.`
     If the ticker had no tripwire activity, a one-line `<TICKER>: none` is enough. If nothing fired, just say "none."
   - **Edge shifts:** one bullet per `[EDGE+]/[EDGE−]` item (group same-direction items into a single bullet if there are several), format:
     `**<TICKER> — EDGE+ / EDGE− / EDGE live test.** <one clause: what the item was, with its dated anchor>.`
     Omit this line entirely if there was no edge activity — don't pad with "none."
   - **Items:** list every substantive item found, one per item, most recent first, as a **headline + one-sentence abridged digest** (a step up from headline-only, but NOT the full multi-clause paragraph — that stays in the report). Format:
     `YYYY-MM-DD — [FRAMEWORK-TAG] — **Headline**. One-sentence abridged digest of what happened → brief impact. [TRIPWIRE #n / EDGE+ / EDGE− if applicable]`
     If nothing material was found, write "nothing material" instead of a list.
   - **Edge & Tripwires recap — conditional on a hit:** if the ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, restate (condensed, taken from the report/ticker file, not memory) its current Edge one-liner and its numbered Tripwires, so the reader sees what fired against what's being watched. If nothing fired, skip the full recap and give one line instead: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`
   - If a tripwire fired, the digest headline must say so.

   (This is the same run-summary spec `daily-watch.md` applies across its ticker set — that file is just this format run automatically over multiple tickers. Keep the two in sync: a change to one should be mirrored in the other.)

*Note: this depends on the report artifact being available — either built earlier in the same session or re-shared by you in a new one. If starting fresh without the prior file, flag it and rebuild/re-attach as needed.*
