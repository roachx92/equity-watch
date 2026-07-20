"""Shared helpers for the deterministic watch-list scripts — stdlib only.

The watch-list is the `tickers/*/` directory glob (see CLAUDE.md): one folder
per ticker, each holding a `news.md`. These helpers give the resolver, the
linters, and the count/commit plumbing a single place to enumerate that tree and
resolve the newest deep-dive report, so the glob-and-max logic is not re-written
per script.

Runs on a bare runner — no third-party deps (that is why this does not use
PyYAML the way `web/hooks/coverage.py` does; front-matter parsing here is the
minimal line form the news.md files actually use).
"""
from __future__ import annotations

import re
from pathlib import Path

_DATE_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
_FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)

_LOG_HEADER = "## Recent News Log"
_ENTRY_BULLET = re.compile(
    r"^-\s+(\d{4}-\d{2}-\d{2})(?:\s+to\s+(\d{4}-\d{2}-\d{2}))?"
)
_CANONICAL_LINK = re.compile(r"\*\*Canonical deep-dive:\*\*.*?(\d{4}-\d{2}-\d{2})\.md")

#: The closed sector vocabulary (§K.2). Closed for the same reason §F.1's tag
#: vocabulary is: an open one drifts, and the corpus already shows what that
#: looks like (`Catalyst/Re-rate driver` vs `Catalysts/Re-rate drivers` vs
#: `Sentiment/Re-rate drivers` all coexist as framework tags today). Adding a
#: slug is a deliberate act: define it in framework/sector-lens.md §K.2 in the
#: same commit that first uses it.
SECTOR_SLUGS = (
    "adv-packaging",
    "ai-dc-lessor",
    "ai-optics",
    "btc-mining",
    "catv-broadband",
)
_SECTOR_HEADER = "## Sector lens"
#: A membership bullet opens bold, then the slug in backticks:
#: ``- **`ai-optics` — sole.** …``. The trailing role/prose is free text. The
#: "not a sector" / "deliberately excluded" notes each ticker carries open bold
#: with a *word* rather than a backtick, so they correctly do not match.
_SECTOR_BULLET = re.compile(r"^-\s+\*\*`([a-z0-9-]+)`")

_TRIPWIRE_HEADER = "## Tripwires"
_TRIPWIRE_MARKER = re.compile(r"\((\d+)\)")
#: An `| # | Expires |` table row — trigger number, then an optional date (blank
#: cell = tracked but undated). Not the prose: the trigger text stays verbatim
#: from the report, so expiry lives in its own field rather than as an inline
#: annotation buried mid-sentence.
_EXPIRES_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})?\s*\|", re.MULTILINE
)

# --- Assessment-tag grammar (§F.1) -----------------------------------------
# Shared by lint_news_log.py and the staleness audit, so both classify a tag
# identically. Polarity is what routing keys off, so misclassifying is
# expensive: a tripwire that says "does not fire" must never read as fired.

#: Any dash a writer might use where §F.1 specifies one.
_DASHES = "—–−-"  # em, en, true-minus, hyphen
_TAG = re.compile(r"\[(TRIPWIRE|EDGE)([^\]]*)\]")
_TRIPWIRE_NUM = re.compile(r"#\s*(\d+)")

#: Canonical tripwire statuses → polarity. Order matters: the first substring
#: match wins, so "does not fire" is tested before the bare "fire".
_TRIPWIRE_STATUS = (
    ("does not fire", "not-fired"),
    ("not sustained", "not-fired"),
    ("checked", "not-fired"),
    ("early-warning", "early-warning"),
    ("live, unresolved", "early-warning"),
    ("fires", "fired"),
    ("fired", "fired"),
)

#: Legacy status spellings accepted on read but flagged for canonicalisation.
_TRIPWIRE_LEGACY = ("not sustained", "live, unresolved", "checked")


