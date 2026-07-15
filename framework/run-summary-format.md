# Run-summary output format

*The single canonical format for the chat-reply digest produced at the end of a news check. Used by BOTH the scheduled daily watch (`daily-watch.md`, run across its ticker set) and the ad-hoc "what's new / latest on [ticker]" workflow (`latest-updates-workflow.md`, Section F, usually one ticker). **Single source of truth — edit here only; the two workflows reference this file, they do not restate it.***

Produce a short digest, **TRIPWIRES FIRST.** The full multi-paragraph detail lives in each ticker's `## Recent News Log` (in `tickers/<TICKER>.md`), not the chat reply — EXCEPT the Tripwires/Edge-shifts bullets below, which each get one detailed line per hit, not just a bare list:

- **🚨 TRIPWIRES:** one bullet per `[TRIPWIRE]` hit (across every ticker checked this run), format:
  `**<TICKER> Tripwire #n — <status, e.g. "live, unresolved" / "early-warning" / "checked, does not fire">.** <one clause: what happened, why it matters, and the next test/date if still pending>.`
  If a ticker had no tripwire activity, a one-line `<TICKER>: none` is enough — don't pad it. If nothing fired anywhere, just say "none."
- **Edge shifts:** one bullet per `[EDGE+]/[EDGE−]` item (group same-direction items for one ticker into a single bullet if there are several), format:
  `**<TICKER> — EDGE+ / EDGE− / EDGE live test.** <one clause: what the item was, with its dated anchor>.`
  Omit a ticker entirely here if it had no edge activity — don't pad with "none."
- **Per-ticker items:** list every substantive item found this run, one per item, most recent first, as a **headline + one-sentence abridged digest** — a step up from headline-only, but still NOT the full multi-clause paragraph (that stays in the ticker file's Recent News Log). Format:
  `YYYY-MM-DD — [FRAMEWORK-TAG] — **Headline**. One-sentence abridged digest of what happened → brief impact. [TRIPWIRE #n / EDGE+ / EDGE− if applicable]`
  Keep the digest to one sentence per item. If nothing material was found for a ticker, write "nothing material" instead of a list.
- **Per-ticker Edge & Tripwires recap — conditional on a hit:** if the ticker had a `[TRIPWIRE]` or `[EDGE+]`/`[EDGE−]` tag this run, restate (condensed, taken from the ticker file, not memory) its current Edge one-liner and its numbered Tripwires, so the reader sees what fired against what's being watched. If nothing fired for that ticker this run, skip the full recap and give one line instead: `<TICKER>: unchanged — Edge and Tripwires as before, nothing fired.`
- If a tripwire fired, the digest headline must say so.

For a single-ticker "what's new" request this collapses naturally to that one ticker; for the daily watch it runs across every ticker checked. Apply all of `standing-rules.md` (Sections A + E) throughout — do not work from a remembered summary.
