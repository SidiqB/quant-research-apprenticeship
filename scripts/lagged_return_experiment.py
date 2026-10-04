"""Reproduce synthetic return linking and future-revision invariance."""

import argparse
import json
from dataclasses import asdict
from datetime import date, timedelta
from math import isclose
from pathlib import Path

from quant_research.alpha.lagged_returns import lagged_return
from quant_research.data.availability import Observation
from quant_research.data.calendar import NyseAutumn2026Calendar

ROOT = Path(__file__).resolve().parents[1]


def run():
    calendar = NyseAutumn2026Calendar(ROOT / "experiments/calendar/nyse-2026-autumn-v1.json")

    def session(day):
        result = calendar.session_on(date.fromisoformat(day))
        assert result is not None
        return result

    first, second, third = (session(day) for day in ("2026-11-02", "2026-11-03", "2026-11-04"))
    later = session("2026-11-05").decision_at
    rows = [
        Observation("SYNTH", "session_return", first.core_close, first.core_close, 0.1),
        Observation("SYNTH", "session_return", second.core_close, second.core_close, -0.1),
    ]
    revision = Observation("SYNTH", "session_return", second.core_close, later, 0.5)
    future = Observation("SYNTH", "session_return", third.core_close, third.core_close, 0.2)

    def feature(batch, decision=third.decision_at, **kwargs):
        return lagged_return(
            batch, calendar, "SYNTH", decision, return_feature="session_return", periods=2, **kwargs
        )

    original = feature(rows)
    extended = feature([*rows, revision, future])
    revised = feature([*rows, revision, future], later, skip=1)
    delayed = feature([*rows, revision, future], later, skip=1, latency=timedelta(microseconds=1))
    missing = feature(rows[:1])
    wrong_latest_vintage = (1 + rows[0].value) * (1 + revision.value) - 1
    wrong_sum = sum(row.value for row in rows)
    assert original == extended
    assert original.value is not None and isclose(original.value, -0.01, abs_tol=1e-12)
    assert revised.value is not None and isclose(revised.value, 0.65, abs_tol=1e-12)
    assert delayed.value == original.value
    assert missing.value is None and missing.missing_at == (second.core_close,)
    assert isclose(wrong_latest_vintage, 0.65, abs_tol=1e-12) and wrong_sum == 0
    return {
        "data_kind": "synthetic",
        "period": "2026-10-30 to 2026-11-05; prospective calendar labels, invented returns",
        "question": "Can valid future additions change an earlier lagged return?",
        "protocol": "Exact session windows, hand compounding, revisions, latency and missingness.",
        "future_extension_unchanged": original == extended,
        "original": asdict(original),
        "after_future_extension": asdict(extended),
        "later_same_window": asdict(revised),
        "one_microsecond_latency_same_window": asdict(delayed),
        "missing_interval": asdict(missing),
        "wrong_latest_vintage_return": wrong_latest_vintage,
        "wrong_sum_return": wrong_sum,
        "interpretation": "Synthetic engineering evidence only; no empirical or compliance claim.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "experiments/lagged_returns/results.json"
    )
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True, allow_nan=False, default=str) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(encoded, end="")
