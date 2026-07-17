---
name: earnings-digest
description: >-
  Break down a watched ticker's earnings call in this equity-watch repo into a retail-readable
  debrief — the reported numbers, cash conversion, management's read on sector demand
  (cross-checked against peers), what was quietly dropped from disclosure, and the market
  reaction decomposed — then assess it all against the ticker's investment thesis, re-rate
  drivers, risks, and pre-committed Edge/Tripwires. Use this whenever the user says "earnings
  digest on <TICKER>", "break down <ticker>'s earnings call", "what did <ticker> say on the
  call", "debrief <ticker> Q3", "<ticker> just reported", or asks what a print means for a
  stock already covered in tickers/ — even without the word "earnings". Writes the analysis to
  tickers/<TICKER>/earnings-debrief.md and the call's discrete news items to the ticker's
  news.md. Scoped to ONE reported quarter; for a general "what's new lately" scan use the
  whats-new skill, and for building a name's full 18-section report use the deep-dive skill.
---

# Earnings digest — one call, broken down and assessed against the thesis

This skill is a **launcher**, not a rulebook. This repo is the master for the research
framework, and the binding rule (`CLAUDE.md`) is: **apply the framework files as written —
never restate the rules from memory.** Read the canonical files below and execute the method
they define. If any is missing from the checkout, STOP and report it.

## Step 0 — establish today's date
Take today's date from the session's current-date context (do **not** infer it from training
data). Distinguish it from **the reporting date** — the digest is anchored to the quarter that
reported, which may be days earlier. Both get stamped: the reporting date on the quarter's
heading, today's date on the run/methodology line and the commit.

## Step 1 — read the canonical framework
Read these directly — do not work from memory of them:
1. **`framework/standing-rules.md`** — Sections A + E, binding on every step. Note the scope:
   this is a **bounded read of one event** against an already-built thesis, so Section A's
   "EXHAUSTIVE BY DEFAULT" diligence depth (which governs full reports) does **not** apply —
   §I.6 sets an explicit depth ceiling instead. Every other Section A rule applies in full,
   especially the numbers discipline (contracted vs. recognized, GAAP vs. non-GAAP, dilution)
   and the honest-counterweight mandate.
2. **`framework/earnings-digest.md`** — **Section I: the method.** §I.1 preconditions ·
   §I.2 the three sub-agents and their source ownership · §I.3 the five-part breakdown ·
   §I.4 the four-part assessment · §I.5 storage + the split with news.md + the Guidance
   track record table · §I.6 final thoughts and the depth ceiling · §I.7 the chat reply.
   This file is the single source of truth for the whole workflow — execute it, don't
   paraphrase it.
3. **`framework/news-check.md`** — **§A** for the sub-agent research method and source-quality
   guidance (§I.2 builds on it) and **§B** for the run-summary digest format (§I.7 emits it).
   Single source of truth for both — don't restate.
4. **`framework/latest-updates-workflow.md`** — **§F.1 only**: the canonical Recent News Log
   entry format, for the news.md half of the output (§I.5). Apply as written.

## Step 2 — confirm the thesis exists (else build it first)
Per §I.1: a digest measures a call **against** something, and with nothing to measure against it
degrades into a summary. Check for `tickers/<TICKER>/news.md` carrying an **Edge** and numbered
**Tripwires**, and the `tickers/<TICKER>/reports/<date>.md` it links. **If the name isn't covered yet,
build the deep-dive first** (use the `deep-dive` skill), then continue here. If the report exists
but the news.md has no Edge/Tripwires, derive them from the report's Final thoughts & conclusion
section first and say that you did.

Then read the thesis context you're assessing against — the ticker's news.md (quote the Edge and
Tripwires **verbatim**, never paraphrased), plus the deep-dive's thesis synthesis, re-rate map,
risks, and financials. And read the existing `earnings-debrief.md` if there is one: the prior
quarters are the baseline for the language-shift, disclosure-removal, and working-capital-trend
checks, and the Guidance track record table is the input to §I.4(a).

