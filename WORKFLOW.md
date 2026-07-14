# Daily "What's New" Workflow (self-contained)

This is the workflow the daily agent runs. It is a condensed, self-contained version of Section F of the Equity Research Framework, with the mandatory Tripwire/Edge assessment.

For EACH ticker file under `tickers/` (IBIDY, WYFI, LPKF):

1. **Read the ticker file** — note its **Edge**, its numbered **Tripwires**, and its thesis context.
2. **Search for recent news/headlines** on the company since the last dated entry in its Recent News Log (or the last ~24-48h if the log is empty). Use reputable/primary sources; date every item; never fabricate — if nothing material, say so.
3. **Categorize** each material event against the framework sections (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Use a short `[TAG]`.
4. **Assess against the Tripwire and Edge — MANDATORY:**
   - **Tripwire:** does the event match, or move materially toward, any numbered tripwire? If yes → tag `[TRIPWIRE]`, name which trigger fired and how close to its threshold, and state the pre-committed action (exit / re-underwrite). This is the highest-priority finding — surface it at the TOP of the run summary, not buried.
   - **Edge:** does the event support or undermine the variant view? Tag `[EDGE+]` (corroborates) or `[EDGE−]` (consensus was right / edge eroding). An accumulation of `[EDGE−]` items means the differentiated thesis is failing even if no single tripwire fired — say so.
5. **Append** substantive, dated items to that ticker file's `## Recent News Log`, most recent first, format:
   `YYYY-MM-DD — [FRAMEWORK-TAG] [TRIPWIRE/EDGE± if any] — one-line summary → impact/implication.`
   Do NOT add "no news" placeholder entries. If nothing material, leave the log unchanged.
6. **Commit & push** the updated ticker files with a message like `daily watch: YYYY-MM-DD` (only if something changed).

## Run summary (the agent's output each day)
Produce a short digest, TRIPWIRES FIRST:
- **🚨 TRIPWIRES:** any `[TRIPWIRE]` hits across all tickers (or "none").
- **Edge shifts:** any `[EDGE+]/[EDGE−]` items.
- **Per-ticker:** 0-3 bullets of material news (or "nothing material").
- If a tripwire fired, the digest headline must say so.

Rules: search first (never answer present-day facts from memory); cite sources; date everything; separate contracted vs recognized; never fabricate; if a source is inaccessible, say so.
