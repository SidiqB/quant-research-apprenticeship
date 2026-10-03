"""Synthetic terminal evidence: hand values, missingness and independent accounting."""

import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime
from fractions import Fraction
from itertools import product
from pathlib import Path

import pytest

from quant_research.data.membership import MembershipHistory, MembershipInterval
from quant_research.data.terminal import HeldPosition, TerminalEvidence, value_terminal

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = date(2026, 1, 2)
EVENT = date(2026, 1, 7)
POSITION = HeldPosition("OLD", 10, 20, REFERENCE)


def evidence(cash):
    return TerminalEvidence("OLD", EVENT, cash, "synthetic:complete-cash")


@pytest.mark.parametrize(
    "cash,value,total_return", [(0, 0, -1), (5, 50, -0.75), (20, 200, 0), (25, 250, 0.25)]
)
def test_hand_cash_examples(cash, value, total_return):
    result = value_terminal(POSITION, evidence(cash))
    assert result.status == "resolved"
    assert result.reference_value == 200
    assert result.terminal_value == value
    assert result.total_return == pytest.approx(total_return, rel=1e-12, abs=1e-12)
    assert result.position is POSITION
    assert result.evidence == evidence(cash)


@pytest.mark.parametrize(
    "record,status", [(None, "missing_event"), (evidence(None), "missing_proceeds")]
)
def test_missing_values_retain_the_position(record, status):
    result = value_terminal(POSITION, record)
    assert result.status == status
    assert result.position is POSITION
    assert result.evidence == record
    assert result.reference_value == 200
    assert result.terminal_value is None
    assert result.total_return is None
    assert value_terminal(POSITION, evidence(0)).total_return == -1


@pytest.mark.parametrize("asset", ["", " OLD", "OLD ", "A B", "A\nB", "A\x00", 1, None])
def test_bad_security_ids_reject(asset):
    with pytest.raises(ValueError, match="asset"):
        replace(POSITION, asset=asset)
    with pytest.raises(ValueError, match="asset"):
        replace(evidence(0), asset=asset)


@pytest.mark.parametrize("ref", ["", " ", "bad ref", "bad\nref", 7, None])
def test_evidence_locator_is_required(ref):
    with pytest.raises(ValueError, match="evidence_ref"):
        replace(evidence(0), evidence_ref=ref)


@pytest.mark.parametrize("value", [True, None, "20", -1, float("inf"), float("nan"), 10**400])
@pytest.mark.parametrize("field", ["shares", "reference_price"])
def test_invalid_position_numbers(field, value):
    with pytest.raises(ValueError):
        replace(POSITION, **{field: value})


@pytest.mark.parametrize("field", ["shares", "reference_price"])
def test_zero_position_inputs_reject(field):
    with pytest.raises(ValueError):
        replace(POSITION, **{field: 0})


@pytest.mark.parametrize("value", [True, "0", -1, float("inf"), float("nan"), 10**400])
def test_invalid_cash_rejects_instead_of_becoming_unknown(value):
    with pytest.raises(ValueError):
        evidence(value)


@pytest.mark.parametrize("value", [None, "2026-01-07", datetime(2026, 1, 7)])
def test_dates_do_not_silently_drop_time_or_coerce(value):
    with pytest.raises(ValueError):
        replace(POSITION, priced_on=value)
    with pytest.raises(ValueError):
        replace(evidence(0), event_date=value)


@pytest.mark.parametrize("cash", [None, 0, 5])
def test_other_security_evidence_cannot_resolve_position(cash):
    with pytest.raises(ValueError, match="asset must match"):
        value_terminal(POSITION, replace(evidence(cash), asset="NEW"))


@pytest.mark.parametrize("day", [date(2026, 1, 1), REFERENCE])
@pytest.mark.parametrize("cash", [None, 0, 5])
def test_prior_or_same_day_events_reject(day, cash):
    with pytest.raises(ValueError, match="must follow"):
        value_terminal(POSITION, replace(evidence(cash), event_date=day))


def test_later_event_and_extreme_dates_are_supported():
    position = replace(POSITION, priced_on=date.min)
    result = value_terminal(position, replace(evidence(5), event_date=date.max))
    assert result.total_return == -0.75


