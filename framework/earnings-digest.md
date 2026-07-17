# Earnings digest workflow

*Section I of the equity research framework — the analytical procedure for breaking down a ticker's earnings call into a debrief a retail investor who already tracks the name can actually use. Read alongside [`standing-rules.md`](standing-rules.md) (Sections A + E), which binds every step here. The digest is stored in the ticker's **earnings-debrief.md** (`tickers/<TICKER>/earnings-debrief.md`); the discrete news items from the same call are stored in the ticker's news.md per [`latest-updates-workflow.md`](latest-updates-workflow.md) §F.1 — see §I.5 below for the split.*

> **Who this is for.** The reader already owns or tracks the ticker and has read the deep-dive. They are not an analyst. They want to know: *what was actually said, what does it change, and what do I watch next.* Write for that person — plain English, jargon defined on first use, mechanics kept straight (backlog is not revenue; a raised guide is not a beat). Depth is not the goal here; **fidelity and consequence are.** This is not a deep dive — see the depth ceiling in §I.6.

---

## I. Earnings digest workflow

*Triggered by requests like "earnings digest on [ticker]," "break down [ticker]'s earnings call," "what did [ticker] say on the call," "debrief [ticker] Q3."*

### I.1 Preconditions — the thesis you are assessing against must already exist

1. **Check for a canonical deep-dive** (`reports/<YYYY-MM-DD>/<TICKER>.md`) and the ticker's news.md (`tickers/<TICKER>/news.md`) carrying its **Edge** and numbered **Tripwires**.
   - If neither exists: **build the full report first** (per [`deep-dive-template.md`](deep-dive-template.md)), create the ticker folder and news.md, derive the Edge/Tripwires into it, then run the digest. A digest with nothing to assess against is a summary, and a summary is not this workflow's output.
   - If the report exists but the news.md has no Edge/Tripwires on file, derive them from the report's **Final thoughts & conclusion** section first, and say that you did.
2. **Read the context, don't recall it** — the ticker's news.md (quote the Edge and numbered Tripwires **verbatim**, not paraphrased), plus the canonical deep-dive's thesis synthesis, re-rate map, risks, and financials sections. These four are what the digest measures the call against; going from memory defeats the entire exercise.
3. **Identify the specific quarter** — fiscal period, reporting date, and whether this is the first digest for the ticker (start a new earnings-debrief.md) or an additional quarter (prepend — see §I.5).

### I.2 Source gathering — primary documents, dispatched in parallel

Apply the Section A sourcing rules in full: **primary documents override secondary commentary, and news summaries are a starting point, never the evidence.** An earnings digest built off a wire-service recap of the print has failed this step.

**Do not research single-threaded.** Dispatch **three parallel sub-agents** in a single dispatch (the [`news-check.md`](news-check.md) §A pattern — self-contained prompts, research-only, no file edits; the orchestrator waits for all three and does every write itself). **Pin all three and the orchestrator to Opus** (`model: opus`), per the model-pinning rule in `deep-dive-template.md` §B0.1 — the synthesis in §I.4 is judgment-dense, and a thin brief is invisible to an orchestrator that cannot audit it from the inside. Record the model used in the digest's methodology line; if a run was not Opus end-to-end, say so in the file as a quality caveat.

| Sub-agent | Sources it owns | What it must return |
|---|---|---|
| **Numbers** | SEC EDGAR — the 8-K and its **EX-99.1 earnings release**, the 10-Q/10-K filed for the period, prior-period filings for the comparison base | Every hard line item by hand: revenue and segment splits, GAAP **and** non-GAAP with the adjustment bridge, margins, cash-flow statement (OCF vs. PP&E capex vs. FCF, reconciled against each other), fully diluted share count, ATM/convert/SBC activity. **The full working-capital block** for this quarter *and the prior three*, so §I.3(b) has a trend and not a level: receivables/DSO (and any concentration within AR), inventory/DIO, payables/DPO, deferred revenue and backlog, cash. Accession numbers and filing dates on every figure. |
| **Call** | The earnings **call itself** — prepared remarks and, critically, the **Q&A** — plus the IR earnings presentation/deck **and the prior quarter's deck, read side by side** | Guidance issued, raised, cut, or conspicuously withheld, with management's stated reason. **Management's characterization of sector demand and market sentiment**, captured faithfully. What analysts pressed on, what got a direct answer, and **what got deflected or non-answered** — a dodged question is a finding, not an absence. Any language shift versus the prior quarter's call on the same topic. **Anything present in the prior deck/release and absent from this one** — a dropped metric, a segment no longer broken out, a KPI redefined or rebased (§I.3(d)). |
| **Sector cross-check** | Peers' recent prints and commentary, sector data/trade press, sell-side reaction *after* the print, the price/multiple reaction and positioning | Independent evidence bearing on management's sector claims — corroborating **or** contradicting. Whether peers describe the same demand environment. **The reaction decomposed** (§I.3(e)): the stock's move on the print, the peer group's and the relevant index's move over the same window, the name's beta if known, and any positioning/short-interest context — enough to separate the company-specific move from the sector tape. |

