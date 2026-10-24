# Active revision - 4 October 2026

[QUANT_CURRICULUM.md](QUANT_CURRICULUM.md) and [CURRICULUM_BACKLOG.md](CURRICULUM_BACKLOG.md)
now govern future work through New Year. C++ is the default; the prior Wednesday-only rule and unfinished
phase dates below are superseded. Completed work and evidence remain valid. See COMMIT_CADENCE.md.

# Roadmap: 21 September - 31 December 2026

This is a research programme with acceptance gates, not a promise that three production platforms
will be finished in 102 days. Daily tasks are in CURRICULUM_BACKLOG.md; BACKLOG.md retains dependency history. Re-plan each Sunday from actual evidence.
The role study prioritises Python, validation, statistics, data integrity and communication, then
execution and derivatives depth. Advanced modelling remains conditional. A gradual finance-focused C++ learning track is now scheduled.

| Phase | Target dates | Deliverables | Gate |
|---|---|---|---|
| 0: Foundations | Sep 21-27 | Package, role study, data policy, availability and validation contracts | Reproducible experiment; tests; lawful data plan |
| 1: Systematic alpha | Sep 28-Oct 25 | Time-varying universe, momentum/reversal, IC, portfolio accounting, costs, chronological validation | Data audit; zero leakage in fixtures; explicit empirical limitations |
| 2: Microstructure | Oct 26-Nov 15 | Price-time book, ledger, event replay, latency, TWAP/VWAP/participation, shortfall | Conservation, deterministic replay, fair policy comparison |
| 3: Derivatives and risk | Nov 16-Dec 13 | Pricing, Greeks, implied volatility, numerical methods, hedging, VaR/ES and stress | Parity, convergence, accounting and model-risk checks |
| 4: Integration | Dec 14-31 | Shared manifests, performance profiling, reproduction, synthesis and interview material | Clean reproduction and claims linked to evidence |

## Current status

Phase 0 underway. Q001 implements availability/revision selection and a synthetic leakage counterexample.
Q002 now implements past-only label-interval purging with explicit boundary and empty-set behavior.
Its synthetic experiment removes two overlapping training labels and retains two safe labels; 49 tests pass.
C001 now provides a compiled one-year savings example with a hand-calculated output check and teaching note.
Q003 now provides versioned manifests and SHA-256 provenance checks; 94 tests pass.
Q004 now specifies a provisional US common-stock universe and compares CRSP/Norgate access evidence.
Its eight-gate declaration checker and synthetic selection example pass 50 new tests (144 total).
Neither real source is admitted; Q004a tracks entitlement and sample audit before empirical research.
Q005a now normalizes availability timestamps to UTC: the future-fold leak is fixed, and 167 tests pass.
Its 10,800 integer-oracle comparisons cover London/New York spring and autumn transitions.
Q005 now validates complete observation batches, including explicit-offset folds and gap rejection.
All 257 tests pass; eight invalid experiment controls are rejected and two valid revisions remain usable.
Q007's first weekly synthesis is complete. Q006a now specifies the calendar/decision contract with a
33-date prospective NYSE fixture; all 292 tests pass, including six corrupted-fixture controls.
Q006b now implements bounded lookup, decision/core validation and complete prior-session history.
All 363 tests pass; 22 valid decisions and 132 boundary checks pass, with nine rejected controls.
Q006 is complete within its bounded scope. C002 now implements reusable annual compound savings
growth: 66 C++ checks and a hand-authored demonstration pass alongside 363 Python tests.
C003 is split into C003a whole-year parsing and later C003b complete CLI; see the active curriculum.
Q008 synthetic corporate-action returns is complete: eight hand cases, 162 exact-ledger comparisons
and three wrong controls pass; all 415 Python tests and 66 C++ checks pass. The four-page PDF is verified.
Q009a historical membership is complete: eight exact date sets, 192 event-ledger comparisons and
55 new tests pass (470 total). The verified four-page note separates effective dates from knowledge
at decision time. Q009b is now complete: six terminal-evidence states, 108 exact-ledger comparisons
and 70 new tests pass (540 total), with a verified four-page note. Holdings remain explicit after
membership exit; unknown proceeds do not imply zero. The bounded Q009 parent is complete.
Q010 lagged features is complete: exact prior-session return linking with availability-aware revision
selection, explicit missingness and retained selected records. All 602 Python tests pass, including 125 exact
wealth paths and 420 window/timing comparisons; the four-page teaching PDF is verified. Q011 remains
a deferred curriculum dependency. Q014 is complete with the October 4 weekly synthesis.
Q004a1 permissions and Q004a2 licensed sample audit remain blocked. Q005b is split into source/knowledge contract Q005b1 and two-batch adapter Q005b2,
with Q013 still required before empirical use. Phase 0's bounded calendar gate is complete; Phase 1 starts with
synthetic mechanics only. Original later-phase dates are superseded by QUANT_CURRICULUM.md. Current checks pass 608 Python
tests, 66 fresh C++ checks and eleven exact two-run JSON replays; no coverage percentage was measured.
No empirical alpha result, live order-book calibration or options-market result exists yet.

