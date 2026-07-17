# LPKF — LPKF Laser & Electronics SE (Xetra: LPK / OTC: LPKFF) — Deep Dive

**Date:** 2026-07-14  ·  **Reference price:** €16.90 (Xetra LPK, 14 Jul 2026 ~17:37 CET; prior close ~€17.15; ~44% below the 22 Jun 2026 ATH of €30.20)  ·  **Status:** final

> Full-diligence report applying `framework/deep-dive-template.md` (Sections B/C/D/G/H) under `framework/standing-rules.md`. Built from four parallel diligence work-streams (primary filing, counterparty, sector, competitive-landscape). Point-in-time figures dated; estimates/opinions labelled; unverifiable items flagged. **Not financial advice — informational research tooling only.**

---

## Executive summary (see §15 for the full synthesis)

LPKF is the pure-play, IP-protected leader in **LIDE (Laser-Induced Deep Etching)** — a two-step laser-modify-then-wet-etch process for structuring glass (through-glass vias / TGV) used in glass-core substrates for AI advanced packaging. It sells the *equipment/process* (picks-and-shovels), not the substrate. The core business is loss-making and cyclical; the equity is priced as an **option on the ~2027 glass-substrate volume ramp**, and that ramp is entirely gated by a handful of downstream glass-substrate makers qualifying and placing first high-volume-manufacturing (HVM) orders.

Two facts anchor this snapshot, both verified in primary filings:

1. **There is no Tier-1-confirmed HVM LIDE order from any named glass-maker as of today.** LPKF filings name zero customers, disclose only "one customer >10%," and *explicitly exclude* HVM advanced-packaging orders from FY2026 guidance. The much-cited "missed 30-June-2026 deadline" is a **press-crystallized expectation, not a filed commitment** — LPKF's own language decouples ramp timing from its control ("determined by qualification of downstream process steps, not by LIDE").
2. **The dilution lever is armed but not pulled.** LPKF has ~20% authorized capital and a €200m convertible shelf (both unused), gross cash of only €5.75m (31 Mar 2026), and a burn quarter behind it (Q1-26 FCF −€7.6m). An activist countermotion demanding a capital raise was *rejected* by management at the 4 Jun 2026 AGM — but management kept a raise explicitly "on the table."

The stock roughly tripled in 2026 (52-wk €5.35–€30.20) then fell ~44% from its June peak; every published sell-side target (~€9–€15) sits **below** the €16.90 spot. This is a timing-and-credibility bet, not a valuation bet.

---

## 1. Business model & role in the value chain

LPKF sells **LIDE equipment** (and licenses the process) to glass-substrate makers. LIDE is a two-step method: a picosecond laser *modifies* glass internally (creating a ~1µm modified zone, no physical hole in step one), then a selective wet etch removes the modified zone faster than the bulk glass, forming a tapered "earthworm" through-glass via. In the AI-packaging value chain, glass-core substrates need thousands of these vias; LPKF supplies the tool that forms them. It is upstream of the substrate maker (Absolics, Samsung Electro-Mechanics, DNP, etc.), who is in turn upstream of the OSAT/foundry and the chip vendor. LPKF therefore monetizes glass-substrate adoption *one derivative removed* — it captures equipment capex, not substrate revenue.

**Reportable segments (FY2025, primary annual report; LIDE sits inside Electronics — there is no standalone glass line):**

| Segment | Rev 2025 (€m) | EBIT 2025 (€m) | Note |
|---|---|---|---|
| **Electronics** (houses LIDE) | 35.9 | **−2.6** | Structurally loss-making; carries the glass option |
| **Development** | 27.1 | +1.3 | Only consistently EBIT-positive segment |
| **Welding** | 24.0 | +0.5 | Just turned positive (from −4.8 in 2024) |
| **Solar** | 28.3 | +1.6 | The fragile funder — collapsed to €1.3m rev in Q1-26 |
| **Total** | **115.3** | **+0.8 (adj)** | FY25 revenue −6.2% YoY |

