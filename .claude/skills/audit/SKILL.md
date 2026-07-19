---
name: audit
description: >-
  Run the staleness audit on watched tickers in this equity-watch repo — check whether a
  ticker's dated deep-dive report has gone stale against everything logged since, and route
  it to CLEAN / PATCH / REFRESH / RE-UNDERWRITE with dated evidence. Use this whenever the
  user says "audit <TICKER>", "run the staleness audit", "is <ticker>'s report still
  current", "which reports need refreshing", "check for stale reports", or asks whether a
  deep-dive needs re-running. Also the skill to use when a tripwire's window has expired or
  an audit Discord alert asks for a decision. This RECOMMENDS only — it never re-runs a
  deep-dive and never edits a ticker's Edge or Tripwires; for the re-run itself use the
  deep-dive skill, and for a routine news scan use the whats-new skill.
---

# Staleness audit — triage, not rewriting

This skill is a **launcher**, not a rulebook. This repo is the master for the research
framework, and the binding rule (`CLAUDE.md`) is: **apply the framework files as written —
never restate the rules from memory.** Read the canonical files below and execute the method
they define. If any is missing from the checkout, STOP and report it.

## Step 0 — establish today's date
Take today's date from the session's current-date context (do **not** infer it from training
data). Tripwire expiry is checked against **today**, so a wrong date silently mis-flags live
triggers as dead — or worse, misses dead ones.

## Step 1 — read the canonical framework
1. **`framework/standing-rules.md`** — Sections A + E. Note especially **"The pre-committed
   Edge & Tripwires — a hard invariant"**: it binds this workflow. The audit **never writes**
   to a ticker's `news.md`. Section A's "EXHAUSTIVE BY DEFAULT" depth does **not** apply —
   this is a bounded triage pass, not a report.
2. **`framework/staleness-audit.md`** — **Section J: the complete method.** §J.1 what the
   audit may never do · §J.2 the two tiers and the boundary between them · §J.3 routing ·
   §J.4 tripwire expiry · §J.5 reporting by exception · §J.6 the REFRESH work order ·
   §J.7 refresh provenance · §J.8 what immutable means. Single source of truth — execute it,
   don't paraphrase it.

## Step 2 — run the deterministic tier
```
python scripts/audit_report.py [--ticker <TICKER>] --json
```
Repo-local, no network, no LLM. Emits per-ticker signals and a verdict. Add `--baseline
<YYYY-MM-DD>` only when auditing against a **specific superseded report** (the refresh path —
see §J.7); otherwise it resolves the latest report by glob itself.

**Read the verdicts as §J.2 defines them.** `CLEAN` and `REFRESH` are final — the tier
counted, and counting is sufficient for both. **`ESCALATE` is not an answer**; it means the
deterministic tier found pressure it cannot interpret, and Step 3 is mandatory. `RE-UNDERWRITE`
from a `fires` tag is final (a prior run already made that assessment against the trigger).

## Step 3 — the judgment pass, ONLY for escalated tickers
Skip entirely if nothing escalated — that gate is what makes the audit cheap enough to run on
every push. For each escalated ticker, read `tickers/<TICKER>/news.md` (the Edge, the numbered
tripwires, and the post-baseline log entries **in full**) plus the report it is being audited
against, and answer only what §J.2's judgment tier asks:

- **Contradiction check** — does a logged item *contradict a specific claim* in the report, or
  merely postdate it? A contradiction that was **wrong when written** is a **PATCH** (§J.8),
  not a refresh.
- **Edge status — pressured or genuinely falsified?** **Read the entries, do not trust the
  tag count.** §J.3 explains why with the live example: both of CIFR's `[EDGE−]` entries say
  in their own text that the Edge's *core was corroborated*, because a two-sided Edge can be
  confirmed by an item that cuts against one of its branches. Falsified → RE-UNDERWRITE.
  Pressured → say so and leave it CLEAN.
- **Expired tripwires (§J.4)** — for each, recommend **remove** (the question it asked is
  settled), **re-date** (its window genuinely moved), or **replace** (a successor trigger from
  a re-underwrite). Recommend; never edit.

Research is **not** part of this skill. If answering a question needs new external facts, that
is what the refresh is for — say so and route, rather than turning the audit into a mini
deep-dive.

## Step 4 — report, and hand the decision over
Lead with the verdict and the **specific dated evidence** that produced it, then the exact
command. Per §J.5 the content must be actionable, so the reader is approving or declining
rather than investigating from scratch.

- **State the route and what it costs**: REFRESH names its **work order** (§J.6 — which
  agents, and what each must re-verify); RE-UNDERWRITE is all four.
- **Never dispatch the re-run yourself** (§J.1). Recommend `/deep-dive <TICKER>`; the human
  runs it. The re-run re-derives this audit live for its provenance block (§J.7), so nothing
  needs carrying forward from this session.
- **Never edit `news.md`** — not the Edge, not a tripwire, not even an expired one. Say what
  should change and let the human say yes.
- A clean audit is a useful result: say explicitly what was checked and that nothing fired.

## Step 5 — post to Discord (only when something warrants it)
Ad-hoc runs post from the session; the scheduled sweep does this itself via
`.github/workflows/audit.yml`. Skip this step on a CLEAN, nothing-forced run — §J.5 is
exception-only reporting, and a routine "all fine" post is how a channel becomes ignorable.

```
python scripts/audit_notify.py --results <audit-json> [--dry-run]
```
It applies §J.5's re-nag suppression itself (same verdict inside ~30 days stays quiet unless
it **escalated**), posts per-ticker verdicts to their own channels, and writes the roll-up.
The poster skips gracefully when a ticker has no webhook configured.

## Guardrails
- Not financial advice — informational research tooling only.
- **The audit flags; a human decides.** Every route that regenerates a report or changes a
  pre-committed trigger is a human decision (§J.1). This is the whole design, not a courtesy.
- Never fabricate evidence. Every claim in a verdict cites a dated log entry, a debrief
  heading, or a tripwire's own expiry date.
- Don't let a judgment pass sprawl into research. Bounded read, then route.