**Source quality** — apply `news-check.md` §A's guidance as written. Quote-aggregator pages are not a source for what was said on a call. **If the transcript or deck cannot be accessed, say so plainly in the digest and state what you used instead** — never reconstruct remarks you did not read (Section A: never fabricate).

### I.3 Part 1 — Breakdown of what was actually said

The first required output part. Two things, and the second is the one that usually gets skipped:

**(a) The reported numbers.** Ships as a table — the **Read** column is the analytical payload, and a digest written as prose has skipped the interpretation step. The **Δ** column is explicit and signed, against **both** anchors, because "beat" collapses two different facts into one word:

| Metric | Reported (dated) | Company guide going in | Consensus going in | Δ vs. guide / vs. consensus | YoY | Read — what it actually means |
|---|---|---|---|---|---|---|

Numbers discipline is not relaxed for a digest — apply Section A in full:
- [ ] **Actual vs. the guide vs. consensus, stated separately.** "Beat" is meaningless without saying beat *what*, and a beat against a guide the company cut last quarter is a different fact from a beat against the original.
- [ ] **GAAP vs. non-GAAP, with what the adjustments exclude.** Name the bridge. A non-GAAP profit next to a GAAP loss is the single most common retail misread and it belongs in the Read column, not a footnote.
- [ ] **Contracted / backlog / bookings vs. RECOGNIZED revenue.** Always state how much of any headline TCV or backlog figure has actually hit the income statement, and when the rest is guided to. Headline order announcements on a call are balance-sheet-adjacent, not revenue.
- [ ] **Dilution discipline.** Check the fully diluted share count and flag ATM usage, converts, or SBC disclosed with the print. A per-share figure that improved on a shrinking denominator is not an operating result.
- [ ] **CapEx vs. OpEx.** If cash burned, say whether it funded hard assets/R&D or just kept the lights on.
- [ ] **Date every point-in-time figure.** They move.
- [ ] **Flag headline optics distortion explicitly** — a one-time gain inflating a base, a guided decline that isn't operational, a segment mix shift doing the work the narrative credits to demand.

**(b) Cash conversion & working capital — MANDATORY, and read as a trend.** *Is the reported revenue turning into cash, and if not, where is it stuck?* This is the earliest fundamental warning the quarter offers: channel stuffing, demand pulled forward, a distributor being carried, and a customer quietly failing all appear in working capital **one to two quarters before they reach the income statement** — by which point the print that reveals them is a re-rate, not a warning. A digest that reads only the income statement finds these a quarter late, every time.

| Measure | This quarter | Prior 3 quarters | Direction | Read — benign or a warning? |
|---|---|---|---|---|

- [ ] **Minimum rows: DSO, DIO, DPO, the cash conversion cycle, and OCF vs. net income.** A level is not a finding — **give every one a direction** (Section A: "~35% of the high-end" is far less useful than a trend). Four quarters is the floor for calling one.
- [ ] **Net income up while OCF flat or negative is the headline finding of that quarter**, not a footnote. Say it in plain English: the company booked profit it has not collected.
- [ ] **Attribute any DSO extension to a named counterparty where the filings allow it.** "DSO rose 11 days" is a metric; "DSO rose 11 days and one private distributor is 74.5% of receivables on extended terms" is the thesis. Where a Tripwire watches a counterparty's channel, **this table is where it fires first** — carry the finding into §I.4(d) rather than leaving it here.
- [ ] **Inventory building faster than revenue** — state whose balance sheet the demand is really sitting on, and whether management addressed it on the call.
- [ ] **Reconcile against the deck's own narrative.** A "record demand" quarter with a lengthening cash conversion cycle is a contradiction the digest must name explicitly rather than report both facts and let them sit adjacent.

