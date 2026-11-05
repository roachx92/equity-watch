---
company: "ASE Technology Holding · NYSE / TWSE"
blurb: "The world's largest chip packager and tester, re-rated from ~7x peak earnings to ~20x a 2027 estimate on an AI margin ramp above its own stated 30% ceiling — with ~NT$54B of undisclosed-terms customer advances behind it."
---

# ASX — ASE Technology Holding Co., Ltd. (NYSE: ASX · TWSE: 3711)

**Canonical deep-dive:** [`reports/2026-10-19.md`](reports/2026-10-19.md) (full deep-dive, diligence window 2026-10-19 — **first coverage, no predecessor**). Resolved by glob over `reports/*.md`. This file holds the monitoring state; the Edge and Tripwires below are the **binding** pre-committed triggers assessed on every whats-new / earnings-digest run. Seeded 2026-10-19 from that report's §18.

**Filer regime — read this before any filing-based assessment.** ASE is a Taiwanese **foreign private issuer**: **20-F annually and 6-K for interims** (quarterly results releases, decks, monthly revenue, and the auditor-reviewed quarterly financial statements, which lag the results by ~3 months). It reports **Taiwan-IFRS in NT$**; **1 ADS = 2 common shares**, and the ADS has traded at a ~5% discount to the local line. Annual XBRL facts use the **`ifrs-full`** taxonomy (`scripts/facts.py --taxonomy ifrs-full`); interim figures come from 6-K HTML. **Forms 3/4 have been filed since 2026-03-18** under the Holding Foreign Insiders Accountable Act — a change in Section 16 law, **not** a loss of FPI status. Read settled closes for both lines: `scripts/prices.py ASX` and `scripts/prices.py 3711.TW`.

## Thesis context (one-paragraph)
ASE is the largest outsourced semiconductor assembly and test (OSAT) company — roughly twice Amkor's packaging-and-test revenue — plus USI, an EMS arm that is a third of revenue at a ~2–3% operating margin. AI has made it the main partner and overflow capacity for the back half of TSMC's CoWoS process: **leading-edge advanced packaging and test (LEAP) revenue went ~US$0.6B (2024) → ~US$1.6B (2025) → "tracking ahead" of US$3.5B (2026)**, with an aim to **double again in 2027**, and **ATM gross margin rose from 23.8% (FY2025) to 27.3% (2Q26)**, with 28–29% guided for 3Q26 and 4Q26 expected to exceed the **30% "structural ceiling"** management itself names. **3Q26 revenue was NT$244.16B (+44.8% YoY), ATM +20.1% QoQ against an 11–13% guide.** The ramp is being bought: **2026 capex ~US$10.5B (~4x depreciation)**, 1H26 free cash flow −NT$40.5B closed entirely by new borrowing, net debt/equity 0.40 → 0.47 in one quarter, a US$1B zero-coupon convertible (conversion NT$927.20) and a NT$50B syndicated loan. The FY2025 20-F newly discloses **customer advance payments under long-term agreements**; the liability lines that hold them rose **~NT$7B (12/2024) → ~NT$61B (3/2026)** non-current, contributing 22% of FY2025 and 67% of 1Q26 operating cash flow — counterparties and prices undisclosed. Concentration: one unnamed customer (likely Apple, unconfirmed) was 25.0% of FY2025 revenue; NVIDIA reaches ASE mostly through TSMC and is not named. TSMC's CEO called the back-end gap "still quite big" on 2026-10-15. The local line settled at **NT$670 (2026-10-19)** and the ADS at **$39.53 (2026-10-16)**, after a 17% three-session, sector-wide drop from the $47.60 high — **~49x trailing EPS and ~20x BofA's 2027E, against 6.5–7.6x at the 2021–22 earnings peak**. The debate is durability, not demand.

