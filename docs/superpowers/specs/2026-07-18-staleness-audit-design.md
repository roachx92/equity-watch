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
4. **Tests** — `scripts/tests/test_audit_report.py`, following existing conventions.

## Open questions

1. **Does the dispatcher call this?** The cron dispatcher already enumerates tickers. A
   weekly `audit_report.py --json` run could post a staleness digest to Discord. Deferred —
   spec the manual path first, wire automation once the thresholds prove themselves.
2. **Price drift threshold.** Needs a Finnhub quote and a judgment call on what magnitude
   makes §14 stale. Proposal: leave price drift out of v1; the quarter-count and
   tag-accumulation signals are repo-local and sufficient to prove the routing.
3. **Does REFRESH really need a new dated file?** It produces a new dated report under this
   spec. The alternative (delta doc) fragments the current view across N files, which the
   "one home each" rule argues against.

## Out of scope

- Automating the re-run itself. The audit **recommends**; a human dispatches `/deep-dive`.
- Retroactively auditing the existing corpus (a one-time backfill, separate).
- Any change to `/whats-new` or `/earnings-digest`.
- Rewriting published judgments — explicitly forbidden by the immutability rule above.

## Net effect

A dated report stops going stale silently. Each ticker gets a cheap, repeatable check that
ends in an explicit, evidence-backed verdict — and the expensive four-agent re-run is spent
only on theses that actually moved, rather than on price refreshes or on nothing at all
until a human happens to notice.
