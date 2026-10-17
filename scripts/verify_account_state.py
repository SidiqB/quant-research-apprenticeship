"""Freshly compile a fixed account struct and verify against independent amounts."""

import argparse
import json
import subprocess
import tempfile
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

HERE = Path(__file__).resolve().parents[1] / "cpp/projects/portfolio_accounting"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE / "account_state.cpp")
args = parser.parse_args()
cash = Decimal("800")
shares = 4
mark = Decimal("50")
assert cash >= 0 and shares >= 0 and mark > 0
holdings = sum((mark for _ in range(shares)), Decimal(0))
wealth = cash + holdings
assert (holdings, wealth) == (Decimal(200), Decimal(1000))
expected = (
    f"initial: cash={cash}; shares={shares}; mark={mark}; holdings={holdings}; wealth={wealth}\n"
    "empty: cash=0; shares=0; wealth=0\n"
).encode()
assert expected == (HERE / "account_state_expected.txt").read_bytes()
with tempfile.TemporaryDirectory(prefix="account-state-") as scratch:
    executable = Path(scratch) / "account_state"
    build = subprocess.run(
        [
            "c++",
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            str(args.source.resolve()),
            "-o",
            str(executable),
        ],
        capture_output=True,
        timeout=60,
    )
    assert (build.returncode, build.stdout, build.stderr) == (0, b"", b""), (
        "Account-state compilation failed or emitted diagnostics",
        build.stderr.decode(),
    )
    for _ in range(2):
        result = subprocess.run([str(executable)], capture_output=True, timeout=10)
        assert (result.stdout, result.stderr, result.returncode) == (expected, b"", 0), (
            "Account-state output/status differs from independent reference"
        )
print(
    json.dumps(
        {
            "study_date": "2026-10-15",
            "task": "L001c",
            "data_kind": "synthetic_fixed_snapshot",
            "money_unit": "whole arbitrary money unit",
            "initial_cash": str(cash),
            "initial_shares": shares,
            "mark": str(mark),
            "holdings": str(holdings),
            "wealth": str(wealth),
            "empty_cash": 0,
            "empty_shares": 0,
            "empty_wealth": 0,
            "fresh_build": True,
            "runs": 2,
            "reference": "Decimal repeated per-share addition",
            "scope": "initialized single-asset account struct; no trading or validation API",
            "personal_review": "Not yet reviewed",
        },
        indent=2,
        sort_keys=True,
    )
)
