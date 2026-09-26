"""Instant-based availability at clock changes, with integer-minute oracles."""

import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta, timezone
from itertools import permutations
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from quant_research.data.availability import Observation, snapshot

LONDON = ZoneInfo("Europe/London")
KEY = ("SYNTH", "signal")


def fold_time(fold, minute=30):
    return datetime(2026, 10, 25, 1, minute, tzinfo=LONDON, fold=fold)


def row(observed, available, value=1):
    return Observation(*KEY, observed, available, value)


def test_future_fold_publication_does_not_leak():
    early, late = fold_time(0), fold_time(1)
    record = row(early, late)
    assert snapshot([record], early) == {}
    assert snapshot([record], late)[KEY] is record


def test_reversed_instants_are_rejected_despite_equal_wall_time():
    with pytest.raises(ValueError, match="precede"):
        row(fold_time(1), fold_time(0))


def test_forward_instants_accepted_despite_backwards_wall_time():
    record = row(fold_time(0, 50), fold_time(1, 10))
    assert record.available_at - record.observed_at == timedelta(minutes=20)


def test_distinct_fold_versions_and_revision_order():
    observed = datetime(2026, 10, 25, tzinfo=UTC)
    first, revised = row(observed, fold_time(0), 1), row(observed, fold_time(1), 2)
    for ordering in permutations([first, revised]):
        assert snapshot(ordering, fold_time(0))[KEY] is first
        assert snapshot(ordering, fold_time(1))[KEY] is revised


def test_latest_observation_uses_instants_before_revision_order():
    old = row(fold_time(0, 50), fold_time(1, 50), 1)
    new = row(fold_time(1, 10), fold_time(1, 20), 2)
    for ordering in permutations([old, new]):
        assert snapshot(ordering, fold_time(1, 55))[KEY] is new


@pytest.mark.parametrize("offset,accepted", [(-1, True), (0, True), (1, False)])
def test_fold_latency_boundary_in_elapsed_microseconds(offset, accepted):
    record = row(fold_time(0), fold_time(0))
    latency = timedelta(hours=1, microseconds=offset)
    assert bool(snapshot([record], fold_time(1), latency=latency)) is accepted


@pytest.mark.parametrize("offset,accepted", [(-1, False), (0, True), (1, True)])
def test_fold_staleness_boundary_in_elapsed_microseconds(offset, accepted):
    # A just-published revision must retain the original observation's age.
    record = row(fold_time(0), fold_time(1))
    max_age = timedelta(hours=1, microseconds=offset)
    assert bool(snapshot([record], fold_time(1), max_age=max_age)) is accepted


def test_spring_clock_change_does_not_inflate_elapsed_time():
    start = datetime(2026, 3, 29, 0, 30, tzinfo=LONDON)
    end = datetime(2026, 3, 29, 2, 30, tzinfo=LONDON)
    record = row(start, start)
    assert snapshot([record], end, latency=timedelta(minutes=90)) == {}
    assert snapshot([record], end, max_age=timedelta(minutes=90))[KEY] is record


@pytest.mark.parametrize("fold", [0, 1])
def test_same_instant_duplicate_rejected_across_zone_representations(fold):
    local = fold_time(fold)
    first = row(local, local)
    equivalent = row(local.astimezone(UTC), local.astimezone(UTC), 2)
    # Validation remains unconditional, even before the version is available.
    with pytest.raises(ValueError, match="duplicate"):
        snapshot([first, equivalent], datetime(2026, 1, 1, tzinfo=UTC))


def test_canonical_storage_preserves_instants_and_leaves_input_unchanged():
    original = fold_time(1)
    record = row(fold_time(0), original)
    assert record.observed_at == datetime(2026, 10, 25, 0, 30, tzinfo=UTC)
    assert record.available_at == datetime(2026, 10, 25, 1, 30, tzinfo=UTC)
    assert record.observed_at.tzinfo is UTC and record.available_at.tzinfo is UTC
    assert original.tzinfo is LONDON and original.fold == 1


@pytest.mark.parametrize("bad", [None, "2026-10-25", datetime(2026, 10, 25)])
def test_invalid_timestamps_rejected_at_all_entry_points(bad):
    for observed, available in [(bad, fold_time(0)), (fold_time(0), bad)]:
        with pytest.raises(ValueError, match="timezone-aware"):
            row(observed, available)
    with pytest.raises(ValueError, match="timezone-aware"):
        snapshot([], bad)


@pytest.mark.parametrize(
    "zone,epoch",
    [
        ("Europe/London", datetime(2026, 10, 25, tzinfo=UTC)),
        ("Europe/London", datetime(2026, 3, 29, tzinfo=UTC)),
        ("America/New_York", datetime(2026, 11, 1, 5, tzinfo=UTC)),
        ("America/New_York", datetime(2026, 3, 8, 6, tzinfo=UTC)),
    ],
)
def test_transition_grid_matches_independent_integer_minute_oracle(zone, epoch):
    zones = [ZoneInfo(zone), UTC, timezone(timedelta(hours=5, minutes=30))]
    schedule = [(0, 15, 1), (0, 75, 2), (50, 55, 3), (70, 80, 4)]
    for representation in zones:
        records = [
            row(
                (epoch + timedelta(minutes=o)).astimezone(representation),
                (epoch + timedelta(minutes=a)).astimezone(representation),
                value,
            )
            for o, a, value in schedule
        ]
        for decision_minute in range(0, 121, 5):
            for latency in (0, 15):
                for max_age in (None, 30, 60):
                    eligible = [
                        (o, a, value)
                        for o, a, value in schedule
                        if a + latency <= decision_minute
                        and (max_age is None or decision_minute - o <= max_age)
                    ]
                    expected = max(eligible)[2] if eligible else None
                    for decision_zone in zones:
                        decision = (epoch + timedelta(minutes=decision_minute)).astimezone(
                            decision_zone
                        )
                        for ordered in (records, list(reversed(records))):
                            selected = snapshot(
                                ordered,
                                decision,
                                latency=timedelta(minutes=latency),
                                max_age=None if max_age is None else timedelta(minutes=max_age),
                            ).get(KEY)
                            assert (selected.value if selected else None) == expected


def test_fold_experiment_reproduces_hand_checked_results(tmp_path):
    root = Path(__file__).resolve().parents[1]
    outputs = [tmp_path / "first.json", tmp_path / "second.json"]
    for output in outputs:
        subprocess.run(
            [sys.executable, str(root / "scripts/fold_experiment.py"), "--output", str(output)],
            check=True,
            capture_output=True,
        )
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
    assert outputs[0].read_bytes() == (root / "experiments/timezones/results.json").read_bytes()
    result = json.loads(outputs[0].read_text())
    assert result["data_kind"] == "synthetic"
    assert result["legacy_future_publication_selected"] is True
    assert result["corrected_future_publication_selected"] is False
    assert result["elapsed_minutes"] == 60
    assert result["wall_clock_minutes"] == 0
    assert result["latency_60_minutes_accepted"] is True
    assert result["max_age_59_minutes_accepted"] is False
    assert result["latest_revision_value"] == 2
