"""Exact effective-date oracles; no empirical or as-known-at claims."""

import json
import subprocess
import sys
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta
from itertools import permutations
from pathlib import Path

import pytest

from quant_research.data.membership import MembershipHistory, MembershipInterval

ROOT = Path(__file__).resolve().parents[1]
D = date(2026, 1, 1)


def day(offset):
    return D + timedelta(days=offset)


@pytest.mark.parametrize("offset,expected", [(0, ()), (1, ("A",)), (2, ("A",)), (3, ()), (4, ())])
def test_inclusive_entry_exclusive_exit(offset, expected):
    history = MembershipHistory((MembershipInterval("A", day(1), day(3)),), D, day(5))
    assert history.members_on(day(offset)) == expected


@pytest.mark.parametrize("asset", [None, True, 1, "", " ", " A", "A ", "A B", "A\nB", "A\x00B"])
def test_invalid_identity(asset):
    with pytest.raises(ValueError, match="asset"):
        MembershipInterval(asset, D, None)


@pytest.mark.parametrize("field", ["entry", "exit"])
@pytest.mark.parametrize("bad", ["2026-01-01", datetime(2026, 1, 1), 0, True])
def test_dates_are_not_implicitly_coerced(field, bad):
    with pytest.raises(ValueError, match=field):
        MembershipInterval(**{"asset": "A", "entry": D, "exit": day(3), field: bad})


@pytest.mark.parametrize("end", [D, day(-1)])
def test_empty_or_reversed_interval(end):
    with pytest.raises(ValueError, match="follow"):
        MembershipInterval("A", D, end)


@pytest.mark.parametrize("field", ["start", "end"])
@pytest.mark.parametrize("bad", [None, "2026-01-01", datetime(2026, 1, 1)])
def test_invalid_coverage_type(field, bad):
    with pytest.raises(ValueError, match=field):
        MembershipHistory(**{"intervals": (), "start": D, "end": day(5), field: bad})


@pytest.mark.parametrize("end", [D, day(-1)])
def test_invalid_coverage_order(end):
    with pytest.raises(ValueError, match="follow"):
        MembershipHistory((), D, end)


@pytest.mark.parametrize("bad", [None, [], (None,), ("A",)])
def test_invalid_record_container(bad):
    with pytest.raises(ValueError, match="tuple"):
        MembershipHistory(bad, D, day(5))


@pytest.mark.parametrize("when", [day(-1), day(5), day(6)])
def test_unknown_coverage_is_not_empty_membership(when):
    with pytest.raises(ValueError, match="coverage"):
        MembershipHistory((), D, day(5)).members_on(when)


@pytest.mark.parametrize("when", [None, "2026-01-01", datetime(2026, 1, 1)])
def test_query_rejects_non_date(when):
    with pytest.raises(ValueError, match="session_date"):
        MembershipHistory((), D, day(5)).members_on(when)


@pytest.mark.parametrize("first_end,second_start", [(3, 2), (3, 0), (None, 4)])
def test_overlap_duplicate_and_open_ended_conflict(first_end, second_start):
    records = (
        MembershipInterval("A", D, None if first_end is None else day(first_end)),
        MembershipInterval("A", day(second_start), day(5)),
    )
    for order in permutations(records):
        with pytest.raises(ValueError, match="overlapping"):
            MembershipHistory(order, D, day(6))


def test_exact_duplicate_rejected():
    record = MembershipInterval("A", D, day(3))
    with pytest.raises(ValueError, match="duplicate"):
        MembershipHistory((record, record), D, day(6))


@pytest.mark.parametrize("entry,exit", [(-3, 0), (5, 6), (5, None)])
def test_irrelevant_interval_rejected(entry, exit):
    record = MembershipInterval("A", day(entry), None if exit is None else day(exit))
    with pytest.raises(ValueError, match="intersect"):
        MembershipHistory((record,), D, day(5))


def test_straddling_open_interval_and_date_extremes():
    history = MembershipHistory((MembershipInterval("A", date.min, None),), D, day(5))
    assert history.members_on(D) == ("A",)
    assert history.members_on(day(4)) == ("A",)
    history = MembershipHistory((MembershipInterval("A", date.min, date.max),), date.min, date.max)
    assert history.members_on(date.min) == ("A",)
    assert history.members_on(date.max - timedelta(days=1)) == ("A",)


def test_empty_is_explicit_and_records_are_immutable():
    history = MembershipHistory((), D, day(5))
    assert history.members_on(D) == ()
    with pytest.raises(FrozenInstanceError):
        history.end = day(6)
    record = MembershipInterval("A", D, None)
    with pytest.raises(FrozenInstanceError):
        record.exit = day(5)


def test_adjacency_reentry_and_input_order_against_event_ledger():
    records = (
        MembershipInterval("A", D, day(2)),
        MembershipInterval("A", day(2), day(4)),
        MembershipInterval("A", day(6), None),
        MembershipInterval("B", day(1), day(3)),
    )
    # Independent event ledger: remove exits, then apply entries each day.
    events = {
        0: ((), ("A",)),
        1: ((), ("B",)),
        2: (("A",), ("A",)),
        3: (("B",), ()),
        4: (("A",), ()),
        6: ((), ("A",)),
    }
    expected, active = [], set()
    for offset in range(8):
        exits, entries = events.get(offset, ((), ()))
        active.difference_update(exits)
        active.update(entries)
        expected.append(tuple(sorted(active)))
    checks = 0
    for order in permutations(records):
        history = MembershipHistory(order, D, day(8))
        for offset, members in enumerate(expected):
            assert history.members_on(day(offset)) == members
            checks += 1
    assert checks == 192


def test_later_entry_does_not_change_earlier_membership():
    old = MembershipInterval("OLD-ID", D, day(3))
    new = MembershipInterval("NEW-ID", day(3), None)
    # Same hypothetical display ticker would not merge these security identities.
    before = MembershipHistory((old,), D, day(6))
    after = MembershipHistory((new, old), D, day(6))
    assert before.members_on(day(1)) == after.members_on(day(1)) == ("OLD-ID",)
    assert after.members_on(day(3)) == ("NEW-ID",)


def test_experiment_replays_twice(tmp_path):
    archived = (ROOT / "experiments/membership/results.json").read_bytes()
    for index in range(2):
        output = tmp_path / f"result-{index}.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/membership_experiment.py"),
                "--output",
                str(output),
            ],
            check=True,
            capture_output=True,
        )
        assert output.read_bytes() == archived
    result = json.loads(archived)
    assert result["data_kind"] == "synthetic"
    assert result["hand_sets_passed"] == 8
    assert result["wrongly_removed"] == ["OLD"]
    assert result["past_members"] == ["OLD", "RETURN", "STAY"]
    assert result["wrong_survivor_filtered_members"] == ["RETURN", "STAY"]
