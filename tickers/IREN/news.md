---
company: "IREN Limited · NASDAQ"
blurb: "Renewable-powered data-center owner that pivoted from Bitcoin mining to an AI-cloud OPERATOR model — $13.1B of Microsoft/NVIDIA cloud contracts with ~$134M annualized recognized AI revenue; the debate is conversion: tranche acceptance, the uncontracted ARR slice, and dilution."
---

# IREN — IREN Limited (NASDAQ: IREN)

**Canonical deep-dive:** [`reports/2026-07-19.md`](reports/2026-07-19.md) (full-framework run, 2026-07-19). This file holds the monitoring state; the Edge and Tripwires below are the binding pre-committed triggers assessed on every whats-new / earnings-digest run.

## Thesis context (one-paragraph)
IREN is an Australian-incorporated, NASDAQ-listed (US domestic filer since FY2025) owner-builder of renewable-powered data centers — ~160MW of BC hydro sites, 750MW at Childress TX, and ~2GW at Sweetwater TX (Sweetwater 1, ~1.4GW, energized Apr 2026) — pivoting near-totally from Bitcoin mining (still 77% of Q3 FY26 revenue, being deliberately shut down at Childress with ~$520M further impairments flagged) into AI compute. Unlike its landlord peer cohort (CIFR/WULF/HUT/APLD sign 10–25-yr triple-net leases), IREN is an **operator**: it owns the GPUs (~$5.8B Dell orders) and sells cloud services — anchored by a **$9.7B/5-yr Microsoft contract** (signed 2025-11-02, four GB300 tranches at Childress, 20% prepaid per tranche) and a **$3.4B/5-yr NVIDIA contract** (signed 2026-05-07, ramp early 2027). As of 3/31/26 **zero Microsoft tranches were accepted, so $0 of the $9.7B is in RPO** (total RPO $710.3M); recognized AI Cloud revenue was $33.6M for the quarter vs. ~$3.1B contracted ARR and a "$3.7B ARR by end-CY2026" target whose remaining ~$1.8B is explicitly uncontracted. The GPU capex is ~96% funded (Fitch-A $3.65B GPU financing closed 6/1/26 + prepayments), cash was ~$2.6B (4/30/26), against $3.75B of converts (strikes $13.64–$85.63), a $6B ATM (~$5B remaining), and a share count up +38.5% YoY. The stock halved from ~$66 (early June) to $33.62 (7/17) in the chip-rout/"neocloud unwind," with ~24.6% of float short. The debate is conversion — acceptance milestones, the uncontracted slice, and dilution — not counterparty quality.

## Edge (variant view — what the crowd may have wrong)
*Verbatim from `reports/2026-07-19.md` §18:*

> The crowd is currently pricing IREN as a *failed landlord* — punishing it with a ~50% discount to the lease-signing cohort for lacking bond-like certainty — while the actual position is a *pre-revenue operator whose build is already ~96% financed at investment-grade cost against AAA/AA offtake*. The variant view must pick a side of one specific question: **is the $134M-recognized vs. $3.1B-contracted gap a timing artifact or a demand mirage?** The bullish variant: it is timing — prepayments are already landing on the balance sheet ($120.4M deferred revenue), the GPU capex is funded, acceptance is mechanical once Dell delivers, and the market is applying a demand-risk discount to what is actually schedule risk on an AAA counterparty's committed tranches. The bearish variant: the market is right about the wrong thing — Microsoft will deliver, but the *uncontracted* $1.8B and everything beyond tranche 4 lands into an AI-capex digestion, and the operator model's utilization risk shows up exactly when the mining cash flow that funds the bridge has been deliberately shut off. If you hold neither view with specificity — if your thesis is just "the contracts are real" — you own consensus with leverage, at 4× beta, into a tape that has stopped paying for announcements.

