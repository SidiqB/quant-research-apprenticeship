"""Synthetic London clock-fold counterexample; no market data or return claims."""

import argparse
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from quant_research.data.availability import Observation, snapshot

ROOT = Path(__file__).resolve().parents[1]


def run():
    london = ZoneInfo("Europe/London")
    early = datetime(2026, 10, 25, 1, 30, tzinfo=london, fold=0)
    late = early.replace(fold=1)
    key = ("SYNTH", "signal")
    future = Observation(*key, early, late, 2)
    first = Observation(*key, early, early, 1)
    # Deliberately retain the old raw-input predicate to expose the defect.
    # The fixed constructor now stores UTC, so comparing its fields is safe.
    legacy_selected = not (late > early or early - late < timedelta(0))
    return {
        "data_kind": "synthetic",
        "question": "Can a repeated local clock time admit a future publication?",
        "protocol": "Fixed instants; old raw predicate versus UTC-normalized selector.",
        "zone": "Europe/London",
        "early_local": early.isoformat(),
        "late_local": late.isoformat(),
        "early_utc": early.astimezone(UTC).isoformat(),
        "late_utc": late.astimezone(UTC).isoformat(),
        "wall_clock_minutes": (late - early).total_seconds() / 60,
        "elapsed_minutes": (late.astimezone(UTC) - early.astimezone(UTC)).total_seconds() / 60,
        "legacy_future_publication_selected": legacy_selected,
        "corrected_future_publication_selected": bool(snapshot([future], early)),
        "latency_60_minutes_accepted": bool(snapshot([first], late, latency=timedelta(minutes=60))),
        "max_age_59_minutes_accepted": bool(
            snapshot([future], late, max_age=timedelta(minutes=59))
        ),
        "latest_revision_value": snapshot([future, first], late)[key].value,
        "interpretation": "Engineering counterexample only; no empirical trading result.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "experiments/timezones/results.json")
    args = parser.parse_args()
    text = json.dumps(run(), indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
