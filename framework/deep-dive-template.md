# Full deep-dive template & mandatory sub-agent prompts

*Sections B, C, D, G, H of the equity research framework — the full-diligence report standard and the four mandatory parallel sub-agent prompt templates. Verbatim; relocated from the former single framework file. Section A (standing rules) and Section E (honest limits) live in `standing-rules.md`; the daily "Latest Updates" workflow (Section F) lives in `latest-updates-workflow.md`.*

**Output & publishing.** Write the finished report as markdown to
`reports/<YYYY-MM-DD>/<TICKER>.md` (today's date; one dated snapshot per run — do not
overwrite prior dates). Then update that ticker's `**Canonical deep-dive:**` line in the
**ticker's news.md** (`tickers/<TICKER>/news.md`) to link the new file, and commit. The
report is the source of truth and is published via GitHub Pages — no `.docx`, no external
sync.

**If this is a new ticker** (no `tickers/<TICKER>/` folder yet), create the folder and its
`news.md` as part of this run: that folder is the watch-list entry, and the daily watch
enumerates `tickers/*/` to find it. The news.md carries YAML front matter (`company`,
`blurb` — these feed the published homepage coverage grid via `hooks/coverage.py`), the
`**Canonical deep-dive:**` link, one-paragraph thesis context, and the §18 **Edge** and
numbered **Tripwires** derived from this report. A report without its ticker folder is
invisible to the daily watch; a folder without a `news.md` is skipped by both the watch and
the site build.

---

## B0. Output architecture — NON-NEGOTIABLE

*Added July 2026 after a gold-standard audit found reports were passing the section checklist while failing the depth and presentation bar. The sections below are not style preferences — **the table structures are the rigor mechanism.** A table with a "Significance" / "Read" / "Durability" column forces an explicit judgment on every row and makes an omission visibly empty; prose lets the same omission pass silently. The audit's finding: a report that merged the four re-rate buckets into one prose-adjacent table silently shipped with **zero** sentiment/technical drivers while its own body cited beta 1.71 and a crowded-proxy unwind. Structure caught what the checklist did not.*

### 1. Model pinning — MANDATORY

- [ ] **Run the orchestrator/synthesis pass on Opus.** The synthesis step — front-loading the argument, filling the "Read" column, netting the re-rate verdict — is where report quality actually lives. It is the least parallelizable and most judgment-dense step. Do not run it on a smaller model.
- [ ] **Dispatch all four mandatory sub-agents on Opus** (`model: opus` on the Agent call). Their output is the evidence base; a weaker model here degrades every downstream section invisibly, because the orchestrator cannot tell a thin brief from a thin fact pattern.
- [ ] **Record the model actually used** in the closing Methodology block (see B0.5). If a run was not on Opus end-to-end, say so in the report — an unpinned run is a quality caveat, not a silent detail.

### 2. Front matter — before §1

