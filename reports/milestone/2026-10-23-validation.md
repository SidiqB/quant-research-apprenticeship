# L002c integration validation - 24 October 2026

Original study date is October 23. All 14 inputs, eight artifacts and five QA records match
original SHA-256 and byte counts before integration. Original manifest, results and validation
are preserved under experiments/portfolio_accounting; pending bytes are untouched. The C++
source is identical. Verifier changes only ROOT/default source paths; Make adds cpp-delayed-order.

Two fresh warning-clean C++17 UBSan builds, each run twice, reproduce the original result JSON
exactly: eight hand/Decimal cases and fifteen invalid integer traces. Three compiled scratch
mutants fail the intended trace comparison: old-price debit, fee-on-missingness and equal
resolution. Actual Python -O refuses execution. Current validation evidence is saved separately
from original experiment-validation. No general future-price invariance proof is claimed.

make check passes 608 Python tests, Ruff lint/62 formatted files, strict mypy/21 package files,
66 savings and 30 parser checks, 75 parser comparisons, four golden outputs, all prior accounting,
8351 buy-boundary comparisons, fresh accounting reproduction, timeline/contract and new delayed
checks. Make rebuilds standard binaries after the Makefile change; temporary drivers compile fresh.
pip --no-cache-dir check passes. No dependency, market data or measured coverage percentage added.

Final teaching PDF has four pages and 11539 normalized characters exactly matching the source.
Renderer heading/page-origin checks pass; all four final Poppler pages visually inspected with
no layout defect. Render log empty. First integration render had a blank spill page after the
first table; shortening the study/integration line removed it, then all checks were repeated.
Original study PDF is unchanged. Staged file/PDF scan and whitespace checks pass before commit;
local links resolve, each file is under 1 MB, and the repository retains its no-reply identity.

Shared October 24 draw is two; this integration is the first independent unit. Publication and
remote/CI observations are recorded after pushing in the run receipt and automation memory.
L002d is next new learning; L002e/f and empirical/foundation gates remain. Personal review stays
Not yet reviewed. No input blocks synthetic continuation.
