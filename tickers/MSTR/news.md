---
company: "Strategy Inc. · NASDAQ"
blurb: "The world's largest corporate Bitcoin holder (~843,775 BTC) wrapped in a convert/preferred/ATM capital-markets machine — a leveraged, premium-to-NAV claim on Bitcoin. Its defining mNAV premium has collapsed from ~2.6x (2024) to a discount (common trades ~0.65x its look-through BTC); in July 2026 the company began selling BTC to fund preferred dividends. The debate is whether the reflexive flywheel restarts or the discount becomes permanent."
---

# MSTR — Strategy Inc. (formerly MicroStrategy Incorporated) (NASDAQ: MSTR)

**Canonical deep-dive:** [`reports/2026-07-21.md`](reports/2026-07-21.md) (initial full-framework build, 2026-07-21). Full-diligence snapshots land at `reports/<YYYY-MM-DD>.md`; this line links to the latest (resolved by glob). This file holds the monitoring state; the Edge and Tripwires below are the **binding** pre-committed triggers assessed on every whats-new / earnings-digest run.

*(Note: legal name changed from "MicroStrategy Incorporated" to "Strategy Inc." effective 2025-08-11; the "Strategy" brand rolled out Feb 2025; Class A common still trades as MSTR.)*

## Thesis context (one-paragraph)
Strategy is not a software company that owns Bitcoin; it is the largest corporate Bitcoin holder on earth — **843,775 BTC (~$54–56B market value, avg cost ~$75,476) as of 2026-07-19** — wrapped in a five-instrument capital-markets engine (common ATM, ~$8.2B convertible notes, and five perpetual-preferred series STRK/STRF/STRD/STRC/STRE) that issues capital to buy more BTC. A ~$477M-revenue, roughly break-even enterprise-analytics business sits underneath and is ~0.8% of BTC carrying value — the equity story is entirely the treasury and its **mNAV premium** (market cap ÷ BTC NAV), which *was the product*: above 1.0x it let the company issue equity accretively, raise Bitcoin-per-share, and reinforce the premium. In mid-2026 that flywheel **inverted**: the premium collapsed from ~2.6–2.8x (late 2024) to a discount (common ~0.65x equity-only, ~1.0x enterprise), BTC fell ~48% from its ~$126K Oct-2025 high to below the ~$75.5K cost basis, and on **2026-07-06 the company sold BTC for the first time since 2022** (~3,588 BTC, at a loss) to fund a ~$1.0–1.8B/yr preferred-dividend bill its software business cannot cover — now bridged by a ~$3.2B USD Reserve and continued ATM issuance, not operations. The debate is not quality vs. price; it is **durability**: whether this is an oversold sentiment dislocation that mean-reverts, or the arithmetic of a levered, fixed-charge closed-end fund whose access to accretive capital is gated by a premium the spot ETF (IBIT) has structurally capped and that has now disappeared. There is no forced-liquidation trigger (unsecured debt, perpetual/discretionary preferred), so the floor is a distressed discount-to-NAV, not zero.

## Edge (variant view — what the crowd may have wrong)
*Derived 2026-07-21 from [`reports/2026-07-21.md`](reports/2026-07-21.md) §18 at the initial full-report build (SEED). Binding until an explicit human decision changes it.*

> The crowd is having the wrong debate. Bulls watch "is the premium high?" and bears say "just buy IBIT" — **both treat the sub-1.0x mNAV as a *sentiment* reading that mean-reverts.** The variant view is that **the premium and the funding model are one mechanism, and it has crossed a structural threshold into reflexive reverse**: below ~1.0x, ~$1.0–1.8B/yr of *senior, mostly-fixed* preferred charges must be funded by issuing common *below* NAV (deepening the discount) or selling BTC (shrinking the NAV backing) — so the discount is not obviously temporary; it can self-perpetuate like a badly-structured closed-end fund, and the spot ETF has permanently removed the access-scarcity that justified any premium at all. But the *equal-and-opposite* differentiated insight is that management retains genuine release valves the bears ignore — **STRD is non-cumulative, STRK pays dividends in stock, STRC resets monthly, and the debt is unsecured and covenant-light** — so there is no death-spiral to zero either; the floor is a discount to a still-tens-of-billions BTC pile, not a wipeout. **The real edge is a specific, defensible view on whether that dividend discretion is enough to prevent a discount from becoming permanent — held jointly with a view on the BTC price path over the Sept–Dec 2026 window (Q2 print, S&P 500 decision, first convert call, Mt. Gox overhang).** If you do not hold both, you have no edge here; you are paying par (or a small enterprise premium) for a levered BTC position with negative carry from the preferred stack, and the discount on the common is the market telling you the spot ETF does it cheaper.

