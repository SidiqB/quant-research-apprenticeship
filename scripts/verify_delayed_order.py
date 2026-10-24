"""Compare one C++ delayed-order fragment with hand cases and a Decimal reference."""

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_event_contract import reference  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=ROOT / "cpp/projects/portfolio_accounting/delayed_order.cpp"
    )
    args = parser.parse_args()
    fixture = ROOT / "experiments/portfolio_accounting/delayed_order_contract_cases.json"
    cases = json.loads(fixture.read_text())["cases"]
    # Two additional hand anchors; each trace starts with a fresh account.
    for index, name, patch, expected in [
        (
            4,
            "no_request_missing",
            {"fill_price": None},
            {
                "request": 0,
                "decision_cash": 800,
                "decision_shares": 4,
                "status": "no_order",
                "cash": 800,
                "shares": 4,
                "fee_charged": 0,
            },
        ),
        (
            2,
            "exact_position_cap",
            {"shares": 9998},
            {
                "request": 2,
                "decision_cash": 107,
                "decision_shares": 9998,
                "status": "filled",
                "cash": 0,
                "shares": 10000,
                "fee_charged": 3,
            },
        ),
    ]:
        case = copy.deepcopy(cases[index])
        case.update(name=name, expected=expected, **patch)
        cases.append(case)
    invalid = []
    for name, patch in [
        ("equal_observation", {"available": 1}),
        ("future_observation", {"available": 2}),
        ("equal_resolution", {"resolution": 1}),
        ("early_resolution", {"resolution": 0}),
        ("negative_event", {"available": -1}),
        ("zero_observed", {"observed_price": 0}),
        ("large_observed", {"observed_price": 10001}),
        ("negative_cash", {"cash": -1}),
        ("large_cash", {"cash": 10001}),
        ("negative_shares", {"shares": -1}),
        ("large_shares", {"shares": 10001}),
        ("zero_fill", {"fill_price": 0}),
        ("negative_fill", {"fill_price": -1}),
        ("large_fill", {"fill_price": 10001}),
        ("malformed_fill_no_request", {"observed_price": 51, "fill_price": 0}),
    ]:
        case = copy.deepcopy(cases[0])
        case.update(name=name, **patch)
        try:
            reference(case)
        except ValueError:
            invalid.append(case)
        else:
            raise AssertionError(("invalid reference accepted", name))
    expected_lines, body = [], []
    for i, case in enumerate(cases + invalid):
        valid = i < len(cases)
        if valid:
            expected = reference(case)
            assert expected == case["expected"], (case["name"], expected)
        else:
            expected = dict(
                request=-1,
                decision_cash=case["cash"],
                decision_shares=case["shares"],
                status="invalid_trace",
                cash=case["cash"],
                shares=case["shares"],
                fee_charged=0,
            )
        fields = [
            case["name"],
            int(valid),
            expected["request"],
            expected["decision_cash"],
            expected["decision_shares"],
            expected["status"],
            expected["cash"],
            expected["shares"],
            expected["fee_charged"],
            case["cash"],
            case["shares"],
        ]
        expected_lines.append(" ".join(map(str, fields)))
        fill = case["fill_price"]
        # Reject incompatible raw types before rendering C++ int literals; this is no CLI.
        ints = [
            case[k]
            for k in ["cash", "shares", "observed_price", "available", "decision", "resolution"]
        ]
        assert all(type(v) is int for v in ints)
        assert fill is None or type(fill) is int
        cash, shares, observed, available, decision, resolution = ints
        has_fill = "false" if fill is None else "true"
        price = 0 if fill is None else fill
        body.append(
            f"{{ AccountState initial{{{cash}, {shares}}}; "
            f"auto t = delayed_order(initial, {observed}, {available}, {decision}, "
            f"{resolution}, {has_fill}, {price}); "
            f'std::cout << "{case["name"]} " << t.valid << " " << t.request '
            '<< " " << t.at_decision.cash_units << " " << t.at_decision.shares '
            '<< " " << t.status << " " << t.after_resolution.cash_units '
            '<< " " << t.after_resolution.shares << " " << t.fee_charged '
            '<< " " << initial.cash_units << " " << initial.shares << "\\n"; }'
        )
    expected_output = ("\n".join(expected_lines) + "\n").encode()
    buy = ROOT / "cpp/projects/portfolio_accounting/validated_buy.cpp"
    with tempfile.TemporaryDirectory(prefix="delayed-order-") as tmp:
        source, binary = Path(tmp) / "probe.cpp", Path(tmp) / "probe"
        source.write_text(
            "#include <iostream>\n"
            + buy.read_text()
            + "\n"
            + args.source.read_text()
            + "\nint main() {\n"
            + "\n".join(body)
            + "\n}\n"
        )
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
                str(binary),
            ],
            capture_output=True,
            timeout=60,
        )
        assert (build.returncode, build.stdout, build.stderr) == (0, b"", b""), build.stderr
        for _ in range(2):
            run = subprocess.run([str(binary)], capture_output=True, timeout=10)
            assert (run.returncode, run.stdout, run.stderr) == (0, expected_output, b""), (
                "Delayed trace differs from hand/reference",
                run.stdout,
                run.stderr,
            )
    print(
        json.dumps(
            {
                "task": "L002c",
                "study_date": "2026-10-23",
                "data_kind": "synthetic_fixed_traces",
                "hand_cases": len(cases),
                "invalid_integer_traces": len(invalid),
                "runs_per_build": 2,
                "fresh_build": True,
                "undefined_behavior_sanitizer": True,
                "caller_state_unchanged": True,
                "outputs": expected_lines,
                "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
                "buy_sha256": hashlib.sha256(buy.read_bytes()).hexdigest(),
                "fixture_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
                "scope": "one complete trace; no general future-price invariance proof",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
