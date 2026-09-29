# Roadmap: 21 September - 31 December 2026

This is a research programme with acceptance gates, not a promise that three production platforms
will be finished in 102 days. Daily tasks are in BACKLOG.md. Re-plan each Sunday from actual evidence.
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
Q006 is complete within its bounded scope; C002 stays ready for Wednesday September 30.
Q008 corporate actions moves to October 1, Q009 membership/terminal-event children to October 2/3,
and Q010 lagged features to October 4. Q014 is the separate October 4 afternoon review.
Q004a1 permissions and Q004a2 licensed sample audit remain blocked. Q005b provenance/batch integration
follows Q013 before empirical use. Phase 0's bounded calendar gate is complete; Phase 1 starts with
synthetic mechanics only. Original later-phase windows are conditional and will be revisited at Q014.
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

C++ learning: follow [CPP_LEARNING_PLAN.md](CPP_LEARNING_PLAN.md), starting with a simple savings calculator.
Wednesday research slots advance this track from 23 September. Production acceleration still requires a
measured hot path and a tested reference; educational projects do not require a speedup justification.

## Scheduling and recovery

Daily research: 08:00 Europe/London. Weekly synthesis: Sunday 16:00 Europe/London.
Read OPERATIONS.md. Automation activates only after the first manual cycle passes. Failed or blocked days produce
an honest status record, not a token contribution. Material direction changes become documented questions while
independent authorised work continues. Personal review is encouraged but does not gate routine progress.
