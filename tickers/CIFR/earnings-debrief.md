---
company: "Cipher Digital · NASDAQ"
blurb: "Earnings debrief log — one entry per reported quarter, most recent first, plus the standing guidance track record."
---

# CIFR — Earnings debrief log

**Canonical deep-dive:** [`reports/2026-07-15.md`](reports/2026-07-15.md) · **Live Edge & Tripwires:** [`tickers/CIFR/news.md`](news.md) — authored there and binding; this file assesses against them and never rewrites them.

*Built per [`framework/earnings-digest.md`](../../framework/earnings-digest.md) (Section I). Quarters are prepended, most recent first, and never overwritten. The Guidance track record below is the one part of this file updated in place.*

---

## Guidance track record

*A promise and its outcome are one fact recorded at two different times. Rows are added when a guide is issued and their outcome columns filled when the period reports. Nothing is ever deleted — a withdrawn guide is the most informative row here.*

**Cipher issues no quarterly revenue, EBITDA, or EPS guidance, and did not at Q4 2025 either.** This is a standing practice, not a withdrawal. It guides via the **contracted-NOI schedule** instead, so that is what this table tracks — the forward numbers management actually commits to.

| Guide issued (date) | For period | What was guided | Outcome (date) | Actual | Hit / missed / cut / withdrawn |
|---|---|---|---|---|---|
| 2026-02-24 · Q4'25 deck ⁺ | Oct 2026 – Sep 2036 | Contracted revenue **~$9.3B** / 600 MW / 2 leases; avg. annualized NOI **$669M**; 2035 NOI $754M | 2026-05-05 | Superseded upward: $11.4B / 700 MW / 3 leases; NOI $787M | **Raised** (third lease added; window unchanged) |
| 2026-02-24 · Q4'25 deck ⁺ | — | Both anchor campuses "on schedule"; NOI window **starts Oct 2026** | 2026-05-05 | Window start **carried forward unchanged** at Oct 2026 | **Reaffirmed** — see §2(d) T#1 |
| 2026-05-05 · Q1'26 deck | Oct 2026 – Sep 2036 | Contracted revenue **~$11.4B** / 700 MW / 3 leases; avg. annualized NOI **$787M**; 2027 NOI $646M; 2035 NOI $892M | *pending* | — | *Pending — first test 2026-08-06* |
| 2026-05-05 · Q1'26 call | FY2026 | **No financial guide issued** (consistent with Q4'25) | n/a | n/a | *n/a — practice, not a withdrawal* |
| 2026-05-05 · Q1'26 call | Third campus | Financing plan **declined** when asked directly (BTIG) | *pending* | — | *Open — the unanswered question* |

⁺ *Backfilled 2026-07-17 from prior filings — reconstructed history, weaker evidence than a promise recorded when made.*

**Running tally:** too few resolved rows to score credibility yet — **one guide resolved, one reaffirmed, zero missed.** The table's value starts at the 2026-08-06 print, when the Q1 NOI schedule gets its first real test. The load-bearing observation for now: **Cipher's only falsifiable forward commitment is the Oct-2026 NOI window start**, and it has now survived one quarter unchanged.

---

## Q1 2026 — reported 2026-05-05 (pre-market)

> **No Tripwire fired.** One real disclosure finding (a KPI redefinition), one materially misleading headline (the OCF "turn"), and one finding that cuts against the thesis file itself: **the Edge is built on a backlog number the company superseded on this call.** See §2(d).

### 1. What was said

#### (a) The reported numbers

Cipher does not guide, so the Δ below is **against consensus only** — there was no company guide to beat or miss.

| Metric | Reported (3/31/26) | Company guide | Consensus going in | Δ vs. guide / consensus | YoY | Read — what it actually means |
|---|---|---|---|---|---|---|
| Revenue (all bitcoin mining) | **$34.84M** | none issued | $33.71M | — / **+3.35%** | **−28.8%** | A 3% beat on a bar the sell-side had already cut ~31%. Near-zero information. Also **−41.7% QoQ** from $59.71M — mining is being dismantled on purpose. |
| HPC / hosting revenue | **$0** | — | — | — | — | **Not a zero-valued line — there is no HPC revenue line at all.** 100% of revenue is the business being wound down. |
| GAAP net loss | **$(114.32)M** | none | — | — | vs $(38.98)M | Includes a **$43.6M non-cash warrant gain**; the loss is worse ex-that. |
| LPS (basic & diluted) | **$(0.28)** | none | $(0.27) | — / **−3.70%** | vs $(0.11) | **Missed.** Computed on 405.1M shares — see dilution below. |
| Adjusted EBITDA (non-GAAP) | **$(48.22)M** | none | ~$(7.3)M | — / **~6.6× miss** | vs **+$7.50M** | The headline swing is only partly operational: D&A collapsed $43.5M→$19.0M as assets went held-for-sale, while comp tripled. |
| Cash (unrestricted) | **$715.20M** | — | — | — | — | **The number the Edge quotes — and it is the wrong number.** See restricted cash below. |
| Restricted cash | **$3,531.14M** | — | — | — | — | Escrowed for construction. **Total cash + restricted = $4,246.34M.** |
| Total debt (carrying) | **$4,732.11M** | — | — | — | vs $2,749.44M | **+$1.98B in one quarter**, all project notes. |

