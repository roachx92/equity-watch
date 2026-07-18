# Deterministic dispatcher for earnings-digest + what's-new

**Date:** 2026-07-18
**Status:** Approved design, pre-implementation
**Branch:** `work/2026-07-18-dispatcher-triggers`

## Problem

The `earnings-digest.yml` and `whats-new.yml` workflows are `workflow_dispatch`-only —
every run is a manual click with a single `ticker` input. We want them to fire on a
**deterministic schedule** instead:

- **Earnings digest** is event-timed: it should run the morning after a watched ticker
  reports. The blocker is that the repo has no source of truth for *when* each ticker
  reports (front matter carries only `company`/`blurb`).
- **What's-new** is continuous with no natural trigger. Running an Opus, multi-sub-agent
  scan across all tickers every day is the token-cost extreme we want to avoid. We want
  a cheap pre-filter that only spends the expensive scan when something material actually
  moved.

## Non-goals

- No change to the analytical behaviour of `earnings-digest.yml` or `whats-new.yml`. They
  keep their coverage guards, their Opus pinning, their PR/commit/Discord flow. The
  dispatcher only *triggers* them.
- No new roster file. The watch-list stays the set of `tickers/*/` folders.
- No committing dispatcher state to `main` (the repo's standing git rule forbids direct
  commits/pushes to `main`).
- No attempt to fake coverage for tickers Finnhub doesn't serve.

## Architecture

One new scheduled workflow, `.github/workflows/dispatcher.yml`, runs a **deterministic
Python script** `scripts/dispatch.py` on a weekday-morning cron. The script uses **no
Claude and no sub-agents** — it is a cheap pre-filter. For each watched ticker it decides
whether an earnings digest and/or a what's-new scan is warranted, then fires the existing
heavy workflow via `gh workflow run <file> -f ticker=<T>`.

```
dispatcher.yml (cron: weekday mornings)
  └─ scripts/dispatch.py
       ├─ glob tickers/*/            → the watch-list
       ├─ Finnhub /calendar/earnings → earnings trigger  (§ Earnings)
       ├─ Finnhub /company-news      → what's-new gate    (§ What's-new gate)
       └─ gh workflow run …          → fire earnings-digest.yml / whats-new.yml
```

**Dispatch mechanism.** `gh workflow run` issues a `workflow_dispatch` via the REST API.
`workflow_dispatch` and `repository_dispatch` are the documented exceptions to GitHub's
`GITHUB_TOKEN` recursion guard, so a token-driven dispatch *does* start a new run. This is
already proven in this repo: `earnings-digest.yml` ends by calling
`gh workflow run pages.yml` with `GITHUB_TOKEN`.

**Single external dependency:** a `FINNHUB_API_KEY` repo secret. Finnhub's free tier
exposes both `/calendar/earnings` and `/company-news`, so one key serves both triggers.

## Earnings trigger — stateless, repo-read dedup

For each ticker:

1. Query `/calendar/earnings?symbol=<T>&from=<yesterday>&to=<today>`.
2. If a report is dated within that window, read the checked-out
   `tickers/<T>/earnings-debrief.md` and check whether **that quarter is already present**
   (match on the reporting date / quarter heading the earnings-digest workflow writes).
3. Dispatch `earnings-digest.yml -f ticker=<T>` **only if the quarter is absent**.

Dedup is derived from the repo itself, so it is **self-healing**: no persisted state to
corrupt, and no risk of double-digesting a quarter even if the what's-new cache (below) is
wiped. This is deliberately independent of the gate's cache so the one genuinely damaging
duplicate case — two debriefs for the same quarter, which prepend and cannot be cleanly
undone — cannot happen from a state loss.

**Foreign names.** IBIDY (Tokyo ADR) and LPKF (Xetra) will not reliably appear on the US
earnings calendar. When the calendar returns nothing for a ticker, the dispatcher logs
`no calendar coverage` and leaves it for manual dispatch — it does not guess a date.

## What's-new gate — keyword filter + 48h cap

For each ticker:

1. Query `/company-news?symbol=<T>&from=<last_news_scan or today-3d>&to=<today>`.
2. Keep a headline only if it matches the **materiality keyword set** — a commented,
   editable constant in `dispatch.py`. Seed list (case-insensitive, word-boundary):
   `earnings, results, guidance, forecast, outlook, contract, award, deal, offering,
   dilution, raise, downgrade, upgrade, price target, SEC, 8-K, 10-Q, CEO, CFO,
   resign, appoint, merger, acquire, acquisition, buyout, halt, recall, lawsuit,
   investigation, bankruptcy`.
