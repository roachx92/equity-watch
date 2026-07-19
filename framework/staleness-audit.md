# Staleness audit — keeping dated reports honest

*Section J of the equity research framework. The single source of truth for the audit method: its signals, its routing, and the rules governing what it may and may not do. Other files reference this one — they do not restate it.*

*Design rationale and the decisions behind each rule: [`docs/superpowers/specs/2026-07-18-staleness-audit-design.md`](../docs/superpowers/specs/2026-07-18-staleness-audit-design.md).*

---

## J.0 — The problem, and the one thing the audit is for

Deep-dive reports are dated, immutable snapshots. Everything else in a ticker's folder keeps moving: `news.md` accumulates dated, assessed items, `earnings-debrief.md` prepends a quarter at a time. Nothing closes the loop back to the report, so the gap between the frozen snapshot and accumulated knowledge widens **silently** until a human happens to notice.

**"Update the deep-dive" is three different operations**, and conflating them either wastes four Opus sub-agents on a price refresh or papers over a broken thesis:

| Situation | Example | Correct treatment |
|---|---|---|
| **Error** — wrong at time of writing | CIFR's stale `~$9.3B` backlog | Erratum patch in place |
| **Facts stale** — numbers moved, thesis structure holds | a quarter reported since | Seeded refresh → new dated report |
| **Thesis moved** — Edge falsified, tripwire fired | IBIDY's unsupported pre-funding leg | Full re-underwrite → new dated report |

**The audit's job is triage, not rewriting.** Decide which applies, on dated evidence, and route. Most audits should end CLEAN. The expensive path is reserved for the case that earns it.

## J.1 — What the audit may never do

- [ ] **Never write to a ticker's `news.md`.** Not the Edge, not the tripwires, not the log. The pre-committed Edge and Tripwires are written **only by explicit human decision** (`standing-rules.md` §A) — that invariant binds the audit exactly as it binds every other workflow. The audit **flags**; a human decides.
- [ ] **Never dispatch a re-run.** It recommends; a human runs `/deep-dive`. This is currently also *structural* — there is no `deep-dive.yml` — and `audit.yml` deliberately withholds `actions: write` so the property is enforced rather than merely intended. **If a `deep-dive.yml` is ever added, this rule is what stops the audit firing it.**
- [ ] **Never commit.** The audit's own outputs are ephemeral by design (see §J.6). Committing would also create a self-trigger loop against its own `push` trigger on `tickers/**`.
- [ ] **The one exception:** canonical-link drift may open a PR unattended. Pure hygiene, zero judgment content.

## J.2 — Two tiers, and the boundary between them

**The deterministic tier clears or escalates. It does not conclude.** This boundary is load-bearing and is the reason the audit is cheap enough to run on every push: the expensive judgment pass is *escalation-gated*.

### Deterministic tier — `scripts/audit_report.py`

Repo-local, stdlib-only, no network, no LLM. **Stateless and idempotent**: every signal recomputed from repo state on each invocation, nothing written back. That property is what lets the deep-dive re-run path call it live to build a provenance block (§J.7).

| Signal | Source |
|---|---|
| Report age | `latest_report_date()` (or `--baseline`) vs. today |
| Unincorporated items | `news.md` log entries dated **after** the baseline |
| `[EDGE−]` / `[EDGE+]` accumulation | assessment tags on those entries |
| Tripwire hits by polarity | `fires` / `early-warning` / `does not fire`, with `#n` |
| Quarters reported since | `earnings-debrief.md` headings after the baseline |
| **Tripwire expiry** | `| # | Expires |` table vs. **today** (§J.4) |
| Canonical-link drift | `news.md` link vs. glob-latest — a hygiene error, per CLAUDE.md's report-resolution rule |

**Tag polarity comes from `tickerlib.parse_assessment_tags`** — the same classifier `lint_news_log.py` uses. A second parser would drift and silently re-acquire the false-positive it exists to prevent: `[TRIPWIRE #4 — reaffirmed, does not fire]` must never read as fired.

### Judgment tier — bounded LLM pass, only on escalation

- **Contradiction check** — does a logged item *contradict a specific claim* in the report, as opposed to merely postdating it? The highest-value question the audit asks, and the only route to a PATCH.
- **Edge status** — pressured, or genuinely falsified?
- **Expired tripwires** — remove, re-date, or replace? (§J.4)

## J.3 — Routing

| Verdict | Trigger | Treatment |
|---|---|---|
| **CLEAN** | No unincorporated items, nothing fired or expired, report recent | None. Record the check. *(An `early-warning` leaves the verdict CLEAN but forces a post — §J.5.)* |
| **ESCALATE** *(deterministic tier only — never a final answer)* | ≥2 `[EDGE−]` · a tripwire's `Expires` date passed unfired | Judgment tier decides what it means. |
| **PATCH** | Judgment tier finds a claim that was wrong **when written** | Erratum in place per §J.8. No re-run. |
| **REFRESH** | Facts stale (≥2 quarters reported, or ≥90d with unincorporated items) but Edge/Tripwires intact | Seeded re-run → new dated report, dispatching the agents the **work order** names (§J.6). |
| **RE-UNDERWRITE** | A tripwire tag explicitly says `fires` · judgment tier concludes the Edge is falsified | **Full** `/deep-dive`, all four sub-agents. |