**Funding read:** the LIDE bet has historically been cross-subsidized by Solar, but Solar is eroding fast (lost a China megaproject; customers deferring on the perovskite technology shift). Development is the only reliable profit engine; Welding just turned. **The cash-generative base under the option is thin and shrinking** — the central structural tension for a company burning to reach a 2027+ payoff.

## 2. Recent catalysts

- **2026-07-02 — Samsung Electro-Mechanics + Sumitomo/Dongwoo form "GlaSSEM" glass-core JV** (share capital KRW 482.1B / ~$310M; SEMCO 66% / Dongwoo 34%; supply-system launch 2H FY2027). Equipment/method not disclosed. A firming 2027 capacity event — SEMCO's standalone line is trade-press-mapped to LPKF LIDE (with Philoptics as dual-source), but *no Tier-1 confirmation*. (Sumitomo PR [T1]; TheElec/vlmkapital [T2/T3].)
- **~2026-06-30 — Press-narrated "self-imposed" LIDE first-series-order deadline passes with no announcement**; stock fell ~28% from the €30.20 ATH. Not a filed commitment (see §3). ([T3].)
- **2026-06-22 — SDAX inclusion effective; stock ATH €30.20** the same day — index-fund buying into a thin float marked the local top; the reversal followed. ([T2].)
- **2026-06-17 — LPKF disclosed LIDE can drill micro-vias into glass up to 2mm thick; validation samples already with customers**; stock +15% to €25.80. ([T2].)
- **2026-06-04 — AGM (Hanover):** no dividend; AOC partner Paul Owsianowski elected to the Supervisory Board; a separate shareholder (Prof. Radatz) countermotion demanding an immediate capital increase for a "LIDE acceleration offensive" was **rejected by management**. ([T1/T2].)
- **2026-04-30 — Q1 2026 results:** revenue €17.1m (−32% YoY), order intake €24.1m (book-to-bill 1.4), adj. EBIT −€5.7m; one "first production-scale capacity-expansion system" order booked (unnamed, small — *not* the awaited HVM series order). ([T1].)
- **Upcoming — H1 2026 report, 23 July 2026, 08:00 CET** — the next hard catalyst and the single most important near-term gate.

## 3. Re-rate map

Ordered by impact on the **multiple** (the option premium), classified by type, with mechanism, estimated impact + confidence, timing, durability. (Standard EV/EBITDA framing is N/M — the company is loss-making; the "multiple" here is the option premium the market pays over sell-side DCF.)

| # | Driver | Type | Mechanism (discount removed) | Est. impact (confidence) | Timing | Durability |
|---|---|---|---|---|---|---|
| 1 | **A named glass-maker places a first HVM/first-series LIDE order** | Fundamental | Removes the "credibility/timing" discount — converts the option from hoped-for to contracted | Large re-rate (moderate) — could add many €/share; anchored to the gap between spot and DCF | Watch 23 Jul H1; else H2 2026–2027 | Structural if it starts a multi-tool cycle |
| 2 | **Glass-core HVM timeline confirmed for 2027 across the ecosystem** | Structural | Validates the thematic option; lifts all glass-substrate names together | Moderate (moderate) | 2026–2027, event-driven | Structural while ramp holds |
| 3 | **Solar/Welding stabilize; core burn narrows toward the North Star 2028 double-digit-margin path** | Fundamental | Removes the "cash-burn-forces-dilution" discount | Small-moderate (low-moderate) | FY2026–2028 | Structural |
| 4 | **SDAX/passive flows, short covering on a thin float** | Sentiment/technical | Positioning, not fundamentals | Can move price hard both ways (moderate) | Ongoing | **Transient — mean-reverts** |

**Near-term binary gates:** (a) the 23 Jul 2026 H1 report — any concrete first-series order, customer-negotiation color, order backlog, and the cash position; (b) the Absolics dual-source award (post-F&S-exclusivity-lapse) and any SEMCO/GlaSSEM HVM tool decision — both directly contested by Philoptics; (c) whether continued burn forces a capital raise.

