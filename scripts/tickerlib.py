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
_ENTRY_BULLET = re.compile(r"^-\s+(\d{4}-\d{2}-\d{2})")
_CANONICAL_LINK = re.compile(r"\*\*Canonical deep-dive:\*\*.*?(\d{4}-\d{2}-\d{2})\.md")

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
    """The leading `YYYY-MM-DD` of a log entry line, or None."""
    match = _ENTRY_BULLET.match(line)
    return match.group(1) if match else None


def canonical_report_date(news_text: str) -> str | None:
    """The date in the `**Canonical deep-dive:**` link, or None if absent.

    Compared against `latest_report_date()` to detect pointer drift — the link
    is a written pointer someone set at a point in time (CLAUDE.md), so it can
    go stale and must never be trusted as the resolver.
    """
    match = _CANONICAL_LINK.search(news_text)
    return match.group(1) if match else None


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
