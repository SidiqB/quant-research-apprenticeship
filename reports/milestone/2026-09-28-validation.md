# Validation record - 28 September 2026

## Scope and baseline

Q006a completes the source/contract/fixture child selected by the September 27 weekly replan. The
question is whether 09:00 New York research decisions can remain valid while session dates, holidays,
early closes and UTC conversion are explicit. The policy separates decision validity, information
availability and executable times. Q006b's public session/decision implementation remains future work.

Started in the clean existing main checkout and acquired the atomic shared run lock with session
 daily-2026-09-28. Restricted fetch failed DNS; approved fetch succeeded. Local and remote were both
82284158e5026f7aa78f5b01fe1356a635723de1, zero ahead and behind. Authenticated read returned zero open
issues. Existing weekly-head CI run 36328605852 completed successfully. Credentials stayed in memory;
no secret was printed or saved. No unrelated work or pending commits were present.

## Sources and bounded evidence

Consulted official NYSE hours/holiday schedule and estimated trading-day count PDF, plus Python zoneinfo
technical documentation on September 28. Links and source sections are in data/calendar-and-decisions.md.
The NYSE page supplies no stable release ID, so source edition and consultation date are explicit.
The new JSON pins our bounded transcription, not a publisher archive. Consulted system IANA version 2026c
and New York TZif SHA-256 are metadata; the runtime database is not bundled or a new pinned dependency.

The prospective fixture covers October 29 through November 30, inclusive. It includes scheduled calendar
facts and synthetic decision cases, not realised market activity, prices or returns. NYSE cash-equity
core reference does not certify every venue or security in the intended empirical universe. No market
data, subscription, new package API or dependency was added. Existing ingestion behavior is unchanged.

## Executed checks

| Check | Observed evidence |
|---|---|
| Targeted new fixture checks | 35 passed |
| Full make check | 292 Python tests passed |
| Code quality | Ruff lint; 32 formatted files; strict mypy on 16 package source files passed |
| C++ | Fresh C++17 build with warning-as-error flags; exact golden-output comparison passed |
| Dependencies | pip --no-cache-dir check: no broken requirements |
| Coverage of dates | 33 dates, exactly once and ordered; 22 sessions; 10 weekend dates; one holiday |
| Official count comparison | 20 November sessions; naive weekdays give 21 |
| Session intervals | All 22 decisions are 30 minutes before open; 390/210-minute regular/short duration |
| Independent cases | Four hand-calculated UTC examples; explicit weekend list; prior-session examples |
| Corruption controls | All six modified copies rejected: missing/duplicate date, holiday, UTC hour, close, extra field |
| Reproduction | Two subprocess outputs match one another and archived contract-audit.json byte-for-byte |
| Prior provenance | Q003 still verifies its four pinned source files and rejects its changed-byte control |
| PDF content | Exact normalized source/text equality: 9,708 non-whitespace characters |
| PDF structure | Four nonblank pages; renderer verifies all headings and text-origin bounds |
| PDF appearance | Every final Poppler page visually inspected; no clipping, overlap or overflow |
| Poppler diagnostics | Final render log empty, using existing temporary writable font configuration |

The fixture SHA-256 is 6a6dcda36695b0ff0fe33f8eabf31c6478dec0a781b3e5a4f11d88414f271082.
Checks run via make check, make calendar-audit, make manifest-experiment and make note NOTE_DATE=2026-09-28.
No coverage percentage was measured. The audit script is outside the package's configured mypy scope;
it is exercised by fixture checks and subprocess replay. It validates these fixed rows, not arbitrary
calendar metadata/schema versions or user decision timestamps.

## Failures and corrections

The first full make check passed all tests and lint, then requested formatting of one generator
expression added after the targeted run. Ruff formatting resolved it; the complete check then passed.
The first PDF contained five pages because one final word overflowed page three onto a near-empty page.
Full-text equality passed but the four-page check correctly failed. Shortening the limitations sentence
removed that overflow. The final PDF was regenerated, text-compared, rendered and inspected on all pages.
Restricted DNS failure was resolved by approved network access, without weakening permissions.

## Review and continuation

All 14 staged files and extracted PDF text were reviewed for credentials, private contact details,
unlicensed content, large assets, unwanted branding and unsupported claims. Automated scans found no
sensitive-pattern matches; all 30 local Markdown links resolve and every staged file is below 1 MB. Only today's policy, fixture,
audit, tests, note/PDF, Make target and progress/validation records belong in this commit. Repository-local
Git identity uses the existing verified no-reply address. Historical artifacts and dates remain unchanged.

A scheduled session is not an execution guarantee or historical source-vintage proof. The first fixture
session has no known predecessor; missing coverage must fail explicitly. Daily bars and source publication
are distinct: a valid after-hours publication must not be rejected by generic ingestion. Halts, auctions,
emergency closures, all-venue calendars and the 2010-2025 empirical period remain out of scope.

Q006a is Done, Q006b Ready; Q006 remains incomplete. C002 retains Wednesday September 30. Q004a still
requires lawful access and a sample audit; Q005b still tracks provenance integration. No input is required
for Q006b. Personal review remains Not yet reviewed. Scheduling remains daily 08:00 Europe/London with
the existing daylight-saving policy; new programme research stops after December 31, 2026.

This is pre-publication evidence. The final briefing and automation memory record the actual commit,
push, remote verification and any CI result subsequently observed. No personal review or new CI success
is inferred from local validation.
