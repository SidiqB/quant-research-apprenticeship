# Timeline integration validation - 23 October 2026

Original study: October 20, L002a. Original validation and pending manifest are retained in
experiments/portfolio_accounting; historical publication wording describes that original run.
All 11 input and eight artifact hashes/sizes verify. The changed curriculum backlog verifies
against its original b50d8a7 Git blob; current progress is merged without replacing later work.

Only fixture path/formatting changes affect the integrated verifier. Two executions match the
original result JSON byte for byte. All four hand rows and three corrupt-fixture controls pass;
actual -O invocation is refused. make decision-timeline is now part of make check.
The full current suite passes 608 Python tests, Ruff/60 formatted files, mypy/21 package files,
66 savings checks, 30 parser checks, 75 parser comparisons, four golden outputs and existing
accounting/readiness/reproduction checks. Standard C++ Make targets rebuild after the Makefile
change; temporary drivers/reproduction also compile fresh. pip consistency passes; no dependency added.

The regenerated PDF has four pages and exactly 9606 normalized source/extracted characters.
Renderer heading/origin checks pass. All four final Poppler pages were visually inspected:
no clipping, overlap or misplaced headings; render log empty. Personal review: Not yet reviewed.
Staged content and extracted PDF are scanned before commit. No empirical performance or measured
coverage percentage is claimed. Current run evidence is in work/run-2026-10-23/.

Today draws two shared commit slots. This is the first independent completed integration unit.
L002b is complete locally from October 22 and is next for integration; L002c is next new learning.
L002d-f/C003b/C004/C005/Q011-13 and Q004a/Q005b remain gates. No personal-review approval required.