## Step 3 — dispatch the three sub-agents, in parallel, on Opus
Per §I.2: **do not research single-threaded**, and **pin the orchestrator and all three
sub-agents to Opus** (`model: opus`) — the synthesis is judgment-dense and a thin brief is
invisible to an orchestrator that can't audit it from the inside. Dispatch **Numbers** (8-K /
EX-99.1 / 10-Q, plus the working-capital block for this quarter **and the prior three**),
**Call** (prepared remarks + Q&A + this deck **and the prior quarter's deck, side by side**),
and **Sector cross-check** (peers, trade data, post-print sell-side reaction, and the peer/index
move needed to decompose the reaction) — each with the source ownership and report-back
requirements §I.2 specifies. Prompts must be **self-contained** (no memory of this conversation).
**Sub-agents research only — they must NOT edit files.** Wait for all three; the orchestrator
does every write itself.

**Primary documents override secondary commentary** (Section A). A digest built off a wire recap
of the print has failed §I.2. If the transcript or deck can't be accessed, say so plainly and
state what you used instead — never reconstruct remarks you didn't read.

## Step 4 — synthesize the digest, then write both artifacts
Execute §I.3 (breakdown) and §I.4 (assessment) as written — the tables are the rigor mechanism,
and the sub-headings stay **separate** so an empty bucket is visibly empty rather than silently
omitted. Then write **both** outputs per §I.5:
- **`tickers/<TICKER>/earnings-debrief.md`** — prepend the quarter, most recent first; never
  overwrite a prior quarter. Update the standing **Guidance track record** table in place (the
  one deliberate exception to the never-edit-history rule): add a row for any guide issued this
  print, fill the outcome columns for the period that just reported, delete nothing.
- **The ticker's `news.md` `## Recent News Log`** — the call's discrete dated news items, **split
  one entry per distinct event** (§F.1 names an earnings call as the example of a multi-fact
  disclosure to split), per the §F.1 format verbatim.
- **Commit** both (e.g. `earnings-digest: <TICKER> <FY period> <date>`).

**If a Tripwire fires**, escalate per §I.4(d): top of the chat reply, top of the debrief entry,
and tagged in the news.md log — naming which numbered trigger fired, how close it sits to its
threshold, and the pre-committed action. **Never silently rewrite an Edge or Tripwire** to
accommodate what a print just did; flag it and leave the re-underwrite as the reader's explicit
decision.

## Step 5 — produce the run summary
Emit the chat digest in the **canonical `news-check.md` §B format — TRIPWIRES FIRST**, scoped to
the one ticker, per §I.7. Add one lead line above it: the quarter, the headline result against
the guide, and the **net assessment** — thesis strengthened / weakened / unchanged. Then link the
debrief file. The full analysis lives in `earnings-debrief.md`, not the chat reply.

## Guardrails
- **Not financial advice** — flag it; this workflow is decision-shaped by construction.
  Informational research tooling only.
- **No unsolicited portfolio-fit, concentration, or position-sizing commentary** — request-only,
  per Section A.
- **Never fabricate** a figure, a quote, or a source. Paraphrase management; minimal quotes; no
  reproduction of transcript text. If a source has no linkable URL, name it plain and say so
  rather than omitting it silently.
- **Give the affirmative read AND the honest counterweight** — a digest of a good quarter that
  reads as a victory lap fails this as surely as one of a bad quarter that reads as a eulogy.
- **Write for the retail reader** who tracks the name: plain English, jargon defined on first
  use, mechanics kept straight (backlog is not revenue; a re-rate is multiple expansion, not
  price rising on revenue growth).
- **Respect the depth ceiling** (§I.6, ~2,000–3,000 words per quarter). If the call genuinely
  warrants re-underwriting the whole name, say so and run the `deep-dive` skill — don't let the
  debrief sprawl into one.
