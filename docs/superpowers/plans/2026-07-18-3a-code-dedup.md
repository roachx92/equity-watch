# 3a Code De-duplication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `web/hooks/coverage.py` reuse `scripts/tickerlib`'s front-matter parser and latest-report resolver instead of carrying its own PyYAML copies, with no change to the published site.

**Architecture:** `coverage.py` is a mkdocs build hook that walks the *assembled* docs tree. It cannot reuse `tickerlib`'s repo-root tree-walkers, but it can reuse the two pure, path-argument helpers — `front_matter(path)` and `latest_report_date(ticker_dir)`. This is a pure refactor guarded by a new characterization test written first (there are no tests on `coverage.py` today).

**Tech Stack:** Python 3.9+ stdlib (`sys`, `pathlib`, `re`), `scripts/tickerlib` (stdlib-only shared lib), pytest for tests, mkdocs for the integration check.

## Global Constraints

- **Stdlib only in `scripts/`** — `tickerlib` has no third-party deps; do not add any. Copied verbatim from the spec.
- **Python 3.9 compatible** — the scripts target 3.9; keep `from __future__ import annotations` at the top of any file using `|` type hints.
- **No behavior change** to the published site or the deterministic scripts — this is a refactor. The homepage coverage cards must render identically.
- **`tickerlib` is untouched** — only `web/hooks/coverage.py` and a new test file change.
- **Test command:** `python3 -m pytest scripts/tests/ -q` (matches CI: `python -m pytest scripts/tests/ -q`).
- **Baseline:** 40 tests pass before this work.

---

### Task 1: Characterization test for `coverage.py`

Locks in `coverage.on_config`'s current output before refactoring. Because this is a
refactor, the test is written to **pass against the current implementation** — it is
the regression net that must stay green through Task 2. `coverage.py` has no tests
today, so this is also its first coverage.

**Files:**
- Create: `scripts/tests/test_coverage.py`

**Interfaces:**
- Consumes: `coverage.on_config(config: dict) -> dict` — reads `config["docs_dir"]`, writes `config["extra"]["coverage_cards"]` (a list of card dicts with keys `sym`, `company`, `blurb`, `monitor`, `report`).
- Produces: nothing (test-only).

- [ ] **Step 1: Write the characterization test**

```python
# scripts/tests/test_coverage.py
import sys
import pathlib

# coverage.py lives in web/hooks/ and itself puts scripts/ on sys.path on import.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "web" / "hooks"))
import coverage  # noqa: E402


def _make_docs(root, sym, company, blurb, reports=()):
    """Build a minimal assembled-docs tree: docs/tickers/<sym>/news.md (+reports)."""
    d = root / "tickers" / sym
    d.mkdir(parents=True)
    (d / "news.md").write_text(
        f'---\ncompany: "{company}"\nblurb: "{blurb}"\n---\n# {sym}\n',
        encoding="utf-8",
    )
    if reports:
        (d / "reports").mkdir()
        for date in reports:
            (d / "reports" / f"{date}.md").write_text("x", encoding="utf-8")
    return root


def _run(docs_dir):
    config = {"docs_dir": str(docs_dir), "extra": {}}
    coverage.on_config(config)
    return config["extra"]["coverage_cards"]


def test_card_carries_front_matter_and_latest_report(tmp_path):
    _make_docs(tmp_path, "AAOI", "Applied Optoelectronics · NASDAQ", "an optics story",
               reports=("2026-07-14", "2026-07-17"))
    cards = _run(tmp_path)
    assert cards == [{
        "sym": "AAOI",
        "company": "Applied Optoelectronics · NASDAQ",
        "blurb": "an optics story",
        "monitor": "tickers/AAOI/news/",
        "report": "tickers/AAOI/reports/2026-07-17/",   # newest of the two
    }]


def test_card_report_is_none_when_no_reports(tmp_path):
    _make_docs(tmp_path, "WYFI", "Wyfi Corp", "no reports yet")
    cards = _run(tmp_path)
    assert cards[0]["report"] is None
    assert cards[0]["company"] == "Wyfi Corp"


def test_multiple_tickers_sorted_by_symbol(tmp_path):
    _make_docs(tmp_path, "ZZZ", "Zzz Inc", "z")
    _make_docs(tmp_path, "AAA", "Aaa Inc", "a")
    cards = _run(tmp_path)
    assert [c["sym"] for c in cards] == ["AAA", "ZZZ"]


def test_folder_without_news_md_is_skipped(tmp_path):
    _make_docs(tmp_path, "AAA", "Aaa Inc", "a")
    (tmp_path / "tickers" / "EMPTY").mkdir()  # no news.md
    cards = _run(tmp_path)
    assert [c["sym"] for c in cards] == ["AAA"]
```

- [ ] **Step 2: Run the test against the current (unchanged) `coverage.py`**

Run: `python3 -m pytest scripts/tests/test_coverage.py -v`
Expected: **PASS (4 tests)** — this characterizes existing behavior. (If any fail, the test is wrong about current behavior; fix the test, not `coverage.py`.)

- [ ] **Step 3: Run the full suite to confirm nothing else moved**

Run: `python3 -m pytest scripts/tests/ -q`
Expected: PASS (44 tests: 40 baseline + 4 new).

- [ ] **Step 4: Commit**

```bash
git add scripts/tests/test_coverage.py
git commit -m "test(coverage): characterize on_config card output before refactor"
```

---

### Task 2: Refactor `coverage.py` to reuse `tickerlib`

