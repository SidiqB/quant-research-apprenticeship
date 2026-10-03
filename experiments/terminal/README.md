# Terminal proceeds are separate from membership

Q009b, 3 October 2026. All positions, events, identifiers and dates here are synthetic.

## Question and contract

Can a terminal valuation retain the held security and distinguish missing proceeds from a supported
zero? Q009a reconstructed historical eligibility; eligibility exit is neither a sale nor evidence of
worthlessness. The hypothesis is that explicit evidence states preserve this distinction and permit
hand-checked arithmetic only when complete cash proceeds are declared.

`HeldPosition` records positive long shares, a positive reference price and its date. `TerminalEvidence`
records the same stable security identity, a strictly later event date, a required evidence locator and
complete cash proceeds per reference share. `cash_per_share=None` means the complete amount is unknown;
`0` is an explicit zero assertion. There is no implicit default. An evidence locator is retained but
not authenticated; even a fabricated locator passes syntax checks, so upstream verification is essential.

`value_terminal(position, evidence)` returns an immutable audit result retaining both inputs.
`missing_event` means no terminal evidence was supplied, not proof that an event occurred.
`missing_proceeds` means event evidence exists but complete proceeds are unresolved. Both states return
`None` for value and return. `resolved` means arithmetic is possible under the caller's assertions,
not settlement, spendable cash or completion of a data audit. No membership input can delete a holding.

For q shares, reference price P and complete cash per share C, reference value B=q*P,
terminal entitlement V=q*C and fractional return R=V/B-1. All units use one currency and share basis.
There are no intervening splits, dividends or trades. The cash claim is valued at par; no discounting,
credit-risk adjustment, costs or taxes are included. Negative, nonfinite, boolean and unsupported numeric
inputs fail. Overflow and positive products/ratios rounding to zero fail explicitly. Binary floats are
approximate: a sufficiently tiny positive recovery can still yield a return rounded to -1 by subtraction.

## Synthetic evaluation

Reference date January 2, 2026; membership exit January 5; possible terminal event January 7.
These are calendar-date labels, not verified sessions. Start with 10 shares at 20: reference value 200.

| Evidence | Terminal entitlement | Return | State |
|---|---|---|---|
| No event evidence | Unknown | Unknown | missing_event |
| Event but incomplete proceeds | Unknown | Unknown | missing_proceeds |
| Explicit complete zero | 0 | -100% | resolved |
| Complete proceeds of 5 per share | 50 | -75% | resolved |
| Complete proceeds of 20 per share | 200 | 0% | resolved |
| Complete proceeds of 25 per share | 250 | +25% | resolved |

The experiment's `partial_recovery` case means a complete known payment recovering only part of the
reference value. It does NOT mean incomplete evidence about the final payment. Partial evidence must
remain unknown. A stock/property consideration event is unsupported and must not be encoded as its
cash component alone. This is not a general merger/delisting processor or a CRSP field adapter.

The deliberately wrong exit filter drops OLD even though 10 shares remain held. Zero-imputation of
unknown proceeds fabricates a -100% return. Neither error provides evidence about real performance.
Unresolved positions must not be silently omitted from aggregate valuations or return samples; this
module supplies no aggregate function. A future ledger needs explicit completeness and settlement rules.

## Reproduce and validate

Run `make terminal-experiment` and `make check`. The experiment writes [results.json](results.json).
Seventy new tests include six hand states, identity/date/type/range errors, ordinary frozen-field
mutation rejection, membership independence and 108 exact Fraction debit/credit-ledger comparisons
across three share sizes, three reference prices, four proceeds and three currency scales. Numeric
comparisons use relative and absolute tolerances of 1e-12; statuses/missing values compare exactly.
Two subprocess runs reproduce the archived JSON bytes. All 540 Python tests and 66 C++ checks pass.

## Sources and limits

Primary sources consulted 3 October 2026:

- [CRSP payment categories](https://www.crsp.org/wp-content/uploads/appendix/FlagType_PT.html)
  distinguish cash, stock/property, missing information and declared worthlessness. This motivates
  separate unknown and explicit-zero states; we do not implement those vendor codes or infer zero
  automatically from a label.
- [CRSP aggregate delisting flags](https://www.crsp.org/wp-content/uploads/appendix/FlagType_DE.html)
  distinguish missing, partial and included values. This motivates checking complete evidence before
  calculation; the project's cash-only rule is not a reproduction of vendor return conventions.
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html#frozen-instances)
  documents emulated frozen fields. Runtime type and financial-domain checks are implemented explicitly.

This is retrospective event arithmetic. Event dates do not establish announcement/publication time,
version, settlement date or tradability. Date-only inputs require a strictly later event; same-day
ordering is deliberately unsupported. No persistent event store, claim lifecycle, reinvestment or
portfolio cash ledger is added. Q004a licensed evidence and Q005b provenance/integration, including
cash completeness, identity, units and vintage selection, remain required before empirical use.
See [today's teaching note](../../research_log/2026-10-03.md) and
[validation](../../reports/milestone/2026-10-03-validation.md). Sidiq review: Not yet reviewed.
