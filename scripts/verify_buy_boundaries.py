"""Compare bounded C++ buys with a direct integer-ledger oracle."""

import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--source",
    type=Path,
    default=ROOT / "cpp/projects/portfolio_accounting/validated_buy.cpp",
)
args = parser.parse_args()
# Tuple order: starting cash, starting shares, quantity, price, separate fee.
edges = (-1, 0, 1, 9999, 10000, 10001)
cases = set(itertools.product(edges, repeat=5))
# Isolate affordability equality and either side for useful interior quantities.
for quantity, price, fee, shares in itertools.product(
    (1, 2, 7, 99), (1, 3, 50, 101), (0, 1, 3), (0, 4, 9999, 10000)
):
    debit = quantity * price + fee
    for cash in (debit - 1, debit, debit + 1):
        cases.add((cash, shares, quantity, price, fee))
# Isolate position capacity at its last available share and either side.
for quantity in (1, 2, 7, 9999, 10000):
    for shares in (10000 - quantity - 1, 10000 - quantity, 10000 - quantity + 1):
        cases.add((10000, shares, quantity, 1, 0))
cases = sorted(cases)


def oracle(case):
    cash, shares, quantity, price, fee = case
    # Python integers can evaluate the direct product without fixed-width overflow.
    # Decide from the post-trade ledger, not C++'s quotient/cap-subtraction guards.
    remaining_cash = cash - quantity * price - fee
    final_shares = shares + quantity
    valid_domain = all(0 <= x <= 10000 for x in (cash, shares, fee)) and all(
        1 <= x <= 10000 for x in (quantity, price)
    )
    accepted = valid_domain and remaining_cash >= 0 and final_shares <= 10000
    if not accepted:
        return (0, cash, shares)
    assert remaining_cash + final_shares * price == cash + shares * price - fee
    return (1, remaining_cash, final_shares)


# Hand anchors constrain the oracle independently of generated counts.
assert oracle((102, 4, 2, 50, 3)) == (0, 102, 4)
assert oracle((103, 4, 2, 50, 3)) == (1, 0, 6)
assert oracle((104, 4, 2, 50, 3)) == (1, 1, 6)
assert oracle((1, 9999, 1, 1, 0)) == (1, 0, 10000)
assert oracle((1, 10000, 1, 1, 0)) == (0, 1, 10000)
assert oracle((100, 0, 1, -1, 0)) == (0, 100, 0)
expected = [oracle(case) for case in cases]
input_bytes = ("\n".join(" ".join(map(str, row)) for row in cases) + "\n").encode()
expected_bytes = ("\n".join(" ".join(map(str, row)) for row in expected) + "\n").encode()
with tempfile.TemporaryDirectory(prefix="buy-boundaries-") as scratch:
    root = Path(scratch)
    source = root / "probe.cpp"
    source.write_text(
        "#include <iostream>\n" + args.source.read_text() + "\n"
        "int main() {\n"
        "int cash, shares, quantity, price, fee;\n"
        "while (std::cin >> cash >> shares >> quantity >> price >> fee) {\n"
        "AccountState state{cash, shares};\n"
        "bool accepted = try_buy(state, quantity, price, fee);\n"
        'std::cout << accepted << " " << state.cash_units << " " << state.shares << "\\n";\n'
        "}\nreturn std::cin.eof() ? 0 : 2;\n}\n"
    )
    executable = root / "probe"
    build = subprocess.run(
        [
            "c++",
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            "-fsanitize=undefined",
            "-fno-sanitize-recover=all",
            str(source),
            "-o",
            str(executable),
        ],
        capture_output=True,
        timeout=60,
    )
    assert (build.returncode, build.stdout, build.stderr) == (0, b"", b""), build.stderr
    for _ in range(2):
        run = subprocess.run(
            [str(executable)],
            input=input_bytes,
            capture_output=True,
            timeout=30,
        )
        assert (run.returncode, run.stderr) == (0, b""), (run.returncode, run.stderr)
        actual = run.stdout.splitlines()
        assert len(actual) == len(expected), "Boundary output count mismatch"
        for case, want, got in zip(cases, expected_bytes.splitlines(), actual, strict=True):
            assert want == got, ("Boundary mismatch", case, want, got)
print(
    json.dumps(
        {
            "study_date": "2026-10-18",
            "task": "L001e",
            "data_kind": "synthetic_generated_boundaries",
            "cases": len(cases),
            "edge_grid_cases": len(edges) ** 5,
            "additional_unique_cases": len(cases) - len(edges) ** 5,
            "accepted": sum(row[0] for row in expected),
            "rejected_unchanged": sum(not row[0] for row in expected),
            "runs": 2,
            "fresh_build": True,
            "undefined_behavior_sanitizer": True,
            "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
            "expected_output_sha256": hashlib.sha256(expected_bytes).hexdigest(),
            "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
            "scope": "selected grid and threshold neighbors; not exhaustive domain proof",
            "personal_review": "Not yet reviewed",
        },
        indent=2,
        sort_keys=True,
    )
)
