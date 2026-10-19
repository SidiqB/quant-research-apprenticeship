# Boundary verification - 18 October 2026

L001e asks whether the unchanged bounded buy agrees with a direct Python integer ledger at policy
edges and affordability/position thresholds. Primary Python, Microsoft and Clang references are
cited in the teaching note. No historical period, external data, new dependency or alpha claim.
Only boundary verification is new learning; yesterday's already-studied buy is separately integrated.

Six hand anchors constrain the reference. The 7776-tuple six-value Cartesian grid plus 575 unique
threshold neighbors produce 8351 comparisons: 250 accepted, 8101 rejected unchanged. Two separate
fresh warning-clean C++17 UBSan builds run every case twice, with exact line comparisons, full
output count, empty stderr and exit zero. JSON reports match exactly. Input and expected-output
hashes identify the deterministic generated fixture; production source hash is recorded. Each
case starts from fresh state. This is not full-domain, sequence or information-timing verification.

Cash and position exclusive-equality mutants compile and fail on intended boundary mismatches.
A third mutant changes price_units <= 0 to price_units == 0 and survives with exit zero. The
initial test runner incorrectly expected detection and stopped; this failed expectation was
investigated and retained. With nonnegative available cash and negative price the quotient is
nonpositive, so positive quantity still rejects at the later affordability guard. The observed
survivor is compatible with redundant rejection, not an accepted negative-price trade. The
original positive-price guard is retained. Real Python -O is refused. All control results are
saved in experiment-validation.json, including the survivor and its explanation.

One pre-execution lint failure was an overlong scope-description string, shortened before the
first correct fixture run. Pending Ruff lint/format pass. Full make check passes 608 Python tests,
Ruff/57 files, strict mypy/21 files, 66 savings and 30 parser checks, 75 parser comparisons, four
golden outputs and all prior C++ checks plus today's integrated buy. Eleven standard binaries
freshly compiled because Makefile changed; temporary readiness/struct/buy builds also ran.
The pending boundary verifier is not yet a tracked Make target or part of remote CI. pip check
passes with the existing disabled-cache warning. No measured coverage percentage is claimed.

Final teaching PDF: four pages; exact normalized 10416-character source/text match; renderer
headings/origins pass; all four final Poppler pages visually inspected without layout defects.
Render log empty. The note was corrected after the surviving mutation observation, regenerated
and fully rechecked. No layout repair or dependency installation. One PDF-operation marker
covered both outputs in this run. All deliverable text and extracted PDF text are scanned;
manifest pins input/artifact hashes and intended destinations after the integration commit.

Shared draw one is allocated to L001d integration. Today's files stay in ignored pending storage;
tracked progress records only the integrated unit. Personal review remains Not yet reviewed.
Next learning: L001f reproduction/consolidation. Keep L002 timing/future-price invariance and
C003b/C004/C005 prerequisites; October 19 trend implementation remains conditional. Q004a/Q005b
still gate empirical work. No necessary input for the next synthetic lesson. Publication outcome
and current actual commit count are recorded in run memory and the pending manifest.

## Integration validation - 19 October 2026

Started from clean main 0cbaa0246cc4ffa17fc5f7072d156d5b384af40d under the shared atomic lock.
All ten original inputs and seven artifacts matched SHA-256 and sizes before copying. Original
result and experiment-validation bytes are preserved; the verifier root changes from parents[3]
to parents[1] for its published scripts location. make cpp-buy-boundaries joins make check.
Two fresh current sanitizer builds, each executing twice, reproduce the original JSON exactly.
Both equality mutations fail on intended boundary mismatches; the negative-price guard mutation
still survives, with the same later rejection explanation. A real -O call is refused. Current
evidence is in experiments/portfolio_accounting/integration-2026-10-19.json.

Full make check passes 608 Python tests, Ruff/58 formatted files, strict mypy/21 package files,
66 savings and 30 parser checks, 75 parser oracle comparisons, four golden outputs and all
fractional/readiness/accounting checks including 8351 buy boundaries. Eleven standard Make
executables freshly compile after the Makefile edit; temporary readiness/struct/buy drivers also
compile. pip --no-cache-dir check passes cleanly. No dependencies or coverage measurement added.

The revised PDF has four pages: all 10500 normalized source characters match extracted text,
renderer headings/origins pass and every final Poppler page was visually inspected. Render log
is empty; no layout repair was needed for this PDF. One artifact-operation marker covers this
PDF and today's separate pending reproduction note. Original pending files are unchanged.
Primary Microsoft integer-operator, Python itertools and Clang sanitizer references were refreshed.

Restricted fetch failed DNS; approved fetch succeeded. Main and origin matched; zero open issues
and successful baseline CI run 39110153739 were observed. London draw one was persisted; prior
actual commits today were zero. This coherent integration consumes the sole slot. The weekly
synthesis and today's new L001f learning remain ignored. Final push/CI outcome belongs in memory
and the integration receipt. Personal review stays Not yet reviewed; no input blocks continuation.
