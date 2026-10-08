# Updated priority - 4 October 2026

C++ is now the default for new educational projects, not just Wednesday. Follow QUANT_CURRICULUM.md
and CURRICULUM_BACKLOG.md; reuse completed C001/C002 and start C003 next. The old C-steps below remain
prerequisite references; their old Wednesday dates are superseded.

# Progressive C++ projects for finance

Requested by Sidiq on 21 September 2026: include finance-related C++ projects, start very simply,
and increase difficulty gradually. This preference is part of the continuing research programme.
Keep each project in its own cpp/projects/<name> directory with build instructions, tests and a teaching note.
These educational implementations do not require a speedup justification. Replacing working research
components with C++ still requires profiling, a validated reference and a demonstrated benefit.

## Cadence

Follow QUANT_CURRICULUM.md and CURRICULUM_BACKLOG.md from October 5. Use one 45-90 minute
bounded concept per day, with C++ as the default and Python for independent checks. Split prerequisites
instead of adding lessons to meet a commit draw. The former Wednesday-only rule is superseded.
Stop after December 31 pending the next scope. Historical evidence sections retain their original dates.

## Ordered backlog

| ID | Project / step | Concepts | Evidence required | Status |
|---|---|---|---|---|
| C001 | Savings growth: fixed-input example | Compile/run, variables, doubles, output | Calculate one year of growth and compare with hand arithmetic | Done |
| C002 | Savings growth: reusable function | Functions, parameters, return values | Zero rate, zero years, invalid inputs; explain compounding convention | Done |
| C003 | Savings growth: command-line inputs; parent of C003a/b | Parsing, branches, errors | Both children complete; clear units and reproducible examples | In progress: C003a parser implemented; verification lessons pending |
| C003a | Whole-year text parser; October 5-11 foundation slice | Text versus value, full consumption, branches, range | Reject fractions, negatives, trailing text and overflow; compare Python oracle; verified notes | In progress: parser implemented October 8; boundary oracle next |
| C003b | Complete CLI after C003a | Principal/rate parsing, units, error reporting | Reject malformed/nonfinite inputs; connect validated arguments to C002; integration checks | Deferred: C003a |
| C004 | Return calculator: a small price series | Vectors, loops, indexing | Hand-check simple returns; reject zero/nonpositive prices under stated scope | Planned |
| C005 | Return calculator: summary statistics | Mean, sample variance, functions | Compare known small samples; handle fewer than two observations | Planned |
| C006 | Cash-flow present value | Structs, vectors, discounting | Hand-check a zero-coupon example; state rate and period conventions | Planned |
| C007 | Bond cash-flow calculator | Multiple functions, test organisation | Sum coupons and principal; distinguish educational price from market quotation | Planned |
| C008 | Vanilla option payoffs | Enums, domain validation, boundaries | Calls and puts above, below and at strike; no pricing claim yet | Planned |
| C009 | Binomial option pricing: one period | Small structs, no-arbitrage conditions | Derive risk-neutral probability; compare hand-calculated price | Planned |
| C010 | Binomial option pricing: multiple periods | Iteration, vector storage | Compare small trees with reference; test convergence after pricing baseline exists | Planned |
| C011 | Monte Carlo: seeded terminal-price sampler | Random engines, distributions | Reproducible seed within documented implementation; sampling uncertainty | Planned |
| C012 | Monte Carlo: option estimate and error bars | Accumulation, numerical error | Compare independent pricing baseline; report confidence intervals | Planned |
| C013 | Portfolio scenario P&L | Containers, clean interfaces | Reconcile positions, shocks and units on a small fixture | Planned |
| C014 | Simple order-book representation | Maps, ownership, invariants | Best bid/ask and cancellation cases; price-time matching is a later extension | Planned |
| C015 | Profile one completed project | Timing, optimisation trade-offs | Equal outputs before/after; no unsupported performance claim | Planned |

Each step gets a beginner explanation of the new C++ syntax, financial definitions, worked mathematics,
build/test commands, limitations and short understanding questions. Use synthetic fixtures explicitly.
Use the simplest supported compiler setup first; introduce build tooling and abstractions only as needed.
Track completion separately from Sidiq's personal review or independent reproduction.

## Evidence from 23 September

C001 is implemented in cpp/projects/savings_growth. The compiled fixed-input example produces
50.00 units of interest and a 1050.00-unit closing balance from 1000.00 at 5% for one year.
The hand-authored output comparison is part of make check; 49 existing Python tests also pass.
Two runs reproduced the output, and a temporary 500% rate mutation was rejected by the comparison.
The four-page teaching PDF was checked for text completeness and visually inspected on every page.
Sidiq review status remains Not yet reviewed. C002 is ready for Wednesday 30 September.

## Separate project request

Sidiq also requested a separate finance-related project linked to an earlier remembered project.
Its exact identity is awaiting clarification; do not substitute the quantum/wormhole project or alter that
project's independent-learning arrangement without confirmation of the intended scope.

## Evidence from 30 September

C002 is complete: a reusable annual-compounding function validates finite nonnegative principal/rate
and whole nonnegative years, preserves zero cases and rejects numeric overflow. Sixty-six C++ checks
pass; the hand-authored output fixture preserves C001 and adds 1102.50 at two years and 1157.625 at
three years. Two replays match; a simple-interest mutation fails. All 363 Python tests and full checks
pass. The four-page teaching PDF passes full-text and every-page visual checks. Intermediate-factor
overflow and implicit integer conversion limitations are explicit; no general exact-money claim.
C003 is Ready for October 7. Sidiq review remains Not yet reviewed.

## Evidence from 5 October

C003a intuition is complete: five hand classifications distinguish a whole count from fractional,
negative, missing and trailing text. A fixed C++ example preserves text separately from the number,
then shows explicit conversion of 2.5 to 2 and the resulting 1102.50 two-year balance. Two exact
replays, an independent Decimal interest ledger, 608 Python tests and the existing 66 C++ checks
pass; the new output comparison is part of make check. The four-page teaching PDF is verified.
The parser is not implemented; October 6 defines grammar/range before October 7 implementation.
Personal review remains Not yet reviewed. C003b and later prerequisites remain deferred.

## Evidence from 7 October

Completed grammar/range after the interrupted October 6 run. See the years_contract.md worksheet in
the savings project: whole ASCII decimal digits, full input, explicit sign/whitespace policy and
nonnegative int range. The fixed conversion_contract.cpp demo observes a successful prefix (2x)
and successful complete negative (-1); neither meets policy. Two exact replays, 608 Python tests,
66 existing C++ checks and three output fixtures pass; the four-page PDF is verified. Parser
implementation remains next on October 8. Continue remaining prerequisites in order without rushing.
C003a/C003 remain in progress; C003b stays deferred; personal review remains Not yet reviewed.

## C003a implementation - 8 October

The whole-year parser is implemented with digit-only spelling, checked decimal conversion,
complete consumption and explicit spelling/range exceptions. Thirty parser checks include
embedded NUL, long text and a hand-calculated C002 connection. All 608 Python tests, 66 prior
C++ checks and four output fixtures pass; fresh compilation and the four-page PDF are verified.
C003a remains in progress: independent boundary oracle next on October 9, then failure,
reproduction and consolidation. C003b and later projects remain conditional on prerequisites.
Personal review remains Not yet reviewed; Q004a/Q005b still gate empirical work.
