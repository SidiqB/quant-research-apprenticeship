# Validation evidence - 1 October 2026

Task: Q008 synthetic corporate-action returns. Used the existing clean local main checkout; acquired
.git/research-run.lock under daily-2026-10-01. Read automation memory, daily instructions, operating
procedure, charter, roadmap, backlog, C++ plan and previous note/evidence. After approved fetch,
main and origin/main both pointed to b6da07af6332b050b8cca93073e51352abf35443 with no divergence.
Restricted fetch initially failed DNS. Authenticated issue read returned zero open issues; credentials
were not printed or stored. Repository-local identity retains the verified account no-reply address.

## Question, primary sources and bounded change

Can explicit share and dividend units reconcile raw-price and holding-period returns? Hypothesis:
value the same opening holding at both endpoints and count its known dividend entitlement exactly once.
Consulted SEC Investor.gov Stock Split and Ex-Dividend Dates on October 1; exact URLs are in the
experiment README and teaching note. Two attempted CRSP methodology links returned 404, so their
search excerpts were not treated as inspected methodology. No vendor equivalence is claimed.

Added the package action_return function with an immutable four-component result, required action
arguments, finite/positive raw prices and share ratio, finite nonnegative entitlement and explicit
numeric range failure. Formula: (ending shares per opening share * raw closing price + cash per
opening share) / raw opening price - 1. Cash is known entitlement valued at par; no reinvestment.
All data is synthetic with no empirical sample period. Eight hand cases and three deliberately wrong
controls are recorded by a reproducible script, JSON output and README; Make exposes the experiment.
No new dependency, real market data, source acquisition, event processor or portfolio ledger.

## Observed validation

| Check | Evidence |
|---|---|
| Hand values | Eight cases pass for all four return components |
| Invalid scalar inputs | 28 cases reject None, bool, text, NaN, both infinities and negatives |
| Zero prices/ratio | Three cases rejected; zero is not inferred terminal evidence |
| Missing actions | Both omitted keyword arguments reject; no no-action defaults |
| Numeric range | Seven cases reject overflow, complete underflow and oversized integer |
| Independent ledger | 162 exact-Fraction comparisons: 54 configurations, three currency scales |
| Remaining checks | Unit conversion, immutability and two exact subprocess replays pass |
| New suite | 52 new Python tests pass |
| Whole project | make check passes: 415 Python tests and 66 C++ checks plus golden output |
| Code quality | Ruff lint and format pass on 38 files; strict mypy passes on 18 package files |
| Fresh compiler check | make -B cpp-check passes C++17 with warnings treated as errors |
| Environment | pip --no-cache-dir check reports no broken requirements |
| Prior provenance | make manifest-experiment still verifies four original hashes |
| Experiment | make corporate-action-experiment reproduces all eight totals and three wrong controls |
| PDF text | All 9,303 normalized non-whitespace source characters match extracted PDF text |
| PDF structure | Four nonblank pages; renderer verifies headings and text-origin bounds |
| PDF appearance | All four final Poppler pages visually inspected; no clipping or overlap |
| Render diagnostics | Empty log with temporary writable font-cache configuration |

Numeric oracles use 1e-12 absolute/relative tolerance, not a universal error bound. The exact-rational
ledger begins with 15 shares rather than reusing the implementation. Component reconciliation and
currency-scale invariance pass. The three intentionally wrong formula outputs are -50%, -75% and +2%
where hand totals are zero; they are detected as mismatches, not accepted as financial observations.
No code mutation test or coverage percentage is claimed. All implementation checks passed first run.

## PDF correction and material limits

The first PDF had five pages with a short source-note overflow. Shortened repeated implementation
and source text; the final four-page PDF was regenerated, exactly text-compared and visually checked
on every page. The failed CRSP link attempts remain recorded here. No layout content is silently lost.

The scalar API cannot authenticate currency, raw-price basis, event completeness, entitlement dates
or vendor provenance. Passing already adjusted prices can double-count actions. Required arguments
prevent accidental omission, not a caller's incorrect assertion. Event ordering, reinvestment,
settlement/financing, fees, taxes, FX and terminal proceeds remain outside scope. Numeric guards reject
some rescalable extreme cases and do not eliminate floating-point rounding. A receivable is not
necessarily settled cash. Missing/zero terminal prices remain unresolved, never assumed zero recovery.

Q008 is Done; Q009a is Ready for October 2, Q009b follows and C003 stays Wednesday October 7.
Updated README, ROADMAP, BACKLOG and CHANGELOG. Q004a licensed access/sample evidence and Q005b
integration remain prerequisites for empirical use. No input is needed for synthetic continuation.
Sidiq review remains Not yet reviewed; publication authorization is separate. Existing daily schedule
is ACTIVE at 08:00 Europe/London; no scheduling mutation. Stop new research after December 31, 2026.
Actual commit/push and observed CI outcomes are recorded in the automation memory and briefing.

Final staged audit: reviewed all 13 task files and extracted PDF text. Automated scans found no
secret, private-contact or unwanted-branding matches; all 30 local Markdown links resolve and all
files are below 1 MB. Staged whitespace checks pass. No unrelated changes or unlicensed data included.
