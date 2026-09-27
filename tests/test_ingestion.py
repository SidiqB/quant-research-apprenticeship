"""Hand-calculated source-clock and batch invariants; all values synthetic."""

import json
import subprocess
import sys
from datetime import UTC, datetime
from itertools import permutations
from pathlib import Path

import pytest

from quant_research.data.availability import snapshot
from quant_research.data.ingestion import ingest_observations

ROOT = Path(__file__).resolve().parents[1]


def row(**changes):
    return dict(
        {
            "asset": "SYNTH",
            "feature": "signal",
            "observed_at": "2026-10-25T01:30:00+01:00",
            "available_at": "2026-10-25T01:30:00+01:00",
            "value": 1,
        },
        **changes,
    )


def ingest(rows, zone="Europe/London"):
    return ingest_observations(rows, source_zone=zone)


@pytest.mark.parametrize("field", list(row()))
def test_missing_fields_rejected(field):
    candidate = row()
    del candidate[field]
    with pytest.raises(ValueError, match="row 1:.*exactly"):
        ingest([candidate])


@pytest.mark.parametrize("candidate", [None, [], "record", {**row(), "extra": 1}])
def test_malformed_rows_rejected(candidate):
    with pytest.raises(ValueError, match="exactly"):
        ingest([candidate])


@pytest.mark.parametrize("field", ["asset", "feature"])
@pytest.mark.parametrize("value", [None, 42, "", " ", " X", "X ", "X\nY", "X\x00Y"])
def test_invalid_identifiers(field, value):
    with pytest.raises(ValueError, match="identifiers"):
        ingest([row(**{field: value})])


@pytest.mark.parametrize(
    "value", [True, False, "1.0", None, [], float("nan"), float("inf"), float("-inf"), 10**400]
)
def test_invalid_values(value):
    with pytest.raises(ValueError, match="value"):
        ingest([row(value=value)])


@pytest.mark.parametrize("value", [0, -1, 1.25])
def test_finite_scalar_values(value):
    assert ingest([row(value=value)])[0].value == float(value)


@pytest.mark.parametrize("zone", [None, "", " UTC", "No/Such_Zone", "/etc/passwd", "../UTC"])
def test_bad_source_zone_even_for_empty_batch(zone):
    with pytest.raises(ValueError, match="source_zone"):
        ingest([], zone)


@pytest.mark.parametrize("field", ["observed_at", "available_at"])
@pytest.mark.parametrize(
    "timestamp",
    [
        None,
        42,
        "2026-10-25T01:30:00",
        "2026-10-25",
        "2026-10-25 01:30:00+01:00",
        "2026-10-25T01:30+01:00",
        "2026-02-30T01:30:00Z",
        "2026-10-25T01:30:60Z",
        "2026-10-25T01:30:00.1234567+01:00",
        "2026-10-25T01:30:00-00:00",
        "2026-10-25T01:30:00+00:60",
        "2026-10-25T01:30:00+24:00",
        "2026-10-25T01:30:00+01:00\n",
    ],
)
def test_timestamp_syntax_and_precision(field, timestamp):
    with pytest.raises(ValueError, match="timestamp"):
        ingest([row(**{field: timestamp})])


@pytest.mark.parametrize("field", ["observed_at", "available_at"])
@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-03-29T01:30:00+00:00",
        "2026-03-29T01:30:00+01:00",
        "2026-07-01T12:00:00Z",
        "2026-10-25T01:30:00-04:00",
    ],
)
def test_gap_and_zone_mismatch_in_either_field(field, timestamp):
    with pytest.raises(ValueError, match="source zone"):
        ingest([row(**{field: timestamp})])


