"""Independent arithmetic, exact window boundaries and adversarial timing checks."""

import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, date, datetime, timedelta
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from quant_research.alpha.lagged_returns import lagged_return
from quant_research.data.availability import Observation
from quant_research.data.calendar import CalendarCoverageError, NyseAutumn2026Calendar
from quant_research.data.corporate_actions import action_return

ROOT = Path(__file__).resolve().parents[1]
CAL = NyseAutumn2026Calendar(ROOT / "experiments/calendar/nyse-2026-autumn-v1.json")
FEATURE = "session_return"


def session(day):
    result = CAL.session_on(date.fromisoformat(day))
    assert result is not None
    return result


def observation(day, value, *, available=None, asset="A", feature=FEATURE):
    end = session(day).core_close
    return Observation(asset, feature, end, available or end, value)


def calculate(rows, day="2026-11-04", **kwargs):
    return lagged_return(rows, CAL, "A", session(day).decision_at, return_feature=FEATURE, **kwargs)


@pytest.mark.parametrize(
    "returns,expected",
    [
        ((0.1, -0.1), -0.01),
        ((0, 0), 0),
        ((-1, 0.5), -1),
        ((0.5, -1), -1),
        ((0.25, 0.2), 0.5),
        ((-0.5, -0.5), -0.75),
    ],
)
def test_hand_compounding(returns, expected):
    rows = [
        observation(day, r) for day, r in zip(("2026-11-02", "2026-11-03"), returns, strict=True)
    ]
    result = calculate(rows, periods=2)
    assert result.value == pytest.approx(expected, abs=1e-12)
    assert result.gross_return == pytest.approx(1 + expected, abs=1e-12)
    assert result.start_at == session("2026-10-30").core_close
    assert result.end_at == session("2026-11-03").core_close
    assert result.observations == tuple(rows)
    assert result.missing_at == ()


def test_later_revisions_never_rewrite_earlier_features():
    decision = session("2026-11-04").decision_at
    rows = [observation("2026-11-02", 0.1), observation("2026-11-03", -0.1)]
    revision = observation("2026-11-03", 0.5, available=decision + timedelta(microseconds=1))
    future = observation("2026-11-04", 100)
    expected = calculate(rows, periods=2)
    for order in permutations([*rows, revision, future]):
        assert calculate(iter(order), periods=2) == expected
    assert calculate([*rows, revision], "2026-11-05", periods=2, skip=1).value == pytest.approx(
        0.65
    )


@pytest.mark.parametrize(
    "offset,latency,expected",
    [(-1, 0, 0.5), (0, 0, 0.5), (1, 0, -0.1), (-1, 1, 0.5), (0, 1, -0.1), (1, 1, -0.1)],
)
def test_revision_latency_boundary(offset, latency, expected):
    decision = session("2026-11-04").decision_at
    rows = [
        observation("2026-11-03", -0.1),
        observation("2026-11-03", 0.5, available=decision + timedelta(microseconds=offset)),
    ]
    assert calculate(rows, latency=timedelta(microseconds=latency)).value == pytest.approx(expected)


@pytest.mark.parametrize("missing", [0, 1, 2])
def test_missing_or_delayed_interval_is_not_zero_or_compressed(missing):
    days = ["2026-10-30", "2026-11-02", "2026-11-03"]
    rows = [observation(day, 0.1) for day in days]
    absent = calculate(rows[:missing] + rows[missing + 1 :], periods=3)
    assert absent.value is None and absent.gross_return is None
    assert absent.missing_at == (session(days[missing]).core_close,)
    rows[missing] = replace(rows[missing], available_at=session("2026-11-05").decision_at)
    assert calculate(rows, periods=3) == absent


def test_empty_input_and_wrong_asset_feature_cannot_fill_gaps():
    wrong = [
        observation("2026-11-03", 0.1, asset="B"),
        observation("2026-11-03", 123, feature="price"),
    ]
    assert calculate(wrong) == calculate([])
    assert calculate([]).missing_at == (session("2026-11-03").core_close,)


def test_skip_does_not_require_values_for_skipped_sessions():
    result = calculate([observation("2026-11-02", 0.25)], skip=1)
    assert result.value == 0.25
    assert result.start_at == session("2026-10-30").core_close
    assert result.required_ends == (session("2026-11-02").core_close,)