3. If ≥1 headline survives the filter **and** `last_news_scan` for this ticker is ≥48h ago
   (or unset), dispatch `whats-new.yml -f ticker=<T>` and set `last_news_scan = now`.

The 48h cap is the primary cost control — it stops a headline-heavy name (e.g. AAOI) from
firing the expensive scan every single day. The keyword filter removes routine noise
(price-move recaps, listicles) that would otherwise trip the gate.

Rationale for keeping the gate deterministic rather than an LLM: materiality *judgement*
is exactly what the paid Opus scan already does well. The gate only needs to be a coarse
"is there plausibly something here?" filter — cheap, predictable, and it fails toward
running the scan (a false positive costs one scan; the scan itself is the real judge).

## State & idempotency

The gate's only state is a per-ticker `last_news_scan` timestamp:

```json
{ "AAOI": { "last_news_scan": "2026-07-18T13:30:00Z" }, "...": { } }
```

Stored via **GitHub Actions cache** (`actions/cache/restore` at job start,
`actions/cache/save` at job end) — **not** a committed file, keeping the dispatcher off
`main`. A daily restore keeps the cache warm, so eviction is unlikely; if it is evicted,
the cost is bounded (a few extra scans, capped by the keyword filter + 48h rule). Earnings
dedup does **not** read this cache (§Earnings), so cache loss never causes a duplicate
quarter.

## Schedule & secrets

- **Cron:** `30 13 * * 1-5` (≈09:30 ET, weekdays). Catches prior-day after-market reports
  and same-morning before-market reports in one pass. `workflow_dispatch` is also enabled
  for manual and shakedown runs.
- **Permissions:** `actions: write` (to dispatch the heavy workflows), `contents: read`.
- **New secret:** `FINNHUB_API_KEY`.

## Observability

Every run writes a per-ticker table to the Actions job summary (`$GITHUB_STEP_SUMMARY`):

| Ticker | Earnings | What's-new | Reason |
| --- | --- | --- | --- |
| AAOI | — | **dispatched** | keyword: "contract" (2 headlines) |
| COHR | **dispatched** | — | earnings reported 2026-07-17 |
| CIFR | — | skipped | rate-capped until 2026-07-19 13:30Z |
| IBIDY | skipped | skipped | no calendar coverage; no material news |

No silent drops — every ticker's outcome and the reason for it are visible, so the token
spend is auditable and the gate's decisions are debuggable.

## Module boundaries (for testability)

`scripts/dispatch.py` is structured so the two I/O edges are injectable:

- `FinnhubClient` — wraps `/calendar/earnings` and `/company-news`. In tests, replaced by a
  fake returning recorded fixtures. No live API call in the test suite.
- `dispatch_workflow(file, ticker)` — wraps `gh workflow run`. In tests, a recording spy.
- Pure decision functions with no I/O:
  - `is_material(headlines, keywords) -> list[matched]`
  - `earnings_due(calendar_rows, today) -> report_date | None`
  - `quarter_already_logged(debrief_text, report_date) -> bool`
  - `news_gate(ticker, headlines, last_scan, now) -> Decision`
- A `--dry-run` flag prints the decision table without dispatching, for the first live
  shakedown against real Finnhub data.

## Testing

Unit tests (fixtures only, no network):

1. Keyword matcher: matches on word boundary, case-insensitive; ignores routine headlines.
2. 48h cap: fires when `last_news_scan` unset / >48h; skips when <48h.
3. Earnings dedup: dispatches when the quarter is absent from the debrief; skips when the
   reporting date is already present.
4. Foreign fallthrough: empty calendar → `no calendar coverage`, no dispatch, no crash.
5. Summary rendering: the decision table matches the decisions taken.

Live shakedown: run `dispatcher.yml` manually with `--dry-run` and confirm the summary
table looks right before enabling the cron.

## Files touched

- `.github/workflows/dispatcher.yml` — new scheduled workflow.
- `scripts/dispatch.py` — new deterministic dispatcher.
- `scripts/tests/test_dispatch.py` (or repo's existing test location) — unit tests + fixtures.
- Repo secret `FINNHUB_API_KEY` — provisioned out of band (documented in the PR).

## Open items / follow-ups (not in this build)

- If Finnhub's international coverage proves better than expected, IBIDY/LPKF could later be
  promoted from manual to auto — no design change, just remove them from the skip path.
- A future materiality-keyword tune could be data-driven (which keywords actually preceded
  a [TRIPWIRE]/[EDGE] hit), but the seed list ships first.
