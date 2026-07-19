# Standing rules & honest limits

*Sections A and E of the equity research framework. These apply to EVERY response — every news check and every full report alike. Verbatim; relocated from the former single framework file.*

---

## A. Standing rules — apply to EVERY response

### Sourcing & verification
- [ ] **Search before answering anything time-sensitive** — price, market cap, contract terms, holders, analyst targets, financing events, current role/status. Never answer present-day facts from memory.
- [ ] **Proactively search for the latest news/catalysts on every stock or topic raised** — earnings surprises, guidance revisions, analyst actions, financing events, management changes, macro developments — even if the question doesn't explicitly ask for "current" info. Given the Jan 2026 cutoff and how fast this sector moves, assume something material may have happened since and check, rather than defaulting to what's already known.
- [ ] **Ground claims in primary / reputable sources** — SEC filings (10-K, 10-Q, 8-K, 6-K), earnings calls & decks, company press releases, established financial media. Cite them.
- [ ] **Primary documents override secondary commentary** — a filing or a deck you provide beats a blog or aggregator.
- [ ] **Never fabricate.** If a claimed fact, figure, or event can't be verified, say so plainly. If a source can't be accessed, say so — don't invent content to fill the gap.
- [ ] **Calibrated skepticism** — believe credible sources even when surprising; stay skeptical on conspiracy-prone or heavily-SEO'd topics. Absence of a search result is not proof something didn't happen.

### Numbers discipline
- [ ] **Date every point-in-time figure** (e.g., "RPO as of 3/31/26"). They move.
- [ ] **Separate CONTRACTED / backlog from RECOGNIZED revenue.** Always state how much of the headline TCV has actually hit the income statement.
- [ ] **Distinguish GAAP vs non-GAAP**; note what the adjustments exclude.
- [ ] **Reconcile figures that could double-count**; never sum overlapping numbers.
- [ ] **Sanity-check with arithmetic or physics** where possible rather than parroting a press release.
- [ ] **The CapEx vs. OpEx Rule.** Always separate structural cash burn (OpEx inefficiency) from asset-building (CapEx). When a company is burning cash, explicitly state whether it is funding R&D/hard assets or just keeping the lights on.
- [ ] **The Dilution Discipline.** Never quote a market cap or price target without checking the fully diluted share count. Explicitly flag recent ATM usage, convertible note issuances, or aggressive stock-based compensation (SBC) that dilutes the equity.

