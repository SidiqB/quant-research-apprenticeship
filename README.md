# Quant Research Apprenticeship

A continuing research programme in systematic investing, market microstructure and derivatives.
The emphasis is on reproducible experiments, correct information timing and explicit model limitations.

## Current evidence

| Date | Completed work | Evidence |
|---|---|---|
| 2026-09-21 | Point-in-time observation and revision selection | Tested implementation; deterministic leakage counterexample |
| 2026-09-21 | Employer role mapping and research programme | 49 deduplicated postings across eight firms; roadmap through December |

The first experiment uses synthetic data to demonstrate an engineering error. It reports no returns or alpha.
The three laboratories are under development; only the shared availability component is implemented.

## Reproduce

Python 3.11+ and Git are required.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,reports]'
make check
make experiment
make note
```

See `requirements-lock.txt` for the initial tested environment. The core package has no runtime dependencies.

## Navigate

- [Research roadmap](ROADMAP.md) and [daily backlog](BACKLOG.md)
- [Research principles](CHARTER.md) and [data policy](data/README.md)
- [Role-skill evidence](career_research/role_skill_analysis.md)
- [First experiment](experiments/availability/README.md)
- [Daily learning note](research_log/2026-09-21.md) and [PDF](reports/daily/2026-09-21-learning-note.pdf)
- [Daily operating procedure](OPERATIONS.md)

Future milestones cover investable universes, signal validation, execution accounting and hedging experiments.
Project outputs must be understood and reproduced before being used as personal interview claims.
