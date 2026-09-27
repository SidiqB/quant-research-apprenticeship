"""Strict in-memory ingestion; source timestamps must carry explicit local offsets.

One declared IANA zone applies to both timestamp fields throughout a batch. This
adapter does not read files, establish entitlement or authenticate source clocks.
"""

import re
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from math import isfinite
from typing import cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from quant_research.data.availability import Observation

_FIELDS = frozenset({"asset", "feature", "observed_at", "available_at", "value"})
_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})"
)


def _timestamp(value: object, zone: ZoneInfo) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value) or value.endswith("-00:00"):
        raise ValueError("timestamp requires seconds and an explicit known offset")
    if not value.endswith("Z") and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
        raise ValueError("invalid timestamp offset")
    try:
        parsed = datetime.fromisoformat(value)
        instant = parsed.astimezone(UTC)
        local = instant.astimezone(zone)
    except (ValueError, OverflowError) as exc:
        raise ValueError("invalid timestamp") from exc
    # A gap has no UTC round trip to this wall label. A fold has two valid
    # round trips, each distinguished by the explicitly supplied offset.
    if (
        local.replace(tzinfo=None) != parsed.replace(tzinfo=None)
        or local.utcoffset() != parsed.utcoffset()
    ):
        raise ValueError("timestamp wall time or offset disagrees with source zone")
    return instant


def _identifier(value: object) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or not value.isprintable():
        raise ValueError("identifiers must be nonempty printable strings without edge whitespace")
    return value


def ingest_observations(
    rows: Iterable[Mapping[str, object]], *, source_zone: str
) -> tuple[Observation, ...]:
    """Validate an entire batch before returning observations in input order.

    Exact fields: asset, feature, observed_at, available_at, value. Timestamps use
    YYYY-MM-DDTHH:MM:SS[.ffffff] with Z or +/-HH:MM. Missing/unknown offsets,
    leap seconds, excess precision, local gaps and inconsistent zones fail.
    Folds require the correct explicit offset; no inference or shifting occurs.
    Values are finite built-in int/float scalars (not bool), converted to float.
    Duplicate UTC (asset, feature, observed_at, available_at) keys fail even for
    identical values; later availability versions remain distinct revisions.
    No partial result escapes on failure; source iterators are still consumed.
    Keep raw source and zone metadata upstream: Observation stores only UTC.
    """
    if not isinstance(source_zone, str) or not source_zone or source_zone != source_zone.strip():
        raise ValueError("source_zone must be a nonempty IANA zone key")
    try:
        zone = ZoneInfo(source_zone)
    except (ValueError, ZoneInfoNotFoundError) as exc:
        raise ValueError("unknown or invalid source_zone") from exc
    accepted: list[Observation] = []
    seen: set[tuple[str, str, datetime, datetime]] = set()
    for index, row in enumerate(rows, start=1):
        try:
            if not isinstance(row, Mapping) or set(row) != _FIELDS:
                raise ValueError("row must contain exactly the five observation fields")
            asset, feature = _identifier(row["asset"]), _identifier(row["feature"])
            value = row["value"]
            if type(value) not in (int, float):
                raise ValueError("value must be a finite int or float, not bool")
            try:
                number = float(cast(int | float, value))
            except OverflowError as exc:
                raise ValueError("value is outside finite float range") from exc
            if not isfinite(number):
                raise ValueError("value must be finite")
            observation = Observation(
                asset,
                feature,
                _timestamp(row["observed_at"], zone),
                _timestamp(row["available_at"], zone),
                number,
            )
            key = (asset, feature, observation.observed_at, observation.available_at)
            if key in seen:
                raise ValueError("duplicate observation version")
            seen.add(key)
            accepted.append(observation)
        except ValueError as exc:
            # Report position and validation rule, never raw source contents.
            raise ValueError(f"row {index}: {exc}") from exc
    return tuple(accepted)
