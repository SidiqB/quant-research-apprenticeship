"""Behavioral tests of bounded lookup, decisions, core hours and exact history."""

import subprocess
import sys
from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from quant_research.data.calendar import CalendarCoverageError, NyseAutumn2026Calendar

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "experiments/calendar/nyse-2026-autumn-v1.json"
NY = ZoneInfo("America/New_York")
CAL = NyseAutumn2026Calendar(FIXTURE)


@pytest.mark.parametrize("session", CAL.sessions)
def test_every_session_has_valid_preopen_decision_and_exact_core_boundaries(session):
    assert CAL.session_on(session.day) == session
    assert CAL.validate_decision(session.decision_at) == session
    assert CAL.validate_decision(session.decision_at.astimezone(NY)) == session
    assert not CAL.is_core_time(session.decision_at)
    microsecond = timedelta(microseconds=1)
    for timestamp in (session.decision_at - microsecond, session.decision_at + microsecond):
        with pytest.raises(ValueError, match="exactly"):
            CAL.validate_decision(timestamp)
    assert not CAL.is_core_time(session.core_open - microsecond)
    assert CAL.is_core_time(session.core_open)
    assert CAL.is_core_time(session.core_open + microsecond)
    assert CAL.is_core_time(session.core_close - microsecond)
    assert not CAL.is_core_time(session.core_close)
    assert not CAL.is_core_time(session.core_close + microsecond)
    for boundary in (session.core_open, session.core_close):
        with pytest.raises(ValueError, match="exactly"):
            CAL.validate_decision(boundary)


@pytest.mark.parametrize(
    "day",
    [
        "2026-10-31",
        "2026-11-01",
        "2026-11-07",
        "2026-11-08",
        "2026-11-14",
        "2026-11-15",
        "2026-11-21",
        "2026-11-22",
        "2026-11-26",
        "2026-11-28",
        "2026-11-29",
    ],
)
def test_all_hand_listed_closed_days(day):
    day = date.fromisoformat(day)
    assert CAL.session_on(day) is None
    assert not CAL.is_core_time(datetime.combine(day, datetime.min.time(), NY))
    with pytest.raises(ValueError, match="closed"):
        CAL.validate_decision(datetime(day.year, day.month, day.day, 9, tzinfo=NY))
    with pytest.raises(ValueError, match="anchor"):
        CAL.previous_sessions(day)


@pytest.mark.parametrize(
    "stamp,day,close",
    [
        ("2026-10-30T13:00:00+00:00", "2026-10-30", "2026-10-30T20:00:00+00:00"),
        ("2026-11-02T14:00:00+00:00", "2026-11-02", "2026-11-02T21:00:00+00:00"),
        ("2026-11-27T14:00:00+00:00", "2026-11-27", "2026-11-27T18:00:00+00:00"),
        ("2026-11-30T14:00:00+00:00", "2026-11-30", "2026-11-30T21:00:00+00:00"),
    ],
)
def test_hand_utc_examples_in_many_representations(stamp, day, close):
    instant = datetime.fromisoformat(stamp)
    for zone in (UTC, NY, ZoneInfo("Asia/Tokyo"), timezone(timedelta(hours=14))):
        session = CAL.validate_decision(instant.astimezone(zone))
        assert session.day == date.fromisoformat(day)
        assert session.core_close == datetime.fromisoformat(close)


@pytest.mark.parametrize("stamp", ["2026-10-30T14:00:00+00:00", "2026-11-02T13:00:00+00:00"])
def test_wrong_fixed_utc_hour_is_rejected(stamp):
    with pytest.raises(ValueError, match="exactly"):
        CAL.validate_decision(datetime.fromisoformat(stamp))


@pytest.mark.parametrize("method", ["validate_decision", "is_core_time"])
@pytest.mark.parametrize("bad", [datetime(2026, 11, 2, 9), "2026-11-02", None, date(2026, 11, 2)])
def test_timestamp_apis_reject_naive_and_non_datetime(method, bad):
    with pytest.raises(ValueError, match="aware datetime"):
        getattr(CAL, method)(bad)


@pytest.mark.parametrize("day", [date(2026, 10, 28), date(2026, 12, 1)])
def test_outside_dates_are_unknown_not_closed(day):
    with pytest.raises(CalendarCoverageError, match="outside"):
        CAL.session_on(day)
    with pytest.raises(CalendarCoverageError, match="outside"):
        CAL.previous_sessions(day)
    for method in (CAL.validate_decision, CAL.is_core_time):
        with pytest.raises(CalendarCoverageError, match="outside"):
            method(datetime(day.year, day.month, day.day, 9, tzinfo=NY))


