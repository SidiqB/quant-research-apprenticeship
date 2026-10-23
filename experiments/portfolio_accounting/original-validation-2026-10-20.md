# Validation - 20 October 2026

L002a is a hand decision/execution timeline, not an implemented event engine. The question,
hypothesis, four-event fixture, units, protocol, sources and limitations are in today's note.
All data are explicitly synthetic with ordered teaching events, no market sample or returns claim.

A Python Decimal reference debits one share at a time and adds each marked share independently
of the hand note's multiplication formulas. All four rows agree. Decision: cash 800/shares 4.
Assumed fill: cash 693/shares 6/wealth 1005. Later mark: wealth 987. Two executions produce
identical JSON with fixture SHA-256. Three copied inconsistent fixtures fail the intended
checks: unavailable decision input, premature trade, and old-price fill debit. These controls
validate a fixed table, not general future-price invariance of a reusable engine.

A real -O invocation fails as intended. Ruff lint/format pass after correcting one long string;
there were no runtime arithmetic failures. No new C++ concept or production behavior was added.
C++ remains the default for L002c after the event/fee/missing-fill contract. Shared make check
passes 608 Python tests, 59 formatted files, mypy's 21 source files and all existing C++ checks,
including integrated reproduction. pip --no-cache-dir check passes without dependency changes.

The four-page PDF exactly matches 9505 normalized source characters; renderer headings/origins
pass. Every final Poppler page is visually checked. Initial font configuration/cache warnings
are resolved using the project's existing temporary-font configuration before final inspection.
Final rendering logs/text evidence are in work/run-2026-10-20/. No source/PDF changes follow QA.

The sole commit slot is allocated to integrating October 19 L001f. This entire new lesson stays
under ignored work/pending/2026-10-20/ with original work date, inputs, artifacts, destinations,
checks and local progress. No tracked file is changed for this new lesson. The October 18
weekly synthesis remains separately pending; inspect both manifests before future dispatch.
Next learning is L002b's event/fee/missing-fill contract, then C++ implementation. L002d-f,
C003b/C004/C005, Q011/Q012/Q013 and Q004a/Q005b remain. Personal review is Not yet reviewed.
