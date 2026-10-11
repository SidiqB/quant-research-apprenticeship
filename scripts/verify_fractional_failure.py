"""Check five fixed scenarios; reject the deliberate bad adapter."""

import json
import subprocess
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build/cpp/savings_growth"
ARCHIVE = ROOT / "experiments/years_parser"
expected = (
    "002\taccepted\t2\t1102.50\n"
    "0\taccepted\t0\t1000.00\n"
    "2.5\trejected\t-\tno calculation\n"
    "0.5\trejected\t-\tno calculation\n"
    "2.0\trejected\t-\tno calculation\n"
)
wrong_expected = (
    "002\taccepted\t2\t1102.50\n"
    "0\taccepted\t0\t1000.00\n"
    "2.5\taccepted\t2\t1102.50\n"
    "0.5\taccepted\t0\t1000.00\n"
    "2.0\taccepted\t2\t1102.50\n"
)
for name, archive, output, exit_code, mismatches in [
    ("correct", "fractional-correct.txt", expected, 0, 0),
    ("wrong", "fractional-negative-control.txt", wrong_expected, 1, 3),
]:
    binary = BUILD / f"fractional-{name}"
    runs = [subprocess.run([str(binary)], capture_output=True, timeout=10) for _ in range(2)]
    for run in runs:
        assert run.returncode == exit_code, (name, run.returncode, run.stderr)
        assert run.stdout == output.encode("ascii"), (name, run.stdout)
        assert run.stderr == f"contract mismatches: {mismatches}\n".encode("ascii"), run.stderr
    assert (ARCHIVE / archive).read_bytes() == runs[0].stdout + runs[0].stderr

principal = Decimal("1000")
rate = Decimal("0.05")
balance = principal * (1 + rate) ** 2
assert balance == Decimal("1102.50")
assert principal * (1 + rate) ** 0 == Decimal("1000")
print(
    json.dumps(
        {
            "data_kind": "synthetic_fixed_strings",
            "correct_cases": 5,
            "correct_accepted": 2,
            "correct_rejected_before_calculation": 3,
            "wrong_adapter_contract_mismatches": 3,
            "wrong_adapter_exit_code": 1,
            "runs_per_binary": 2,
            "decimal_two_year_balance": str(balance.quantize(Decimal("0.01"))),
            "no_fractional_year_balance_defined": True,
        },
        indent=2,
        sort_keys=True,
    )
)
