"""Retrospective effective-date membership, bounded by declared complete coverage.

This is not an as-known-at history: announcement times and revisions are absent.
Session dates must be mapped upstream; membership does not imply tradability.
"""

from dataclasses import dataclass
from datetime import date


def _date(value: date, field: str) -> None:
    # datetime subclasses date, but silently discarding its time/zone is unsafe.
    if type(value) is not date:
        raise ValueError(f"{field} must be a date, not a datetime or string")


@dataclass(frozen=True)
class MembershipInterval:
    """A stable security ID is included from entry through the day before exit.

    exit=None declares continuation through the history's coverage, not forever.
    IDs are caller-verified identities, never automatically resolved tickers.
    """

    asset: str
    entry: date
    exit: date | None

    def __post_init__(self) -> None:
        if not isinstance(self.asset, str) or not self.asset or self.asset.strip() != self.asset:
            raise ValueError("asset must be a nonempty ID without surrounding whitespace")
        if any(character.isspace() or not character.isprintable() for character in self.asset):
            raise ValueError("asset must not contain whitespace or control characters")
        _date(self.entry, "entry")
        if self.exit is not None:
            _date(self.exit, "exit")
            if self.exit <= self.entry:
                raise ValueError("exit must follow entry")


@dataclass(frozen=True)
class MembershipHistory:
    """One universe with caller-declared complete coverage [start, end).

    Missing assets inside coverage mean nonmembers only under that completeness
    assertion. Outside coverage raises; an empty tuple asserts an empty universe.
    Intervals may extend beyond coverage but must intersect it. Overlap/duplicates
    for one ID fail; adjacent intervals and separated re-entry are accepted.
    Construction sorts O(n log n); each query scans O(n) plus output sorting.
    """

    intervals: tuple[MembershipInterval, ...]
    start: date
    end: date

    def __post_init__(self) -> None:
        _date(self.start, "start")
        _date(self.end, "end")
        if self.end <= self.start:
            raise ValueError("coverage end must follow start")
        if not isinstance(self.intervals, tuple) or any(
            not isinstance(item, MembershipInterval) for item in self.intervals
        ):
            raise ValueError("intervals must be a tuple of MembershipInterval records")
        ordered = tuple(sorted(self.intervals, key=lambda item: (item.asset, item.entry)))
        previous: MembershipInterval | None = None
        for item in ordered:
            if item.entry >= self.end or (item.exit is not None and item.exit <= self.start):
                raise ValueError("every interval must intersect declared coverage")
            if previous is not None and item.asset == previous.asset:
                if previous.exit is None or item.entry < previous.exit:
                    raise ValueError("overlapping or duplicate intervals for one asset")
            previous = item
        object.__setattr__(self, "intervals", ordered)

    def members_on(self, session_date: date) -> tuple[str, ...]:
        """Return sorted stable IDs; no present-day survivor list is consulted."""
        _date(session_date, "session_date")
        if not self.start <= session_date < self.end:
            raise ValueError("session_date outside declared membership coverage")
        return tuple(
            sorted(
                item.asset
                for item in self.intervals
                if item.entry <= session_date and (item.exit is None or session_date < item.exit)
            )
        )
