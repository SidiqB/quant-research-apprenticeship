"""Boundary, invalid-input and independent overlap checks for past-only splits."""

from datetime import UTC, datetime, timedelta, timezone
from random import Random
from zoneinfo import ZoneInfo

import pytest

from quant_research.validation.purging import LabelInterval, purged_holdout


def day(value):
    return datetime(2026, 1, value, tzinfo=UTC)


def label(name, start, end):
    return LabelInterval(name, day(start), day(end))


@pytest.mark.parametrize("offset,kept", [(-1, True), (0, False), (1, False)])
def test_touching_endpoint_is_purged(offset, kept):
    rows = [
        LabelInterval("train", day(1), day(5) + timedelta(microseconds=offset)),
        label("test", 5, 9),
    ]
    result = purged_holdout(rows, day(5), day(8))
    assert result.train == ((0,) if kept else ())
    assert result.purged == (() if kept else (0,))
    assert result.evaluation == (1,)


def test_variable_horizons_and_half_open_decision_window():
    rows = [
        label(str(i), start, end)
        for i, (start, end) in enumerate([(1, 3), (2, 5), (3, 10), (4, 4), (5, 6), (7, 10), (8, 9)])
    ]
    result = purged_holdout(iter(rows), day(5), day(8))
    assert result.train == (0, 3)
    assert result.purged == (1, 2)
    assert result.evaluation == (4, 5)
    assert result.excluded == (6,)


@pytest.mark.parametrize("rows", [[label("e", 5, 6)], [label("t", 1, 9), label("e", 5, 6)]])
def test_empty_training_is_reported_without_reintroducing_rows(rows):
    result = purged_holdout(rows, day(5), day(7))
    assert result.train == ()
    assert result.evaluation == (len(rows) - 1,)


@pytest.mark.parametrize("rows", [[], [label("t", 1, 2)], [label("future", 8, 9)]])
def test_empty_evaluation_is_rejected(rows):
    with pytest.raises(ValueError, match="no decisions"):
        purged_holdout(rows, day(5), day(8))


@pytest.mark.parametrize("end", [day(4), day(5)])
def test_invalid_window(end):
    with pytest.raises(ValueError, match="after"):
        purged_holdout([], day(5), end)


@pytest.mark.parametrize("name", ["", " ", None, 17])
def test_invalid_identity(name):
    with pytest.raises(ValueError, match="nonempty string"):
        LabelInterval(name, day(1), day(2))


@pytest.mark.parametrize("bad", [datetime(2026, 1, 1), None, "2026-01-01"])
def test_aware_timestamp_required_everywhere(bad):
    for start, end in [(bad, day(2)), (day(1), bad)]:
        with pytest.raises(ValueError, match="timezone-aware"):
            LabelInterval("bad", start, end)
        with pytest.raises(ValueError, match="timezone-aware"):
            purged_holdout([], start, end)


def test_reversed_label_rejected():
    with pytest.raises(ValueError, match="precede"):
        label("bad", 3, 2)


def test_unsorted_and_duplicate_rows_rejected_even_outside_window():
    with pytest.raises(ValueError, match="chronological"):
        purged_holdout([label("e", 5, 6), label("t", 1, 2)], day(5), day(8))
    with pytest.raises(ValueError, match="duplicate"):
        purged_holdout([label("e", 5, 6), label("e", 8, 9)], day(5), day(8))
    with pytest.raises(ValueError, match="LabelInterval"):
        purged_holdout([None], day(5), day(8))


def test_panel_decisions_and_equivalent_timezones():
    offset = timezone(timedelta(hours=3))
    rows = [
        label("asset_a", 1, 2),
        label("asset_b", 1, 5),
        LabelInterval("e", day(5).astimezone(offset), day(6)),
    ]
    result = purged_holdout(rows, day(5).astimezone(offset), day(8))
    assert result.train == (0,)
    assert result.purged == (1,)
    assert result.evaluation == (2,)
    assert rows[-1].decision_at.tzinfo is UTC


def test_dst_fold_compares_instants_not_wall_clock():
    london = ZoneInfo("Europe/London")
    earlier = datetime(2026, 10, 25, 1, 30, tzinfo=london, fold=0)
    later = datetime(2026, 10, 25, 1, 30, tzinfo=london, fold=1)
    rows = [LabelInterval("t", earlier, earlier), LabelInterval("e", later, later)]
    result = purged_holdout(rows, later, datetime(2026, 10, 25, 3, tzinfo=london))
    assert result.train == (0,)
    assert result.evaluation == (1,)
    with pytest.raises(ValueError, match="precede"):
        LabelInterval("backwards", later, earlier)


def test_seeded_intervals_match_independent_closed_interval_oracle():
    rng = Random(20260922)
    epoch = day(1)
    for _ in range(100):
        starts = sorted(rng.randrange(30) for _ in range(40))
        starts.append(30)  # Guarantee an evaluation observation at the boundary.
        rows = [
            LabelInterval(
                str(i),
                epoch + timedelta(hours=start),
                epoch + timedelta(hours=start + rng.randrange(45)),
            )
            for i, start in enumerate(starts)
        ]
        start, end = epoch + timedelta(hours=30), epoch + timedelta(hours=40)
        result = purged_holdout(rows, start, end)
        expected_purged = tuple(
            i
            for i, row in enumerate(rows)
            if row.decision_at < start and max(row.decision_at, start) <= min(row.label_end, end)
        )
        assert result.purged == expected_purged
        assert set(result.train) == set(range(40)) - set(expected_purged)
        assert sorted(result.train + result.evaluation + result.purged + result.excluded) == list(
            range(len(rows))
        )
        extended = rows + [LabelInterval("future", end, end + timedelta(hours=1))]
        future_result = purged_holdout(extended, start, end)
        assert (future_result.train, future_result.evaluation, future_result.purged) == (
            result.train,
            result.evaluation,
            result.purged,
        )


def test_experiment_matches_hand_work_and_reproduces_committed_artifact(tmp_path):
    import json
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    outputs = [tmp_path / "first.json", tmp_path / "second.json"]
    for output in outputs:
        subprocess.run(
            [sys.executable, str(root / "scripts/purging_experiment.py"), "--output", str(output)],
            check=True,
            capture_output=True,
            text=True,
        )
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
    assert outputs[0].read_bytes() == (root / "experiments/purging/results.json").read_bytes()
    result = json.loads(outputs[0].read_text())
    assert result["data_kind"] == "synthetic"
    for method, names, overlaps in [
        ("decision_only", ["A", "B", "C", "D"], 2),
        ("one_row_gap", ["A", "B", "C"], 2),
        ("interval_purging", ["A", "D"], 0),
    ]:
        assert result[method] == {
            "sample_ids": names,
            "retained_count": len(names),
            "overlap_count": overlaps,
        }
    assert result["purged_ids"] == ["B", "C"]
    assert result["evaluation_ids"] == ["E", "F", "G"]
    assert result["excluded_ids"] == ["H"]
