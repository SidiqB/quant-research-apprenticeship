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
| C003 | Savings growth: command-line inputs; parent of C003a/b | Parsing, branches, errors | Both children complete; clear units and reproducible examples | In progress: C003a complete; C003b unfinished |
| C003a | Whole-year text parser; October 5-11 foundation slice | Text versus value, full consumption, branches, range | Reject fractions, negatives, trailing text and overflow; compare Python oracle; verified notes | Done: consolidation studied October 12, integrated October 13 |
| C003b | Complete CLI after C003a | Principal/rate parsing, units, error reporting | Reject malformed/nonfinite inputs; connect validated arguments to C002; integration checks | Deferred: separate CLI lessons |
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

## C003a boundary verification - 9 October

Independent Python integer/byte-pattern checks agree with the unchanged C++ parser on 75 synthetic
inputs: 47 accepted, 21 spelling errors and seven range errors. The target maximum is accepted;
its successor is rejected. Two scratch mutations (exclusive upper limit and NUL truncation) fail
for the intended mismatches. All 608 Python tests, 96 existing C++ checks, four output fixtures
and quality checks pass. Two oracle replays agree; the four-page teaching PDF is verified.
Only the boundary slot is complete. Next on October 10: fractional-truncation failure, then
reproduction and consolidation in dependency order. C003a/C003 remain in progress; C003b and
later projects remain conditional. Personal review stays Not yet reviewed; empirical gates remain.

## C003a failure lesson - studied October 10, integrated October 11

The zero-budget October 10 lesson is now integrated after all seven input and eight artifact hashes
matched. Five fixed C++ cases verify two acceptances and three rejections before calculation; a
separate deliberately wrong adapter produces three forbidden acceptances and expected exit 1.
make check includes this failure check. Two replays match the original archived result; 608 Python
tests, 96 existing C++ checks, 75 oracle comparisons and four output fixtures pass. All nine C++
executables freshly compile warning-clean; the revised four-page teaching PDF is verified.

Only the failure slot is complete. Reproduction/teach-back is the next lesson, then consolidation;
inspect ignored pending manifests before dispatch, since today's draw of 1 is allocated to this
integration. C003a/C003 remain in progress. C003b, vectors/statistics and the ledger retain their
prerequisites; Q004a/Q005b still gate empirical work. Personal review remains Not yet reviewed.

## C003a reproduction - studied October 11, integrated October 12

The fresh-build recipe is now scripts/reproduce_years_evidence.py. Six temporary C++17 executables
reproduce 66 savings and 30 parser checks, the demo, 75 oracle cases and exact correct/wrong fractional
outputs; each path runs twice. Original evidence and integration provenance are in experiments/years_parser.
All 17 input and five artifact hashes matched before integration. The three-page teaching note is
reverified, and full checks pass. Only reproduction is complete; consolidation/readiness is next.
Personal review remains Not yet reviewed. Later curriculum and empirical gates remain unchanged.

## Weekly refinement - written October 11, integrated October 12

The October 5-11 synthesis and verified six-page PDF are in reports/weekly. C003a consolidation
comes next. Ledger work is narrowed to L001a-f cash/position/fee accounting, followed separately by
L002 delayed decision/execution and future-price invariance. The October 19 trend slot is conditional.
C003b CLI, C004 returns and C005 statistics remain explicit carryover; Q004a/Q005b empirical gates
remain. See CURRICULUM_BACKLOG.md for the merged sequence. No personal mastery or review is inferred.

## C003a consolidation - studied October 12, integrated October 13

C003a's repository teaching slice is complete. Eight fixed traces distinguish four parser rejections,
three finite balances and one accepted horizon whose calculation overflows. The unchanged production
functions are freshly compiled and run twice by make cpp-years-readiness, now part of make check.
Original pending inputs/artifacts all match their hashes; original result JSON is preserved. The
four-page teaching PDF is reverified. Next learning: L001a cash, position and marked wealth.
C003 remains in progress because C003b is unfinished; C004/C005 and L002 timing retain prerequisites.
Q004a/Q005b gates remain; personal review stays Not yet reviewed. No empirical result is claimed.

## L001a cash and marked wealth - 13 October

One fixed C++ position now has three synthetic valuation snapshots: cash 800 and four shares
marked at 50/55/45 give wealth 1000/1020/980. Independent Decimal addition agrees; two exact runs
and two JSON replays match. A scratch share-plus-price mutation is rejected. make cpp-marked-wealth
is part of make check. The four-page note explains units, unchanged cash and valuation limits.
L001a only is complete; next is L001b one-buy/fee equations. L001's reusable state changes, L002
delayed decisions and C003b/C004/C005 remain unfinished. Q004a/Q005b empirical gates are unchanged;
no market result or personal-review transition is claimed. Shared draw 3; two coherent units ready,
including October 12 consolidation. No extra lesson or artificial third commit is created.

