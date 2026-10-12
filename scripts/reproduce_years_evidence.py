"""Reproduce the existing C003a evidence in an empty temporary build directory."""

import hashlib
import json
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O: assertion checks are required")

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "OPERATIONS.md").is_file())
PROJECT = ROOT / "cpp/projects/savings_growth"
flags = ["-std=c++17", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
units = [
    ("savings-tests", "test_savings.cpp", ["savings.cpp"], []),
    ("years-tests", "test_years.cpp", ["years.cpp", "savings.cpp"], []),
    ("demo", "parse_years_demo.cpp", ["years.cpp", "savings.cpp"], []),
    ("probe", "years_probe.cpp", ["years.cpp"], []),
    ("correct", "fractional_failure.cpp", ["years.cpp", "savings.cpp"], []),
    ("wrong", "fractional_failure.cpp", ["years.cpp", "savings.cpp"], ["-DWRONG_ADAPTER"]),
]
inputs = {str((PROJECT / f).relative_to(ROOT)) for _, src, deps, _ in units for f in [src, *deps]}
inputs.update(
    [
        "cpp/projects/savings_growth/savings.hpp",
        "cpp/projects/savings_growth/years.hpp",
        "scripts/years_boundary_oracle.py",
    ]
)
checks = []
with tempfile.TemporaryDirectory(prefix="years-reproduce-") as directory:
    build = Path(directory)
    assert not list(build.iterdir())
    for name, src, deps, defines in units:
        compile_run = subprocess.run(
            [
                "c++",
                *flags,
                *defines,
                str(PROJECT / src),
                *(str(PROJECT / f) for f in deps),
                "-o",
                str(build / name),
            ],
            capture_output=True,
            check=True,
            timeout=60,
        )
        assert compile_run.stdout == compile_run.stderr == b""
    fixtures = [
        ("savings-tests", b"Savings function checks passed: 66\n", b"", 0),
        ("years-tests", b"Passed 30 whole-year parser checks\n", b"", 0),
        ("demo", (PROJECT / "parse_years_expected.txt").read_bytes(), b"", 0),
    ]
    for name, file, code, mismatches in [
        ("correct", "fractional-correct.txt", 0, 0),
        ("wrong", "fractional-negative-control.txt", 1, 3),
    ]:
        stderr = f"contract mismatches: {mismatches}\n".encode()
        combined = (ROOT / "experiments/years_parser" / file).read_bytes()
        assert combined.endswith(stderr)
        fixtures.append((name, combined[: -len(stderr)], stderr, code))
    for name, expected, error, status in fixtures:
        for _ in range(2):
            result = subprocess.run([str(build / name)], capture_output=True, timeout=10)
            assert (result.stdout, result.stderr, result.returncode) == (expected, error, status), (
                name
            )
        checks.append({"binary": name, "runs": 2, "expected_exit": status, "exact_match": True})
    expected_oracle = (ROOT / "experiments/years_parser/boundary-oracle.json").read_bytes()
    for _ in range(2):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/years_boundary_oracle.py"),
                "--probe",
                str(build / "probe"),
            ],
            capture_output=True,
            check=True,
            timeout=60,
        )
        assert result.stdout == expected_oracle and not result.stderr
    checks.append({"binary": "probe", "runs": 2, "oracle_cases_per_run": 75, "exact_match": True})

balance = Decimal("1000")
credits = []
for _ in range(2):
    credit = balance * Decimal("0.05")
    credits.append(str(credit.quantize(Decimal("0.01"))))
    balance += credit
assert credits == ["50.00", "52.50"] and balance == Decimal("1102.50")
report = {
    "data_kind": "synthetic_reproduction",
    "recipe_study_date": "2026-10-11",
    "baseline_commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip(),
    "fresh_temporary_build": True,
    "executables_compiled": len(units),
    "flags": flags,
    "compiler": subprocess.check_output(["c++", "--version"], text=True).splitlines()[0],
    "checks": checks,
    "decimal_credits": credits,
    "decimal_balance": "1102.50",
    "input_sha256": {
        f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in sorted(inputs)
    },
    "personal_review": "Not yet reviewed",
}
print(json.dumps(report, indent=2, sort_keys=True))
