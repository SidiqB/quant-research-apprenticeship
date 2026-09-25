# Source admission and survivor-selection diagnostics

Q004, 25 September 2026. Run `make access-experiment` or
`.venv/bin/python scripts/access_experiment.py --output /tmp/access-results.json`.

The dated [evidence registry](../../configs/data-access-2026-09-25.toml) summarizes public documentation
and unresolved project access. These are human assessments, not observed market data. The
[universe contract](../../data/universe-and-access.md) defines the eight gates and cites primary sources.
An all-verified declaration passes the checklist; every single downgrade to documented, unknown or failed
blocks it. The experiment checks all 24 such downgrades and records zero ready real-source candidates.
This does not authenticate evidence, perform downloads or automatically enforce downstream ingestion.

The separate synthetic example invests 100 invented units each in A, B and C for one invented period.
Final values are 120, 90 and a confirmed zero recovery. The full sample returns -30%; retrospectively
retaining only A and B reports +5%. The difference is 35 percentage points. No costs, cash flows,
rebalancing, sampled market period or empirical estimate is involved. The direction of selection bias
need not be positive in real samples; missing terminal proceeds cannot be assumed zero.

Acceptance protocol fixed before implementation: both unverified candidates block; all eight single-gate
omissions are invalid; all 24 downgrades block; malformed evidence fails; independent arithmetic and exact
JSON repeatability pass. Tests cover these properties. No model selection or threshold tuning occurred.
