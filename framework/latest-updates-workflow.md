# "Latest Updates" workflow — the complete "what's new" spec

*Section F of the equity research framework — the single, complete home for the "what's new / latest on [ticker]" check: the procedure, plus the three mechanical specs it applies. Read alongside `standing-rules.md` (Sections A + E), which binds every step here.*

> **Numbering note (July 2026 audit).** The Edge/Tripwire pre-investment checklist lives in the deep-dive's **Final thoughts & conclusion** section. That is **§18** in the current template (which grew to 18 sections); reports published **before the July 2026 gold-standard audit carry the same checklist at §16**, and the ticker news.md files correctly cite §16 against those existing reports. Follow the section *name*, not the number, when they disagree.

> **Consolidated July 2026.** The research method (§F.2) and the run-summary digest format (§F.3) previously lived in a separate `news-check.md`, because they were shared between this workflow and a scheduled all-ticker daily watch. That daily watch was removed, so the two files were merged here — **one workflow, one file.** Anything that previously cited `news-check.md` §A now cites **§F.2**; anything that cited `news-check.md` §B now cites **§F.3**. **§F.1 is unchanged** and keeps its number, since the ticker news.md files and the earnings-digest workflow anchor to it.

**The three specs — one home each, referenced never restated:**

| Spec | What it governs | Where |
|---|---|---|
| **Research it** | The parallel sub-agent method, source quality, search window, stop condition | **§F.2** |
| **Store it** | The `## Recent News Log` entry format in a ticker's news.md | **§F.1** |
| **Report it** | The chat-reply run-summary digest | **§F.3** |