def test_holiday_weekend_and_early_close_use_exact_instants():
    rows = [observation("2026-11-25", 0.1), observation("2026-11-27", -0.1)]
    result = calculate(rows, "2026-11-30", periods=2)
    assert result.value == pytest.approx(-0.01)
    assert result.start_at == session("2026-11-24").core_close
    assert result.required_ends == (
        datetime(2026, 11, 25, 21, tzinfo=UTC),
        datetime(2026, 11, 27, 18, tzinfo=UTC),
    )
    # Holiday publication is allowed; publication is distinct from interval end.
    holiday = replace(rows[0], available_at=datetime(2026, 11, 26, 12, tzinfo=UTC))
    assert calculate([holiday, rows[1]], "2026-11-30", periods=2).value == result.value
    wrong_close = replace(
        rows[1],
        observed_at=datetime(2026, 11, 27, 21, tzinfo=UTC),
        available_at=datetime(2026, 11, 27, 21, tzinfo=UTC),
    )
    assert calculate([rows[0], wrong_close], "2026-11-30", periods=2).value is None


def test_timezone_representation_and_clock_change():
    row = observation("2026-10-30", 0.1)
    expected = calculate([row], "2026-11-02")
    assert expected.end_at == datetime(2026, 10, 30, 20, tzinfo=UTC)
    assert expected.decision_at == datetime(2026, 11, 2, 14, tzinfo=UTC)
    for zone in (ZoneInfo("America/New_York"), ZoneInfo("Europe/London"), ZoneInfo("Asia/Tokyo")):
        converted = replace(
            row,
            observed_at=row.observed_at.astimezone(zone),
            available_at=row.available_at.astimezone(zone),
        )
        assert (
            lagged_return(
                [converted], CAL, "A", expected.decision_at.astimezone(zone), return_feature=FEATURE
            )
            == expected
        )


@pytest.mark.parametrize(
    "day,periods,skip",
    [("2026-10-29", 1, 0), ("2026-10-30", 1, 0), ("2026-11-04", 4, 0), ("2026-11-04", 1, 3)],
)
def test_full_start_boundary_must_be_covered(day, periods, skip):
    with pytest.raises(CalendarCoverageError, match="insufficient"):
        calculate([], day, periods=periods, skip=skip)


@pytest.mark.parametrize(
    "stamp",
    [
        datetime(2026, 11, 4, 14),
        datetime(2026, 11, 4, 21, tzinfo=UTC),
        datetime(2026, 11, 7, 14, tzinfo=UTC),
        datetime(2026, 12, 1, 14, tzinfo=UTC),
    ],
)
def test_invalid_decisions(stamp):
    with pytest.raises(ValueError):
        lagged_return([], CAL, "A", stamp, return_feature=FEATURE)


@pytest.mark.parametrize(
    "name,value",
    [
        ("periods", 0),
        ("periods", -1),
        ("periods", True),
        ("periods", 1.0),
        ("periods", "2"),
        ("skip", -1),
        ("skip", True),
        ("skip", 1.0),
        ("skip", None),
        ("latency", -1),
        ("latency", timedelta(microseconds=-1)),
    ],
)
def test_invalid_window_arguments(name, value):
    with pytest.raises(ValueError):
        calculate([], **{name: value})


@pytest.mark.parametrize("field", ["asset", "return_feature"])
@pytest.mark.parametrize("bad", ["", " A", "A\n", "A\x7f", None, 1])
def test_invalid_identifiers(field, bad):
    args = {"asset": "A", "return_feature": FEATURE, field: bad}
    with pytest.raises(ValueError, match="identifiers"):
        lagged_return([], CAL, decision_at=session("2026-11-04").decision_at, **args)


@pytest.mark.parametrize("value", [-1.01, True, False, Fraction(1, 2)])
def test_invalid_target_return_domain(value):
    with pytest.raises(ValueError, match="target returns"):
        calculate([observation("2026-11-03", value)])


def test_duplicate_future_or_other_asset_versions_still_fail():
    for row in (observation("2026-11-04", 0.2), observation("2026-11-03", 0.2, asset="B")):
        with pytest.raises(ValueError, match="duplicate"):
            calculate([row, row])
    with pytest.raises(ValueError, match="Observation"):
        calculate([{}])


def test_result_is_frozen_and_input_sequence_is_not_retained():
    rows = [observation("2026-11-03", 0.25)]
    result = calculate(rows)
    rows.clear()
    assert result.value == 0.25 and len(result.observations) == 1
    with pytest.raises(FrozenInstanceError):
        result.value = 0


