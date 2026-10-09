"""Compare the C++ years parser with a bounded, independent Python reference.

Synthetic engineering checks only. The probe reports the target int maximum;
Python forms its successor without overflowing a C++ int. No financial CLI.
"""

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


def reference(text: bytes, maximum: int) -> str:
    """Apply the contract using a full byte regex and Python integer arithmetic."""
    if re.fullmatch(rb"[0-9]+", text) is None:
        return "invalid"
    value = int(text, 10)
    return "range" if value > maximum else f"ok {value}"


def cases(maximum: int) -> list[bytes]:
    """Fixed small values, adjacent boundaries, and malformed complete inputs."""
    values = [*range(21), maximum - 1, maximum, maximum + 1, maximum + 2, maximum * 10]
    inputs = [str(value).encode("ascii") for value in values]
    inputs += [b"000" + text for text in inputs]
    inputs += [
        b"",
        b"-1",
        b"-0",
        b"+2",
        b" 2",
        b"2 ",
        b"2\t",
        b"2\n",
        b"\n2",
        b"2.5",
        b"2.0",
        b"2x",
        b"2e0",
        b"0x2",
        b"1_000",
        b"1,000",
        b"2\x00x",
        b"\x00",
        b"\xd9\xa2",
        b"\xff",
        b"0" * 1000 + b"2",
        b"9" * 1000,
        b"9" * 1000 + b"x",
    ]
    return inputs


def run(probe: Path) -> dict[str, object]:
    executable = str(probe.resolve())
    limit = subprocess.run([executable, "--int-max"], check=True, capture_output=True, timeout=10)
    if re.fullmatch(rb"[0-9]+\n", limit.stdout) is None or limit.stderr:
        raise RuntimeError("probe returned malformed target limit")
    maximum = int(limit.stdout)
    if maximum < 32767:
        raise RuntimeError("target limit is below the required C++ int minimum")
    inputs = cases(maximum)
    counts: Counter[str] = Counter()
    for text in inputs:
        expected = reference(text, maximum)
        observed = subprocess.run(
            [executable], input=text, check=True, capture_output=True, timeout=10
        )
        if observed.stdout != (expected + "\n").encode("ascii") or observed.stderr:
            raise RuntimeError(
                f"mismatch for {text[:40]!r} ({len(text)} bytes): "
                f"expected {expected!r}, observed {observed.stdout[:80]!r}"
            )
        counts[expected.split()[0]] += 1
    return {
        "data_kind": "synthetic",
        "int_max": maximum,
        "cases": len(inputs),
        "outcomes": dict(sorted(counts.items())),
        "mismatches": 0,
        "boundary_values": {
            str(value): reference(str(value).encode("ascii"), maximum)
            for value in (0, maximum - 1, maximum, maximum + 1, maximum + 2)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path, default=Path("build/cpp/savings_growth/years_probe"))
    args = parser.parse_args()
    print(json.dumps(run(args.probe), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
