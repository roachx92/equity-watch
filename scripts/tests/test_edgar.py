"""Tests for scripts/edgar.py — all offline; `_get` is monkeypatched throughout.

The load-bearing behaviour is that a request is always *identified*. An
unidentified request is what EDGAR 403s on, and those 403s are why two research
passes had to downgrade "no filings this window" to an aggregator-sourced claim.
"""
import sys
import pathlib

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import edgar  # noqa: E402

TICKER_INDEX = {
    "0": {"cik_str": 820318, "ticker": "COHR", "title": "COHERENT CORP."},
    "1": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
}

SUBMISSIONS = {
    "name": "COHERENT CORP.",
    "sicDescription": "Semiconductors",
    "fiscalYearEnd": "0630",
    "exchanges": ["NYSE"],
    "filings": {
        "recent": {
            "filingDate": ["2026-07-24", "2026-07-22", "2026-07-08", "2026-05-06"],
            "form": ["4", "144", "SCHEDULE 13G/A", "10-Q"],
            "accessionNumber": [
                "0000899140-26-000726",
                "0001950047-26-007261",
                "0000315066-26-001472",
                "0000820318-26-000013",
            ],
            "primaryDocument": ["x.xml", "y.htm", "z.htm", "q.htm"],
            "reportDate": ["2026-07-22", "", "", "2026-03-31"],
            "primaryDocDescription": ["FORM 4", "144", "13G/A", "10-Q"],
        }
    },
}


@pytest.fixture
def wired(monkeypatch):
    """Route _get to fixtures so no test touches the network."""
    def fake(url, timeout=25):
        if url == edgar._TICKERS_URL:
            return TICKER_INDEX
        if "submissions" in url:
            return SUBMISSIONS
        raise AssertionError(f"unexpected URL {url}")
    monkeypatch.setattr(edgar, "_get", fake)


def test_identity_prefers_env(monkeypatch):
    monkeypatch.setenv("EDGAR_IDENTITY", "Jane Doe jane@example.com")
    assert edgar.identity() == "Jane Doe jane@example.com"


def test_identity_falls_back_to_a_nonempty_ua(monkeypatch):
    """Never send an empty UA — that is precisely what EDGAR 403s on."""
    monkeypatch.delenv("EDGAR_IDENTITY", raising=False)
    assert edgar.identity().strip()


def test_request_always_carries_a_user_agent(monkeypatch):
    """Regression guard for the 403 class: assert the header is actually set."""
    seen = {}

    class FakeResp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return b"{}"

    def fake_urlopen(req, timeout=25):
        seen["ua"] = req.get_header("User-agent")
        return FakeResp()

    monkeypatch.setattr(edgar.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(edgar.json, "load", lambda f: {})
    edgar._get("https://data.sec.gov/anything")
    assert seen["ua"], "request went out with no User-Agent"


def test_resolve_cik(wired):
    assert edgar.resolve_cik("COHR") == 820318
    assert edgar.resolve_cik("cohr") == 820318


def test_resolve_cik_unknown_ticker_explains_itself(wired):
    with pytest.raises(edgar.EdgarError) as exc:
        edgar.resolve_cik("NOPE")
    assert "may not be an SEC filer" in str(exc.value)


def test_filings_returns_all_by_default(wired):
    rows, meta = edgar.filings("COHR")
    assert len(rows) == 4
    assert meta["cik"] == 820318
    assert meta["name"] == "COHERENT CORP."


def test_since_filters_the_window(wired):
    """The exact query the 2026-07-29 run could not answer from primary source."""
    rows, _ = edgar.filings("COHR", since="2026-07-27")
    assert rows == []


def test_since_is_inclusive_on_the_boundary(wired):
    rows, _ = edgar.filings("COHR", since="2026-07-24")
    assert [r["date"] for r in rows] == ["2026-07-24"]


def test_form_filter_is_case_insensitive(wired):
    rows, _ = edgar.filings("COHR", forms=["10-q"])
    assert len(rows) == 1
    assert rows[0]["form"] == "10-Q"


def test_filing_url_is_built_from_accession(wired):
    rows, _ = edgar.filings("COHR", forms=["10-Q"])
    url = rows[0]["url"]
    assert "000082031826000013" in url  # dashes stripped
    assert url.endswith("/q.htm")


def test_limit_caps_results(wired):
    rows, _ = edgar.filings("COHR", limit=2)
    assert len(rows) == 2


def test_empty_window_says_it_was_verified_directly(wired):
    """The message must distinguish a primary-source check from an aggregator gap."""
    rows, meta = edgar.filings("COHR", since="2026-07-27")
    out = edgar.render("COHR", rows, meta, "2026-07-27")
    assert "No filings on/after 2026-07-27" in out
    assert "data.sec.gov" in out


def test_non_sec_filer_short_circuits_without_network(capsys):
    """LPKF must report 'not an SEC filer', never a misleading empty window."""
    rc = edgar.main(["LPKF"])
    assert rc == 0
    assert "not an SEC filer" in capsys.readouterr().out
