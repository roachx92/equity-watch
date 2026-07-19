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
| Price/multiple drift *(optional)* | one Finnhub quote vs. the report's reference price — the dispatcher already holds this dependency |

### Judgment (bounded LLM pass, only when the deterministic tier flags)

- **Contradiction check** — does any logged item *contradict a specific claim* in the report,
  as opposed to merely postdating it? This is the CIFR `$9.3B` case and is the highest-value
  question the audit asks.
- **Edge status** — pressured vs. genuinely falsified.
- **Tripwire expiry** — *are the triggers still live?* CIFR's four Tripwires are all keyed to
  pre-2027 events; by mid-2027 most will have resolved, leaving the watch-list toothless
  while still looking populated. **A watch-list of resolved triggers is worse than an empty
  one**, because it reads as coverage. This check has no deterministic proxy and is the
  reason the audit cannot be fully scripted.

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
3. **Classify status polarity, defaulting to "not fired."** Only an *affirmative* fire
   (bare `[TRIPWIRE]`, or a status like `live, unresolved` / `fires`) routes to
   RE-UNDERWRITE. Anything matching `does not fire` · `not sustained` · `checked` ·
   `reaffirmed` · `early-warning` counts as **surfaced-but-not-fired** — it raises the
   verdict to REFRESH at most, never RE-UNDERWRITE. **Default to the cheaper route when the
   status is unrecognized**, and print the unparsed tag so a human sees it. A false CLEAN is
   recoverable next audit; a false RE-UNDERWRITE burns four Opus agents immediately.

**Framework follow-up (separate PR):** §F.1 should define the closed vocabulary and status
grammar this parser assumes, and `lint_news_log.py` should enforce it — otherwise the
grammar keeps drifting and the parser rots. Spec'd here because the audit depends on it;
not bundled, because it touches the log format and every ticker file that follows it.

## Routing

Deterministic tier runs first and is cheap; it either clears the ticker or escalates.

| Verdict | Trigger | Treatment |
|---|---|---|
| **CLEAN** | No unincorporated items, no tags, <90d old | None. Record the check. |
| **PATCH** | Contradiction check finds a claim that was wrong *when written* | Erratum in place per the immutability rule. No re-run. |
| **REFRESH** | Facts stale (≥2 quarters reported, or material price/multiple drift, or ≥90d with unincorporated catalysts) but Edge/Tripwires intact | **Seeded** re-run → new dated report. Two sub-agents (filing + sector) rather than four; structural sections (business model, value-chain position) verified rather than re-derived. |
| **RE-UNDERWRITE** | A tripwire **affirmatively fired** (per the tag-grammar polarity rule — *not* merely surfaced) · ≥2 `[EDGE−]` accumulated · Edge assessed as falsified · Tripwires expired by resolution | **Full** `/deep-dive` re-run, all four sub-agents. |

`≥2 [EDGE−]` is not invented — `latest-updates-workflow.md` §F already states that an
accumulation of EDGE− means the differentiated thesis is failing even with no Tripwire
fired. That rule exists and is currently unused as a trigger; this wires it up.

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
3. **`.claude/skills/audit/SKILL.md`** — launcher. Runs the deterministic tier, then the
   bounded judgment pass only for escalated tickers, then reports the routing decision.
   **Does not itself re-run a deep-dive** — it recommends; the human dispatches.
4. **`.github/workflows/audit.yml`** — weekly sweep + push-triggered per-ticker re-audit +
   `workflow_dispatch`. Actions-cache state, exception-only Discord reporting.
   **No `actions: write`** — it has nothing to dispatch, and withholding the permission
   makes the recommend-only property enforceable rather than merely intended.
5. **`scripts/notify_discord_audit.py`** *(or a `--kind audit` mode on the existing ticker
   poster)* — decide at implementation time; the existing poster already takes `--kind`, so
   extending it is likely cheaper than a third script. Note `notify_discord_dispatch.py` and
   `notify_discord_ticker.py` already coexist, so a third would be the point at which the
   posters want consolidating (cf. the 3a code-dedup work).
6. **Provenance block wiring** — the block is *conditional*: an initial deep-dive has no
   predecessor and carries none, so it does not belong in `report-template.md` as a standing
   section. Instead: **Section J defines its shape** (single source of truth), and the
   **deep-dive skill** gains a step — when a run is audit-triggered, emit the block and
   perform the Edge diff against the superseded report. `report-template.md` gets a one-line
   conditional pointer, not a copy of the format.
7. **Tests** — `scripts/tests/test_audit_report.py`, following existing conventions.
   Must cover the tag-grammar polarity cases explicitly: `[TRIPWIRE #4 — reaffirmed, does
   not fire]` and `[TRIPWIRE #4 — touched, not sustained]` must **not** route to
   RE-UNDERWRITE, and U+2212 vs ASCII minus must both parse.

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

*(No open questions remain. The remaining prerequisite is the §F.1 tag-grammar
follow-up, tracked in "Tag grammar" above as a separate PR.)*

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
