# Validation evidence - 3 October 2026

Task: Q009b terminal-event evidence separate from membership. Used the existing clean local main
checkout; acquired .git/research-run.lock with session daily-2026-10-03. Read automation memory,
operating/daily instructions, charter, roadmap, backlog, C++ plan and previous note/evidence.
Restricted fetch failed DNS; approved fetch succeeded. Local main and origin/main started at
a5f9f861bb2ec94bca438e752c42e094474913b3, without divergence. Authenticated issue read returned zero
open issues, without displaying or storing credentials. Retained the repository-local no-reply identity.
No unrelated edits were present. Standing publication authority is separate from personal review.

## Research, implementation and scope

Question: can terminal valuation preserve holdings while distinguishing missing proceeds from explicit
zero? Hypothesis: separate evidence states prevent a membership exit from erasing holdings or inventing
a return, and complete cash proceeds permit hand-checked arithmetic. Consulted official CRSP payment
categories/aggregate delisting flags and Python dataclasses documentation. The experiment README and
teaching note cite exact URLs and distinguish our contract from vendor conventions.

Added HeldPosition, TerminalEvidence, TerminalValuation and value_terminal. Complete proceeds are
required explicitly; None means unknown, zero means supported complete zero. Result retains both
inputs, including unresolved holdings. Missing event evidence does not prove a terminal event occurred.
Dates are strict date-only; event must follow reference date and match identity even if proceeds are
missing. Input validation rejects invalid IDs/locators, booleans, unsupported numbers, negatives,
nonfinite inputs and unsupported numeric range. Ordinary frozen-field mutation is rejected.

Scope is positive long shares, positive reference price, complete nonnegative cash per reference
share, one currency/basis and no intervening split/dividend/trade. Entitlement is valued at par, not
settled cash. The caller asserts completeness and evidence authenticity; syntax cannot verify them.
Stock/property and incomplete payments remain unsupported/unknown. This is retrospective arithmetic,
not as-known-at selection, a vendor adapter, a settlement engine or a portfolio aggregate.

## Observed evidence

| Check | Result |
|---|---|
| Six hand states | Missing event, missing proceeds and four complete cash cases match |
| Numeric fixture | Reference 200; terminal values unknown, unknown, 0, 50, 200, 250 |
| Numeric returns | Unknown, unknown, -1, -0.75, 0 and +0.25 |
| Wrong exit filter | Deletes OLD incorrectly; correct result retains its 10-share input |
| Wrong zero imputation | Produces -100% where the correct return remains unknown |
| Independent exact accounting | 108 Fraction debit/credit-ledger comparisons agree |
| Targeted checks | 70 new tests pass, including dates/IDs/missingness/range and immutability |
| Replay | Two subprocess runs match archived JSON bytes; Make target reproduces result |
| Whole project | make check: 540 Python tests; 66 C++ checks and golden output pass |
| Code quality | Ruff lint/44 formatted files pass; strict mypy passes on 20 source files |
| Fresh compilation | make -B cpp-check passes warning-clean C++17 build and all checks |
| Dependencies | pip --no-cache-dir check reports no broken requirements |
| Provenance regression | Four original Q003 hashes and audit controls pass |
| PDF structure | Four nonblank pages; renderer checks headings and text-origin bounds |
| PDF text | Exact normalized agreement of all 9,536 source-text characters |
| PDF appearance | All four Poppler pages visually inspected; no clipping, overlap or spill pages |
| Render diagnostics | Empty log using a temporary writable font-cache configuration |

The exact ledger spans three quantities (including fractional shares), three prices, four cash amounts
and three currency scales. It computes profit from exact credit minus debit, then profit/debit. Numeric
tolerance is relative/absolute 1e-12; statuses and missing values compare exactly. The membership test
shows eligibility ending before the event while the position remains present. No aggregation result is
claimed. A known partial recovery means complete proceeds below reference value, not partial evidence.

The first full check found one 101-character experiment line after all tests passed. Wrapped the line
and reran the full check successfully; no failure was suppressed. First PDF render passed all text and
visual checks. No coverage percentage or mutation-test claim is made. No dependency or market data added.

## Progress and limitations

Q009b and bounded Q009 are Done; Q010 is Ready for October 4. Q014 remains the separate October 4
16:00 synthesis, C003 remains October 7. Updated README, ROADMAP, BACKLOG, CHANGELOG and Make targets.
No date changes. Personal review remains Not yet reviewed. No user input needed for synthetic continuation.
Licensed access/sample evidence and Q005b provenance integration remain empirical prerequisites; carry
identity, complete cash units, availability and vintages into that integration before real-data use.

No event time, announcement time, vintage, settlement date, discounting, credit risk, costs or tax is
modelled. Unknown positions must not be omitted from aggregates. Floats are approximate; intermediate
range limitations and tiny positive recoveries rounding to -1 in return subtraction are documented.
No empirical performance, investment recommendation or personal mastery is claimed.

The existing daily schedule remains ACTIVE at 08:00 Europe/London, including daylight-saving changes;
no scheduling mutation. Stop new research after December 31, 2026. Publication, exact remote verification
and observed CI outcome are recorded in automation memory and the user briefing after the commit.

Final staged audit: reviewed all 13 task files and extracted PDF text. Automated scans found no
credential, private-contact or unwanted-branding matches; all 34 local Markdown links resolve and
all files are below 1 MB. Staged whitespace checks pass. Only task files and synthetic fixtures are
included; no unlicensed dataset or unrelated edit is staged. The final full check also passes after
making the deliberately wrong zero-imputation control an explicit calculation in the experiment.