**The adjustment bridge, and what it excludes** *(arithmetic verified on both years)*: net loss $(114.32)M → EBITDA $(67.33)M → adj. EBITDA $(48.22)M.
- **SBC of $27.05M is added back** — 3.0× the year-ago $9.13M and **78% of the entire $35.0M compensation line**. Non-cash but genuinely dilutive. Adj. EBITDA is **$(75.3)M with SBC left in**.
- **The $43.6M warrant gain is correctly removed** (a subtraction). That is honest discipline, not a flatter — worth saying plainly.
- **Bitcoin marks are *not* adjusted out** — the $(24.2)M realized loss and $3.8M unrealized gain both stay in, worsening adj. EBITDA by ~$20.5M. A miner that excludes power-contract marks but keeps bitcoin marks is choosing **asymmetrically**; it happens to cut against them this quarter, but the inconsistency is the point.

**Dilution — the share count the market cap should be measured against is ~52% higher than the basic count.** 405.27M shares outstanding, but **209.85M antidilutive shares are excluded** because the period is a loss: 161.93M convert conversion rights, 24.18M Google penny warrants, 23.74M unvested RSUs. **Fully diluted ≈ 615.1M (+51.8%).** Blended convert strike ≈ **$9.09** *(derived: $1,472.5M ÷ 161.93M — my arithmetic, not disclosed)*, so against a ~$20 stock **both converts are equity in economic substance, not debt**. Clean positive on the dilution watch: **ATM usage in Q1 was effectively nil** — shares rose only 303,304 and APIC rose less than SBC alone. Cipher funded entirely with project debt, not paper.

**Debt — the $4.73B / $5.2B conflict, resolved.** Sources disagree; both numbers are right and they measure different things. The balance sheet gives **$4.73B carrying** ($355.35M short-term + $4,376.76M long-term, net of discounts and issuance costs). Summing the instruments gives **~$5.17B principal**: 2030 converts $172.5M + 2031 converts $1,300M + Barber Lake 7.125% $1,700M + Black Pearl 6.125% ~$2,000M. *(Derived — the reconciliation is mine.)* **Cipher's own deck quotes principal**, which is why "$5.2B total debt / $4.2B cash / $960M net debt" is internally consistent. **Use $4.73B for balance-sheet work, $5.2B when reading the deck.** A separate $5.21B figure circulating on filing-mirror sites is a different animal — it is debt **plus the $481.55M warrant liability**, which is not debt. Don't repeat it.

**Contracted vs. recognized vs. collected — the accounting shape of the whole thesis.** ~$11.4B contracted · **$0 recognized** · **$0 collected in advance**. As lessor under leases that have not commenced, ASC 842 gives Cipher **no asset, no receivable, no deferred revenue** — the entire backlog is a lease-footnote disclosure with **zero balance-sheet presence**. What *is* on the balance sheet is the cost side only: PP&E $633.4M → **$1,307.3M** (CIP $834.4M), against $4.73B of debt. **All cost recognized, all revenue in a footnote.** Stockholders' equity fell to $714.2M — **11.2% of assets**.

#### (b) Cash conversion & working capital

| Measure | Q2'25 | Q3'25 | Q4'25 | Q1'26 | Direction | Read — benign or warning? |
|---|---|---|---|---|---|---|
| Operating cash flow | $(56.2)M | $(50.1)M | $(54.4)M | **+$91.5M** | "turned" | **Warning — the turn is an artifact.** See below. |
| Net income | $(45.8)M | $(3.3)M | $(734.2)M | $(114.3)M | — | NI↔OCF gap: **+$679.8M** (Q4) then **+$205.9M** (Q1). Neither is a usable earnings proxy. |
| Capex | $(112.5)M | $(44.7)M | $(229.8)M | **$(554.0)M** | ↑ 2.4× QoQ | Asset-building, not lights-on. The entire cash story. |
| **FCF** | $(168.7)M | $(94.8)M | $(284.3)M | **$(462.5)M** | ↓↓ | **Negative in all six quarters retrieved. The only honest read.** |
| AP + accrued | n/r | $50.0M | $130.2M | **$402.6M** | ↑ +$272.4M | Construction payables tracking capex — **not** the shrinking mining business. |
| AR / DSO | ~$1.8M / ~3.8d | $0.70M / 0.9d | $0.69M / 1.1d | **$8.49M / 21.9d** | ↑ 12.4× | **Not a receivables-quality signal — see below.** |
| Deferred revenue / advances | none | none | none | **none** | flat | Building $5.5B+ of contracted capacity **without collecting a dollar up front**. |
| Inventory / DIO / CCC | none | none | none | **none** | n/a | **Not computable, and that is a fact, not a gap.** Any CCC quoted for CIFR is manufactured. |

