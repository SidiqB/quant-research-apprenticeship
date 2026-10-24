# Validation - 23 October 2026

L002c implements one bounded C++ delayed-order trace after L002a/b. Question/hypothesis,
fixed synthetic data, protocol, primary sources, units and limitations are in the teaching note.
No new strategy family, real market data, empirical performance or personal mastery is claimed.

The C++ fragment reuses unchanged validated_buy.cpp through a temporary combined translation
unit. Eight hand cases agree with the independent per-share Decimal contract reference:
three filled, one unresolved, two model-rejected and two no-order. Fifteen invalid integer
traces reject with invalid_trace/request -1, unchanged snapshots/caller and zero fee. All
caller accounts remain unchanged because the initial account is passed by value. The caller
must explicitly adopt returned final state after inspecting validity and status.

Two fresh warning-clean C++17 builds with UBSan and no recovery, each executed twice, give
identical output and result JSON. Three separate scratch mutants compile, then fail the intended
trace mismatch: old-price debit, fee on missingness and equal-resolution allowance. Actual -O
execution is refused. Ruff lint/format pass after routine formatting; correct runtime checks
passed on first execution. Compiler is Apple Clang 21.0.0. No installed build binary is reused.
This is a typed integer interface, not a text parser; raw Boolean/fractional conversions need
an upstream gate. No persistent order ID, retry lifecycle or general future-price invariance
proof is provided. L002d remains next, including a deliberately leaking control.

Tracked make check passed for each integration: 608 Python tests, all C++ checks, Ruff
(60 then 61 files), strict mypy/21 source files. New timeline/contract Make checks pass;
pip consistency passes with no added dependency. Pending L002c is checked separately and is
not yet in tracked Make checks or remote CI. Staged audits covered 19 files and 62 local links
per commit, including extracted PDF text, sensitive/contact/branding scans, size and whitespace.

Three final PDFs have four pages each: integrated October20 has 9606 normalized characters;
integrated October22 has 10455; today's pending note has 11648. Every final source/text comparison
is exact; renderer headings/page origins pass. Every final Poppler page visually inspected,
with no clipping, overlapping elements or stranded headings; all final render logs empty.
Today's first draft had six pages including table/answer spills; second had five with one
stranded table row. Those split tables also made the strict text audit fail on repeated headers.
Tightened prose and table labels, then reran all checks on the final four-page PDF. No changes
after final visual inspection. One artifact-operation marker covered the three outputs.

Shared draw two; actual commits two: 4a30e71 integrates L002a and c84d743 integrates L002b.
Both pushed normally. Independent ls-remote matches c84d7435a176037e60e89b5016060b3663e1428d;
CI run 39932417055 completed successfully for that exact SHA. No publication blocker remains.
This new lesson is pending only because the shared allowance is exhausted. All original pending
L002a/b artifacts remain unchanged; added receipts record integration separately.

Progress is saved locally in progress.json and integration-manifest.json; later integration
must preserve the actual study date, validate provenance, adapt verifier paths and add a Make
check, repeat fresh builds and controls, regenerate/verify the PDF, then publish within allowance.
Personal review remains Not yet reviewed. No input blocks synthetic continuation; Q004a/Q005b
still require lawful data-access/source evidence before real acquisition. L002d-f, C003b/C004/C005
and Q011-13 remain gates; trend and later windows conditional. Stop new research after December31.