@pytest.mark.parametrize(
    "zone,early,late,expected_early,expected_late",
    [
        (
            "Europe/London",
            "2026-10-25T01:30:00+01:00",
            "2026-10-25T01:30:00+00:00",
            "2026-10-25T00:30:00+00:00",
            "2026-10-25T01:30:00+00:00",
        ),
        (
            "America/New_York",
            "2026-11-01T01:30:00-04:00",
            "2026-11-01T01:30:00-05:00",
            "2026-11-01T05:30:00+00:00",
            "2026-11-01T06:30:00+00:00",
        ),
        (
            "Australia/Lord_Howe",
            "2026-04-05T01:45:00+11:00",
            "2026-04-05T01:45:00+10:30",
            "2026-04-04T14:45:00+00:00",
            "2026-04-04T15:15:00+00:00",
        ),
    ],
)
def test_explicit_folds_and_reversed_chronology(zone, early, late, expected_early, expected_late):
    observations = ingest(
        [
            row(observed_at=early, available_at=early),
            row(observed_at=early, available_at=late, value=2),
        ],
        zone,
    )
    assert observations[0].observed_at.isoformat() == expected_early
    assert observations[1].available_at.isoformat() == expected_late
    assert all(x.observed_at.tzinfo is UTC and x.available_at.tzinfo is UTC for x in observations)
    assert (
        snapshot(observations, datetime.fromisoformat(expected_early))["SYNTH", "signal"].value == 1
    )
    assert (
        snapshot(observations, datetime.fromisoformat(expected_late))["SYNTH", "signal"].value == 2
    )
    with pytest.raises(ValueError, match="precede"):
        ingest([row(observed_at=late, available_at=early)], zone)


@pytest.mark.parametrize(
    "zone,timestamp",
    [
        ("America/New_York", "2026-03-08T02:30:00-05:00"),
        ("America/New_York", "2026-03-08T02:30:00-04:00"),
        ("Australia/Lord_Howe", "2026-10-04T02:15:00+10:30"),
        ("Australia/Lord_Howe", "2026-10-04T02:15:00+11:00"),
    ],
)
def test_non_london_gaps(zone, timestamp):
    with pytest.raises(ValueError, match="source zone"):
        ingest([row(observed_at=timestamp, available_at=timestamp)], zone)


def test_normal_dates_and_microseconds_across_spring_jump():
    observation = ingest(
        [row(observed_at="2026-03-29T00:59:59.999999Z", available_at="2026-03-29T02:00:00+01:00")]
    )[0]
    assert (observation.available_at - observation.observed_at).total_seconds() == 0.000001


@pytest.mark.parametrize("changed_value", [1, 2])
def test_duplicate_instants_fail_with_identical_or_conflicting_values(changed_value):
    first = row(observed_at="2026-01-01T00:00:00Z", available_at="2026-01-01T00:00:00Z")
    alias = {**first, "available_at": "2026-01-01T00:00:00.000000+00:00", "value": changed_value}
    for order in permutations([first, alias]):
        with pytest.raises(ValueError, match="row 2: duplicate"):
            ingest(order, "UTC")


def test_order_preservation_revisions_key_separation_and_no_input_mutation():
    raw = [
        row(),
        row(available_at="2026-10-25T01:30:00+00:00", value=2),
        row(asset="SECOND"),
        row(feature="other"),
    ]
    before = json.dumps(raw)
    for order in permutations(raw):
        observations = ingest(iter(order))
        assert [(x.asset, x.feature, x.value) for x in observations] == [
            (x["asset"], x["feature"], x["value"]) for x in order
        ]
        assert (
            snapshot(observations, datetime(2026, 10, 25, 2, tzinfo=UTC))["SYNTH", "signal"].value
            == 2
        )
    assert json.dumps(raw) == before


def test_empty_batch_and_failure_returns_no_partial_result_or_source_values():
    assert ingest([]) == ()
    result = "unchanged"
    with pytest.raises(ValueError, match="row 2: identifiers") as error:
        result = ingest(iter([row(), row(asset=" secret-source-id ")]))
    assert result == "unchanged"
    assert "secret-source-id" not in str(error.value)


def test_experiment_replays_twice(tmp_path):
    outputs = [tmp_path / "one.json", tmp_path / "two.json"]
    for output in outputs:
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/ingestion_experiment.py"),
                "--output",
                str(output),
            ],
            check=True,
            capture_output=True,
        )
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
    assert outputs[0].read_bytes() == (ROOT / "experiments/ingestion/results.json").read_bytes()
    result = json.loads(outputs[0].read_text())
    assert result["accepted_versions"] == 2
    assert result["decision_values"] == [1.0, 2.0]
    assert all(result["rejected_controls"].values())
