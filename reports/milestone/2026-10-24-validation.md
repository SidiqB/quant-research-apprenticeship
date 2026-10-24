# Validation - 24 October 2026

Question: does changing only valid future evidence preserve the earlier request and account
snapshot? L002d tests the unchanged C++ delayed order on a declared synthetic grid. Primary
sources, pre-implementation hypothesis/protocol, equations, worked cases, costs and limitations
are in research_log/2026-10-24.md. Production source remains identical to L002c; no dependency,
market sample, empirical result, performance claim or personal-review transition is added.

## New experiment evidence

Five observed prices and four account pairs form 20 prefixes. Nine future fill choices and
two later event indices form 18 suffixes each. All 360 valid traces preserve caller state;
340 within-prefix past projections match. Independent rule anchors pass for all traces and
all 360 resolution states match a Decimal per-share reference. Six hand anchors agree before
C++ execution. Actual counts: 66 filled, 126 model-rejected, 24 unresolved, 144 no-order.

Two standalone final verifier invocations each freshly compile the correct source and four
separate mutants. Each binary executes twice with identical stdout, empty stderr and zero
exit status. Correct result JSON matches byte-for-byte across the two invocations. Three
mutants fail the intended paired projection check: future-price signal (trace 6), future
cash affordability (trace 12), overwriting the past snapshot (trace 2). Constant no-order
passes invariance but fails the decision anchor. These are detected logical errors after
successful compilation/execution, not accidental compiler failures. Actual Python -O is
refused. The normal Make target also runs all controls; --skip-controls is an explicit
optional diagnostic, never used for the recorded full replays or full checks.

Compiler: Apple Clang 21.0.0; C++17, Wall/Wextra/Wpedantic/Werror and UBSan with recovery
disabled. Result JSON pins source, buy, fixture and complete stdout hashes. Separate dated
validation JSON pins the verifier/reference and result bytes. No exhaustive-history claim:
only selected valid prefixes/suffixes, events 0/1 then 2/9, whole-unit account/price domain.
Malformed futures are excluded from this relation and retain the existing L002c invalid suite.

## Repository and PDF checks

make check passes 608 Python tests, Ruff lint and 63 file formatting checks, strict mypy
for 21 package files, 66 savings and 30 parser checks, 75 parser oracle comparisons, four
golden outputs, all prior readiness/accounting checks, 8351 buy-boundary comparisons, fresh
five-program accounting reproduction, timeline/contract/delayed-order and new invariance
checks. Standard Make binaries rebuild after the Makefile change; temporary probes compile
fresh. pip --no-cache-dir check passes. No coverage percentage was measured.

Initial Ruff run found two overlong strings; split/shortened them and reran lint/format.
The first executable experiment passed. The draft prose's filled/rejected subtotals were
corrected against the actual JSON (66/126) before final PDF verification. Final source and
result claims agree. No production code adjustment was needed to pass the test.

Today's final PDF has four pages and 10754 normalized characters exactly matching Markdown.
Renderer heading/page-origin checks and every-page Poppler visual inspection pass; render
log empty using the existing writable font configuration. No clipping, stranded tables or
layout defects. Integration PDF also has four verified pages; its initial blank spill page
was fixed and reverified as recorded in October 23 integration validation. One operation
marker covers the two outputs. No PDF was edited after final visual verification.

The complete staged diff, extracted PDF and local links are reviewed before commit; sensitive
content/contact/branding scan and whitespace checks pass, each artifact is under 1 MB and
no-reply Git identity is retained. Only programme task files are staged.

## Progress and publication boundary

Shared London draw two, reused unchanged; zero prior commits today. First unit is 18af1df,
which integrates October 23 L002c with all 27 provenance records verified. Original pending
artifacts remain unchanged and study date is preserved. This independent L002d validation
is the second unit. Current dispatch and original planned-slot rows reflect actual dates.
L002e adverse-fill costs is next, then L002f reproduction; no catch-up lesson is added.

Normal push and independent remote verification follow the second commit. Exact publication
and remote CI results are recorded in work/run-2026-10-24/publication-receipt.json and the
automation memory, without inventing a result in this pre-publication record. Sidiq review
remains Not yet reviewed. No input blocks synthetic continuation; Q004a/Q005b access/source
evidence is required before real data acquisition. Foundation/deferred strategy gates remain.
Daily schedule remains 08:00 Europe/London including DST; stop new research after December 31.
