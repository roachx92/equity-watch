---
company: "Credo Technology · NASDAQ"
blurb: "SerDes-based interconnect for AI datacenters — the AEC leader at 68% gross margin, priced for ~45% long-term compounding, in a socket count NVIDIA's rack architecture decides."
---

# CRDO — Credo Technology Group Holding Ltd (NASDAQ: CRDO)

**Canonical deep-dive:** [`reports/2026-08-22.md`](reports/2026-08-22.md) (seed report, 2026-08-22 — first full-framework run on this ticker). Full-diligence snapshots land at `reports/<YYYY-MM-DD>.md`; this line links to the latest (resolved by glob). This file holds the monitoring state; the Edge and Tripwires below are the **binding** pre-committed triggers, derived from that report's §18 and seeded here on 2026-08-22.

## Thesis context (one-paragraph)
Credo sells signal integrity: a **224G/lane PAM4 SerDes** monetised as **Active Electrical Cables** (copper cables with retimer silicon in the connector — the overwhelming majority of revenue), **optical DSPs and retimers**, and **licensable SerDes IP/chiplets** on TSMC N3. FY2026 (ended 2026-05-02) revenue was **$1,335.1m, +205.7%**, at **68.0% gross margin**, with **$445.0m GAAP operating income**, **~$407m free cash flow**, **$1.44bn cash and zero debt**. Over 99% of the FY26 revenue increase came from AEC volume at hyperscale datacenter customers. Concentration is severe but improving by *addition*: on a contracting-party basis Customer A is **49%** of revenue and 53% of receivables with B at 32%; on an end-customer basis D/B/E are **33/32/19%**, and the top end-customer fell from 63% to 33% while growing ~60% in dollars. There are **no minimum purchase commitments** and RPO is $31.9m, against **$359.9m of Credo's own non-cancellable purchase obligations**. At **$230.57** (2026-08-21) the stock trades at **37.5× forward earnings — third-lowest in its peer set** — while embedding ~+83% implied NTM revenue growth and ~45% implied long-term EPS CAGR. The debate is not quality or solvency; it is **duration**.

## Edge (variant view — what the crowd may have wrong)
*Derived 2026-08-22 from [`reports/2026-08-22.md`](reports/2026-08-22.md) §18 and seeded here (seed run — nothing was overwritten).*

> Your edge — what do you believe that the crowd doesn't? The crowd debates **"copper versus optics"** and treats it as a binary that Credo either wins or loses. That framing is wrong in both directions, and the sell-side's 56%-of-average target dispersion is evidence nobody has resolved it. The variant view is that **the copper-versus-optics question is already settled and is not the risk**: copper wins inside ~3 metres on power, permanently, and NVIDIA says so explicitly — while optics wins beyond ~7 metres, equally permanently. Credo's franchise does not live or die on that boundary moving. **It lives or dies on how many 2-to-7-metre links exist per unit of compute — and that is an architecture decision made by NVIDIA, not a physics outcome.** MGX's cable-free PCB midplane removes AEC sockets *without any optics involved at all*, which means the most-discussed threat (CPO) is not the operative one and the operative one (rack topology) is barely discussed. The corollary is that the FY27 optical guide is not a hedge against CPO — it is a hedge against **Credo's own sockets being designed out of the rack**, which is why management spent ~$750–770m on it. If you do not hold a specific view on rack topology two generations out, you do not have an edge here; you are underwriting a physics debate that was already decided and missing the architecture one that wasn't.

## Sector lens
*Assigned 2026-08-22 per `framework/sector-lens.md` §K.1, derived from `reports/2026-08-22.md` §5/§6/§10 and anchored against its §18.*

- **`ai-optics` — sole.** Channels: **demand** (dominant), **peer-comp** and **supply**. Anchoring is explicit: **Tripwire #4** is FY2027 optical revenue tracking below ~$400m — a direct slug variable, in a market where Marvell holds 60–70% and Broadcom >30%. **Tripwire #5** is NVIDIA rack architecture eliminating third-party AECs or excluding Credo from a major interconnect ecosystem — the slug's "NVIDIA architecture shifts" watch item stated verbatim. **Tripwire #2** (a licensed cable prime or Astera winning a dual-source) is a peer-set variable. The Edge itself turns on rack topology, which is the slug's newly added watch item. **Supply** matters unusually here: LightCounting reports InP/EML orders running ~30% above output, a constraint that mechanically *preserves* copper demand.
- **The slug was widened on 2026-08-22 in the same commit that added this ticker** (§K.2), from "datacom optical transceivers and components" to cover the **copper interconnect that competes with them at short reach**. Copper and optics are one competitive system — an AEC and an AOC bid for the same 2–7 m link — so a slug covering only the optical half would have left Tripwire #2's exact test unsearched.
- **Shares this slug with COHR and AAOI — and the signs can invert.** A CPO or LPO adoption milestone is `[EDGE−]`-adjacent here (it removes DSP attach and, eventually, copper sockets) but can be `[EDGE+]` for an optical-component supplier positioned to sell into it. Per §K.5, assess against *this* ticker's §18, never a sector-level sentiment read.

## Tripwires (pre-committed exit / re-underwrite triggers)
*Derived 2026-08-22 from [`reports/2026-08-22.md`](reports/2026-08-22.md) §18. Trigger identity (the numbering) is stable across any future promotion. Expiry dates in the table below (§J.4).*

Pre-commit to re-underwriting or exiting if ANY of these fire:

- **(1)** the **2026-09-01 Q1 FY27 print** lands below the $465m guide floor, **or** management withdraws, lowers, or fails to reaffirm the **>80% FY27 growth** guide, **or** declines to give a 2H shape that makes it arithmetic — confirming the FQ3 spike was a pull-forward.
- **(2)** a **licensed cable prime (Amphenol, TE Connectivity or Molex) or Astera Labs is disclosed or credibly reported to have won a dual-source or design-win at any customer representing ≥19% of Credo revenue** — the commoditisation mechanism in the Pre-Mortem.
- **(3)** **GAAP gross margin prints below 65%** in any quarter, or management guides below 65%, signalling AEC price competition or an adverse optical mix.
- **(4)** **FY2027 optical revenue tracks below ~$400m** on a run-rate basis by the FQ3 FY27 print (~March 2027), i.e. the >$600m guide misses by a third or more — the optical conversion failing.
- **(5)** **NVIDIA discloses a rack architecture that eliminates third-party AECs from the scale-out tier**, or Credo is publicly excluded from a major NVIDIA interconnect ecosystem while a named rival is included.

Any one = the thesis is impaired; decide the action now, not after the drawdown.

| # | Expires |
|---|---|
| 1 | 2026-09-30 |
| 2 | 2027-08-31 |
| 3 | 2027-08-31 |
| 4 | 2027-03-31 |
| 5 | 2027-12-31 |

## Recent News Log
*(Entry format: [`framework/latest-updates-workflow.md`](../../framework/latest-updates-workflow.md) §F.1 — the single source of truth, including its ~1,200-character ceiling. Tag only when an item actually bears on the sections above, using the closed vocabulary in §F.1 — `[EDGE+]`/`[EDGE−]` (binary — omit if neither) and `[TRIPWIRE #n — fires|early-warning|does not fire]`. Seeded 2026-08-22 from the initial full-report build; no items logged yet.)*