**(c) Management's read on the sector — MANDATORY, and cross-checked.** What management said about demand, pricing, competition, customer behavior, and sentiment in their sector — **paraphrased, minimally quoted** (Section A: no reproduction of copyrighted source text). This is not colour; it is often the most thesis-relevant content on the call, because it is where management's forward view is stated before it shows up in a filing. Ships as a table, because the third column is the whole point:

| What management said about the sector | Where (prepared remarks / Q&A / deck) | Independent check — does outside evidence agree? |
|---|---|---|

- [ ] **Label fact vs. estimate vs. opinion** (Section A). Management's demand characterization is an *interested party's opinion* until the sector agent corroborates it — mark it as such, and say plainly when peers describe a different environment.
- [ ] **Note the language shift versus last quarter's call** where one exists. "Strong demand" → "customers digesting inventory" is a material disclosure delivered as an adverb.
- [ ] **Record what was dodged.** Name the question and note that it went unanswered. Analysts ask about the same pressure points the Tripwires watch; a deflection there is evidence.

**(d) What management *didn't* say — MANDATORY.** The highest-signal-per-word content on any call, and the only part of it that requires the prior quarter's materials open alongside this one. **Disclosure is sticky: companies keep publishing a metric right up until it turns against them, then stop.** A KPI that vanishes from the deck is a disclosure event, and it is one the wire recaps will not carry, because nothing was announced. Ships as a table:

| What's missing | Last disclosed (quarter + figure) | Management's stated reason, if any | Read — why it likely went away |
|---|---|---|---|

Hunt for all four kinds:
- [ ] **A metric dropped from the deck or release** that appeared in the prior one — this is why the Call agent reads both decks side by side.
- [ ] **A segment or customer no longer broken out**, or rolled into an "other" line. Aggregation is how a deteriorating line stops being visible without anything being restated.
- [ ] **A KPI redefined, rebased, or re-scoped** — the same name over a different denominator is worse than a dropped metric, because it *looks* continuous. State the old and new definitions and, where the filings allow, restate the current quarter on the old basis.
- [ ] **A previously routine forward number withheld** — a guide not reissued, a target quietly dropped, a milestone date no longer repeated.

**Calibration, per Section A:** absence of evidence is not evidence of absence, and there are benign explanations (a genuine segment reorganization, immateriality, a metric that outlived its usefulness). **Take management's stated reason at face value and record it — then say whether the timing is consistent with it.** A metric retired the same quarter it would first have looked bad is a different fact from one retired at a fiscal-year boundary alongside a restructuring. Label the read as **opinion**, not fact, and where nothing is missing, **say that explicitly** — a clean check here is a genuinely reassuring result and belongs in the file.

**(e) The reaction, decomposed.** The stock's move on a print is only a fundamental datapoint once the sector's move is stripped out — otherwise the digest records the tape and calls it a verdict. This is what separates §I.4's sentiment-technical bucket from its fundamental one, so decompose it before assessing:

- [ ] **State the move against its comparison set**: the stock's move over the print window, the peer group's and relevant index's move over the same window, and therefore the **company-specific residual** — the part actually attributable to this print. Rough is fine; label it an estimate (Section A). "Fell 8% on the print" when the whole optics complex fell 7% that session is a sector datapoint being misfiled as a company one.
- [ ] **Say what the market appeared to react to**, and be honest when it wasn't the fundamentals — a positioning unwind, a short squeeze, a crowded-proxy move, an index event. Where the reaction is mostly sector or technical, that finding belongs in the **sentiment-technical** re-rate bucket in §I.4(b), and it must **not** be written up as the market's judgment on the quarter.
- [ ] **Distinguish a price move from a re-rate.** Did the multiple actually change, or did the price track earnings through a flat multiple? Only the former is a re-rate (Section A).
- [ ] **A large residual in either direction is itself a finding** — the market saw something in this print. Name what, or say plainly that you can't identify it and that the gap is unresolved.