## Sector lens
*Assigned 2026-07-20 per `framework/sector-lens.md` §K.1, derived from `reports/2026-07-19.md` §5/§6/§10 and anchored against its §18. (Backfill: the 2026-07-19 seed omitted this section — Section K had merged only hours before that run, which applied the pre-K Step 4a. Derivation is from the same report; no new research.)*

- **`ai-dc-lessor`.** Channels: **peer-comp** (dominant) and **demand**. The market prices IREN against the miner-pivot landlord cohort — CIFR/WULF/HUT/APLD, with CIFR "the market's standard IREN pair-trade" (report §5) — plus the neocloud operators (CoreWeave, Nebius) that are its true model peers; the Edge's entire framing is the crowd mispricing IREN as a *failed landlord* at a ~50% discount to that cohort, so peer lease terms and neocloud funding/credit conditions re-mark IREN with no company event at all (the June–July "neocloud unwind" halving the stock is exactly this channel). Demand: Tripwires #1 and #2 turn on hyperscaler AI-capex follow-through — Microsoft tranche acceptance entering RPO, and whether the uncontracted ~$1.8B slice of the "$3.7B ARR" target lands into an AI-capex digestion (the Edge's bearish branch). The registry's power/interconnect watch items (ERCOT ILLE, Batch Zero) carry §10's regime residual: 75%+ of capacity is ERCOT-concentrated.
- **`btc-mining`.** Channel: **regime**. Legacy exposure being deliberately amputated (Childress mining shutdown, ~$520M further impairments flagged) but still 77% of Q3 FY26 revenue and the pre-AI-revenue opex bridge — Tripwire #4 turns on BTC sustained below ~$50K while mining still funds that bridge. **Sunset:** membership ends when mining stops funding the bridge (Childress wind-down complete / AI cloud revenue covering opex) — the same event that lapses Tripwire #4's premise, so per §K.1 the sector question rides on the audit's #4 expiry flag rather than a second clock.

## Tripwires (pre-committed exit / re-underwrite triggers)
*Verbatim from `reports/2026-07-19.md` §18 (primary tripwire + pre-committed secondaries). Reformatted 2026-07-20 into one bullet per numbered trigger (formatting only — text unchanged, per the §58 convention) and the `| # | Expires |` table appended per `framework/staleness-audit.md` §J.4; both were omitted at the 2026-07-19 seed.*

- **(1)** **A Microsoft tranche delivery/acceptance milestone slips — evidenced by the $9.7B failing to begin entering RPO by the FY2026 annual report (~Aug–Sep 2026), or management re-dating tranche commissioning beyond CY2026 on any call.** RPO is the un-spinnable number: signatures don't move it, only accepted delivery does. Pre-committed action: exit or fully re-underwrite on the first slip — do not average into a schedule miss on the #1 contract, because the entire financing stack (prepayments, the A-rated GPU debt, the ATM's viability) is sequenced off that schedule.
- **(2)** The end-CY2026 print shows the "$3.7B ARR" target abandoned, re-dated, or filled with undisclosed/startup-credit counterparties → re-underwrite (the growth leg is broken even if Microsoft performs).
- **(3)** Cumulative ATM issuance materially accelerates below ~$30/share (dilution into weakness — the pre-mortem spiral's first observable link) → exit.
- **(4)** BTC sustained below ~$50K while mining still funds the bridge (pre-AI-revenue opex cover breaks) → reassess sizing immediately.

| # | Expires |
|---|---|
| 1 | 2026-09-30 |
| 2 | 2027-02-28 |
| 3 | 2027-07-31 |
| 4 | 2027-07-31 |

## Recent News Log
*(Entry format: [`framework/latest-updates-workflow.md`](../../framework/latest-updates-workflow.md) §F.1 — the single source of truth. Tag only when an item actually bears on the sections above, using the closed vocabulary in §F.1 — `[EDGE+]`/`[EDGE−]` (binary — omit if neither) and `[TRIPWIRE #n — fires|early-warning|does not fire]`. Seeded 2026-07-19 from the initial full-report build.)*
