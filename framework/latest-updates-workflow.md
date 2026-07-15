# "Latest Updates" workflow

*Section F of the equity research framework — the analytical procedure for "what's new / latest on [ticker]" checks, including the mandatory §16 Tripwire/Edge assessment. Verbatim; relocated from the former single framework file. Read alongside `standing-rules.md` (Sections A + E), which binds every step here.*

---

## F. "Latest Updates" workflow

*Triggered by requests like "latest on [ticker]," "what's new with X," "any updates on X."*

1. **Check whether a full framework report already exists** for the ticker (`reports/<YYYY-MM-DD>/<TICKER>.md`, with the Edge/Tripwires mirrored into `tickers/<TICKER>.md`).
   - If not: **build the full report first** (per `deep-dive-template.md`, written as a dated markdown report in `reports/`), derive the §16 Edge/Tripwires into the ticker file, then continue.
2. **Search for recent news/events** tied to the stock since the last dated entry in the ticker's Recent News Log (or since report creation, if this is the first check).
3. **Categorize each event against the framework's own sections** — Business model, Catalysts, Re-rate drivers, Moat/Competition, Technological moat/competing tech, Secular positioning, Financials/Capital stack, Risks/Concentration/Geopolitics, Bull/Base/Bear, Bottleneck fit, Sentiment, Asymmetry, Management/Insider activity, Valuation multiples, Investment thesis — to gauge which part of the thesis it actually touches.
4. **Assess every event against the §16 Tripwire and Edge — MANDATORY.** For each piece of news, explicitly ask:
   - **Does it trip the Tripwire?** Does the event match (or move materially toward) any of the pre-committed exit/re-underwrite triggers named in the ticker's Edge/Tripwires (in `tickers/<TICKER>.md`, restated verbatim from the deep-dive report's §16)? If yes, this is the highest-priority finding: **flag it prominently at the top of the chat reply AND in the Recent News Log entry**, tag the entry **[TRIPWIRE]**, state which specific trigger fired and how close it is to the stated threshold, and note the pre-committed action (exit / re-underwrite). Never bury a tripwire event inside a routine news list.
   - **Does it strengthen or weaken the Edge?** Does the event support or undermine the differentiated/variant view the thesis rests on (§16 "Your edge")? Tag it **[EDGE+]** if it corroborates the variant view, **[EDGE−]** if it cuts against it (i.e., consensus was right and your edge is eroding). An accumulation of EDGE− items means the differentiated thesis is failing even if no single tripwire has fired — say so explicitly.
   - If the ticker file has no §16 Tripwire/Edge on file yet, **derive them first** (per §16, from the deep-dive report) before assessing, and note that you did.
5. **If there's substantive, dated news:** append it to the ticker's **`## Recent News Log` in `tickers/<TICKER>.md`** (most recent first) — **NOT** to the deep-dive report. The report (`reports/<YYYY-MM-DD>/<TICKER>.md`) is a point-in-time snapshot; ongoing news accumulates only in the ticker file's living log. Use the ticker-file entry format (date + `[framework category tag]` + any `[TRIPWIRE]/[EDGE+]/[EDGE−]` tag + bolded headline + full detail → impact + `Source: [Name](URL) (date)`). If any entry is a `[TRIPWIRE]`, also surface it in the chat reply as a headline callout, not just in the log.
6. **If nothing substantial turns up:** say so in the chat reply — do **not** add a placeholder or "no news" entry to the ticker file. Keep the log clean. (Still state explicitly that you checked the news against the Tripwire and Edge and nothing fired — a clean check is itself a useful, reassuring result.)
7. **End with a run summary.** Produce the chat-reply digest in the **canonical format defined in [`run-summary-format.md`](run-summary-format.md)** — the same format the scheduled daily watch produces, so a one-off check and the automated run read identically (just scoped to the ticker(s) asked about).

*Note: this presupposes a full deep-dive report (and therefore the ticker file's §16 Edge/Tripwires) already exists — see step 1. If starting fresh without it, build the report first and derive the Edge/Tripwires, then continue.*
