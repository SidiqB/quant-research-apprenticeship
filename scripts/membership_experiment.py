"""Reproduce a synthetic membership history and a present-day filtering error."""

import argparse
import json
from datetime import date
from pathlib import Path

from quant_research.data.membership import MembershipHistory, MembershipInterval

ROOT = Path(__file__).resolve().parents[1]


def run():
    records = (
        MembershipInterval("OLD", date(2026, 1, 1), date(2026, 1, 5)),
        MembershipInterval("STAY", date(2026, 1, 1), None),
        MembershipInterval("NEW", date(2026, 1, 5), None),
        MembershipInterval("RETURN", date(2026, 1, 2), date(2026, 1, 4)),
        MembershipInterval("RETURN", date(2026, 1, 7), None),
    )
    history = MembershipHistory(records, date(2026, 1, 1), date(2026, 1, 9))
    expected = (
        ("OLD", "STAY"),
        ("OLD", "RETURN", "STAY"),
        ("OLD", "RETURN", "STAY"),
        ("OLD", "STAY"),
        ("NEW", "STAY"),
        ("NEW", "STAY"),
        ("NEW", "RETURN", "STAY"),
        ("NEW", "RETURN", "STAY"),
    )
    rows = []
    for day, hand_members in enumerate(expected, start=1):
        when = date(2026, 1, day)
        actual = history.members_on(when)
        if actual != hand_members:
            raise AssertionError(f"hand membership mismatch at {when}")
        rows.append({"date": when.isoformat(), "members": actual})
    final_members = set(history.members_on(date(2026, 1, 8)))
    past_members = history.members_on(date(2026, 1, 2))
    wrong = tuple(asset for asset in past_members if asset in final_members)
    if wrong != ("RETURN", "STAY") or past_members != ("OLD", "RETURN", "STAY"):
        raise AssertionError("survivor-filter counterexample failed")
    return {
        "data_kind": "synthetic",
        "period": "2026-01-01 inclusive to 2026-01-09 exclusive; calendar-date labels only",
        "question": "Can effective intervals retain past members that later exit?",
        "protocol": "Eight exact hand sets; final-date filter must wrongly remove OLD.",
        "intervals": [
            {
                "asset": x.asset,
                "entry": x.entry.isoformat(),
                "exit": None if x.exit is None else x.exit.isoformat(),
            }
            for x in records
        ],
        "daily_members": rows,
        "hand_sets_passed": len(rows),
        "past_members": past_members,
        "wrong_survivor_filtered_members": wrong,
        "wrongly_removed": sorted(set(past_members) - set(wrong)),
        "interpretation": "Effective-date mechanics only; no publication vintage or return claim.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "experiments/membership/results.json")
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True, allow_nan=False) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(encoded, end="")
