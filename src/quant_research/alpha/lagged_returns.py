"""Availability-aware geometric linking over exact prior-session intervals."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite

from quant_research.data.availability import Observation, snapshot
from quant_research.data.calendar import NyseAutumn2026Calendar


def _identifier(value: str) -> None:
    if not isinstance(value, str) or not value or any(c.isspace() or ord(c) < 32 for c in value):
        raise ValueError("identifiers must be nonempty strings without whitespace or controls")
    if "\x7f" in value:
        raise ValueError("identifiers must not contain controls")


@dataclass(frozen=True)
class LaggedReturn:
    """Auditable feature; None means incomplete evidence, never a zero return."""

    asset: str
    return_feature: str
    decision_at: datetime
    periods: int
    skip: int
    latency: timedelta
    start_at: datetime
    end_at: datetime
    required_ends: tuple[datetime, ...]
    observations: tuple[Observation | None, ...]
    gross_return: float | None
    value: float | None

    @property
    def missing_at(self) -> tuple[datetime, ...]:
        return tuple(
            end
            for end, row in zip(self.required_ends, self.observations, strict=True)
            if row is None
        )


def lagged_return(
    observations: Iterable[Observation],
    calendar: NyseAutumn2026Calendar,
    asset: str,
    decision_at: datetime,
    *,
    return_feature: str,
    periods: int = 1,
    skip: int = 0,
    latency: timedelta = timedelta(0),
) -> LaggedReturn:
    """Link declared fractional one-session returns known at a pre-open decision.

    Each target row asserts a return from the previous session's core close to
    observed_at, which must match an exact required core close to be selected.
    The caller establishes consistent identity, basis, currency, reinvestment,
    costs, interval coverage and honest availability of ALL underlying inputs.
    This API cannot authenticate those assertions or convert prices into returns.

    periods counts included intervals; skip omits most recent completed sessions.
    Require periods + skip + 1 covered prior sessions to establish the start.
    Select each interval's latest available revision with elapsed UTC latency.
    Missing intervals remain None; never pad, compress gaps or use another asset.
    Valid future additions cannot change past results. Malformed/duplicate input
    anywhere still raises: the invariance promise applies to valid batches only.
    """
    _identifier(asset)
    _identifier(return_feature)
    if type(periods) is not int or periods < 1:
        raise ValueError("periods must be a positive integer")
    if type(skip) is not int or skip < 0:
        raise ValueError("skip must be a nonnegative integer")
    if not isinstance(latency, timedelta) or latency < timedelta(0):
        raise ValueError("latency must be a nonnegative timedelta")
    decision = calendar.validate_decision(decision_at)
    prior = calendar.previous_sessions(decision.day, periods + skip + 1)
    window = prior[: periods + 1]
    ends = tuple(session.core_close for session in window[1:])
    buckets: dict[datetime, list[Observation]] = {end: [] for end in ends}
    seen: set[tuple[str, str, datetime, datetime]] = set()
    for row in observations:
        if not isinstance(row, Observation):
            raise ValueError("input rows must be Observation records")
        _identifier(row.asset)
        _identifier(row.feature)
        version = (row.asset, row.feature, row.observed_at, row.available_at)
        if version in seen:
            raise ValueError("duplicate observation version")
        seen.add(version)
        if (row.asset, row.feature) != (asset, return_feature):
            continue
        if type(row.value) not in (int, float) or not isfinite(row.value) or row.value < -1:
            raise ValueError("target returns must be finite built-in numbers at least -1")
        if row.observed_at in buckets:
            buckets[row.observed_at].append(row)
    selected = tuple(
        snapshot(buckets[end], decision.decision_at, latency=latency).get((asset, return_feature))
        for end in ends
    )
    gross: float | None = None
    value: float | None = None
    if all(row is not None for row in selected):
        gross = 1.0
        for selected_row in selected:
            assert selected_row is not None
            factor = 1.0 + selected_row.value
            product = gross * factor
            if not isfinite(product):
                raise ValueError("linked return exceeds the supported numeric range")
            if gross > 0 and factor > 0 and product == 0:
                raise ValueError("linked return underflows the supported numeric range")
            gross = product
        value = gross - 1.0
    return LaggedReturn(
        asset,
        return_feature,
        decision.decision_at,
        periods,
        skip,
        latency,
        window[0].core_close,
        window[-1].core_close,
        ends,
        selected,
        gross,
        value,
    )