### I.4 Part 2 — Assessment: what the call does to the thesis

The second required output part, and the analytical core. Assess the call against **four things, each as its own sub-heading — never merged**. An empty heading must be visibly empty, so a bucket the call genuinely didn't touch gets an explicit "unchanged, and here's why that's the right read" rather than a silent omission.

**(a) The underlying investment thesis.** Take the deep-dive's thesis and its "what has to be true" conjunction, restate it in one line, and state which legs the call **supported, weakened, or left untested**. Be specific about *which leg* — "the thesis is intact" is not an assessment. Where the call moved a leg, say by how much and on what evidence. **Where a leg rests on a forward number, discount that number by the Guidance track record (§I.5)** — a thesis leaning on a guide from management that has cut three of its last five is not the same thesis as one leaning on management that has hit every guide it issued. That is what the table is *for*; consult it here rather than treating each guide as if it arrived with no history.

**(b) Re-rating drivers.** Assess against the deep-dive's re-rate map, **keeping the four types separate** (fundamental / structural / sentiment-technical / macro — per `deep-dive-template.md` Section D). Keep the mechanics straight: **a re-rate is multiple expansion, not the price rising because revenue grew** (Section A). The question is not "was this a good quarter" — it is *did this print remove a specific discount the market was applying, or add one.* Note where a driver's **timing window** moved, since a driver pushed a year out is materially de-rated even when it's intact. Close by naming which bucket the call weighted most.

**(c) Risks.** Which named risks from the deep-dive did the call **quantify, escalate, de-escalate, or newly surface**? Concentration figures, supply dependencies, and counterparty health get their updated numbers here, dated. **Update the Pre-Mortem** (Section A: the single most likely fundamental mechanism the equity goes to zero) — state whether the call moved that mechanism closer, further away, or not at all, and name the mechanism rather than the category.

**(d) Edge and Tripwires — MANDATORY, quoted verbatim from the ticker's news.md.** Every numbered Tripwire gets a row. Ships as a table:

| # | Tripwire (verbatim from news.md) | Status this print | Evidence from the call / filing, with the figure |
|---|---|---|---|

- [ ] **Status is one of: fires / early-warning (moving toward the threshold, with the distance stated) / checked, does not fire.** A Tripwire not addressed is still a row — "the call gave no read on this" is a status, and a Tripwire silently dropped from the table is the failure mode this rule exists to prevent.
- [ ] **If any Tripwire fires: escalate.** Flag it at the top of the chat reply **and** at the top of the debrief entry, name which numbered trigger fired and how close it sits to its stated threshold, and restate the **pre-committed action** (exit / re-underwrite). Never bury it inside the quarter's narrative.
- [ ] **Assess the Edge separately** — did the print corroborate the variant view (**EDGE+**) or show consensus was right (**EDGE−**)? An accumulation of EDGE− across quarters means the differentiated thesis is failing even with no single Tripwire fired — and an earnings-debrief.md with several quarters on file is exactly where that pattern becomes visible. **Say so explicitly when you see it.**
- [ ] **Never silently rewrite the Edge or the Tripwires.** They are pre-committed in the ticker's news.md and are binding. A digest that softens a threshold a print just crossed has inverted the entire purpose of committing to it in advance. Flag it, state the pre-committed action, and leave the re-underwrite as an explicit decision for the reader to make deliberately.

### I.5 Storage — the debrief file, and the split with news.md

**One earnings call produces two artifacts, and they do not overlap:**

| Artifact | Holds | Spec |
|---|---|---|
| `tickers/<TICKER>/earnings-debrief.md` | **The quarter's full digest** — the numbers and cash-conversion breakdown, sector read, what wasn't said, the decomposed reaction, and the four-part assessment. The analysis. Plus the standing **Guidance track record** table, which spans quarters rather than belonging to any one. | This file (§I.3–I.6) |
| `tickers/<TICKER>/news.md` `## Recent News Log` | **The discrete dated news items** the call disclosed — one entry per distinct event, **split, not merged** (F.1 names an earnings call as the example of a multi-fact disclosure to split). | [`latest-updates-workflow.md`](latest-updates-workflow.md) **§F.1 — verbatim, single source of truth. Do not restate it here or apply a variant of it.** |

