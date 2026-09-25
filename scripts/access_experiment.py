"""Audit declared access evidence and run explicitly synthetic negative controls."""

import argparse
import copy
import json
import tomllib
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

from quant_research.data.access import REQUIREMENTS, assess_access

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "experiments/data_access/results.json"
    )
    args = parser.parse_args()
    registry = tomllib.loads((ROOT / "configs/data-access-2026-09-25.toml").read_text())
    candidates = []
    for record in registry["sources"]:
        result = assess_access(record)
        candidates.append({**asdict(result), "ready": result.ready})

    complete = {
        "source_id": "synthetic-evidence-only",
        "requirements": {
            name: {"status": "verified", "reference": "Invented evidence for a negative control"}
            for name in REQUIREMENTS
        },
    }
    assert assess_access(complete).ready
    blocked = 0
    for name in REQUIREMENTS:
        for status in ("documented", "unknown", "failed"):
            changed = copy.deepcopy(complete)
            changed["requirements"][name]["status"] = status
            assessment = assess_access(changed)
            assert not assessment.ready and assessment.blockers == (name,)
            blocked += 1

    # Three equally funded holdings, each initially worth 100 invented currency units.
    # A closes at 120, B at 90, C has confirmed zero recovery. C later disappears.
    # No sample selection engine or treatment of real delisting proceeds is implied.
    initial = Decimal(100)
    terminal = (Decimal(120), Decimal(90), Decimal(0))
    population = sum(terminal) / (3 * initial) - 1
    survivors = sum(terminal[:2]) / (2 * initial) - 1
    result = {
        "assessment_as_of": registry["as_of"],
        "candidate_assessments": candidates,
        "synthetic_gate_checks": {"complete_passes": True, "downgrades_blocked": blocked},
        "synthetic_survivorship_example": {
            "period": "one invented holding period",
            "full_population_return": float(population),
            "survivors_only_return": float(survivors),
            "difference_percentage_points": float((survivors - population) * 100),
        },
        "interpretation": (
            "Candidate entries are human documentation assessments, not market data. "
            "Gate controls and returns are synthetic. "
            "No entitlement or empirical alpha is inferred."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
