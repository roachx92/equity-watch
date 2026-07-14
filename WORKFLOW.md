# Daily "What's New" Workflow (operational checklist)

This is the operational checklist for the daily agent. It applies **Section F** of `Equity_Research_Framework.md` to this repo's file layout. It does NOT restate the rules — the binding source is the framework file:

- **Standing rules** = `Equity_Research_Framework.md` **Section A** (search first; cite primary sources; never fabricate; date every figure; contracted vs recognized; honest counterweight; not financial advice). Apply them to every step below. If this checklist ever conflicts with Section A, **Section A wins**.
- **Workflow procedure** = `Equity_Research_Framework.md` **Section F** + its §16 Tripwire/Edge step. The steps below are just how to execute that against `tickers/*.md`.
- **Token budget:** don't `Read` the whole framework file — extract just Sections A and F (see `PROMPT.md` for the exact commands). Sections B–E, G, H are full-diligence-only content and are not needed here.
- **Search budget:** this is a lightweight daily scan, not a full diligence pass. Section A's "exhaustive, don't stop early" diligence-depth rule is self-scoped to full report runs ("run the framework on [TICKER]") and does NOT apply to this daily check. 1-2 targeted searches per ticker is sufficient — do not iterate to exhaustion.

For EACH ticker file under `tickers/` (IBIDY, WYFI, LPKF):

1. **Read the ticker file** — note its **Edge**, its numbered **Tripwires**, and its thesis context.
2. **Search for recent news/headlines** on the company since the last dated entry in its Recent News Log (or the last ~24-48h if the log is empty), per the search budget above. Use reputable/primary sources; date every item; never fabricate — if nothing material, say so.
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
- **Per-ticker Edge & Tripwires recap:** for each ticker, restate (condensed, taken from the ticker file, not memory) its current Edge one-liner and its numbered Tripwires — so the reader always has "what to look for" in view, not just what fired. Include this even on a quiet day with no hits.
- If a tripwire fired, the digest headline must say so.

Rules: apply **all** of `Equity_Research_Framework.md` Section A to every step above — do not work from a remembered summary. If `Equity_Research_Framework.md` is missing from the checkout, STOP and report it.
