"""Audit the fixed Q006a schedule; not a general session lookup or decision validator."""

import argparse
import json
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "experiments/calendar/nyse-2026-autumn-v1.json"


def run():
    raw = FIXTURE.read_bytes()
    fixture = json.loads(raw)
    days = fixture["days"]
    expected_dates = [(date(2026, 10, 29) + timedelta(days=i)).isoformat() for i in range(33)]
    if [row["date"] for row in days] != expected_dates:
        raise ValueError("Fixture must cover all 33 dates exactly once in order")
    zone = ZoneInfo(fixture["zone"])
    sessions = []
    previous = None
    for row in days:
        day = date.fromisoformat(row["date"])
        expected_status = (
            "weekend"
            if day.weekday() >= 5
            else "holiday"
            if day == date(2026, 11, 26)
            else "early_close"
            if day == date(2026, 11, 27)
            else "regular"
        )
        if row["status"] != expected_status:
            raise ValueError("Status disagrees with the bounded source transcription")
        fields = {"date", "status"}
        if expected_status == "holiday":
            fields.add("name")
            if row["name"] != "Thanksgiving Day":
                raise ValueError("Incorrect holiday name")
        if expected_status in {"regular", "early_close"}:
            fields.update({"decision_utc", "core_open_utc", "core_close_utc"})
        if set(row) != fields:
            raise ValueError("Unexpected fixture record fields")
        if expected_status not in {"regular", "early_close"}:
            continue
        close = "13:00:00" if expected_status == "early_close" else "16:00:00"
        for key, wall in (
            ("decision_utc", "09:00:00"),
            ("core_open_utc", "09:30:00"),
            ("core_close_utc", close),
        ):
            expected = datetime.fromisoformat(f"{day}T{wall}").replace(tzinfo=zone)
            if row[key] != expected.astimezone(UTC).isoformat():
                raise ValueError("Explicit fixture UTC value disagrees with named-zone rules")
        duration = datetime.fromisoformat(row["core_close_utc"]) - datetime.fromisoformat(
            row["core_open_utc"]
        )
        sessions.append(
            {
                **row,
                "previous_session": previous,
                "core_minutes": int(duration.total_seconds() / 60),
            }
        )
        previous = row["date"]
    november = [s for s in sessions if s["date"].startswith("2026-11")]
    if len(november) != 20:
        raise ValueError("November count disagrees with the official 20-session total")
    return {
        "data_kind": "scheduled_calendar_fixture_with_synthetic_decision_cases",
        "fixture_id": fixture["fixture_id"],
        "fixture_sha256": sha256(raw).hexdigest(),
        "question": "Can a pre-open decision remain valid under a bounded exchange schedule?",
        "protocol": "Audit every date and UTC instant; cross-check the official November count.",
        "calendar_dates": len(days),
        "status_counts": dict(sorted(Counter(row["status"] for row in days).items())),
        "november_sessions": len(november),
        "weekday_only_november_count": sum(
            row["date"].startswith("2026-11") and date.fromisoformat(row["date"]).weekday() < 5
            for row in days
        ),
        "sessions": sessions,
        "interpretation": (
            "Fixture consistency only. Q006b must implement public lookup/decision validation. "
            "Scheduled sessions and synthetic decisions do not establish trading or fills."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "experiments/calendar/contract-audit.json"
    )
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "sessions"}, indent=2))