def test_overflow_and_tiny_positive_gross():
    with pytest.raises(ValueError, match="exceeds"):
        calculate([observation("2026-11-02", 1e308), observation("2026-11-03", 1e308)], periods=2)
    rows = [
        Observation("A", FEATURE, s.core_close, s.core_close, -1 + 2**-53)
        for s in CAL.sessions[1:-1]
    ]
    result = calculate(rows, "2026-11-30", periods=20)
    assert result.gross_return == 2**-1060
    assert result.value == -1  # subtraction rounds; positive gross is retained


def test_corporate_action_return_is_linkable_only_under_declared_reinvestment():
    # Explicit split/dividend arithmetic, then a separate synthetic +10% interval.
    r = action_return(100, 49, shares_per_old_share=2, cash_per_old_share=2).total_return
    assert calculate(
        [observation("2026-11-02", r), observation("2026-11-03", 0.1)], periods=2
    ).value == pytest.approx(0.1)


def test_exact_fraction_wealth_ledger_for_125_paths():
    possibilities = (Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 10), Fraction(1, 2))
    for path in product(possibilities, repeat=3):
        wealth = Fraction(100)
        rows = []
        for day, r in zip(("2026-10-30", "2026-11-02", "2026-11-03"), path, strict=True):
            wealth += wealth * r
            rows.append(observation(day, float(r)))
        result = calculate(rows, periods=3)
        assert result.value == pytest.approx(float((wealth - 100) / 100), rel=1e-12, abs=1e-12)


def test_all_eligible_windows_against_independent_index_and_wealth_oracle():
    # Index arithmetic, explicit availability filtering and Fraction wealth updates;
    # never call the production selector or previous_sessions to form expectations.
    rows = []
    exact = {}
    for index, s in enumerate(CAL.sessions[1:], 1):
        r = Fraction((index % 5) - 2, 10)
        row = Observation("A", FEATURE, s.core_close, s.core_close, float(r))
        rows.append(row)
        exact[(row.observed_at, row.available_at)] = r
        if index + 2 < len(CAL.sessions):
            revised = replace(row, available_at=CAL.sessions[index + 2].decision_at, value=0.5)
            rows.append(revised)
            exact[(revised.observed_at, revised.available_at)] = Fraction(1, 2)
    comparisons = 0
    for j, decision in enumerate(CAL.sessions):
        for periods, skip in product(range(1, 5), range(3)):
            if periods + skip + 1 > j:
                continue
            for latency in (timedelta(0), timedelta(microseconds=1)):
                ends = [CAL.sessions[k].core_close for k in range(j - skip - periods, j - skip)]
                chosen = []
                wealth = Fraction(100)
                for end in ends:
                    candidates = [
                        r
                        for r in rows
                        if r.observed_at == end and r.available_at <= decision.decision_at - latency
                    ]
                    row = max(candidates, key=lambda r: r.available_at)
                    chosen.append(row)
                    wealth += wealth * exact[(row.observed_at, row.available_at)]
                result = calculate(
                    rows, decision.day.isoformat(), periods=periods, skip=skip, latency=latency
                )
                assert result.observations == tuple(chosen)
                assert result.value == pytest.approx(float((wealth - 100) / 100), abs=1e-12)
                past = [r for r in rows if r.available_at <= decision.decision_at]
                assert (
                    calculate(
                        past, decision.day.isoformat(), periods=periods, skip=skip, latency=latency
                    )
                    == result
                )
                future_revisions = [
                    replace(
                        r, value=99, available_at=decision.decision_at + timedelta(microseconds=1)
                    )
                    for r in chosen
                ]
                assert (
                    calculate(
                        [*past, *future_revisions],
                        decision.day.isoformat(),
                        periods=periods,
                        skip=skip,
                        latency=latency,
                    )
                    == result
                )
                comparisons += 1
    assert comparisons == 420


def test_two_replays_match_archived_result(tmp_path):
    for index in range(2):
        output = tmp_path / f"result-{index}.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/lagged_return_experiment.py"),
                "--output",
                str(output),
            ],
            check=True,
            capture_output=True,
        )
        assert (
            output.read_bytes() == (ROOT / "experiments/lagged_returns/results.json").read_bytes()
        )
