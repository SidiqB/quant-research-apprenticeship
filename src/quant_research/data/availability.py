"""Reference point-in-time selection with explicit publication and revision times.

All timestamps must be timezone-aware. A record is usable only after its
availability time, including a caller-specified processing latency. Equality
is permitted: callers needing strictly earlier information must use latency.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite


def _aware(value: datetime) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamps must be timezone-aware datetimes")


@dataclass(frozen=True)
class Observation:
    """One version of a scalar observation for an asset and feature.

    observed_at identifies the economic observation; available_at is the first
    instant this version could have been used. A revision keeps observed_at
    unchanged and has a later available_at. Values must be finite.
    """

    asset: str
    feature: str
    observed_at: datetime
    available_at: datetime
    value: float

    def __post_init__(self) -> None:
        if not self.asset.strip() or not self.feature.strip():
            raise ValueError("asset and feature must be nonempty")
        _aware(self.observed_at)
        _aware(self.available_at)
        if self.available_at < self.observed_at:
            raise ValueError("availability cannot precede observation")
        if not isfinite(self.value):
            raise ValueError("value must be finite")


def snapshot(
    observations: Iterable[Observation],
    decision_at: datetime,
    *,
    latency: timedelta = timedelta(0),
    max_age: timedelta | None = None,
) -> dict[tuple[str, str], Observation]:
    """Select latest known observation, then latest known revision, per key.

    Reject duplicate (asset, feature, observed_at, available_at) versions even
    if identical, because ambiguous ingestion must be resolved upstream.
    Staleness is measured from observed_at; a revision does not refresh age.
    Missing or stale keys are omitted, never imputed. Complexity is O(n).
    """
    _aware(decision_at)
    if latency < timedelta(0) or (max_age is not None and max_age < timedelta(0)):
        raise ValueError("latency and max_age must be nonnegative")
    selected: dict[tuple[str, str], Observation] = {}
    seen: set[tuple[str, str, datetime, datetime]] = set()
    for item in observations:
        version = (item.asset, item.feature, item.observed_at, item.available_at)
        if version in seen:
            raise ValueError("duplicate observation version")
        seen.add(version)
        if item.available_at > decision_at or decision_at - item.available_at < latency:
            continue
        if max_age is not None and decision_at - item.observed_at > max_age:
            continue
        key = (item.asset, item.feature)
        previous = selected.get(key)
        if previous is None or (item.observed_at, item.available_at) > (
            previous.observed_at,
            previous.available_at,
        ):
            selected[key] = item
    return selected
