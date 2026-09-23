# Changelog

## 2026-09-23

- Completed C001 with a small fixed-input C++ savings example: 1000 units at 5% for one year gives
  50 units of interest and 1050 units closing wealth, under explicitly synthetic assumptions.
- Added warning-clean C++17 build/run targets and a hand-authored output comparison to make check;
  49 existing Python tests still pass. A separate wrong-rate diagnostic failed the comparison as intended.
- Wrote the beginner teaching note, verified its four-page PDF text and layout, and recorded validation.
- Marked C002 ready for the next Wednesday slot; preserved Q003 as the next non-C++ task and Q005a as open.
  Personal review remains Not yet reviewed. No empirical return or performance-speedup claim is made.

## 2026-09-22

- Implemented a chronological holdout with closed-interval label purging, explicit audit indices,
  UTC timestamp normalization and validation of windows, IDs and ordering.
- Added 24 tests, including endpoint equality, empty training, daylight-saving folds, independent
  overlap checks and deterministic experiment reproduction; 49 total tests pass.
- Added a synthetic variable-horizon experiment: chronology and a one-row gap both retain two
  overlapping labels; interval purging removes both and preserves two safe training samples.
- Wrote the teaching note and verified five-page PDF; added a dated note target and experiment command.
- Recorded the existing availability selector's named-zone fold defect as Q005a before ingestion;
  UTC-normalized inputs remain the documented workaround. No empirical performance claim is made.
- Completed Q002, made Q003 ready, and preserved Wednesday's C001 learning slot and personal review status.

## 2026-09-21

- Established standalone Python package, research charter, data policy and continuous-integration checks.
- Implemented timezone-aware point-in-time selection with revision, latency, staleness and duplicate checks.
- Added deterministic synthetic leakage experiment, unit tests and learning-note rendering workflow.
- Researched 49 current employer postings and prioritised a dated research backlog through 31 December.
- Refined role keyword coding to distinguish software testing from financial backtesting and options from optional wording.
- Verified initial GitHub validation and documented daily/weekly schedule prompts and activation dependency.
- Activated daily 08:00 and Sunday 16:00 research schedules against the saved local main checkout.
- Added the requested progressive C++ finance learning track, starting with savings arithmetic and using Wednesday research slots.
