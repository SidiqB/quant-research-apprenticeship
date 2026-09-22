"""A single past-only holdout with closed label intervals and audited purging."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime


def _utc(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamps must be timezone-aware datetimes")
    # Compare instants, including the two occurrences of a daylight-saving fold.
    return value.astimezone(UTC)


@dataclass(frozen=True)
class LabelInterval:
    """Sample identity and closed information interval [decision_at, label_end].

    label_end is the last instant used to construct the target, not necessarily
    its publication/receipt time. Delayed availability needs an upstream audit.
    A zero-duration interval is valid; missing or reversed endpoints are not.
    Timestamps are stored in UTC; IDs must be globally unique within a split.
    """

    sample_id: str
    decision_at: datetime
    label_end: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.sample_id, str) or not self.sample_id.strip():
            raise ValueError("sample_id must be a nonempty string")
        start, end = _utc(self.decision_at), _utc(self.label_end)
        if end < start:
            raise ValueError("label_end cannot precede decision_at")
        object.__setattr__(self, "decision_at", start)
        object.__setattr__(self, "label_end", end)


@dataclass(frozen=True)
class PurgedSplit:
    """Original input positions, including removals for auditability.

    Empty train is a valid diagnostic result, not permission to fit a model.
    Callers must reject/skip such a fold and report it, never restore purged rows.
    """

    train: tuple[int, ...]
    evaluation: tuple[int, ...]
    purged: tuple[int, ...]
    excluded: tuple[int, ...]


def purged_holdout(
    labels: Iterable[LabelInterval],
    evaluation_start: datetime,
    evaluation_end: datetime,
) -> PurgedSplit:
    """Partition ordered labels for one fixed-model chronological holdout.

    Evaluation decisions lie in [evaluation_start, evaluation_end). Training
    decisions precede evaluation_start and survive only if label_end is strictly
    earlier too. Equality is purged: closed intervals sharing the boundary use
    the same instant. Decisions at/after evaluation_end are excluded, never used
    for training. Evaluation label ends may extend beyond evaluation_end.

    Reject missing evaluation rows, reversed/empty windows, unordered decisions
    and duplicate IDs. Tied decisions allow panel data. Return original indices
    without reordering. O(n) time and O(n) storage; no post-test training/embargo,
    fold generation, model fitting, or empirical independence guarantee.
    """
    start, end = _utc(evaluation_start), _utc(evaluation_end)
    if end <= start:
        raise ValueError("evaluation_end must be after evaluation_start")
    train: list[int] = []
    evaluation: list[int] = []
    purged: list[int] = []
    excluded: list[int] = []
    seen: set[str] = set()
    previous: datetime | None = None
    for index, label in enumerate(labels):
        if not isinstance(label, LabelInterval):
            raise ValueError("labels must contain LabelInterval records")
        if label.sample_id in seen:
            raise ValueError("duplicate sample_id")
        seen.add(label.sample_id)
        if previous is not None and label.decision_at < previous:
            raise ValueError("decisions must be in nondecreasing chronological order")
        previous = label.decision_at
        if label.decision_at < start:
            if label.label_end < start:
                train.append(index)
            else:
                purged.append(index)
        elif label.decision_at < end:
            evaluation.append(index)
        else:
            excluded.append(index)
    if not evaluation:
        raise ValueError("evaluation window contains no decisions")
    return PurgedSplit(tuple(train), tuple(evaluation), tuple(purged), tuple(excluded))
