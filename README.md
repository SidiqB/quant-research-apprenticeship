# Quant Research Apprenticeship

A continuing research programme in systematic investing, market microstructure and derivatives.
The emphasis is on reproducible experiments, correct information timing and explicit model limitations.

## Current evidence

| Date | Completed work | Evidence |
|---|---|---|
| 2026-10-19; integrated October 20 | L001f fresh accounting reproduction | Five fresh C++ builds, exact archived results, failure controls and verified four-page note |
| 2026-10-15; integrated October 17 | L001c account struct | Original hashes verified; exact fresh builds; swapped-field control; verified four-page note |
| 2026-10-14 | L001b fixed buy and fee equations | Independent cash ledger; two rejected mutations; verified four-page teaching note |
| 2026-09-21 | Point-in-time observation and revision selection | Tested implementation; deterministic leakage counterexample |
| 2026-09-22 | Chronological holdout with forward-label purging | 49 tests; two synthetic overlaps removed; five-page teaching note |
| 2026-09-23 | First C++ savings calculation | Hand-calculated output test; 50.00 interest and 1050.00 closing balance; four-page teaching note |
| 2026-09-24 | Versioned experiment manifests and source checksums | 94 tests; four source hashes verified; changed-byte rejection; four-page teaching note |
| 2026-09-25 | Universe contract and data-source admission | 144 tests; 24 downgrade controls; two sources remain unverified; five-page teaching note |
| 2026-09-26 | UTC availability across clock changes | 167 tests; 10,800 oracle comparisons; future-fold leak fixed; four-page teaching note |
| 2026-09-27 | Strict source-zone observation ingestion | 257 tests; eight invalid batches rejected; explicit fold/gap policy; four-page teaching note |
| 2026-09-27 | First weekly synthesis and backlog replan | Replayed evidence; calendar/access tasks split; verified weekly PDF |
| 2026-09-28 | Bounded calendar and pre-open decision contract | 292 tests; 33 explicit dates; six rejected corruptions; four-page teaching note |
| 2026-09-29 | Bounded session and decision validation | 363 tests; 22 valid decisions; 132 boundary checks; four-page teaching note |
| 2026-09-30 | Reusable C++ annual savings growth | 66 C++ checks; 363 Python tests; compound-versus-simple demo; four-page teaching note |
| 2026-10-01 | Synthetic split/dividend returns | 415 Python tests; eight hand cases; 162 exact-ledger comparisons; four-page teaching note |
| 2026-10-02 | Historical membership intervals | 470 Python tests; eight date sets; 192 event-ledger comparisons; four-page teaching note |
| 2026-10-03 | Cash terminal evidence separate from membership | 540 Python tests; six hand states; 108 exact-ledger comparisons; four-page teaching note |
| 2026-10-04 | Availability-aware lagged return features | 602 Python tests; 125 exact wealth paths; 420 timing/window comparisons; four-page teaching note |
| 2026-10-04 | Second weekly synthesis and curriculum refinement | 608 Python tests; 66 fresh C++ checks; eleven exact replays; verified weekly PDF |
| 2026-10-05 | C003a text-versus-value intuition | Five hand cases; compiled conversion demo; independent Decimal check; verified four-page note |
| 2026-10-07 | C003a grammar and range contract | Two compiled conversion counterexamples; exact output check; verified four-page note; parser next |
| 2026-10-08 | C003a whole-year parser implementation | 30 parser checks; 608 Python tests; four output fixtures; verified four-page note |
| 2026-10-09 | C003a independent boundary verification | 75 exact Python/C++ comparisons; two rejected mutations; verified four-page note |
| 2026-09-21 | Employer role mapping and research programme | 49 deduplicated postings across eight firms; roadmap through December |

The experiments use synthetic data to demonstrate timing errors and validate financial arithmetic. They report no alpha.
The three laboratories are under development; shared availability selection and label purging are implemented.
Availability observations and decisions now normalize to UTC, repairing the daylight-saving fold leak.
The purging splitter also uses UTC. Strict ingestion now requires explicit source offsets, validates
local clocks against a declared zone, and rejects malformed rows and duplicate versions.
The bounded calendar now validates pre-open decisions separately from core trading hours and requires
complete prior-session windows. Unknown calendar coverage raises an explicit error.
Corporate-action arithmetic now separates raw price, capital and total returns with explicit share
and dividend units; missing actions cannot silently default to no action.
Historical membership now uses stable IDs and effective-date intervals with explicit coverage.
Inactive members remain in earlier universes; publication vintages and completeness need upstream evidence.
Terminal cash valuation now retains holdings and distinguishes missing evidence from explicit zero.
Complete cash entitlement is valued at par; settlement and information-vintage integration remain separate.

