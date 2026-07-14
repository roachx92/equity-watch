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

## Search budget — this is a lightweight daily scan, not a full diligence pass
1-2 targeted searches per ticker is sufficient (e.g., one general news search + one follow-up only if the first surfaces something ambiguous that needs a date/number confirmed). Do NOT iterate to exhaustion, do NOT chase every tangential source, and do NOT re-verify facts that are already settled in the ticker file's thesis context. If a search turns up nothing material, move on — that is a valid, complete result for this workflow (see Section F step 6 / "if nothing turns up" in WORKFLOW.md).

## Task
For each file in `tickers/` (IBIDY.md, WYFI.md, LPKF.md):
1. Read its Edge and Tripwires and thesis context.
2. Search for news on that company since the last dated entry in its Recent News Log (or the last ~48h if empty) — per the search budget above.
3. Assess every material item against the framework sections AND that ticker's Tripwires and Edge (per Section F step 4). Tag: `[TRIPWIRE]` (name which trigger + how close to threshold + pre-committed action), `[EDGE+]`/`[EDGE−]`.
4. Append substantive, dated items to that ticker's `## Recent News Log` (most recent first, per WORKFLOW.md format). No "no news" placeholders.
5. If any file changed, commit all changes with message `daily watch: <today's date>` and push to the default branch.
6. End with a run summary, **TRIPWIRES FIRST**: a 🚨 line listing any tripwire hits across all tickers (or "none today"), then edge shifts, then 0-3 material-news bullets per ticker. If a tripwire fired, lead with it.
7. **Per-ticker Edge & Tripwires recap — conditional on a hit.** If that ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, include the full recap (a short restatement of its current Edge one-liner and its numbered Tripwires, taken verbatim/condensed from the ticker file — not from memory) so the reader sees exactly what fired against what's being watched. If the ticker had no such hit this run, replace the full recap with a single line: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`

Do not restate or paraphrase the standing rules from memory — apply them from the extracted `Equity_Research_Framework.md` sections as written. If that file is missing from the checkout, STOP and report it rather than proceeding on a remembered version.
