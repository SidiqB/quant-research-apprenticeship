# Validation evidence - 14 October 2026

## Run, predeclared question and sources

Worked in the existing main checkout under the shared atomic run lock. Started clean at
fc260415e65774baf7c4c04ec502e91fdbbd878b, matching origin/main after fetch. Restricted fetch
failed DNS; approved network fetch succeeded. Authenticated read found zero open issues and
successful CI for that baseline; no credentials were printed or saved. Existing repository
identity was retained. Read operating instructions, curriculum, cadence, charter, backlogs,
roadmap, C++ plan, prior note/validation and both automation memories. No parent AGENTS.md applied.

Persisted London-date draw 3; a repeated read returns the same draw. Actual committer-date
history and both memories showed zero earlier programme commits today. All four pending manifests
have integration receipts; no package is repeated. One coherent lesson is available, so one
commit is planned. No additional lesson or artificial split fills the other two slots.
The existing ACTIVE 08:00 Europe/London schedule remains unchanged; stop after December 31.

L001b asks how one affordable buy affects cash, shares and wealth when fill equals unchanged mark.
Before implementation predicted that notional moves from cash to holdings and only the fee
reduces wealth. Fixed synthetic inputs: cash 800, four shares, buy two at 50 and fee 3 in whole
arbitrary money units. No historical period, market data, fitting, strategy or empirical metric.
Consulted the SEC Investor.gov bulletin on miscellaneous broker fees, Microsoft built-in types
and Python subprocess documentation. Links and source/assumption distinctions are in the note.
A different Investor.gov fee-bulletin page failed direct retrieval; the cited miscellaneous-fees
bulletin was retrieved successfully and supplies the accounting-cost reference.

## Implementation and independent evidence

Added buy_equations.cpp and buy_expected.txt in cpp/projects/portfolio_accounting, a Decimal
reference in scripts/verify_buy_equations.py, archived JSON and provenance, and a Make target
included in make check. Constants, arithmetic and output reuse known syntax; no struct, mutable
account, reusable buy API or external input is introduced. Fixed constants satisfy positivity,
whole-unit and affordability assumptions; all fixed arithmetic lies between -3 and 1000.
The bounded int argument does not establish arbitrary-input overflow safety or money precision.

The hand-authored expected output preceded execution. Independent Decimal debits process each
share separately, then the fee once, and value holdings by repeated addition. Checks cover
cash debit 103, holdings increase 100, shares increase 2, final cash 697, holdings 300 and wealth
997. Cash plus notional plus fee restores 800; wealth plus fee restores 1000. Every output byte,
empty stderr and status 0 match twice per invocation. Two report invocations match exactly.
The compiled example and reference passed first run.

Two scratch-only mutations, omitting the fee and omitting the new shares, both compile warning-clean
and are rejected by the verifier with exit 1 and its intended reference-mismatch diagnostic.
An actual -O invocation is refused with exit 1, the explicit guard and no stdout. Mutation files
remain ignored; production source is unchanged. Source/result SHA-256 values, compiler and control
outcomes are in experiments/portfolio_accounting/validation-2026-10-14.json.

Full make check passes: 608 Python tests, Ruff lint/55 formatted files, strict mypy/21 package
files, 66 savings and 30 parser checks, 75 independent parser-boundary comparisons, four previous
golden outputs, fractional correct/wrong controls, eight readiness cases twice, three marked
snapshots twice and today's one-buy fixture twice. Eleven standard Make executables compiled
warning-clean today, including the targeted new build before the full run; readiness also built
its separate temporary executable. Apple Clang 21, C++17, -Wall -Wextra -Wpedantic -Werror.
pip consistency passes with an unwritable-cache warning only. No dependency added, coverage
percentage measured, new Python unit-test count claimed or empirical performance inferred.

## Teaching PDF, progress and publication

The final four-page PDF passes renderer heading/text-origin checks. All 9,588 normalized source
characters exactly match the extracted PDF text. Every final Poppler page was inspected visually:
no clipping, overlap, lost text or spill page. Final render log is empty. The PDF-operation marker
ran once before authoring. An optional contact-sheet helper failed because system Python lacked
Pillow; no dependency was installed, and all four original page PNGs were inspected directly.
The final PDF required no layout correction.

Progress advances only L001b. L001c's position struct is next, followed by validated buy/state
changes, independent boundaries and reproduction. L002 timing/future-price invariance, C003b,
C004/C005 and Q004a/Q005b retain their gates. Sidiq review remains Not yet reviewed. No input is
necessary for synthetic continuation; lawful source evidence remains necessary before real data.

The staged task files are reviewed for whitespace, local links, sizes, sensitive/contact content,
unwanted branding and unsupported claims before commit. Actual commit/push and exact remote/CI
outcomes are recorded in the briefing and automation memory after publication; they cannot be
asserted prospectively inside this commit. Standing publication authority is separate from review.

Post-commit review caught an overbroad README command insertion in yesterday's historical paragraph.
The new command belongs in the command list only. A separate documentation correction removes
the stray line without rewriting history. Actual planned publication is therefore two commits:
one lesson and one correction, within draw 3. No extra lesson or independent research unit is claimed.
The source, executable checks, results and verified PDF are unchanged by this correction.