*(The numbers do not run in flow order — §F.1 keeps its number because it is anchored from every ticker's news.md and from `earnings-digest.md`. Read them as: research **§F.2** → store **§F.1** → report **§F.3**.)*

**Plus three assessment disciplines (added November 2026) — also one home each.** The Tripwire/Edge assessment in step 4 answers *"what does this do to the thesis?"* It does not answer *"was this news to the market?"*, *"how big is it?"*, or *"how real is it?"* — and an item can be right on the first question while silent on the other three.

| Discipline | The question it answers | Where |
|---|---|---|
| **Expectations baseline** | Delivered against *what*? Was it already known? | **§F.4** |
| **Impact sizing** | Which value driver, how large against a dated base, when? | **§F.5** |
| **Maturity ladder** | For a technology item: which rung is *evidenced*, not claimed? | **§F.6** |

None of the three adds or changes a tag — §F.1's closed vocabulary is untouched. They govern what the entry's detail and `→ impact` clause must contain.

**Also used by the earnings digest.** `earnings-digest.md` (Section I) applies **§F.2**'s research method and source-quality guidance to its own three sub-agents, and **§F.1** verbatim for the news items a call discloses. It does **not** use §F.3 — the earnings chat reply has its own format (§I.7).

---

## F. "Latest Updates" workflow

*Triggered by requests like "latest on [ticker]," "what's new with X," "any updates on X."*

1. **Check whether a full framework report already exists** for the ticker (`tickers/<TICKER>/reports/<YYYY-MM-DD>.md`, with the Edge/Tripwires mirrored into the ticker's news.md at `tickers/<TICKER>/news.md`). **Resolve the actual latest by globbing `tickers/<TICKER>/reports/*.md` and sorting by date** (CLAUDE.md's report-resolution rule) — never trust the news.md `Canonical deep-dive:` line blindly; refresh it if it's stale.
   - If not: **build the full report first** (per `deep-dive-template.md`, written as a dated markdown report at `tickers/<TICKER>/reports/<YYYY-MM-DD>.md`), create the ticker's folder and news.md, derive the §18 Edge/Tripwires into it, then continue.
2. **Search for recent news/events** tied to the stock since the last dated entry in the ticker's Recent News Log (or since report creation, if this is the first check) — using the agentic **parallel research sub-agent** method in **§F.2 below** (self-contained sub-agent prompts, source-quality guidance, first-run ~14-day window). Don't research single-threaded — dispatch a thorough sub-agent pass on the ticker (or several in parallel split by research angle) for full search quality.
3. **Categorize each event against the framework's own sections** — Business model, Catalysts, Re-rate drivers, Moat/Competition, Technological moat/competing tech, Secular positioning, Financials/Capital stack, Risks/Concentration/Geopolitics, Bull/Base/Bear, Bottleneck fit, Sentiment, Asymmetry, Management/Insider activity, Valuation multiples, Investment thesis — to gauge which part of the thesis it actually touches.
4. **Assess every event against the §18 Tripwire and Edge — MANDATORY.** For each piece of news, explicitly ask:
   - **Does it trip the Tripwire?** Does the event match (or move materially toward) any of the pre-committed exit/re-underwrite triggers named in the ticker's Edge/Tripwires (in the ticker's news.md, `tickers/<TICKER>/news.md`, restated verbatim from the deep-dive report's §18)? If yes, this is the highest-priority finding: **flag it prominently at the top of the chat reply AND in the Recent News Log entry**, tag the entry **[TRIPWIRE]**, state which specific trigger fired and how close it is to the stated threshold, and note the pre-committed action (exit / re-underwrite). Never bury a tripwire event inside a routine news list.
   - **Does it strengthen or weaken the Edge?** Does the event support or undermine the differentiated/variant view the thesis rests on (§18 "Your edge")? Tag it **[EDGE+]** if it corroborates the variant view, **[EDGE−]** if it cuts against it (i.e., consensus was right and your edge is eroding). An accumulation of EDGE− items means the differentiated thesis is failing even if no single tripwire has fired — say so explicitly.
   - **Delivered against what? — the expectations baseline (§F.4).** For every item carrying a figure, a date or a guide, state the baseline it is measured against and the verdict (above / in line / below / new / already known). An item with no stated baseline cannot say whether it was news.
   - **How big, on which driver, and when? — impact sizing (§F.5).** The `→ impact` clause names the value driver the item touches, sizes it against a dated base figure, dates when it lands, and says which of the report's Bull / base / bear drivers it bears on. "Not sizable" with the missing input named is a valid answer; a bare "positive for the thesis" is not.
   - **For a technology or product item — which rung is evidenced? (§F.6).** Place it on the maturity ladder and weight it at the rung the evidence supports, not the rung the release claims. Test its technical content against the slug's **mechanism sheet** (`sector-lens.md` §K.8); a claim that contradicts the sheet is either news or an error, and the entry must say which.
   - **Sector findings get this identical treatment — same questions, same tags.** A sector item is assessed against *this ticker's* §18, not scored at the sector level: the same headline can point opposite ways for two tickers sharing a slug (see `sector-lens.md` §K.5). Apply the **§K.6 materiality bar** before logging — bears on a Tripwire or Edge branch · re-prices the peer group · shifts a sector baseline the thesis quotes — and log per §K.7 with framework tag `[Sector/<slug>]`, naming the transmission channel in the `→ impact` clause. Below the bar: one line in the digest at most, never an entry.
   - If the ticker's news.md has no §18 Tripwire/Edge on file yet, **derive them first — from the LATEST report**, resolved by globbing `tickers/<TICKER>/reports/*.md` and sorting by date (CLAUDE.md's report-resolution rule), never from whichever report you happen to have open or the `Canonical deep-dive:` link. **State which dated report you derived them from.** These become the *binding* pre-committed triggers everything downstream is measured against, so seeding them from a superseded report installs a stale thesis as the baseline — the most expensive place in the system to be wrong. **Assign the ticker's sector(s)** in a `## Sector lens` section per `framework/sector-lens.md` §K.1 — derived from that same report's §5/§6/§10 and anchored against its §18 (membership only counts if a Tripwire or Edge branch references one of the sector's variables), with the transmission channel named per sector and slugs drawn from the closed §K.2 vocabulary. **Write the tripwires as a bullet list, one `- **(n)** ...` line per numbered trigger, not one dense paragraph** — split a report's prose into one bullet per `(n)` as a formatting change only, never rewording, dropping, or merging what a trigger says. **Append the `| # | Expires |` table** (`framework/staleness-audit.md` §J.4) immediately after the tripwire prose — one row per numbered trigger, dated from the trigger's own text where it names a window, else ~12 months out as a review horizon. The date is its own field; never splice it into the verbatim prose. Then assess, and note that you derived them.
5. **If there's substantive, dated news:** append it to the ticker's `## Recent News Log` per **§F.1 below — the canonical entry format**. Do not restate or paraphrase that spec anywhere else; apply it as written.
6. **If nothing substantial turns up:** say so in the chat reply — do **not** add a placeholder or "no news" entry to the ticker's news.md. Keep the log clean. (Still state explicitly that you checked the news against the Tripwire and Edge and nothing fired — a clean check is itself a useful, reassuring result.)
7. **End with a run summary.** Produce the chat-reply digest in the **canonical format defined in §F.3 below**, scoped to the ticker(s) asked about.

*Note: this presupposes a full deep-dive report (and therefore the ticker's news.md §18 Edge/Tripwires) already exists — see step 1. If starting fresh without it, build the report first and derive the Edge/Tripwires, then continue.*

---

## F.1 Recent News Log — canonical entry format (SINGLE SOURCE OF TRUTH)

*The one authoritative spec for **how a news item gets written into a ticker's news.md**. This workflow (step 5 above) and the earnings digest (`earnings-digest.md` §I.5) both use it verbatim. **Edit here only.** Other files reference this section; they do not restate it.*

### Where it goes

- **Append to the `## Recent News Log` in the ticker's news.md — `tickers/<TICKER>/news.md` — most recent first.** Each watched ticker is a **folder** under `tickers/`, named for the symbol, holding that ticker's `news.md` (thesis context, Edge, numbered Tripwires, and the living log). The folder is the unit of the watch-list; the news.md is its state.
- **Never to the deep-dive report.** `tickers/<TICKER>/reports/<YYYY-MM-DD>.md` is a dated point-in-time snapshot and is immutable once published; ongoing news accumulates **only** in the ticker's news.md.
- **Never add "no news" placeholder entries.** If a ticker's research pass found nothing material within the window, leave that ticker's log unchanged. A clean check gets reported in the chat digest, not written to the file.
- **Price alone is not a material event, however it's tagged.** A move whose only stated cause is sentiment, rotation, de-risking or positioning — with **no dated disclosure behind it** (a filing, a release, a peer print, a policy action, a disclosed insider transaction) — is not loggable, whether tagged `[Sentiment/Technical]` or `[Sector/<slug>]`, and even when the price happens to cross a round number or a Tripwire's stated price precondition. A Tripwire fires on a real event; a price level crossing with nothing behind it is commentary on the tape, not a finding. Report it in the chat digest (§F.3) as colour if at all, and hold the news.md entry for whichever dated disclosure actually confirms or breaks the thesis next. Worked example and the sector-specific carve-out: `sector-lens.md` §K.6.

### Format

```
YYYY-MM-DD — [FRAMEWORK-TAG] — **Headline**. Full detail of the event → impact/implication. Source: [Name1](URL1), [Name2](URL2) (<date>). [TRIPWIRE/EDGE± if any]
```

- **`YYYY-MM-DD`** — the event's date, not the run date.
- **`[FRAMEWORK-TAG]`** — the framework section the event actually touches (Business model, Catalysts, Re-rate drivers, Moat/Competition, Tech moat, Secular, Financials/Capital stack, Risks/Concentration, Bull/Base/Bear, Bottleneck, Sentiment, Asymmetry, Management/Insider, Valuation, Thesis). Short tag, right after the date.
- **Headline** — bolded, one line, leads the summary portion so the entry is scannable before the full detail.
- **Assessment tag** — per the mandatory assessment in step 4 above, **at the very end of the entry, after the source citation** — mirrors the chat-digest per-item line format in §F.3, so the headline and its substance read first and the classification reads as the entry's closing verdict. Include only when one applies; omit entirely otherwise, don't pad with "none." **This positional rule is forward-looking only** — it governs new entries; existing log entries are historical record and are never rewritten to match a later format revision. The vocabulary is closed — see below.

### Assessment-tag grammar (CLOSED VOCABULARY)

**Why this is closed rather than free-text:** these tags are not decoration. The staleness
audit routes off their **polarity**, and a misread is expensive in a specific direction — a
tripwire whose own text says *"does not fire"* must never be counted as fired, or it
dispatches a full four-sub-agent re-underwrite for nothing. Free-text statuses cannot be
classified reliably, so the vocabulary is fixed and machine-checked
(`scripts/lint_news_log.py`, via `tickerlib.parse_assessment_tags`).

**Edge tags — binary. There are exactly two, and no qualifiers:**

| Tag | Meaning |
|---|---|
| `[EDGE+]` | Corroborates the variant view |
| `[EDGE−]` | Cuts against it — consensus was right, the edge is eroding (**U+2212**, not a hyphen) |

**If an item does neither, it carries no Edge tag** — per the omit rule above. Do not invent a
neutral tag and do not append qualifiers (`[EDGE+, tangential]`): the strength, the nuance and
the "why" already live in the entry's mandatory full detail and `→ impact` clause, where a
human reads them. A qualifier adds nothing a machine can use and nothing a reader lacks.

> **Not to be confused with §F.3's ⚪ "EDGE live test."** That is a *digest-level status* —
> what state the Edge is in right now, summarised across the run — not a per-item
> classification. An individual news item either corroborated the variant view or cut against
> it; the Edge as a whole can separately be under an unresolved live test. Two different
> questions, two different layers.

**The rule that decides whether a tag value should exist: does it change what happens?**
`[EDGE−]` counts toward the audit's re-underwrite threshold and `[EDGE+]` is its
counterweight, so both earn their place. A neutral value would route to nothing. (This is
also why tripwires legitimately carry three statuses while edges carry two — each tripwire
status routes differently; see below.)

**Tripwire tags** — always numbered, always with a status:

```
[TRIPWIRE #<n> — <status>]
```

| Status | Meaning | Audit polarity |
|---|---|---|
| `fires` | The pre-committed trigger tripped. The stated action (exit / re-underwrite) is due. | **fired** |
| `early-warning` | Moving toward the threshold; not tripped. State the distance. | early-warning |
| `does not fire` | Assessed against the trigger and explicitly did **not** trip. | not-fired |

Free elaboration may follow the status keyword: `[TRIPWIRE #4 — does not fire, touched but
not sustained]`. **`#n` is mandatory** — "which trigger" is the whole point; an unnumbered
tripwire tag is a lint failure.

**A tag with no recognised status is a hard lint failure**, deliberately: an unclassifiable
tag would otherwise be silently assumed one way or the other by the audit.

**Legacy spellings** already in the corpus (`[EDGE — live test, unresolved]`,
`[EDGE+, tangential]`, `[TRIPWIRE #n — live, unresolved]`, `… — touched, not sustained`) are
**accepted on read and mapped**, but flagged as warnings for canonicalisation. Per the rule
above, they are **not** retroactively rewritten — history stands as written. New entries use
the closed vocabulary only.

**Sector-derived entries** carry framework tag **`[Sector/<slug>]`** in the leading tag
position (slug from the closed §K.2 vocabulary), then the usual assessment tags at entry end.
Their `→ impact` clause must **name the transmission channel and state that no company event
occurred**, so a later reader can tell an indirect move from a direct one — e.g.
`→ … no CIFR-specific event; channel: peer-comp`. Full spec: `sector-lens.md` §K.7.

### Content rules

**Length ceiling — roughly 1,200 characters (~150–200 words) per entry.** A log nobody re-reads has failed at its actual job, which is to be the accumulated state a future run and a future reader work from. Entries that run 3,000–5,000 characters are not more rigorous; they are the research pass pasted in rather than distilled, and the finding drowns.

**Reference instance:** IREN's **2026-07-01 Together AI entry** (`tickers/IREN/news.md`) — read it there rather than from a copy here. ~1,200 characters, and every part earns its place: a one-sentence headline carrying a single finding, two sentences of figures, an explicit `→` clause naming the *specific* tripwire clause it bears on, the honest limits in one clause, source, tags. That shape is the target.

- **Detail that changes the assessment stays; everything else goes.** The anti-gloss rule still binds — "reported strong results" is still a failure, and exact figures, named counterparties and deal terms still belong *in* the entry so it stands on its own. But that was never a licence for length. **Cut:** broad-market colour that is not about this ticker (index levels, peer ticks, macro narration beyond the one line that explains the move); prose assessment of tripwires the item does **not** move (the tag says it — `[TRIPWIRE #3 — does not fire]` needs no paragraph); meta-commentary about what a *previous* entry said; and multi-sentence confidence essays where one clause does the work ("price is quote-derived, moderate confidence").
- **One finding per headline.** If the bolded headline needs two "and"s or an em-dashed second clause to fit everything, that is two entries.
- **One entry per distinct event.** Split a multi-fact disclosure — an earnings call covering several separate items, say — into **separate entries**, each independently dated, categorized, and tagged. Never merge unrelated facts into one line to save space.
- **State the implication, not just the fact.** The `→ impact/implication` clause is mandatory and is the entry's centre of gravity: *what this does to the thesis*. It should be readable on its own and name the tripwire clause or Edge branch it touches, not gesture at "the thesis" generally.
- **State the baseline, the size and the rung — one clause each, inside the ceiling.** Per **§F.4**, the detail names what the item is measured against (`vs. guide $2.2–2.4B (8/12): above the top`). Per **§F.5**, the `→` clause sizes the item on a named driver against a dated base. Per **§F.6**, a technology item states its evidenced rung. These **displace narration; they do not raise the length ceiling** — each is a clause, and an entry that cannot fit them is carrying colour it should cut. Where one cannot be established, say so in a few words (`no baseline found`, `not sizable: prepayment terms undisclosed`) rather than omitting it silently.
- **A correction to an earlier entry is its own entry**, dated the day the correction was established — not a parenthetical bolted onto an unrelated item. That keeps both the original and the correction independently readable, and stops one entry carrying two jobs.

**This is forward-looking only.** It governs new entries; existing log entries are historical record and are **never** rewritten to match a later format revision — the same rule the assessment-tag positional convention above carries, and for the same reason: the log is a dated record of what was known when, and retro-editing destroys that.

### Sources

- **Every source is a markdown link to its direct URL** — the actual article, filing, or press release, so the reader can click through and verify it themselves. A bare publication name is not a citation.
- **No linkable URL** (e.g. a paywalled terminal feed): write the name plain, without brackets, and say so — never fabricate a URL, and never drop the attribution silently.
- Multiple sources are comma-separated; the trailing `(<date>)` is the publication date.

### Tripwire escalation

If any entry carries `[TRIPWIRE]`, it must **also** surface at the top of the chat digest as a headline callout (per §F.3) — naming which numbered trigger fired, how close it sits to its stated threshold, and the pre-committed action (exit / re-underwrite). Never let a tripwire exist only inside the log, and never bury it in a routine news list.

---

## F.2 Research method — parallel research sub-agents

Do not research single-threaded — use the agentic, multi-agent pattern even for a one-off "what's new" request. **This is the quality bar for getting new info on a stock: parallel research sub-agents, not a single quick search.**
- **Multiple tickers (a check spanning several names):** dispatch **one sub-agent per ticker, all in parallel** in a single dispatch (via the Task/Agent tool).
- **Single ticker ("what's new on X"):** dispatch a thorough research pass on that one ticker — one dedicated sub-agent, or several in parallel split by research angle (e.g. filings/financing vs. product/competitive vs. sentiment/positioning) when the question warrants depth.
- **Plus one mandatory sector/thematic sub-agent — always, on every run.** The company-specific angles above only find events the *company* generated; a material sector event moves the ticker with no company event at all, and that miss is silent (an angle nobody searches produces no entries, which reads exactly like "nothing happened"). Its prompt is specified in **`framework/sector-lens.md` §K.4** — it carries the ticker's `## Sector lens` verbatim, the §K.2 registry entry for each slug, the same search window, and the same Edge/Tripwires as every other agent. Findings are assessed and logged exactly like direct news (§K.5–K.7), never as a separate sentiment score.

**Plus the adversarial pass on a confirmation run — `adversarial-review.md` §L.** Every agent above is dispatched with the Edge verbatim *and a hunt-list derived from it* (item 5 below), so they all search the thesis's own terms; the 2026-07-29 COHR run sent four and all four came back `[EDGE+]`. When a ticker's Edge has accumulated **five or more consecutive same-signed items with no contrary one**, dispatch the §L red team as well — it is deliberately **denied the hunt-list**, and its findings are **reconciled, never averaged** against the others. Full spec in §L; do not restate it here.

Each sub-agent runs a thorough, multi-query pass — no fixed query cap; **typically 6-10+ distinct searches**, following threads, using WebFetch on primary sources where accessible. **Sub-agents research only — they must NOT edit any files.** Wait for all sub-agents to finish, then the orchestrator synthesizes every report and does all file writes itself. This mirrors the framework's Section H multi-agent pattern (`deep-dive-template.md`).

Each sub-agent's prompt must be self-contained (it has no memory of the parent conversation) and must include:
1. Today's date and the ticker/company name.
2. An instruction to `Read tickers/<TICKER>/news.md` first (the ticker's news.md — one folder per ticker under `tickers/`, the folder name is the symbol) and quote, verbatim and not from memory or paraphrase: its exact Edge, its numbered Tripwires **each paired with its `Expires` date from the `| # | Expires |` table** (§J.4 — the date lives in its own field, so a trigger quoted without it is missing half its meaning), and its **`## Sector lens`** memberships and transmission channels. **Then read two reference inputs:** the **mechanism sheet** for each of the ticker's slugs (`framework/mechanisms/<slug>.md`, per `sector-lens.md` §K.8 — if none exists, say so in the report-back and do not improvise one from memory), and the **base-case anchors** — the news.md `## Thesis context` paragraph and the latest report's Bull / base / bear table (latest by glob, per CLAUDE.md), which carry the dated figures an item is sized against (§F.5). Quote the **trigger text only** — the italic provenance preamble and any `### Change log` entries are archival edit-history, not part of the pre-commitment, and must not be carried into the prompt.
3. The search window: since the last dated entry in that ticker's Recent News Log, or **~14 days back if the log is empty** (see First-run window below).
4. The Source-quality guidance below.
5. An explicit hunt-list: one line per numbered Tripwire plus the Edge's specific mechanism, so the sub-agent searches for what would actually break or confirm the thesis, not just generic company news. **Order the hunt-list by proximity to expiry, nearest first, and state each trigger's `Expires` date on its line.** A trigger whose window closes in ten weeks and one that closes in three years do not deserve equal search effort — and the near-expiry ones are exactly where the staleness audit escalates (§J.4), so an unranked hunt-list has the research pass and the audit looking at different things. **For the sector agent, the hunt-list is the §K.2 registry's standing watch items for each of the ticker's slugs, plus its `## Sector lens` transmission channels** — and every reported item must name which channel carried it (demand / peer-comp / supply / regime).
6. A report-back format: every material dated item with exact date + source name **with its direct URL** (the actual article/filing/press-release link, not just a publication name) + **full substantive detail** (figures, named parties, terms — not a vague gloss), each assessed against that ticker's actual Tripwires/Edge. If a source has no directly linkable URL (e.g. a paywalled terminal feed), say so explicitly rather than omitting the link silently. **Each item also returns the three assessment inputs:** **(a)** its **baseline** per §F.4 — what was guided, previously filed or expected, with that baseline's own date and source, or an explicit "no baseline found"; **(b)** the **raw figures needed to size it** per §F.5 — amounts, durations, start dates, share counts — reported as found, with the sizing arithmetic left to the orchestrator; **(c)** for a technology or product item, the **evidenced rung** per §F.6 and what evidences it, plus any point where the item **contradicts the mechanism sheet**.
7. **An explicit stop condition.** Bounding the *scope* is not the same as telling the agent when to *stop* — write the sufficiency test into the prompt: **"Stop as soon as you can answer the items above, and report what you have."** Give a soft budget and a hard one (e.g. "aim for ~6–10 tool calls; if you pass ~20, stop and report what you have with the gaps named"), and state plainly that **a gap you name is worth more than a gap you spend ten more searches failing to close** — a flagged "could not retrieve X" is a usable result the orchestrator can caveat, while extra queries that still fail are pure latency. The rule is "stop when the listed items are answered **or demonstrably unreachable**," never "stop when tired": an unreachable required item is itself a finding and must be reported, not silently dropped.

Do not iterate to exhaustion beyond that, do not chase every tangential source, and do not re-verify facts already settled in the ticker's news.md thesis context. If a sub-agent's search turns up nothing material, that's a valid, complete result — don't force a finding. *(This bounded scan is distinct from a full "run the framework" deep dive, which IS exhaustive per Section A's Diligence-depth rule.)*

### Source quality
Favor primary/reputable sources — SEC EDGAR filings (10-K/10-Q/8-K/6-K), company press releases and IR pages, wire services (PR Newswire, Business Wire, GlobeNewswire, Reuters, Bloomberg), and established sector trade press (e.g. DigiTimes, TrendForce for semis). Quote-aggregator/data-only pages (Yahoo Finance quote, Google Finance, Investing.com quote, Morningstar quote, TradingView symbol page, CNBC quote, stockanalysis.com) carry price data but rarely article content — don't treat them as a source for a news item; run follow-up queries narrowed to a specific event type (e.g. "<ticker> 8-K", "<ticker> press release") instead. When using WebSearch, pass `blocked_domains` for these quote-only sites if the tool supports it.

**Non-US filers:** a ticker that does not file with the SEC has a different primary-source set — e.g. a Japanese TSE filer's 決算短信 (kessan tanshin) and 有価証券報告書 via TDnet/EDINET, a German filer's Bundesanzeiger/IR releases. Point the sub-agent at the right regulator and IR site rather than EDGAR, and expect primary sources in the local language; link them anyway and note the language.

### First-run window
If a ticker's Recent News Log is empty (first-ever check), search back **~14 days**, not just ~48h — a tight window on day one silently misses material context (a financing, a contract, a filing) that predates the check. Once the log has at least one dated entry, revert to the tight "since the last dated entry" window for all subsequent runs.

---

## F.3 Run-summary output format

Produce a short chat-reply digest that **leads with the actual news items found** — so the reader sees what's worth recording in the log before any assessment — then gives the tripwire/edge assessment beneath. The full multi-paragraph detail lives in each ticker's `## Recent News Log` (in that **ticker's news.md** — `tickers/<TICKER>/news.md`), not the chat reply — EXCEPT the Tripwires/Edge-shifts bullets below, which each get one detailed line per hit, not just a bare list.

**Escalation override — a fired tripwire always leads.** If any `[TRIPWIRE]` fired this run, put its 🚨 callout at the very TOP of the reply, above the items list — a fired tripwire is the highest-priority output and must never be buried under routine news. Absent a fired tripwire, the items list leads. Either way, when a tripwire fires the digest headline must say so.

Order of the digest:

- **Per-ticker items — FIRST.** List every substantive item found this run, one per item, most recent first, as a **headline + one-sentence abridged digest** — a step up from headline-only, but still NOT the full multi-clause paragraph (that stays in the ticker's news.md Recent News Log). Format — **the `[FRAMEWORK-TAG]` goes at the END of the line**, so the headline and its impact read first:
  `YYYY-MM-DD — **Headline**. One-sentence abridged digest of what happened → brief impact. [TRIPWIRE #n / 🟢 EDGE+ / 🔴 EDGE− if applicable] [FRAMEWORK-TAG]`
  Keep the digest to one sentence per item. **That sentence carries the §F.4 verdict and the §F.5 size where they exist** (`…revenue $2,370M, above the top of the guide → …`) — they are what tells the reader whether the item was news and whether it is large, so they are the last things to cut. If nothing material was found for a ticker, write "nothing material" instead of a list.
- **🚨 TRIPWIRES:** one bullet per `[TRIPWIRE]` hit (across every ticker checked this run), format:
  `**<TICKER> Tripwire #n — <status, e.g. "live, unresolved" / "early-warning" / "checked, does not fire">.** <one clause: what happened, why it matters, and the next test/date if still pending>.`
  If a ticker had no tripwire activity, a one-line `<TICKER>: none` is enough — don't pad it. If nothing fired anywhere, just say "none."
- **Edge shifts:** one bullet per `[EDGE+]/[EDGE−]` item (group same-direction items for one ticker into a single bullet if there are several), format — **emoji-tagged (🟢 EDGE+ / 🔴 EDGE− / ⚪ EDGE live test) the same way 🚨 tags Tripwires above, and a one-line parenthetical summary of the Edge itself is inline, the same way the Tripwire bullet carries its own context inline, so no separate recap block is needed**:
  `**<TICKER> — 🟢 EDGE+ / 🔴 EDGE− / ⚪ EDGE live test** (<the Edge's variant view, condensed to one line, taken from the ticker's news.md, not memory>).** <one clause: what the item was, with its dated anchor>.`
  Omit a ticker entirely here if it had no edge activity — don't pad with "none."
- **📅 Next checkpoints — closes the digest.** Always a **bullet list — one bullet per live, dated forward test** (a pending Tripwire threshold, a scheduled report, a construction/regulatory milestone named in the news items above), ordered **most-imminent first**. **Every bullet bolds both the date and the event** — this is the consistent standard; never collapse it into a comma-separated run-on line. Format:
  `- **<YYYY-MM-DD>** — **<the event / forward test>** (<optional one clause: which Tripwire/Edge it resolves, or what a pass vs. fail looks like>).`
  In a multi-ticker run, lead each bullet with its ticker (`- **<TICKER>** · **<YYYY-MM-DD>** — **<event>** …`); a single-ticker run omits it. This is what turns "nothing fired" into an actionable forward look rather than a dead end. Omit the block entirely only when there is no live dated checkpoint to name.

For a single-ticker "what's new" request this collapses naturally to that one ticker; for a check spanning several names it runs across every ticker checked.

---

## F.4 Expectations baseline — delivered against what?

*Applied in step 4 to every item that carries a figure, a date or a guide. Added November 2026.*

**Why this exists.** A stock moves on news **minus what was already expected**. The Tripwire/Edge assessment measures an item against *this thesis*; it says nothing about whether the item was a surprise. Without a baseline, "revenue $2.37B" is a fact with no sign — the same number is a beat, a miss or a non-event depending on what was guided and what the street carried. The corpus already does this well where a company guide exists (COHR's 2026-11-04 print is logged against the $2.2–2.4B guide) and not at all where it doesn't.

**Use the highest baseline available, and name which one it is:**

| # | Baseline | Where it comes from | Standing |
|---|---|---|---|
| 1 | **The company's own prior commitment** — a guide, a stated date, a stated target | The prior print, deck or release; often already in this log | Primary |
| 2 | **The previously disclosed state** — the last filed value of the same line | The prior filing (`scripts/facts.py`), or the prior log entry | Primary |
| 3 | **Dated sell-side consensus** | A named source with its own date | **Estimate — label it as one** |
| 4 | **The report's own base case** — what *this thesis* assumed | The latest report's financials and Bull / base / bear table | The thesis's expectation, not the market's |

**The verdict is one of five words, stated in prose** (it is not a tag): **above** · **in line** · **below** · **new** (first disclosure — no prior expectation existed) · **already known** (restates something disclosed on a named earlier date).

**Rules:**

- **"Already known" is not a new event.** If the item restates a disclosure already in the log, it is not logged again and never counted twice — a second headline about the same fact is not a second fact.
- **A baseline carries its own date and source**, exactly like the item. "Above expectations" with no named expectation is the gloss §F.1 forbids.
- **Consensus is the one permitted use of an aggregator figure — as a labelled estimate, never as a fact, and never as the source for the item itself.** §F.2's source-quality rule is unchanged for news. If only an undated or unattributed consensus figure can be found, that is "no baseline found."
- **Never fabricate a baseline, and never back-solve one from the price reaction.** "The stock fell, so it must have missed" inverts the inference and is the §F.1 price-only failure in another form. **"No baseline found" is a complete, honest result** — state it in those words.
- **Surprise and thesis direction are two different questions.** An above-consensus print can be `[EDGE−]`, and a miss can be `[EDGE+]`. The baseline verdict never decides the tag, and the tag never decides the verdict.
- **A qualitative event** (a suit, an appointment, a policy action) has no numeric baseline; apply the **new / already known** test only.

**Earnings digest:** `earnings-digest.md` has its own actual-vs-guide-vs-consensus table for the debrief. This section governs the **news.md log entries** the call produces, which §I.5 routes through §F.1.

---

## F.5 Impact sizing — which driver, how large, when

*Applied in step 4 to every logged item. Governs the `→ impact` clause. Added November 2026.*

**Why this exists.** "Corroborates the Edge" gives a direction and no magnitude. A booth demonstration and a 10-Q line can each end as one `[EDGE−]`, and a headline contract value reads as large until it is annualised and dated. The tag stays binary by design (§F.1); **the size belongs in the `→` clause, where a human reads it.**

**The `→` clause answers four things:**

1. **Driver** — which line of value the item touches: **revenue** · **margin** · **cash flow** · **share count** (dilution) · **balance sheet / liquidity** · **multiple** (risk, duration, or the terminal assumptions the market capitalises). Name one; an item that touches several names the largest.
2. **Magnitude against a named, dated base.** The base figure comes from the news.md `## Thesis context` or the latest report (resolved by glob) — say which and give its date. Show the arithmetic in compressed form and **label it derived**.
3. **Timing** — the period it lands in, and whether it is one-off or recurring.
4. **Scenario direction** — which **stated driver** in the latest report's Bull / base / bear table the item bears on, and which way. *(Reports predating the 18-section template may number that section differently — follow the name.)*

**Rules:**

- **Annualise and date a headline contract value.** Section A's contracted-vs-recognised rule applies: state when recognition starts and what it is per year. Worked from the corpus: COHR's 2026-11-04 PhotonLink disclosure is "~$20B, five-year, ramping from early CY2028" — roughly **$4B a year on a flat-line assumption (derived), none before CY2028**, against FY2026 revenue of $7,118.2M. The headline and the sized version are not the same finding.
- **Direction only on scenarios — a news check never restates a probability or a price range.** Those belong to the dated report, which is immutable; re-weighting them is a refresh or a re-underwrite (`staleness-audit.md`). The entry says *"bears on the Bear driver 'InP flips to surplus' — toward"*, nothing more. **An accumulation of items pushing one scenario's drivers the same way is itself a finding — say so in the digest**, the same way step 4 requires for accumulating `[EDGE−]`.
- **"Not sizable" is a valid result, with the missing input named** — `not sizable: prepayment terms undisclosed`. That is more useful than a number nobody can source, and it tells the next run what to look for.
- **Never invent a magnitude.** Where the input is hedged, give a range and keep the hedge. Standing rules' arithmetic sanity-check applies: a size that fails a one-line cross-check against the base is not written.
- **Size the item, not the thesis.** One clause. This is not a mini-valuation and does not justify exceeding §F.1's ceiling.

---

## F.6 Technology items — the maturity ladder

*Applied in step 4 to any technology or product-readiness item, whether the company's own or a sector peer's. Added November 2026.*

**Why this exists.** Technology news arrives in the vocabulary of the party announcing it, and "demonstrates", "samples", "ramps" and "ships" are not interchangeable. The corpus already weighs this by hand — the 2026-09-21 Marvell entry in COHR's log is tagged "at demonstrator weight", and COHR's Tripwire #4(b) turns on vendors "shipping production volume" rather than announcing. This section makes that weighting a fixed scale so it is applied the same way across tickers and runs.

| Rung | Stage | What evidences it |
|---|---|---|
| 1 | **Announced** — paper, roadmap, intent | A release, a talk, a standards contribution |
| 2 | **Demonstrated** — booth, lab, hero result | A demo with stated parameters; no customer |
| 3 | **Sampling** | Samples stated as shipped to customers, named or not |
| 4 | **Qualified** — design-win, customer qualification passed | A customer or third party naming the part, or a disclosed qualification |
| 5 | **Production volume** | Shipment data, a named bill of materials, a customer statement |
| 6 | **Revenue** | Recognised and disclosed in a filing or a print |

**Rules:**

- **State the rung evidenced and what evidences it.** Where the announcing party claims a higher rung than a third party can check, record both: *claimed 5, evidenced 3*.
- **Weight at the evidenced rung.** An interested party's assertion about its own product is a claim; a customer or a filing naming it is evidence.
- **A rung change is the event.** A second demonstration at the same rung is not a new finding unless its stated parameters change a row of the mechanism sheet (`sector-lens.md` §K.8).
- **Where a Tripwire is written in ladder terms, the rung is the test** — "production volume" is rung 5, and rung 2 does not fire it however prominent the announcement.
- **Check the technical content against the mechanism sheet.** A claim that contradicts the sheet is either **news** (the mechanism moved — the most valuable technical finding a run can return) or **an error** in the item, the sheet, or the thesis. Say which, with the source; never silently pick. A contradiction that reaches a ticker's **Edge premise** is an erratum candidate under `staleness-audit.md` §J.8, routed to a human.
- **Scope.** The ladder is for technology and product readiness. It does not apply to financial, regulatory or legal items — do not stretch it to fit them.

**This is forward-looking only**, on the same terms as §F.1: §F.4–§F.6 govern new entries; existing log entries are historical record and are never rewritten to match.