**The headline finding: the OCF "turn" is a payables build, not a turn.** OCF was negative for four straight quarters at a remarkably steady ~$50M/qtr structural burn, then printed **+$91.5M**. The entire swing is an **+$83.3M increase in operating liabilities**. Strip it and **OCF ≈ +$8.2M** — essentially breakeven, consistent with the prior run-rate improving modestly, not inverting. **Cipher is partly financing its build on contractor payables, and that shows up in *operating* cash flow.** It reverses when payables normalize. A reader who saw "first positive operating cash flow" and stopped there got the quarter backwards.

**The DSO spike is a false positive — and this is the calibration that matters.** AR jumped 12.4× and DSO went 1.1 → 21.9 days, which looks alarming. It isn't, because **the AR line changed meaning**: at 12/31/25 it was "amounts due from only customer, mining pool operator"; at 3/31/26 it is **"amounts due related to change orders requested from tenants for HPC data centers."** The 21.9-day DSO is computed on mining revenue against a receivable that has nothing to do with mining revenue. It is the **first receivable Cipher has ever booked against an HPC tenant** — a construction change-order reimbursement, not rent. Watch it as an early HPC-relationship datapoint; do not read it as collection stress. *(DPO is equally meaningless here — AP/COGS×90 gives 1,006 days, and that absurdity is itself the signal that AP is construction, not cost-of-revenue.)*

**The contradiction worth naming:** management called the quarter proof they are "no longer an aspirational HPC developer" while the cash statement shows **$554M/qtr going out, $0 HPC coming in, and the only positive operating line manufactured by unpaid contractor bills.**

#### (c) Management's read on the sector — cross-checked

*Standing label: this is an **interested party's opinion** until corroborated. Cipher is a lessor talking its own book at a point of maximum expectation. Venue matters — volunteered in prepared remarks is different evidence from extracted under questioning.*

| What management said | Where | Independent check — does outside evidence agree? |
|---|---|---|
| West Texas "one of the most sought-after regions in the country for large-scale AI infrastructure" | Prepared (volunteered) | **Corroborated, strongly.** Hyperscaler capex was *raised* in the late-Apr prints: Meta to $125–145B, Microsoft $30.9B (+84%), Alphabet $35.7B, Amazon $44.2B. Aggregate 2026 ≈ **$725B, +77% YoY**. [T] |
| "We continue to see premium pricing in our negotiations"; **"I do not see lease rates going down for premium sites with good timelines"** | **Q&A — extracted by Macquarie**, not volunteered | **Corroborated but read narrowly.** TeraWulf independently reported demand "very strong" and **15-year terms becoming common**; Hut 8 signed 352 MW / $9.8B / 15-yr with a 3.0% escalator on 5/6 — near-identical structure. But note the double qualifier: *premium* sites with *good* timelines. It is a defensible claim about the top of the market that says nothing about the average, and is **not** a denial that rates are falling elsewhere. [T] |
| ERCOT/power scarcity as Cipher's advantage; 2.0 GW gated on Batch Zero finalizing "in June" | Prepared + Q&A ("**hoping** for a good outcome") | **Contradicted / heavily qualified — the weak leg.** ERCOT's large-load queue is **438 GW, ~90% data centers**, and **ERCOT itself warned the Texas AI power boom "may not materialize."** The PUCT only approved the Batch Zero process on **2026-06-18** — the orderly queue process *did not exist* at the time of this call. The queue is simultaneously the demand validation management claims **and** the reason any specific Q4-2026 energization date is fragile. [P/T] |
| Financing conditions: another bond would price "at similar, if not better terms" | Prepared + Q&A | **Corroborated by a third-party price, not opinion.** Black Pearl $2.0B priced at 6.125%, **oversubscribed 6.5×**, a full point below the prior deal; **both bond complexes trading above par**; $200M revolver closed **undrawn** with Morgan Stanley/Goldman/JPM/Wells/Santander/SMBC. **This is the strongest corroborated item on the call.** [T] |
| Mining "fully self-funded"; bitcoin gone "by end of '27 at the latest" | Prepared | Consistent with the numbers: $0.028/kWh fixed PPA through Jul 2027, BTC holdings down to **1,116 BTC / $76.2M**. [P] |

**Language shift vs. Q4 2025 — three, all the same direction, none individually material:**
1. **Demand's first derivative flattened.** Q4: *"lease pricing continues to move in our favor alongside growing demand"* (prepared). Q1: *"I do not see lease rates going down…"* (Q&A). **Prices rising for us → prices not falling, for the good sites** — and volunteered optimism became extracted reassurance.
2. **Delivery timing: absolute → contractual.** Q4 "on track" / "tracking to meet milestones"; Q1 "tracking to meet **contractual** early access and rack-ready dates." **Thin signal — log it, don't act on it** (Q4 already said "tracking," and both releases still say "remains on schedule").
3. **Financing scope narrowed by one adjective — the most consequential shift.** Q4 CFO: no additional equity needed to fund **"currently contracted developments"** (a defined set). Q1 CFO: liquidity sufficient for the **"near-term development pipeline"** (an undefined horizon). *"Near-term" is not a period; it is an adverb* — said in the same quarter a fourth campus was signed whose financing the CFO then **declined to specify**.

