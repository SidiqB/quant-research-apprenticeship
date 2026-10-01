"""Independent wealth oracles and invalid-input controls for synthetic actions."""

import json
import subprocess
import sys
from dataclasses import FrozenInstanceError
from fractions import Fraction
from itertools import product
from pathlib import Path

import pytest

from quant_research.data.corporate_actions import action_return

ROOT = Path(__file__).resolve().parents[1]
BASE = dict(start_price=100, end_price=49, shares_per_old_share=2, cash_per_old_share=2)


@pytest.mark.parametrize(
    "start,end,ratio,cash,raw,capital,income,total",
    [
        (100, 110, 1, 0, 0.10, 0.10, 0, 0.10),
        (100, 90, 1, 0, -0.10, -0.10, 0, -0.10),
        (100, 50, 2, 0, -0.50, 0, 0, 0),
        (20, 100, 0.2, 0, 4, 0, 0, 0),
        (100, 98, 1, 2, -0.02, -0.02, 0.02, 0),
        (100, 103, 1, 2, 0.03, 0.03, 0.02, 0.05),
        (100, 49, 2, 2, -0.51, -0.02, 0.02, 0),
        (100, 54, 2, 2, -0.46, 0.08, 0.02, 0.10),
    ],
)
def test_hand_calculated_components(start, end, ratio, cash, raw, capital, income, total):
    result = action_return(start, end, shares_per_old_share=ratio, cash_per_old_share=cash)
    assert result.raw_price_return == pytest.approx(raw, rel=1e-12, abs=1e-12)
    assert result.capital_return == pytest.approx(capital, rel=1e-12, abs=1e-12)
    assert result.income_return == pytest.approx(income, rel=1e-12, abs=1e-12)
    assert result.total_return == pytest.approx(total, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize("field", BASE)
@pytest.mark.parametrize("bad", [None, True, "2", float("nan"), float("inf"), -float("inf"), -1])
def test_invalid_input(field, bad):
    values = {**BASE, field: bad}
    with pytest.raises(ValueError, match=field):
        action_return(**values)


@pytest.mark.parametrize("field", ["start_price", "end_price", "shares_per_old_share"])
def test_zero_price_or_ratio_is_not_missing_or_terminal_evidence(field):
    with pytest.raises(ValueError, match=field):
        action_return(**{**BASE, field: 0})


@pytest.mark.parametrize("field", ["shares_per_old_share", "cash_per_old_share"])
def test_unknown_action_cannot_default_to_no_action(field):
    values = BASE.copy()
    del values[field]
    with pytest.raises(TypeError):
        action_return(**values)


@pytest.mark.parametrize(
    "changes",
    [
        {"end_price": 1e308, "shares_per_old_share": 2},
        {"end_price": 1e308, "shares_per_old_share": 1, "cash_per_old_share": 1e308},
        {"start_price": 1e-308},
        {"end_price": 5e-324, "shares_per_old_share": 0.1},
        {"start_price": 1e308, "end_price": 1e-308},
        {"start_price": 1e308, "cash_per_old_share": 1e-308},
        {"start_price": 10**400},
    ],
)
def test_numeric_range_failure_is_explicit(changes):
    with pytest.raises(ValueError, match="range"):
        action_return(**{**BASE, **changes})


def test_exact_fraction_holdings_oracle_and_currency_scale():
    checks = 0
    for start, end, ratio, cash in product(
        (20, 100, 250), (10, 50, 120), (Fraction(1, 5), Fraction(1), Fraction(2)), (0, 2)
    ):
        opening_shares = 15
        opening_wealth = opening_shares * start
        closing_shares = opening_shares * ratio
        dividend_entitlement = opening_shares * cash
        expected = (closing_shares * end + dividend_entitlement - opening_wealth) / opening_wealth
        for scale in (Fraction(1, 100), Fraction(1), Fraction(100)):
            result = action_return(
                float(start * scale),
                float(end * scale),
                shares_per_old_share=float(ratio),
                cash_per_old_share=float(cash * scale),
            )
            assert result.total_return == pytest.approx(float(expected), rel=1e-12, abs=1e-12)
            assert result.capital_return + result.income_return == pytest.approx(
                result.total_return, rel=1e-12, abs=1e-12
            )
            checks += 1
    assert checks == 162


def test_pre_and_post_split_dividend_units_must_be_converted():
    # A 1-unit dividend on each of two ending shares equals 2 per opening share.
    correct = action_return(**BASE)
    wrong = action_return(**{**BASE, "cash_per_old_share": 1})
    assert correct.total_return == 0
    assert wrong.total_return == pytest.approx(-0.01)


def test_result_is_immutable():
    result = action_return(**BASE)
    with pytest.raises(FrozenInstanceError):
        result.total_return = 2


def test_experiment_replays_twice_and_matches_hand_results(tmp_path):
    archived = (ROOT / "experiments/corporate_actions/results.json").read_bytes()
    for index in range(2):
        output = tmp_path / f"result-{index}.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/corporate_action_experiment.py"),
                "--output",
                str(output),
            ],
            check=True,
            capture_output=True,
        )
        assert output.read_bytes() == archived
    result = json.loads(archived)
    assert result["data_kind"] == "synthetic"
    assert result["hand_cases_passed"] == 8
    assert result["wrong_controls_detected"] == 3
    assert result["wrong_control_returns_expected_zero"] == pytest.approx(
        {"ignore_split": -0.5, "invert_split": -0.75, "double_count_dividend_after_split": 0.02}
    )
