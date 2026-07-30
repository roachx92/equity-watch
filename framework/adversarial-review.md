# Adversarial review — the pass whose job is to be wrong about the thesis

*Section L of the equity research framework. One sub-agent per run whose success
criterion is **inverted**: it is dispatched to break the Edge, not to test it.
Other files reference this one — they do not restate it.*

---

## L.0 — Why this exists

Every research sub-agent in this framework is dispatched with the ticker's Edge
quoted verbatim and, per `latest-updates-workflow.md` §F.2(5), **a hunt-list
derived from that Edge and its numbered Tripwires**. That rule is right and
should stay: it is what stops a pass from returning generic company news.

But it means every agent searches *the thesis's own terms*. The 2026-07-29 COHR
run dispatched four sub-agents and **all four returned `[EDGE+]`** — reported in
the digest as "three independent corroborations." They were not independent.
They shared a framing, a hunt-list, and a definition of what counted as relevant.
**Four confirmations from one framing is one confirmation.**

The corpus shows the shape of it. Across the watch-list: **74 `[EDGE+]` against
30 `[EDGE−]`**. COHR sits at 17–3 with a run of seven consecutive `+`; MSTR at
24–4; **WYFI at 4–0 and IBIDY at 1–0 — theses no logged item has ever cut
against.** Only CIFR is majority-negative (2–11), and CIFR is precisely the name
whose Edge the audit escalated.

That ratio is **not** evidence of a biased analyst. A well-chosen variant view
should be right more often than wrong, and these theses were adopted because
someone believed them. It is evidence of something narrower and fixable: **no
step in the process is trying to produce the other sign.** A pipeline that only
ever asks *"does this corroborate?"* will answer that question, and a long
unbroken run of confirmations is exactly the condition under which confirmation
bias is least visible from the inside.

A second failure has the same root. On 2026-07-22, AAOI's and COHR's logs
recorded the *same* Alphabet print, citing the *same* CNBC URL, and
**contradicted each other** — AAOI said the FY2026 capex guide was "kept at
$180–190B … reaffirmed, not raised again"; COHR said it was raised to
$195–205B. Alphabet's CFO said verbatim it was updated to $195–205B. AAOI's
entry was wrong, and it reasoned *from* the wrong figure to a Tripwire #3
assessment. It survived because **nothing's job was to check it.**

## L.1 — The red-team agent

**One dedicated sub-agent per qualifying run.** Its prompt is self-contained
(§F.2) and carries:

1. Today's date and the ticker.
2. The **Edge verbatim** and the numbered **Tripwires with their `Expires`
   dates** — it must know precisely what it is attacking.
3. The run's **load-bearing figures** — every number the orchestrator intends to
   rely on, with the source each came from (see §L.4).

**It is deliberately NOT given the §F.2(5) hunt-list.** That list is derived from
the Edge, so handing it over reproduces the framing this pass exists to escape.
The red team derives its own angles from first principles: *what would have to be
true for this thesis to be wrong, and where would that show up first?*

**Its brief has four parts:**

- **Steelman the consensus.** The Edge is by construction a variant view, so
  something is on the other side of it. State the consensus position in its
  strongest form, with its best evidence — not as a strawman to knock down.
- **Name the falsifier.** What specific, observable fact would make the Edge
  wrong? Not "competition intensifies" — a named mechanism with a place it would
  appear first.
- **Go looking for it.** Dated, sourced, specific.
- **Attack the reasoning, not only the facts.** An Edge can be built on true
  figures and still not follow from them.

**The success criterion is inverted, and the prompt must say so explicitly:**

> A specific, dated, sourced item that cuts against the Edge is the most valuable
> thing you can return. Finding nothing is a **weaker** result than finding a real
> problem — and you must say plainly which of the two happened. Do not manufacture
> a concern to satisfy this; an honest "I looked here, here and here and the Edge
> held" is a genuine finding, but it must be stated as *coverage*, not as
> endorsement.

**It must not be told the current `[EDGE+]`/`[EDGE−]` tally**, nor which way
prior runs landed. A red team that knows the thesis is 17–3 is anchored before
it starts.

## L.2 — Reconcile, never average

If the red team returns a contradiction and the other agents return
corroboration, **that is a live test, not a wash.** Both are surfaced.

- Do **not** net them into a single sentiment.
- Do **not** let "three agents said + and one said −" resolve by majority. The
  three shared a framing; the one did not. They are not four votes.
- The orchestrator's job is to say **which is load-bearing and why** — and if it
  cannot, the honest output is that the Edge is under an unresolved live test
  (§F.3's ⚪ status exists for exactly this).

A run that ends "the red team found X, and here is why X does not overturn the
Edge" is a **stronger** result than one where nothing was looked for.

## L.3 — When it runs

- **Deep-dive: always.** A fifth mandatory sub-agent alongside the four in
  `deep-dive-template.md` §H/§G. A full re-underwrite that never argued the other
  side has not been underwritten.
- **Whats-new: on a confirmation run.** When the ticker's Edge has accumulated
  **five or more consecutive same-signed items with no contrary one**, the next
  run dispatches the red team. That is the state in which the framing is least
  visible, and it is measurable from the log rather than left to judgment
  (`scripts/crossref.py`-adjacent tooling can count it).
- **Audit: on an Edge-pressure escalation.** §J's judgment tier asks whether an
  Edge is *pressured or genuinely falsified*. That question should not be
  answered only by re-reading entries written under the original framing.

**A ticker whose Edge has never once been contradicted is a candidate regardless
of run count** — WYFI (4–0) and IBIDY (1–0) are not necessarily right; they may
simply never have been argued with.

## L.4 — Fact-check duty

The red team also re-verifies the run's **load-bearing figures against primary
source**. This is cheap now and was not before:

| Claim type | Verify with |
|---|---|
| A filing exists / does not exist in a window | `scripts/edgar.py --since` |
| A tagged financial-statement line item | `scripts/facts.py` |
| A close, a % move, a drawdown | `scripts/prices.py` (never a percentage headline) |
| The same event logged under a peer | `scripts/crossref.py --duplicates` |

**Worked example — the failure this clause is written against.** Both the AAOI
and COHR entries for Alphabet's 2026-07-22 print cited the same URL and
disagreed by $15B on the largest hyperscaler's capex guide. One number, one
source, two records, no reconciliation. A single primary-source check would have
caught it; nothing was assigned to make one.

**A disagreement between two tickers' logs about the same event is always a
finding**, and it is an erratum under `staleness-audit.md` §J.8 — wrong when
written — not staleness.

## L.5 — Output, and what it may not do

The red team **researches and argues; it never writes.** Same rule as every
other sub-agent (§F.2, §K.4): the orchestrator does all file writes.

It reports:

- the **steelmanned consensus** view;
- the **named falsifier(s)** and whether each was found, with dated sources;
- any **factual error** in the run's own load-bearing figures;
- an explicit closing line stating which happened: *a real problem was found*, or
  *the listed angles were searched and the Edge held.*

**It does not assign the `[EDGE±]` tag.** Tagging is the orchestrator's
assessment against the ticker's own §18 (§F step 4), and a red team that tagged
its own findings would be scoring its own exam. Its findings are **input** to
that assessment.

And the standing invariant is unchanged: **nothing here edits an Edge or a
Tripwire.** A red-team finding that the Edge is falsified is a recommendation to
re-underwrite, routed to a human exactly as `standing-rules.md` requires.

_Not financial advice — informational research tooling only._
