"""Check one fixed synthetic position against independent Decimal addition."""

import argparse
import json
import subprocess
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--executable", type=Path, default=ROOT / "build/cpp/portfolio_accounting/marked_wealth"
)
args = parser.parse_args()
labels = ("initial", "higher mark", "lower mark")
marks = (Decimal("50"), Decimal("55"), Decimal("45"))
cash = Decimal("800")
shares = 4
# Independently add one marked share four times; no multiplication in this reference.
holdings = [sum((mark for _ in range(shares)), Decimal(0)) for mark in marks]
wealth = [cash + holding for holding in holdings]
assert holdings == [Decimal("200"), Decimal("220"), Decimal("180")]
assert wealth == [Decimal("1000"), Decimal("1020"), Decimal("980")]
assert wealth[1] - wealth[0] == Decimal("20")
assert wealth[2] - wealth[0] == Decimal("-20")
expected = "".join(
    f"{label}: cash={cash}; shares={shares}; mark={mark}; holdings={holding}; wealth={value}\n"
    for label, mark, holding, value in zip(labels, marks, holdings, wealth, strict=True)
).encode()
assert expected == (ROOT / "cpp/projects/portfolio_accounting/expected.txt").read_bytes()
for _ in range(2):
    result = subprocess.run([str(args.executable.resolve())], capture_output=True, timeout=10)
    assert (result.stdout, result.stderr, result.returncode) == (expected, b"", 0), (
        "Marked-wealth output/status differs from the independent reference"
    )
print(
    json.dumps(
        {
            "study_date": "2026-10-13",
            "task": "L001a",
            "data_kind": "synthetic_fixed_snapshots",
            "money_unit": "whole arbitrary money unit",
            "shares": shares,
            "cash": str(cash),
            "marks": [str(x) for x in marks],
            "holdings": [str(x) for x in holdings],
            "wealth": [str(x) for x in wealth],
            "runs": 2,
            "snapshot_comparisons_per_run": 3,
            "reference": "Decimal addition of four separately marked shares",
            "trades": 0,
            "costs": "omitted; no execution model",
            "personal_review": "Not yet reviewed",
        },
        indent=2,
        sort_keys=True,
    )
)
