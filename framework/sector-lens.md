# Sector lens — the indirect channel

*Section K of the equity research framework. How a ticker's sector membership is assigned, the closed registry of sectors, and how sector news is searched, assessed and logged. Other files reference this one — they do not restate it.*

---

## K.0 — Why this exists

Every name in this watch-list is a high-beta member of a theme complex. A material sector event moves the ticker **with no company event at all**, and until this section existed nothing in the framework required anyone to look for it.

The corpus proves the gap rather than merely asserting it. CIFR's log entry for 2026-07-09→17 records a **~25% drawdown in a window where CIFR itself did nothing** — no lease, no filing, no company news. The entire move was sector: a semiconductor/AI-infrastructure de-risking, plus peers (CleanSpark, TeraWulf) signing leases CIFR didn't match. That entry exists only because the researcher happened to look sideways; §F.2's hunt-list never asked for it.

**The failure mode is silent by construction.** A sector angle nobody searches produces no entries, and an absence of entries reads exactly like "nothing happened."

## K.1 — Assigning a sector: the three-part test

Each part is answerable from the ticker's own deep-dive report — this is a **derivation, not a separate research task**.

| Test | Question | Report section |
|---|---|---|
| **Peer-pricing** | Would a material item about a peer move this ticker with **zero** company news? The sector is the peer set the market prices it against. | **§5** Competitive comparison & moat |
| **Demand-aggregate** | Which single upstream spending aggregate does the thesis depend on? | **§6** Secular / thematic positioning |
| **Regime-residual** | Any leftover macro/asset-regime exposure not captured above? | **§10** Sector bottleneck / structural analysis |

**The anchoring rule — this is what keeps the lens from becoming a news firehose.** A candidate sector counts **only if a numbered Tripwire or a branch of the Edge references one of its variables.** If nothing in §18 turns on it, it is not this ticker's sector; it is background noise about an industry the ticker happens to sit in.

**Ordering is forced.** Membership is a function of the Tripwires, so it cannot be derived before §18 exists. Assign the sector immediately *after* deriving Edge/Tripwires, in the same step.

**At least one sector is mandatory** — everything trades against something. If no peer set can be named, that is a finding about the thesis, not a reason to skip: say so explicitly rather than inventing a catch-all slug.

**Record the transmission channel, not just the label.** For each sector, name *how* it reaches this ticker — **demand** (upstream spending) · **peer-comp** (multiple re-rates off comparable deals) · **supply** (input scarcity/pricing) · **regime** (macro/asset-price state). The channel is what makes an assessment possible; a bare slug is not actionable.

**Sunsets.** Where a membership is temporary, record the condition — and **anchor it to the Tripwire whose expiry is the same event** rather than building a second expiry mechanism. CIFR's `btc-mining` membership dies when HPC rent commences, which is precisely what expires Tripwire #4; when the audit flags #4 expired, the sector question rides along in that same human decision (§J.4).

## K.2 — The registry (closed vocabulary)

Deliberately closed, for the reason §F.1's tag vocabulary is: an open one drifts. The corpus already shows what that looks like — `Catalyst/Re-rate driver`, `Catalysts/Re-rate drivers` and `Sentiment/Re-rate drivers` all coexist as framework tags today, which is why the audit's work-order mapping has to sit in a judgment tier instead of a script.

| Slug | Scope | Standing watch items |
|---|---|---|
| `ai-dc-lessor` | AI/HPC datacenter lessors, colocation and neoclouds | Hyperscaler capex guides · peer lease/colo deals **and their terms** (the multiple comp, not just the headline) · neocloud funding & credit conditions (CoreWeave, Fluidstack, Nscale, Lambda) · power & interconnect policy (e.g. ERCOT ILLE) |
| `btc-mining` | Bitcoin price regime and miner economics | BTC price and ETF flows · hashprice · miner-to-HPC pivot announcements |
| `ai-optics` | Datacom optical transceivers and components | Hyperscaler capex · NVIDIA architecture shifts (CPO, external laser source, OCP standardization) · LightCounting / Cignal AI vendor rankings · EML and laser supply · China export policy |
| `catv-broadband` | Cable access-network capex (DOCSIS 4.0 cycle) | MSO capex guides (Charter, Comcast) · Dell'Oro DOCSIS forecasts · distributor channel health |
| `adv-packaging` | AI-accelerator substrates and advanced packaging | NVIDIA substrate allocation · ABF substrate capacity adds · glass-core / TGV roadmap events · TSMC CoWoS capacity |

