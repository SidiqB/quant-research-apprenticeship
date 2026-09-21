from datetime import UTC, datetime, timedelta, timezone
from itertools import permutations

import pytest

from quant_research.data.availability import Observation, snapshot


def t(hour=0):
    return datetime(2026, 1, 1, hour, tzinfo=UTC)


def obs(observed=0, available=1, value=100.0, asset="X", feature="earnings"):
    return Observation(asset, feature, t(observed), t(available), value)


def test_future_publication_is_not_available():
    assert snapshot([obs(available=2)], t(1)) == {}


def test_revision_is_not_retroactive():
    initial, revision = obs(), obs(available=4, value=50)
    assert snapshot([initial, revision], t(2))["X", "earnings"] == initial
    assert snapshot([initial, revision], t(4))["X", "earnings"] == revision


def test_newest_observation_precedes_later_revision_of_old_observation():
    old_revision, new = obs(available=5), obs(observed=2, available=3, value=200)
    assert snapshot([old_revision, new], t(6))["X", "earnings"] == new


def test_order_does_not_matter():
    records = [obs(), obs(available=4), obs(observed=2, available=3)]
    expected = snapshot(records, t(5))
    for ordering in permutations(records):
        assert snapshot(ordering, t(5)) == expected


def test_latency_and_equality_boundary():
    record = obs()
    assert snapshot([record], t(1))["X", "earnings"] == record
    assert snapshot([record], t(1), latency=timedelta(microseconds=1)) == {}
    assert snapshot([record], t(2), latency=timedelta(hours=1))


def test_max_age_is_not_reset_by_revision():
    assert snapshot([obs(available=4)], t(4), max_age=timedelta(hours=3)) == {}
    assert snapshot([obs()], t(4), max_age=timedelta(hours=4))


def test_assets_and_features_remain_separate():
    records = [obs(), obs(asset="Y"), obs(feature="price")]
    assert len(snapshot(records, t(2))) == 3


def test_missing_stays_missing():
    assert snapshot([], t()) == {}


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_rejected(value):
    with pytest.raises(ValueError, match="finite"):
        obs(value=value)


@pytest.mark.parametrize("field", ["asset", "feature"])
def test_empty_keys_rejected(field):
    with pytest.raises(ValueError, match="nonempty"):
        obs(**{field: " "})


def test_bad_time_order_rejected():
    with pytest.raises(ValueError, match="precede"):
        obs(observed=2, available=1)


def test_naive_timestamp_rejected():
    with pytest.raises(ValueError, match="timezone"):
        Observation("X", "f", datetime(2026, 1, 1), t(1), 1)
    with pytest.raises(ValueError, match="timezone"):
        snapshot([], datetime(2026, 1, 1))


@pytest.mark.parametrize("argument", ["latency", "max_age"])
def test_negative_durations_rejected(argument):
    with pytest.raises(ValueError, match="nonnegative"):
        snapshot([], t(), **{argument: timedelta(seconds=-1)})


def test_duplicate_versions_fail_even_when_not_yet_available():
    with pytest.raises(ValueError, match="duplicate"):
        snapshot([obs(), obs(value=2)], t())


def test_timezone_equivalence():
    decision = datetime(2026, 1, 1, 2, tzinfo=timezone(timedelta(hours=1)))
    assert snapshot([obs()], decision) == snapshot([obs()], t(1))


def test_appending_future_versions_does_not_change_past_snapshot():
    base = [obs()]
    assert snapshot(base, t(2)) == snapshot(base + [obs(available=3, value=-999)], t(2))


def test_generator_supported():
    assert snapshot((x for x in [obs()]), t(2)) == snapshot([obs()], t(2))