- [ ] **Title block:** `EQUITY RESEARCH — DEEP DIVE (EXHAUSTIVE DILIGENCE)`, company legal name, every listing line (exchange:code · ADR ticker **with its ratio** · HQ · FY end), and a one-line italic positioning tagline.
- [ ] **Metric dashboard — a ~14–16 cell table**, market data on one side, fundamentals on the other. Minimum: price (dated) · ADR price · market cap · fully diluted share count · 52-wk range · 12-mo change · trailing P/E + EV/EBITDA · consensus rating & avg PT | latest FY revenue (YoY) · operating profit (YoY) · net income (YoY, with any distortion flagged) · lead segment profit · next-FY guidance · largest customer (name + % of revenue) · #2 customer · capex program. A reader must get the whole quantitative shape of the name without scrolling.
- [ ] **Reference-price note + SOURCE-CONFLICT protocol.** Date every price. **When quote sources disagree, do not flag-and-abandon** ("~$41, unreconciled, treat as stale" is a failure). Run the cross-check and show the arithmetic: reconcile the ordinary against the ADR via the stated FX rate and ratio, then use a third anchor (e.g. the ADR's own 52-wk high) to disqualify the outlier. State which figure you adopted and why. An unreconciled headline price contaminates every multiple in §14.
- [ ] **NOT FINANCIAL ADVICE block** enumerating the specific primary sources relied on (with filing dates/accession numbers), the filer's regime where non-US (e.g. JP-GAAP, ¥ reporting, does not file with the SEC), and a note that low-tier share figures are labeled as such throughout.

### 3. Executive summary — MANDATORY, front-loaded, and complete

Not a teaser and not a deferral to §15. **A summary that says "see §15 for the full synthesis" has failed this bar.** It must stand alone and carry the entire argument:
- [ ] The one-paragraph statement of what the company is and what the debate actually is (quality vs. price vs. durability — name which).
- [ ] The two or three **hard, primary-sourced facts** that anchor the snapshot, each with its figure and filing source.
- [ ] **Three reasons to own — each with its honest counterweight**, fully developed inline (not cross-referenced).
- [ ] **What has to be true** — the conjunction the thesis rests on.
- [ ] **Bottom line** — a plain-English close.

### 4. Table mandate — these sections ship as tables, not prose

The gold standard uses **13 tables**; a report with 3 is not applying this framework. Required, at minimum:

| Section | Required table | The column that carries the rigor |
|---|---|---|
| Front matter | Metric dashboard | — (the at-a-glance grid itself) |
| §1 | Segment split | margin + YoY, not just sales |
| §2 | Catalysts | **Significance** — why it moves the thesis |
| §3 | **Four** separate typed tables | **Durability** + confidence-tiered impact |
| §4 | Level 2 landscape-by-role; market-share tiers | **Basis / reliability** per row |
| §5 | Level 1 competing technologies | **Trade-off vs. the subject's approach** |
| §7 | Income statement, actual vs. guidance | **Read** — the interpretation of each line |
| §9 | Bull / base / bear | **What drives it** + a skew note |
| §17 | Customer → demand transmission | **Impact on revenue & stock** |

### 5. Closing block — Sources, Methodology & Caveats

- [ ] **Methodology paragraph:** the dated diligence window, the four work-streams run, **the model used** (per B0.1), and every primary source named with its date/accession number; secondary/trade sources named separately.
- [ ] **Numbered key caveats** — a structured list, not a paragraph. Every unresolved conflict, every figure that could not be retrieved, every gap left open, each numbered so it can be cited and closed on the next run. The gold standard carries 7.

### 6. Depth floor

- [ ] **~7,000+ words for a full deep dive.** This is a floor for a genuinely exhaustive pass, not a target to pad toward — but a report landing near ~4,500 has almost certainly summarized where it should have diligenced. If the sources genuinely ran dry earlier, say so explicitly in the caveats rather than letting the length pass unremarked.

### 7. Numbers discipline at gold-standard depth

*The audit found the gold-standard document itself **failed** here, while the shorter report passed — so this cuts both ways and neither prior artifact is a numerical reference.*
- [ ] **A narrative repeated by trade press is not a balance-sheet fact.** Where a widely-reported story (e.g. "customers pre-funded the capex") is not in the filings, say so explicitly and state what the filings *do* show — even when the narrative is the more attractive sentence. The gold standard asserted a customer-prepayment split as fact when it existed only in trade press; the shorter report correctly caught that advances had *fallen* YoY. **Follow the shorter report's discipline here, not the gold standard's.**
- [ ] **Reconcile cash-flow line items against each other before writing them.** Do not let a construction-in-progress reclass be written up as debt repayment. If OCF, capex, and FCF do not tie, resolve it against the filing rather than picking the flattering read.
- [ ] **Give market-share figures a direction, not just a level.** "~35% of the high-end" is far less thesis-relevant than "~85% (2023) → ~55% (2026) as a named rival qualifies." A static share number with no trend is an incomplete finding.
- [ ] **Tag every claim inline with its source tier** (`[P]` primary / `[T]` trade press / `[T3]` market-report/Substack). Prose tiering in a closing note is weaker — the tier belongs next to the claim.

---

## B. Full deep-dive template — the standard sections

Use all that apply; not every question needs all eighteen. **§B0 (output architecture) is not optional and applies to every full report** — the sections below define the *content*; B0 defines the *form*, and the form is what enforces the depth.

1. **Business model & role in the value chain** — what it does, how it makes money, where it sits in the sector's stack. **Ships with a segment table** (sales · segment profit · margin · YoY) plus a "position in the value chain" paragraph that states explicitly what the company is *not* (not a chip maker, not an interposer maker) and which segment is the actual equity story vs. ballast.
2. **Recent catalysts** — the most significant recent events, each with a **date**, sourced from current news. **Ships as a table: Date | Event | Significance.** Order most-recent-first and **include upcoming/scheduled catalysts as rows** (flagged as upcoming), not just past events. Reach back far enough to catch structural events that still shape the landscape (a rival's take-private, a plant opening) — not just the last few weeks. The **Significance** column is mandatory per row: an event without a stated thesis consequence is a headline, not a catalyst. **Resolve status questions rather than deferring them** — "ownership in flux, status to verify" on a rival is a research gap, not a finding; go close it.
3. **Re-rate map** — the drivers that would expand or compress the multiple (not just move the price), each **classified by type** (fundamental / structural / sentiment-technical / macro — see Section D) and ordered by impact, with its **mechanism** (the specific discount it removes), an **estimated multiple impact with confidence tier**, **timing window**, and **durability**. **Render as FOUR SEPARATE TABLES under four bolded sub-headings — one per type — never one merged table with a "Type" column.** This is a hard requirement with a specific history: the merged form let a report ship with zero sentiment/technical drivers while its own body cited beta 1.71, a −10% session, and a crowded-proxy unwind. Four headings make an empty bucket impossible to miss. **Every bucket must be populated**; if one genuinely has no drivers, write that under its heading and justify it. Close with the **near-term binary gates** (ordered, highest-impact first) and a **net re-rate verdict** that names *which single bucket carries the most weight right now* — and, where the horizons differ, states the dominant bucket for the next 12 months separately from the 3–5 year thesis. See Section D for the full methodology.
4. **Competitive comparison & moat** — *this is a first-class section, not a paragraph.* Build it to the **full depth mandated in Section G** (Level 1 competing technologies/approaches; Level 2 company-landscape-by-role; estimated market share with tiers; head-to-head vs the single closest rival; source-reliability tiering) and close with an **explicit moat verdict** (thin / moderate / wide — and why, conditioned on the landscape).
5. **Technological moat & competitive technologies** — the company's core technological differentiation (proprietary architecture, patents/IP, performance edge, integration capability), benchmarked explicitly against peers' technology. **Distinguish genuinely proprietary, defensible tech from an orchestration/integration layer built on third-party components.** This section carries the **Level 1 technology/approach comparison** and the **defensibility assessment** from Section G (patents filed vs granted, replicability, switching costs, capital barrier; who controls each substitute) and gives a **verdict: technological moat durable, emerging (optionality), or absent.** (§4 and §5 together must fully satisfy the Section G standard — split the material between them however reads best, but omit nothing.)
6. **Secular / thematic positioning** — exposure to the relevant structural driver (agentic AI, power scarcity, etc.); note **first- vs second-derivative** exposure.
7. **Financials — contracted vs. recognized, unit economics, capital stack** — revenue growth, margins, financial health, cash / runway / financing stack. **Leads with an income-statement table: Metric | latest FY actual | next FY guidance | Read.** The **Read** column is the analytical payload — it interprets each line (e.g. "net income guided −9% on a base effect, not an operating turn; OP still +45%"). A §7 written as prose has skipped the interpretation step. **Explicitly call out any headline optics distortion** (one-time gains inflating a prior-year base, a guided decline that isn't operational) — a momentum holder misreading the headline is itself a re-rate trigger, and it belongs in §3's fundamental bucket too. **Explicit contracted-vs-recognized split.** GAAP vs non-GAAP. **Unit Economics & Capital Stack:** demand a breakdown of unit economics (cost to scale, yield/learning-curve trajectory, gross margin trajectory), and the profit bridge (price/mix vs. volume — state the ratio where derivable). Map the full capital stack — exact debt maturities, convertible strike prices and resulting diluted share count, and ongoing ATM equity dilution programs. **Reconcile OCF, capex, and FCF against each other and against the financing line** before writing any of them (per B0.7).
8. **Risks** — operational, financial, market. **Named and specific**, not generic. Draw on the actual 10-K risk factors where available. **Concentration & Geopolitics:** explicitly quantify customer concentration (e.g., "Customer A = 45% of revenue"). Map critical supply-chain dependencies (single-source materials, specific foundry reliance) and evaluate exposure to tariffs, export controls, or sovereign risk.
9. **Bull / base / bear** — **ships as a table: Scenario | Prob. | Price range | What drives it**, each with a **subjective probability** and a **price range**, anchored to a stated reference price and a valuation framework. **Close with an explicit skew note** — the shape of the distribution, not just its ends. State whether the bear case is a de-rating of a profitable franchise (floor = earnings power) or a solvency wipeout (floor = zero), and whether the bear path is faster-acting than the bull path. Two names with identical ranges can have opposite skews; the note is where that gets said.
10. **Sector bottleneck / structural analysis** — the binding constraint in the industry and how the name fits solving or monetizing it.
11. **Sentiment** — retail (Stocktwits / Reddit / forums) and institutional (13F / analyst), framed as a battleground where relevant.
12. **Asymmetry verdict** — floor vs ceiling. Is it a genuine low-floor / high-ceiling asymmetric bet, or a leveraged directional bet with fat tails? Be explicit.
13. **Management & Insider Alignment** — *a wide moat is useless if management destroys shareholder value.* Evaluate the C-suite's track record of meeting their own forward guidance. Summarize recent insider buying vs. selling over the trailing 6–12 months. Assess how management is incentivized (e.g., bonuses tied to revenue growth vs. return on invested capital / ROIC).
14. **Valuation Multiples & Implied Expectations** — *Section 9 gives a price range; this contextualizes the multiple behind it.* Identify the current valuation multiple (EV/EBITDA, NTM P/E, Price/Book, etc.) and benchmark it against its own 5-year historical average and direct peers. Explicitly state what growth rate the current stock price is already pricing in, and whether the multiple looks compressed or stretched.
15. **Investment thesis (synthesis)** — the closing distillation. A **3–4 bullet list of the most compelling, name-specific reasons to own the stock**, each paired with its **honest counterweight** (the specific thing that breaks it). Keep each reason differentiated (not generic sector beta) and each counterweight concrete (tie to the Pre-Mortem where relevant). Close with a one-line synthesis of **what has to be true** for the thesis to work. **This section does not substitute for the front-loaded executive summary (B0.3) — both ship.** The exec summary carries the argument for a reader who reads nothing else; §15 is the distillation *after* the evidence has been laid out. An exec summary that defers to §15 has failed B0.3.
16. **Review of the investor's submitted thesis (CONDITIONAL — only when one was submitted)** — when the reader has supplied their own thesis or read on the name, assess it explicitly rather than silently writing around it. Three parts: **(a) Confirmed correct** — which of their mechanisms the diligence supports, quantified against primary sources (their instinct + your figure). **(b) Corrections & refinements** — where the diligence contradicts or sharpens them; be specific about *which leg* is wrong (e.g. "right mechanism, wrong lead customer"), and name what their thesis omits that the report weights heavily. **(c) Net assessment** — a fair, direct verdict that neither flatters nor dismisses. Correct a wrong mental model before crediting a right conclusion (per Section A). **Omit this section entirely when no thesis was submitted — do not invent one to review.**
17. **Customer demand → stock price & future growth** — the transmission chain from end-customer demand to the equity, stated explicitly rather than left implicit. Open with the **chain in one line** (e.g. *unit volume × content per unit × the company's share × price/mix → segment revenue → operating leverage → earnings → multiple*), then a **table: Customer | Demand signal (dated, with figures) | Impact on revenue & stock** — one row per material customer, each labeled by role (PRIMARY driver / STABLE anchor + optionality / INCREMENTAL accelerant / PARTIAL capture). Close by translating to **near term (≈12 months), medium term (2–4 years), and long term (4+ years)**, naming which variable dominates each horizon. **The key discipline:** demand is necessary but not sufficient — state explicitly what converts an "influx of orders" into *this company's* earnings (share retention against dual-sourcing, capacity timing, price/mix), because that gap is where most customer-demand theses break. This section is where customer concentration stops being a §8 risk bullet and becomes a model.
18. **Final thoughts & conclusion** — the closing wrap for the *whole report*, not just the bull case in §15. Pull the threads from every prior section (business model, catalysts, re-rate map, moat, financials, risks, valuation, sentiment, asymmetry, management) into one coherent final read on where the name sits today. Then give the investor a concrete pre-investment checklist:
    - **Your edge — what do you believe that the crowd doesn't?** State the one differentiated view the thesis rests on, in plain language. If the honest answer is "nothing — I just agree with where the stock already is," say so: that itself is a finding (you're paying for consensus, so the only way to win is if consensus is simply too cautious). This is the single most important gut-check — an idea with no variant view is a bet that the market stays mispriced in your favor for no particular reason.
    - **Your tripwire — what would prove you wrong?** Name the single specific, observable event — a missed print, a lost contract, a named metric crossing a stated line — that would mean the thesis is broken and it's time to exit or re-underwrite, decided *in advance* rather than rationalized away afterward. (Distinct from "what kills the thesis fastest" below, which is the underlying *mechanism*; this is the concrete *trigger + action* you commit to before you own it — the discipline that separates a plan from bag-holding.)
    - **Time horizon fit** — how long the thesis needs to play out to resolve (tie to the binary gates / catalyst calendar) vs. a shorter trading horizon.
    - **Conviction-appropriate sizing** — flag explicitly when the thesis is binary or single-counterparty-dependent (warrants smaller/hedged exposure) vs. genuinely diversified across multiple independent catalysts.
    - **What kills the thesis fastest** — the single fastest-acting invalidation trigger, cross-referenced to the Pre-Mortem (§8) and the highest-impact near-term binary gate (§3).
    - **Where the price already sits relative to the thesis** — underpriced, fairly priced, or already pricing in the optimistic case (tie back to §14 Valuation Multiples).
    - **What to monitor next** — the specific dated catalysts/gates worth tracking going forward.
    Close with a short, plain-English bottom line. Keep this section generic/framework-level guidance the investor applies themselves — **no unsolicited portfolio-fit or position-sizing commentary specific to the reader** (that stays request-only, per the standing rule in Section A).

---

## C. Catalyst / milestone tracking — when watching a name

- [ ] Confirmed earnings date, or an estimated window flagged as such.
- [ ] Each upcoming milestone: **what + when (date/quarter) + why it matters + pass/fail threshold.**
- [ ] Ordered by impact on the thesis, highest first.
- [ ] Scheduled events (earnings) separated from unscheduled catalysts (contract signings, financing closes).

---

## D. Re-rate mapping — methodology (backs Section B.3)

Now a **standard section of every full deep-dive** (Section B.3), not just an on-request extra. Also used standalone when the question is specifically "what re-rates it."

- [ ] **Classify every driver by type** — don't lump a contract win in with a short squeeze:
  - **Fundamental** — company-specific execution/financial events (contract win, capacity ramp, margin inflection, guidance raise/cut).
  - **Structural** — sector/peer-driven multiple shifts (peer re-rate/sympathy move, index inclusion/exclusion, capital rotation into/out of the theme).
  - **Sentiment / technical** — positioning-driven, not fundamentals-driven (short covering/squeeze, momentum/flow, retail attention spikes, options gamma/dealer positioning).
  - **Macro** — rate path, risk-on/risk-off regime, dollar/commodity moves, policy shifts (tariffs, subsidies, export controls) that reprice the whole group.
- [ ] Order drivers by impact on the **multiple**, not on the price.
- [ ] For each driver: the **mechanism** (which specific discount it removes) + an **estimated multiple impact** (e.g., "+1–2x EV/EBITDA") **with a labeled confidence tier** (high / moderate / low) — never a fabricated precise point estimate; state what the estimate is anchored to (peer comp, historical precedent, management commentary) + the **timing window**.
- [ ] Distinguish **priced-in known events** from genuine **new information**.
- [ ] **Flag durability per driver** — structural and sentiment/technical drivers can move the stock hard and fast but tend to mean-revert; state whether each driver re-rates the multiple *structurally* (sticky) or moves price *transiently* without changing the multiple's foundation.
- [ ] Name the **near-term binary gates** that resolve most of the thesis.
- [ ] Close with a **net re-rate verdict** — net the upside re-rate potential against the downside de-rate risk across all four buckets, and state which single bucket carries the most weight for this name right now.

---

## G. Competitive Moat & Landscape — MANDATORY depth standard (backs Section B.4–B.5)

*The competitive landscape is one of the most decision-relevant parts of any thesis and must be built to the depth below in EVERY full report — never a one-line "peers are X, Y, Z." A dedicated sub-agent (prompt template at the end of this section) produces this when running multi-agent; single-threaded runs must still produce the full structure. Split the output across Sections B.4 and B.5 however reads best, but include all six elements.*

**1. Level 1 — competing / substitute TECHNOLOGIES or approaches (not just companies).** A table of the rival *ways to solve the same problem* — for a tech/semis name these are technical approaches (e.g., laser-induced etch vs. direct laser drill vs. photosensitive glass vs. plasma/DRIE); for a non-tech name, competing business models / delivery mechanisms. For each: **how it works · who champions it · its specific trade-off vs. the subject's approach** (cost, quality, yield, throughput, capital intensity). State which approach the industry is converging on and why.

**2. Level 2 — company landscape mapped BY ROLE in the value chain.** Not a flat peer list — group players by function: **(a) direct rivals** (same product/socket), **(b) adjacent / complementary players**, **(c) suppliers**, **(d) customers who could vertically integrate / in-house the function** (a key, often-missed threat). Name real companies in each bucket with a one-line role.

**3. Estimated market share among all competitors — with honest data discipline.** Give the reader a share picture, but:
   - **Distinguish audited revenue share from "design-in" / qualification / self-reported metrics.** A company's own "N% of customers selected us" is *design-in breadth*, not revenue share — label it as such and attribute it to the company.
   - **When no hard third-party share data exists (common in nascent markets), say so explicitly and use tiers** — *leader / strong #2 / niche / latent-scaling-threat* — with a **clearly-labeled illustrative estimate** (ranges, not false-precision points). **Never fabricate a precise %.** Cite the data vintage and whether the market is pre-volume.
   - Include the **market-size** context (TAM today vs. projected, with CAGR) and flag when sources disagree because they scope the market differently (substrate vs. equipment vs. material, etc.).

**4. Head-to-head with the single closest competitor.** Identify the *one* rival that actually competes for the same sockets and go deep: where they win/lose against each other, shared customers (dual-sourcing), any public technical disputes or claims/counter-claims, and who is gaining. This is usually where the real moat question is decided.

**5. Source-reliability tiering.** Explicitly rank the evidence: **primary/company filings & IR > established trade press (e.g., TheElec, DigiTimes, Yole, TrendForce) > retail research / Substack / forums.** Do not state low-reliability claims (exclusivity deals, unconfirmed design wins, aggressive timelines) as fact — attribute and hedge them.

**6. Moat verdict, conditioned on the landscape.** Thin / moderate / wide AND durable / emerging (optionality) / absent — explicitly reasoned against *who else is in the race and who could scale in*. Distinguish genuinely proprietary/defensible tech from an orchestration/integration layer on third-party components. Name the single most likely way the moat erodes (ties to the Pre-Mortem).

### Hard-coded sub-agent prompt template (competitive-moat/landscape agent)

*Fill the [BRACKETS] and dispatch as one of the parallel diligence agents on every full run.*

> You are doing competitive-moat and landscape diligence for an equity research report. Today is [DATE]. Knowledge cutoff is stale for markets — verify everything via web tools, never from memory, never fabricate; flag anything unverifiable and tier your sources by reliability. COMPANY: [COMPANY] ([TICKER]); its core product/technology is [CORE TECH/PRODUCT]. Produce a dense, sourced brief with these six parts, each with dates + source URLs:
> 1. **Level 1 — competing/substitute technologies or approaches:** a table of the rival ways to solve the same problem — how each works, who champions it, and its specific trade-off vs. [COMPANY]'s approach (cost/quality/yield/throughput/capital). State which approach the industry is converging on and why.
> 2. **Level 2 — company landscape by role:** group real named players into (a) direct rivals, (b) adjacent/complementary, (c) suppliers, (d) customers who could vertically integrate/in-house the function.
> 3. **Estimated market share:** distinguish audited revenue share from self-reported "design-in"/qualification metrics; where no hard data exists, say so and give labeled illustrative tiers (leader / strong #2 / niche / latent threat) with ranges — never fabricate precise %. Include market-size (TAM now vs. projected + CAGR) and note where sources disagree on scope.
> 4. **Head-to-head vs. the single closest competitor:** where each wins/loses, shared/dual-sourced customers, public disputes or competing claims, who is gaining.
> 5. **Source-reliability tiering:** primary/IR > established trade press > retail/Substack; do not present low-reliability claims as fact.
> 6. **Moat verdict:** thin/moderate/wide AND durable/emerging/absent, reasoned against who else is racing and who could scale in; distinguish proprietary defensible tech from an integration layer; name the single most likely way the moat erodes.
> Return sourced, tiered, and explicit about what could not be verified.

---

## H. Filing, Counterparty & Sector — MANDATORY sub-agent templates (backs Section A)

*These three, together with the competitive-moat/landscape agent (Section G), are the four mandatory parallel sub-agents dispatched on every full run. Fill the [BRACKETS] and dispatch each as its own agent; when running single-threaded, still cover all three work-streams directly.*

### Hard-coded sub-agent prompt template (filing agent)

> You are doing primary-filing diligence for an equity research report. Today is [DATE]. Knowledge cutoff is stale for markets — pull filings directly from SEC EDGAR (or the equivalent primary regulator for non-SEC filers, e.g. a German SE's Bundesanzeiger/IR filings), never rely on secondary news summaries; flag anything unverifiable or undisclosed. COMPANY: [COMPANY] ([TICKER]). Produce a dense, sourced brief, each item dated with a source URL/filing reference:
> 1. **Latest primary filings** — 10-K/10-Q/8-K (or 20-F/6-K/local equivalent) — filing dates and direct links.
> 2. **Customer-concentration %** — each named customer as a share of revenue, dated.
> 3. **Segment splits** — revenue/margin by reportable segment.
> 4. **Cash-flow statement** — operating cash flow vs. PP&E capex, dated; CapEx-vs-OpEx read (asset-building vs. structural burn).
> 5. **Full risk-factor section** — named and specific items, not paraphrased into generic categories.
> 6. **Insurance/coverage disclosures.**
> 7. **Related-party transactions.**
> 8. **Capital stack** — debt maturities, convertible strike prices, ATM/SBC programs, basic and fully diluted share count.
> Return sourced, dated, and explicit about anything not disclosed or unverifiable.

### Hard-coded sub-agent prompt template (counterparty agent)

> You are doing counterparty diligence for an equity research report. Today is [DATE]. Verify everything via primary sources; never fabricate; flag anything unverifiable. COMPANY: [COMPANY] ([TICKER]). Identify every material counterparty — anchor tenants/customers, the controlling parent, key financing partners/lenders — and for each produce:
> 1. **Who they are and their role/relationship to [COMPANY]** (dollar or percentage exposure where disclosed).
> 2. **Their own solvency** — recent financials, credit ratings, leverage.
> 3. **Their own recent capital raises, funding rounds, or liquidity events** — a counterparty's own funding round can be the single most thesis-relevant fact and will not appear in [COMPANY]'s own filings.
> 4. **Any public signs of financial stress** — covenant issues, credit downgrades, missed payments, management turnover.
> 5. **Concentration risk this creates for [COMPANY]** if this counterparty's ability to pay/perform breaks down — remember, their ability to pay **is** the thesis.
> Return sourced, dated, and explicit about what could not be verified.

### Hard-coded sub-agent prompt template (sector agent)

> You are doing market/sector diligence for an equity research report. Today is [DATE]. Use connected finance/data tools for live data; never rely on stale training data for current figures. COMPANY: [COMPANY] ([TICKER]). Produce a dense, sourced, dated brief:
> 1. **Current price, market cap, fully diluted share count, 52-week range.**
> 2. **Short interest** — % of float, days-to-cover, recent trend.
> 3. **Options positioning** — notable OI/volume skew, implied volatility percentile.
> 4. **Analyst coverage** — consensus rating, price targets (high/low/average), recent revisions.
> 5. **Peer/theme linkages** — which sector ETFs, indices, or thematic baskets include this name, and how correlated its recent moves are to the broader theme vs. idiosyncratic/company-specific.
> 6. **Recent sector-wide news** that could be macro/structural re-rate drivers (rate moves, index rebalances, peer earnings read-throughs).
> Return sourced, dated, and explicit about what could not be verified.

---

*Standard adopted July 2026 (competitive-landscape depth standard, Section G, added July 2026; filing/counterparty/sector mandatory sub-agent templates, Section H, added July 2026; Final Thoughts & Conclusion added July 2026; "Your edge" (variant-perception) and "Your tripwire" (falsification/exit-trigger) gut-checks added to its pre-investment checklist July 2026; the "Latest Updates" workflow (Section F) now mandatorily assesses each news item against the §18 Tripwire and Edge, with [TRIPWIRE]/[EDGE+]/[EDGE−] tagging, July 2026).*

***Gold-standard audit, July 2026 — the current bar.** Benchmarked the report corpus against the Ibiden/4062 Opus deep-dive. Finding: reports were passing the section checklist while failing on depth and form — all five clustered at ~4,500–5,600 words vs. the benchmark's ~7,400, and used 3 tables where the benchmark used 13. The audit's core lesson is that **the table structures ARE the rigor mechanism**, not decoration: a merged re-rate table let a report ship with zero sentiment/technical drivers while its own body cited beta 1.71 and a crowded-proxy unwind. Changes made: **Section B0 (output architecture)** added as non-negotiable — model pinning (Opus for orchestrator + all four sub-agents), front-matter metric dashboard, source-conflict cross-check protocol, a mandatory front-loaded executive summary, the 13-table mandate, a numbered-caveats closing block, a ~7,000-word depth floor, and numbers discipline. The template grew to **18 sections**: §16 (review of a submitted investor thesis, conditional) and §17 (customer-demand transmission chain) added; Final Thoughts renumbered to §18.*

***A note on the benchmark's own limits — read this before treating it as a reference.*** *The audit found the gold-standard document **failed** the numbers-discipline bar in places the shorter report passed: it asserted a customer-prepayment split as fact when it existed only in trade press, and its capex/FCF/debt-repayment figures conflict with the shorter report's read of the same filings (¥64.3B vs ¥106.1B capex; "comfortably positive FCF" vs "FCF ≈ ¥0"). **The benchmark is the architecture standard, not a numerical source.** Where the two conflict, resolve against the primary filing — and follow the shorter report's filing-level skepticism (B0.7), not the benchmark's. The target is the benchmark's structure with that report's rigor.*

*Applied to every ticker unless you override it for a specific request.*
