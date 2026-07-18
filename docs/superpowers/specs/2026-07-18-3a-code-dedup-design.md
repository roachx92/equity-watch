# 3a — Code de-duplication (Part 3 backlog, bucket 3a code half)

**Date:** 2026-07-18
**Branch:** `work/2026-07-18-3a-code-dedup` (worktree `.claude/worktrees/3a-code-dedup`, based on `main`)

## Context

The 2026-07-18 pipeline-efficiency review captured a deferred "Part 3" backlog in
`docs/part-2-scripts-plan.md`. Bucket **3a** is "DRY the docs & code." This spec
covers **only the code half**; the prose half (rules restated across framework /
SKILL launchers) is a separate follow-up PR.

The backlog's 3a code items were written before two later merges shifted the tree,
so the surface is smaller than the doc reads today:

- **Already resolved:** the "Discord color constants copy-pasted across two
  posters" item — `notify_discord.py` was retired with the daily-watch pipeline
  (PR #29); only `notify_discord_ticker.py` remains, so there is no duplication.
- **Was "three front-matter parsers," now two:** `notify_discord_ticker.py` does
  not parse front matter. The two that remain are `scripts/tickerlib.front_matter`
  (stdlib) and `web/hooks/coverage.py._front_matter` (PyYAML).
- **No real cross-check test exists** guarding the two latest-report resolvers —
  the backlog described one as planned, but it was never built. Unifying removes
  the divergence risk outright.

## Goal

One implementation of each shared primitive, with `web/hooks/coverage.py` reusing
`scripts/tickerlib` instead of carrying its own copies. **No behavior change** to
the published site or to the deterministic scripts.

## The scripts ↔ web/hooks boundary

`coverage.py` is a mkdocs build hook: it scans the *assembled* docs tree
(`config["docs_dir"]`, i.e. `web/site_src/`), not the repo-root `tickers/`. So its
tree-walking (`glob` over `docs_dir/tickers/*/news.md`) cannot be replaced by
`tickerlib.ticker_dirs`/`news_files` (those resolve from the repo root). Only the
two **pure, path-argument** helpers are shared:

- `tickerlib.front_matter(path)` — parse a file's leading `---` block.
- `tickerlib.latest_report_date(ticker_dir)` — newest `reports/<date>.md` date.

Both operate on whatever path/dir they are given, so they work equally on the
`site_src/` tree (where `reports/` is copied by `build.sh`) and the repo root.

## Units of change

### Unit 1 — Single front-matter parser

- Delete `coverage._front_matter` and its `import yaml` and duplicate
  `_FRONT_MATTER` regex.
- Add `scripts/` to `sys.path` and import `tickerlib`:
  ```python
  import sys
  from pathlib import Path
  sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
  import tickerlib  # noqa: E402
  ```
  `parents[2]` of `web/hooks/coverage.py` is the repo root; `__file__`-relative so
  it is robust to whatever cwd mkdocs runs the hook from.
- Call `tickerlib.front_matter(Path(path))` where `_front_matter` was called.

**Parity:** `coverage` only ever reads `company` and `blurb`, which are
single-line quoted scalars in every real `news.md` (e.g.
`company: "Applied Optoelectronics · NASDAQ"`). The stdlib parser returns those
identically to `yaml.safe_load`. Its regex is *more* lenient (optional trailing
newline). A code comment will note the stdlib parser handles single-line scalars
only — if front matter ever needs nested YAML, that is a separate decision (and
`lint_news_structure` could enforce the single-line form).

### Unit 2 — Single latest-report resolver

`coverage._latest_report` keeps its one distinct responsibility — formatting the
site URL — but delegates date-finding to `tickerlib`:

```python
def _latest_report(ticker_dir, sym):
    date = tickerlib.latest_report_date(Path(ticker_dir))
    return f"tickers/{sym}/reports/{date}/" if date else None
```

The duplicate `_DATE_FILE` regex leaves `coverage.py` entirely.

### `build.sh` / `serve.sh` — left as-is (per decision 2026-07-18)

The two scripts share an 8-line assembly block, but the duplication is small and
extracting a sourced snippet adds a third shell file. Decision: leave them
untouched. This keeps the PR purely Python. (Can revisit as a trivial follow-up.)

## Testing

- `tickerlib` is **untouched** → its existing tests stay green unchanged.
- **New — `scripts/tests/test_coverage.py`** (`coverage.py` has no tests today):
  import the hook, build a tmp docs tree with a `news.md` (front matter) + dated
  `reports/`, run `on_config` against a minimal fake `config` dict, and assert the
  emitted cards carry the correct `sym`, `company`, `blurb`, `monitor`, and
  `report` URL — plus a no-reports case returning `report: None`. This exercises
  the `tickerlib` import and both delegations end-to-end. The test adds
  `web/hooks/` to `sys.path` the same way the existing tests add `scripts/`.
- **Integration** (mkdocs): after the change, run `web/scripts/build.sh --strict`
  and confirm the strict build passes and the homepage coverage cards still
  render — this proves `coverage.py` reuses `tickerlib` correctly inside the real
  mkdocs hook, not just in isolation.

## Out of scope

- `build.sh` / `serve.sh` de-dup — left as-is per the 2026-07-18 decision.
- The prose half of 3a (rules restated across framework / SKILL launchers) — separate PR.
- 3b (runtime Opus/dedup/cache) and 3c (human toil).
- Any refactor of `tickerlib` itself or the mkdocs config.

## Net effect

- One front-matter parser and one latest-report resolver — `coverage.py` reuses
  both from `scripts/tickerlib` instead of carrying copies.
- `coverage.py` depends on `scripts/tickerlib` — an intentional `web/hooks` →
  `scripts` reuse (that is what the shared lib is for); PyYAML drops out of our
  hook code.
- `coverage.py` gains its first test.
