# Daily routine prompt

You are running the daily "What's New" equity watch. Search for the latest — never answer present-day facts from memory. This repository has been cloned into your workspace.

**First, establish today's date** from the session's current-date context (do not guess or infer it from memory/training data). Use that exact date throughout this run: as the anchor for "since the last dated entry" / "last ~48h" news searches, as the date stamped on every log entry and every source citation, and in the commit message (`daily watch: <today's date>`) and the run summary.

## Order of authority (read these first, in this order)
1. **`Equity_Research_Framework.md` → Section A (Standing rules).** These are BINDING and apply to every step and every sentence you produce: search before answering anything time-sensitive; ground claims in primary/reputable sources and cite them; never fabricate (if unverifiable or a source is inaccessible, say so); date every point-in-time figure; separate contracted/backlog from recognized revenue; label fact vs estimate vs opinion; give the honest counterweight; not financial advice. If anything below appears to conflict with Section A, Section A wins.
2. **`Equity_Research_Framework.md` → Section F ("Latest Updates" workflow)** and its §16 Tripwire/Edge assessment step — the analytical procedure.
3. **`WORKFLOW.md`** — the operational checklist that applies Section F to this repo's file layout (how to read each ticker file, tag, append the news log, commit).

## Task
This routine currently checks **`tickers/LPKF.md` only** (IBIDY.md and WYFI.md remain in `tickers/` as monitoring files but are out of scope for this scheduled routine until re-enabled):
1. Read its Edge and Tripwires and thesis context.
2. Search for news on the company since the last dated entry in its Recent News Log (or the last ~48h if empty).
3. Assess every material item against the framework sections AND its Tripwires and Edge (per Section F step 4). Tag: `[TRIPWIRE]` (name which trigger + how close to threshold + pre-committed action), `[EDGE+]`/`[EDGE−]`.
4. Append substantive, dated items to its `## Recent News Log` (most recent first, per WORKFLOW.md format). No "no news" placeholders.
5. If the file changed, commit with message `daily watch: <today's date>` and push to the default branch.
6. End with a run summary, **TRIPWIRES FIRST**: a 🚨 line listing any tripwire hit (or "none today"), then edge shifts, then 0-3 material-news bullets. If a tripwire fired, lead with it.
7. **Include an Edge & Tripwires recap** in the summary (a short restatement of the current Edge one-liner and the numbered Tripwires, taken verbatim/condensed from the ticker file — not from memory) so the reader always sees what is being watched for, alongside what did or didn't fire this run.

Do not restate or paraphrase the standing rules from memory — apply them from `Equity_Research_Framework.md` as written. If that file is missing from the checkout, STOP and report it rather than proceeding on a remembered version.