#### (d) What management *didn't* say

**One real finding out of four checks. Three come back genuinely clean — which is itself a result worth recording.**

| What's missing | Last disclosed | Management's stated reason | Read — why it likely went away |
|---|---|---|---|
| **"Adjusted Earnings (Loss)" — replaced by "Adjusted EBITDA"** | Q4'25: adjusted net loss **$55M** | Verbatim: after stacking four debt issues, "interest expense has become a significant component of net loss that is **not directly tied to our underlying operating performance**"; new measure is "more comparable to measures used by industry peers" | **Defensible reason, conveniently timed — leaning convenient.** [P] |
| Third lease's **tenant, rent, NOI contribution, and commencement** | never disclosed | NDA-until-financing (Cipher's demonstrated pattern) | **Not a removal** — a name never given, not one withdrawn. Resolved 34 days later (AWS/Stingray, 6/8). |

**On the KPI switch — the timing test.** The peer-comparability argument is real: data-center lessors are quoted on EBITDA/NOI, and a company mid-pivot has a fair claim to a metric that survives the transition. **Record that at face value.** But Cipher switched to a metric that **excludes interest expense** in the *first quarter after* stacking ~$5.2B of debt — and precisely during the ~6-quarter window where interest accrues on $3.7B of project notes while HPC rent is still $0. Under the old metric, each pre-rent quarter would have printed visibly worse. **The change is exactly coincident with the period in which the old metric would have been most unflattering, and it retires the number that most directly tracks the Edge's "execution-and-financing gap."** Note the self-refuting edge in the rationale: for a **leveraged developer-lessor whose entire equity story is whether contracted rent outruns project debt service, interest expense *is* the operating performance.** Both things are true at once. *Watch whether Adjusted EBITDA quietly becomes the only number quoted once rent begins.* **Opinion, not fact.**

**Clean checks (recorded because a clean check is a real result):** no headline metric was dropped — contracted revenue, NOI, capacity, hash rate, J/TH, BTC mined and the PPA rate all carried forward, and Q1 **added** disclosure (2027 NOI, per-site energization dates, equipment-secured percentages). No segment or site was rolled into an "other" line; the site breakout got **finer**. **The NOI window was specifically checked for rebasing and had not been rebased** — Oct 2026 – Sep 2036 in both decks, identical definition. And rent-commencement dates were absent from *both* releases, so their absence here is **consistent practice, not a withholding**. **Direction of travel is more disclosure, not less.**

#### (e) The reaction, decomposed

**Day 1 was real. It was gone by day 3. Both facts matter.**

| Window | CIFR | Clean-peer sector move | Residual (estimate) |
|---|---|---|---|
| 5/4 → 5/5 (print day) | **+23.53%** ($17.89 → $22.10) | **~+5.2%** median (MARA +2.79%, HUT +3.11%, CORZ +5.17%, WULF +5.38%, RIOT +8.94% — all without own catalysts) | **~+16 to +18pp** |
| 5/4 → 5/8 (3 sessions) | **+14.87%** | **WGMI +14.89%** | **≈ 0.0pp** |
| 5/4 → 5/15 | +13.64% | WGMI +13.29% | ≈ +0.4pp |

*Estimates. Beta to the miner cohort assumed ~1.3 (not retrieved); CIFR's beta vs. S&P is 3.196, so the +1.03% Nasdaq day explains ~3pp at most — the market factor is negligible here. Volume 50.67M vs. ~27.4M average confirms a genuine repricing event, not drift.*

**The mechanism is visible in the tape: on 5/6, CIFR fell −0.86% while WGMI rose +10.19%** — the day Hut 8 announced its $9.8B lease and the cohort ripped on *someone else's* news. **Cipher gave back its entire idiosyncratic premium into a sector melt-up.** The widely-circulated "+23.5% on the print" is a one-session artifact; on any window longer than a day, the print is **not distinguishable from holding the miner ETF**.

**No re-rate.** The sell-side anchors this cohort on EV/contracted-backlog (EBITDA is negative and meaningless pre-rent):

| | Pre-print | Post-print | Change |
|---|---|---|---|
| Contracted backlog | ~$9.3B | **$11.4B** | **+22.6%** |
| Share price | $17.89 | $22.10 | **+23.5%** |
| EV/contracted-backlog *(est.)* | ~1.22× | ~1.14× | **−6%** |

**The price tracked the numbers through a flat-to-lower multiple.** Backlog rose ~22.6%, the stock rose ~23.5%, and the market **added a lease at the multiple it was already paying**. It did not decide Cipher's leases were worth more per dollar. *(Robust to the net-debt uncertainty: −6% at $4.0B net debt, −1.5% at $0.96B.)*

**What the tape was actually paying for — the cleanest cross-check available.** Same week, same sector, one differentiator: **lease announcements, not numbers.** CIFR missed adjusted EBITDA by ~6.6× and rose **+23.5%** because it announced a third campus. **CORZ missed and fell −9.2%** on 5/7 for the sole sin of *not* announcing a lease. HUT rose ~30% purely on its lease. **In this window the market assigned ~zero weight to reported financials and ~all weight to backlog additions.**

