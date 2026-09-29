# Validation evidence - 29 September 2026

Task: Q006b bounded session lookup and decision validation. Existing local main checkout; atomic
.git/research-run.lock acquired under daily-2026-09-29. Read operating instructions, charter, roadmap,
backlog, C++ plan, previous note/evidence and automation memory. The initial clean main was cb610d6,
one commit ahead of origin/main 8228415 without divergence. Preserved that pending commit. Restricted
fetch failed DNS; approved network fetch succeeded. Authenticated GitHub issue read returned zero open
issues. No credentials were displayed or stored. No personal review or publication status was inferred.

## Research and scope

Consulted official NYSE hours/holiday schedule and Python datetime/zoneinfo documentation on September 29.
Question: can bounded validation preserve valid pre-open decisions while rejecting closed dates, wrong
clocks and unknown history? The data are the unchanged prospective Q006a calendar plus synthetic
clock inputs. The implementation is intentionally specific to the reviewed 33-date fixture. Exact bytes
must match its pinned SHA-256; installed timezone rules must agree with all explicit reference instants.
This verifies identity/consistency, not exchange authenticity, historical vintages or actual trading.

## Observed checks

| Check | Evidence |
|---|---|
| Targeted suite | 71 new cases pass |
| Full suite | make check: 363 tests pass |
| Lint and format | Ruff passes; 35 files already formatted |
| Types | Strict mypy passes on 17 package files |
| C++ | Fresh C++17 build with warnings as errors; golden output matches |
| Dependencies | pip --no-cache-dir check: no broken requirements |
| Decision/core separation | All 22 intended pre-open decisions accepted and outside core time |
| Core boundary checks | 132 exact/adjacent-microsecond checks pass across 22 sessions |
| Invalid experiment inputs | All nine rejected: closure, clock, naive, fractional and coverage cases |
| Closed dates | All 11 hand-listed holiday/weekend dates return no session and reject decisions |
| Independent examples | Four hand UTC cases, four predecessor cases and explicit 20-session date list |
| History limits | Nov 25 has only 19 prior sessions; Nov 27/30 supply complete requested 20-session windows |
| Representation controls | New York, UTC, Tokyo and +14:00 equivalents; UTC/local date-boundary checks |
| Input/integrity controls | Invalid types/counts, immutable outputs, three changed-byte inputs and wrong zone rules |
| Ingestion independence | A holiday publication passes the existing generic observation adapter |
| Reproduction | Two subprocess outputs match archived decision-validation.json bytes |
| Prior evidence | Q006a audit unchanged; Q003 still verifies four original source hashes |
| PDF text | Exact normalized Markdown/extracted-text equality: 9,955 non-whitespace characters |
| PDF structure | Four nonblank pages; renderer checks headings and text-origin bounds |
| PDF appearance | Every final Poppler page inspected; no clipping, overlap or overflow |
| Poppler diagnostics | Final render log empty with temporary writable font configuration |

Commands: make check; make calendar-experiment calendar-audit manifest-experiment;
.venv/bin/python -m pip --no-cache-dir check; make note NOTE_DATE=2026-09-29.
The package API is within strict mypy scope; the experiment is exercised by subprocess tests.
No coverage percentage or performance improvement was measured. No dependencies were added.

## Failures and corrections

The initial targeted tests and mypy passed. Ruff found three diagnostic string lines beyond 100
characters; wrapped the literals, preserving their exact output. The subsequent full check passed.
The first PDF had five pages, including a short overflow continuation of the limitations paragraph.
Moved that paragraph to available space on the sources page. The final four-page PDF was regenerated,
full-text compared, rendered and visually checked on every page. No content was silently removed.
Restricted DNS required approved network access; permission settings were not weakened.

## Review and continuation

The task includes package logic/tests, deterministic experiment/result, Make target, usage/contract
updates, note/PDF and progress/validation records. All 14 staged files and extracted PDF text were
reviewed for secrets, private contact data, unlicensed content, large assets, unwanted branding and
unsupported claims. Automated scans found no sensitive/contact/branding matches; all 37 local Markdown
links resolve and every staged file is below 1 MB. Repository-local Git identity retains the verified
account no-reply address. Historical artifacts and unrelated files remain unchanged.

Q006b/Q006 are Done within bounded acceptance criteria. C002 remains September 30; Q008 is Ready for
October 1. Q004a still needs lawful access and sample evidence; Q005b still gates provenance integration.
No input is needed to continue independent synthetic mechanics. Sidiq review is Not yet reviewed.
Daily schedule remains active at 08:00 Europe/London; no scheduling changes. Stop new research after
December 31, 2026. No venue-general calendar, fill, observation availability or alpha claim is made.

This is pre-publication evidence. The final briefing and automation memory record actual commit/push,
remote verification and any subsequently observed CI result. Local checks do not imply remote CI success.