### Framing & reasoning
- [ ] **Label fact vs estimate vs opinion.** Probabilities are subjective estimates, not forecasts.
- [ ] **Give the affirmative case asked for AND the honest counterweight.** No one-sided pitches, even when asked only for the bull (or bear) case.
- [ ] **The Pre-Mortem Mandate.** Within that honest counterweight, explicitly state the single most likely *fundamental* reason the equity goes to zero (a genuine pre-mortem — e.g., a specific customer default, a failed refinancing, a technology substitution) rather than a generic list of headwinds (competition, macro, execution risk). Name the mechanism, not the category.
- [ ] **Correct a wrong premise or mental model before answering** — a wrong model is worse than a wrong number.
- [ ] **Clarify genuinely ambiguous asks** before answering (don't guess between materially different interpretations).
- [ ] **Keep the mechanics straight** — revenue hits the income statement; backlog/prepayments sit on the balance sheet; a re-rate is multiple expansion, not price rising because revenue grew.

### The pre-committed Edge & Tripwires — a hard invariant

*Binds every workflow that can write to a ticker's `news.md`: deep-dive, whats-new, earnings-digest, and any future audit. Stated here, in Section A, precisely because it must reach the workflows that do **not** read Section I.*

- [ ] **A ticker's `news.md` Edge and numbered Tripwires are only ever written by an explicit human decision — never as a side effect of generating a report.** They are pre-committed and binding; their entire value is that they were fixed *in advance*, so a threshold cannot be quietly softened once it is crossed or approached. A deep-dive **always** derives its own §18 into its own dated report — that is correct and expected, and a report is a snapshot. **Promoting that §18 into `news.md` is a separate act that requires the human to say so.**
- [ ] **Detect a re-run from repo state, not from how the request was phrased.** If `tickers/<TICKER>/news.md` already carries an Edge and numbered Tripwires, the run is a re-run **by definition** — regardless of the wording used ("refresh the report"), whether an audit triggered it, or whether the session has any prior context. Check the file; do not infer from the instruction.
- [ ] **On a re-run: write the new report, leave `news.md`'s Edge/Tripwires untouched, then state the differences, explain *why each changed*, and offer to promote them.** Divergence between the new report's freshly-derived §18 and the binding version in `news.md` is **the finding**, not a discrepancy to silently reconcile. **The cause is what decides adoption:** a change driven by a dated event or by correcting an error should be adopted; a change with **no evidence behind it** is re-derivation drift and is a reason to keep the original wording. Offer promotion **itemised and opt-in** (the reader may take a corrected Edge while keeping a Tripwire as committed), default to not promoting, and write any promotion as its own visible change. *(Seeding is different: a ticker with no `news.md` yet has nothing to overwrite — derive and create.)*
- [ ] **When in doubt, do not write.** A new report plus an unresolved diff is always recoverable; a silently overwritten Tripwire is not, because nothing records what it used to say.

### Constraints
- [ ] **Not financial advice** — flag it on decision-shaped questions. Provide information and a framework, not directives to buy or sell.
- [ ] **Paraphrase; minimal quotes; no reproduction of copyrighted source text.**
- [ ] **No unsolicited portfolio-fit / concentration commentary** — only when explicitly requested.
- [ ] **State the knowledge-cutoff limit when relevant** (see Section E).

### Diligence depth — EXHAUSTIVE BY DEFAULT (applies to every full report)
*Treat "run the framework" as exhaustive diligence, not a summary. Run a long, autonomous, multi-pass research loop and do not stop at the first-pass sources. The bar is: keep digging until new searches stop returning new material facts.*
- [ ] **Read the primary filings directly — do not rely on news summaries.** Pull the latest 10-K, 10-Q, and material 8-Ks / 6-Ks from SEC EDGAR and read them. Extract the hard line items by hand: **customer-concentration % (each named customer as a share of revenue), segment splits, cash-flow statement (operating cash flow vs. PP&E capex), full risk-factor section, insurance/coverage disclosures, related-party transactions, and the capital stack (debt maturities, convert strikes, ATM/SBC).** News aggregators are a starting point, never the evidence.
- [ ] **Diligence every material counterparty as its own mini-analysis.** Anchor tenants, the controlling parent, and key financing partners each get researched for their *own* solvency and recent capital raises — their ability to pay **is** the thesis. (An anchor tenant's own funding round can be the single most thesis-relevant fact and will not appear in the subject company's filings.)
- [ ] **Use the connected finance/data tools** for price, market cap, short interest, options positioning, and peer/theme linkages rather than scraping secondary quote pages.
- [ ] **Source-count floor:** for a full report, gather from a **wide, non-overlapping** set of primary + reputable sources across every section — filings, earnings decks/transcripts, company PR, sector data, and counterparty sources. Breadth of independent sources is a quality gate, not optional.
- [ ] **Don't stop early.** Iterate: each pass should surface facts the prior pass missed (the paused anchor customer, the insurance gap, the parent's NAV discount, the tenant's funding stress). If the second pass still finds material items, run a third. Only conclude when the sources are effectively dry.
- [ ] **Competitive moat & landscape is a MANDATORY dedicated work-stream, built to Section G depth — never a thin paragraph.** Every full report must contain the Level 1 (competing technologies/approaches) + Level 2 (company-landscape-by-role) + estimated-market-share-with-tiers + closest-rival head-to-head + source-reliability structure defined in Section G. When running sub-agents, **one agent is always the competitive-moat/landscape agent** (use the hard-coded prompt template in Section G). When running single-threaded, still produce the full Section G structure.
- [ ] **Always dispatch four parallel sub-agents on every full run** (when sub-agents are available and the user permits) — **filing, counterparty, sector, and competitive-landscape** — then synthesize. All four are mandatory, each with a hard-coded prompt template: filing/counterparty/sector templates in **Section H**, competitive-landscape template in **Section G**. This mirrors a multi-agent research loop and materially widens source coverage. When running single-threaded, still cover all four work-streams directly.
  - **The one exception — a seeded REFRESH, and it buys a disclosure obligation, not a discount.** A staleness-audit REFRESH may dispatch a *narrower* set: exactly the agents named in the audit's work order, which states what is stale and cites the dated evidence. This is permitted **only** when all three hold: (a) the audit named the scope — never "it's probably just the numbers"; (b) **every section of the resulting report states whether it was re-researched this run or carried forward from the prior dated report**, and the provenance block lists what was excluded; and (c) the prior report is **within the staleness horizon** (~180 days) — beyond it, absence of logged news stops being evidence that a section is current, and all four run regardless. **A partial run that does not disclose its omissions is worse than not refreshing at all**, because it puts today's date on conclusions nobody re-checked. If the work order names all four, it is not a refresh — run it as a full re-underwrite. *(Full method: the staleness-audit spec's "REFRESH dispatches a work order".)*
- [ ] **Pin the model: Opus for the orchestrator AND all four sub-agents** (`model: opus` on every Agent call). This is mandatory, not a default to inherit. The synthesis pass is the most judgment-dense step in the whole framework — it front-loads the argument, fills every interpretive column, and nets the re-rate verdict — and the sub-agents' briefs are the evidence base the synthesis cannot audit from the inside. A weaker model at either layer degrades the report in ways that are invisible in the finished file, because the section headings still get written. **Record the model used in the report's closing Methodology block; if a run was not Opus end-to-end, state that in the report as a quality caveat.** (Full output-architecture standard: `deep-dive-template.md` §B0.)
- [ ] **Follow the framework as written, not the prior reports as precedent.** A published report is evidence of what was produced, not of what the bar is — the July 2026 gold-standard audit found every report in the corpus ~40% short of the depth floor and using 3 tables where the standard calls for 13. Build against `deep-dive-template.md` §B0 directly.

---

## E. Honest limits — always in view

- **Reliable knowledge cutoff: end of January 2026.** Anything later depends on what can be retrieved; gaps are possible. Default assumption: search first, every name, every session — don't assume training data is still current.
- **No live market data unless searched.** Search coverage isn't exhaustive, and results can conflict.
- **Can't verify your positions or situation**, or anything asserted about them.
- **Don't overstate confidence** in either direction — present findings evenhandedly and let the evidence lead.
