# Discord Notification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Post the daily watch's §B run-summary digest to a Discord channel every weekday, delivered deterministically outside the LLM session.

**Architecture:** The routine agent writes the digest to `summaries/YYYY-MM-DD.md` (frontmatter + verbatim §B body) and commits it. A GitHub Action fires on push to `summaries/**` and runs a dependency-free Python poster that builds a colored header embed, chunks the body under Discord's 2000-char limit, and POSTs to a webhook.

**Tech Stack:** Python 3 stdlib only (`urllib`, `json`, `argparse`, `re`) for the poster; pytest for tests; GitHub Actions (`actions/checkout`, `actions/setup-python`); Discord webhooks.

## Global Constraints

- Poster uses **Python 3 stdlib only** — no `requests`, no PyYAML. The Action runner has no third-party deps installed.
- Poster file is `scripts/notify_discord.py` (**underscore**, so the test module can `import` it).
- The §B digest format lives **only** in `framework/news-check.md`. This work persists and delivers that digest; it never restates or reformats the digest spec.
- Embed colors: **red `0xD9342B` (14234667)** when `tripwires_fired > 0`, else **green `0x2ECC71` (3066993)**.
- Chunk limit: **1900** chars (headroom under Discord's 2000 hard cap).
- Secret name: **`DISCORD_WEBHOOK_URL`** (GitHub Actions secret; already created).
- Default branch: `main`. Repo: `roachx92/equity-watch`. The Action must build the file URL from `${{ github.server_url }}/${{ github.repository }}/...` — no hardcoded org/repo.

---

### Task 1: Poster core — parse, chunk, embed (pure functions)

**Files:**
- Create: `scripts/notify_discord.py`
- Test: `scripts/tests/test_notify_discord.py`

**Interfaces:**
- Consumes: nothing (first task).
- Produces:
  - `RED = 0xD9342B`, `GREEN = 0x2ECC71` (module constants)
  - `parse_summary(path: str) -> tuple[dict, str]` — returns `(meta, body)`. `meta` has keys `date: str`, `tickers_checked: int`, `tripwires_fired: int`, `edge_shifts: int` (missing/invalid numeric fields default to `0`; missing `date` defaults to the filename stem). `body` is the digest text with the frontmatter block removed and surrounding blank lines stripped.
  - `build_header_embed(meta: dict, file_url: str | None = None) -> dict` — returns a Discord webhook payload `{"embeds": [ {title, description, color} ]}`.
  - `chunk(body: str, limit: int = 1900) -> list[str]` — splits on line boundaries; each chunk `<= limit`; empty body → `[]`.

- [ ] **Step 1: Ensure pytest is available**

Run: `python -m pytest --version || pip install pytest`
Expected: prints a pytest version.

- [ ] **Step 2: Write the failing tests**

Create `scripts/tests/test_notify_discord.py`:

```python
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import notify_discord as nd  # noqa: E402


SAMPLE = """---
date: 2026-07-15
tickers_checked: 5
tripwires_fired: 1      # count of [TRIPWIRE] hits this run
edge_shifts: 2          # count of EDGE+/EDGE- items this run
---
🚨 TRIPWIRES
• **CIFR Tripwire #2 — early-warning.** Hashprice down 18% WoW.

EDGE SHIFTS
• **AAOI — EDGE+.** 800G design win (2026-07-15).

PER-TICKER
2026-07-15 — [CATALYST] — **AAOI 800G win**. Digest → impact.
"""


def _write(tmp_path, text, name="2026-07-15.md"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_parse_summary_reads_frontmatter_and_body(tmp_path):
    meta, body = nd.parse_summary(_write(tmp_path, SAMPLE))
    assert meta["date"] == "2026-07-15"
    assert meta["tickers_checked"] == 5
    assert meta["tripwires_fired"] == 1
    assert meta["edge_shifts"] == 2
    assert body.startswith("🚨 TRIPWIRES")
    assert "---" not in body


def test_parse_missing_fields_default_zero_and_date_from_stem(tmp_path):
    text = "---\ntickers_checked: 3\n---\nnothing material\n"
    meta, body = nd.parse_summary(_write(tmp_path, text, "2026-07-16.md"))
    assert meta["date"] == "2026-07-16"       # from filename stem
    assert meta["tripwires_fired"] == 0        # missing → 0
    assert meta["edge_shifts"] == 0
    assert meta["tickers_checked"] == 3
    assert body == "nothing material"


def test_embed_color_red_on_tripwire():
    embed = nd.build_header_embed(
        {"date": "2026-07-15", "tickers_checked": 5,
         "tripwires_fired": 1, "edge_shifts": 2})
    assert embed["embeds"][0]["color"] == nd.RED


def test_embed_color_green_when_no_tripwire():
    embed = nd.build_header_embed(
        {"date": "2026-07-15", "tickers_checked": 5,
         "tripwires_fired": 0, "edge_shifts": 0})
    assert embed["embeds"][0]["color"] == nd.GREEN


def test_embed_counts_line_and_link():
    embed = nd.build_header_embed(
        {"date": "2026-07-15", "tickers_checked": 5,
         "tripwires_fired": 1, "edge_shifts": 2},
        file_url="https://example.com/s.md")
    desc = embed["embeds"][0]["description"]
    assert "1 tripwire" in desc and "2 edge" in desc and "5 checked" in desc
    assert "[Full run →](https://example.com/s.md)" in desc


def test_chunk_never_exceeds_limit():
    body = "\n".join(f"line {i} " + "x" * 50 for i in range(200))
    for c in nd.chunk(body, limit=200):
        assert len(c) <= 200


def test_chunk_reassembles_when_no_line_exceeds_limit():
    body = "\n".join(f"line {i}" for i in range(50))
    assert "\n".join(nd.chunk(body, limit=100)) == body


def test_chunk_empty_body_returns_empty_list():
    assert nd.chunk("", limit=1900) == []


def test_chunk_short_body_is_single_chunk():
    assert nd.chunk("hello\nworld", limit=1900) == ["hello\nworld"]
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python -m pytest scripts/tests/test_notify_discord.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'notify_discord'`.

- [ ] **Step 4: Write the minimal implementation**

Create `scripts/notify_discord.py`:

```python
#!/usr/bin/env python3
"""Post a daily-watch summary file to a Discord webhook.

Reads summaries/<date>.md (frontmatter + §B digest body), builds a colored
header embed, chunks the body under Discord's message limit, and POSTs.
Python 3 stdlib only — runs on a bare GitHub Actions runner.
"""
import re
from pathlib import Path

RED = 0xD9342B
GREEN = 0x2ECC71

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def parse_summary(path):
    text = Path(path).read_text(encoding="utf-8")
    meta_raw, body = {}, text
    m = _FRONTMATTER.match(text)
    if m:
        fm, body = m.group(1), m.group(2)
        for line in fm.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta_raw[key.strip()] = val.split("#", 1)[0].strip()

    def as_int(key):
        try:
            return int(meta_raw.get(key, 0))
        except ValueError:
            return 0

    meta = {
        "date": meta_raw.get("date") or Path(path).stem,
        "tickers_checked": as_int("tickers_checked"),
        "tripwires_fired": as_int("tripwires_fired"),
        "edge_shifts": as_int("edge_shifts"),
    }
    return meta, body.strip("\n")


def build_header_embed(meta, file_url=None):
    color = RED if meta["tripwires_fired"] > 0 else GREEN
    counts = (
        f'{meta["tripwires_fired"]} tripwire(s) · '
        f'{meta["edge_shifts"]} edge shift(s) · '
        f'{meta["tickers_checked"]} checked'
    )
    description = counts
    if file_url:
        description += f"\n[Full run →]({file_url})"
    return {
        "embeds": [{
            "title": f'Daily Watch — {meta["date"]}',
            "description": description,
            "color": color,
        }]
    }


def chunk(body, limit=1900):
    chunks, cur = [], ""
    for line in body.split("\n"):
        while len(line) > limit:            # a single over-long line: hard split
            if cur:
                chunks.append(cur)
                cur = ""
            chunks.append(line[:limit])
            line = line[limit:]
        candidate = line if not cur else cur + "\n" + line
        if len(candidate) <= limit:
            cur = candidate
        else:
            chunks.append(cur)
            cur = line
    if cur:
        chunks.append(cur)
    return chunks
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python -m pytest scripts/tests/test_notify_discord.py -v`
Expected: PASS (8 passed).

- [ ] **Step 6: Commit**

```bash
git add scripts/notify_discord.py scripts/tests/test_notify_discord.py
git commit -m "feat: notify-discord poster core (parse, chunk, embed)"
```

---

### Task 2: Poster CLI — posting, dry-run, 429 retry

**Files:**
- Modify: `scripts/notify_discord.py` (append `post`, `main`, `__main__` guard + imports)
- Test: `scripts/tests/test_notify_discord.py` (add dry-run smoke test)

**Interfaces:**
- Consumes: `parse_summary`, `build_header_embed`, `chunk` from Task 1.
- Produces:
  - `post(webhook_url: str, payload: dict) -> int` — POSTs one payload as JSON; on HTTP 429 sleeps `Retry-After` and retries (up to 5); returns HTTP status.
  - `main(argv: list[str] | None = None) -> int` — CLI: `notify_discord.py <summary> [--file-url URL] [--dry-run]`. Builds `[header_embed] + [{"content": c} for c in chunk(body)]`. `--dry-run` prints one JSON payload per line and posts nothing (exit 0). Otherwise reads `DISCORD_WEBHOOK_URL` from env (exit 1 if unset) and POSTs each message with a 0.6s gap.

- [ ] **Step 1: Write the failing test**

Add to `scripts/tests/test_notify_discord.py`:

```python
def test_dry_run_prints_header_and_chunks_without_network(tmp_path, capsys):
    p = _write(tmp_path, SAMPLE)
    rc = nd.main([p, "--file-url", "https://example.com/s.md", "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) >= 2                      # header embed + >=1 body chunk
    import json
    header = json.loads(lines[0])
    assert header["embeds"][0]["title"] == "Daily Watch — 2026-07-15"
    assert json.loads(lines[1])["content"].startswith("🚨 TRIPWIRES")


def test_main_missing_webhook_env_returns_1(tmp_path, monkeypatch):
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    rc = nd.main([_write(tmp_path, SAMPLE)])   # no --dry-run, no env
    assert rc == 1
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest scripts/tests/test_notify_discord.py -k "dry_run or missing_webhook" -v`
Expected: FAIL — `AttributeError: module 'notify_discord' has no attribute 'main'`.

- [ ] **Step 3: Implement the CLI**

Add to the top of `scripts/notify_discord.py` imports:

```python
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
```

Append to `scripts/notify_discord.py`:

```python
def post(webhook_url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url, data=data, headers={"Content-Type": "application/json"})
    for _ in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                time.sleep(float(exc.headers.get("Retry-After", "1")))
                continue
            raise
    raise RuntimeError("Discord POST failed after retries (HTTP 429)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Post a summary file to Discord.")
    ap.add_argument("summary", help="path to summaries/<date>.md")
    ap.add_argument("--file-url", default=None, help="URL for the 'Full run →' link")
    ap.add_argument("--dry-run", action="store_true", help="print payloads, do not post")
    args = ap.parse_args(argv)

    meta, body = parse_summary(args.summary)
    messages = [build_header_embed(meta, args.file_url)]
    messages += [{"content": c} for c in chunk(body)]

    if args.dry_run:
        for msg in messages:
            print(json.dumps(msg, ensure_ascii=False))
        return 0

    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("DISCORD_WEBHOOK_URL not set", file=sys.stderr)
        return 1

    for i, msg in enumerate(messages):
        post(webhook, msg)
        if i < len(messages) - 1:
            time.sleep(0.6)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run all tests to verify they pass**

Run: `python -m pytest scripts/tests/test_notify_discord.py -v`
Expected: PASS (10 passed).

- [ ] **Step 5: Manual integration check (throwaway webhook)**

Create a temp fixture and post to a **test** Discord channel's webhook:

```bash
DISCORD_WEBHOOK_URL='<your-TEST-webhook>' \
  python scripts/notify_discord.py reports/README.md --file-url https://example.com --dry-run
# then, against a disposable test channel only:
DISCORD_WEBHOOK_URL='<your-TEST-webhook>' \
  python scripts/notify_discord.py <a-real-summary-fixture>.md --file-url https://example.com
```
Expected (dry-run): JSON payloads print. Expected (live): a green/red header embed + body message appear in the test channel.

- [ ] **Step 6: Commit**

```bash
git add scripts/notify_discord.py scripts/tests/test_notify_discord.py
git commit -m "feat: notify-discord CLI with dry-run and 429 retry"
```

---

### Task 3: GitHub Action — post newly added summaries on push

**Files:**
- Create: `.github/workflows/notify-discord.yml`

**Interfaces:**
- Consumes: `scripts/notify_discord.py` (Task 2), secret `DISCORD_WEBHOOK_URL`.
- Produces: a `push` workflow that, for each summary file **added** in the push, posts it to Discord.

- [ ] **Step 1: Write the workflow**

Create `.github/workflows/notify-discord.yml`:

```yaml
name: Notify Discord

on:
  push:
    branches: [main]
    paths:
      - 'summaries/**'

permissions:
  contents: read

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout (with previous commit for diff)
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Post newly added summaries to Discord
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: |
          set -euo pipefail
          before='${{ github.event.before }}'
          after='${{ github.sha }}'
          if [ -z "$before" ] || [ "$before" = "0000000000000000000000000000000000000000" ]; then
            base="HEAD^"
          else
            base="$before"
          fi
          added=$(git diff --name-only --diff-filter=A "$base" "$after" -- 'summaries/**' || true)
          if [ -z "$added" ]; then
            echo "No newly added summaries in this push; nothing to post."
            exit 0
          fi
          echo "Newly added summaries:"; echo "$added"
          printf '%s\n' "$added" | while IFS= read -r f; do
            [ -n "$f" ] || continue
            url="${{ github.server_url }}/${{ github.repository }}/blob/${{ github.sha }}/$f"
            python scripts/notify_discord.py "$f" --file-url "$url"
          done
```

- [ ] **Step 2: Validate the YAML parses**

Run: `python -c "import yaml, sys; yaml.safe_load(open('.github/workflows/notify-discord.yml')); print('valid')"`
Expected: prints `valid`. (If PyYAML is absent locally: `pip install pyyaml` first — this is a local check only, not a runtime dep.)

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/notify-discord.yml
git commit -m "feat: notify-discord GitHub Action on summaries/** push"
```

- [ ] **Step 4: Live end-to-end verification (after merge)**

After this branch merges to `main`, add a hand-written `summaries/<today>.md` (frontmatter + a couple of digest lines) and push it. Confirm the Action runs (Actions tab) and a message lands in the real Discord channel. Then delete the test file or leave it as the first real entry.

---

### Task 4: `daily-watch.md` — write the summary file each run

**Files:**
- Modify: `daily-watch.md` (the Task list, currently steps 6–8, and the "Run summary" section)

**Interfaces:**
- Consumes: nothing in code; instructs the routine agent to produce `summaries/<date>.md`.
- Produces: the file the Action (Task 3) consumes.

- [ ] **Step 1: Restructure the Task steps**

In `daily-watch.md`, replace the current steps 6–8 (`Commit & push` / `Produce the run summary` / `Per-ticker Edge & Tripwires recap`) with this ordering so the summary file exists before the commit:

```markdown
6. **Produce the run summary** — the chat digest in the canonical §B format
   (`framework/news-check.md`), TRIPWIRES FIRST, including the conditional
   per-ticker Edge & Tripwires recap. This same digest is both your chat output
   and the body of the summary file in the next step.
7. **Write the summary file** — write the digest to `summaries/<today>.md`,
   prefixed with a YAML frontmatter block, then the verbatim §B digest body:

       ---
       date: <today>
       tickers_checked: <count of tickers/*.md scanned this run>
       tripwires_fired: <count of [TRIPWIRE] hits this run>
       edge_shifts: <count of [EDGE+]/[EDGE−] items this run>
       ---
       <the §B digest, exactly as produced in step 6>

   Write this file **every run**, even when nothing material was found (the body
   then carries the §B "nothing material" content and the counts are `0`) — it is
   the daily heartbeat that drives the Discord post. Do not restate the §B format
   here; `framework/news-check.md` §B is its single source.
8. **Commit & push** the updated ticker files **and** `summaries/<today>.md` with
   a message `daily watch: <today's date>`. Because the summary file is new every
   run, this commit always happens (unlike before, when it was skipped on a
   no-change day). The push triggers the Discord notification Action.
```

- [ ] **Step 2: Update the "Run summary" section pointer**

In the `## Run summary` section of `daily-watch.md`, append one sentence:

```markdown
The same digest is persisted verbatim (with a frontmatter counts block) to
`summaries/<today>.md` in step 7 above; a GitHub Action posts that file to
Discord on push. The digest format remains defined only in
`framework/news-check.md` §B.
```

- [ ] **Step 3: Verify the doc reads coherently**

Run: `git diff daily-watch.md`
Expected: steps 6–8 reordered as above; run-summary section gains the persistence sentence; no other steps disturbed.

- [ ] **Step 4: Commit**

```bash
git add daily-watch.md
git commit -m "docs: daily-watch writes summaries/<date>.md for Discord notify"
```

---

### Task 5: Repo docs — file map, backlog, §B pointer

**Files:**
- Modify: `CLAUDE.md` (File map)
- Modify: `docs/part-2-scripts-plan.md` (backlog)
- Modify: `framework/news-check.md` (§B, one-line pointer)

**Interfaces:**
- Consumes: the components built in Tasks 1–4.
- Produces: documentation only.

- [ ] **Step 1: Add to the `CLAUDE.md` File map**

Under `## File map`, add these bullets (after the `tickers/*.md` bullet):

```markdown
- `summaries/<YYYY-MM-DD>.md` — per-run persisted copy of the §B run-summary
  digest (frontmatter counts + digest body), written by `daily-watch.md` each
  run. Consumed by the Discord notification Action; also the daily heartbeat.
- `scripts/notify_discord.py` — dependency-free poster: parses a summary file,
  builds a colored header embed, chunks the body under Discord's limit, POSTs to
  the `DISCORD_WEBHOOK_URL` webhook. Locally runnable with `--dry-run`.
- `.github/workflows/notify-discord.yml` — on push to `summaries/**`, posts each
  newly added summary to Discord via the poster.
```

- [ ] **Step 2: Mark the backlog item done in `docs/part-2-scripts-plan.md`**

Add a new numbered item under `## Backlog` (or a "Done" note):

```markdown
6. **Discord notification of the run summary. — DONE.** The daily watch writes
   its §B digest to `summaries/<date>.md`; `.github/workflows/notify-discord.yml`
   fires on push and `scripts/notify_discord.py` posts a colored header embed +
   chunked body to a Discord webhook (`DISCORD_WEBHOOK_URL` secret). Deterministic
   plumbing outside the LLM session — the dividing-line pattern in action.
```

- [ ] **Step 3: Add the §B persistence pointer in `framework/news-check.md`**

At the end of the `## B. Run-summary output format` section, append:

```markdown
> The daily watch persists this exact digest to `summaries/<date>.md` (with a
> frontmatter counts block) so a GitHub Action can post it to Discord. That is a
> delivery concern only — this section remains the single source of the digest
> format; the summary file body **is** this digest, unmodified.
```

- [ ] **Step 4: Verify and commit**

Run: `git diff --stat CLAUDE.md docs/part-2-scripts-plan.md framework/news-check.md`
Expected: three files changed, additions only.

```bash
git add CLAUDE.md docs/part-2-scripts-plan.md framework/news-check.md
git commit -m "docs: record Discord notify in file map, backlog, and §B"
```

---

## Self-Review

**Spec coverage:**
- §1 summary file + frontmatter → Task 4 (agent writes it), Task 1 (`parse_summary`).
- §2 daily-watch step → Task 4.
- §3 Action (trigger, added-only guard, first-push fallback, file URL) → Task 3.
- §4 poster (embed color, counts+link, chunk, dry-run, 429) → Tasks 1–2.
- §5 secret → Global Constraints + Task 3 env (setup already done by user).
- Testing (chunker TDD, embed color, dry-run smoke) → Tasks 1–2.
- Docs updates → Task 5.
- Out-of-scope (site publish, mentions) → intentionally omitted.

**Placeholder scan:** No TBD/TODO; every code step shows full code; test bodies are concrete.

**Type consistency:** `parse_summary → (meta, body)`, `build_header_embed(meta, file_url)`, `chunk(body, limit)`, `post(url, payload)`, `main(argv)` used identically across Tasks 1–3. Colors `RED`/`GREEN` defined in Task 1, referenced in Task 1 tests only. File named `notify_discord.py` consistently in poster, tests, Action, and docs.

**Deviation from spec:** filename is `notify_discord.py` (underscore) rather than `notify-discord.py` (hyphen), so the pytest module can import it. The workflow file remains `notify-discord.yml`. Noted in Global Constraints.
