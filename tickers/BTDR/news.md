---
company: "Bitdeer Technologies Group · NASDAQ"
blurb: "Largest listed bitcoin miner by hashrate (73 EH/s self-mining) that designs its own ASICs, now an AI datacenter landlord on a $4.7B/16-yr Norway lease — funded by $1.92B of debt, $518M of it owed to the CEO's own affiliate and maturing before the lease pays."
---

# BTDR — Bitdeer Technologies Group (NASDAQ: BTDR)

**Canonical deep-dive:** [`reports/2026-08-06.md`](reports/2026-08-06.md) (full-framework seed run, 2026-08-06; first report for this ticker). Full-diligence snapshots land at `reports/<YYYY-MM-DD>.md`; this line links to the latest (resolved by glob). This file holds the monitoring state; the Edge and Tripwires below are the **binding** pre-committed triggers assessed on every whats-new / earnings-digest run.

*(Note: Cayman-incorporated, Singapore-HQ **foreign private issuer** — files 20-F/6-K, not 10-K/10-Q/8-K. Reported under IFRS through FY2025 and transitioned to **US GAAP effective 2026-01-01**, so FY2025 and Q1'26 figures are not directly comparable.)*

## Thesis context (one-paragraph)
Bitdeer is three businesses on one balance sheet: the largest bitcoin miner among US-listed names by operating hashrate (**73.0 EH/s self-mining, 102.0 EH/s total under management, June 2026**), one of only two listed miners that **designs its own ASICs** (SEALMINER, now 9.45 J/TH — at parity with Bitmain, not ahead), and as of 2026-08-04 an AI/HPC landlord on a **16-year, ~$4.7bn colocation lease** at Tydal, Norway with **Volta**, an NVIDIA Cloud Partner that emerged from stealth the same day with ~$300M of equity. The lease is well-drafted — ~$202/kW/month average, 3% escalators, ~90% NOI, campus wholly owned, no tenant warrants issued — but carries a **tenant no-fee termination at year 10** (honest committed value ~$2.9bn, not $4.7bn), its ~$1.3bn of J.P. Morgan-arranged letters of credit are **"anticipated," not executed**, and **$0 is recognized** (Phase 1 targets 2026-12-31). Against that: FY2025 operating cash flow **−$1.74bn** and FCF ≈ **−$2.0bn**, ~71% of it working capital going into SEALMINER wafers and chips; borrowings of **$1,920.1M at 3/31/26** against **$297.7M of cash and 31 BTC held**; and **$517.8M of that debt owed to BIT Group — an unrated private company chaired by CEO Jihan Wu, who controls 69.5% of the votes — falling due within twelve months, i.e. before Tydal pays a dollar.** The stock gapped **+13.7% on the lease announcement and closed flat**, then fell again through a Cantor upgrade. Sell-side is Buy with a $22.89 average against $11.06 spot, but the two freshest post-lease targets ($18 Cantor, $22 Needham) sit below it, and **43.18% of the float is short with shorts *adding* ~7.3M shares into the announcement**.

## Edge (variant view — what the crowd may have wrong)
*Derived 2026-08-06 from [`reports/2026-08-06.md`](reports/2026-08-06.md) §18 on the seed run. This Edge is the **narrowed, post-adversarial** version: the §L red team falsified the original draft's central claim (that the related-party debt was secured against the Norway/Tydal assets) by going to the 20-F pledge language, and it was withdrawn. See that report's "Adversarial review" block for the full reconciliation.*

> Twelve analysts averaging $22.89 and a 43%-short float are arguing about whether the Volta lease closes — whether the ~$1.3bn of letters of credit execute, whether a company that emerged from stealth on the day of the announcement can pay sixteen years of rent. **The variant view is that the lease is not what decides this equity over the next three quarters. The binding constraint is a maturity, not a milestone: $517,822k of debt owed to BIT Group — an unrated private company chaired by Bitdeer's own CEO — falls due within twelve months of 3/31/26, landing across Q4 2026 and Q1 2027, which is precisely the window *before* Tydal Phase 1 energizes (target 2026-12-31) and therefore before the lease pays a single dollar. In that same window Bitdeer must fund ~$500M of remaining Tydal capex. It holds $297.7M of cash and 31 bitcoin.** The affiliate has no comparably-sized third-party substitute, requires no default and no foreclosure to extract value, and negotiates across the table from a management team whose CEO chairs it and controls 69.5% of the votes on both sides — with **no fairness opinion, no independent committee and no disclosed arm's-length mechanism** anywhere in the record. The re-rate the market is waiting on is gated on the price of a rollover nobody outside the company will ever see quoted. **What the crowd has right, and this Edge does not dispute: the inventory is being absorbed (~74,000 rigs placed in Q2'26), the lease terms are genuinely good, and the operating execution is real.** The disagreement is narrow, dated and specific — it is about which line item resolves first.

## Sector lens
*Assigned 2026-08-06 per `framework/sector-lens.md` §K.1, derived from [`reports/2026-08-06.md`](reports/2026-08-06.md) §5/§6/§10 and anchored against its §18.*

- **`ai-dc-lessor` — primary.** Channels: **peer-comp** (dominant) and **demand**. Anchored to Tripwires **#1** and **#2**, both of which turn on lessor-complex variables (project-vs-related-party financing, LC execution, rent commencement). The peer-comp channel is demonstrated, not assumed: on **2026-07-29 BTDR fell 13.4%** and on **2026-07-30 it rose 24.7%**, both with **zero company news**, tracking CIFR (−14.3% / +28.3%) and IREN (~−14% / +27.4%) and the AI Infrastructure Growth Index (−11.13%). BTDR is priced as a levered expression of the AI-infra factor, **not** as a bitcoin proxy — bitcoin barely moved across both sessions.
- **`btc-mining` — secondary but not residual.** Channel: **demand** (hashprice and BTC are the direct revenue driver for ~78% of Q1'26 revenue), with **regime** secondary. Anchored to Tripwire **#5**, which turns explicitly on hashprice and self-mining gross margin. Sunset condition: this membership weakens if and when Tydal rent commences and mining revenue falls below ~50% of the total — the same event that expires Tripwire #5.
- **⚠️ Coverage gap flagged for a human decision, not resolved unilaterally.** Tripwire **#4** turns on **merchant ASIC vendor roadmaps** (a competitor shipping at or below 9.0 J/TH in volume — Bitmain, Auradine, MicroBT, Canaan, Block/Proto). No slug in the closed §K.2 registry carries ASIC-vendor roadmap events as a standing watch item: `btc-mining`'s watch items are BTC price, ETF flows, hashprice and miner-to-HPC pivots. **Recommendation: add "merchant ASIC vendor efficiency roadmaps and volume-ship dates (Bitmain, MicroBT, Canaan, Auradine, Block/Proto)" to `btc-mining`'s standing watch items in §K.2.** Per §K.3 widening is free and narrowing is dangerous, so this is a low-risk addition — but it is a framework edit and belongs to the human, not to this run. **Until it is made, Tripwire #4 has no routed search angle and will only be caught by chance.**

## Tripwires (pre-committed exit / re-underwrite triggers)
*Derived 2026-08-06 from [`reports/2026-08-06.md`](reports/2026-08-06.md) §18 on the seed run. Expiry dates in the table below (§J.4).*

Pre-commit to re-underwriting or exiting if ANY of these fire:

- **(1)** the **related-party maturity is rolled on value-transferring terms** — the ~$517.8M is refinanced with *additional* collateral pledged, an equity-linked or conversion feature attached, or a coupon more than ~200bp above the existing 9.0% + reference — **or** the drawn related-party balance exceeds **~$900M**. *(This is the Edge's own falsification test: if it rolls cleanly at market terms, the Edge was wrong and the affiliate is a feature, not a risk.)*
- **(2)** **Tydal Phase 1 fails to energize by 2027-01-31** (one month past the stated 2026-12-31 target), **or** the ~$1.3bn of letters of credit are still not disclosed as **executed** — rather than "anticipated" — by the Q3 2026 report.
- **(3)** **inventory absorption stalls:** two consecutive quarters in which inventory plus prepayments fail to decline **while** self-mining hashrate fails to rise — the rate of absorption falling below the rate of build — **or** any inventory write-down is taken.
- **(4)** **the moat leg breaks:** R&D stays below ~$25M per quarter for two consecutive quarters **while** a competitor ships at or below 9.0 J/TH in volume.
- **(5)** **hashprice sustains below ~$30/PH/s/day for a full quarter while self-mining gross margin remains negative.**

Any one = the thesis is impaired; decide the action now, not after the drawdown.

| # | Expires |
|---|---|
| 1 | 2027-06-30 |
| 2 | 2027-03-31 |
| 3 | 2027-06-30 |
| 4 | 2027-08-06 |
| 5 | 2027-06-30 |

### Rejected triggers
*Recorded because a rejected pre-commitment is itself a pre-commitment — it stops the same trigger being re-proposed later as though it were new.*

- **"Equity issued below the 2032 converts' $9.925 conversion price"** — **rejected.** It already happened (5,503,030 Class A at **$7.94** on 2026-02-19) without the thesis being wrong. It describes Bitdeer's normal financing behaviour, not a falsification. There is also a live **$700M ATM** ($130.4M gross drawn), and ATM shares clear at prevailing market prices — so no raise is "priced off" the balance sheet in the way an earlier draft of this Edge assumed.
- **"Tydal Phase 1 slips past 2027-03-31"** — **rejected.** 2027-03-31 is the **Phase 2** target; that wording allowed a three-month cushion past even the later milestone and could not have bitten. Replaced by the 2027-01-31 test in Tripwire #2.

## Recent News Log
*Canonical entry format: `framework/latest-updates-workflow.md` §F.1 — most recent first. Every item is assessed against the Edge and the numbered Tripwires above; do not restate the format here.*

*(No entries yet — this file was seeded by the 2026-08-06 deep-dive. The first whats-new run will populate it. Note for that run: **Q2 2026 results are due 2026-08-10, 07:00 ET**, and Tripwires #3, #4 and #5 all read directly off that balance sheet.)*
