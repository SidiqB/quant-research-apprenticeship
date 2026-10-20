"""Freshly rebuild and reproduce the five existing accounting evidence sets."""

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "OPERATIONS.md").is_file())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--evidence-dir", type=Path, default=ROOT / "experiments/portfolio_accounting")
args = parser.parse_args()
project = ROOT / "cpp/projects/portfolio_accounting"
units = [
    ("marked-wealth", "verify_marked_wealth.py", "marked_wealth.cpp"),
    ("buy-equations", "verify_buy_equations.py", "buy_equations.cpp"),
    ("account-state", "verify_account_state.py", None),
    ("validated-buy", "verify_validated_buy.py", None),
    ("buy-boundaries", "verify_buy_boundaries.py", None),
]
checks = []
with tempfile.TemporaryDirectory(prefix="accounting-reproduce-") as directory:
    build = Path(directory)
    assert not list(build.iterdir())
    for name, verifier, source in units:
        command = [sys.executable, str(ROOT / "scripts" / verifier)]
        if source is not None:
            executable = build / name
            compilation = subprocess.run(
                [
                    "c++",
                    "-std=c++17",
                    "-Wall",
                    "-Wextra",
                    "-Wpedantic",
                    "-Werror",
                    str(project / source),
                    "-o",
                    str(executable),
                ],
                capture_output=True,
                timeout=60,
            )
            assert (compilation.returncode, compilation.stdout, compilation.stderr) == (
                0,
                b"",
                b"",
            ), (name, compilation.stderr)
            command.extend(["--executable", str(executable)])
        # The remaining three verifiers each compile their own temporary C++ driver.
        result = subprocess.run(command, cwd=build, capture_output=True, timeout=90)
        assert (result.returncode, result.stderr) == (0, b""), (name, result.stderr)
        expected = (args.evidence_dir.resolve() / f"{name}.json").read_bytes()
        assert result.stdout == expected, ("Archived evidence mismatch", name)
        checks.append({"name": name, "result_sha256": hashlib.sha256(expected).hexdigest()})
print(
    json.dumps(
        {
            "study_date": "2026-10-19",
            "task": "L001f",
            "data_kind": "synthetic_reproduction",
            "fresh_cpp_builds": 5,
            "executions_per_build": 2,
            "archived_results_exact": checks,
            "existing_build_directory_used": False,
            "scope": "reproduction of isolated snapshots and buys; no sequence or timing proof",
            "personal_review": "Not yet reviewed",
        },
        indent=2,
        sort_keys=True,
    )
)
