"""Bounded NYSE reference schedule, not a live exchange calendar or execution model.

Only the exact reviewed Q006a fixture is supported. Unknown dates raise rather
than becoming closed days. A new schedule requires a reviewed version change.
"""

import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from hashlib import sha256
from pathlib import Path
from zoneinfo import ZoneInfo

FIXTURE_SHA256 = "6a6dcda36695b0ff0fe33f8eabf31c6478dec0a781b3e5a4f11d88414f271082"


class CalendarCoverageError(ValueError):
    """The bounded reference cannot establish the requested date or history."""


@dataclass(frozen=True)
class Session:
    """One scheduled session, with UTC instants and its New York date."""

    day: date
    decision_at: datetime
    core_open: datetime
    core_close: datetime


def _instant(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be an aware datetime")
    return value.astimezone(UTC)


@dataclass(frozen=True, init=False)
class NyseAutumn2026Calendar:
    """Immutable, checksum-pinned teaching calendar for 2026-10-29 to 2026-11-30.

    Pass the repository's experiments/calendar/nyse-2026-autumn-v1.json path.
    Even formatting changes are rejected. The checksum proves identity with the
    reviewed fixture, not source authenticity or realised exchange operations.
    Timestamp APIs accept instants; raw source-clock validation belongs upstream.
    """

    coverage_start: date
    coverage_end: date
    sessions: tuple[Session, ...]
    _zone: ZoneInfo

    def __init__(self, fixture_path: Path) -> None:
        raw = fixture_path.read_bytes()
        if sha256(raw).hexdigest() != FIXTURE_SHA256:
            raise ValueError("unsupported calendar fixture: SHA-256 mismatch")
        # Hash validation fixes schema, complete date coverage and closure rows.
        # Independently check installed zone rules against all pinned UTC values.
        fixture = json.loads(raw)
        zone = ZoneInfo(fixture["zone"])
        sessions = []
        for row in fixture["days"]:
            if row["status"] not in {"regular", "early_close"}:
                continue
            day = date.fromisoformat(row["date"])
            times = tuple(
                datetime.fromisoformat(row[key])
                for key in ("decision_utc", "core_open_utc", "core_close_utc")
            )
            closing = time(13) if row["status"] == "early_close" else time(16)
            for instant, wall in zip(times, (time(9), time(9, 30), closing), strict=True):
                expected = datetime.combine(day, wall, zone).astimezone(UTC)
                if instant != expected:
                    raise ValueError("installed timezone rules disagree with pinned calendar")
            sessions.append(Session(day, *times))
        object.__setattr__(self, "coverage_start", date.fromisoformat(fixture["coverage_start"]))
        object.__setattr__(self, "coverage_end", date.fromisoformat(fixture["coverage_end"]))
        object.__setattr__(self, "sessions", tuple(sessions))
        object.__setattr__(self, "_zone", zone)

    def session_on(self, day: date) -> Session | None:
        """Return a session, None for known closure, or raise for unknown coverage.

        Dates are explicitly New York dates. Datetime arguments are rejected to
        prevent silently using a UTC date as a local session label.
        """
        if not isinstance(day, date) or isinstance(day, datetime):
            raise ValueError("session day must be a date, not a datetime")
        if not self.coverage_start <= day <= self.coverage_end:
            raise CalendarCoverageError("date outside verified calendar coverage")
        return next((session for session in self.sessions if session.day == day), None)

    def validate_decision(self, timestamp: datetime) -> Session:
        """Require exactly 09:00 New York on a listed session; return that session.

        Validity alone does not establish sufficient feature history or fills.
        Equivalent aware representations are accepted; all comparisons use UTC.
        """
        instant = _instant(timestamp)
        session = self.session_on(instant.astimezone(self._zone).date())
        if session is None:
            raise ValueError("decision date is a known closed day")
        if instant != session.decision_at:
            raise ValueError("decision must be exactly 09:00:00 New York")
        return session

    def is_core_time(self, timestamp: datetime) -> bool:
        """Use open <= instant < close; false for known closed days.

        Outside coverage raises, including when the UTC date is covered but its
        New York date is not. This scheduling predicate never promises a fill.
        """
        instant = _instant(timestamp)
        session = self.session_on(instant.astimezone(self._zone).date())
        return session is not None and session.core_open <= instant < session.core_close

    def previous_sessions(self, day: date, count: int = 1) -> tuple[Session, ...]:
        """Return exactly count prior sessions in ascending order, excluding day.

        The anchor must itself be a covered session. Insufficient history raises;
        no partial window, weekday extrapolation or observation padding is used.
        """
        if type(count) is not int or count < 1:
            raise ValueError("count must be a positive integer")
        if self.session_on(day) is None:
            raise ValueError("history anchor must be a session date")
        prior = tuple(session for session in self.sessions if session.day < day)
        if len(prior) < count:
            raise CalendarCoverageError("insufficient verified prior sessions")
        return prior[-count:]