**Sell-side, after the print:** thin and slow — Needham $22→$25 ten days later; Bernstein initiated Outperform $32 a month later. Consensus ~16 analysts, Strong Buy, avg PT $32.63. **But underneath the unanimous Buys sits the most informative datapoint in this whole exercise: FY2026 consensus revenue was cut from ~$427.3M to ~$237.6M — a ~44% reduction.** The analysts did not change their minds about the thesis; they changed their minds about **when any revenue arrives**, and kept the rating. That is the textbook "lowered estimate under a maintained Buy."

#### (f) Part 1 in brief

- 📊 **The numbers:** revenue $34.8M beat consensus +3.35% on a bar already cut ~31%, but adjusted EBITDA missed **~6.6×** and mining fell −41.7% QoQ by design. $0 HPC revenue. No company guide, so "beat" is near-meaningless.
- 💵 **Cash conversion:** the "first positive OCF" (+$91.5M) is **an $83.3M payables build, not a turn** — strip working capital and OCF ≈ +$8M. FCF negative in all six quarters. Cipher is partly financed by unpaid contractors.
- 🏭 **Sector read:** ⚠️ mixed. Hyperscaler capex +77% to ~$725B ✅ corroborates demand; financing strength ✅ corroborated by a third-party bond price (oversubscribed 6.5×). But ERCOT/energization ❌ contradicted — 438 GW queue, ERCOT's own "may not materialize" warning.
- 🔇 **What wasn't said:** one real finding — the headline metric switched from "Adjusted Earnings" to **"Adjusted EBITDA," which now excludes interest**, the first quarter after stacking ~$5.2B of debt. Defensible reason, conveniently timed. Otherwise a clean check — disclosure got *finer*, not thinner.
- 🎢 **The reaction:** +23.5% on the print, but the company-specific residual (~+16–18pp) **fully decayed to ≈0 in three sessions**. No re-rate — EV/backlog went ~1.22× → ~1.14×; the market added a lease at the multiple it already paid.

### 2. What it means

#### (a) The underlying investment thesis

The thesis rests on this conjunction: **the ~$9.3B backlog converts on schedule from ~Q4 2026, and the remaining capex gets funded without forced dilution.**

- **Leg 1 — "backlog converts on schedule": supported, on company-reported evidence only.** The strongest datapoint is quiet and structural: the **Oct-2026 NOI window start carried forward unchanged** from the Q4 deck. Had commencement slipped, that number had to move. It didn't. Equipment-secured percentages (Black Pearl 93% Phase I / 80% Phase II; Barber Lake ~99%) are specific and falsifiable. **But the schedule has no independent corroboration**, and the outside evidence on ERCOT cuts the other way.
- **Leg 2 — "funded without forced dilution": supported, and this is where the call is strongest.** Zero equity issued, $1.97B raised entirely as project debt, revolver closed undrawn, bonds above par. Discounted by the guidance track record: **too few resolved rows to discount by** — but the release itself admits **"equity funding is still required"** for the third campus, and the CFO's no-equity language narrowed from "currently contracted developments" to "near-term."
- **Leg 3 — untested and unasked: the counterparties.** Nothing on Fluidstack's credit. Not one analyst asked.

**A leg the deep-dive got wrong: the backlog is $11.4B / 700 MW / three leases, not $9.3B / two.** See §2(d).

#### (b) Re-rating drivers — four buckets, kept separate

**Fundamental.** The print removed no discount. The only fundamental driver that moved is **negative**: FY26 consensus revenue cut ~44%, formalizing that the mining engine is being disassembled faster than HPC arrives. The pre-rent trough is now consensus, not a surprise. **Timing windows unchanged** — Oct 2026 anchor intact.

**Structural.** The genuine positive. A **third investment-grade hyperscale lease** (+$2.1B, +100 MW) extends the counterparty stack and demonstrates platform repeatability — three leases in ~8 months. The **$200M revolver** is the first corporate-level facility in company history, structurally widening the funding toolkit beyond per-project notes.

**Sentiment / technical.** **This bucket carries the most weight for the quarter, and it is where the honest reading lives.** The +23.5% was a sentiment event that fully decayed in three sessions; a 13.32% short float *(Feb 2026 snapshot — could not retrieve a figure dated at the print)* with ~2.3 days to cover, beta 3.196, and 125%-above-average volume are consistent with a squeeze contribution, **hypothesis not finding**. The regime itself is the driver: **a market paying only for announcements**.

**Macro.** Hyperscaler capex +77% to ~$725B is a genuine tailwind and corroborated. **ERCOT is the offsetting macro risk** and it is under-weighted in the thesis file: a 438 GW queue, ERCOT's own "may not materialize" warning, and a Batch Zero process that didn't formally exist until 6/18.

**Net verdict — which bucket carries the most weight right now:** **sentiment/technical for the next 12 months** (the tape is paying for announcements, not results, and will re-price violently on the first *non*-announcement); **structural for the 3–5 year thesis** (the lease stack is the durable asset). **The fundamental bucket contributed nothing this quarter** — and on this evidence, cannot until rent begins.

