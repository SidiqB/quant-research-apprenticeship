# Roadmap: 21 September - 31 December 2026

This is a research programme with acceptance gates, not a promise that three production platforms
will be finished in 102 days. Daily tasks are in BACKLOG.md. Re-plan each Sunday from actual evidence.
The role study prioritises Python, validation, statistics, data integrity and communication, then
execution and derivatives depth. Advanced modelling and C++ remain conditional.

| Phase | Target dates | Deliverables | Gate |
|---|---|---|---|
| 0: Foundations | Sep 21-27 | Package, role study, data policy, availability and validation contracts | Reproducible experiment; tests; lawful data plan |
| 1: Systematic alpha | Sep 28-Oct 25 | Time-varying universe, momentum/reversal, IC, portfolio accounting, costs, chronological validation | Data audit; zero leakage in fixtures; explicit empirical limitations |
| 2: Microstructure | Oct 26-Nov 15 | Price-time book, ledger, event replay, latency, TWAP/VWAP/participation, shortfall | Conservation, deterministic replay, fair policy comparison |
| 3: Derivatives and risk | Nov 16-Dec 13 | Pricing, Greeks, implied volatility, numerical methods, hedging, VaR/ES and stress | Parity, convergence, accounting and model-risk checks |
| 4: Integration | Dec 14-31 | Shared manifests, performance profiling, reproduction, synthesis and interview material | Clean reproduction and claims linked to evidence |

## Current status

Phase 0 underway. Q001 implements availability/revision selection and a synthetic leakage counterexample.
Q002 is next: purge training-label intervals that overlap evaluation decisions.
No empirical alpha result, live order-book calibration or options-market result exists yet.

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

C++: only a measured hot path with a tested Python reference qualifies. If none exists, publish the profiling result.

## Scheduling and recovery

Daily research: 08:00 Europe/London. Weekly synthesis: Sunday 16:00 Europe/London.
Read OPERATIONS.md. Automation activates only after the first manual cycle passes. Failed or blocked days produce
an honest status record, not a token contribution. Material direction changes become documented questions while
independent authorised work continues. Personal review is encouraged but does not gate routine progress.
