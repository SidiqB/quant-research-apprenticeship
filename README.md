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
| 2026-09-21 | Employer role mapping and research programme | 49 deduplicated postings across eight firms; roadmap through December |

The experiments use synthetic data to demonstrate information-timing errors. They report no alpha.
The three laboratories are under development; shared availability selection and label purging are implemented.
The availability selector currently requires UTC-normalized inputs for safe daylight-saving fold comparisons;
its named-zone regression is recorded in BACKLOG.md as Q005a. The new purging splitter normalizes to UTC.

## Reproduce

Python 3.11+, Git, Make, and a C++17-capable Clang or GCC compiler are required for the full checks.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,reports]'
make check
make experiment
make purging-experiment
make manifest-experiment
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
- [First C++ savings example](cpp/projects/savings_growth/README.md) and [C++ learning plan](CPP_LEARNING_PLAN.md)
- [Latest learning note](research_log/2026-09-24.md) and [PDF](reports/daily/2026-09-24-learning-note.pdf)
- [Daily validation evidence](reports/milestone/2026-09-24-validation.md)
- [Daily operating procedure](OPERATIONS.md)

Future milestones cover investable universes, signal validation, execution accounting and hedging experiments.
Project outputs must be understood and reproduced before being used as personal interview claims.