## L001b one-buy equations - 14 October

The fixed C++ buy demonstration reconciles cash 800 to 697, shares 4 to 6 and wealth 1000
to 997 after buying two shares at 50 with a separate fee of 3. Fill equals the unchanged mark.
Independent Decimal per-share accounting, two exact runs and two JSON replays agree; scratch
omitted-fee and missing-share controls fail as intended. make cpp-buy-equations is part of
make check; all 608 Python tests and existing C++ checks pass. The four-page teaching PDF
is verified. Only L001b is complete; next is L001c's single position struct, followed by the
validated buy, boundary and reproduction lessons. L002 timing, C003b/C004/C005 and empirical
Q004a/Q005b gates remain. Personal review stays Not yet reviewed. Draw 3; one coherent unit,
with no pending packages to integrate or artificial extra commits.

## L001c struct - studied October 15, integrated October 17

The account struct lesson is integrated after all 11 original inputs and nine artifacts matched
the pending manifest. Cash 800 and four shares at mark 50 still give wealth 1000; a separate
empty-brace object is zero initialized. Two fresh builds reproduce the original result; a
swapped initializer is rejected. make cpp-account-state now joins make check. Full checks and
the revised four-page teaching PDF pass. Original study evidence and dates are preserved.

Only L001c is integrated here. No October 16 lesson artifact was found; no completion is inferred.
The next lesson is L001d's validated buy; inspect pending manifests before dispatch because the
October 17 draw of one is allocated to this integration. L001e/f, L002 timing, C003b/C004/C005
and Q004a/Q005b gates remain. October 19 trend work stays conditional. Personal review remains
Not yet reviewed. No input blocks synthetic continuation.

## L001d validated buy - studied October 17, integrated October 18

The bounded whole-unit try_buy operation is integrated after all 11 original input and eight
artifact hashes/sizes matched. Three hand-authored accepted transitions and eleven rejected
unchanged states reproduce the original results in two fresh sanitizer builds, each run twice.
Omitted-fee and fee-on-rejection controls fail as intended. make cpp-validated-buy now joins
make check; 608 Python tests, quality checks and all existing C++ checks pass. The revised
four-page teaching PDF is verified; original study date and evidence are preserved.

Only L001d is integrated here. Next learning is L001e's independent boundaries; inspect ignored
pending manifests before dispatch because October 18's one-commit allowance is allocated to
this integration. L001f reproduction, L002 timing/future-price invariance, C003b/C004/C005 and
Q004a/Q005b empirical gates remain. Trend implementation stays conditional. Personal review
remains Not yet reviewed, and no input blocks the next synthetic lesson.

## L001e boundaries - studied October 18, integrated October 19

The unchanged buy function agrees with a direct integer-ledger oracle on 8351 selected tuples:
250 accepted and 8101 rejected with unchanged state. Ten original inputs and seven artifacts
match the pending manifest. Two current fresh sanitizer builds reproduce the original result,
each running twice. Exclusive cash/position mutations are detected; the negative-price guard
mutation still survives because the later affordability guard rejects. Preserve this limitation.
make cpp-buy-boundaries now joins make check. Full checks pass 608 Python tests and existing
C++/quality checks; the revised four-page teaching PDF is verified. No empirical claim is made.

Only L001e is integrated here. Next learning is L001f reproduction/consolidation; inspect pending
packages before dispatch because the October 19 draw of one is allocated to this integration.
The October 18 weekly synthesis remains queued separately. L002 timing/future-price invariance,
C003b/C004/C005 and Q004a/Q005b gates remain; trend implementation stays conditional. Personal
review remains Not yet reviewed. No input blocks synthetic continuation.

## L001f reproduction - studied October 19, integrated October 20

The fresh accounting recipe rebuilds five existing C++ programs in temporary storage and
reproduces all five archived JSON sets exactly. Two full recipes, each with two executions
per build, agree with the original evidence. All 24 original inputs and seven pending artifacts
match their hashes/sizes. The changed-cash archive is rejected and actual -O execution refused.
make cpp-accounting-reproduce now joins make check. Full checks and the four-page teaching PDF
pass. This proves current-toolchain output reproduction, not identical binaries across platforms,
sequence correctness or decision timing. The known negative-price mutation survivor is retained.

L001's bounded repository teaching slice is complete; personal review stays Not yet reviewed.
Next learning is L002a's hand decision/execution timeline, then the event/fee/missing-fill contract
before a bounded C++ component. Inspect pending manifests before dispatch. October 18's weekly
synthesis remains queued; preserve newer progress when integrating its plan. L002 timing and
future-price invariance, C003b/C004/C005 and Q004a/Q005b remain gates. Trend and later strategy
windows are conditional; no catch-up lessons or empirical claim. No input blocks synthetic work.
