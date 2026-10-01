"""Single-interval raw-price returns with explicit share and cash units."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class ActionReturn:
    """Fractional returns; cash is recognised entitlement, not spendable cash."""

    raw_price_return: float
    capital_return: float
    income_return: float
    total_return: float


def _number(name: str, value: float, *, positive: bool) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    try:
        converted = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds the supported numeric range") from exc
    if not isfinite(converted) or (converted <= 0 if positive else converted < 0):
        bound = "positive" if positive else "nonnegative"
        raise ValueError(f"{name} must be finite and {bound}")
    return converted


def action_return(
    start_price: float,
    end_price: float,
    *,
    shares_per_old_share: float,
    cash_per_old_share: float,
) -> ActionReturn:
    """Value one opening share across a known split/dividend interval.

    Prices are unadjusted, positive and in the same currency. The share ratio
    is ending shares per opening share (2 for a 2-for-1 split). Cash is the
    known nonnegative dividend entitlement per OPENING share, valued at par.
    Both action fields are required: 1 and 0 explicitly assert no action.
    No event ordering, dates, entitlement discovery, reinvestment or terminal
    proceeds are inferred. Unknown actions/prices must remain unresolved.
    """
    start = _number("start_price", start_price, positive=True)
    end = _number("end_price", end_price, positive=True)
    ratio = _number("shares_per_old_share", shares_per_old_share, positive=True)
    cash = _number("cash_per_old_share", cash_per_old_share, positive=False)
    ending_equity = ratio * end
    ending_wealth = ending_equity + cash
    raw_gross = end / start
    capital_gross = ending_equity / start
    income = cash / start
    total_gross = ending_wealth / start
    quantities = (ending_equity, ending_wealth, raw_gross, capital_gross, income, total_gross)
    if not all(isfinite(value) for value in quantities):
        raise ValueError("calculation exceeds the supported numeric range")
    if min(ending_equity, raw_gross, capital_gross, total_gross) <= 0 or (cash > 0 and income == 0):
        raise ValueError("calculation underflows the supported numeric range")
    return ActionReturn(raw_gross - 1, capital_gross - 1, income, total_gross - 1)