**Why `[EDGE−]` accumulation escalates rather than concluding.** A tag count is a proxy for *pressure*; it is never evidence the Edge *changed*. The live corpus proves the difference: both of CIFR's `[EDGE−]` entries state in their own text that the Edge's **core was corroborated** — one says so outright — because that Edge is two-sided ("either the bullish variant … or the bearish variant … pick a side"), so an item can cut against one branch while confirming the thesis. Concluding RE-UNDERWRITE from the count alone dispatches four Opus agents on a name whose own log says the thesis is working.

Only three things speak to actual change, in ascending strength: the tag count (pressure) → reading the entries (pressured vs. falsified) → **re-deriving §18 and diffing it** (proof). Only the third is conclusive, and it happens *during* the re-run — so the audit's job is to make that bet cheap and evidence-backed, not to eliminate it.

A tag that says `fires` is different in kind: a prior run already made that assessment against the pre-committed trigger, so the deterministic tier is **relaying a determination, not inferring one**.

## J.4 — Tripwire expiry

Every tripwire's window eventually closes: the print it watched happens, the commencement target passes, the premise lapses. **An expired, unfired trigger still reads as coverage while being dead — worse than an empty slot**, because a watch-list of resolved triggers looks populated.

**Grammar.** The date is its own field, not an inline annotation buried mid-sentence — the trigger prose stays verbatim from the report. Inside `## Tripwires`, the numbered `(n) …` triggers are written as a bullet list (one `- **(n)** …` line each, not one dense paragraph — a report's prose is split into bullets as a formatting change only, never reworded), and immediately after them a small table carries one row per trigger:

```
| # | Expires |
|---|---|
| 1 | 2027-03-31 |
| 2 | 2027-06-30 |
```

Parsed by `tickerlib.tripwire_expiries`, which reads the trigger numbers from the prose's `(n)` markers and the dates from the table.

- **The date** comes from the trigger's own text where it names a window (a print date, a guided ship window, a commencement target); otherwise ~12 months from the report as a review horizon.
- **Checked against today**, not the baseline — expiry is a property of the trigger's own window, not of what got logged since the report.
- **Expiry ≠ fired.** It means the window closed *without* the trigger firing.
- **A trigger with a blank cell, or no row at all, is surfaced as untracked** (hygiene, not staleness) rather than guessed at.

**Detection is deterministic; the response is not.** An expired trigger has three possible fates — **removed** (the question it asked is settled), **re-dated** (its window genuinely moved, e.g. a slipped commencement), or **replaced** by a successor from a re-underwrite. Which one applies is a judgment about the thesis, so per §J.1 the audit flags it and **a human decides**. Never auto-remove: silently deleting a trigger destroys the pre-commitment as surely as silently rewriting one.

## J.5 — Reporting: by exception

Separate **how often the audit runs** from **how often it speaks**. It is cheap and deterministic, so running it often is fine; noise control belongs entirely here, in the reporting layer, never in throttling the trigger.

- **Silent when CLEAN.** A weekly "all fine" post is how a channel becomes ignorable.
- **One exception: a CLEAN verdict carrying an `early-warning` still posts.** Verdict and notification are **separate outputs** (`audit_report.py` emits a `notify` flag independent of the verdict) — approaching a trigger is high signal for a human even when it is correctly no signal for the router.
- **Re-nag suppression:** don't repeat the same verdict for ~30 days unless it **escalates**. Cache eviction costs at worst one duplicate nudge.
- **Always write the artifact** even when silent, so a human can confirm the audit ran.
- **Routing:** a per-ticker verdict goes to that ticker's own Discord channel, alongside the news that caused it; the sweep's roll-up goes to the dispatcher channel.
- **Content must be actionable:** the verdict, the *specific dated evidence* that produced it, and the exact command to run. The audit should arrive carrying the decision, so the human is approving or declining rather than investigating from scratch.

**Why `early-warning` never escalates the route.** `standing-rules.md` §A: a threshold "cannot be quietly softened once it is crossed **or approached**." A REFRESH re-derives §18 and then prompts to promote it — so routing an approaching-but-untripped trigger there would manufacture a threshold-rewrite opportunity at exactly the moment the threshold is being approached.

## J.6 — REFRESH dispatches a work order

A partial re-run is only defensible if the audit says **what** is stale and dispatches exactly the agents that own it. The audit already computes dated evidence to justify its verdict; that evidence **is** the work order.

| Evidence | Agent |
|---|---|
| `[Financials/…]`, `[Management/Insider]`, a quarter reported | **filing** (§H) |
| `[Risks/Concentration]`, anchor tenant / customer / financing partner | **counterparty** (§H) |
| `[Moat/Competition]`, `[Tech moat]` | **competitive-landscape** (§G) |
| `[Sentiment/…]`, `[Catalyst/Re-rate driver]`, secular demand | **sector** (§H) |

The judgment tier owns this mapping — the framework-tag vocabulary is open and has drifted, so it can't be matched reliably by script. `audit_report.py` emits a *hint* only.

**The agent set is the union of the work-streams named. If it comes out as all four, it is not a REFRESH** — run it as a full re-underwrite and say so.

**This buys a disclosure obligation, not a discount** (`standing-rules.md` §A carries the matching exception to the four-agent mandate, gated on all three of these):

1. **The audit named the scope** — never "it's probably just the numbers."
2. **Section-level provenance.** Every section of the resulting report states whether it was **re-researched this run** or **carried forward from `<prior-date>`**, and the provenance block lists what was excluded. A partial re-run otherwise puts today's date on sections nobody re-checked — *fresh numbers under conclusions reasoned from superseded ones, which reads as current while being wrong.* **A partial run that does not disclose its omissions is worse than not refreshing at all.**
3. **Within the staleness horizon (~180 days).** The work order can only name what the audit can *see*, and what it sees comes from `news.md`. A section that went stale with **no logged news is invisible to it** — guarding that unknown-unknown is why the four-agent mandate exists. So "no logged news in area X" is a proxy for "X is current," and that proxy **decays**: past the horizon, all four run regardless.

## J.7 — Refresh provenance: re-derive, don't recall

The audit's outputs are **ephemeral by design** — the Discord message scrolls away, `.audit-state` is evictable and never committed. So when a human runs `/deep-dive` days or weeks later, **there is no stored audit record to quote.** That is not a hole to fill with a new store; it means the provenance block is **recomputed, not recalled**.

**Rule: an audit-triggered deep-dive re-runs the audit live, before writing the report, and builds the block from that run.** Every deterministic signal is a pure function of current repo state, so it returns the same verdict or a more current one.

- **Ordering is load-bearing.** Signals are relative to `latest_report_date()`. The moment the new report is written that baseline becomes *today*, so "items after the report date" collapses to empty and the audit returns **CLEAN with no evidence** — the block would then state, confidently, that nothing was stale. Pass **`--baseline <superseded-report-date>`**, which is also the semantically correct question: *what has happened since the report I am replacing?*
- **The block is conditional on a predecessor existing (repo state), not on the run being "audit-triggered."** That is undetectable — a human types `/deep-dive <T>` with no flag and no memory of a three-week-old nudge. Gating on it would silently skip the block on every hand-initiated re-run, which is the same failure `standing-rules.md` §A already closes for Edge/Tripwires, one artifact over.

**Required contents** — see the deep-dive skill for where it is written:

- Which audit triggered it, dated, and the verdict.
- The specific signals that fired, **with dated, citable evidence**.
- The prior report it supersedes, linked.
- **The work order that was run and what it excluded** (§J.6).
- **The Edge diff** — the orchestrator re-derives the Edge independently (withholding the prior one from sub-agents, per the asymmetric-context rule below) and compares. If it came out materially unchanged, **say so explicitly**: a thesis surviving independent re-derivation is a real finding. If it changed, that is the single most important sentence in the new report.

**The failure mode to prevent:** *"Routine refresh; updated for latest data."* That tells a future reader nothing about whether the refresh was warranted or what moved, and makes the refresh chain unauditable exactly when someone is reconstructing how a view evolved.

**Asymmetric context for the re-run.** Handing research agents the existing Edge makes them confirm it, defeating a variant view whose whole value is falsifiability — but feeding nothing forward loses expensively-won corrections. So split by kind: **feed forward** corrections, errata, disconfirming findings, and "what the filings actually say vs. what trade press claims"; **withhold** the Edge, the numbered tripwires, verdicts, and the bull/base/bear bands. Then diff.

## J.8 — What "immutable" means

The framework says reports are immutable once published. Resolution:

- **Immutable as to judgment.** A verdict, Edge, tripwire, probability, or bull/base/bear band is **never** restated to match how things turned out. This preserves the "what did I actually believe on date X" property that makes the corpus scoreable.
- **Patchable as to fact, with a visible scar.** A figure that was *wrong when written* may be corrected in place and **must** carry a dated `> **ERRATUM (corrected YYYY-MM-DD)**` block naming what was wrong, what it should have been, and how it was caught.
- A fact that was *right when written and has since changed* is **not** an erratum — that is staleness, and it routes to REFRESH.
- **Immutability attaches at commit, not at first write.** A report amended within the run that created it has never been published — which is what lets the provenance block, composed after the Edge diff, be written into the file the run already created.
