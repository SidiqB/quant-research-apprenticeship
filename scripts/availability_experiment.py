"""Deterministic counterexample: observation date is not information availability."""

import json
from datetime import UTC, datetime
from pathlib import Path

from quant_research.data.availability import Observation, snapshot

ROOT = Path(__file__).resolve().parents[1]


def main():
    records = [
        Observation(
            "SYNTH",
            "earnings",
            datetime(2026, 1, 1, tzinfo=UTC),
            datetime(2026, 1, 3, tzinfo=UTC),
            100.0,
        ),
        Observation(
            "SYNTH",
            "earnings",
            datetime(2026, 1, 1, tzinfo=UTC),
            datetime(2026, 1, 5, tzinfo=UTC),
            60.0,
        ),
    ]
    rows = []
    for day in range(1, 7):
        decision = datetime(2026, 1, day, tzinfo=UTC)
        safe = snapshot(records, decision).get(("SYNTH", "earnings"))
        # Deliberately invalid comparator: final revised data joined on observation date.
        naive = records[-1] if records[-1].observed_at <= decision else None
        rows.append(
            {
                "decision": decision.isoformat(),
                "naive_final_value": naive.value if naive else None,
                "available_value": safe.value if safe else None,
            }
        )
    result = {
        "data_kind": "synthetic",
        "observation_period": "2026-01-01/2026-01-06",
        "question": "Does joining on observation date leak future revisions?",
        "decisions": rows,
        "mismatched_decisions": sum(r["naive_final_value"] != r["available_value"] for r in rows),
        "total_decisions": len(rows),
        "interpretation": "Engineering counterexample only; no trading performance claim.",
    }
    output = ROOT / "experiments/availability/results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