Both get written on an earnings run. The debrief is the analysis; the log is the record. A Tripwire that fires appears in both, and in the chat digest.

**The debrief file:**
- **Prepend each new quarter — most recent first**, under a dated `## <FY period> — reported <YYYY-MM-DD>` heading. **Never overwrite a prior quarter and never edit one after the fact.** The accumulated history *is* the file's second job: it is the only place the reader can see management's story evolve across calls — a guide raised, then held, then quietly withdrawn — and a file that only holds the latest quarter throws that away. (Contrast `reports/`: immutable dated snapshots. Same discipline, different granularity.)
- **YAML front matter and a header block** matching the ticker's news.md conventions: the `**Canonical deep-dive:**` link and a pointer back to `news.md` for the live Edge/Tripwires, so the file is navigable on the published site.
- **A `## Guidance track record` table sits at the top of the file, above the quarters — the one part of this file that is UPDATED IN PLACE rather than prepended.** Every other rule here says never edit history; this table is the deliberate exception, because a promise and its outcome are one fact recorded at two different times. Add a row when a guide is **issued**; fill its outcome columns when the period it covered **reports**. Never delete a row — a withdrawn guide is the most informative row in the table and deleting it destroys exactly the evidence the table exists to hold.

  | Guide issued (date) | For period | What was guided | Outcome (date) | Actual | Hit / missed / cut / withdrawn |
  |---|---|---|---|---|---|

  **Why this earns its place:** the deep-dive's **Management & Insider Alignment** section calls for evaluating "the C-suite's track record of meeting their own forward guidance" — but a report is a point-in-time snapshot, so today that judgment is formed once at report time from whatever history was reconstructable, and never updated again. This table accrues the evidence *prospectively*, at effectively zero marginal cost: both numbers are already being extracted in §I.3(a), and the only new work is writing the promise down when it's made. Three or four quarters in, management's credibility stops being an impression and becomes a countable record — **and a countable record is the input the next deep-dive's §13 should be built from.** State the running tally in plain English beneath the table (e.g. "hit 3 of 5 guides since FY2025; the two misses were both cut mid-quarter rather than missed at the print").
  - [ ] **Record the guide as given**, including the hedges and the range — not a rounded midpoint. A guide "of ~$180–198M, weighted to the back half, assuming no customer push-outs" that lands at $181M is a different outcome from a clean $181M against a $190M point guide, and only the verbatim range shows it.
  - [ ] **Distinguish a miss from a cut.** A guide lowered mid-quarter and then met is not a hit; it is a cut followed by a hit, and it takes two rows or an explicit note. This distinction is precisely what a naive beat/miss tally launders away.
  - [ ] **Backfill on the first run** from prior filings where the history is retrievable, and **mark backfilled rows as such** — reconstructed history is weaker evidence than a promise you recorded when it was made. If the history isn't retrievable, say so rather than starting silently at this quarter.
- **Every source is a markdown link to its direct URL** — the filing, the release, the deck. A bare publication name is not a citation. No linkable URL (a paywalled transcript, say): name it plain and say so. Never fabricate a URL; never drop the attribution silently.
- **Close each quarter's entry with a one-line methodology note** — the sources relied on with accession numbers/dates, the model used (per §I.2), and anything that could not be retrieved.

### I.6 Part 3 — Final thoughts: what to watch going forward

The third required output part. The closing wrap for the *whole digest*, not a restatement of the assessment. **This section is where the reader decides what to do next, so it must be the most scannable part of the file — a reader skimming only §3 should come away knowing what to watch, in what order, and what a pass vs. a fail looks like, without reading a paragraph.** Prose here is a failure mode: pull the threads into short labeled blocks, in this fixed running order, so an earnings-debrief.md reads identically across tickers and quarters. **CIFR's Q1'26 Final Thoughts is the canonical worked example of the format below — the rendered template in §I.7 shows exactly how the blocks, emoji markers, and pass/fail bullets should look.**

**Emoji markers are part of the format, not decoration** — they are the visual anchors that make the section skimmable, and they carry through verbatim into the chat reply (§I.7). Use them consistently: **🔴** bearish / **🟢** bullish (lean and per-point horizon tags), **✅** What to watch, **⚠️** the single #1 highest-priority watch item, **💲** Where the price sits, **🔀** What would flip the read.

