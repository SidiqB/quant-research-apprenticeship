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

## Account struct: L001c

Studied October 15; integrated October 17. Run `make cpp-account-state` from the root.
The verifier freshly compiles account_state.cpp and compares two executions with a hand-authored
fixture and independent Decimal addition. AccountState groups cash and one share count; mark
and wealth stay external/derived. Initial wealth is 1000; a separate empty snapshot is zero.
This snapshot example has no validated trade API or arbitrary-input arithmetic guarantee.
See [teaching note](../../../research_log/2026-10-15.md) and its separate validation evidence.

## Validated buy: L001d

Studied October 17; integrated October 18. Run `make cpp-validated-buy` from the root.
validated_buy.cpp defines the two-field AccountState and try_buy as a self-contained teaching
slice. It rejects invalid state, nonpositive quantity/price, invalid fees, insufficient cash
and position-cap violations before changing either field. Whole-unit values are capped at
10000, with no debt or short selling. A false result preserves both original fields.

The Python verifier freshly compiles a temporary C++17 driver with the undefined-behavior
sanitizer, then checks 14 hand-authored outcomes twice. It refuses disabled assertions.
See [October 17 note](../../../research_log/2026-10-17.md),
[original result](../../../experiments/portfolio_accounting/validated-buy.json) and
[validation](../../../reports/milestone/2026-10-17-validation.md).
This does not add shared headers, execution timing, fractional units or market realism.
Independent boundaries and reproduction remain separate lessons; personal review is unchanged.

## Independent boundaries: L001e

Studied October 18; integrated October 19. Run `make cpp-buy-boundaries`, now part of `make check`.
A Python direct-product ledger compares 8351 selected integer tuples with the unchanged C++ buy:
250 accepted, 8101 rejected unchanged. Each fresh sanitizer build executes the whole set twice.
Two exclusive-equality mutations fail; relaxing the negative-price guard survives because the
later affordability check still rejects. These selected inputs do not exhaust the domain.
See [teaching note](../../../research_log/2026-10-18.md),
[result](../../../experiments/portfolio_accounting/buy-boundaries.json) and
[validation](../../../reports/milestone/2026-10-18-validation.md).
Reproduction and L002 decision/execution timing remain separate; no market claim is established.

## Fresh reproduction: L001f

Studied October 19; integrated October 20. Run `make cpp-accounting-reproduce`, part of `make check`.
The recipe compiles five existing C++ programs in temporary directories, runs each twice through
its independent verifier and matches five archived JSON files exactly. Existing build executables
are not used. The two buy drivers additionally use UBSan. A changed-cash scratch archive fails
comparison; disabled assertions are refused. Source and original evidence bytes are preserved.
See [teaching note](../../../research_log/2026-10-19.md),
[result](../../../experiments/portfolio_accounting/reproduction.json) and
[validation](../../../reports/milestone/2026-10-19-validation.md).
L001's bounded teaching slice is complete. This is current-toolchain output reproduction, not
bit-identical binary reproduction, an event-sequence proof or personal mastery. L002 timing follows.

## L002a timeline integrated October 23

Four hand rows match per-share Decimal accounting; three corrupt fixtures are rejected.
Run `make decision-timeline` from the repository root. Study date: 2026-10-20.
Only this bounded teaching slice is complete; L002c implementation and L002d-f remain.
Personal review: Not yet reviewed. Real-data access/provenance gates remain.

## L002b event contract integrated October 23

Six hand/reference outcomes agree; ten invalid traces and five corrupt tables are rejected.
Run `make event-contract` from the repository root. Study date: 2026-10-22.
Only this bounded teaching slice is complete; L002c implementation and L002d-f remain.
Personal review: Not yet reviewed. Real-data access/provenance gates remain.