def parse_assessment_tags(line: str) -> list[dict]:
    """Classify every `[TRIPWIRE …]` / `[EDGE …]` tag on one log-entry line.

    Returns one dict per tag: ``kind`` (TRIPWIRE|EDGE), ``polarity``,
    ``number`` (tripwires), ``raw``, and ``legacy`` (True when the spelling is
    accepted but non-canonical).

    **Polarity defaults to the cheaper/safer value when a status is
    unrecognised** — ``None`` — so an unparseable tag never routes a caller to
    the expensive branch on its own. Callers must surface ``polarity is None``
    rather than silently treating it as a fire.
    """
    out: list[dict] = []
    for kind, body in _TAG.findall(line):
        raw, rest = f"[{kind}{body}]", body.strip()
        if kind == "EDGE":
            # §F.1: edges are BINARY — [EDGE+] or [EDGE−], no neutral, no
            # qualifiers. "neutral" exists here only to classify legacy corpus
            # entries ("[EDGE — live test, unresolved]") without hard-failing
            # them; it is not a writable form and routes to nothing.
            sign = rest[:1]
            if sign == "+":
                polarity = "positive"
                legacy = "," in rest  # e.g. "[EDGE+, tangential]" — qualifier dropped
            elif sign in "−-–—~" and sign:
                if "live test" in rest.lower() or sign == "~":
                    polarity, legacy = "neutral", True  # legacy only
                else:
                    # A leading dash is the minus sign; U+2212 is canonical.
                    polarity, legacy = "negative", sign != "−"
            else:
                polarity, legacy = None, False  # bare [EDGE] or unknown — undefined
            out.append({"kind": "EDGE", "polarity": polarity, "number": None,
                        "raw": raw, "legacy": legacy})
            continue

        num = _TRIPWIRE_NUM.search(rest)
        low = rest.lower()
        polarity = next((p for token, p in _TRIPWIRE_STATUS if token in low), None)
        out.append({
            "kind": "TRIPWIRE",
            "polarity": polarity,
            "number": int(num.group(1)) if num else None,
            "raw": raw,
            "legacy": any(t in low for t in _TRIPWIRE_LEGACY),
        })
    return out


def repo_root() -> Path:
    """Repo root, resolved from this file's location (scripts/ sits at the root)."""
    return Path(__file__).resolve().parents[1]


def ticker_dirs(root: Path | None = None) -> list[Path]:
    """Every `tickers/<SYM>/` folder, sorted — the watch-list, half-created or not."""
    root = root or repo_root()
    tickers = root / "tickers"
    if not tickers.is_dir():
        return []
    return sorted(p for p in tickers.iterdir() if p.is_dir())


def news_files(root: Path | None = None) -> list[Path]:
    """Every `tickers/<SYM>/news.md` that exists, sorted by symbol."""
    return [d / "news.md" for d in ticker_dirs(root) if (d / "news.md").is_file()]


def front_matter(path: Path) -> dict:
    """Parse the leading `---` block into a flat {key: value} dict.

    Stdlib-only: handles the one-line `key: "value"` form the news.md front
    matter uses (company, blurb). Not a general YAML parser.
    """
    text = Path(path).read_text(encoding="utf-8")
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
            val = val[1:-1]
        data[key.strip()] = val
    return data


def log_entries(text: str) -> list[tuple[int, str]]:
    """(1-based line number, line) for each bullet in the Recent News Log section.

    Scoped to lines *under* the `## Recent News Log` heading on purpose: every
    news.md carries a header note that documents the tag format, and a naive
    whole-file scan reads those examples as real tagged entries.
    """
    lines = text.splitlines()
    out, in_section = [], False
    for i, line in enumerate(lines, start=1):
        if line.startswith("## "):
            in_section = line.strip() == _LOG_HEADER
            continue
        if in_section and _ENTRY_BULLET.match(line):
            out.append((i, line))
    return out


