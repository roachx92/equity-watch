---
name: whats-new
description: >-
  Check the latest news/updates on a watched ticker in this equity-watch repo and assess
  every item against that ticker's pre-committed Tripwires and Edge, then append dated
  entries to its Recent News Log and produce the canonical run-summary digest. Use this
  whenever the user says "what's new on <TICKER>", "latest on <ticker>", "any updates on
  <company>", "catch me up on <ticker>", "did anything happen with <ticker>", or asks for
  recent developments on a stock already covered in tickers/ — even without the word "news".
  This is the lighter, bounded news-scan entry point, and it spans whatever happened since the
  last check. Two neighbours: if the request is specifically about **one earnings call or print**
  ("<ticker> just reported", "break down the call"), use the earnings-digest skill instead; for
  building a name's full 18-section report from scratch (or "run the framework on <ticker>"),
  use the deep-dive skill.
---

# What's new — bounded news check on a watched ticker

This skill is a **launcher**, not a rulebook. This repo is the master for the research
framework, and the binding rule (`CLAUDE.md`) is: **apply the framework files as written —
never restate the rules from memory.** Read the canonical files below and execute the method
they define. If any is missing from the checkout, STOP and report it.

## Step 0 — establish today's date
Take today's date from the session's current-date context (do **not** infer it from training
data). Use it as the anchor for the "since last entry" search window, the date stamped on every
log entry and every source citation, and the commit message.

## Step 1 — read the canonical framework
Read these directly (small, purpose-scoped) — do not work from memory of them:
1. **`framework/standing-rules.md`** — Sections A + E, binding on every step. Note the explicit
   exception: this bounded scan does **NOT** apply Section A's "EXHAUSTIVE BY DEFAULT" diligence
   depth (that's for full reports) — the search window here is bounded (see §A of news-check).
2. **`framework/latest-updates-workflow.md`** — Section F: the analytical procedure, including
   the **mandatory §18 Tripwire/Edge assessment** of every item, and **§F.1** — the canonical
   Recent News Log entry format (single source of truth; don't restate it).
3. **`framework/news-check.md`** — the shared spec: **§A** the parallel research-sub-agent
   method (self-contained prompts, source-quality guidance, first-run ~14-day window) and **§B**
   the run-summary digest format. This file is the single source of truth for both — don't
   restate it.

## Step 2 — confirm the ticker is covered (else build it first)
Per Section F step 1: a "what's new" check presupposes a full report and the §18 Edge/Tripwires
already exist. Each watched ticker is a **folder** under `tickers/`, named for the symbol,
holding that ticker's **news.md**. Check for `tickers/<TICKER>/news.md` with an Edge and numbered
Tripwires (and a `tickers/<TICKER>/reports/<date>.md` it links). **If the name isn't covered yet, build
the deep-dive first** (use the `deep-dive` skill / `framework/deep-dive-template.md`), which
creates the ticker's folder and news.md and derives the Edge/Tripwires into it, then continue
here.

## Step 3 — dispatch bounded research sub-agents, in parallel
Per `news-check.md` §A: **do not research single-threaded.** Dispatch a thorough parallel
sub-agent pass (one dedicated agent, or several split by angle — filings/financing vs.
product/competitive vs. sentiment/positioning — when depth is warranted). Each self-contained
prompt must include: today's date + ticker; an instruction to `Read tickers/<TICKER>/news.md`
(the ticker's news.md) and quote its exact Edge and numbered Tripwires **verbatim**; the search
window (since the last dated log entry, or ~14 days back if the log is empty); the source-quality
guidance; a hunt-list of one line per Tripwire + the Edge mechanism; and the report-back format
(dated items, direct source URLs, full substantive detail). **Sub-agents research only — they
must NOT edit files.**

## Step 4 — assess, then write to the ticker's news.md
Wait for the sub-agents, then yourself:
- **Categorize** each material event against the framework sections (short `[TAG]`).
- **Assess against the §18 Tripwire and Edge — MANDATORY.** Tag `[TRIPWIRE]` (name which
  trigger fired, how close to threshold, the pre-committed action) — highest priority, surface
  it at the TOP. Tag `[EDGE+]` / `[EDGE−]` for items that corroborate/undermine the variant view;
  call out an accumulation of `[EDGE−]` even if no single tripwire fired.
- **Append full-detail, dated entries** to the ticker's `news.md` `## Recent News Log` per the
  canonical entry format in `framework/latest-updates-workflow.md` §F.1 (most recent first,
  never to the deep-dive report — that's a frozen snapshot). Apply §F.1 as written; do not
  restate its rules here.
- **Commit** the updated news.md if anything changed (e.g. `whats-new: <TICKER> <date>`).

## Step 5 — produce the run summary
Emit the chat digest in the **canonical format defined in `news-check.md` §B**: the per-ticker
news items lead (so the reader sees what's worth logging first), then 🚨 tripwires, then edge
shifts, then the conditional Edge & Tripwires recap — with the **fired-tripwire escalation
override** (a 🚨 callout goes to the very top when any tripwire fires). A single-ticker request
collapses naturally to that one ticker. Even a clean check (nothing fired) is a useful result —
say explicitly that you checked against the Tripwire
and Edge and nothing fired.

## Guardrails
- Not financial advice — informational research tooling only. Never fabricate a figure or a
  source; if a source has no linkable URL, say so rather than omitting it silently.
- Keep the log clean: full detail in the ticker's news.md, one-sentence digest in the chat reply.
