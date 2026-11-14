# Mechanism sheet — `ai-optics`

*Per [`sector-lens.md`](../sector-lens.md) §K.8. Reference for research agents, **not** a pre-commitment and not a thesis. Every row is derived from a dated report in this repo and carries its source; nothing here was written from memory. Members: AAOI, COHR, CRDO.*

**Sources.** **[C]** = [`tickers/COHR/reports/2026-10-04.md`](../../tickers/COHR/reports/2026-10-04.md) (§4, §5, §10). **[D]** = [`tickers/CRDO/reports/2026-08-22.md`](../../tickers/CRDO/reports/2026-08-22.md) (§4). Reliability tiers ([P] primary, [T] trade press, [T3] weak) are those reports' own and are not re-graded here.

## 1. The unit of content

**A port** — one high-speed link end (400G, 800G, 1.6T). Demand is counted in ports; what each port consumes depends on **reach** and **architecture**, and those two choices decide who gets paid. Optical ports consume **laser die** grown on indium phosphide (InP); short-reach ports may consume none.

## 2. Content per 1.6T port, by architecture

| Architecture | InP laser die per port | What it does to value | As of / source |
|---|---|---|---|
| **EML pluggable** | **≈8 EML** | Best reach and signal quality; uses the most InP and the scarcest part | 2026-10-04 [C §4] |
| **Silicon-photonics pluggable + CW laser** | **≈2 CW** | ~4x fewer InP die; value moves to the SiPho foundry and the assembler. Over half of a ~$40B transceiver market in 2026 (LightCounting, [T]) | 2026-10-04 [C §4] |
| **Co-packaged / near-packaged optics with external laser source** | **≈2 ultra-high-power CW** | **Removes the pluggable module.** Fewer, higher-priced lasers; engine value to TSMC and the switch vendor | 2026-10-04 [C §4] |
| **Heterogeneous InP-on-silicon** | integrated | Removes the discrete laser and the attach step | 2026-10-04 [C §4] |
| **VCSEL / GaAs** | **0 InP** | Short-reach scale-up only | 2026-10-04 [C §4] |
| **Copper (DAC / ACC / AEC)** | **0** | No optics at all inside its reach band | 2026-10-04 [C §4]; 2026-08-22 [D §4] |
| **PCB midplane / backplane** | 0 | **Removes the cable entirely**, in-rack | 2026-08-22 [D §4] |

## 3. Copper reach by SerDes generation — the copper/optics boundary

Reach roughly halves per SerDes doubling, because insertion loss scales with frequency [D §4]. As of 2026-08-22:

| | 400G (56G/lane) | 800G (112G/lane) | 1.6T (224G/lane) |
|---|---|---|---|
| Passive DAC | ~3 m | ~2–3 m | ~1–2 m (**contested**) |
| ACC (redriver) | ~5 m | ~4–5 m | ~2–3 m |
| AEC (retimed) | ~7 m | ~5–7 m | ~3 m |
| AOC / pluggable optics | 30–100 m | 30–100 m | 30–100 m |

**By reach tier** [D §4]: 0–2 m is passive copper; 2–7 m is the AEC band; 7 m to row scale is pluggable optics and AOC, with LPO/LRO and CPO entering; row-to-row and beyond is optics.

## 4. Who supplies which socket

| Socket | Named participants | As of / source |
|---|---|---|
| **EML die** (merchant) | Lumentum, Broadcom, Mitsubishi — ~72% combined [T]; Coherent not top three | 2026-10-04 [C §4, §5] |
| **CW-DFB laser die** | Broadcom and Sumitomo lead, then Coherent and LandMark — four ≈ 74% [T]; Coherent's is all captive, merchant share ≈ 0% | 2026-10-04 [C §5] |
| **Transceiver assembly** | Innolight, Eoptolink, Coherent, Lumentum, AAOI, Credo, Accelink, Cisco/Acacia, Jabil; Fabrinet moving from supplier to direct | 2026-10-04 [C §5] |
| **External laser source** | Lumentum, Coherent, TFC, Eugenlight, Sivers/O-Net/Enablence, Sumitomo | 2026-10-04 [C §5] |
| **InP substrates** | AXT (6-inch, Beijing) | 2026-10-04 [C §5] |
| **DSP** | Marvell, Broadcom | 2026-10-04 [C §5] |
| **AEC silicon** | Credo (224G/lane PAM4 SerDes and DSP); cable body and assembly are not proprietary (BizLink) | 2026-08-22 [D §4] |
| **Customers who can in-house** | Broadcom (captive InP, and a merchant seller), NVIDIA (owns the CPO architecture), Google (in-house OCS), Amazon | 2026-10-04 [C §5] |

## 5. The binding constraint

**Laser die — and specifically 200G EML chips at 1.6T** [C §10]. It is being attacked from both ends:

- **Demand side:** die per port falls ~4x as silicon photonics and co-packaged optics replace EML pluggables (§2 above).
- **Supply side:** capacity is multiplying — Broadcom more than tripling, Lumentum adding 50%+, Coherent doubling twice, heterogeneous InP-on-silicon shipping at volume [C §4, §5].

Whether supply outruns demand is **not settled by these facts**; LightCounting's framing is that EMLs may be replaced by silicon photonics while the overall InP laser market keeps growing [C §4].

## 6. Distinctions that are routinely got wrong

- **An EML is not a CW laser.** Both are InP, but they are different parts with different die counts per port and different supplier rankings (§2, §4). Treating "InP lasers" as one pool is the error that sat in COHR's first Edge (§K.8).
- **Three markets, not one** [C §5]: total transceivers at all speeds · high-speed AI datacom (800G/1.6T) · InP laser die. A share figure from one says nothing about another.
- **Owning InP is not selling InP.** A captive laser fab protects module share but earns no merchant rent on scarcity [C §10].
- **LPO/LRO attacks optical DSP content, not copper.** LPO removes the DSP; at 1.6T the industry moved toward LRO, which re-inserts a transmit-side DSP [D §4].
- **CPO and the cable-free midplane are different threats.** CPO replaces pluggables with optics at the switch; the midplane removes a copper socket with no optics involved [D §4].

## 7. Open disputes — unresolved, do not settle by assertion

- **CPO timing.** Dell'Oro calls 2026 the initial volume ramp and LightCounting expects high volume in 2027; SemiAnalysis argues cost and serviceability push NVIDIA's intra-rack CPO to 2028–29 [D §4, as of 2026-08-22].
- **Passive DAC reach at 224G/lane** — the ~1–2 m figure is contested [D §4].
- **InP: scarcity or surplus by 2027–28** — the central open question of §5.
- **Market size.** Yole and LightCounting differ by more than 40% on scope for 2031 transceivers [C §5].

## Change note

- **2026-11-14** — seeded from [C] and [D]. AAOI's reports were not used; a row that an AAOI report contradicts is a finding under §K.8.

_Not financial advice — informational research tooling only._
