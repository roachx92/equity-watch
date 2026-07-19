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
  stock already covered in tickers/ — even without the word "earnings". Also triggers on
  **retrieval** phrasing for an already-covered quarter — "pull <ticker> Q1'26 earnings", "show
  me <ticker>'s Q3 debrief", "what did the <ticker> Q2 digest say" — which **displays** that
  quarter's already-written chat output from earnings-debrief.md rather than re-running
  research (see Step 0.5: retrieval vs. fresh run). Writes the analysis to
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

## Step 0.5 — retrieval vs. fresh run
Before doing any research, decide which of these this request is:

- **Retrieval** — the user is asking to see/pull/recall a quarter that's **already written** in
  `tickers/<TICKER>/earnings-debrief.md` (e.g. "pull CIFR Q1'26 earnings," "show me LPKF's Q2
  debrief," "what did the Q3 digest say"). **Check the file first** — read its `## <FY period> —
  reported <date>` headings and match against the quarter named or implied. If it's there:
  **skip straight to rendering** — read that quarter's §1(f)/§2(e) "in brief" blocks and its §3
  Final Thoughts, and reproduce them as the chat reply in the exact §I.7 shape (lead line → Part
  1 in brief → Part 2 in brief → Final Thoughts → file link). **Do not dispatch sub-agents, do
  not re-research, do not rewrite the file, and do not run Step 6's Discord post** — a retrieval
  displays what's already on record; it isn't a new run and doesn't need to renotify the
  channel. Only post to Discord on retrieval if the user explicitly asks to.
- **Fresh run** — the named quarter is **not yet in the file** (a new print, or the ticker has no
  earnings-debrief.md at all), or the user is explicitly asking for a new/updated breakdown
  ("earnings digest on X," "break down X's call," "X just reported"). Proceed through Steps 1–6
  below in full.

If it's ambiguous which quarter is meant (e.g. just "pull CIFR earnings" with no quarter named
and multiple quarters on file), default to the **most recent** quarter in the file — most recent
first is the file's own ordering convention (§I.5).

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
3. **`framework/latest-updates-workflow.md`** — **two sections only**: **§F.2** for the sub-agent
   research method and source-quality guidance, including its non-US-filer note (§I.2 builds on
   it), and **§F.1** for the canonical Recent News Log entry format, used verbatim for the
   news.md half of the output (§I.5). **Do NOT use §F.3** — that is the what's-new run-summary
   format; the earnings chat reply has its own structure (§I.7).

## Step 2 — confirm the thesis exists (else build it first)
Per §I.1: a digest measures a call **against** something, and with nothing to measure against it
degrades into a summary. Check for `tickers/<TICKER>/news.md` carrying an **Edge** and numbered
**Tripwires**. **Resolve the actual latest report by globbing `tickers/<TICKER>/reports/*.md` and
sorting by date** (per CLAUDE.md's report-resolution rule) — don't just trust whatever the
news.md `Canonical deep-dive:` line says; if it's stale, refresh it as part of this run.
**If the name isn't covered yet, build the deep-dive first** (use the `deep-dive` skill), then
continue here. If the report exists but the news.md has no Edge/Tripwires, derive them first from
**that same latest report** you just resolved by glob — its Final thoughts & conclusion section —
and **state which dated report you used**. Never derive from the `Canonical deep-dive:` link or a
report you already had open: these become the binding pre-committed triggers, so seeding them from
a superseded snapshot installs a stale thesis as the baseline. **Assign the ticker's sector(s)** in a `## Sector lens` section per `framework/sector-lens.md` §K.1 — derived from that same report's §5/§6/§10 and anchored against its §18, with the transmission channel named per sector and slugs from the closed §K.2 vocabulary. **Write the tripwires as a
bullet list, one `- **(n)** ...` line per numbered trigger, not one dense paragraph** — split
a report's prose into one bullet per `(n)` as a formatting change only, never rewording,
dropping, or merging what a trigger says. **Append the `| # | Expires |`
table** (`framework/staleness-audit.md` §J.4) right after the tripwire bullets — one row per
numbered trigger, dated from the trigger's own text where it names a window, else ~12 months out
as a review horizon; the date is its own field, never spliced into the verbatim prose.

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
Emit the chat reply **per `framework/earnings-digest.md` §I.7**: it is assembled from the three
parts' own emoji-bullet summaries — a lead line (quarter, headline result vs. guide, net
assessment: thesis strengthened / weakened / unchanged), then **Part 1 in brief** (§I.3(f)),
**Part 2 in brief** (§I.4(e)), then the full **Final Thoughts** block (§I.6, all seven blocks),
then the link to the debrief file. The what's-new run-summary format (`latest-updates-workflow.md`
§F.3) is **not** used in the earnings chat reply. If any Tripwire fired, its 🚨 line leads the entire reply (§I.4(d) escalation). The full
analysis — the numbers, cash-conversion, sector cross-check, and four-part assessment — lives in
`earnings-debrief.md`, not the chat reply.

## Step 6 — post the digest to the ticker's Discord channel
Immediately after producing the run summary, post it to that ticker's Discord channel via
`scripts/notify_discord_ticker.py` — runs locally, right in the session, regardless of whether
anything was committed or pushed to GitHub.

```
python scripts/notify_discord_ticker.py --ticker <TICKER> --kind earnings-digest --date <today's-date> \
  --text-file <path-to-digest> [--tripwire-fired]   # if any [TRIPWIRE] hit this run — colors the embed red
```

- **`--kind earnings-digest` is mandatory** — the whats-new skill posts to this exact same
  per-ticker channel, so the embed title is the only thing that tells the two run types apart
  in the Discord feed. Pass `--date <today's-date>` so the title reads
  `<TICKER> — Earnings Digest (<date>)`.
- Write the exact chat reply produced in Step 5 to a scratch file and pass it via `--text-file`
  (or pipe it via stdin without that flag).
- Pass `--tripwire-fired` whenever any `[TRIPWIRE]` fired this run.
- **The script skips gracefully (exit 0, a one-line stderr note) if the ticker has no webhook
  configured** in `.secrets/discord-webhooks.json` (local, gitignored — see
  `.secrets/discord-webhooks.example.json` for the template). Don't treat this as a failure and
  don't block the chat reply on it.
- If it posts successfully, say so in one line at the end of the chat reply. If it skipped (not
  configured), don't mention Discord at all.

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
