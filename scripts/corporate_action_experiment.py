"""Hand-check synthetic split/dividend returns; no market data or alpha."""

import argparse
import json
from dataclasses import asdict
from math import isclose
from pathlib import Path

from quant_research.data.corporate_actions import action_return

ROOT = Path(__file__).resolve().parents[1]
# label, raw opening/closing price, ending shares per old share, cash per old share,
# hand-calculated total return. Cash is entitlement valued at par, without reinvestment.
CASES = (
    ("no_action_gain", 100, 110, 1, 0, 0.10),
    ("no_action_loss", 100, 90, 1, 0, -0.10),
    ("two_for_one_split", 100, 50, 2, 0, 0.0),
    ("one_for_five_reverse_split", 20, 100, 0.2, 0, 0.0),
    ("cash_dividend_offset", 100, 98, 1, 2, 0.0),
    ("dividend_and_gain", 100, 103, 1, 2, 0.05),
    ("split_and_dividend", 100, 49, 2, 2, 0.0),
    ("split_dividend_and_gain", 100, 54, 2, 2, 0.10),
)


def run():
    rows = []
    for label, start, end, ratio, cash, expected in CASES:
        actual = action_return(start, end, shares_per_old_share=ratio, cash_per_old_share=cash)
        if not isclose(actual.total_return, expected, rel_tol=1e-12, abs_tol=1e-12):
            raise AssertionError(f"hand value mismatch: {label}")
        rows.append(
            {
                "case": label,
                "start_price": start,
                "end_price": end,
                "shares_per_old_share": ratio,
                "cash_per_old_share": cash,
                "expected_total_return": expected,
                **asdict(actual),
            }
        )
    wrong_controls = {
        "ignore_split": 50 / 100 - 1,
        "invert_split": (50 / 2) / 100 - 1,
        "double_count_dividend_after_split": (2 * (49 + 2)) / 100 - 1,
    }
    if any(isclose(value, 0, abs_tol=1e-12) for value in wrong_controls.values()):
        raise AssertionError("a deliberately wrong zero-return control escaped")
    return {
        "data_kind": "synthetic",
        "period": "undated single holding intervals; no empirical sample",
        "question": "Can explicit share/cash units reconcile split and dividend returns?",
        "protocol": "Eight hand totals; three wrong controls; tolerance 1e-12.",
        "cash_convention": "known entitlement per opening share, valued at par; no reinvestment",
        "cases": rows,
        "wrong_control_returns_expected_zero": wrong_controls,
        "hand_cases_passed": len(rows),
        "wrong_controls_detected": len(wrong_controls),
        "interpretation": "Arithmetic validation only; no vendor admission or alpha claim.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "experiments/corporate_actions/results.json"
    )
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True, allow_nan=False) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(encoded, end="")
