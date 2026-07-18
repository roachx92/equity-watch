import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import resolve_report as rr  # noqa: E402
import tickerlib as tl  # noqa: E402

# A news.md whose canonical line ALSO references an older report in prose — the
# fix must rewrite only the backtick pointer, never the prose link.
NEWS = """---
company: "ABC Co"
blurb: "b"
---
# ABC

**Canonical deep-dive:** [`reports/{ptr}.md`](reports/{ptr}.md) (re-run {ptr}; \
supersedes the immutable [2026-07-14](reports/2026-07-14.md) snapshot).

## Recent News Log
"""


def _mk(root, sym, ptr, reports):
    d = root / "tickers" / sym
    (d / "reports").mkdir(parents=True)
    for date in reports:
        (d / "reports" / f"{date}.md").write_text("x", encoding="utf-8")
    (d / "news.md").write_text(NEWS.format(ptr=ptr), encoding="utf-8")
    return d


def test_pointer_date_reads_backtick_pointer_not_prose():
    ptr, idx = rr._pointer_date(NEWS.format(ptr="2026-07-17"))
    assert ptr == "2026-07-17"          # not the prose 2026-07-14 link
    assert idx is not None


def test_check_reports_ok_when_pointer_matches(tmp_path):
    _mk(tmp_path, "ABC", ptr="2026-07-17", reports=("2026-07-14", "2026-07-17"))
    rows = rr.check(tmp_path)
    assert rows == [("ABC", "2026-07-17", "2026-07-17", "ok")]


def test_check_detects_drift(tmp_path):
    _mk(tmp_path, "ABC", ptr="2026-07-14", reports=("2026-07-14", "2026-07-17"))
    rows = rr.check(tmp_path)
    assert rows[0][3] == "drift"


def test_fix_rewrites_only_the_pointer(tmp_path):
    d = _mk(tmp_path, "ABC", ptr="2026-07-14", reports=("2026-07-14", "2026-07-17"))
    fixed = rr.fix(tmp_path)
    assert fixed == ["ABC"]
    text = (d / "news.md").read_text(encoding="utf-8")
    assert "[`reports/2026-07-17.md`](reports/2026-07-17.md)" in text  # pointer updated
    assert "[2026-07-14](reports/2026-07-14.md)" in text               # prose link untouched
    assert rr.check(tmp_path)[0][3] == "ok"                             # now clean


def test_check_flags_missing_pointer(tmp_path):
    d = _mk(tmp_path, "ABC", ptr="2026-07-17", reports=("2026-07-17",))
    (d / "news.md").write_text("---\ncompany: x\nblurb: y\n---\n# ABC\n", encoding="utf-8")
    assert rr.check(tmp_path)[0][3] == "no-pointer"


def test_agrees_with_coverage_hook_on_real_tree():
    """Guard the two newest-report implementations against drift."""
    import importlib.util
    import pytest
    pytest.importorskip("yaml")
    root = tl.repo_root()
    hook = root / "web" / "hooks" / "coverage.py"
    if not hook.is_file():
        pytest.skip("coverage hook not present")
    spec = importlib.util.spec_from_file_location("coverage_hook", hook)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for d in tl.ticker_dirs(root):
        mine = tl.latest_report_date(d)
        theirs = mod._latest_report(str(d), d.name)
        if mine is None:
            assert theirs is None
        else:
            assert theirs == f"tickers/{d.name}/reports/{mine}/"
