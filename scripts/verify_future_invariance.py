"""Check selected future-suffix invariance in the unchanged delayed C++ order."""

import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from verify_event_contract import reference

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "cpp/projects/portfolio_accounting/delayed_order.cpp"
BUY = ROOT / "cpp/projects/portfolio_accounting/validated_buy.cpp"
FIXTURE = ROOT / "experiments/portfolio_accounting/future_invariance_cases.json"


def cases_from_fixture(fixture):
    cases = []
    for observed, account, fill, resolution in itertools.product(
        fixture["observed_prices"],
        fixture["accounts"],
        fixture["fill_prices"],
        fixture["resolution_events"],
    ):
        case = dict(
            cash=account[0],
            shares=account[1],
            observed_price=observed,
            available=0,
            decision=1,
            resolution=resolution,
            fill_price=fill,
        )
        reference(case)  # Validate types and complete-trace domain before C++ literals.
        cases.append(case)
    assert len(cases) == 360 and len({tuple(c.values()) for c in cases}) == 360
    for anchor in fixture["hand_anchors"]:
        assert anchor["input"] in cases
        assert reference(anchor["input"]) == anchor["expected"], "Hand anchor differs"
    return cases


def probe(source_text, cases):
    body = []
    for i, case in enumerate(cases):
        fill = case["fill_price"]
        has_fill = "false" if fill is None else "true"
        body.append(
            f"{{ AccountState initial{{{case['cash']}, {case['shares']}}}; "
            f"auto t = delayed_order(initial, {case['observed_price']}, 0, 1, "
            f"{case['resolution']}, {has_fill}, {0 if fill is None else fill}); "
            f'std::cout << {i} << " " << t.valid << " " << t.request '
            '<< " " << t.at_decision.cash_units << " " << t.at_decision.shares '
            '<< " " << t.status << " " << t.after_resolution.cash_units '
            '<< " " << t.after_resolution.shares << " " << t.fee_charged '
            '<< " " << initial.cash_units << " " << initial.shares << "\\n"; }'
        )
    with tempfile.TemporaryDirectory(prefix="future-invariance-") as tmp:
        cpp, binary = Path(tmp) / "probe.cpp", Path(tmp) / "probe"
        cpp.write_text(
            "#include <iostream>\n"
            + BUY.read_text()
            + "\n"
            + source_text
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
                str(cpp),
                "-o",
                str(binary),
            ],
            capture_output=True,
            timeout=60,
        )
        assert (build.returncode, build.stdout, build.stderr) == (0, b"", b""), build.stderr
        outputs = []
        for _ in range(2):
            run = subprocess.run([str(binary)], capture_output=True, timeout=10)
            assert (run.returncode, run.stderr) == (0, b""), "Runtime failure"
            outputs.append(run.stdout)
    assert outputs[0] == outputs[1], "Replay differs"
    rows = []
    for line in outputs[0].decode().splitlines():
        fields = line.split()
        assert len(fields) == 11, "Malformed trace output"
        rows.append([int(x) if j != 5 else x for j, x in enumerate(fields)])
    assert len(rows) == len(cases), "Missing trace"
    return rows, outputs[0]


def verify(rows, cases):
    baselines = {}
    comparisons = 0
    for i, (row, case) in enumerate(zip(rows, cases, strict=True)):
        assert row[:2] == [i, 1], "Trace validity differs"
        key = (case["observed_price"], case["cash"], case["shares"])
        # Compare actual C++ observations across futures before checking an oracle.
        projection = row[2:5]
        if key in baselines:
            assert projection == baselines[key], f"Past projection changed: trace {i}"
            comparisons += 1
        else:
            baselines[key] = projection
    for row, case in zip(rows, cases, strict=True):
        request = 2 if case["observed_price"] <= 50 else 0
        assert row[2:5] == [request, case["cash"], case["shares"]], "Decision anchor differs"
        assert row[9:] == [case["cash"], case["shares"]], "Caller state changed"
        expected = reference(case)
        assert row[5:9] == [expected[k] for k in ("status", "cash", "shares", "fee_charged")], (
            "Resolution differs from Decimal reference"
        )
    assert len(baselines) == 20 and comparisons == 340
    return comparisons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--skip-controls", action="store_true")
    args = parser.parse_args()
    fixture = json.loads(FIXTURE.read_text())
    cases = cases_from_fixture(fixture)
    source = args.source.read_text()
    rows, output = probe(source, cases)
    comparisons = verify(rows, cases)
    controls = []
    if not args.skip_controls:
        call = "decide_quantity(observed_price, available_event, decision_event)"
        for label, old, new, message in [
            (
                "future_price_signal",
                call,
                "decide_quantity(has_fill ? fill_price : observed_price, "
                "available_event, decision_event)",
                "Past projection changed",
            ),
            (
                "future_affordability",
                "trace.valid = true;",
                "trace.valid = true;\n    if (has_fill && 2 * fill_price + 3 > initial.cash_units) "
                "{ trace.request = 0; }",
                "Past projection changed",
            ),
            (
                "overwrite_past_snapshot",
                "return trace;\n}",
                "trace.at_decision = trace.after_resolution;\n    return trace;\n}",
                "Past projection changed",
            ),
            (
                "constant_no_order",
                "if (observed_price <= 50)",
                "if (observed_price < 1)",
                "Decision anchor differs",
            ),
        ]:
            assert source.count(old) == 1, label
            mutant_rows, _ = probe(source.replace(old, new), cases)
            try:
                verify(mutant_rows, cases)
            except AssertionError as error:
                assert message in str(error), (label, str(error))
                controls.append(dict(mutation=label, compiled=True, detected=str(error)))
            else:
                raise AssertionError(("Control escaped", label))
    anchor_rows = []
    for anchor in fixture["hand_anchors"]:
        index = cases.index(anchor["input"])
        anchor_rows.append(dict(name=anchor["name"], input=anchor["input"], output=rows[index]))
    print(
        json.dumps(
            dict(
                task="L002d",
                study_date="2026-10-24",
                data_kind="synthetic_selected_suffix_grid",
                prefixes=20,
                suffixes_per_prefix=18,
                traces=len(cases),
                past_projection_comparisons=comparisons,
                decimal_resolution_comparisons=len(cases),
                runs_per_build=2,
                correct_fresh_builds=1,
                control_fresh_builds=len(controls),
                status_counts=dict(sorted(Counter(row[5] for row in rows).items())),
                controls=controls,
                hand_anchors=anchor_rows,
                source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
                buy_sha256=hashlib.sha256(BUY.read_bytes()).hexdigest(),
                fixture_sha256=hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
                output_sha256=hashlib.sha256(output).hexdigest(),
                scope="Selected valid traces only; not arbitrary histories or malformed futures",
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