**1. The read in one line.** Where the name sits **after** this print, in one or two plain-English sentences — the whole quarter's meaning before any detail.

**2. The directional lean — up top, not buried.** State the lean the quarter earns in one word (**bullish / bearish / neutral**), tagged **🔴** (bearish) / **🟢** (bullish). Where the **12-month and multi-year reads diverge, split the horizon and give each its own lean** (the same dominant-bucket discipline as the re-rate verdict, §I.4(b)) rather than averaging them into a single mushy call — e.g. "🔴 bearish next ~12 months · 🟢 constructive over 3–5 years." One line here; the justifying points come in block 6. This is a **lean on the print, not a rating on the stock**: explicitly **not** a buy/sell recommendation (not financial advice). A neutral verdict is legitimate when the print genuinely cut both ways — but "neutral" must be *argued* (the offsetting forces named), never used to dodge a call the evidence supports.

**3. ✅ What to watch — a priority-ordered bullet list, highest-impact first.** This is the section's centre of gravity and it **consolidates the dated gates, the next binary, and the fastest-acting invalidation into one ranked list** rather than three separate prose paragraphs. **Every item carries: the trigger · when (dated) · what a pass vs. a fail looks like** (per Section C). "Watch the 1.6T ramp" is not an item; "**the >$200M 1.6T order ships in the guided Q3–Q4 2026 window** — pass: ships on time; **fail: slips → Tripwire #3 fires → pre-committed action is exit/re-underwrite**" is. Requirements:
   - [ ] **Rank by impact, and flag the #1 item with ⚠️** — the single gate that matters most (usually also the fastest-acting invalidation: the Tripwire now closest to firing). Mark it and state how far from its threshold it sits.
   - [ ] **Fold the "next binary"** — the single highest-impact unresolved question the call created — into the list as the top item or an explicit callout, not a separate paragraph.
   - [ ] **Every item is dated or explicitly "open, no date,"** and names the Tripwire it would fire where one applies.

**4. 💲 Where the price sits — one short block.** Did the reaction price in the news, overshoot it, or ignore it? **Tie to the multiple, not just the price** — a price move through a flat multiple is not a re-rate.

**5. 🔀 What would flip the read — two bullets.** The specific observable that turns the lean **🟢 bullish**, and the one that **🔴 confirms/turns it bearish** — each named in advance so it's a pre-decision, not a post-hoc rationalization.

**6. Why the lean — the 3–4 justifying points.** Justify block 2's directional lean with **3–4 key points synthesized across the digest's own findings** — the reported numbers, the cash-conversion read, the sector cross-check, the decomposed reaction, and the Edge/Tripwire assessment — **not new claims introduced here.** Keep each point to a bold lead sentence plus short support, and **tag each with its horizon/direction** (🔴 bearish-12mo / 🟢 bullish-3–5yr) so the split in block 2 is visible at a glance. Carry the honest counterweight here (Section A — no victory lap, no eulogy): at least one point must argue the other side of the lean.

**7. Bottom line.** Close with a **short, plain-English** wrap.

**Constraints on this section, per Section A:** keep it framework-level guidance the investor applies themselves. **Not financial advice** — flag it; this is decision-shaped by construction. **No unsolicited portfolio-fit, concentration, or position-sizing commentary** — request-only. **Give the affirmative read AND the honest counterweight** — a digest of a good quarter that reads as a victory lap has failed this rule as surely as one of a bad quarter that reads as a eulogy.

**Depth ceiling — this is not a deep dive.** Target **~2,000–3,000 words** per quarter's entry (the Guidance track record table sits outside the count — it spans quarters and grows by one row). The deep-dive's ~7,000-word floor is a floor for exhaustive diligence against a whole company; this is a bounded read of one event against an already-built thesis, and length here trades directly against the reader actually finishing it. If the call genuinely warrants a re-underwrite of the whole name, **say so and run the deep-dive** — do not let the debrief sprawl into one.

### I.7 Chat reply

Produce the run digest in the canonical format defined in [`news-check.md`](news-check.md) **§B — TRIPWIRES FIRST**, scoped to the one ticker, so an earnings run and a routine watch run read identically. Add one lead line above it: the quarter, the headline result against the guide, and the **net assessment** — thesis strengthened / weakened / unchanged.

