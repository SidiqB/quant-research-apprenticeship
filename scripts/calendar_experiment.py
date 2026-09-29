"""Reproduce bounded decision/core/history checks using synthetic timestamps."""

import argparse
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from quant_research.data.calendar import (
    FIXTURE_SHA256,
    CalendarCoverageError,
    NyseAutumn2026Calendar,
)

ROOT = Path(__file__).resolve().parents[1]


def run():
    calendar = NyseAutumn2026Calendar(ROOT / "experiments/calendar/nyse-2026-autumn-v1.json")
    boundary_checks = 0
    for session in calendar.sessions:
        assert calendar.validate_decision(session.decision_at) == session
        assert not calendar.is_core_time(session.decision_at)
        for boundary, shift, expected in (
            (session.core_open, -1, False),
            (session.core_open, 0, True),
            (session.core_open, 1, True),
            (session.core_close, -1, True),
            (session.core_close, 0, False),
            (session.core_close, 1, False),
        ):
            assert calendar.is_core_time(boundary + timedelta(microseconds=shift)) is expected
            boundary_checks += 1
    rejected = {}
    for label, stamp in {
        "weekend": "2026-11-28T14:00:00+00:00",
        "holiday": "2026-11-26T14:00:00+00:00",
        "wrong_fixed_utc_hour": "2026-11-02T13:00:00+00:00",
        "one_microsecond_early": "2026-11-27T13:59:59.999999+00:00",
        "one_microsecond_late": "2026-11-27T14:00:00.000001+00:00",
        "core_open_is_not_decision": "2026-11-27T14:30:00+00:00",
        "naive": "2026-11-27T09:00:00",
        "before_coverage": "2026-10-28T13:00:00+00:00",
        "after_coverage": "2026-12-01T14:00:00+00:00",
    }.items():
        try:
            calendar.validate_decision(datetime.fromisoformat(stamp))
        except ValueError as exc:
            rejected[label] = str(exc)
        else:
            raise AssertionError(f"invalid decision accepted: {label}")
    history = {}
    for day in (date(2026, 11, 25), date(2026, 11, 27), date(2026, 11, 30)):
        try:
            prior = calendar.previous_sessions(day, 20)
        except CalendarCoverageError:
            history[day.isoformat()] = {"status": "insufficient_history"}
        else:
            history[day.isoformat()] = {
                "status": "complete",
                "count": len(prior),
                "first": prior[0].day.isoformat(),
                "last": prior[-1].day.isoformat(),
            }
    examples = []
    for stamp in ("2026-10-30T13:00:00", "2026-11-02T14:00:00", "2026-11-27T14:00:00"):
        session = calendar.validate_decision(datetime.fromisoformat(stamp).replace(tzinfo=UTC))
        examples.append(
            {
                "day": session.day.isoformat(),
                "decision_utc": session.decision_at.isoformat(),
                "core_open_utc": session.core_open.isoformat(),
                "core_close_utc": session.core_close.isoformat(),
                "previous_session": calendar.previous_sessions(session.day)[0].day.isoformat(),
                "core_minutes": int((session.core_close - session.core_open).total_seconds() / 60),
            }
        )
    return {
        "data_kind": "scheduled_calendar_fixture_with_synthetic_decision_cases",
        "fixture_sha256": FIXTURE_SHA256,
        "question": (
            "Can bounded decision validation preserve pre-open decisions and fail on unknowns?"
        ),
        "protocol": (
            "Check all sessions and microsecond core boundaries; reject nine invalid decisions."
        ),
        "valid_preopen_decisions": len(calendar.sessions),
        "core_only_rule_incorrectly_rejected_decisions": len(calendar.sessions),
        "core_boundary_checks_passed": boundary_checks,
        "invalid_decisions_rejected": rejected,
        "twenty_session_history": history,
        "examples": examples,
        "interpretation": (
            "Scheduling correctness only; no prices, fills, realised sessions or alpha."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "experiments/calendar/decision-validation.json"
    )
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
