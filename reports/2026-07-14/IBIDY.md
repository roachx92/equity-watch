# IBIDY — Ibiden Co., Ltd. (TSE: 4062 / OTC ADR: IBIDY) — Deep Dive

**Date:** 2026-07-14  ·  **Reference price:** ¥19,215 (TSE 4062, intraday 2026-07-15 JST; prior close ¥20,240 on 2026-07-07) / ADR IBIDY ~$41 (approx — depositary ratio unreconciled, treat as stale)  ·  **Status:** final

> Full-diligence report applying `framework/deep-dive-template.md` (Sections B/C/D/G/H) under `framework/standing-rules.md`. Built from four parallel diligence work-streams (primary filing, counterparty, sector, competitive-landscape). Point-in-time figures are dated; estimates and opinions are labelled; unverifiable items are flagged. **Not financial advice — informational research tooling only.**

---

## Executive summary (see §15 for the full synthesis)

Ibiden is the leader in the highest-complexity organic **ABF FC-BGA package substrates** that sit under high-end CPUs and, increasingly, AI GPUs/accelerators. The franchise is genuinely first-rate; the debate is **price and the glass-substitution clock**, not quality. Two hard facts anchor this snapshot, both verified against the FY3/26 securities report (filed 18 Jun 2026):

1. **The customer base has inverted to AI.** NVIDIA is now #1 at **29.4%** of FY3/26 net sales (¥122,470M), overtaking Intel at **18.1%** (¥75,319M) — figures confirmed against primary filings, not analyst estimates.
2. **The "pre-funded capex" narrative is prospective, not yet visible.** The balance-sheet "advances received" line actually *fell* YoY to **¥80,950M** (from ¥92,084M) at 31 Mar 2026. Customer pre-payment of the ¥500B FY26–28 build is a forward story reported by trade press, not something already sitting on the balance sheet — the single most important nuance in this report.

The stock has run ~478–518% over the trailing year (52-wk range ¥3,032–¥27,480) and trades ~**39.6x EV/EBITDA** — richly valued on any historical frame. The variant view (the Edge) is that the market over-fears glass-core as a clean existential threat when Ibiden is inside TSMC's glass (CoPoS) program as a build-up partner; the diligence broadly supports that framing while adding a genuine, already-visible erosion signal: Ibiden's share of the very-highest-end AI-server substrate has reportedly slipped from ~85% (2023) toward ~55% (2026) as Unimicron qualifies.

---

## 1. Business model & role in the value chain

Ibiden makes the **organic ABF FC-BGA package substrate** — the large, high-layer-count (14–20+ layer) organic laminate that carries a flip-chip die (or a CoWoS/CoWoS-L module) and fans its I/O out to the motherboard BGA. It sits directly beneath the most advanced logic in the stack: the substrate is the base of the package, under the silicon interposer / RDL and the dies. In the AI-accelerator value chain the flow is: TSMC fabs and packages the GPU (CoWoS) → the packaged module is mounted on an Ibiden FC-BGA substrate → the substrate goes on the board. Ibiden does **not** sell to TSMC; it sells the substrate to the chip vendor (NVIDIA, Intel, AMD), so its demand is a derivative of accelerator/CPU unit volume × substrate area × ASP.

**Reportable segments (FY3/26, primary tanshin filed 11 May 2026):**

| Segment | Net sales | Segment profit | Margin | YoY sales |
|---|---|---|---|---|
| **Electronics** (IC package substrates / FC-BGA) | ¥243,316M | ¥45,248M | **18.6%** | +23.4% |
| **Ceramics** (DPF/GPF auto filters) | ¥82,554M | ¥7,646M | 9.3% | −1.8% |
| **Others** | ¥90,330M | ¥8,964M | 9.9% | +2.5% |
| **Consolidated** | ¥416,201M | ¥62,027M | 14.9% | +12.7% |

Electronics is the entire growth-and-margin story (segment margin 13.6%→18.6% YoY) and carries ~73% of consolidated segment profit. Ceramics margin *collapsed* 14.5%→9.3% on soft auto/EV-transition demand plus a ¥2,024M impairment — a reminder that the legacy business is cyclical and currently a drag, not a cushion.

