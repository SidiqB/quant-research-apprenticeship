# Validation evidence - 17 October 2026

L001d introduces one bounded whole-unit buy operation. Question and protocol are in the teaching
note, with official Microsoft, Python and Clang sources. Three accepted cases match hand-authored
cash/share results; eleven rejected cases retain both original fields. Two fresh C++17 builds,
each run twice, give exact stdout, empty stderr and exit zero with undefined-behavior sanitizer
support enabled. JSON replays match. Apple Clang 21.0.0, arm64, was observed. Correct code passed
first execution; formatting was applied before execution. No market data or dependency added.

Omitted-fee and rejected-order fee-deduction scratch variants compile and fail the intended
output comparison with verifier exit 1. Real -O invocation is refused. Negative controls and
source/result hashes are recorded separately. Scratch mutations never replace the correct source.
The fixed cases are implementation checks; independent generated boundary verification remains
L001e, including each negative and upper-bound policy edge. No coverage percentage is claimed.

The shared full make check passes 608 Python tests, Ruff/56 files, strict mypy/21 package files,
66 savings and 30 parser checks, 75 oracle cases, four golden outputs, fractional controls,
readiness traces, marked wealth, buy equations and the newly integrated struct check. Eleven
standard Make binaries were freshly compiled, plus temporary readiness/struct executables.
The pending verifier separately passes Ruff lint/format. pip consistency passes with a cache
warning. The pending buy is not yet part of main or remote CI.

The final teaching PDF has four pages. Full normalized extracted text equals all 10695 source
characters; renderer headings/origins pass and every final Poppler page was visually inspected.
An initial five-page version had a one-line spill; shortening the introductory paragraph removed
it, then full text and rendering checks were repeated. Final render log is empty. One PDF-operation
marker covered the two PDFs created in this run; no dependency installation was required.

The October 17 draw is one. That slot integrates October 15's previously completed L001c, whose
original 11 inputs/nine artifacts all matched. Today's sole new learning unit, L001d, stays in
ignored pending storage with this evidence, verified PDF, progress and integration manifest.
No saved October 16 lesson was found; no reason for its absence or review transition is invented.
Personal review remains Not yet reviewed. Next learning is L001e boundaries, not a repeat of L001d.
L001f reproduction, L002 timing, C003b/C004/C005 and Q004a/Q005b gates remain; trend stays conditional.

The run held the shared lock. Restricted DNS prevented initial fetch; first approval timed out,
then the allowed single retry fetched successfully. No open issues and successful baseline CI.
Publication outcomes belong in the final run memory/receipt. No input blocks synthetic continuation.

## Integration validation - 18 October 2026

The preceding sections preserve original October 17 observations. Integration starts from clean
main ce2ce13358b19cd730c64a9c38412c72c067c8e8 under the shared atomic lock. All 11 original inputs
and eight artifacts matched their SHA-256/size manifest before copying. The C++ source, original
result and original experiment evidence are preserved byte-for-byte. The verifier's default path
now points to the published C++ source, and make cpp-validated-buy is included in make check.
No shared header or broader educational scope is introduced.

Two fresh current C++17 sanitizer builds, each executed twice, reproduce the original JSON exactly.
Omitted-fee and fee-on-rejection scratch controls compile then fail the intended comparison with
verifier exit 1. A real -O call is refused. Current control results and source/result hashes are
in integration-2026-10-18.json. Apple Clang 21.0.0 on arm64 was observed. Full make check passes
608 Python tests, Ruff/57 formatted files, strict mypy/21 package files, 66 savings and 30 parser
checks, 75 parser boundary comparisons, four golden outputs and all accounting/readiness/failure
checks including the new target. Eleven standard Make executables were freshly compiled following
the Makefile change; readiness, struct and buy checkers also compile temporary drivers. pip check
passes with the existing disabled-cache warning. No dependencies or coverage percentage added.

The revised final PDF has four pages with an exact 10716-character normalized source-text match.
Renderer heading/origin checks pass; every final Poppler page was visually inspected. Final
render log is empty. No layout repair was needed; original pending files remain untouched.
The single PDF-operation marker covered this PDF and the separate pending October 18 note.
Microsoft integer-operator and Clang sanitizer documentation were consulted again on October 18.

Restricted fetch failed DNS; approved fetch succeeded. Local main and fetched origin matched,
zero open issues were observed, and baseline CI run 39068947035 succeeded. No platform rejection
or permission bypass. Shared London draw one was confirmed twice; actual prior commits today
were zero. This integration is the sole prepared commit. All staged text and extracted PDF text
are checked for sensitive/contact/branding patterns, local links and file sizes; git diff --check
is required before committing. Final publication outcome belongs in run memory and the receipt.
Today's separate L001e learning package remains ignored after allocation of the sole slot.
Personal review remains Not yet reviewed; no input blocks synthetic continuation.
