"""Check a fixed hand timeline; this is not a reusable execution engine."""

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

FIXTURE = (
    Path(__file__).resolve().parents[1] / "experiments/portfolio_accounting/decision-timeline.json"
)


def verify(fixture):
    assert fixture["data_kind"] == "synthetic_hand_timeline"
    decision = fixture["decision_event"]
    fill = fixture["fill_event"]
    known = fixture["decision_input"]
    assert known["available_event"] < decision < fill, "unavailable decision input"
    rows = fixture["rows"]
    assert [row["event"] for row in rows] == [0, 1, 2, 3]
    assert [row["kind"] for row in rows] == [
        "observation",
        "decision",
        "assumed_fill",
        "later_mark",
    ]
    assert known["price"] == rows[0]["mark"], "observation mismatch"
    quantity = 2 if known["price"] <= 50 else 0
    assert fixture["order_quantity"] == quantity == 2
    cash = Decimal(fixture["initial_cash"])
    shares = fixture["initial_shares"]
    price, fee = Decimal(fixture["fill_price"]), Decimal(fixture["fee"])
    assert price > 0 and fee >= 0
    for row in rows:
        if row["event"] == fill:
            # Separate one-share debits rather than the note's n*p formula.
            for _ in range(quantity):
                cash -= price
                shares += 1
            cash -= fee
            assert cash >= 0
        assert (row["cash"], row["shares"]) == (cash, shares), "state timing mismatch"
        holdings = sum((Decimal(row["mark"]) for _ in range(shares)), Decimal(0))
        assert row["wealth"] == cash + holdings, "wealth mismatch"
    return len(rows)


def main():
    fixture = json.loads(FIXTURE.read_text())
    rows = verify(fixture)
    controls = []
    for name in ["future_input", "trade_at_decision", "fill_at_old_price"]:
        bad = copy.deepcopy(fixture)
        if name == "future_input":
            bad["decision_input"] = {"price": 52, "available_event": 2}
        elif name == "trade_at_decision":
            bad["rows"][1].update(cash=697, shares=6, wealth=997)
        else:
            bad["rows"][2].update(cash=697, wealth=1009)
        try:
            verify(bad)
        except AssertionError as error:
            controls.append({"name": name, "diagnostic": str(error)})
        else:
            raise AssertionError(("Corrupt fixture survived", name))
    print(
        json.dumps(
            {
                "study_date": "2026-10-20",
                "task": "L002a",
                "data_kind": "synthetic_hand_timeline",
                "rows_verified": rows,
                "decision_state": {"cash": 800, "shares": 4},
                "post_fill_state": {"cash": 693, "shares": 6, "wealth": 1005},
                "final_wealth": 987,
                "corrupt_fixtures_rejected": controls,
                "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
                "scope": (
                    "hand-timeline consistency only; "
                    "no execution engine or general invariance proof"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