@pytest.mark.parametrize(
    "position,record", [(None, None), ("OLD", None), (POSITION, {}), (POSITION, 0)]
)
def test_wrong_record_types_reject(position, record):
    with pytest.raises(ValueError):
        value_terminal(position, record)


@pytest.mark.parametrize("shares,price", [(1e308, 20), (1e-300, 1e-300)])
def test_reference_value_range(shares, price):
    with pytest.raises(ValueError, match="numeric range"):
        HeldPosition("OLD", shares, price, REFERENCE)


@pytest.mark.parametrize(
    "shares,price,cash",
    [
        (1e308, 1, 2),  # terminal value overflow
        (1, 1e-300, 1e300),  # gross return overflow
        (1e-300, 1e300, 1e-300),  # terminal value underflow
        (1, 1e300, 1e-300),  # gross return underflow
    ],
)
def test_terminal_range_failures(shares, price, cash):
    position = HeldPosition("OLD", shares, price, REFERENCE)
    with pytest.raises(ValueError, match="numeric range"):
        value_terminal(position, evidence(cash))


def test_zero_proceeds_are_not_mistaken_for_underflow():
    result = value_terminal(HeldPosition("OLD", 1e-300, 1, REFERENCE), evidence(0))
    assert result.terminal_value == 0
    assert result.total_return == -1


def test_records_and_results_reject_mutation():
    result = value_terminal(POSITION, evidence(None))
    for obj, field, value in [
        (POSITION, "shares", 0),
        (result.evidence, "cash_per_share", 0),
        (result, "terminal_value", 0),
    ]:
        with pytest.raises(FrozenInstanceError):
            setattr(obj, field, value)


def test_membership_exit_is_neither_a_sale_nor_terminal_evidence():
    history = MembershipHistory(
        (MembershipInterval("OLD", date(2026, 1, 1), date(2026, 1, 5)),),
        date(2026, 1, 1),
        date(2026, 1, 9),
    )
    holdings = (POSITION,)
    assert history.members_on(REFERENCE) == ("OLD",)
    assert history.members_on(date(2026, 1, 5)) == ()
    assert tuple(p for p in holdings if p.asset in history.members_on(EVENT)) == ()
    assert holdings == (POSITION,)
    assert value_terminal(holdings[0], None).terminal_value is None
    assert value_terminal(holdings[0], evidence(5)).terminal_value == 50
    assert holdings[0].shares == 10


def test_exact_fraction_ledger_and_currency_scaling():
    checks = 0
    for shares, price, cash, scale in product(
        (Fraction(1, 4), Fraction(1), Fraction(10)),
        (1, 20, 100),
        (0, 1, 5, 125),
        (Fraction(1, 100), Fraction(1), Fraction(100)),
    ):
        # Exact debit/credit ledger, with no floating arithmetic in the oracle.
        debit = shares * price * scale
        credit = shares * cash * scale
        profit = credit - debit
        position = HeldPosition("OLD", float(shares), float(price * scale), REFERENCE)
        result = value_terminal(position, evidence(float(cash * scale)))
        assert result.reference_value == pytest.approx(float(debit), rel=1e-12, abs=1e-12)
        assert result.terminal_value == pytest.approx(float(credit), rel=1e-12, abs=1e-12)
        assert result.total_return == pytest.approx(float(profit / debit), rel=1e-12, abs=1e-12)
        checks += 1
    assert checks == 108


def test_experiment_replays_twice(tmp_path):
    archived = (ROOT / "experiments/terminal/results.json").read_bytes()
    for index in range(2):
        output = tmp_path / f"terminal-{index}.json"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/terminal_experiment.py"), "--output", str(output)],
            check=True,
            capture_output=True,
        )
        assert output.read_bytes() == archived
    result = json.loads(archived)
    assert result["data_kind"] == "synthetic"
    assert result["hand_cases_passed"] == 6
    assert result["wrong_exit_filtered_holdings"] == []
    assert result["preserved_shares"] == 10
    assert [row["terminal_value"] for row in result["cases"]] == [None, None, 0, 50, 200, 250]
