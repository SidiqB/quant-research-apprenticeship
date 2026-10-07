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