Replaces the local PyYAML front-matter parser and the local date-glob with calls into
`tickerlib`, removing the duplication. The Task 1 test is the guard: it must stay green.

**Files:**
- Modify: `web/hooks/coverage.py`

**Interfaces:**
- Consumes: `tickerlib.front_matter(path: pathlib.Path) -> dict` and `tickerlib.latest_report_date(ticker_dir: pathlib.Path) -> str | None`.
- Produces: `coverage.on_config` unchanged externally (same card dicts).

- [ ] **Step 1: Replace the import block**

Replace the top of `web/hooks/coverage.py` — the current lines:

```python
from __future__ import annotations

import glob
import os
import re

import yaml

_DATE_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
_FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _front_matter(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else {}


def _latest_report(ticker_dir: str, sym: str) -> str | None:
    """Newest `tickers/<SYM>/reports/<date>.md` as a site path, or None if none."""
    reports_dir = os.path.join(ticker_dir, "reports")
    dates = []
    if os.path.isdir(reports_dir):
        for entry in os.listdir(reports_dir):
            match = _DATE_FILE.match(entry)
            if match:
                dates.append(match.group(1))
    if not dates:
        return None
    return f"tickers/{sym}/reports/{max(dates)}/"  # ISO dates sort lexically
```

with:

```python
from __future__ import annotations

import glob
import os
import sys
from pathlib import Path

# Reuse the deterministic watch-list helpers instead of re-implementing the
# front-matter parser and report-date glob here. scripts/ sits at the repo root
# (parents[2] of web/hooks/coverage.py); __file__-relative so it resolves under
# whatever cwd mkdocs runs the hook from. tickerlib is stdlib-only, so this hook
# no longer needs PyYAML.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import tickerlib  # noqa: E402


def _latest_report(ticker_dir: str, sym: str) -> str | None:
    """Newest `tickers/<SYM>/reports/<date>.md` as a site path, or None if none.

    Date-finding is delegated to tickerlib; this only formats the site URL.
    """
    date = tickerlib.latest_report_date(Path(ticker_dir))
    return f"tickers/{sym}/reports/{date}/" if date else None
```

Note: `tickerlib.front_matter` handles the single-line quoted scalars the news.md
front matter uses (`company`, `blurb`). If front matter ever needs nested YAML, that
is a separate decision — `lint_news_structure` could enforce the single-line form.

- [ ] **Step 2: Point `on_config` at `tickerlib.front_matter`**

In `on_config`, change the meta line — from:

```python
        meta = _front_matter(path)
```

to:

```python
        meta = tickerlib.front_matter(Path(path))
```

Leave the rest of `on_config` (the `glob`, `sym` derivation, card assembly, `_latest_report` call) unchanged.

- [ ] **Step 3: Run the Task 1 test — it must still pass**

Run: `python3 -m pytest scripts/tests/test_coverage.py -v`
Expected: **PASS (4 tests)** — identical card output, now via `tickerlib`.

- [ ] **Step 4: Run the full suite**

Run: `python3 -m pytest scripts/tests/ -q`
Expected: PASS (44 tests).

- [ ] **Step 5: Confirm PyYAML and the old regexes are gone from the hook**

Run: `grep -nE "import yaml|_front_matter|_FRONT_MATTER|_DATE_FILE|import re" web/hooks/coverage.py`
Expected: **no output** (all removed; `re` is no longer used here either).

- [ ] **Step 6: Integration check — real mkdocs strict build**

Run: `web/scripts/build.sh --strict`
Expected: build succeeds ("Documentation built"), no strict warnings. This proves
`coverage.py` reuses `tickerlib` correctly inside the actual hook. (`site_src/` and
`site/` are gitignored — do not commit them.)

- [ ] **Step 7: Confirm the working tree is clean apart from the intended change**

Run: `git status --porcelain`
Expected: only `M web/hooks/coverage.py` (plus any gitignored build output, which
`git status` will not show).

- [ ] **Step 8: Commit**

```bash
git add web/hooks/coverage.py
git commit -m "refactor(coverage): reuse tickerlib front-matter + report resolver, drop PyYAML"
```

---

## Verification checklist (run before opening the PR)

- [ ] `python3 -m pytest scripts/tests/ -q` → 44 passed.
- [ ] `grep -nE "import yaml|_front_matter|_FRONT_MATTER|_DATE_FILE" web/hooks/coverage.py` → no output.
- [ ] `web/scripts/build.sh --strict` → builds clean; open `web/site/index.html` and confirm the Coverage grid still shows every ticker card linking to its latest report.
- [ ] `git log --oneline main..HEAD` → three commits: spec, characterization test, refactor.
- [ ] `git status --porcelain` → clean (no stray or build-output files staged).

## Notes for the implementer

- **This is a refactor, so the test is written to pass first** (Task 1), not fail — it is a characterization/regression guard. Do not "make it fail then pass"; make it lock in current behavior, then keep it green through Task 2.
- **`parents[2]`** is correct for `web/hooks/coverage.py` → repo root (`web/hooks/` is two levels down). The existing script tests use `parents[1]` because they live one level down in `scripts/tests/`; do not copy that number.
- **Do not touch `tickerlib.py`, `build.sh`, `serve.sh`, `mkdocs.yml`, or the CI workflow.** `build.sh`/`serve.sh` de-dup was explicitly deferred; the `lint.yml` `pip install pyyaml` line is harmless and out of scope.
