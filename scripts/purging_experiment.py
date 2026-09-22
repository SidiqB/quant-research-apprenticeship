"""Synthetic variable-horizon counterexample; no prices or performance claims."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from quant_research.validation.purging import LabelInterval, purged_holdout

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "experiments/purging/results.json")
    args = parser.parse_args()
    rows = [
        LabelInterval(
            name, datetime(2026, 1, start, tzinfo=UTC), datetime(2026, 1, end, tzinfo=UTC)
        )
        for name, start, end in [
            ("A", 1, 3),
            ("B", 2, 5),
            ("C", 3, 7),
            ("D", 4, 4),
            ("E", 5, 6),
            ("F", 6, 8),
            ("G", 7, 10),
            ("H", 8, 9),
        ]
    ]
    start, end = datetime(2026, 1, 5, tzinfo=UTC), datetime(2026, 1, 8, tzinfo=UTC)
    split = purged_holdout(rows, start, end)
    naive = tuple(i for i, row in enumerate(rows) if row.decision_at < start)

    def summary(indices):
        # Independent general intersection rule for closed label vs half-open window.
        overlaps = [i for i in indices if rows[i].decision_at < end and rows[i].label_end >= start]
        return {
            "sample_ids": [rows[i].sample_id for i in indices],
            "retained_count": len(indices),
            "overlap_count": len(overlaps),
        }

    result = {
        "data_kind": "synthetic",
        "information_period": "2026-01-01/2026-01-10",
        "question": "Can chronological decisions still leak forward-label information?",
        "hypothesis": (
            "Interval purging removes touching/crossing training labels; ordering alone does not."
        ),
        "evaluation_protocol": (
            "Fixed past-only holdout; predeclared variable horizons; no model fitting."
        ),
        "label_interval_convention": "closed; touching evaluation start is purged",
        "evaluation_window": {
            "start_inclusive": start.isoformat(),
            "end_exclusive": end.isoformat(),
        },
        "rows": [
            {
                "sample_id": row.sample_id,
                "decision_at": row.decision_at.isoformat(),
                "label_end": row.label_end.isoformat(),
            }
            for row in rows
        ],
        "decision_only": summary(naive),
        "one_row_gap": summary(naive[:-1]),
        "interval_purging": summary(split.train),
        "purged_ids": [rows[i].sample_id for i in split.purged],
        "evaluation_ids": [rows[i].sample_id for i in split.evaluation],
        "excluded_ids": [rows[i].sample_id for i in split.excluded],
        "interpretation": (
            "Engineering counterexample only; no empirical leakage rate or alpha claim."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
