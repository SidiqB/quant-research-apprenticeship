# Progressive C++ projects for finance

Requested by Sidiq on 21 September 2026: include finance-related C++ projects, start very simply,
and increase difficulty gradually. This preference is part of the continuing research programme.
Keep each project in its own cpp/projects/<name> directory with build instructions, tests and a teaching note.
These educational implementations do not require a speedup justification. Replacing working research
components with C++ still requires profiling, a validated reference and a demonstrated benefit.

## Cadence

Starting Wednesday 23 September, use the Wednesday daily research slot for the next eligible C++ step.
Use one 45-90 minute step per run; split a step further if needed. Do not add a second daily workload.
An unfinished Python task keeps its place for the next non-C++ run. Existing dates remain planning targets;
revise them in the weekly synthesis when work moves. Stop at 31 December under the existing programme scope.
Do not skip prerequisites to reach a more impressive title. Later projects may remain unfinished in 2026.

## Ordered backlog

| ID | Project / step | Concepts | Evidence required | Status |
|---|---|---|---|---|
| C001 | Savings growth: fixed-input example | Compile/run, variables, doubles, output | Calculate one year of growth and compare with hand arithmetic | Done |
| C002 | Savings growth: reusable function | Functions, parameters, return values | Zero rate, zero years, invalid inputs; explain compounding convention | Done |
| C003 | Savings growth: command-line inputs | Parsing, branches, errors | Reject malformed input; clear units and reproducible examples | Ready |
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
