"""Independent acceptance evidence for Q006a's fixed prospective schedule, not a calendar API."""

import json
import runpy
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "experiments/calendar/nyse-2026-autumn-v1.json"
AUDIT = ROOT / "scripts/calendar_contract_audit.py"
DATA = json.loads(FIXTURE.read_text())
BY_DATE = {row["date"]: row for row in DATA["days"]}


def test_source_and_scope_are_explicit():
    assert DATA["schema_version"] == 1
    assert DATA["data_kind"] == "scheduled_calendar_fixture"
    assert DATA["source_url"] == "https://www.nyse.com/trade/hours-calendars"
    assert DATA["consulted_on"] == "2026-09-28"
    assert DATA["zone"] == "America/New_York"
    assert (DATA["coverage_start"], DATA["coverage_end"]) == ("2026-10-29", "2026-11-30")
    assert DATA["decision_local"] == "09:00:00"
    assert DATA["core_open_local"] == "09:30:00"
    assert DATA["regular_close_local"] == "16:00:00"
    assert DATA["early_close_local"] == "13:00:00"
    assert DATA["consulted_tzdb_version"]
    assert len(bytes.fromhex(DATA["consulted_zone_tzif_sha256"])) == 32


def test_closed_dates_match_hand_list_and_have_no_fake_times():
    weekends = {
        "2026-10-31",
        "2026-11-01",
        "2026-11-07",
        "2026-11-08",
        "2026-11-14",
        "2026-11-15",
        "2026-11-21",
        "2026-11-22",
        "2026-11-28",
        "2026-11-29",
    }
    assert {r["date"] for r in DATA["days"] if r["status"] == "weekend"} == weekends
    assert all(set(BY_DATE[d]) == {"date", "status"} for d in weekends)
    assert BY_DATE["2026-11-26"] == {
        "date": "2026-11-26",
        "status": "holiday",
        "name": "Thanksgiving Day",
    }
    assert [r["date"] for r in DATA["days"] if r["status"] == "holiday"] == ["2026-11-26"]


@pytest.mark.parametrize(
    "day,decision,opening,closing",
    [
        ("2026-10-30", "13:00", "13:30", "20:00"),
        ("2026-11-02", "14:00", "14:30", "21:00"),
        ("2026-11-27", "14:00", "14:30", "18:00"),
        ("2026-11-30", "14:00", "14:30", "21:00"),
    ],
)
def test_utc_values_match_hand_arithmetic(day, decision, opening, closing):
    for key, clock in zip(
        ("decision_utc", "core_open_utc", "core_close_utc"),
        (decision, opening, closing),
        strict=True,
    ):
        assert BY_DATE[day][key] == f"{day}T{clock}:00+00:00"


@pytest.mark.parametrize("row", [r for r in DATA["days"] if "decision_utc" in r])
def test_preopen_gap_and_regular_or_short_session(row):
    decision, opening, closing = (
        datetime.fromisoformat(row[key])
        for key in ("decision_utc", "core_open_utc", "core_close_utc")
    )
    assert opening - decision == timedelta(minutes=30)
    expected = 210 if row["date"] == "2026-11-27" else 390
    assert closing - opening == timedelta(minutes=expected)


@pytest.mark.parametrize(
    "defect",
    [
        "missing_date",
        "duplicate_date",
        "holiday_open",
        "wrong_utc",
        "early_close_lost",
        "extra_field",
    ],
)
def test_audit_rejects_corrupted_fixture(tmp_path, defect):
    data = deepcopy(DATA)
    rows = data["days"]
    by_date = {r["date"]: r for r in rows}
    if defect == "missing_date":
        rows.pop(3)
    elif defect == "duplicate_date":
        rows[3] = dict(rows[2])
    elif defect == "holiday_open":
        by_date["2026-11-26"]["status"] = "regular"
    elif defect == "wrong_utc":
        by_date["2026-11-02"]["decision_utc"] = "2026-11-02T13:00:00+00:00"
    elif defect == "early_close_lost":
        by_date["2026-11-27"]["core_close_utc"] = "2026-11-27T21:00:00+00:00"
    else:
        rows[0]["unexpected"] = True
    candidate = tmp_path / "candidate.json"
    candidate.write_text(json.dumps(data))
    run = runpy.run_path(str(AUDIT))["run"]
    run.__globals__["FIXTURE"] = candidate
    with pytest.raises(ValueError):
        run()


def test_two_audit_replays_match_archived_bytes_and_prior_sessions(tmp_path):
    archived = ROOT / "experiments/calendar/contract-audit.json"
    for i in range(2):
        output = tmp_path / f"audit-{i}.json"
        subprocess.run(
            [sys.executable, str(AUDIT), "--output", str(output)],
            check=True,
            capture_output=True,
            text=True,
        )
        assert output.read_bytes() == archived.read_bytes()
    result = json.loads(archived.read_text())
    assert result["calendar_dates"] == 33
    assert result["status_counts"] == {"regular": 21, "early_close": 1, "weekend": 10, "holiday": 1}
    assert result["november_sessions"] == 20
    sessions = {s["date"]: s for s in result["sessions"]}
    assert sessions["2026-10-29"]["previous_session"] is None
    assert sessions["2026-11-02"]["previous_session"] == "2026-10-30"
    assert sessions["2026-11-27"]["previous_session"] == "2026-11-25"
    assert sessions["2026-11-30"]["previous_session"] == "2026-11-27"
