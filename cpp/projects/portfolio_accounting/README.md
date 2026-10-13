# Portfolio accounting: marked wealth

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
accounting API. Fractional-money representation, input/range checks, buy/fee equations, state updates,
structs and delayed decisions need their separate curriculum steps. Marked value is not executable
liquidation cash. No data licence, empirical performance or personal understanding is established.