**Then append the entire §I.6 Final Thoughts section — every block, verbatim from the debrief, with its emoji markers — immediately after the §B digest and before the debrief link.** All seven blocks come across in order: **(1)** the read in one line, **(2)** the directional lean (🔴/🟢, horizon-split), **(3)** the ✅ priority-ordered "What to watch" list with pass/fail per item (#1 flagged ⚠️), **(4)** 💲 where the price sits, **(5)** 🔀 what would flip the read, **(6)** the 3–4 points behind the lean, and **(7)** the bottom line. **This is not optional and is not reduced to a summary, a single block, or a one-liner** — the chat reply is the surface the reader actually reads after an earnings run, and Final Thoughts *is* the reader's action layer: the verdict, the watch list, the flip triggers, and the price read are exactly what a reader needs in the reply, not only in the file. Reproduce them as written in the debrief (§I.6 already caps this section's length and mandates its scannable form, so appending it whole does not bloat the reply). Close with the link to the debrief file. The rest of the digest — the numbers breakdown, cash-conversion table, sector cross-check, and the four-part assessment (§I.3–I.4) — stays in `earnings-debrief.md` and is *not* reproduced in the chat reply.

**Canonical worked example — the shape every chat reply's appended Final Thoughts must take** (from CIFR Q1'26; substitute the ticker's own content, keep the structure and markers):

> **The read in one line:** Cipher passed every Tripwire — but only because nobody tested it (six analysts asked zero questions about the four things that break the thesis). The market isn't pricing fundamentals; it's pricing lease announcements. Nothing is resolved. **Everything rests on one date in October.**
>
> **Directional lean: 🔴 bearish next ~12 months · 🟢 constructive over 3–5 years.** Near term is all sentiment (a tape that pays only for announcements, a hard date with no outside corroboration); long term is a real, strengthening asset (the lease stack + demonstrably cheap financing).
>
> **✅ What to watch — highest priority first:**
> 1. **⚠️ Does the Oct-2026 NOI window hold? — next test 2026-08-06 (Q2 print).** The whole thesis and the fastest-acting invalidation. **Pass:** window start carries forward unchanged a second straight quarter. **Fail:** slips by even a month in any deck → **Tripwire #1 fires** → exit/re-underwrite.
> 2. **Barber Lake Phase I delivery — ~Sep 2026.** First genuinely falsifiable delivery. Pass: on time. Fail: slips.
> 3. **Black Pearl initial rent — ~Oct 2026.** The first real rent dollar. Watch the ambiguity: final phase ~Mar 2027, and Tripwire #1 is written against the *first* milestone only.
> 4. **Third-campus financing — open, no date.** Watch for an equity raise (pressures Tripwire #2) vs. more cheap project debt.
> 5. **ERCOT Batch Zero outcome — submissions closed 2026-07-10.** Gates ~2.0 GW of the pipeline.
>
> **💲 Where the price sits:** Fairly priced on the market's own terms — no multiple expansion (EV/backlog ~1.22× → ~1.14×). Paid the cohort multiple for cohort risk.
>
> **🔀 What would flip the read:**
> - **→ 🟢 bullish:** first rent recognized on schedule — the fundamental bucket finally contributes.
> - **→ 🔴 bearish (confirmed):** the Oct-2026 window start moves by so much as a month in any deck.
>
> **Why bearish near-term, bullish long-term:**
> 1. 🔴 Market pays for announcements, not results — +23.5% on a lease, gave it all back in three sessions.
> 2. 🔴 The one hard date has thin, company-only corroboration — guided to milestones-not-rent, un-corroborated by ERCOT.
> 3. 🔴 Fundamentals contributed nothing; pre-rent trough deepened — $0 HPC revenue, OCF "turn" was an $83.3M payables build, FY26 consensus cut ~44%.
> 4. 🟢 Counterweight — the funding leg got materially stronger — $1.97B cheap project debt, oversubscribed bonds above par, a third IG lease.
>
> **Bottom line:** A quarter with no bad news and no good news either. Cipher signed a third lease and proved it can raise debt cheaply, and the market shrugged and paid the same multiple. The thesis is intact and entirely unresolved. **Everything still rests on a date in October.**
>
> Full breakdown and reasoning: `tickers/CIFR/earnings-debrief.md`.