C003a's October 5 intuition slot is complete: five hand classifications and a compiled conversion
example show why an integer argument cannot recover a discarded fraction. Two exact replays and
an independent Decimal ledger pass with 608 Python tests, 66 C++ checks and both output fixtures.
The four-page teaching PDF is verified. C003a remains in progress; October 6 defines grammar/range
and October 7 implements the parser. Personal review remains Not yet reviewed.

C003a's grammar/range prerequisite is complete on October 7 after the interrupted October 6 run.
The contract requires complete ASCII decimal digits in the nonnegative int range. A fixed C++
experiment demonstrates successful prefix conversion and complete negative conversion; neither
satisfies the contract. Three output fixtures, 66 C++ checks and 608 Python tests pass, and the
four-page PDF is verified. Parser implementation is next on October 8; remaining steps shift in
dependency order. The earlier October 6/7 plan above is superseded without backdating progress.

## Long-term scope and conditional extensions

Alpha: add value and quality only after obtaining fundamentals with release vintages; volatility/liquidity signals
follow validated prices and volumes. Add constrained portfolios, covariance shrinkage and attribution after accounting.
Use linear baselines before selected nonlinear models. Regime studies and multiple-testing corrections must report
uncertainty, test counts and selection effects. Do not claim point-in-time validity from current constituents alone.

Microstructure: queue priority and latency require declared assumptions. Synthetic replay establishes software
correctness; calibration and trade-sign research need licensed event data. No exchange realism is claimed from a toy book.

Derivatives: option chains need quote-time alignment and licence review. Smiles/surfaces require static-arbitrage
checks. Local volatility and Heston are optional extensions beyond a validated baseline; calibration quality and
identifiability determine whether implementation is justified within 2026.

C++ learning: follow [CPP_LEARNING_PLAN.md](CPP_LEARNING_PLAN.md), starting with a simple savings calculator.
C++ is the default under the October 4 curriculum, beginning with one years-only parsing slice. Production acceleration still requires a
measured hot path and a tested reference; educational projects do not require a speedup justification.

## Scheduling and recovery

Daily research: 08:00 Europe/London. Weekly synthesis: Sunday 16:00 Europe/London.
Read OPERATIONS.md. Automation activates only after the first manual cycle passes. Failed or blocked days produce
an honest status record, not a token contribution. Material direction changes become documented questions while
independent authorised work continues. Personal review is encouraged but does not gate routine progress.

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

## Weekly refinement - written October 18, integrated October 22

The October 12-18 synthesis and regenerated verified PDF are in reports/weekly. Original evidence
and current integration validation are kept separate. All 67 original inputs, five artifacts and
five QA records verify, including eight changed inputs checked at their original Git baseline.
The saved plan is merged against completed L001e/f progress. L002a was studied October 20 and
is complete locally pending publication; L002b's event/fee/missing-fill contract is next.
No October 21 package was found; no completion or reason is inferred. Inspect pending manifests.

Trend's October 19-25 window is deferred for L002a-f prerequisites; later strategy windows remain
conditional. C004 returns/vectors, C005 statistics, C003b CLI, Q011/Q012/Q013 and Q004a/Q005b gates
are preserved. No extra lesson is added to fill today's draw of one. Full checks pass 608 Python
tests and existing C++/quality checks. Personal review stays Not yet reviewed; no empirical claim.

## L002a timeline - studied 2026-10-20, integrated 23 October

Four hand rows match per-share Decimal accounting; three corrupt fixtures are rejected.
Original pending provenance and results are preserved in experiments/portfolio_accounting.
The fixture verifier now joins make check; current checks and regenerated teaching PDF are
validated before publication. Original work date is retained; personal review stays Not yet reviewed.
L002a is integrated. L002b was studied October 22 and remains separately pending;
next new learning is L002c, one bounded C++ delayed order. L002d-f timing/invariance and
C003b/C004/C005/Q011-13/Q004a/Q005b remain gates. Trend/later windows remain conditional.
No empirical result or personal mastery is claimed. No input blocks synthetic continuation.

## L002b event contract - studied 2026-10-22, integrated 23 October

Six hand/reference outcomes agree; ten invalid traces and five corrupt tables are rejected.
Original pending provenance and results are preserved in experiments/portfolio_accounting.
The fixture verifier now joins make check; current checks and regenerated teaching PDF are
validated before publication. Original work date is retained; personal review stays Not yet reviewed.
L002a/b is integrated. L002b was studied October 22 and integrated here;
next new learning is L002c, one bounded C++ delayed order. L002d-f timing/invariance and
C003b/C004/C005/Q011-13/Q004a/Q005b remain gates. Trend/later windows remain conditional.
No empirical result or personal mastery is claimed. No input blocks synthetic continuation.

## L002c delayed C++ order - studied October 23, integrated October 24

Eight hand/reference traces and fifteen invalid integer traces pass in two fresh UBSan builds,
each executed twice. Three compiled mutants are detected and actual -O is refused. All 27
original provenance records verify; original source/results/study evidence are preserved.
make cpp-delayed-order now joins make check. Current full checks and the revised teaching
PDF are verified before publication. No general future-price invariance claim is made here.
Next learning is L002d: paired valid future-price mutations and a leaking control. L002e/f,
C003b/C004/C005/Q011-13/Q004a/Q005b remain gates; later strategy windows are conditional.
Personal review stays Not yet reviewed. No input blocks synthetic continuation.
