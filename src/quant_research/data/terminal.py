"""Retrospective cash-only terminal valuation, independent of membership.

This is an evidence-labelled calculation, not settlement or as-known-at selection.
Amounts must be complete, in one currency and on the position's share basis.
"""

from dataclasses import dataclass
from datetime import date
from math import isfinite
from typing import Literal


def _identifier(value: str, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a nonempty identifier")
    if any(c.isspace() or not c.isprintable() for c in value):
        raise ValueError(f"{name} must not contain whitespace or control characters")


def _date(value: date, name: str) -> None:
    if type(value) is not date:
        raise ValueError(f"{name} must be a date, not a datetime or string")


def _amount(value: float, name: str, *, positive: bool) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{name} must be a finite built-in number")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds the supported numeric range") from exc
    if not isfinite(result) or (result <= 0 if positive else result < 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}")
    return result


@dataclass(frozen=True)
class HeldPosition:
    """Positive long shares at a positive reference price before the event.

    No intervening splits, dividends or trades are handled. priced_on is strictly
    before the terminal event date; intraday ordering is outside this contract.
    """

    asset: str
    shares: float
    reference_price: float
    priced_on: date

    def __post_init__(self) -> None:
        _identifier(self.asset, "asset")
        _date(self.priced_on, "priced_on")
        for name in ("shares", "reference_price"):
            object.__setattr__(self, name, _amount(getattr(self, name), name, positive=True))
        value = self.shares * self.reference_price
        if not isfinite(value) or value <= 0:
            raise ValueError("reference value exceeds or underflows the supported numeric range")


@dataclass(frozen=True)
class TerminalEvidence:
    """Caller assertion of a cash-only terminal event for one security.

    None means unknown COMPLETE proceeds, including partial or unsupported terms.
    Zero is an explicit supported zero, never a missing-value substitute. A finite
    amount asserts complete entitlement, valued at par, per reference share.
    evidence_ref is a required locator; its existence/truth is not authenticated.
    """

    asset: str
    event_date: date
    cash_per_share: float | None
    evidence_ref: str

    def __post_init__(self) -> None:
        _identifier(self.asset, "asset")
        _identifier(self.evidence_ref, "evidence_ref")
        _date(self.event_date, "event_date")
        if self.cash_per_share is not None:
            object.__setattr__(
                self,
                "cash_per_share",
                _amount(self.cash_per_share, "cash_per_share", positive=False),
            )


@dataclass(frozen=True)
class TerminalValuation:
    """Audit result preserving the input position, even when value is unresolved.

    resolved means arithmetic is available under caller assertions, not that a
    position has settled or that a licence/provenance audit has passed.
    """

    position: HeldPosition
    evidence: TerminalEvidence | None
    status: Literal["missing_event", "missing_proceeds", "resolved"]
    reference_value: float
    terminal_value: float | None
    total_return: float | None


def value_terminal(position: HeldPosition, evidence: TerminalEvidence | None) -> TerminalValuation:
    """Value the event retrospectively; membership cannot erase the holding.

    Missing event evidence does NOT establish that an event occurred. Unknown
    terminal values/returns remain None, never zero or a carried-forward price.
    Evidence must concern the same security and a later calendar date. This API
    has no decision timestamp or publication vintage and cannot select features.
    """
    if not isinstance(position, HeldPosition):
        raise ValueError("position must be a HeldPosition")
    if evidence is not None and not isinstance(evidence, TerminalEvidence):
        raise ValueError("evidence must be a TerminalEvidence or None")
    reference = position.shares * position.reference_price
    if evidence is None:
        return TerminalValuation(position, None, "missing_event", reference, None, None)
    if evidence.asset != position.asset:
        raise ValueError("evidence asset must match position asset")
    if evidence.event_date <= position.priced_on:
        raise ValueError("event_date must follow priced_on")
    if evidence.cash_per_share is None:
        return TerminalValuation(position, evidence, "missing_proceeds", reference, None, None)
    value = position.shares * evidence.cash_per_share
    gross = value / reference
    if not isfinite(value) or not isfinite(gross):
        raise ValueError("terminal calculation exceeds the supported numeric range")
    if evidence.cash_per_share > 0 and (value == 0 or gross == 0):
        raise ValueError("terminal calculation underflows the supported numeric range")
    return TerminalValuation(position, evidence, "resolved", reference, value, gross - 1)
