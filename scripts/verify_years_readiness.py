"""Fixed-case consolidation; run from the repository root without -O."""

import hashlib
import json
import subprocess
import tempfile
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")
root = Path(__file__).resolve().parents[1]
project = root / "cpp/projects/savings_growth"
# This is the observed target from the published boundary experiment, not a C++ overflow.
maximum = json.loads((root / "experiments/years_parser/boundary-oracle.json").read_text())[
    "int_max"
]
assert maximum == 2147483647
balance = Decimal("1000") * (1 + Decimal("0.05")) ** 2
assert balance == Decimal("1102.5000")
expected = (
    "blank: spelling; calculation skipped\n"
    "zero: years=0; balance=1000.00\n"
    f"leading zeros: years=2; balance={balance:.2f}\n"
    "fraction: spelling; calculation skipped\n"
    "suffix: spelling; calculation skipped\n"
    "beyond range: range; calculation skipped\n"
    f"maximum positive rate: years={maximum}; calculation overflow; no balance\n"
    f"maximum zero rate: years={maximum}; balance=1000.00\n"
).encode()
# Independent magnitude bound: 1.05**20 > 2, and 2**1024 exceeds finite double max.
assert Decimal("1.05") ** 20 > 2 and maximum > 20 * 1024
inputs = [
    project / "readiness_trace.cpp",
    project / "years.cpp",
    project / "years.hpp",
    project / "savings.cpp",
    project / "savings.hpp",
    root / "experiments/years_parser/boundary-oracle.json",
]
with tempfile.TemporaryDirectory(prefix="readiness-") as directory:
    exe = Path(directory) / "trace"
    c = subprocess.run(
        [
            "c++",
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            "-I",
            str(project),
            str(inputs[0]),
            str(project / "years.cpp"),
            str(project / "savings.cpp"),
            "-o",
            str(exe),
        ],
        capture_output=True,
        check=True,
        timeout=60,
    )
    assert not c.stdout and not c.stderr
    for _ in range(2):
        r = subprocess.run([str(exe)], capture_output=True, timeout=10)
        assert (r.stdout, r.stderr, r.returncode) == (expected, b"", 0)
report = {
    "data_kind": "synthetic_fixed_strings",
    "study_date": "2026-10-12",
    "baseline_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "cases": 8,
    "runs": 2,
    "parser_rejections": 4,
    "finite_balances": 3,
    "accepted_then_overflow": 1,
    "int_max": maximum,
    "independent_magnitude_bound": "1.05^20 > 2; int_max > 20*1024",
    "compiler": subprocess.check_output(["c++", "--version"], text=True).splitlines()[0],
    "input_sha256": {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs
    },
    "stdout": expected.decode(),
    "personal_review": "Not yet reviewed",
}
print(json.dumps(report, indent=2, sort_keys=True))