*Source tier: primary Ibiden tanshin/securities report [P].*

## 2. Recent catalysts

- **2026-06-16 — TSMC discloses CoPoS glass-substrate validation, names Ibiden (with Innolux) as build-up partner.** 3-layer design, 0.8mm glass core between two ABF build-up layers; validation showed warpage (COP) −16%, effective CTE −19%, modulus +31%, resistance −27%, inductance −42%. TSMC HVM target ~4Q28–1Q29; Ibiden's own roadmap lists glass-core at CY2030. (DigiTimes, JPCA Show; corroborated Kuo/X — trade press [T].) *This is direct support for the Edge.*
- **2026-07-01 — NVIDIA reportedly scraps 4-die Rubin Ultra design over CoWoS-L substrate warpage**, reverting to a dual-die package; glass CoPoS pilot "not before end-2026," HVM "late 2028–2029." Evidence that organic ABF is hitting a complexity ceiling at the frontier — and that the glass clock keeps slipping past 2028 (favourable to the Edge). (Tom's Hardware, TechTimes [T].)
- **2026-07-06 — Unimicron seeks up to $1.4B via GDS offering** to fund raw-material procurement and capacity, after a >700% 12-month run. A well-funded challenger scaling into Ibiden's segment (Bloomberg [T]).
- **2026-05-11 — FY3/26 full-year results:** net sales ¥416.2B (+12.7%), operating profit ¥62.0B (+30.3%), net profit ¥63.7B (+89.0%, aided by a ¥49.4B securities-sale gain). FY3/27 guidance: sales ¥500B (+20.1%), OP ¥90B (+45.1%) [P].
- **2026-02 — ¥500B FY26–28 capex program** to lift generative-AI substrate capacity to ~2.5× by FY2028; first phase ~¥220B at the Gama plant (Cell 6), mass production FY2027+ [P].
- **Upcoming — Q1 FY3/27 results scheduled 4 Aug 2026** (quarter ended Jun 2026); no Q1 primary data exists yet.

## 3. Re-rate map

Ordered by impact on the **multiple** (not the price); each classified by type (see Section D), with mechanism, estimated multiple impact + confidence tier, timing, and durability.

| # | Driver | Type | Mechanism (discount removed) | Est. multiple impact (confidence) | Timing | Durability |
|---|---|---|---|---|---|---|
| 1 | **Rubin ramp confirms Ibiden sole/lead-source on the hardest packages** | Fundamental | Removes the "share-erosion to Unimicron" discount; proves pricing power (substrate area +~75% vs Blackwell, ASP >2x) | +3–5x EV/EBITDA (moderate) — anchored to prior AI-cycle re-rates | 2H FY2027 (Rubin) | Structural if share holds |
| 2 | **Glass-core fears recede / Ibiden's CoPoS build-up seat is affirmed** | Structural (sentiment-adjacent) | Removes the "2028 existential displacement" de-rating overhang | +2–3x (moderate) | 2026–2028, event-driven on each glass disclosure | Structural |
| 3 | **ABF shortage (demand ~22% CAGR vs supply ~12%) drives pricing** | Structural | Sector-wide tightness lifts substrate ASPs and peer multiples together | +1–2x (moderate) | 2027 shortage window | Structural while shortage holds |
| 4 | **Advances actually land / capacity fills to plan** | Fundamental | Removes the "overbuild / capex-not-recovered" discount; converts the pre-funding narrative into balance-sheet fact | +1–2x (low-moderate) | FY3/27 prints | Structural |
| 5 | **Yen weakness (~¥162/$)** | Macro | Inflates JPY-reported export earnings; can reverse on intervention | +0–1x (low) | Ongoing | Transient (mean-reverts) |

**Near-term binary gates:** (a) Q1 FY3/27 print (4 Aug 2026) — Electronics margin trajectory and any advances inflow; (b) each incremental glass/CoPoS disclosure and its named supplier; (c) any confirmation of NVIDIA allocation share on Vera Rubin (Ibiden vs. Kinsus/Unimicron/Shinko).

**Net re-rate verdict:** Upside re-rate potential is real but **already substantially priced** — at ~40x EV/EBITDA the market has discounted much of the Rubin-cycle earnings. The single most weighty bucket is **fundamental** (Rubin share/ASP + advances landing); the largest downside bucket is **structural** (glass-core substitution and share dilution). Net: the multiple has more room to *compress* on disappointment than to expand on confirmation — this is a "prove the earnings, defend the share" set-up, not a cheap re-rate.

## 4. Competitive comparison & moat

**Scope discipline (critical):** "market share" here means three different things and sources constantly conflate them — (a) *total* ABF/FC-BGA (incl. PC, where Unimicron leads ~22% by volume); (b) *high-end AI-server-grade* FC-BGA (where Ibiden leads); (c) *ABF film* (Ajinomoto ~95% material near-monopoly, a different layer). Ibiden's moat lives in bucket (b).

**Level 2 — landscape by role:**
- **(a) Direct rivals (high-end ABF FC-BGA):** Shinko Electric (closest technical peer at the top end; ownership in flux under a JIC/JBIC-led take-private — status to verify), **Unimicron** (#1 volume, fastest-gaining challenger), AT&S (aggressive Kulim/Malaysia capacity, some financial strain), Nan Ya PCB, Kinsus (reportedly qualified into Vera Rubin), Simmtech, Daeduck.
- **(b) Adjacent/complementary:** OSATs Amkor/ASE/JCET (own CoWoS-style assembly + panel-level packaging; partners *and* potential encroachers); foundry packaging TSMC / Intel Foundry; glass-core entrants SKC/Absolics, Samsung Electro-Mechanics; Corning as glass supplier.
- **(c) Suppliers:** **Ajinomoto Fine-Techno** (ABF film ~95%, announced ~30% price hike effective Q3 2026 — a capital-light chokepoint above every organic-substrate maker); glass suppliers Corning/SCHOTT/AGC/NEG; equipment incl. **LPKF** (LIDE/TGV for glass), DISCO, Onto Innovation.
- **(d) Customers who could vertically integrate:** NVIDIA, Intel, Samsung (most credible integrator — owns SEMCO substrates + a glass program), hyperscaler ASIC teams. Near-term in-housing is unlikely (multi-year qualification, capital-heavy, Ajinomoto-film dependency).

**Estimated market share — honest tiers (share % below are T3 market-report/Substack tier, illustrative not audited):** In the *high-end FC-BGA* slice, one breakdown puts Ibiden ~35% / Shinko ~18% / Unimicron ~14% / AT&S ~10% / Nan Ya ~5%. In the *narrowest AI-server-grade* slice, a single (unaudited) source estimates Ibiden **~85% (2023) → ~55% (2026)** with Unimicron rising from ~10% — i.e., still the clear leader but **actively ceding share**. Do not quote a single precise Ibiden % as fact; the defensible statement is "dominant but declining share of AI-grade FC-BGA, roughly mid-50s%-to-mid-30s% depending on how narrowly the segment is drawn." Glass-core TAM (new segment): SEMI cited ~$200M (2026) → >$2B (2030) off a tiny base (secondary summary — flag).

**Head-to-head — Ibiden vs. Unimicron (closest volume/momentum rival):** Ibiden wins on yield maturity at 14–20+ layers, largest body sizes, tightest line/space, incumbent lead-source status, and margin power; loses on capacity constraint, capital intensity, and single-country concentration (adding ~$1.2B Arizona, 2027). Unimicron wins on scale/cost and is gaining via a ~$1.4B GDS raise and UMC backing; loses on not-yet-proven volume yield at GPU-class layer counts. **NVIDIA is the marquee dual-source dynamic** — deliberately qualifying second sources to de-risk Ibiden's chokehold. Who's gaining: Unimicron. The near-monopoly is normalizing toward an oligopoly at the high end.

**Moat verdict: WIDE but NARROWING — durable near-term, structurally challenged medium-term.** The edge is genuinely proprietary process yield at the extreme (tacit, qualification-gated, capital-heavy know-how), reinforced by the TSMC CoPoS build-up seat and the Ajinomoto-film chokepoint that constrains everyone equally. The caveat: Ibiden owns neither of the two scarcest inputs (Ajinomoto film; glass + TGV tooling in the glass world) — much of its value is *converting* others' materials with superior yield, so if the material or format changes the moat must be re-earned.

## 5. Technological moat & competitive technologies

**Level 1 — competing ways to build the accelerator package substrate/core:**

| Approach | How it works | Champions | Trade-off vs. Ibiden's high-end organic ABF |
|---|---|---|---|
| **High-layer organic ABF build-up (incumbent)** | Organic core + many laser-drilled ABF build-up layers, sub-15µm L/S | Ibiden (highest end), Shinko, Unimicron, AT&S | Baseline; cheapest at scale, mature yield. Weakness: **warpage/CTE mismatch** worsens past reticle scale — hitting physical limits |
| **Glass-core substrate** (glass core + ABF build-up on top) | Glass core, TGV vertical routing, build-up both faces; CTE near-Si, ultra-flat, <2µm L/S | Intel, Samsung EM, SKC/Absolics, **TSMC CoPoS (with Ibiden)** | Better warpage/flatness/density. Weakness now: **brittleness/micro-cracks, immature yield, no HVM until ~2027–2029**, higher initial cost |
| **Si interposer — CoWoS-S** | 2.5D passive Si interposer with TSVs, then onto FC-BGA | TSMC | Highest density but reticle-limited/expensive; *complements* the substrate — Ibiden still sells it |
| **Fan-out/RDL — CoWoS-R/-L, InFO** | Organic RDL or RDL + Si bridge replaces Si interposer; still on FC-BGA | TSMC; NVIDIA Blackwell runs CoWoS-L | Cheaper/larger; sits *on top of* the organic substrate — expands Ibiden content |
| **Panel-level packaging (PLP/CoPoS)** | 300mm wafers → large rectangular panels; enabler for glass | ASE (310mm), Amkor, TSMC CoPoS | ~30% cost cut / >90% utilization; weakness: warpage/handling on large panels, immature — the format shift that could reset the yield lead |

**Convergence view (2027–2030 flagships):** layered coexistence, not clean substitution. High-layer organic ABF stays the production standard through at least 2028 and likely dominates volume into 2029+. Glass-core enters commercially late-2026/2027 (Intel, SKC/Absolics first), ramps 2028–2030, targeted first at the largest reticle-plus packages where organic warpage fails — and **Ibiden is inside TSMC's CoPoS tent** as the ABF/build-up validation partner. Near-term substitution risk is therefore lower than headlines imply; the medium-term risk is the *core material* migrating to glass suppliers Ibiden doesn't own.

**Defensibility:** the moat is real and technical (not a mere integration layer) but is anchored to a material (organic ABF) and a share (near-100% of the hardest parts) that are both already eroding at the edges. **Verdict: durable for organic AI substrates through ~2028; emerging-threatened thereafter.** The decisive question — does Ibiden's ABF build-up expertise carry onto glass cores? — currently reads *partial-yes* (glass cores still need ABF build-up on top; Ibiden is explicitly in TSMC's program), which is precisely the Edge's mechanism.

## 6. Secular / thematic positioning

Ibiden is a **first-derivative** beneficiary of AI accelerator capex: every incremental high-end GPU/accelerator needs a high-complexity substrate, and substrate area/ASP is rising per generation (Rubin substrate area reportedly +~75% vs Blackwell). It is also exposed to the **ABF shortage** thesis (demand ~22% CAGR 2025–28 vs supply ~12% → shortage from 2027, gap >20% in 2027; server-CPU + AI share of ABF demand rising 54%→66% 2026→2028). The second-derivative/optionality layer is glass-core: Ibiden participates via CoPoS but does not own the glass or the TGV tooling. Net: high-quality secular exposure, but the same secular wave is pulling forward the technology (glass, panel-level, and even substrate-free CoWoP explorations) that could dilute organic content over time.

## 7. Financials

**FY3/26 (year ended Mar 2026, primary tanshin):** net sales ¥416.2B (+12.7%); operating profit ¥62.0B (+30.3%, 14.9% margin); net profit ¥63.7B (+89.0%) — *net profit was flattered by a ¥49.4B extraordinary gain on sale of investment securities*, so the +89% headline overstates operating momentum. Diluted EPS ¥214.91 vs basic ¥228.16.

**Cash flow / capex:** operating cash flow ¥106.4B; PP&E capex ¥106.1B → **FCF ≈ ¥0**. Net investing (−¥52.4B) was cushioned by ¥57.5B of investment-securities sales (the one-off cross-shareholding monetization). Construction-in-progress fell ¥202.0B→¥111.8B as Ono assets were placed in service.

**The ¥500B FY26–28 program & pre-funding — contracted vs. recognized discipline:**
- ¥500B/3yr ≈ ¥167B/yr vs current OCF ¥106B and D&A ¥66B → ~2.5× annual D&A and above OCF; **undeliverable from internal cash alone**, hence reliance on customer advances, the ¥295.7B cash hoard, and securities monetization. Heavy fixed-cost/depreciation build ahead → operating leverage both ways.
- **Pre-funding is prospective, not yet on the balance sheet.** "Advances received" was **¥80,950M at 31 Mar 2026, DOWN ¥11,133M YoY** (a drag on OCF). Trade press reports customer-specific prepayments (Intel ¥220B / NVIDIA ¥280B mapped to Gama/Ono) but **this split is not in Ibiden's filings** — treat as [T], unconfirmed. The "customers pre-funded it" thesis is a forward expectation (FY3/27+), not a FY3/26 fact.

**Capital stack (31 Mar 2026):** interest-bearing debt ≈ ¥192.5B (bonds ¥60B, long-term loans ¥60B, **convertible bonds ¥72.5B** adding ~15,584K diluted shares at ~¥4,650 implied post-split conversion, short-term loans repaid to ¥0) vs **cash & deposits ¥295.7B → net cash**. Balance sheet was *de-levered ahead of the ramp* (financing CF −¥157.5B). Shares (post 2-for-1 split effective 1 Jan 2026): outstanding ≈ 279.2M, **fully diluted ≈ 294.8M** (CB dilution). Dividend payout conservative (~13%, forecast ~17%); no active buyback. **Dilution discipline note:** the CB is the main dilution vector (~5.6% of shares); no ATM/aggressive SBC flagged.

**CapEx-vs-OpEx read:** the cash "burn" here is unambiguously *asset-building* (AI-substrate capacity), not structural OpEx burn — but it is large enough that recovery depends on the AI demand curve holding and the advances actually landing.

## 8. Risks

Named/specific, drawing on the FY3/26 securities-report risk section:
- **Capex-recovery / overbuild (explicitly named).** ¥500B build to ~2.5× capacity; if demand projections fail, invested capacity may not be recovered. This is the classic substrate over-build trap and maps directly to Tripwire #2.
- **Customer concentration.** Named-customer revenue ≈47.5% (NVIDIA 29.4% + Intel 18.1%), essentially all in Electronics where the two are likely >75% of segment sales. NVIDIA is now the single largest dependency.
- **Intel is the fragile counterparty.** FY2025 revenue $52.9B (−0.5%), net loss −$267M, cash $14.3B vs LT debt ~$44.1B; 18A HVM began Jan 2026 at ~55–65% yield, below the 70–80% profitability threshold (CFO: not profitable until end-2026). Weak/volatile Intel CPU volumes translate directly into softer FC-BGA pull. (NVIDIA/AMD/TSMC are all financially strong — no solvency risk there.)
- **Technology substitution (only implicitly disclosed).** Glass-core is **not named as a discrete risk factor** — it is folded into generic "technology innovation / product-need change" language. Longer-tail: NVIDIA's exploration of **CoWoP** (substrate-free chip-on-wafer-on-PCB) for a future Rubin GR150 platform (~late-2026/2027 feasibility; Rubin/Rubin Ultra still on ABF per current reporting).
- **Single-region concentration / disaster.** Manufacturing clustered in Gifu (Ono/Gama/Ogaki); earthquake/flood exposure with **no quantified BI insurance disclosure** (admitted product-liability coverage gap).
- **FX.** Large USD/EUR exposure; yen weakness is a current tailwind that can reverse on intervention.

**Pre-Mortem (the single most likely fundamental path to permanent impairment):** *not* a solvency default by any customer — it is **architectural substitution stranding advance-funded organic capacity.** If flagship 2028–2030 accelerators move the core to glass (Intel/Samsung/SKC-Absolics leading, TSMC CoPoS the foundry vector) *and* the scarce competence migrates to glass forming + TGV (LPKF, Corning) + panel-level assembly (ASE/Amkor) faster than Ibiden's build-up content can follow, the ¥500B of new organic-FC-BGA capacity underfills after the advance-funded contract windows lapse (post-2028) — depreciation without revenue. Secondary path: NVIDIA dual-sourcing simply compresses Ibiden's high-end share and pricing within organic.

## 9. Bull / base / bear

Anchored to ¥19,215 (TSE 4062, mid-Jul 2026). Probabilities are subjective estimates, not forecasts.

- **Bull (~30%): ¥28,000–35,000+.** Rubin ramps with Ibiden as lead-source at rising ASP; ABF shortage lifts pricing; advances land and Ono/Gama fill to plan; glass fears fade as Ibiden's CoPoS seat is affirmed. Multiple holds ~40x on materially higher FY28–29 earnings.
- **Base (~45%): ¥16,000–22,000.** Earnings grow into the ~40x multiple; Ibiden keeps the high-end lead but cedes some share to Unimicron/Kinsus; glass stays a 2028+ story. Stock roughly tracks earnings; multiple drifts down modestly as the AI-substrate trade normalizes.
- **Bear (~25%): ¥9,000–14,000.** Any of: Rubin allocation visibly diluted to rivals; an AI-capex air-pocket / CoWoS destock; advances fail to land and overbuild fears take hold; or a pulled-forward glass/CoWoP commitment naming a non-Ibiden supplier. Multiple compresses toward the low-20s x on a de-rate + earnings miss.

Valuation framework: EV/EBITDA on FY28–29 substrate earnings, cross-checked to peer multiples (premium to Unimicron/AT&S justified by high-end lead but that premium is the thing at risk).

## 10. Sector bottleneck / structural analysis

The binding constraint in AI hardware has been **advanced packaging and substrate supply**, not raw wafers. CoWoS capacity is scaling hard (~75k wpm end-2025 → 125–130k target end-2026; supply-demand gap narrowing ~20%→~10% by end-2026), which pushes the bottleneck *downstream* onto the substrate: ABF demand ~22% CAGR vs ~12% supply → shortage from 2027. Ibiden monetizes exactly this bottleneck at the highest-value node (largest, highest-layer substrates), and the Ajinomoto-film chokepoint above it keeps the oligopoly structure intact. The risk is that the bottleneck *migrates* — to glass forming/TGV and panel-level assembly — into arenas where Ibiden is a participant, not the owner.

## 11. Sentiment

- **Institutional/analyst:** consensus **Buy** (~13 Buy / 3 Hold / 1 Sell of ~16–17); blended 12-mo PT ~¥20,662–21,525 (roughly flat-to-+12% vs spot). **Important caveat:** individual broker targets retrieved (JPM ~¥12,900; MS Equal-Weight ~¥13,000; Goldman conviction Buy) sit *well below* the live price — the datapoints look stale/lagging, and brokers have repeatedly chased the price higher. The bull case rests on FY28–29 earnings brokers are still rebasing toward.
- **Positioning/technical:** high beta (~1.71); trades as a high-torque proxy for the AI-substrate trade (−10% on 6 Jul 2026 in the sector rout, below its ¥27,480 52-wk high). TSE line short-selling ratio could not be retrieved (JPX portal blocked); OTC ADR short data is thin/unreported.
- **Battleground framing:** the debate is not franchise quality — it is whether ~40x survives share dilution + the glass clock.

## 12. Asymmetry verdict

This is **not** a low-floor/high-ceiling asymmetric bet. It is a **high-quality, richly-priced compounder with a two-sided multiple**: the ceiling is capped by an already-elevated ~40x that has discounted much of the Rubin cycle, while the floor is soft because the same multiple can compress hard on share-dilution or glass-timeline news. The franchise floor (net-cash balance sheet, real cash generation, oligopoly position) limits the *terminal* downside, but the *multiple* downside is live. Closer to a leveraged directional bet on "the AI-substrate premium holds" than a genuine asymmetry.

## 13. Management & insider alignment

- **Track record / guidance:** management raised FY guidance through the Blackwell ramp and delivered the FY3/26 beat; the ¥500B program is board-approved and phased (Gama ¥220B first). Payout is conservative (~13%→~17%) with cash retained for capex — capital allocation is growth-first, ROIC-sensitive rather than shareholder-return-led.
- **Insider/ownership:** no controlling shareholder; group is ~30 consolidated subs. Related-party transactions are routine (property leases, group logistics/outsourcing via Ibiden Jushi/Sangyo/Human Network) with **no quantified amounts and no director/major-shareholder self-dealing disclosed** — low related-party risk. Specific insider buy/sell data for the trailing 6–12 months was not retrievable in this pass (flag).
- **Alignment read:** the ¥500B build is the key capital-allocation call; it is de-risked in narrative by customer advances but, per §7, those advances have not yet materialized on the balance sheet — the alignment question is whether management is building ahead of *contracted* demand or *hoped-for* demand. D&O insurance is company-paid (standard).

## 14. Valuation multiples & implied expectations

Current (2026-07-15 aggregator): **EV/EBITDA ~39.6x** (range 34–39.6x across sources), trailing P/E ~83.7x, **forward P/E ~71.5x**, P/B **9.01x**, EV/Revenue ~11.85x. Versus Ibiden's own pre-AI-cycle history (P/B ~1–3x; EV/EBITDA high-single-to-mid-teens x mid-cycle), every multiple is at a multi-year extreme — the ~478–518% re-rate is a multiple event as much as an earnings event. **A clean 5-year EV/EBITDA series and current hard multiples for Shinko/Unimicron/AT&S could not be retrieved this pass (flag — needs a terminal pull);** directionally Ibiden trades at a premium to Unimicron/AT&S on its perceived high-end lead.

**Implied expectations:** at ~40x EV/EBITDA / ~71x forward P/E, the price already embeds sustained AI-substrate share leadership *and* successful ¥500B capacity absorption *and* glass fears staying a 2028+ tail. The multiple looks **stretched, not compressed** — it is pricing the optimistic operational case, leaving little margin for share dilution or a demand air-pocket.

## 15. Investment thesis (synthesis)

Three name-specific reasons to own, each with its honest counterweight:

1. **Highest-complexity substrate leadership at the exact AI bottleneck.** Ibiden owns the hardest-to-make organic FC-BGA and is the lead-source under NVIDIA's flagship accelerators (29.4% of revenue, verified). — *Counterweight:* that lead is measurably eroding (AI-server-grade share reportedly ~85%→~55% since 2023) as NVIDIA dual-sources Unimicron/Kinsus; the moat is normalizing to an oligopoly.
2. **Inside the glass transition, not displaced by it.** Ibiden is TSMC's named CoPoS build-up partner — glass swaps the *core* while ABF build-up carries over, exactly the Edge's mechanism. — *Counterweight:* Ibiden owns neither the glass nor the TGV tooling; a vertically integrated glass entrant (Samsung, or an Intel-licensed ecosystem) could capture core *and* build-up.
3. **Fortress balance sheet funding a pre-committed AI capacity build.** Net cash (¥295.7B), de-levered ahead of a ¥500B growth program with customer advances behind it. — *Counterweight:* the advances have *not yet landed* (¥80.95B, down YoY); the build is ~2.5× D&A and above OCF, so if demand or advances disappoint, it becomes depreciation without revenue (the Pre-Mortem).

**What has to be true:** Ibiden must (a) hold enough high-end AI-substrate share and ASP through the Rubin cycle to grow into a ~40x multiple, (b) convert the pre-funding narrative into actual advances/utilization, and (c) keep its build-up seat as glass arrives ~2028–2030. If all three hold, the rich multiple is defensible; if any one breaks, the multiple — not just the price — de-rates.

## 16. Final thoughts & conclusion

Pulling the threads together: Ibiden is a genuinely world-class franchise selling into the tightest node of the AI hardware stack, with verified AI-customer inversion (NVIDIA #1), a net-cash balance sheet, and a credible seat in the glass transition. None of that is the debate. The debate is that the market has already paid for all of it — ~40x EV/EBITDA, ~71x forward earnings, 9x book — while two real cracks are visible in the primary data: share is eroding at the very high end, and the celebrated "pre-funded capex" has not yet shown up on the balance sheet.

Pre-investment checklist:
- **Your edge — what do you believe that the crowd doesn't?** The differentiated view is *not* "AI is big and Ibiden makes AI substrates" (that is consensus and why it's up ~500% at ~40x). The variant view is that the market treats glass-core as a clean existential threat when glass swaps the substrate *core* while ABF build-up laminates on top — so Ibiden's build-up expertise carries over and it holds a CoPoS seat. The diligence *supports* this (TSMC named Ibiden; the glass HVM clock keeps slipping past 2028), which means the glass "de-rating" risk is likely over-feared. If you don't hold a differentiated view like this, you are simply agreeing with a richly-priced consensus — size accordingly.
- **Your tripwire — what would prove you wrong?** Any one of: (1) NVIDIA publicly shifts high-end substrate allocation toward Unimicron (breaks the #1-customer moat); (2) two consecutive prints show Ono/new-plant utilization stalling below plan while capex keeps rising (capacity outrunning demand); (3) a glass-core HVM commitment for a flagship AI accelerator lands materially before ~2028 *and* names a supplier other than Ibiden. Any one = thesis broken; decide the action now.
- **Time-horizon fit:** the thesis resolves over ~18–36 months (Rubin ramp 2H FY2027; glass HVM 2028–2029) — a multi-year hold, not a trade. The near-term gate is the Q1 FY3/27 print (4 Aug 2026).
- **Conviction-appropriate sizing:** the thesis is diversified across multiple catalysts (Rubin, ABF shortage, glass optionality) rather than single-counterparty-binary — but the *valuation* is the concentrated risk. Size to the multiple, not just the franchise.
- **What kills the thesis fastest:** a pulled-forward glass/CoWoP HVM commitment naming a non-Ibiden supplier, or a visible NVIDIA allocation shift to Unimicron — either de-rates the multiple immediately (ties to Pre-Mortem §8 and gate §3).
- **Where the price sits vs. the thesis:** **already pricing the optimistic case.** At ~40x the stock has discounted sustained share leadership + capacity absorption + benign glass timing. Underpriced only if consensus is *too cautious* on Rubin ASP — possible, but not the base case.
- **What to monitor next:** Q1 FY3/27 (4 Aug 2026, Electronics margin + advances-received line); each glass/CoPoS disclosure and its named supplier; Vera Rubin allocation reporting; Unimicron's capacity ramp post-$1.4B raise; Ajinomoto ABF pricing.

**Bottom line:** A superb franchise at a demanding price. The Edge (glass is over-feared) holds up under diligence, but it is largely a reason *not to short* rather than a reason the stock is cheap. The honest read: you are paying full price for quality, defended by a moat that is real but narrowing — own it for the franchise and the Rubin cycle with eyes open to a two-sided multiple, not as a bargain.

---

### Source-reliability note
Primary Ibiden filings (tanshin 11 May 2026; securities report/EDINET S100YC4B 18 Jun 2026) anchor the financials, segment, customer-concentration, capital-stack and advances figures — these are high-reliability [P]. Counterparty financials (NVIDIA/Intel/TSMC) are from their own primary filings [P]. Sector/market-share and glass-timeline items are established trade press (DigiTimes/TrendForce/Nikkei/Bloomberg) [T]; the high-end and AI-server share percentages (35% / 85%→55%) are market-report/Substack tier [T3] — explicitly illustrative, not audited. Explicitly unverified: the Intel ¥220B / NVIDIA ¥280B prepayment split (trade press, not in filings); a live reconciled ADR price/ratio; TSE short-interest ratio; a clean 5-year and peer multiple set; trailing insider buy/sell data.

*Not financial advice — informational research tooling only.*
