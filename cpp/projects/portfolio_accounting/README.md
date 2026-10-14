# Portfolio accounting: marked wealth and one buy

L001a starts with one already owned synthetic long position. It values three fixed snapshots:
800 cash units and four shares marked at 50, 55 or 45 give wealth 1000, 1020 or 980.
There is no trade, liability or cash movement. All amounts use whole arbitrary money units.

Run `make cpp-marked-wealth`, or `make check` for the whole project. The C++17 example uses small
fixed constants and no external input. The Python Decimal reference adds each share separately,
compares the hand-authored expected output and checks stdout, stderr and exit status twice.
Run the verifier without `-O`; it explicitly refuses disabled assertions.

Read [the October 13 note](../../../research_log/2026-10-13.md) for units, the hand calculation,
line-by-line explanation, limitations and exercises. The archived result is in
[marked-wealth.json](../../../experiments/portfolio_accounting/marked-wealth.json).

The fixed constants are nonnegative and every intermediate fits int. This is not an arbitrary-input
accounting API. Fractional-money representation, input/range checks, reusable state updates,
structs and delayed decisions need their separate curriculum steps. Marked value is not executable
liquidation cash. No data licence, empirical performance or personal understanding is established.

## L001b: one buy and its fee

Run `make cpp-buy-equations`. The fixed buy_equations.cpp example starts with cash 800 and
four shares, buys two shares at the unchanged mark of 50 and pays a separate fee of 3.
Cash becomes 697, shares become 6, holdings become 300 and wealth becomes 997. The 100 spent
on shares becomes 100 of marked holdings; the fee is the entire wealth decrease under the
equal-fill/mark assumption. All money is in whole arbitrary units; no external input is accepted.

The hand-authored buy_expected.txt and scripts/verify_buy_equations.py independently reconcile
a Decimal per-share cash ledger, compare every output byte, and check empty stderr/status twice.
The verifier rejects `-O`. Full `make check` includes this target. Scratch omitted-fee and
missing-share mutations compile but fail verification; see the validation record.

Read [the October 14 note](../../../research_log/2026-10-14.md),
[archived result](../../../experiments/portfolio_accounting/buy-equations.json) and
[validation](../../../reports/milestone/2026-10-14-validation.md). Only the equations and fixed
example are complete. L001c introduces a struct next; L001d/e add validated state updates and
boundaries. No unaffordable-order rejection, general overflow handling or execution timing is
implemented here. Different fill/mark prices invalidate the fee-only wealth-loss conclusion.
