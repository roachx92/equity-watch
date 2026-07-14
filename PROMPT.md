# Daily routine prompt

You are running the daily "What's New" equity watch. Today's date is the current date — search for the latest, never answer present-day facts from memory.

This repository has been cloned into your workspace. Do this:

1. Read `WORKFLOW.md` — follow it exactly.
2. For each file in `tickers/` (IBIDY.md, WYFI.md, LPKF.md): read its Edge and Tripwires, search for news on that company since the last dated entry in its Recent News Log (or the last ~48h if empty), and assess every material item against the framework sections AND against that ticker's Tripwires and Edge.
3. Tag anything that fires: `[TRIPWIRE]` (name which trigger + how close to threshold + pre-committed action), `[EDGE+]`/`[EDGE−]` (supports/undermines the variant view).
4. Append substantive, dated items to each ticker's `## Recent News Log` (most recent first, per the WORKFLOW format). No "no news" placeholders. Never fabricate; cite sources; date everything; separate contracted vs recognized revenue.
5. If any ticker file changed, commit all changes with message `daily watch: <today's date>` and push to the default branch.
6. End with a run summary, **TRIPWIRES FIRST**: a 🚨 line listing any tripwire hits across all tickers (or "none today"), then any edge shifts, then 0-3 bullets of material news per ticker. If a tripwire fired, lead the summary with it.

Be concise and evidence-led. If a source can't be verified, say so rather than inventing.
