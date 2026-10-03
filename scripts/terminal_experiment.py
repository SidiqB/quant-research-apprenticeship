"""Hand-check synthetic cash terminal evidence independently of membership exit."""

import argparse
import json
from dataclasses import asdict
from datetime import date
from math import isclose
from pathlib import Path

from quant_research.data.membership import MembershipHistory, MembershipInterval
from quant_research.data.terminal import HeldPosition, TerminalEvidence, value_terminal

ROOT = Path(__file__).resolve().parents[1]


def run():
    position = HeldPosition("OLD", 10, 20, date(2026, 1, 2))
    history = MembershipHistory(
        (MembershipInterval("OLD", date(2026, 1, 1), date(2026, 1, 5)),),
        date(2026, 1, 1),
        date(2026, 1, 9),
    )
    rows = []
    cases = (
        ("no_event", None, "missing_event", None, None),
        ("unknown_proceeds", None, "missing_proceeds", None, None),
        ("supported_zero", 0, "resolved", 0, -1),
        ("partial_recovery", 5, "resolved", 50, -0.75),
        ("at_reference", 20, "resolved", 200, 0),
        ("cash_premium", 25, "resolved", 250, 0.25),
    )
    for label, cash, status, expected_value, expected_return in cases:
        evidence = (
            None
            if label == "no_event"
            else TerminalEvidence("OLD", date(2026, 1, 7), cash, f"synthetic:{label}")
        )
        result = value_terminal(position, evidence)
        if result.status != status or result.terminal_value != expected_value:
            raise AssertionError(f"status or value mismatch: {label}")
        if expected_return is None:
            if result.total_return is not None:
                raise AssertionError("unknown return became numeric")
        elif result.total_return is None or not isclose(
            result.total_return, expected_return, rel_tol=1e-12, abs_tol=1e-12
        ):
            raise AssertionError(f"return mismatch: {label}")
        if result.position != position:
            raise AssertionError("holding lost during valuation")
        rows.append({"case": label, **asdict(result)})
    members = history.members_on(date(2026, 1, 5))
    wrong_holdings = [position.asset] if position.asset in members else []
    if members or wrong_holdings or len(rows) != 6:
        raise AssertionError("exit counterexample failed")
    unknown = TerminalEvidence("OLD", date(2026, 1, 7), None, "synthetic:unknown-proceeds")
    wrong_zero_return = (unknown.cash_per_share or 0) / position.reference_price - 1
    if wrong_zero_return != -1 or value_terminal(position, unknown).total_return is not None:
        raise AssertionError("zero-imputation counterexample failed")
    return {
        "data_kind": "synthetic",
        "period": "2026-01-02 reference; Jan 5 membership exit; Jan 7 event; date labels only",
        "question": "Can terminal valuation preserve holdings and distinguish missing from zero?",
        "protocol": "Six hand cases; exit-filter and zero-imputation wrong controls.",
        "members_on_exit": members,
        "wrong_exit_filtered_holdings": wrong_holdings,
        "preserved_held_asset": position.asset,
        "preserved_shares": position.shares,
        "wrong_unknown_zero_imputed_return": wrong_zero_return,
        "hand_cases_passed": len(rows),
        "cases": rows,
        "interpretation": (
            "Complete cash entitlement at par; no settlement, vintage or alpha claim."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "experiments/terminal/results.json")
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True, allow_nan=False, default=str) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(encoded, end="")
