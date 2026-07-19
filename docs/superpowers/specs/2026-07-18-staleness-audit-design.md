# Staleness audit — the re-underwrite entry point (Section J)

**Date:** 2026-07-18
**Branch:** `work/2026-07-18-staleness-audit-spec` (based on `main`)

## Context

Deep-dive reports are dated, immutable snapshots (`tickers/<T>/reports/<YYYY-MM-DD>.md`).
Everything else in a ticker's folder keeps moving: `news.md` accumulates dated,
Tripwire/Edge-assessed items, and `earnings-debrief.md` prepends a quarter at a time.
Nothing currently closes the loop back to the report, so the gap between the frozen
snapshot and accumulated knowledge widens silently until someone notices by hand.

Three failures from the 2026-07-18 session motivate this:

- **CIFR** — the report (dated 2026-07-15) used a `~$9.3B / 600 MW / two-lease` backlog
  that had been superseded at the **2026-05-05** Q1 print, two months *before* the report
  was researched. The earnings digest caught it and — correctly, per §I.4(d) — flagged
  rather than rewrote. It then sat flagged until a human explicitly asked for the fix.
- **IBIDY** — the digest found the "customers pre-funded the ¥500bn capex" leg appears in
  **no primary filing** (the ¥280bn/¥220bn figures are Ibiden's own plant capex). That is a
  load-bearing thesis correction that a cold re-run might not independently rediscover:
  the trade-press narrative is ubiquitous, and the filings are Japanese and 403-blocked.
- **AAOI** — already has two reports (07-14, 07-17), the second marked as superseding but
  not overwriting. So "re-run and supersede" is the established pattern, with no rule for
  *when* it is warranted.

## The core insight

**"Update the deep-dive" is three different operations**, and conflating them either
wastes four Opus sub-agents on a price refresh or papers over a broken thesis:

| Situation | Example | Correct treatment |
|---|---|---|
| **Error** — wrong at time of writing | CIFR `$9.3B` | Erratum patch in place |
| **Facts stale** — numbers moved, thesis structure holds | price/multiple, catalyst list | Seeded refresh → new dated report |
| **Thesis moved** — Edge falsified, Tripwire fired, business changed | IBIDY pre-funding leg | Full re-underwrite → new dated report |

The audit's job is **triage**, not rewriting: decide which of these applies, on evidence,
and route. Most audits should end in "clean" or "patch" — the expensive path is reserved
for the case that earns it.

## Decision: what "immutable" means (resolves a live inconsistency)

The framework says reports are "immutable once published." The 2026-07-18 CIFR erratum
patched one in place. Both cannot be right. **Resolution:**

- **Immutable as to judgment.** A verdict, Edge, Tripwire, probability, or bull/base/bear
  band is **never** restated to match how things turned out. This is what preserves the
  "what did I actually believe on date X" property that makes the corpus scoreable.
- **Patchable as to fact, with a visible scar.** A figure that was *wrong when written* may
  be corrected in place, and **must** carry a dated `> **ERRATUM (corrected YYYY-MM-DD)**`
  block naming what was wrong, what it should have been, and how it was caught.

A fact that was *right when written and has since changed* is **not** an erratum — that is
staleness, and it routes to refresh, not patch. The distinction is "wrong then" vs.
"overtaken since."

## Signals

### Deterministic (scriptable, no LLM)

Computed from the repo alone, except where noted:

| Signal | Source |
|---|---|
| Report age in days | `tickerlib.latest_report_date()` vs. today |
| Unincorporated news items | `news.md` entries dated **after** the report date |
| `[EDGE−]` accumulation | edge tags on entries after the report date |
| `[TRIPWIRE]` hits | tripwire tags on entries after the report date |
| Quarters reported since | `earnings-debrief.md` `## <period> — reported <date>` headings after the report date |
| Canonical-link drift | `news.md` `Canonical deep-dive:` link vs. glob-latest (a hygiene error, per CLAUDE.md's report-resolution rule) |
| Tripwire expiry | `[expires: YYYY-MM-DD]` annotations in the `## Tripwires` section vs. **today** (not the baseline — expiry is a property of the trigger's own window). Added 2026-07-19; grammar below. |
| Price/multiple drift — **deferred, not in v1** (see Open questions #2) | one Finnhub quote vs. the report's reference price. Listed only to record what was considered: adopting it would make the audit non-repo-local and break the recompute-on-demand property the provenance block depends on. |

### Judgment (bounded LLM pass, only when the deterministic tier flags)

- **Contradiction check** — does any logged item *contradict a specific claim* in the report,
  as opposed to merely postdating it? This is the CIFR `$9.3B` case and is the highest-value
  question the audit asks.
- **Edge status** — pressured vs. genuinely falsified.
- **Tripwire expiry — the "what replaces it" half.** *Detection* became deterministic on
  2026-07-19: every tripwire now carries an `[expires: YYYY-MM-DD]` annotation (the date its
  window closes or its premise lapses — CIFR's four are all keyed to pre-2027 events, and by
  mid-2027 most will have resolved, leaving the watch-list toothless while still looking
  populated; **a watch-list of resolved triggers is worse than an empty one**, because it
  reads as coverage). The deterministic tier compares those dates to today and flags. What
  it cannot do is decide **what happens next** — whether the expired trigger gets removed,
  re-dated because its window genuinely moved (a slipped commencement date), or replaced by
  a successor trigger from a re-underwrite. That is a judgment about the thesis, and per
  `standing-rules.md` §A it is an **explicit human decision**: the audit flags, never edits.

  **Grammar** (parsed by `tickerlib.tripwire_expiries`): inside the `## Tripwires` section,
  each numbered trigger `(n)` owns the `[expires: YYYY-MM-DD]` between its marker and the
  next. The date comes from the trigger's own text where it names a window (a print date, a
  guided ship window, a commencement target), else ~12 months from the report as a review
  horizon. A trigger without an annotation is surfaced as **untracked** (hygiene, not
  staleness) rather than guessed at. Expiry ≠ fired: expiry means the window closed
  *without* the trigger firing.

## Tag grammar — a blocking prerequisite

Scanning the real corpus (2026-07-18) shows the tag vocabulary has **drifted organically**,
because §F.1 mandates tagging but never defines a closed vocabulary or a status grammar.
The actual inventory across `tickers/*/news.md`:

| Count | Tag |
|---|---|
| 15 | `[EDGE+]` |
| 13 | `[EDGE−]` — **U+2212 true minus, not ASCII hyphen** |
| 3 | `[EDGE — live test, unresolved]` — em-dash, free-text status, neither + nor − |
| 1 | `[EDGE+, tangential]` — qualified positive |
| 6 | `[TRIPWIRE]` — bare |
| 1 | `[TRIPWIRE #1 — live, unresolved]` |
| 1 | `[TRIPWIRE #3 — early-warning, management-downplayed]` |
| 1 | `[TRIPWIRE #4 — reaffirmed, does not fire]` |
| 1 | `[TRIPWIRE #4 — touched, not sustained]` |

**This breaks naive counting, and the failure is expensive in exactly the direction the
triage design exists to prevent.** A scanner that routes `≥1 [TRIPWIRE` → RE-UNDERWRITE
would dispatch four Opus sub-agents on `[TRIPWIRE #4 — reaffirmed, does not fire]` — a tag
whose text says the opposite. Same for `touched, not sustained`. Likewise, `[EDGE — live
test, unresolved]` is neither positive nor negative and must not count toward the
`≥2 [EDGE−]` threshold.

The deterministic tier therefore **must** parse, not match:

1. **Normalize the sign** — accept U+2212 (`−`), ASCII `-`, and U+2013/2014 dashes.
2. **Split tag from status** — `[TRIPWIRE #n — <status>]` yields a number and a free-text status.
3. **Classify status polarity against the closed §F.1 vocabulary, defaulting to the cheaper
   route.** Only `fires` routes to RE-UNDERWRITE. `does not fire` (and the legacy spellings
   `not sustained` / `checked`) is **not-fired** and routes to nothing. `early-warning` (and
   legacy `live, unresolved`) is its own polarity and **does not escalate the route** — see
   "Decision: `early-warning` alerts, it does not escalate" below. An unrecognised status is
   a **hard lint failure at write time**, so it should not reach the audit; if one does,
   treat it as not-fired and print the raw tag. A false CLEAN is recoverable next audit; a
   false RE-UNDERWRITE burns four Opus agents immediately.

   *Note what is deliberately **not** on the fired list: a **bare `[TRIPWIRE]`** and
   `live, unresolved`. Earlier drafts of this spec routed both to RE-UNDERWRITE. §F.1 now
   makes `#n` plus a recognised status mandatory (so a bare tag is a lint failure, not an
   implied fire), and maps `live, unresolved` to early-warning — "unresolved" describes a
   trigger still being watched, which is the opposite of one that tripped.*

**Framework prerequisite — landed.** §F.1 now defines the closed vocabulary and status
grammar this parser assumes, `tickerlib.parse_assessment_tags` implements it, and
`lint_news_log.py` enforces it (#50, merged 2026-07-19). Kept as a separate change because it
touches the log format and every ticker file that follows it. **`parse_assessment_tags` is
the single classifier** — `audit_report.py` must call it rather than growing a second
parser, or the two drift and the audit silently re-acquires the bug this section exists to
prevent.

## Routing

Deterministic tier runs first and is cheap; it either clears the ticker or escalates.

| Verdict | Trigger | Treatment |
|---|---|---|
| **CLEAN** | No unincorporated items, no fired tags, <90d old. *An `early-warning` tag leaves the verdict CLEAN but forces a post — see below.* | None. Record the check. |
| **PATCH** | Contradiction check finds a claim that was wrong *when written* | Erratum in place per the immutability rule. No re-run. |
| **REFRESH** | Facts stale (≥2 quarters reported, or ≥90d with unincorporated catalysts) but Edge/Tripwires intact | **Seeded** re-run → new dated report, dispatching **the agents the audit's work order names** — see "REFRESH dispatches a work order" below. Not a fixed count. |
| **ESCALATE** *(deterministic tier only — never a final answer)* | ≥2 `[EDGE−]` accumulated · a tripwire's `[expires:]` date has passed unfired | Judgment tier reads the entries and decides: pressured vs. falsified for the Edge; remove / re-date / replace for an expired trigger. A count is a proxy for pressure, never evidence of change — the live corpus proves it (CIFR's two `[EDGE−]` entries both say the Edge's core was *corroborated*). |
| **RE-UNDERWRITE** | A tripwire **affirmatively fired** (per the tag-grammar polarity rule — *not* merely surfaced; the deterministic tier may relay this because a prior run already made the assessment) · judgment tier concludes the Edge is falsified | **Full** `/deep-dive` re-run, all four sub-agents. |

`≥2 [EDGE−]` is not invented — `latest-updates-workflow.md` §F already states that an
accumulation of EDGE− means the differentiated thesis is failing even with no Tripwire
fired. That rule exists and is currently unused as a trigger; this wires it up.

### Decision: `early-warning` alerts, it does not escalate

An `early-warning` tag means the pre-committed trigger is being **approached and has not
tripped**. Earlier drafts routed it to "REFRESH at most." That is a category error, and
`standing-rules.md` §A says why:

> their entire value is that they were fixed *in advance*, so a threshold cannot be quietly
> softened once it is crossed **or approached**.

A REFRESH produces a new dated report, which re-derives §18 and then prompts to promote the
new Edge and Tripwires into `news.md`. So routing `early-warning` → REFRESH **manufactures a
threshold-rewrite opportunity at exactly the moment the threshold is being approached** —
the specific failure the pre-commitment exists to prevent. It also acts on a trigger that the
pre-commitment explicitly says is not yet the trigger, which is the same softening from the
other direction.

**Resolution — separate the verdict from the notification.** This is the same split the
cadence section already draws between how often the audit *runs* and how often it *speaks*:

- **Verdict: unchanged.** `early-warning` never escalates the route on its own. It carries no
  weight toward RE-UNDERWRITE and does not by itself produce a REFRESH.
- **Notification: forced.** An `early-warning` **breaks the silent-when-CLEAN rule** and
  posts — naming the tripwire `#n`, its stated distance from the threshold, and the
  pre-committed action that *would* become due if it trips. Approaching a trigger is high
  signal for a human even when it is correctly no signal for the router.

The three statuses therefore still each route differently — `fires` → RE-UNDERWRITE,
`early-warning` → CLEAN-but-loud, `does not fire` → CLEAN and silent — which is what earns
tripwires three states under §F.1's "does the value change what happens?" test.

Where other signals independently produce a REFRESH or RE-UNDERWRITE, any live
`early-warning` tags ride along in that message as supporting evidence. **They colour a
verdict; they never cause one.**

### REFRESH dispatches a work order, not a fixed agent count

An earlier draft specified REFRESH as "two sub-agents (filing + sector)." That number was
arbitrary, and it contradicted `standing-rules.md` §A ("Always dispatch four parallel
sub-agents… All four are mandatory") with no stated exception — so the cheap path had no
mechanism and the two documents disagreed.

**A partial re-run is only defensible if the audit says *what* is stale and dispatches
exactly the agents that own it.** The audit already computes dated, specific evidence in
order to justify its verdict; that same evidence *is* the work order. Requiring the audit to
emit it costs nothing extra and turns "spend less" from a hopeful default into a targeted
repair with a stated scope.

**Routing evidence → work-stream.** §F.1 log entries already carry a categorising framework
tag, which maps onto the four hard-coded agent templates:

| Evidence in the audit's finding | Agent dispatched |
|---|---|
| `[Financials/…]`, `[Management/Insider]`, capital stack, a quarter reported since the report | **filing** (§H) |
| `[Risks/Concentration]`, anchor tenant / customer / financing-partner news | **counterparty** (§H) |
| `[Moat/Competition]`, `[Tech moat]` | **competitive-landscape** (§G) |
| `[Sentiment/…]`, `[Catalyst/Re-rate driver]`, secular-demand items | **sector** (§H) |

The judgment tier does this mapping, not the deterministic tier: the framework-tag vocabulary
is **open and has drifted** (`Catalyst/Re-rate driver` vs. `Catalysts/Re-rate drivers` vs.
`Sentiment/Re-rate drivers` all appear in the corpus today), so it cannot be matched
reliably by a script. That is the same failure the assessment tags had before #50, one layer
over. Closing that vocabulary would let the deterministic tier route directly and is a
worthwhile follow-up — **but it is not a blocker**, because REFRESH is an escalated verdict
and the judgment pass is already running by the time a work order is needed.

**The work order names, per stale area:** the work-stream, the specific claim or section to
re-verify, and the dated evidence that flagged it. The agent set is the union of the
work-streams named — one, two, three, or four. **If it comes out as all four, it is not a
REFRESH**; run it as a full re-underwrite and say so.

#### The safeguard this requires: section-level provenance

A partial re-run produces a report with **today's date on sections that were not
re-researched.** Left unmarked, that is precisely the failure this spec already names as
worse than obvious staleness — *"fresh numbers under conclusions reasoned from superseded
ones… it reads as current while being wrong, and nothing flags it."* A narrower agent set
therefore **buys a disclosure obligation, not just a saving**:

- **Every section states its provenance** — re-researched this run, or carried forward
  unchanged from `<prior-report-date>`.
- **The provenance block lists the work order and, explicitly, what was *not* re-researched.**
  The omissions are the part a future reader cannot reconstruct.

#### The backstop: absence of logged news decays as evidence

The work order can only name what the audit can *see*, and what it can see comes from
`news.md` — which comes from prior what's-new runs. **A section that went stale with no
logged news is invisible to it.** Guarding against exactly that unknown-unknown is why the
four-agent mandate exists.

So "no logged news in area X" is a proxy for "area X is still current," and that proxy decays
with time. **Beyond a staleness horizon — proposed: the prior report older than ~180 days —
run all four regardless of how narrow the work order is.** This number is a judgment call to
tune with use, not a derived one; it is stated as arbitrary rather than dressed up.

## Asymmetric context — the anchoring rule for REFRESH and RE-UNDERWRITE

The obvious idea ("re-run with `news.md` as context") has a real failure mode: hand the
research agents the existing Edge and they will tend to confirm it, which defeats a
variant view whose whole value is falsifiability. `CLAUDE.md` already warns against using a
prior report as the quality precedent. But feeding *nothing* forward risks losing
expensively-won corrections (the IBIDY pre-funding finding).

**Resolution — split by kind, not by file:**

- **Feed forward** (fights anchoring): corrections and errata, disconfirming findings, and
  "what the filings actually say vs. what trade press claims." These are the costly-to-
  rediscover facts.
- **Withhold** (causes anchoring): the Edge, the numbered Tripwires, verdicts, the
  bull/base/bear bands. The orchestrator re-derives these independently.
- **Then diff.** Compare the freshly-derived Edge against the prior one as an explicit step.
  **That diff is itself a finding** and belongs in the new report's closing block.

So `news.md` log entries and `earnings-debrief` figures go into sub-agent prompts; the Edge
blockquote does not.

## When and how the audit runs

### Cadence — two triggers, not one

**Separate how often the audit *runs* from how often it *speaks*.** These are different
questions and conflating them produces bad cadence reasoning. The audit is cheap,
deterministic and repo-local, so running it often is fine — verdicts stay fresh. Noise is
controlled entirely in the reporting layer (exception-only, state-change, re-nag
suppression), not by throttling the trigger.

**This is safe only because the expensive tier is escalation-gated.** The judgment (LLM)
pass runs *solely* when the deterministic tier flags. If that gating is ever weakened,
frequent running stops being cheap and the cadence argument has to be reopened.

Measured frequency (2026-07-18, trailing 30 days): `news.md` changed **3–7 times per
ticker** — not daily, even though the dispatcher runs every weekday. Three things hold it
down: the dispatcher's keyword gate, its 48h per-ticker rate cap, and §F's rule forbidding
"no news" placeholder entries, so `news.md` only changes when something material was found.

The two triggers cover **different populations**, which is why both are needed:

1. **Event-driven, per ticker.** The audit's inputs change at exactly one moment — when a
   `whats-new` or `earnings-digest` run commits a new log entry or quarter. Trigger on the
   push rather than coupling the workflows:

   ```yaml
   on:
     push:
       paths: ['tickers/**/news.md', 'tickers/**/earnings-debrief.md']
   ```

   Both heavy workflows squash-merge to `main`, so this fires automatically and audits only
   the affected ticker, the moment a `[TRIPWIRE]` or `[EDGE−]` is logged. **No self-trigger
   loop**: the audit writes state to the Actions cache and never commits.

2. **Weekly sweep** (`schedule`, Monday morning) — covers the **quiet tickers the push
   trigger structurally cannot reach.** A ticker with no material news for three months
   never fires a push, and that is *exactly* the ticker whose report is aging into
   staleness unnoticed. The sweep is not a throttled version of the push trigger; it covers
   a disjoint population (time-driven drift on inactive names vs. event-driven drift on
   active ones). Monday so the week opens with the decision.

Plus `workflow_dispatch` for manual runs, matching the dispatcher's `dry_run` convention.

**Own workflow (`audit.yml`), not a step inside `dispatcher.yml`** — because the audit needs a
**`push` trigger the dispatcher does not have**, and a step inside a cron-only workflow
cannot express that. A separate workflow also keeps the audit's cache namespace, permissions
(notably *no* `actions: write`) and failure modes independent of the dispatcher's.

### Reporting — by exception

Reuses the dispatcher's plumbing: Actions-cache state (`.audit-state`, its own key
namespace, mirroring the deliberate choice to keep gate state out of `main`) and a Discord
poster shaped like `notify_discord_dispatch.py`.

- **Silent when CLEAN.** A weekly "all fine" post is how a channel becomes ignorable.
  **One exception: a CLEAN verdict carrying an `early-warning` tag still posts** (see the
  early-warning decision above) — the verdict and the notification are separate outputs, so
  `audit_report.py` emits a `notify` flag independent of the verdict rather than the poster
  inferring "post if not CLEAN."
- **Post on non-CLEAN or on state change**, with re-nag suppression: do not repeat the same
  verdict for ~30 days unless it *escalates*. Cache eviction causes at worst one duplicate
  nudge — acceptable.
- **Always write the artifact** even when silent, so a human can confirm the audit ran.
- **Routing:** a per-ticker verdict goes to that ticker's own Discord channel, alongside the
  news that caused it; the weekly roll-up goes to the dispatcher channel.
- **Content must be actionable**: the verdict, the *specific evidence* that produced it
  (e.g. "2 `[EDGE−]` since 2026-07-15; Q2 reported 2026-08-06 absent from report"), and the
  exact command to run.

### Does REFRESH auto-run? No — and the reason is §I.4(d), not cost

**Every route that regenerates a report is human-prompted, REFRESH included.** The
governing rule already exists in `earnings-digest.md` §I.4(d):

> **Never silently rewrite the Edge or the Tripwires.** They are pre-committed in the
> ticker's news.md and are binding… leave the re-underwrite as an explicit decision for the
> reader to make deliberately.

A REFRESH produces a **new dated report**, which re-derives §18 — the Edge and the numbered
Tripwires — and `news.md`'s `Canonical deep-dive:` link then resolves to it. An automated
REFRESH would therefore **silently replace the reader's pre-committed exit triggers**, which
is exactly what §I.4(d) forbids; routing it through a workflow instead of a digest does not
make it a different act. The failure mode is concrete: you could wake up to different
Tripwires than you committed to, which destroys the property that makes them worth having.

**The tempting middle option — "auto-update facts, human-gate the thesis" — does not
survive the evidence.** CIFR's stale `$9.3B` sat *inside the Edge's central sentence*
("the entire sell-side thesis rests on the same fact — the ~$9.3B backlog"). A facts-only
auto-refresh would have either left the Edge quoting a superseded number or silently edited
it. Facts and thesis are not cleanly separable, and **a report with fresh numbers under
conclusions reasoned from superseded ones is worse than an obviously stale one** — it reads
as current while being wrong, and nothing flags it.

**What may auto-run:** canonical-link drift only (`news.md` pointing at a non-latest
report). Pure hygiene, zero judgment content, already deterministic — this may open a PR
unattended. Nothing else.

**The correct lever is cheapness of the decision, not removal of it.** The audit should
arrive carrying the verdict, the specific evidence, and the exact command, so the human is
approving or declining rather than investigating from scratch.

### Refresh provenance — every audit-triggered report states why it exists

A REFRESH or RE-UNDERWRITE produces a **new dated report** (decided 2026-07-18). That new
file must carry a **dated provenance block**, in the same position and spirit as the
erratum block, naming *specifically* why it superseded its predecessor.

**Both, always — this is additive, not a relocation.** The Discord message still fires
exactly as specified under "Reporting — by exception"; the provenance block is a *second*
record, not a replacement for the first. They serve different jobs and neither substitutes
for the other:

| | Discord message | Provenance block in the report |
|---|---|---|
| **Job** | Timely nudge — *act on this now* | Durable provenance — *why this report exists* |
| **Timing** | At audit time, before any re-run | Written into the new report, after the re-run |
| **Lifetime** | Scrolls away | Permanent, versioned with the corpus |
| **Audience** | You, this week | Any reader, any time later |

A reader opening `reports/2026-11-01.md` months later must be able to see why it replaced
`reports/2026-07-15.md` without archaeology — and equally, an audit that finds something
must reach you at the time even if no re-run is ever dispatched. **A REFRESH that produced
no Discord message, or a Discord message that produced no provenance block, is a bug in
either direction.** The corpus already half-does this — AAOI's
07-17 report says it *"supersedes — but does not overwrite — the immutable 2026-07-14
snapshot"* — but records the supersession without the **reasons**. This formalizes the
missing half.

Required contents:

- **Which audit triggered it**, dated, and the verdict (REFRESH / RE-UNDERWRITE).
- **The specific signals that fired, with their evidence** — dated and citable, e.g.
  *"2 `[EDGE−]` logged 2026-08-02 and 2026-09-14; Q2 FY2027 reported 2026-08-06 absent from
  the prior report."*
- **The prior report it supersedes**, linked.
- **The work order that was run, and what it excluded** — which agents were dispatched and,
  explicitly, **which sections were carried forward rather than re-researched** (see
  "section-level provenance"). On a full four-agent re-underwrite this is one line saying so;
  on a partial refresh it is the load-bearing disclosure, because the omissions are what a
  future reader cannot reconstruct from the file.
- **The Edge diff.** Per the asymmetric-context rule the orchestrator re-derives the Edge
  independently and compares it to the prior one — **this block is where that diff lands.**
  If the Edge came out materially unchanged, *say so explicitly*: a thesis surviving
  independent re-derivation is a real finding, not an absence of one. If it changed, that is
  the single most important sentence in the new report.

**The failure mode to prevent:** *"Routine refresh; updated for latest data."* That tells a
future reader nothing about whether the refresh was warranted, what moved, or what might
have been missed — and it makes the refresh chain unauditable exactly when someone is trying
to reconstruct how a view evolved. **Reasons must be specific and evidence-linked, or the
block has failed its purpose.**

#### Where the block's contents come from — re-derive, don't persist

The audit's own outputs are both **ephemeral by design**: the Discord message scrolls away,
and the `.audit-state` cache is evictable and deliberately never committed. So at the moment
the human runs `/deep-dive` — which may be days or weeks after the audit flagged the ticker
— there is **no stored audit record for the provenance block to quote**. That is not a hole
to fill with a new store; it is a signal that the block should be **recomputed, not
recalled**.

**Rule: an audit-triggered deep-dive re-runs the audit itself, live, immediately before
writing the new report, and builds the provenance block from that run.** Concretely, the
deep-dive skill's audit-triggered path invokes `scripts/audit_report.py --ticker <T> --json`
and renders the block from its output.

This works because **every deterministic signal is a pure function of current repo state** —
unincorporated items, `[EDGE−]` accumulation, tripwire tags, and quarters-reported are all
recomputed from `news.md` and `earnings-debrief.md` against the (still unchanged) prior
report date. Re-running them at refresh time yields the same verdict, or a **more current**
one if something else landed in the interval — which is strictly better than quoting a
verdict that has since gone stale. The judgment-tier contradiction check likewise does not
need persisting: the refresh's own sub-agent research covers that ground anyway, and the
Edge diff is by definition produced *during* the re-run, not before it.

**Why not a committed audit log** (e.g. an append-only `tickers/<T>/audit-log.md`): it would
buy a permanent record of runs the spec has already decided not to keep (**silent when
CLEAN**), and it would cost the two properties that make the audit cheap enough to run on
every push — it must stay **stateless and idempotent**, and it must **never commit**, which
is what closes the self-trigger loop against its own `push` trigger on `tickers/**`. A store
whose only consumer can recompute its contents on demand is not worth those costs. Revisit
only if a signal is ever added that is **not** recomputable from the repo (a point-in-time
price quote being the obvious candidate — and note this is a second, independent reason
price drift was ruled out of v1).

**Consequence for reporting:** the Discord message and the provenance block are not just
different in job and lifetime (table above) — they are **separately derived**, from two
audit runs at two different times. If they disagree, the *report block is authoritative*
(it is the more recent computation) and the divergence is itself worth a sentence in the
block: something moved between the flag and the refresh.

**Ordering is load-bearing — compute before you write.** Every deterministic signal is
defined relative to `latest_report_date()`, which is `max()` over the dated files on disk.
**The moment the new report is written, that baseline becomes today** — so "items dated
after the report date" collapses to the empty set, quarters-reported-since goes to zero, and
the audit returns **CLEAN with no evidence**. The provenance block would then state, with
full confidence, that nothing was stale: the exact inversion of the truth, in the one field
whose entire job is explaining why the report was regenerated, and invisible in the finished
file because the block still renders.

Two mitigations, **both** required:

1. The skill runs the audit **before** the report is written (i.e. before deep-dive Step 3).
2. `audit_report.py` takes **`--baseline <YYYY-MM-DD>`** to pin the comparison date
   explicitly, so a correct result does not depend on invocation order at all.

(2) is the real fix; (1) alone is a convention, and a convention that inverts the output when
broken — silently, in the direction of "all clear" — is not a safe thing to rely on. The
refresh path passes the **superseded** report's date as the baseline, which is also the
semantically correct question: *what has happened since the report I am replacing?*

**Where the block is physically written:** the Edge diff is only available *after* the
re-derivation, so the block is composed during deep-dive Step 4b and written into the report
file Step 3 already created. That is not a violation of report immutability — **immutability
attaches at commit (Step 5), not at first write.** A report amended within the run that
created it has never been published.

### Human-in-the-loop is currently structural, not just policy

**There is no `deep-dive.yml` workflow.** `whats-new` and `earnings-digest` each have one;
a deep-dive re-run is session-only. So the audit *cannot* dispatch a re-run the way the
dispatcher fires the other two — it can only recommend, and a human runs `/deep-dive`.

This matches the intent, and it is worth recording that the guarantee is **load-bearing**:
if a `deep-dive.yml` is ever added, the structural block disappears and the audit will need
an explicit **"recommend only, never dispatch"** rule written into it, plus the removal of
`actions: write` from its permissions.

## Deliverables

1. **`framework/staleness-audit.md`** — Section J. The method: signals, routing table, the
   immutability rule, the asymmetric-context rule. Single source of truth; other files
   reference it and do not restate it.
2. **`scripts/audit_report.py`** — the deterministic tier. Reuses `tickerlib`
   (`latest_report_date`, `ticker_dirs`, `front_matter`); no new parsers. Emits a per-ticker
   verdict table; `--json` for machine use; exits non-zero only on canonical-link drift
   (a genuine hygiene error), never on staleness (which is a decision, not a failure).
   **Must be stateless and idempotent** — every signal recomputed from repo state on each
   invocation, no writes to the repo. This is what lets the deep-dive skill re-run it at
   refresh time to build the provenance block (see "Where the block's contents come from"),
   and what keeps its own `push` trigger loop-free. `--ticker <T>` scopes it to one name;
   **`--baseline <YYYY-MM-DD>` pins the comparison date** instead of defaulting to
   `latest_report_date()`, so the refresh path gets a correct answer regardless of whether
   the new report has already been written (see "Ordering is load-bearing").
3. **`.claude/skills/audit/SKILL.md`** — launcher. Runs the deterministic tier, then the
   bounded judgment pass only for escalated tickers, then reports the routing decision.
   **On a REFRESH verdict it must emit the work order** — the work-streams to dispatch, the
   specific claim/section each must re-verify, and the dated evidence behind each — since the
   judgment tier is the only layer that can map the open framework-tag vocabulary onto the
   four agent templates. A REFRESH verdict without a work order is incomplete output: it
   licenses a narrower run without stating its scope, which is the one thing
   `standing-rules.md` §A's exception forbids. **Does not itself re-run a deep-dive** — it
   recommends; the human dispatches.
4. **`.github/workflows/audit.yml`** — weekly sweep + push-triggered per-ticker re-audit +
   `workflow_dispatch`. Actions-cache state, exception-only Discord reporting.
   **No `actions: write`** — it has nothing to dispatch, and withholding the permission
   makes the recommend-only property enforceable rather than merely intended.
5. **`scripts/notify_discord_audit.py`** *(or a `--kind audit` mode on the existing ticker
   poster)* — decide at implementation time; the existing poster already takes `--kind`, so
   extending it is likely cheaper than a third script. Note `notify_discord_dispatch.py` and
   `notify_discord_ticker.py` already coexist, so a third would be the point at which the
   posters want consolidating (cf. the 3a code-dedup work).
6. **Provenance block wiring** — the block is conditional, and **the condition is repo state,
   not the run's context.** Glob `tickers/<T>/reports/*.md`: if a dated report other than this
   run's already exists, this run supersedes it and the block is **required**.

   **Do not condition it on the run being "audit-triggered" — that is not detectable.** The
   human types `/deep-dive <T>` with no flag and possibly no memory of the Discord nudge from
   three weeks ago; the session cannot tell an audit-prompted refresh from a spontaneous one.
   Gating on it would silently skip the block on every hand-initiated re-run — **the identical
   failure mode `standing-rules.md` §A already closes for Edge/Tripwires** ("detect a re-run
   from repo state, not from how the request was phrased"), reappearing one artifact over. The
   audit verdict is the block's **content**, not its trigger; a refresh nobody audited still
   supersedes a predecessor and still owes the reader an explanation, which the live
   `audit_report.py --baseline <superseded-date> --ticker <T> --json` call supplies either way.

   An initial deep-dive has no predecessor and carries no block, so this does not belong in
   `report-template.md` as a standing section: **Section J defines its shape** (single source
   of truth), the **deep-dive skill** gains the step, and `report-template.md` gets a one-line
   conditional pointer, not a copy of the format.
7. **Tests** — `scripts/tests/test_audit_report.py`, following existing conventions.
   Must cover the tag-grammar polarity cases explicitly: `[TRIPWIRE #4 — reaffirmed, does
   not fire]` and `[TRIPWIRE #4 — touched, not sustained]` must **not** route to
   RE-UNDERWRITE, and U+2212 vs ASCII minus must both parse. **Plus idempotence:** two
   invocations against unchanged repo state must return an identical verdict and evidence
   set — the provenance block's correctness rests on that property, so it is a test, not an
   assumption. **Plus the ordering inversion:** with a newer dated report present on disk,
   `--baseline <older-date>` must still return the pre-existing signals, where the default
   baseline would return CLEAN. That is the regression test for the failure mode described
   under "Ordering is load-bearing" — the one that fails silently toward "all clear."
   **Plus the early-warning split:** an `early-warning` tag alone must leave the verdict
   CLEAN *and* set `notify` — assert **both** halves, since a test checking only the verdict
   would pass while the alert was silently dropped.

## Open questions

1. ~~**Does the dispatcher call this?**~~ **Resolved 2026-07-18** — see "When and how the
   audit runs" above. Own `audit.yml` (weekly sweep + push-triggered per-ticker), reporting
   by exception to Discord. The audit **informs**; the human decides and dispatches the
   re-run. Not folded into `dispatcher.yml` because the audit needs a `push` trigger the
   cron-only dispatcher cannot express.
2. ~~**Price drift threshold.**~~ **Resolved 2026-07-18 — out of v1.** No Finnhub quote, no
   price/multiple signal. The audit stays **fully repo-local and deterministic**, which is
   what keeps it cheap enough to run on every push (see the escalation-gating caveat above)
   and keeps it free of an external API dependency and its failure modes. The quarter-count
   and tag-accumulation signals are sufficient to prove the routing. Revisit only if v1
   demonstrably misses staleness that a price signal would have caught.
3. ~~**Does REFRESH really need a new dated file?**~~ **Resolved 2026-07-18 — yes.** REFRESH
   produces a new dated report, not a delta doc, so the current view always lives in exactly
   one file (per the "one home each" rule) and the prior snapshot stays immutable. Each such
   report carries the provenance block specified above.

4. ~~**Does `early-warning` justify a REFRESH?**~~ **Resolved 2026-07-19 — no.** It alerts
   without escalating the route; see "Decision: `early-warning` alerts, it does not escalate."
   Routing it to REFRESH would create a threshold-rewrite opportunity precisely when the
   threshold is being approached, which `standing-rules.md` §A forbids in as many words.

*(No open questions remain, and the §F.1 tag-grammar prerequisite has landed (#50). The spec
is complete as a design; nothing under Deliverables is implemented yet.)*

## Out of scope

- Automating any re-run — **REFRESH and RE-UNDERWRITE alike**. The audit **recommends**; a
  human dispatches `/deep-dive`. Governed by §I.4(d), not by cost; see the REFRESH section
  above. The sole exception is canonical-link drift, which may auto-PR.
- Retroactively auditing the existing corpus (a one-time backfill, separate).
- Any change to `/whats-new` or `/earnings-digest`.
- Rewriting published judgments — explicitly forbidden by the immutability rule above.

## Net effect

A dated report stops going stale silently. Each ticker gets a cheap, repeatable check that
ends in an explicit, evidence-backed verdict — and the expensive four-agent re-run is spent
only on theses that actually moved, rather than on price refreshes or on nothing at all
until a human happens to notice.
