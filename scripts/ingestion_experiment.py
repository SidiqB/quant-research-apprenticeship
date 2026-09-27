"""Synthetic source-clock ingestion audit; no market data or return estimates."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from quant_research.data.availability import snapshot
from quant_research.data.ingestion import ingest_observations

ROOT = Path(__file__).resolve().parents[1]


def run():
    first = {
        "asset": "SYNTH",
        "feature": "signal",
        "value": 1,
        "observed_at": "2026-10-25T01:30:00+01:00",
        "available_at": "2026-10-25T01:30:00+01:00",
    }
    revision = {**first, "available_at": "2026-10-25T01:30:00+00:00", "value": 2}
    controls = {
        "duplicate_version": [first, dict(first)],
        "missing_identifier": [{k: v for k, v in first.items() if k != "asset"}],
        "ambiguous_without_offset": [{**first, "available_at": "2026-10-25T01:30:00"}],
        "gap_pre_transition_offset": [{**first, "observed_at": "2026-03-29T01:30:00Z"}],
        "gap_post_transition_offset": [{**first, "observed_at": "2026-03-29T01:30:00+01:00"}],
        "inconsistent_zone": [{**first, "available_at": "2026-10-25T01:30:00-04:00"}],
        "nonfinite_value": [{**first, "value": float("nan")}],
        "reversed_instants": [{**first, "observed_at": "2026-10-25T01:30:00+00:00"}],
    }
    rejected = {}
    for name, records in controls.items():
        try:
            ingest_observations(records, source_zone="Europe/London")
        except ValueError:
            rejected[name] = True
        else:
            rejected[name] = False
    accepted = ingest_observations([first, revision], source_zone="Europe/London")
    decisions = [datetime(2026, 10, 25, hour, 30, tzinfo=UTC) for hour in (0, 1)]
    return {
        "data_kind": "synthetic",
        "question": "Can strict source-zone ingestion reject malformed clocks without guessing?",
        "protocol": (
            "Hand-calculated UTC instants; two valid fold versions and eight invalid batches."
        ),
        "source_zone": "Europe/London",
        "accepted_versions": len(accepted),
        "availability_utc": [x.available_at.isoformat() for x in accepted],
        "decision_utc": [x.isoformat() for x in decisions],
        "decision_values": [snapshot(accepted, d)["SYNTH", "signal"].value for d in decisions],
        "rejected_controls": rejected,
        "interpretation": (
            "Structural validation only; no source authentication or empirical claim."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "experiments/ingestion/results.json")
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, allow_nan=False) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
