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
| 2026-09-21 | Employer role mapping and research programme | 49 deduplicated postings across eight firms; roadmap through December |

The experiments use synthetic data to demonstrate information-timing errors. They report no alpha.
The three laboratories are under development; shared availability selection and label purging are implemented.
Availability observations and decisions now normalize to UTC, repairing the daylight-saving fold leak.
The purging splitter also uses UTC. Strict ingestion now requires explicit source offsets, validates
local clocks against a declared zone, and rejects malformed rows and duplicate versions.

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
- [First C++ savings example](cpp/projects/savings_growth/README.md) and [C++ learning plan](CPP_LEARNING_PLAN.md)
- [Clock-change availability experiment](experiments/timezones/README.md)
- [Strict ingestion experiment](experiments/ingestion/README.md)
- [Latest learning note](research_log/2026-09-27.md) and [PDF](reports/daily/2026-09-27-learning-note.pdf)
- [Daily validation evidence](reports/milestone/2026-09-27-validation.md)
- [Daily operating procedure](OPERATIONS.md)

Future milestones cover investable universes, signal validation, execution accounting and hedging experiments.
Project outputs must be understood and reproduced before being used as personal interview claims.