def entry_date(line: str) -> str | None:
    """A log entry's effective date for staleness purposes, or None.

    §F.1 entries may be a single date or a `DATE to DATE` range (e.g. an
    event that unfolded over several days). The *end* date is what matters —
    a range's content is "as of" its later date, so a range starting before
    a report but ending after it is genuinely post-report information, not
    pre-report. Keying off the leading date alone made such an entry (and
    any [EDGE-]/tripwire tag on it) invisible to the staleness audit whenever
    its start predated the baseline even though its end postdated it.
    """
    match = _ENTRY_BULLET.match(line)
    if not match:
        return None
    return match.group(2) or match.group(1)


def canonical_report_date(news_text: str) -> str | None:
    """The date in the `**Canonical deep-dive:**` link, or None if absent.

    Compared against `latest_report_date()` to detect pointer drift — the link
    is a written pointer someone set at a point in time (CLAUDE.md), so it can
    go stale and must never be trusted as the resolver.
    """
    match = _CANONICAL_LINK.search(news_text)
    return match.group(1) if match else None


def sector_slugs(news_text: str) -> list[str]:
    """Sector slugs a ticker is assigned to, from its `## Sector lens` section.

    Reads the membership bullets (``- **`slug`** …``) and ignores the prose
    around them, so the "deliberately excluded" / "not a sector" notes each
    ticker carries — which explain what was considered and rejected — do not
    read as memberships. Returns slugs in document order; validation against
    `SECTOR_SLUGS` is the linter's job, not this parser's.
    """
    out: list[str] = []
    in_section = False
    for line in news_text.splitlines():
        if line.startswith("## "):
            in_section = line.strip().startswith(_SECTOR_HEADER)
            continue
        if not in_section:
            continue
        match = _SECTOR_BULLET.match(line)
        if match and match.group(1) not in out:
            out.append(match.group(1))
    return out


def tripwire_expiries(news_text: str) -> dict[int, str]:
    """{tripwire number: expiry date} from the `| # | Expires |` table.

    Scoped to the `## Tripwires` section. The numbered triggers `(n)` in the
    prose (which stays verbatim from the report — never rewritten to carry a
    date inline) establish which numbers exist; a small table below the prose
    carries each one's date in its own field: `| 1 | 2027-03-31 |`. A trigger
    with no row, or a row with a blank date cell, is tracked-but-undated
    (returns ""), which the audit surfaces rather than guessing a window.

    Expiry means the trigger's own window has closed — the event it watched
    has resolved or its premise has lapsed — NOT that it fired. An expired
    tripwire still on the watch-list is dead weight that reads as coverage,
    which is worse than an empty slot.
    """
    lines = news_text.splitlines()
    section: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("## "):
            in_section = line.strip().startswith(_TRIPWIRE_HEADER)
            continue
        # Stop at any `###` subheading — notably `### Change log` (§J.4), which
        # lives inside `## Tripwires` but is free prose about *past* changes.
        # Scoping it out structurally means a change-log line may say anything,
        # including a parenthesised number, without being read as a trigger.
        if line.startswith("### "):
            in_section = False
            continue
        if in_section:
            section.append(line)
    text = "\n".join(section)

    # Which trigger numbers exist, from the prose markers (1..k in order; a
    # stray out-of-sequence parenthesised number in free text is skipped).
    numbers: list[int] = []
    for m in _TRIPWIRE_MARKER.finditer(text):
        n = int(m.group(1))
        if n == len(numbers) + 1:
            numbers.append(n)

    dates = {int(m.group(1)): (m.group(2) or "") for m in _EXPIRES_ROW.finditer(text)}
    return {n: dates.get(n, "") for n in numbers}


def latest_report_date(ticker_dir: Path) -> str | None:
    """Newest `tickers/<SYM>/reports/<YYYY-MM-DD>.md` date, or None if none.

    ISO dates sort lexically, so `max()` is the newest — same rule as
    `web/hooks/coverage.py._latest_report`.
    """
    reports_dir = ticker_dir / "reports"
    if not reports_dir.is_dir():
        return None
    dates = [
        m.group(1)
        for entry in reports_dir.iterdir()
        for m in [_DATE_FILE.match(entry.name)]
        if m
    ]
    return max(dates) if dates else None
