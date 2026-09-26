# Daily validation - 26 September 2026

## Scope and findings

Q005a repairs the known Q001 named-zone fold bug. Observation now converts aware observation and
availability timestamps to UTC before ordering validation and storage; snapshot converts decision_at
before selection. The existing predicates and priority order operate on UTC instants. Original caller
datetimes are not mutated; the returned Observation is the input object, with canonical UTC fields.
This representation change is documented. Missing zone/fold evidence is not invented by conversion.

The central synthetic London 25 October fixture has two 01:30 labels, at 00:30 UTC and 01:30 UTC.
The old raw predicate admits the later publication at the earlier decision; the repaired selector
rejects it. At the later instant, a first-fold publication has waited 60 minutes, satisfying an equal
latency. A first-fold observation fails a 59-minute age limit even with a newly arrived revision.
Two fold releases are distinct; equivalent UTC/local representations of one release are duplicates.
No market dataset, estimated return, investment recommendation or measured speedup is involved.

## Verification evidence

| Check | Observed result |
|---|---|
| Checkout and lock | Clean existing main; shared atomic run lock acquired and ownership recorded |
| Remote baseline | Approved fetch: remote fab2f76; local c4c9b41 ahead by one, no divergence |
| Open issues | Authenticated read returned an empty list; credentials never printed or saved |
| Pre-fix reproduction | Original selector incorrectly admitted the later London fold |
| Pre-fix new tests | 16 failed, 6 passed; experiment test deselected until implemented |
| Targeted post-fix tests | 44 availability cases passed |
| Full suite | make check passed: 167 Python tests, 23 new cases |
| Code quality | Ruff lint passed; 27 files formatted; strict mypy passed for 15 source files |
| C++ | Warning-clean C++17 build and golden-output comparison passed |
| Dependencies | pip --no-cache-dir check passed; no new dependency |
| Independent oracle | 10,800 exact selection comparisons passed using integer-minute eligibility |
| Boundaries | Latency/age thresholds checked at equality and one microsecond either side |
| Invalid inputs | Reversed UTC instants and naive/non-datetime timestamps rejected |
| Identity | Distinct folds retained; equivalent instant duplicates rejected even before availability |
| Replay | Two subprocess experiment runs matched one another and stored JSON exactly |
| Prior evidence | Q001 result unchanged; Q003 audit still verified four pinned source files |
| PDF text | All 9,007 normalized non-whitespace source characters matched extracted text exactly |
| PDF structure | Renderer verified headings, four nonblank pages and text-origin page bounds |
| PDF appearance | All four final Poppler PNGs visually inspected: readable, no clipping or overlap |

## Protocol and limitations

The 10,800 comparisons are 4 transitions x 3 record representations x 25 decision times x 2 latencies
x 3 maximum-age policies x 3 decision representations x 2 record orders. The independent oracle uses
integer offsets from UTC epochs rather than datetime arithmetic. Transitions cover London and New York,
spring and autumn 2026. The experiment's raw legacy predicate is deliberately invalid demonstration code;
it does not implement a second production selector. All observations and values are synthetic.

The test contract assumes supplied aware timestamps encode the intended instants. UTC conversion alone
does not resolve ambiguous input strings, validate nonexistent spring-gap labels, verify source clocks,
retain original zone metadata, establish historical availability or guarantee market-data entitlement.
Q005 must define ingestion policies; no new real-data claim is permitted by this fix. Leap seconds are
outside scope. Named-zone tests rely on available IANA rules; explicit expected offsets expose mismatch.

Official Python datetime, zoneinfo and PEP 495 documentation was consulted on 26 September. References
are recorded in the experiment README and daily note. The original Q001 UTC artifact and Q003 pinned
files were not edited. No coverage percentage or CI outcome is inferred from local success. Sidiq review
status remains Not yet reviewed.

## Failures, artifact review and continuation

Restricted fetch failed DNS; approved fetch succeeded. All 16 pre-fix regression failures were resolved
by UTC normalization. The first full post-fix check passed. A temporary writable font configuration was
used for Poppler; the final render log is empty. The first PDF render had four clean pages and required
no layout correction. Its full text was audited independently of the renderer's heading check.

All 13 staged files and extracted PDF text were reviewed for credentials, contact information,
unlicensed content, unwanted branding, large assets and unsupported claims. Automated scans found
no matches; 19 local Markdown links resolve and every staged file is below 1 MB. Only Q005a changes
and progress updates are staged. The repository-local no-reply Git identity is retained.

This is the pre-commit evidence record. Actual commit, push/remote verification and any observed CI result
belong in the final briefing and automation memory. The standing publication authorization is distinct
from personal review. Preserve yesterday's local commit; do not rewrite history or bypass platform checks.
Q005 is next, Q004a remains access-blocked, and C002 stays on Wednesday 30 September. Reproduce with
make check, make fold-experiment, make experiment and make note NOTE_DATE=2026-09-26.
