# Validation evidence - 4 October 2026

Task: Q010 lagged return features. Used the existing clean local main checkout and acquired the
shared atomic .git/research-run.lock under session daily-2026-10-04. Read automation memory,
daily/operating instructions, charter, roadmap, backlog, C++ plan and previous note/evidence.
Restricted fetch failed DNS; approved fetch succeeded. Local main and origin/main started at
d3385dee05f7f361bd6ce1f22ba7016d1de5a410 with no divergence. Authenticated GitHub issue read returned
zero open issues; no credentials displayed or stored. Retained the repository-local no-reply identity.
Standing publication authorisation is separate from personal review. No unrelated edits were present.

## Research and scope

Question: can valid future additions change a past lagged return? Hypothesis: exact session windows
and per-interval as-known-at revision selection prevent this while retaining explicit missingness.
Consulted CFA Institute's 2020 GIPS linking definition, official NYSE hours/calendar and Python datetime.
An Investor.gov total-return glossary URL lacked substantive text; it was not used as evidence.
No current standards-compliance, empirical performance, licensed-data or preregistration claim.

Added frozen LaggedReturn and lagged_return, reusing Q001 selection and Q006's bounded calendar.
Link declared one-session returns with explicit asset/field, periods, skip and latency. Preserve
settings, start/end, exact required closes, selected records, missing closes and gross/fractional
results. A complete starting boundary is required; skipped sessions need calendar coverage but not
return values. Missing required observations cannot become zero, older data or another asset.
Strict counts/latency/IDs/target numeric checks and global duplicate rejection are implemented.

Inputs assert complete previous-close intervals, units, identity, action/cost/reinvestment basis and
honest availability of every underlying input. Code cannot authenticate these assertions. Q008's
entitlement arithmetic does not prove reinvestment feasibility; Q009b unresolved proceeds cannot
complete the input window. The integration test is synthetic arithmetic only. No data adapter,
membership selection, settlement, strategy, ranking or forward-target implementation was added.

## Observed checks

| Check | Result |
|---|---|
| Hand linking | +10%, -10% gives -1%; zero, losses, complete loss and gains also match |
| Future extension | Original full feature unchanged after later returns/revisions; 24 orders agree |
| Later same window | +65% after revised return becomes available; -1% with one microsecond latency |
| Wrong controls | Summing gives 0%; latest-vintage leakage gives +65% at the earlier decision |
| Missingness | Absent/delayed intervals remain None, with explicit missing timestamps |
| Independent exact ledger | 125 Fraction wealth paths agree at 1e-12 relative/absolute tolerance |
| Independent window/timing oracle | 420 comparisons pass, including prefix and future-revision invariance |
| Targeted suite | 62 tests pass; calendar, UTC, gaps, skips, invalid inputs and range checks |
| Determinism | Two subprocess runs match archived JSON bytes; Make target reproduces result |
| Full project | make check: 602 Python tests, 66 C++ checks and golden output pass |
| Code quality | Ruff lint, 47 formatted files and strict mypy on 21 package files pass |
| Fresh compilation | make -B cpp-check passes warning-clean C++17 build and all checks |
| Dependencies | pip --no-cache-dir check reports no broken requirements |
| Provenance | Original Q003 experiment still verifies all four pinned hashes and controls |
| PDF structure | Four nonblank pages, all headings present, text-origin bounds checked |
| PDF text | Exact normalized agreement of all 10,136 source-text characters |
| PDF appearance | All four final Poppler PNGs inspected; no clipping, overlap or spill pages |
| Render diagnostics | Empty final Poppler log with temporary writable font-cache configuration |

The independent timing oracle uses list indices, explicit available-time filtering and Fraction
wealth updates rather than production history or snapshot helpers to form expected results. Its
420 cases cover every eligible window of one through four periods, skips zero through two, and
zero/one-microsecond latency within the pinned calendar. Every full result equals its eligible
historical prefix and remains equal after a future revision is added to each selected interval.

## Failures and limits

The first targeted run passed 61 tests and failed an incorrect underflow expectation. Twenty factors
of 2^-53 produce 2^-1060, which remains representable; corrected the test to assert positive gross
and rounded fractional return -1. No production fix or complete-underflow test is claimed. The
first full check passed 602 tests then found two zip calls missing explicit strict arguments; fixed.
The next full check found reused loop-variable typing in mypy; renamed the variable. Final full
check passes. Initial five-page PDF had the last answer on a spill page; shortened repeated limitation
text and regenerated. Final four-page PDF passed full text and all-page visual checks.

Future-invariance applies to valid batches with unchanged originals and honest publication times.
Malformed/duplicate future input or a failed input iterator can raise. Off-grid observations cannot
fill the exact required closes. Float intermediate checks are conservative and tiny positive gross
can produce rounded -100% fractional return. Calendar coverage and source assertions limit use.
No new dependency, market data, coverage percentage, speedup or mutation-test result is claimed.

## Progress and publication

Q010 Done within the declared-return contract; Q011 Ready for October 5. Q014 remains today's separate
16:00 synthesis; C003 remains Wednesday October 7. No target dates moved. Updated README, ROADMAP,
BACKLOG, CHANGELOG and Make targets. Q004a access/sample and Q005b integration remain empirical gates;
include return interval, economic basis and underlying-input availability evidence in Q005b.
No user input needed for synthetic continuation. Sidiq review remains Not yet reviewed.

The existing daily schedule remains ACTIVE at 08:00 Europe/London including daylight-saving changes;
no scheduling mutation. Stop new research after December 31, 2026 and request the next scope.
Commit, exact remote verification and observed CI outcome are recorded in automation memory and
the user briefing after publication, without inventing a future outcome in this committed report.

Final staged audit: reviewed all 13 task files and extracted PDF text. Scans found no credential,
private-contact or unwanted-branding matches; all 36 local Markdown links resolve, every staged
file is below 1 MB and whitespace checks pass. Only task files and synthetic fixtures are staged.
No unlicensed data, unrelated edits or unsupported empirical claims are included.