## Edge (variant view — what the crowd may have wrong)
*Seeded **2026-10-19** from [`reports/2026-10-19.md`](reports/2026-10-19.md) §18, verbatim. First coverage — nothing superseded. The mandatory §L adversarial pass was aimed at the **draft** Edge and found a real problem: the draft claimed ASE was self-funding its AI capacity while NVIDIA pre-paid rivals, which the FY2025 20-F's new Note 37(e) advance-payment disclosure contradicts from primary source; TSMC's 2026-10-15 call also contradicted the draft's "shortage closing" premise. The Edge below was rebuilt around what the filings show — the report's Sources, methodology & caveats records the reconciliation.*

> The consensus reads ASE's AI ramp as a structural margin story: leading-edge advanced packaging and test (LEAP) revenue from ~US$1.6B (2025) to >US$3.5B (2026) with a stated aim to double again in 2027, lifting ATM gross margin from 23.8% (FY2025) to 27.3% (2Q26), 28–29% guided for 3Q26 and >30% expected in 4Q26 — and it is paying ~20x a 2027 estimate that is 3.7x FY2025 earnings, against 6.5–7.6x at the last earnings peak. **What the consensus does not price is that a material part of this ramp is pre-sold, and pre-sold capacity has a different earnings shape from scarce capacity.** ASE's FY2025 20-F newly discloses long-term customer agreements with advance payments, and the liability lines that hold them rose from ~NT$7B (12/2024) to ~NT$61B (3/2026) non-current — roughly NT$54B (≈US$1.7B) of cash received for capacity not yet delivered, from customers ASE does not name, at prices it does not disclose.
>
> **So the differentiated call is this: the variable that decides the equity is not the LEAP headline — it is what the advances do next.** They have flattered reported cash flow (22% of FY2025 operating cash flow, 67% of 1Q26's; ex-advances, 1Q26 OCF was ~NT$12B against NT$44B of capex payments), and as they are worked off against future revenue, 2027–28 revenue arrives without matching cash — just as the US$10.5B 2026 build adds an estimated NT$34–47B a year of depreciation. And capacity that customers pre-pay is capacity whose price was fixed when it was scarce: management's own "structural ceiling" of 30% ATM margin, which 4Q26 is expected to exceed, is more likely the negotiated top of a cycle than the floor of a new one. The market is capitalising contracted shortage pricing as franchise pricing.
>
> **What this Edge explicitly does not claim.** It does not claim AI demand fails — TSMC's CEO called the back-end gap "still quite big" on 2026-10-15. It does not claim TSMC is reclaiming work — outsourcing is widening. It does not claim the advances are bad: they reduce volume risk, and they are the reason this is a re-rating of a profitable franchise rather than a capacity gamble. And it does not cover testing, which grows with die count independently of the CoWoS shortage. **It claims that the margin and cash-flow path the price assumes is the least certain part of the story, and that the evidence on it — the advance balance and the post-ceiling margin — arrives over the next four prints.**

## Sector lens
*Assigned 2026-10-19 per `framework/sector-lens.md` §K.1, derived from [`reports/2026-10-19.md`](reports/2026-10-19.md) §5/§6/§10 and anchored against its §18.*

- **`adv-packaging` — primary, and the only slug assigned.** The §K.2 scope names the OSAT tier and ASE (ASX) explicitly, so **no new slug needed defining**. Channels, in order of strength:
  - **demand.** NVIDIA / custom-ASIC accelerator volume through **TSMC's CoWoS capacity and its back-end handoff** (oS, CoW overflow, CoWoP) — the variable behind Tripwire **#1** and the Edge's margin path.
  - **peer-comp.** The OSAT and test group re-prices together: on 2026-10-15 ASE, KYEC, Powertech, Advantest and ASMPT fell 8–15% with no company news. Amkor's margins, capex and **customer prepayments** (NVIDIA ~US$1.5B) and KYEC's NVIDIA test prepayment are the direct comps for the Edge's advance-payment mechanism and for Tripwires **#2**/**#3**.
  - **supply.** TSMC's own CoWoS expansion (and Intel EMIB-T as a second source) is competing capacity — the shortage-closure path the pre-mortem turns on (Tripwires **#1**, **#3**).
  - **regime.** AI-complex and memory sell-offs move the name on sympathy (§K.2's demonstrated regime-beta channel); log them only under §K.6.
  - **Sunset condition: none** — the AI back-end is the thesis.
- **No second slug.** `ai-optics` was tested (ASE ships co-packaged optics in small volume around year-end 2026) but no numbered Tripwire or Edge branch turns on an optics variable. `ai-dc-lessor` is a demand aggregate one step further removed (hyperscaler capex reaches ASE only through NVIDIA/TSMC). Recorded here so the absence is a decision rather than an oversight.

## Tripwires (pre-committed exit / re-underwrite triggers)
*Seeded 2026-10-19 from [`reports/2026-10-19.md`](reports/2026-10-19.md) §18 — verbatim, one bullet per trigger (a formatting change only). Trigger identity (the numbering) originates here. Expiry dates in the table below (§J.4).*

Pre-commit to re-underwriting or exiting if ANY of these fire:

- **(1)** **ASE withdraws or cuts its aim to double LEAP revenue in 2027** at any results call, **or** 2026 LEAP finishes below US$3.5B, **or** 2027 LEAP finishes below 2x 2026, **or** ASE or TSMC discloses a reduction in TSMC's handoff of CoW or on-substrate work to ASE/SPIL. **Committed action: re-underwrite** — the demand leg of every scenario above rests on it.
- **(2)** **The advance balance declines for two consecutive quarters while quarterly equipment capex stays at or above US$1.5B** — measured on other current plus other non-current liabilities in the reviewed financial statements. Customers would be consuming pre-paid capacity without renewing it while ASE keeps building. **Committed action: re-underwrite toward the bear case.**
- **(3)** **ATM gross margin below 26% for two consecutive quarters while ATM revenue is still growing year on year** — depreciation outrunning price, not a demand drop. **Committed action: exit or re-underwrite; do not wait for the full-year print.**
- **(4)** **Any primary equity issuance** (cash capital increase, GDR or placement — excluding conversion of the existing NT$927.20 convertible and employee awards) **or net debt/equity above 0.65 at any quarter-end.** **Committed action: re-underwrite** — the build would be outrunning both the cash flow and the customer funding.
- **(5)** **[UPWARD — re-underwrite, do not exit]** if **ATM gross margin is at or above 30% in each of two consecutive quarters in 2027 *and* operating cash flow excluding the change in other operating liabilities exceeds PP&E cash capex over the same two quarters**, the Edge is falsified on its own terms: margins would be holding after the ceiling *and* the core business would be self-funding without the advances. **Committed action: re-underwrite upward.**

Any one of #1–#4 = the thesis is impaired; #5 vindicates it — decide the action now, not after the drawdown.

| # | Expires |
|---|---|
| 1 | 2028-03-31 |
| 2 | 2027-12-31 |
| 3 | 2028-03-31 |
| 4 | 2027-10-31 |
| 5 | 2028-03-31 |

**Expiry basis (§J.4).** **#1** runs through the FY2027 print (~Feb 2028), when 2027 LEAP against 2x 2026 is first measurable. **#2** is a ~14-month review horizon over five quarters of reviewed balances (the reviewed statements lag results by ~3 months). **#3** and **#5** are defined on 2027 quarters, so they resolve with the FY2027 print. **#4** is a ~12-month review horizon covering the capex peak.

### Change log
*Per §J.4 — the pointer, not the argument. Full reasoning for each change is in the superseding report's Refresh Provenance block.*

- **2026-10-19** — **initial seed.** Edge and Tripwires #1–#5 established from [`reports/2026-10-19.md`](reports/2026-10-19.md) §18. First coverage; nothing superseded, so there is no provenance block in that report (§J.7 applies only to a report with a predecessor).

## Recent News Log
*Newest first. Entry format is the canonical spec in `framework/latest-updates-workflow.md` §F.1 — apply it as written, do not restate it. Every entry carries its §18 assessment: `[EDGE+]` / `[EDGE−]`, and `[TRIPWIRE #n — fires | early-warning | does not fire]` for each trigger touched.*

*(Empty — seeded 2026-10-19. The first whats-new run on ASX appends here.)*