def test_utc_day_does_not_override_new_york_date():
    # UTC is in range, New York is still the unknown prior date.
    with pytest.raises(CalendarCoverageError):
        CAL.is_core_time(datetime(2026, 10, 29, 1, tzinfo=UTC))
    # UTC is out of range, New York is the last known evening, outside core hours.
    assert not CAL.is_core_time(datetime(2026, 12, 1, 1, tzinfo=UTC))
    with pytest.raises(ValueError, match="exactly"):
        CAL.validate_decision(datetime(2026, 12, 1, 1, tzinfo=UTC))


@pytest.mark.parametrize("bad", [datetime(2026, 11, 2, tzinfo=UTC), "2026-11-02", None])
def test_date_apis_require_explicit_date(bad):
    for method in (CAL.session_on, CAL.previous_sessions):
        with pytest.raises(ValueError, match="must be a date"):
            method(bad)


@pytest.mark.parametrize(
    "day,previous",
    [
        ("2026-10-30", "2026-10-29"),
        ("2026-11-02", "2026-10-30"),
        ("2026-11-27", "2026-11-25"),
        ("2026-11-30", "2026-11-27"),
    ],
)
def test_previous_session_crosses_closed_days(day, previous):
    assert [s.day.isoformat() for s in CAL.previous_sessions(date.fromisoformat(day))] == [previous]


def test_twenty_session_window_has_exact_history_and_never_partial_results():
    expected = [
        "2026-10-30",
        "2026-11-02",
        "2026-11-03",
        "2026-11-04",
        "2026-11-05",
        "2026-11-06",
        "2026-11-09",
        "2026-11-10",
        "2026-11-11",
        "2026-11-12",
        "2026-11-13",
        "2026-11-16",
        "2026-11-17",
        "2026-11-18",
        "2026-11-19",
        "2026-11-20",
        "2026-11-23",
        "2026-11-24",
        "2026-11-25",
        "2026-11-27",
    ]
    assert [s.day.isoformat() for s in CAL.previous_sessions(date(2026, 11, 30), 20)] == expected
    assert len(CAL.previous_sessions(date(2026, 11, 27), 20)) == 20
    for day, count in [(date(2026, 11, 25), 20), (date(2026, 11, 30), 22), (CAL.coverage_start, 1)]:
        with pytest.raises(CalendarCoverageError, match="insufficient"):
            CAL.previous_sessions(day, count)
    # A valid first decision need not have enough feature history.
    CAL.validate_decision(datetime(2026, 10, 29, 13, tzinfo=UTC))


@pytest.mark.parametrize("count", [0, -1, True, 1.0, "1", None])
def test_invalid_history_count(count):
    with pytest.raises(ValueError, match="positive integer"):
        CAL.previous_sessions(date(2026, 11, 30), count)


def test_calendar_and_returned_sessions_are_immutable():
    with pytest.raises(FrozenInstanceError):
        CAL.coverage_end = date(2027, 1, 1)
    with pytest.raises(FrozenInstanceError):
        CAL.sessions[0].core_close = CAL.sessions[0].core_open


@pytest.mark.parametrize("raw", [b"{}", FIXTURE.read_bytes() + b"\n", b"not json"])
def test_changed_or_malformed_fixture_fails_before_parsing(tmp_path, raw):
    path = tmp_path / "changed.json"
    path.write_bytes(raw)
    with pytest.raises(ValueError, match="SHA-256"):
        NyseAutumn2026Calendar(path)


def test_installed_timezone_mismatch_is_rejected(monkeypatch):
    monkeypatch.setattr("quant_research.data.calendar.ZoneInfo", lambda _: ZoneInfo("UTC"))
    with pytest.raises(ValueError, match="timezone rules"):
        NyseAutumn2026Calendar(FIXTURE)


def test_closed_day_publication_remains_valid_ingestion():
    from quant_research.data.ingestion import ingest_observations

    rows = [
        {
            "asset": "SYNTH",
            "feature": "close",
            "value": 1.0,
            "observed_at": "2026-11-25T16:00:00-05:00",
            "available_at": "2026-11-26T12:00:00-05:00",
        }
    ]
    observations = ingest_observations(rows, source_zone="America/New_York")
    assert len(observations) == 1
    assert observations[0].available_at == datetime(2026, 11, 26, 17, tzinfo=UTC)


def test_two_replays_match_archived_result(tmp_path):
    archived = ROOT / "experiments/calendar/decision-validation.json"
    for index in range(2):
        output = tmp_path / f"replay-{index}.json"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/calendar_experiment.py"), "--output", str(output)],
            check=True,
            capture_output=True,
        )
        assert output.read_bytes() == archived.read_bytes()
