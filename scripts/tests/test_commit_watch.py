import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import commit_watch as cw  # noqa: E402


def test_staged_targets_includes_summary_when_present(tmp_path):
    (tmp_path / "summaries").mkdir()
    (tmp_path / "summaries" / "2026-07-18.md").write_text("x", encoding="utf-8")
    targets = cw.staged_targets(tmp_path, "2026-07-18")
    assert "tickers/*/news.md" in targets
    assert "summaries/2026-07-18.md" in targets


def test_staged_targets_omits_missing_summary(tmp_path):
    targets = cw.staged_targets(tmp_path, "2026-07-18")
    assert targets == ["tickers/*/news.md"]


def test_dry_run_runs_no_mutating_git(tmp_path, monkeypatch, capsys):
    calls = []

    def fake_git(root, *args):
        calls.append(args)
        return ""  # status --porcelain returns nothing

    monkeypatch.setattr(cw, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(cw, "_git", fake_git)
    rc = cw.main(["--date", "2026-07-18", "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "daily watch: 2026-07-18" in out
    # dry-run may inspect status, but must never add/commit/push
    assert all(a[0] not in ("add", "commit", "push") for a in calls)


def test_main_skips_commit_when_nothing_staged(tmp_path, monkeypatch, capsys):
    def fake_git(root, *args):
        if args[:2] == ("diff", "--cached"):
            return ""  # nothing staged
        return ""

    monkeypatch.setattr(cw, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(cw, "_git", fake_git)
    rc = cw.main(["--date", "2026-07-18", "--no-push"])
    assert rc == 0
    assert "nothing staged" in capsys.readouterr().out


def test_main_commits_and_pushes(tmp_path, monkeypatch):
    calls = []

    def fake_git(root, *args):
        calls.append(args[0])
        if args[:2] == ("diff", "--cached"):
            return "tickers/ABC/news.md\n"  # something staged
        return ""

    monkeypatch.setattr(cw, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(cw, "_git", fake_git)
    assert cw.main(["--date", "2026-07-18"]) == 0
    assert "commit" in calls and "push" in calls


def test_main_no_push_flag_skips_push(tmp_path, monkeypatch):
    calls = []

    def fake_git(root, *args):
        calls.append(args[0])
        if args[:2] == ("diff", "--cached"):
            return "tickers/ABC/news.md\n"
        return ""

    monkeypatch.setattr(cw, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(cw, "_git", fake_git)
    assert cw.main(["--date", "2026-07-18", "--no-push"]) == 0
    assert "commit" in calls and "push" not in calls