Lagged features now link declared one-session returns over exact prior-session windows and select
only available revisions. Missing intervals remain explicit; valid future additions preserve earlier results.

## Reproduce

Python 3.11+, Git, Make, and a C++17-capable Clang or GCC compiler are required for the full checks.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,reports]'
make check
make experiment
make purging-experiment
make manifest-experiment
make access-experiment
make fold-experiment
make ingestion-experiment
make calendar-audit
make calendar-experiment
make corporate-action-experiment
make membership-experiment
make terminal-experiment
make lagged-return-experiment
make cpp-savings
make cpp-text-years
make cpp-conversion-contract
make cpp-years-oracle
make cpp-fractional-failure
make cpp-years-readiness
make cpp-marked-wealth
make cpp-buy-equations
make cpp-account-state
make cpp-validated-buy
make cpp-buy-boundaries
make cpp-accounting-reproduce
make note
```

Use `make note NOTE_DATE=YYYY-MM-DD` to rebuild a specific daily note.

See `requirements-lock.txt` for the initial tested environment. The core package has no runtime dependencies.

## Navigate

- [Research roadmap](ROADMAP.md) and [daily backlog](BACKLOG.md)
- [Research principles](CHARTER.md) and [data policy](data/README.md)
- [Role-skill evidence](career_research/role_skill_analysis.md)
- [First experiment](experiments/availability/README.md)
- [Label-purging experiment](experiments/purging/README.md)
- [Manifest provenance audit](experiments/manifests/README.md)
- [Universe and access contract](data/universe-and-access.md) and [admission experiment](experiments/data_access/README.md)
- [C++ savings growth](cpp/projects/savings_growth/README.md) and [C++ learning plan](CPP_LEARNING_PLAN.md)
- [Clock-change availability experiment](experiments/timezones/README.md)
- [Strict ingestion experiment](experiments/ingestion/README.md)
- [Calendar/decision contract](data/calendar-and-decisions.md) and [bounded fixture audit](experiments/calendar/README.md)
- [Corporate-action return fixture](experiments/corporate_actions/README.md)
- [Historical membership fixture](experiments/membership/README.md)
- [Terminal cash evidence fixture](experiments/terminal/README.md)
- [Lagged return fixture](experiments/lagged_returns/README.md)
- [Latest learning note](research_log/2026-10-10.md) and [PDF](reports/daily/2026-10-10-learning-note.pdf)
- [Daily validation evidence](reports/milestone/2026-10-10-validation.md)
- [Weekly synthesis](reports/weekly/2026-09-27-synthesis.md), [PDF](reports/weekly/2026-09-27-synthesis.pdf) and [validation](reports/weekly/2026-09-27-validation.md)
- [Daily operating procedure](OPERATIONS.md)

Future milestones cover investable universes, signal validation, execution accounting and hedging experiments.
Project outputs must be understood and reproduced before being used as personal interview claims.

## October curriculum update

[C++ strategy curriculum](QUANT_CURRICULUM.md) and [daily learning plan](CURRICULUM_BACKLOG.md)
now guide new projects through 31 December. Study major families slowly, including two weeks of
statistical arbitrage. [Commit cadence](COMMIT_CADENCE.md) records the requested daily 0-3 draw.

## Latest weekly synthesis

[October 4 synthesis](reports/weekly/2026-10-04-synthesis.md),
[verified PDF](reports/weekly/2026-10-04-synthesis.pdf) and
[validation](reports/weekly/2026-10-04-validation.md) distinguish tested accounting from missing
source/settlement evidence. The active next step is C003a whole-year parsing, not the superseded
October 5 ranking date. The shared 0-3 publication draw begins October 5; study pace stays one concept daily.

C003a has a parser, independent boundary oracle and [fractional-input failure check](experiments/years_parser/README.md).
The failure lesson was studied October 10 and integrated October 11 after the zero-budget day.
The next lesson is reproduction/teach-back, then consolidation; inspect ignored pending manifests
before dispatch. C003a remains in progress. Personal review remains Not yet reviewed.

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

## Weekly evidence integrated October 22

The [October 12-18 synthesis](reports/weekly/2026-10-18-synthesis.md) and
[verified PDF](reports/weekly/2026-10-18-synthesis.pdf) preserve the original study period;
[current validation](reports/weekly/2026-10-22-integration-validation.md) records revalidation.
L001 accounting is complete within its bounded teaching scope. L002a's October 20 timeline
is locally complete pending integration; L002b's event/fee/missing-fill contract comes next.
The curriculum now explicitly defers trend for timing prerequisites; later windows are conditional.
Inspect pending manifests before dispatch. Personal review remains Not yet reviewed.

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