**Net re-rate verdict:** This is an **asymmetric, event-gated option**, not a compounding re-rate. The single heaviest bucket is **fundamental** — one named HVM order re-legitimizes the entire premium; its absence deflates it. The largest downside bucket is also fundamental (dilution from sustained burn) plus the sentiment/technical unwind of a thin-float momentum name. Because spot sits ~30–90% above every published DCF target, the multiple has more room to compress on "another quarter of samples, not orders" than to expand on incremental theme news alone — only a hard order changes the equation.

## 4. Competitive comparison & moat

**Framing:** this is a **pre-volume equipment market** — nobody ships AI glass substrates at volume today, so hard % market share of via-formation equipment is not measurable. Anyone quoting a clean % is fabricating. Labeled tiers below.

**Level 2 — landscape by role:**
- **(a) Direct rivals (via-formation equipment):** **Philoptics (KOSDAQ: 161580)** — the clear head-to-head; laser-*drill*-then-etch (distinct from LIDE's modify-then-etch); co-supplier at SEMCO's pilot line and exclusive TGV supplier at Absolics' pilot line. Via Mechanics/Ushio (legacy direct-drill — weak current evidence in glass-core HVM, flag). E&R (Taiwan, unverified/T3). F&S Electron (Korea — had an Absolics exclusivity that reportedly lapsed March 2026, T3).
- **(b) Adjacent/complementary:** glass suppliers Corning/AGC/NEG/SCHOTT (Corning also a vertical-integration threat — own glass + own "damage-and-etch" IP + a $6B Meta glass deal Jan 2026); metrology Onto/Camtek; wet-chem/etch partners Chemtronics/Soulbrain/F&S (LIDE *requires* a downstream etch-chemistry partner — a complement and a dependency).
- **(c) Suppliers to LPKF:** laser sources/optics — **Coherent/II-VI** (UV/ps sources) — a genuine upstream dependency.
- **(d) Customers who could vertically integrate the via step:** Absolics/SKC, Samsung Electro-Mechanics, Corning (highest risk), JNTC (explicitly in-house-focused, buys LPKF gear "to benchmark"), Intel, TSMC/Amkor, DNP.

**Estimated share — tiers (pre-volume, no fabricated %):** Tier A / presumptive standard-setter: **LPKF/LIDE** — company claims >80% of major players preparing glass ramps are *qualifying* with LPKF equipment and 20+ units shipped (self-reported, engagement-count based, *not* revenue share). Tier B / credible niche rivals with real references: **Philoptics** (most real-world Korean deployments), Corning (captive). Tier C / latent in-house threat: substrate makers internalizing the step once qualified.

**Head-to-head — LPKF vs. Philoptics (closest rival):** A *live, contested* head-to-head, not a settled monopoly. In a public Sept-2024 dispute (TheElec), Philoptics claimed LIDE offers "only one hole size"; LPKF rebutted (two modes — drill/cutting) and countered that Philoptics' physical-hole-then-etch route risks residual micro-cracks. **LPKF wins on** sidewall/crack integrity, granted-and-defended IP, breadth of engagements, and an inferred (not confirmed) exclusive Intel CPO/glass-waveguide relationship. **Philoptics wins on** hole-size flexibility (~10µm), price/local support, and the broadest Korean-fab references (named at both Absolics and SEMCO). Both are named suppliers at Absolics and SEMCO — this is **dual-sourcing, not an LPKF sweep**. Philoptics' balance sheet is weaker (FY2025 revenue KRW 103.4B, −75% YoY; first operating loss in four years).

**Moat verdict: MODERATE and EMERGING** — trending moderate-durable if Intel/HVM qualifies LIDE, but at risk of staying thin if Korean fabs standardize on Philoptics or Corning in-houses it. See §5 for the defensibility detail and the single erosion path.

## 5. Technological moat & competitive technologies

**Level 1 — competing ways to form through-glass vias:**

| Method | How it works | Champion(s) | Trade-off vs. LIDE |
|---|---|---|---|
| **LIDE (laser-modify + wet etch)** | ps-laser modifies glass internally, then selective wet etch → tapered crack-free via | **LPKF** (originator, 2017) | Baseline: crack-free, no thermal damage, panel-scale throughput. Weakness: inherent taper; needs downstream wet-chem + metrology partners |
| **Laser-drill-then-etch** | Laser ablates a physical through-hole, then etch smooths/heals sidewall | **Philoptics** | Flexible hole sizes (~10µm) but starts from a physically drilled hole → residual-micro-crack/integrity risk |
| **Direct laser drilling/ablation** | Ultrashort-pulse / Bessel-beam / excimer removes material directly | Via Mechanics/Ushio, DPSS/excimer makers | Faster/simpler but micro-cracks, larger taper; crack-free only at slow multi-pass → HVM yield problem |
| **Damage-and-etch (Corning variant)** | Laser damage track + chemical etch, coupled to in-house glass | **Corning** | Conceptually close to LIDE but bundled with captive glass → a vertical-integration threat |
| **Photosensitive glass** | UV-crystallize exposed regions, then etch | Specialty-glass makers | Needs costly special glass; niche, not mainstream substrate glass |
| **Plasma/DRIE, sandblast/EDM/ECDM** | Dry etch / abrasive / discharge machining | Fabs; legacy MEMS | Too slow / coarse / edge-damaging for fine-pitch deep vias — not HVM-viable |

**Convergence view (2027 glass-core HVM):** the industry is converging on the **laser-modify + wet-etch class** (the LIDE approach) rather than pure direct drilling, because the binding constraint is TGV yield / crack-free sidewalls at fine pitch (target ~6µm via, ~15:1 aspect ratio), and modify-then-etch is the only route demonstrating that at panel throughput. The live contest is *within* this class: LPKF's LIDE vs. Philoptics' drill-then-etch vs. Corning's captive damage-and-etch.

**Defensibility (patents granted *and defended*):** LPKF's core European LIDE patent (granted 2022) survived a full opposition (opponent did not appeal by Feb 2025); a KIPO grant (effective 1 Sep 2025) covers the characteristic two-stage "earthworm" via geometry. This is stronger than typical first-mover IP — granted and litigation-tested, not merely filed. (Note: several retail/AI-generated sources wrongly attribute LIDE patents to Philoptics — this is false; primary sources confirm the IP is LPKF's.) Real switching costs exist once a fab qualifies a tool into a yielding flow (matched etch chemistry, metrology, plating). **But** the patents protect LIDE's specific mechanism, not the *application* — Philoptics' drill-then-etch and Corning's damage-and-etch are legally distinct routes to a similar end-via, so the patent wall does not exclude rivals from the market. **Verdict: durable *emerging* moat — real, defended IP + first-mover process maturity, but not an exclusionary wall.**

