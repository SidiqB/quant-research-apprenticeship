# Quant Research Apprenticeship

A continuing research programme in systematic investing, market microstructure and derivatives.
The emphasis is on reproducible experiments, correct information timing and explicit model limitations.

## Current evidence

| Date | Completed work | Evidence |
|---|---|---|
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
- [Latest learning note](research_log/2026-10-04.md) and [PDF](reports/daily/2026-10-04-learning-note.pdf)
- [Daily validation evidence](reports/milestone/2026-10-04-validation.md)
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
