"""Verify L002b hand expectations; this is reference tooling, not a trading engine."""

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "experiments/portfolio_accounting/delayed_order_contract_cases.json"
)


def reference(case):
    """Use exact per-share debits, keeping decision fields separate from resolution."""
    for key in ["cash", "shares", "observed_price", "available", "decision", "resolution"]:
        if type(case[key]) is not int:
            raise ValueError("integer domain")
    if not (0 <= case["cash"] <= 10000 and 0 <= case["shares"] <= 10000):
        raise ValueError("account domain")
    if not 1 <= case["observed_price"] <= 10000:
        raise ValueError("observation domain")
    if not 0 <= case["available"] < case["decision"] < case["resolution"]:
        raise ValueError("event order")
    fill = case["fill_price"]
    if fill is not None and (type(fill) is not int or not 1 <= fill <= 10000):
        raise ValueError("fill domain")
    quantity = 2 if case["observed_price"] <= 50 else 0
    cash, shares, fee = Decimal(case["cash"]), case["shares"], 0
    if quantity == 0:
        status = "no_order"
    elif fill is None:
        status = "unresolved"
    else:
        candidate_cash, candidate_shares = cash, shares
        for _ in range(quantity):
            candidate_cash -= Decimal(fill)
            candidate_shares += 1
        candidate_cash -= Decimal(3)
        if candidate_cash < 0 or candidate_shares > 10000:
            status = "rejected_by_model"
        else:
            status, cash, shares, fee = "filled", candidate_cash, candidate_shares, 3
    return {
        "request": quantity,
        "decision_cash": case["cash"],
        "decision_shares": case["shares"],
        "status": status,
        "cash": int(cash),
        "shares": shares,
        "fee_charged": fee,
    }


def verify(case):
    actual = reference(case)
    for key, value in case["expected"].items():
        assert actual[key] == value, f"{case['name']}: {key} mismatch"
    assert set(actual) == set(case["expected"]), "expected fields incomplete"
    return actual


def main():
    path = FIXTURE
    fixture = json.loads(path.read_text())
    assert fixture["data_kind"] == "synthetic_contract_examples"
    results = [{"name": c["name"], **verify(c)} for c in fixture["cases"]]
    invalid = []
    for label, patch, diagnostic in [
        ("same_event_observation", {"available": 1}, "event order"),
        ("future_observation", {"available": 2}, "event order"),
        ("same_event_resolution", {"resolution": 1}, "event order"),
        ("early_resolution", {"resolution": 0}, "event order"),
        ("negative_event", {"available": -1}, "event order"),
        ("zero_fill", {"fill_price": 0}, "fill domain"),
        ("negative_fill", {"fill_price": -1}, "fill domain"),
        ("boolean_fill", {"fill_price": True}, "fill domain"),
        ("fractional_cash", {"cash": 800.5}, "integer domain"),
        ("negative_cash", {"cash": -1}, "account domain"),
    ]:
        bad = copy.deepcopy(fixture["cases"][0])
        bad.update(patch)
        try:
            reference(bad)
        except ValueError as error:
            assert str(error) == diagnostic
            invalid.append(label)
        else:
            raise AssertionError(("invalid trace accepted", label))
    controls = []
    for index, label, patch in [
        (0, "debit_at_decision", {"decision_cash": 693}),
        (1, "fee_on_missing_fill", {"cash": 797, "fee_charged": 3}),
        (1, "invent_fill_at_observed_price", {"status": "filled", "cash": 697}),
        (3, "fee_on_rejection", {"cash": 103, "fee_charged": 3}),
        (4, "trade_without_request", {"status": "filled", "shares": 6}),
    ]:
        bad = copy.deepcopy(fixture["cases"][index])
        bad["expected"].update(patch)
        try:
            verify(bad)
        except AssertionError as error:
            assert "mismatch" in str(error)
            controls.append({"name": label, "diagnostic": str(error)})
        else:
            raise AssertionError(("corrupt table survived", label))
    print(
        json.dumps(
            {
                "task": "L002b",
                "study_date": "2026-10-22",
                "data_kind": "synthetic_contract_examples",
                "examples": results,
                "invalid_traces_rejected": invalid,
                "corrupt_tables_rejected": controls,
                "fixture_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "scope": (
                    "hand contract/reference only; C++ timing and invariance remain unimplemented"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