## Sector lens
*Assigned 2026-07-21 per `framework/sector-lens.md` §K.1, derived from `reports/2026-07-21.md` §5/§6/§10 and anchored against its §18. The `btc-treasury` slug is defined in §K.2 in this same commit (a genuinely new sector — a treasury company has no hashpower and is priced on mNAV, not hashprice, so `btc-mining` does not fit).*

- **`btc-treasury` — primary (sole).** Channels: **regime** (dominant) + **peer-comp** + **demand**. Bitcoin's price is the master variable driving every asset, liability and the premium (regime — anchors Tripwire #4). The mNAV premium re-rates off the whole corporate-BTC-treasury cohort — Metaplanet, Twenty One/XXI, Strive/ASST and MARA-treasury all de-rated to discounts together in 2026, dragging MSTR (peer-comp — anchors Tripwire #1). Spot-BTC-ETF flows (IBIT) are the disintermediating demand aggregate that structurally caps the premium (demand — bears on the Edge). No sunset: the membership is the thesis, not a temporary condition.

## Tripwires (pre-committed exit / re-underwrite triggers)
*Derived 2026-07-21 from [`reports/2026-07-21.md`](reports/2026-07-21.md) §18/§8 at the initial build (SEED). Binding and pre-committed; only an explicit human decision changes them. Expiry dates in the table below (§J.4).*

Pre-commit to re-underwriting or exiting if ANY of these fire:

- **(1)** **mNAV holds below ~1.0x (enterprise) / the common stays at a discount for a full quarter** while the company funds preferred dividends primarily by selling BTC or issuing common below NAV — the reflexive flywheel has *structurally inverted*. Action: re-underwrite as a de-levering closed-end fund (value on BTC-per-share and a discount, not a compounding premium).
- **(2)** **Accelerating forced BTC sales** — BTC sold in two or more consecutive months beyond the initial 2026-07-06 ~3,588 BTC to fund dividends/interest, **or** the USD Reserve runway falls below ~6 months without replenishment — the "never sell" model is permanently broken and the NAV backing is actively shrinking. Action: exit / re-underwrite; the collateral is being consumed to pay carry.
- **(3)** **Distressed preferred funding** — a preferred-dividend deferral (invoking STRD non-cumulative / board discretion), a STRC monthly reset above ~13–14%, or STRK dividends shifting to stock-settlement — the funding market is demanding a distressed yield or the company is conserving cash. Action: treat as a credit event on the capital structure.
- **(4)** **Bitcoin breaks and holds materially below the ~$75,476 cost basis toward/below the prior ~$58K low** (e.g. sustained below ~$55K) while the preferred stack must still be serviced — the master-counterparty asset is impaired below the level that keeps the stack self-sustaining. Action: re-underwrite the dividend bridge.
- **(5)** **An existential non-price event** — a custody loss/failure at Coinbase/Anchorage/Fidelity, an Investment Company Act (40-Act) reclassification, or a Saylor key-person/control discontinuity (departure/incapacity triggering the Class B→A collapse). Action: exit.

Any one = the thesis is impaired; decide the action now, not after the drawdown.

| # | Expires |
|---|---|
| 1 | 2027-07-21 |
| 2 | 2027-07-21 |
| 3 | 2027-07-21 |
| 4 | 2027-07-21 |
| 5 | 2027-07-21 |

## Recent News Log
*(Entry format: [`framework/latest-updates-workflow.md`](../../framework/latest-updates-workflow.md) §F.1 — the single source of truth. Tag only when an item actually bears on the sections above, using the closed vocabulary in §F.1 — `[EDGE+]`/`[EDGE−]` (binary — omit if neither) and `[TRIPWIRE #n — fires|early-warning|does not fire]`. Seeded 2026-07-21 from the initial full-report build; no news items logged yet — the first whats-new run will populate this.)*
