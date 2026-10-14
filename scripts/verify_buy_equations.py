"""Reconcile one fixed synthetic buy against a share-by-share Decimal cash ledger."""

import argparse
import json
import subprocess
from decimal import Decimal
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O")

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--executable", type=Path, default=ROOT / "build/cpp/portfolio_accounting/buy_equations"
)
args = parser.parse_args()
cash_before = Decimal("800")
price = Decimal("50")
fee = Decimal("3")
shares_before = 4
buy_shares = 2
assert cash_before >= 0 and price > 0 and fee >= 0
assert shares_before >= 0 and buy_shares > 0

# Independent ledger: debit one share at a time, then debit the explicit fee once.
cash = cash_before
shares = shares_before
notional = Decimal(0)
for _ in range(buy_shares):
    cash -= price
    shares += 1
    notional += price
assert cash >= fee, "Fixed buy must be affordable including the fee"
cash -= fee
holdings_before = sum((price for _ in range(shares_before)), Decimal(0))
holdings_after = sum((price for _ in range(shares)), Decimal(0))
wealth_before = cash_before + holdings_before
wealth_after = cash + holdings_after
cash_debit = cash_before - cash
holdings_increase = holdings_after - holdings_before
wealth_change = wealth_after - wealth_before
assert (cash, shares, holdings_after, wealth_after) == (Decimal(697), 6, Decimal(300), Decimal(997))
assert cash_debit == notional + fee == Decimal(103)
assert holdings_increase == notional == Decimal(100)
assert wealth_change == -fee == Decimal(-3)
assert cash + notional + fee == cash_before
assert wealth_after + fee == wealth_before
expected = (
    f"before: cash={cash_before}; shares={shares_before}; mark={price}; wealth={wealth_before}\n"
    f"buy: shares={buy_shares}; fill={price}; notional={notional}; fee={fee}\n"
    f"after: cash={cash}; shares={shares}; holdings={holdings_after}; wealth={wealth_after}\n"
    f"reconcile: cash_debit={cash_debit}; holdings_increase={holdings_increase}; "
    f"wealth_change={wealth_change}\n"
).encode()
assert expected == (ROOT / "cpp/projects/portfolio_accounting/buy_expected.txt").read_bytes()
for _ in range(2):
    result = subprocess.run([str(args.executable.resolve())], capture_output=True, timeout=10)
    assert (result.stdout, result.stderr, result.returncode) == (expected, b"", 0), (
        "Buy-equations output/status differs from the independent reference"
    )
print(
    json.dumps(
        {
            "study_date": "2026-10-14",
            "task": "L001b",
            "data_kind": "synthetic_fixed_buy",
            "money_unit": "whole arbitrary money unit",
            "cash_before": str(cash_before),
            "shares_before": shares_before,
            "buy_shares": buy_shares,
            "fill_and_unchanged_mark": str(price),
            "notional": str(notional),
            "fee": str(fee),
            "cash_after": str(cash),
            "shares_after": shares,
            "holdings_after": str(holdings_after),
            "wealth_before": str(wealth_before),
            "wealth_after": str(wealth_after),
            "cash_debit": str(cash_debit),
            "holdings_increase": str(holdings_increase),
            "wealth_change": str(wealth_change),
            "runs": 2,
            "reference": "Decimal per-share cash debits and holdings addition; fee debited once",
            "scope": "one affordable buy; no external input, reusable state API or timing model",
            "personal_review": "Not yet reviewed",
        },
        indent=2,
        sort_keys=True,
    )
)