## 6. Secular / thematic positioning

LPKF is a **second-derivative** play on AI advanced packaging: it doesn't sell substrates, it sells the tool that structures the glass for substrates. Exposure to the structural driver (AI accelerators needing glass-core substrates for better warpage/flatness/density than organic ABF) is real but *indirect and timing-lagged* — LPKF only monetizes when substrate makers commit HVM capex, which is 2027–2028 at the earliest and gated by their downstream qualification. It is the only listed pure-play on LIDE glass structuring, so it trades as a high-beta thematic proxy — which cuts both ways (it captured the full 2026 glass-hype run *and* the full reversal). First-derivative names (glass suppliers Corning/AGC, substrate makers) capture the theme sooner and more diversified.

## 7. Financials

**FY2025 (primary annual report):** revenue €115.3m (−6.2%); adjusted group EBIT +€0.8m; net loss driving EPS −€0.59. Operating cash flow +€16.3m — but **working-capital-driven** (receivables −€16.6m, inventory −€7.3m released), masking the operating loss. Total capex €6.7m (of which €5.7m capitalized development for LIDE/software). FCF +€9.7m; year-end cash €10.0m; net cash +€7.0m.

**Q1 2026:** revenue €17.1m (−32% YoY, Solar collapse), adj. EBIT −€5.7m, net loss −€7.4m, EPS −€0.30. **Operating cash flow −€6.4m; FCF −€7.6m** (net loss + €3.5m inventory build for Q2/Q3 deliveries). **Gross cash fell to €5.75m** (from €10.0m); net cash ≈ **−€1.5m** as current bank borrowings rose €4.2m. Equity €71.0m (from €78.1m); equity ratio 67.8%.

