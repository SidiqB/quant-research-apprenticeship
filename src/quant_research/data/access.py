"""Fail-closed assessment of declared evidence, not an entitlement verification service."""

from dataclasses import dataclass

REQUIREMENTS = (
    "licence_entitlement",
    "local_access",
    "historical_identity",
    "inactive_coverage",
    "corporate_actions",
    "terminal_events",
    "availability_vintages",
    "permitted_outputs",
)
STATUSES = ("verified", "documented", "unknown", "failed")


@dataclass(frozen=True)
class AccessAssessment:
    source_id: str
    blockers: tuple[str, ...]

    @property
    def ready(self) -> bool:
        """True only when every required evidence assertion is verified."""
        return not self.blockers


def assess_access(record: object) -> AccessAssessment:
    """Validate a complete record and return blockers in a stable requirement order.

    References identify human evidence; this function does not fetch or authenticate
    them. Passing this check cannot itself authorize a purchase, download or claim.
    Unknown, failed and vendor-documented requirements all block research admission.
    """
    if not isinstance(record, dict) or set(record) != {"source_id", "requirements"}:
        raise ValueError("record requires exactly source_id and requirements")
    source_id = record["source_id"]
    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("source_id must be nonblank text")
    evidence = record["requirements"]
    if not isinstance(evidence, dict) or set(evidence) != set(REQUIREMENTS):
        raise ValueError("requirements must contain exactly the eight required gates")
    blockers = []
    for name in REQUIREMENTS:
        item = evidence[name]
        if not isinstance(item, dict) or set(item) != {"status", "reference"}:
            raise ValueError(f"{name} requires exactly status and reference")
        status, reference = item["status"], item["reference"]
        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError(f"{name} has invalid status")
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError(f"{name} requires a nonblank evidence reference")
        if status != "verified":
            blockers.append(name)
    return AccessAssessment(source_id, tuple(blockers))
