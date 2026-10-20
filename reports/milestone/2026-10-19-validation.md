# L001f validation - study October 19, integration October 20

The original local study rebuilt five accounting programs, executed each twice and matched
all five archived result sets. Its exact controls/compiler record is preserved in
experiments/portfolio_accounting/validation-2026-10-19.json. The original pending manifest
is preserved in pending-2026-10-19-manifest.json beside it. No study date is backfilled.

Before integration, all 24 original input and seven artifact SHA-256 hashes and sizes matched.
The published recipe, result and original validation JSON are byte-identical to their pending
originals. The recipe already locates the repository from either path. Added a meaningful
cpp-accounting-reproduce Make target to make check and adapted publication/command prose only.
No C++ production function changed. Original ignored artifacts remain intact.

Current integration: two complete recipes each compile five fresh warning-clean C++17 programs
in temporary directories and execute each twice. All five result sets match archives exactly;
both recipe outputs match the original reproduction.json bytes. Struct and fixed demos are
warning-clean; the two buy drivers additionally use UBSan. Apple Clang 21.0.0 was observed.
A scratch archive changing marked cash 800 to 801 fails the intended archive comparison;
a real Python -O invocation is refused. integration-2026-10-20.json records these observations.

Full make check passes 608 Python tests, Ruff lint/format (59 files), strict mypy (21 package
files), 66 savings and 30 parser checks, 75 parser-oracle cases, four golden outputs and all
existing fractional/readiness/accounting checks plus the integrated reproduction. Eleven
standard Make executables rebuild after the Makefile change; temporary verifier drivers also
build afresh. pip --no-cache-dir check passes. No dependencies or measured coverage added.

The regenerated four-page note preserves the original work date, updates the command path
and records October 20 integration. Exact normalized Markdown/PDF text agrees on 9299 characters;
renderer heading and page-origin checks pass. All four final Poppler pages are visually checked.
Initial Poppler renders emitted font configuration/cache warnings; the existing temporary-font
configuration is used for final rendering. Final render logs and the text audit are kept in
ignored work/run-2026-10-20/. Original October 19 pending PDF is unchanged.

This is output reproduction on the current toolchain, not bit-identical binary reproducibility,
a sequence/timing proof, profitability or personal mastery. Preserve L001e's surviving relaxed
negative-price guard mutation: its later affordability guard still rejects. L002 timing and
future-price invariance, C003b/C004/C005 and Q004a/Q005b remain unfinished prerequisites.

One coherent integration uses October 20's shared draw of one. Current timeline study and the
October 18 weekly synthesis remain pending by cadence. Publication/remote verification belongs
in run memory and the integration receipt. Personal review remains Not yet reviewed.