**CapEx-vs-OpEx read (important):** the cash burn is an **operating-loss / OpEx burn, NOT an asset build.** CapEx is tiny (~€1.2m/qtr, almost all capitalized R&D). This is not a company funding hard assets ahead of a ramp — it is a company covering operating losses while it waits for the ramp. That distinction matters for the dilution question.

**Runway / capital stack:** gross cash €5.8m + an undrawn syndicated facility (€25.0m cash tranche, ~€12.5m cash headroom cited, + €7.5m guarantee facility), five banks, term to **31 Dec 2028**; management asserts going-concern ≥12 months. Debt is low (€3.0m drawn at YE25); **no convertibles outstanding.** Shares outstanding **24,496,546** (basic = diluted; options anti-dilutive under losses); free float **89.4%** (only AOC >10%). **Contracted vs. recognized discipline:** the entire LIDE thesis is *pre-contracted* — order intake €24.1m in Q1 with book-to-bill 1.4 is real, but HVM glass orders are neither booked nor in guidance; there is no backlog conversion story yet, only prototyping/expansion orders.

## 8. Risks

Named/specific:
- **The gating risk — no HVM order lands (or lands late).** The whole equity is an option on a first-series glass order that has not been placed and is *outside LPKF's control* (gated by customers' downstream qualification). Maps directly to Tripwire #1 (a second missed date) and #4 (timeline slips past 2027).
- **Rival TGV wins the reference socket (Tripwire #2 — live, not fired).** Philoptics is already co-qualified at Absolics and SEMCO — the two most advanced glass lines. It has not been reported to *displace* LPKF, but at Korean fabs it is at minimum co-incumbent. The offsetting positive is LPKF's inferred (unconfirmed) Intel lock. A Philoptics win at *Intel* would be the sharpest trigger.
- **Dilution from sustained burn (Tripwire #3 — armed, not tripped).** ~20% authorized capital + a €200m convertible shelf are ready and unused; a shareholder (Radatz) is actively pushing a raise; management rejected it *but kept it on the table* for "a larger transaction exceeding available financial resources." With €5.75m gross cash and a −€7.6m FCF quarter, prolonged burn without an order is the scenario that forces a dilutive raise on a thin float.
- **Funder erosion.** The profitable segments cross-subsidizing LIDE (Solar, Development, Welding) are themselves fragile — Solar cratered to €1.3m revenue in Q1-26. If the funders roll off before the option pays, the burn accelerates.
- **Vertical integration / in-house threat.** Corning (own glass + damage-and-etch) and IDMs (Samsung, Intel, JNTC) can internalize via formation once qualified.
- **Disclosure gap:** LPKF's formal risk matrix is generic and does **not** discretely rate the thesis-critical risks (glass-ramp timing, single-customer concentration, dilution) — investors must synthesize them from narrative.

**Pre-Mortem (single most likely fundamental path to permanent impairment):** *not* insolvency — it is **the glass ramp arriving on a rival's tool.** If the two most advanced 2027-window lines (Absolics dual-source award; SEMCO/GlaSSEM HVM) standardize their HVM TGV on **Philoptics** (already co-qualified there) or Corning in-houses damage-and-etch with captive glass, LIDE is designed out of the reference process at exactly the moment volume arrives. LPKF then burns through its option window without the anchor order, is forced into a dilutive raise on a thin float at a depressed price, and the equity re-rates to its loss-making-core value (sell-side €9–€13) — a permanent impairment of the option premium, even without bankruptcy.

## 9. Bull / base / bear

Anchored to €16.90 (Xetra, 14 Jul 2026). Subjective probabilities.

- **Bull (~30%): €25–€35+.** A named glass-maker (SEMCO/GlaSSEM or Absolics) places a first multi-tool HVM LIDE order in 2026–2027; the Intel/CPO relationship is confirmed; the option converts to a contracted ramp. The premium re-legitimizes and expands.
- **Base (~40%): €12–€20.** LIDE stays "samples and expansion orders," HVM slips into 2027–2028 but remains credible; Solar drags, burn continues but the bank line holds; stock oscillates on theme news and each quarterly, converging toward — but above — sell-side DCF as the option decays with time.
- **Bear (~30%): €6–€11.** A second missed date, or Philoptics/Corning winning a named reference socket, or a dilutive raise on the thin float. The premium collapses toward loss-making-core value (the €9–€13 sell-side cluster) or below.

Framework: sum-of-the-parts (loss-making equipment core valued on EV/Sales ~1–2x, worth roughly the sell-side €9–€13) **plus** an option premium for the glass ramp; today's price is ~€4–€8/share of pure option premium above the DCF cluster.

## 10. Sector bottleneck / structural analysis

The binding constraint LPKF is levered to is **TGV yield at fine pitch** — reliably forming crack-free, high-aspect-ratio vias in glass at panel throughput is the hard step that gates glass-core substrate HVM. LPKF's LIDE is arguably the best answer to that specific bottleneck, which is why >80% of players are said to be qualifying with it. But LPKF sits *two derivatives* from the AI-accelerator demand it's betting on: accelerator demand → substrate-maker capex decision → via-formation tool order. The bottleneck that actually gates *LPKF's revenue* is not silicon demand but the **downstream qualification calendar of a few Korean/US/Japanese substrate lines** — a slow, customer-controlled process. The whole thesis is a bet on *when* that calendar produces its first HVM tool order and *whose* tool it names.

## 11. Sentiment

- **Analyst:** ratings skew Buy/Hold (Warburg Buy €10.00–€12.30; Berenberg Buy €10.00; Hauck Aufhäuser Buy; Montega Hold €9–€15) but the **entire published target cluster (~€9–€15) sits well below the €16.90 spot** — verified. At the 22-Jun peak the stock was reported ~148% above the Warburg target. Analysts like the story medium-term but won't underwrite un-ordered 2027+ volume in a DCF — so fundamentals-based targets lag a momentum/option-driven tape. (Blended consensus mean unverified — MarketScreener 403.)
- **Positioning/technical:** thin float (24.5M shares, 89.4% free float but concentrated activist/coalition holding + active shorts). Disclosed net-short fell from ~2.4% to ~1.1% (Qube 1.10%, per late-June Bundesanzeiger via press) as quant shorts covered; Voleon disclosed 2.13% net short in the filing agent's read. SDAX inclusion (22 Jun) forced passive buying into the thin float, amplifying the squeeze up and the sell-the-news reversal. Mechanically volatile on flow and disclosure changes.
- **Battleground:** consensus is *already skeptical, not complacent* — every target sits below spot. The debate is timing/credibility of the first order, not whether glass is real.

## 12. Asymmetry verdict

This **is** a genuine asymmetric, option-like bet — but with a soft floor, not a hard one. The floor is the loss-making equipment core (~€9–€13 sell-side), which is itself eroding (Solar decline, continued burn, dilution risk that could reset the share count lower). The ceiling is a real multi-tool HVM cycle across the glass ecosystem (a plausible €25–€35+). So it is low-floor / high-ceiling in *shape* — but the floor is not truly protected (dilution can lower it) and the high ceiling requires a specific, customer-controlled event to fire. Closer to a **leveraged directional bet on the timing and vendor-selection of the glass ramp** than a safe low-floor asymmetry. Binary-ish and single-catalyst-dependent — size accordingly.

## 13. Management & insider alignment

- **Governance/activist:** LPKF's largest holder is **Active Ownership Capital (AOC)**, ~10–11% (holder since 2020), characterized by the CEO as "constructive cooperation"; AOC partner **Paul Owsianowski** was elected to the Supervisory Board on 4 Jun 2026. Board refresh underway (Chair Jean-Michel Richard → Alexa Siebert; Dr. Arne Schneider, Elmos CEO, added — semiconductor expertise). **Crucially, the dilutive-raise push at the AGM came from a *different* shareholder (Prof. Radatz), not AOC — and management rejected it.** As a >10% holder, AOC would be *diluted* by a raise and is incentivized to *oppose* one; so the activist situation is not, today, driving the dilution tripwire (a correction to the common framing that "the activist fight resolving against management" is the near risk — the raise pressure is coming from elsewhere).
- **Alignment/incentives:** management is executing the "North Star" transformation targeting a double-digit EBIT margin by 2028; FY26 guidance (revenue €105–120m; adj. EBIT margin −3.0% to +4.5%) deliberately **excludes** HVM glass orders — conservative framing that avoids over-promising the option, though it sits awkwardly against the CEO's verbal "concrete discussions" that the market crystallized into a 30-June expectation. No dividend (FY25 profit retained). Insider option pool ~1.24m shares (PSO payout capped at €20). Related-party transactions are immaterial (€230k to Supervisory Board members); AOC is arm's-length. AGM quorum was very low (~15.2% of capital represented) — wide-open float, low insider control.

## 14. Valuation multiples & implied expectations

Standard multiples are **N/M** (loss-making: net income −€17.45m, EPS −€0.71 TTM). Market cap ~€413m on 24.5M shares at €16.90. On FY26 revenue guidance €105–120m, **EV/Sales ≈ 3.5–3.9x** — extremely rich for a cyclical, loss-making equipment maker whose largest segments are mature. (Precise EV/Sales and P/B could not be pinned — current net cash/book value not fully pulled; equity €71.0m at Q1-26 implies P/B ~5–6x, treat as approximate.) The market is **capitalizing the LIDE/glass option, not the P&L.**

**Implied expectations:** with every sell-side DCF at ~€9–€13 (excluding un-ordered volume), the ~€4–€8/share above that cluster is **pure option premium** — the price already embeds the market's expectation that a hard glass-HVM order lands and the ramp is real. So the stock is *not* cheap on any near-term fundamental; it is a bet that the option pays before it decays. The multiple looks **stretched relative to booked fundamentals and compressed only relative to a blue-sky glass scenario the sell-side refuses to underwrite.**

## 15. Investment thesis (synthesis)

Reasons to own, each with its honest counterweight:

1. **Only listed pure-play on the best answer to the glass-TGV bottleneck.** LIDE is the presumptive standard (>80% qualifying), with granted-and-defended IP. — *Counterweight:* the patents protect the mechanism, not the application; Philoptics (drill-then-etch) and Corning (damage-and-etch) are legally distinct routes already co-qualified at the most advanced lines.
2. **Real, near-dated catalyst calendar.** GlaSSEM (2H'27), Absolics (~end-2026 first-commercial + dual-source award), and the 23-Jul H1 report are concrete gates that could produce the first HVM order. — *Counterweight:* every gate to date has produced "samples/expansion orders, not HVM"; timing is customer-controlled and has already disappointed once.
3. **Defended IP + first-mover process maturity create real switching costs once a fab qualifies LIDE.** — *Counterweight:* the fabs that matter (Absolics, SEMCO) are dual-sourcing, and Corning/Samsung/JNTC could in-house the step; the moat is emerging, not secured.

**What has to be true:** a named glass-substrate maker must place a first multi-tool HVM LIDE order *on LPKF's tool* within the option's decay window (roughly the next 12–24 months), before sustained burn forces a dilutive raise on the thin float. If that order lands, the premium re-rates and compounds; if it slips again or names a rival, the premium deflates toward the loss-making-core value.

## 16. Final thoughts & conclusion

Pulling the threads together: LPKF is a genuinely differentiated, IP-protected leader in exactly the process step that gates glass-core substrates — but it is a loss-making, cash-burning company two derivatives removed from the AI demand it's levered to, and the entire equity above ~€9–€13 is an option premium on an HVM order that no filing yet confirms and that is controlled by other companies' qualification calendars. The diligence sharpened rather than resolved the debate: the theme is real and firming (GlaSSEM, Absolics, Intel/TSMC glass roadmaps all advancing), but the two most advanced 2027 lines are dual-sourcing with Philoptics, and LPKF's clearest counter-moat (an inferred exclusive Intel/CPO relationship) is unconfirmed.

Pre-investment checklist:
- **Your edge — what do you believe that the crowd doesn't?** Consensus here is *already skeptical, not complacent* — every analyst target (€9–€15) sits below spot (€16.90), so the market has not bid this to an uncritical high. A real edge must be sharper than "glass is real": it is a specific view on **timing and vendor selection** — e.g., that the missed 30-June date is a one-off slip (a press-crystallized expectation, not a filed commitment — the diligence supports this) rather than a pattern, and that the 23-Jul H1 or a subsequent quarter delivers the first hard glass-HVM order *on LPKF's tool* specifically (not Philoptics'). If you don't hold a view on *when* the order lands *and why it names LIDE over Philoptics*, you don't have an edge — you're underwriting the same option premium the sell-side has already flagged as rich.
- **Your tripwire — what would prove you wrong?** Any one of: (1) a *second* missed/slipped LIDE first-series-order date after the 30-Jun miss (credibility gone); (2) a rival TGV method (Philoptics) winning a *named* major design socket — especially at Intel — displacing LIDE-as-standard; (3) a deeply dilutive capital raise going through on the thin float; (4) the glass volume-production timeline slipping materially past 2027. Any one breaks the thesis — decide the action now.
- **Time-horizon fit:** the thesis resolves on the customer qualification calendar — plausibly 6–24 months, with the 23-Jul H1 the nearest read. It needs patience through burn; not a short-horizon trade despite the volatility.
- **Conviction-appropriate sizing:** **binary and single-catalyst-dependent** (one HVM order gate, contested by one main rival) — warrants smaller/hedged exposure, not a core position. The thin float amplifies both directions.
- **What kills the thesis fastest:** Philoptics (or Corning in-house) winning a named HVM reference socket at Absolics/SEMCO — designs LIDE out at the moment volume arrives (ties to Pre-Mortem §8 and gate §3). Second-fastest: a dilutive raise announced alongside another "no order" quarter.
- **Where the price sits vs. the thesis:** **already pricing meaningful optimism** — ~€4–€8/share of option premium above the sell-side DCF cluster. Underpriced only if you believe the first HVM order is both imminent and LPKF's; otherwise fairly-to-richly priced for a pre-order, loss-making name.
- **What to monitor next:** the 23-Jul-2026 H1 report (order color, backlog, cash); the Absolics dual-source decision and any SEMCO/GlaSSEM HVM tool award (LPKF vs. Philoptics); a fresh Bundesanzeiger short-position pull; any capital-raise signal; confirmation (or denial) of the inferred Intel/CPO relationship.

**Bottom line:** A high-quality, genuinely differentiated technology option — but an *option*, priced as one, on an event LPKF does not control and a rival is actively contesting. Own it only with a specific, dated view on the first HVM order and its vendor, in size appropriate to a binary bet — and treat 23 July, then the Korean fabs' HVM tool decisions, as the moments that prove or break it.

---

### Source-reliability note
Primary LPKF filings (FY2025 annual report 26 Mar 2026; Q1-2026 report 30 Apr 2026; AGM 4 Jun 2026; financial calendar) anchor financials, segments, capital stack, risk factors, and governance [T1] — text-extracted directly from the report PDFs. Counterparty capacity events (Sumitomo/GlaSSEM PR; NIST/CHIPS Absolics award; SKC rights offering) are primary/reputable [T1/T2]. Glass-roadmap and vendor-mapping items are established trade press (TheElec, TrendForce, DigiTimes, Börse-Express) [T2]; supply-chain vendor attributions and the Intel/CPO inference are trade-press/Substack tier [T2/T3] — explicitly not Tier-1. Explicitly unverified: any Tier-1 statement that a named counterparty uses LPKF LIDE for HVM (none exists); the Absolics→LPKF post-March-2026 switch (T3 rumor); the identity of LPKF's inferred exclusive US semi partner; a live reconciled blended analyst consensus; exact P/B and net-cash. The "missed 30-June deadline" is a press expectation, not a filed commitment.

*Not financial advice — informational research tooling only.*
