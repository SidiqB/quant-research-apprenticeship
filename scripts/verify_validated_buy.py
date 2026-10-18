"""Compile one bounded buy operation; check hand-authored transitions twice."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--source", type=Path, default=ROOT / "cpp/projects/portfolio_accounting/validated_buy.cpp"
)
args = parser.parse_args()
# name, starting cash/shares, quantity/price/fee, accepted, final cash/shares.
# Explicit expected outputs are hand calculations, not the C++ rejection algorithm.
cases = [
    ("buy", 800, 4, 2, 50, 3, True, 697, 6),
    ("exact_cash", 103, 4, 2, 50, 3, True, 0, 6),
    ("fee_unaffordable", 102, 4, 2, 50, 3, False, 102, 4),
    ("fee_exceeds_cash", 2, 4, 1, 1, 3, False, 2, 4),
    ("zero_quantity", 800, 4, 0, 50, 3, False, 800, 4),
    ("negative_quantity", 800, 4, -1, 50, 3, False, 800, 4),
    ("zero_price", 800, 4, 2, 0, 3, False, 800, 4),
    ("negative_fee", 800, 4, 2, 50, -1, False, 800, 4),
    ("invalid_cash", -1, 4, 2, 50, 3, False, -1, 4),
    ("invalid_shares", 800, -1, 2, 50, 3, False, 800, -1),
    ("outside_domain", 10001, 4, 2, 50, 3, False, 10001, 4),
    ("position_cap", 800, 10000, 1, 50, 3, False, 800, 10000),
    ("zero_fee", 100, 0, 2, 50, 0, True, 0, 2),
    ("large_product_rejected", 10000, 0, 10000, 10000, 0, False, 10000, 0),
]
expected_lines = []
body = []
for name, cash, shares, quantity, price, fee, accepted, final_cash, final_shares in cases:
    if accepted:
        assert final_cash == cash - sum(price for _ in range(quantity)) - fee
        assert final_shares == shares + quantity
        assert final_cash + final_shares * price == cash + shares * price - fee
    else:
        assert (final_cash, final_shares) == (cash, shares)
    expected_lines.append(f"{name} {int(accepted)} {final_cash} {final_shares}")
    body.append(
        f"{{ AccountState s{{{cash}, {shares}}}; bool ok = try_buy(s, {quantity}, "
        f'{price}, {fee}); std::cout << "{name} " << ok << " " << s.cash_units '
        '<< " " << s.shares << "\\n"; }'
    )
expected = ("\n".join(expected_lines) + "\n").encode()
with tempfile.TemporaryDirectory(prefix="validated-buy-") as scratch:
    root = Path(scratch)
    source = root / "probe.cpp"
    source.write_text(
        "#include <iostream>\n"
        + args.source.read_text()
        + "\nint main() {\n"
        + "\n".join(body)
        + "\n}\n"
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
        result = subprocess.run([str(executable)], capture_output=True, timeout=10)
        assert (result.returncode, result.stdout, result.stderr) == (0, expected, b""), (
            "Buy transition differs from hand reference",
            result.stdout,
            result.stderr,
        )
print(
    json.dumps(
        {
            "study_date": "2026-10-17",
            "task": "L001d",
            "data_kind": "synthetic_fixed_cases",
            "cases": len(cases),
            "accepted": sum(c[6] for c in cases),
            "rejected_unchanged": sum(not c[6] for c in cases),
            "runs": 2,
            "fresh_build": True,
            "undefined_behavior_sanitizer": True,
            "outputs": expected_lines,
            "scope": "bounded whole-unit buy; no execution timing or market claim",
            "personal_review": "Not yet reviewed",
        },
        indent=2,
        sort_keys=True,
    )
)