**Adding a slug is a deliberate act.** A new ticker that fits nothing here gets its slug defined — scope, peer set, watch items — **in the same commit** that adds the ticker. Prefer reusing an existing slug over minting a near-duplicate.

## K.3 — Membership changes on a re-run

**Sector membership is scope, not a pre-commitment — and it does *not* inherit §A's never-overwrite invariant.** A Tripwire's whole value is that it was fixed in advance and cannot be softened once approached. A sector assignment has no such property: it is a search-routing decision, and getting it wrong means the wrong peers were searched, which the next run corrects. Applying commitment machinery here would add friction that buys nothing.

It is not symmetric either, and the asymmetry runs **opposite** to the audit's cheaper-route default (§J.2):

- **Widening is free.** Adding a sector searches more; the worst case is some irrelevant peer news that the materiality bar filters out.
- **Narrowing is dangerous.** Dropping a sector deletes a search angle, and the resulting blind spot is **invisible precisely because nothing gets logged from it**. Nobody notices an absence.

So: **additions apply freely and are noted. Removals require the recorded sunset condition to have actually occurred, and are stated as a finding** — a sector change is itself thesis news. CIFR moving from `btc-mining`-primary to `ai-dc-lessor`-primary *is* the pivot, and should read as loudly as a Tripwire status change.

## K.4 — Searching: the sector sub-agent

`latest-updates-workflow.md` §F.2 dispatches this as a **named, mandatory angle** alongside the company-specific ones. Its self-contained prompt carries:

1. Today's date and the ticker.
2. The ticker's `## Sector lens` section **verbatim** — memberships and transmission channels.
3. The registry entry above for each slug: scope and standing watch items.
4. The same search window as the rest of the run.
5. The ticker's Edge and numbered Tripwires verbatim — the sector agent assesses against the *same* triggers as everyone else.
6. Report-back format: dated items, direct source URLs, and **the transmission channel named per item** (demand / peer-comp / supply / regime).
7. An explicit stop condition and tool-call budget (§F.2's standing rule).

**Sub-agents research only — they must NOT edit files.**

## K.5 — Assessing: same machinery, per ticker

Sector findings run through the **same mandatory §18 assessment** as direct news (§F step 4). Nothing new is needed — the CIFR chip-rout entry already demonstrates the finished form, quoting peer moves and closing with *"No Tripwire fired: … (T#4), … (T#2), … (T#3), … (T#1)."*

**Impact is per-ticker and signed, never a global sentiment score.** The same headline can point opposite ways for two tickers in one sector: a glass-core high-volume commitment arriving early is **`[EDGE+]` for LPKF** (its option premium is the LIDE/TGV thesis) and **tripwire-adjacent for IBIDY** (Tripwire #3 is that exact substitution clock pulling forward). One search result, opposite signs — which is why assessment happens against *that ticker's* §18, not against the sector.

## K.6 — The materiality bar

Log a sector item **only if** it does one of:

- **(a)** bears on a named Tripwire or a branch of the Edge;
- **(b)** re-prices the peer group in a way that moves this ticker's multiple environment;
- **(c)** shifts a sector baseline the thesis quotes (e.g. the ~$725B aggregate hyperscaler capex figure inside COHR's Tripwire #3).

Anything else gets at most one line in the chat digest and **is not logged**. §F's no-placeholder rule applies unchanged: a quiet sector week produces no entry.

## K.7 — Logging: §F.1 unchanged

Sector-derived entries use the canonical §F.1 entry format with framework tag **`[Sector/<slug>]`**, then the usual `[EDGE±]` / `[TRIPWIRE #n — status]` at entry end.

The mandatory `→ impact` clause must **name the indirect channel explicitly**, so a later reader can tell a sector-transmitted move from a company event:

```
YYYY-MM-DD — [Sector/ai-dc-lessor] — **<headline>**. <detail> → <impact; no <TICKER>-specific
event, channel: peer-comp> [EDGE−]
```

**Audit tie-in:** `[Sector/…]` is a routing key. `scripts/audit_report.py`'s `WORK_STREAM_HINTS` maps it to the **sector** work-stream, so a stale sector-tagged entry sends a REFRESH work order to the right sub-agent (§J.6).