#### (c) Risks

- **Escalated: ERCOT/energization.** Independent evidence contradicts the comfortable reading. **Newly surfaced, and it is the sharpest correction here:** management guides to **contractual milestones** (early access, rack-ready, substantial completion) — **not to rent commencement**. Those are different events, **and the gap between them is exactly where slippage would first hide.**
- **Escalated: quality of earnings.** OCF positive only via an $83.3M payables build; construction payables up +$272.4M in a quarter. **Cipher is partly financed by its contractors.**
- **De-escalated: Fluidstack (T#3).** It *raised* — ~$750M at ~$7B, reportedly in talks for ~$1B at ~$18B (Jane Street, Situational Awareness), a Macquarie facility up to $10B, ~$6.7B of Google-backstopped contracted revenue. [T]
- **De-escalated: near-term liquidity.** $4.25B total cash+restricted; net debt **~$486M** (carrying) / ~$926M (principal) — not the "$715M vs. $4.73B" the Edge implies.
- **Quantified: dilution.** ~615M fully diluted vs. 405M basic; SBC $27M/qtr and rising 3.0× YoY.

**Pre-mortem, updated.** The single most likely fundamental mechanism to zero remains: **a Black Pearl or Barber Lake energization slip pushes rent past the window in which project-note interest is being serviced out of escrow, forcing an equity raise into a de-rated stock — with ~615M fully diluted shares and 11.2% equity/assets to absorb it.** **The call moved this mechanism slightly further away** (financing access demonstrably strong, bonds above par, revolver undrawn) **while moving its trigger slightly closer** (ERCOT's queue is worse than the thesis file credits, and management guides to contractual milestones rather than to rent).

#### (d) Edge and Tripwires

| # | Tripwire (verbatim from `news.md`) | Status | Evidence |
|---|---|---|---|
| **1** | *"the first HPC rent-commencement milestone (Black Pearl/AWS or Barber Lake/Fluidstack) **slips materially past ~Q4 2026**… this is the single highest-priority trigger"* | **Checked — does not fire. Reaffirmed.** | **Oct-2026 NOI window start carried forward unchanged** in the Q1 deck [T, deck-via-coverage]; Barber Lake topped out April (~800k sq ft in 127 days), ~99% equipment secured, Sep-2026 commencement per 10-Q; Black Pearl 93%/80% secured, ~Oct 2026 initial. **Caveats: guides to *contractual milestones*, not rent; no analyst tested the date; ERCOT does not corroborate.** First falsifiable checkpoint: **2026-08-06**. |
| **2** | *"A **large, dilutive equity raise executed at a de-rated price**… to plug the capex-vs-cash gap ($715M cash vs. multi-GW capex ahead)"* | **Checked — does not fire. The quarter cuts against it.** | Zero equity issued; ATM effectively nil (+303,304 shares); $1.97B raised as project debt; revolver **undrawn**; bonds **above par** *(third-party price — the strongest evidence here)*. **But:** the release admits **"equity funding is still required"** for campus three; BTIG asked how it gets financed and **got "flexibility," not a plan**; the no-equity pledge narrowed to "near-term." **Live, not tripped. And the tripwire's own premise is wrong — see below.** |
| **3** | *"**Fluidstack shows funding/credit stress** that the capped ($1.73B) Google backstop would not fully cover, OR any HPC tenant defaults/renegotiates/delays"* | **Checked — does not fire. Moved favorably.** | Fluidstack **raised** rather than stressed (see §2(c)). **But the call is silent: zero commentary, and across ~6 analysts, zero questions.** This exposure **cannot be assessed from the call** and must be sourced elsewhere — Fluidstack's own funding news, or the Barber Lake bond's trading level as a credit read-through. |
| **4** | *"**BTC falls materially further** while mining is still the only recognized-revenue source, breaking the self-funding bridge before HPC rent begins"* | **Checked — does not fire at this print. Premise substantially dismantled.** | BTC was **~$81,286 on 5/5** — the bridge was intact. *(It has since fallen ~20% to ~$65K — already logged in news.md's 6/25–7/15 entry.)* **The re-scoping finding:** the bridge is **not** funded by mining. Mining is $34.8M/qtr and falling by design, structural ex-WC OCF is **~+$8M**, and the BTC position is down to **$76.2M**. The build is funded by **$4.25B of cash and escrowed construction accounts**. A further BTC drawdown now mostly hits a $76M position, not the construction plan. **The residual risk is sentiment/multiple, not liquidity.** |

**Edge — corroborated in its skepticism, and simultaneously wrong in its numbers.**

The Edge demands you pick a side. **This print tested the bullish variant at its strongest and it did not print.** The bullish variant needs the market to be under-crediting counterparty quality such that Cipher earns *"a premium within the cohort rather than a peer-average multiple."* The quarter delivered **exactly that evidence** — a third investment-grade hyperscale lease — and earned **zero multiple expansion** (EV/backlog ~1.22× → ~1.14×) plus a residual that fully decayed in three sessions. **The market is already paying peer multiple for counterparty quality and declines to pay a premium for it. Tag: EDGE−** against the bullish variant specifically.

The Edge's **skeptical core is corroborated**: six analysts, **zero questions on any of the four Tripwires**, and the one adjacent question deflected. A crowded, uncritical Q&A generated **less disconfirming evidence than a normal call would** — which is precisely "a richly-priced, crowded consensus at a point of maximum expectation."

**But two of the Edge's own load-bearing numbers are wrong, and per §I.4(d) I am flagging rather than rewriting them:**

1. **"the ~$9.3B backlog" is stale.** Cipher disclosed **~$11.4B / 700 MW / three leases on this call — 2026-05-05, two months before the deep-dive was written.** The Edge's central sentence quotes a number the company had already superseded. *(Two independent agents corroborate $11.4B from deck coverage; it is **absent from the press-release text** and the deck PDF itself was never opened — treat as [T], deck-via-coverage, not [P].)*
2. **"$715M cash against ~$4.73B debt" materially overstates the funding gap.** It omits **$3.53B of restricted construction cash**. Total cash+restricted is **$4.25B**; net debt is **~$486M**. Both quoted figures are individually correct and the framing built from them is not.

**Neither is a reason to soften the Edge — the skepticism survives both corrections.** But an Edge whose headline number is two months stale is measuring against the wrong thing, and **Tripwire #4 is drafted against a mechanism that has largely already been dismantled.** Both need a deliberate re-underwrite decision, made explicitly. **That is your call to make, not this digest's.**

#### (e) Part 2 in brief

- 🎯 **Thesis legs:** Leg 1 "backlog converts on schedule" — *supported on company evidence only* (Oct-2026 window held), no independent corroboration. Leg 2 "funded without forced dilution" — *strengthened*, the call's strongest leg. Leg 3 counterparties — *left untested*, not one analyst asked.
- 🔄 **Re-rate:** the print *removed no discount* — fundamental bucket contributed nothing (FY26 revenue cut ~44%). Only **structural** moved positively (third IG lease + first corporate revolver); **sentiment/technical** carries the next 12 months.
- ⚠️ **Risks:** *escalated* — ERCOT/energization and quality-of-earnings (payables-financed OCF). *De-escalated* — Fluidstack (raised, not stressed) and near-term liquidity (net debt ~$486M, not the implied $4B). Pre-Mortem unchanged: an energization slip forces an equity raise into a de-rated stock.
- 🚨 **Tripwires & Edge:** ✅ all four checked, none fire (#1 reaffirmed, #2 live but cuts against, #3 moved favorably, #4 premise dismantled). 🔴 **EDGE−** against the *bullish* variant — it delivered its best evidence (a third IG lease) and earned zero premium. Note: the Edge's own numbers ($9.3B backlog, $715M-vs-$4.73B) are stale and need a deliberate re-underwrite.

### 3. Final thoughts — what to watch going forward

*Not financial advice — a framework to apply yourself.*

**The read in one line:** Cipher passed every Tripwire — but only because nobody tested it (six analysts asked zero questions about the four things that break the thesis). The market isn't pricing fundamentals; it's pricing lease announcements — CIFR missed adjusted EBITDA 6.6× and rose 23% *because* it announced a third lease, while Core Scientific missed with no lease and fell 9%. Nothing is resolved. **Everything rests on one date in October.**

**Directional lean: 🔴 bearish next ~12 months · 🟢 constructive over 3–5 years.** The near term is all sentiment (a tape that pays only for announcements, and a hard date with no outside corroboration); the long term is a real, strengthening asset (the lease stack + demonstrably cheap financing). The four points behind this lean are at the bottom of this section.

---

#### ✅ What to watch — highest priority first

*Each line: the trigger · when · what a pass vs. a fail looks like.*

1. **Does the Oct-2026 NOI window hold? — next test 2026-08-06 (Q2 print).** ⚠️ *This is the whole thesis and the single fastest-acting invalidation.*
   - **Pass:** the Oct-2026 start carries forward unchanged for a second straight quarter (schedule has now survived two independent tests).
   - **Fail:** it slips by even a month in any deck → **Tripwire #1 FIRES** → pre-committed action is exit / re-underwrite.
   - **Why it's fragile:** the schedule is *company-reported only*, management guides to **contractual milestones, not rent commencement**, and ERCOT's 438 GW queue doesn't corroborate any specific Q4-2026 energization.
2. **Barber Lake Phase I delivery — ~Sep 2026.** First genuinely falsifiable delivery; 10-Q says rent commences Sep 2026. **Pass:** delivers on time. **Fail:** slips.
3. **Black Pearl initial rent — ~Oct 2026.** The first real rent dollar — the thesis's reason for existing. **Watch the ambiguity:** the final phase is ~Mar 2027 and Tripwire #1 is written against the *first* milestone, so phasing alone won't trip it.
4. **Third-campus financing — open, no date.** The question BTIG asked and management wouldn't answer. **Watch for:** an equity raise (would pressure **Tripwire #2**) vs. more cheap project debt (confirms the funding strength).
5. **ERCOT Batch Zero outcome — submissions closed 2026-07-10.** Gates ~2.0 GW of the pipeline. Reveille and Ulysses are already approved and **not** exposed.

#### 💲 Where the price sits

Fairly priced **on the market's own terms** — no multiple expansion (the third lease was added at the multiple already paid, EV/backlog ~1.22× → ~1.14×). You're paid the cohort multiple for cohort risk — no premium for counterparty quality, no discount for execution risk. The bull/bear split is a multiple debate: bulls say 20×+ NOI as the build de-risks; bears say 10–12× until first cash in 2027. *(Indicative — promotional source [T3].)*

#### 🔀 What would flip the read

- **→ bullish:** first rent recognized on schedule — the fundamental bucket finally contributes and the thesis stops being a promise.
- **→ bearish (confirmed):** the Oct-2026 window start moves by so much as a month in any deck.

#### Why bearish near-term, bullish long-term — the four points

*All synthesized from the analysis above; nothing new introduced here.*

1. **🔴 Market pays for announcements, not results — 12mo.** +23.5% on the third-lease announcement despite a 6.6× EBITDA miss, then **gave the entire premium back in three sessions** (−0.86% on 5/6 while peers rose +10% on Hut 8's news). No guaranteed lease cadence to keep feeding it → re-prices hard on the first quarter without one.
2. **🔴 The one hard date has thin, company-only corroboration — 12mo.** Oct-2026 window is self-reported, guided to milestones-not-rent, and un-corroborated by ERCOT. Tripwire #1 sits closer to its threshold than the clean pass suggests.
3. **🔴 Fundamentals contributed nothing, and the pre-rent trough deepened — 12mo.** $0 HPC revenue, mining down 41.7% QoQ by design, the OCF "turn" was an $83.3M payables build (real OCF ≈ +$8M), FY26 consensus revenue cut ~44%.
4. **🟢 The counterweight — the funding leg got materially stronger — 3–5yr.** Zero equity issued, $1.97B raised as project debt, Black Pearl's $2.0B oversubscribed 6.5× at 6.125%, bonds above par, revolver undrawn, a third IG hyperscale lease, and Fluidstack raised rather than stressed.

*Not a rating on the stock — a lean on what the print did to the thesis. Not financial advice.*

**Bottom line.** A quarter with **no bad news and no good news either** — $0 HPC revenue, a mining business being deliberately dismantled, an operating cash flow "turn" that was really unpaid contractor bills, and a 23% pop that the sector reclaimed in three sessions. What actually happened: **Cipher signed a third lease and proved it can raise debt cheaply, and the market shrugged and paid the same multiple.** The thesis is intact and entirely unresolved. **Everything still rests on a date in October.**

---

*Methodology — sources retrieved 2026-07-16, digest written 2026-07-17, quarter reported 2026-05-05. Three parallel sub-agents (numbers / call / sector cross-check), **all four passes on Opus** per §I.2. **`sec.gov/Archives` returned HTTP 403 to every automated attempt** — the income statement, adj. EBITDA bridge and balance sheet are primary-grade via GlobeNewswire's carriage of the EX-99.1 as issued (accession 0001819989-26-000025, filed 2026-05-05); cash-flow, debt-footnote and lease detail rest on filing-mirror extractions of the 10-Q (accession 0001819989-26-000028) whose **subtotals reconcile exactly to the balance sheet but whose component lines do not sum** — treat component detail as indicative. **The earnings decks were never opened** (IR site timed out); all deck figures — including the $11.4B backlog and the Oct-2026 NOI window — are **second-hand via coverage** and are corroborated across two independent sources but are not primary. Prior-quarter working-capital data is aggregator-sourced, validated against five independent primary ties (incl. 9M-2025 OCF summing to the 10-Q's $(153,506)K and FY2025 revenue to $223.95M). One transcript rendering (Motley Fool) contains a verifiable AWS/Fluidstack site swap; every load-bearing claim was cross-checked against a second rendering. Seeking Alpha's transcript is paywalled and was not accessed. Short interest is a Feb-2026 snapshot, not dated at the print. Reaction residuals are **estimates** (miner-cohort beta assumed ~1.3, not retrieved). Not financial advice.*

*Numbered caveats: **(1)** Whether a Q1 guide existed at the Q4'25 call — unresolved (search limit); the Δ in §1(a) is vs. consensus only. **(2)** $11.4B / $787M NOI / 700 MW — deck-via-coverage, absent from release text. **(3)** Fluidstack contract value conflicts: ~$3.0B/168 MW critical IT (secondary) vs. $3.8B/300 MW (news.md). **(4)** Revolver drawn vs. undrawn not disclosed in filings; short-term borrowings rose $317.6M unexplained (call says undrawn). **(5)** Power pipeline 4.2 GW (news.md) vs. "~3.3 GW" on the call. **(6)** Individual convert strikes per tranche not retrieved; blended ~$9.09 is derived. **(7)** Receivables concentration within the $8.5M HPC AR — no named split disclosed.*
