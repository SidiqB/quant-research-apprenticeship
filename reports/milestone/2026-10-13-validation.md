# Validation evidence - 13 October 2026

## Run and scope

Used existing local main and acquired the shared atomic run lock. Main started clean at c8c925e,
matched origin after fetch, and had successful baseline CI and zero open issues. Restricted fetch
failed DNS; approved network retry succeeded. Existing authenticated read displayed no credentials.
Read operating/curriculum/cadence instructions, backlogs, charter, previous evidence and both memories.
No applicable parent AGENTS.md. The persisted London-date draw is 3; history and memories showed no
previous programme commits on this date. Unchanged ACTIVE daily schedule is 08:00 Europe/London;
programme ends after December 31, 2026. Personal review remains Not yet reviewed.

First independent unit: integrated October 12 C003a consolidation after all eight input and seven
artifact hashes matched. Commit 3b26d43 preserves its study date, original result and production
functions; validation is in 2026-10-12-validation.md. Current readiness replay agrees with the original
after the source path moved. C003a complete; C003b and the parent C003 are not complete.

Second unit and sole new lesson: L001a cash, position and marked wealth. Before implementation,
predicted W=C+q*p and unchanged cash across three marks. Inputs are a synthetic initial cash 800,
position four shares and alternative marks 50, 55, 45 in whole arbitrary money units per share.
No market data, historical period, trade, fitting or empirical-performance metric is present.
Consulted Investor.gov NAV, Microsoft built-in types and official Python subprocess documentation;
source links and the distinctions between published facts and fixture assumptions are in the note.

## Implementation and checks

marked_wealth.cpp reuses const int declarations, multiplication, addition and output. No external
input or reusable interface is offered. All fixed nonnegative constants and intermediates fit the
minimum C++ int range; fractional money, arbitrary-input validation and overflow policy are deferred
to their own lessons. expected.txt is hand-authored before execution. The independent verifier uses
Decimal addition of four marked shares, matches that fixture and compares stdout/stderr/status twice.

Observed wealth 1000/1020/980 and holdings 200/220/180 match, with cash 800 in every row. Changes +20
and -20 reconcile against the initial snapshot. Two full verifier invocations produce byte-identical
JSON. The C++17 build uses -Wall -Wextra -Wpedantic -Werror and Apple Clang 21 with no diagnostics.
A scratch mutation replacing each shares*mark with shares+mark also compiles warning-clean, but is
rejected with verifier exit 1 and the intended reference-mismatch diagnostic. The production source
is untouched by that mutation. Actual -O invocation exits 1 with the guard and empty stdout.
Source/result hashes and compiler are in experiments/portfolio_accounting/validation-2026-10-13.json.

Full make check passed: 608 Python tests, Ruff lint and 54 formatted files, strict mypy/21 package
files, 66 savings and 30 parser checks, 75 independent boundary comparisons, four existing golden
outputs, fractional correct/wrong controls, eight readiness cases twice and three wealth snapshots
twice. Ten standard Make executables compiled today across the two units; the readiness recipe
freshly compiled a separate temporary executable. pip consistency passed, with an unwritable-cache
warning only. No new dependencies, line/branch coverage percentage or extra Python test count claimed.
Today's new executable and verifier passed on their first run; deliberate negative controls failed
as intended. The prior unit's preformat lint complaint is recorded in its validation.

## PDF and publication audit

Today's PDF has four final pages and exactly matches all 8,268 normalized source characters.
Renderer headings/text origins pass; all four final Poppler pages were visually inspected with no
clipping, overlap or missing content. Initial rendering put three answers on a short spill page;
a deliberate section break balances the final four pages. All final checks were repeated; final
Poppler log is empty. The PDF-operation marker ran once before authoring today's two PDF outputs.
Yesterday's integrated four-page PDF has separate full-text and visual verification evidence.

Progress advances only L001a. Next L001b derives one buy and explicit fee, then the later struct,
validated state update, independent boundary and reproduction steps. L002 timing remains separate;
trend remains conditional. Q004a/Q005b and C003b/C004/C005 prerequisites remain. No necessary input
blocks synthetic continuation; licensed access evidence is still needed before real data.

Two meaningful units use two of the three slots. No artificial third unit or extra lesson is made.
Audit task files for whitespace, local links, size, sensitive/contact content and unwanted branding
before committing. Push and exact remote/CI outcomes are recorded in the run briefing and memory,
since the commit cannot truthfully contain its own completed remote outcome in advance.
