# Validation evidence - 2 October 2026

Task: Q009a historical membership intervals. Used the existing clean local main checkout; acquired
.git/research-run.lock under daily-2026-10-02. Read memory, operating/daily instructions, charter,
roadmap, backlog, C++ plan and previous note/evidence. Restricted fetch failed DNS; approved fetch
succeeded. Local main and origin/main started at beb35a44c65463ca83b29ebb395087e70817a8b7, without
divergence. Authenticated issue read returned zero open issues; credentials were not printed or saved.
The repository-local verified no-reply identity was retained. No unrelated edits were present.

## Research and scope

Question: can effective intervals recover historical members that later exit? Hypothesis: stable IDs
with inclusive entry and exclusive exit avoid filtering earlier populations by a later roster.
Consulted CRSP Research Data Products' permanent identifier page (redirected to Morningstar) and
Python's datetime documentation. Exact URLs and source implications are in the experiment README
and teaching note. Half-open boundaries and strict dates are project choices, not a vendor standard.

Added immutable MembershipInterval and MembershipHistory records with required exits (None means
asserted continuation within coverage), strict dates/IDs, declared complete coverage, canonical
record ordering, same-ID overlap rejection and sorted immutable query results. Intervals may extend
beyond coverage but must intersect it. Adjacent intervals and re-entry pass. Queries outside coverage
raise rather than return an empty set. One universe per history; no publication/revision fields.

Synthetic fixture: four IDs, five intervals, eight calendar-date labels January 1-8, 2026. These are
not exchange sessions or observed securities. OLD exits January 5, NEW enters then, RETURN leaves
and re-enters, STAY remains. On January 2 all three OLD/RETURN/STAY belong; intersection with the
January 8 roster wrongly removes OLD. No prices/returns or direction of performance bias are inferred.

## Observed checks

| Check | Evidence |
|---|---|
| Hand fixture | All eight explicit membership sets match |
| Wrong survivor control | One of three historical members incorrectly removed |
| Independent ledger | 192 exact comparisons: eight dates, 24 input orders |
| Targeted suite | 55 new tests pass |
| Boundaries | Inclusive entry/exclusive exit, adjacency, gaps and re-entry pass |
| Invalid data | Bad IDs/types/dates, reversed intervals/coverage, duplicates and overlaps reject |
| Coverage | Out-of-range dates reject, empty universe explicit, straddling intervals pass |
| Robustness | Frozen results, date extremes and future new-entry independence pass |
| Replay | Two subprocess results match archived JSON bytes |
| Whole project | make check passes: 470 Python tests; 66 C++ checks and golden output |
| Code quality | Ruff lint and 41 formatted files pass; strict mypy on 19 package files passes |
| Fresh compilation | make -B cpp-check passes C++17 with warnings treated as errors |
| Dependencies | pip --no-cache-dir check reports no broken requirements |
| Existing provenance | make manifest-experiment verifies four original Q003 hashes |
| Experiment command | make membership-experiment reproduces archived synthetic result |
| PDF text | All 8,961 normalized non-whitespace source characters match extracted text |
| PDF structure | Four nonblank pages; renderer verifies headings and text-origin bounds |
| PDF appearance | All four Poppler pages visually inspected; no clipping, overlap or spill pages |
| Render diagnostics | Empty log with temporary writable font-cache configuration |

The event-ledger oracle removes exits then applies entries; it is independent of interval containment.
Tests cover adjacent intervals for one ID, simultaneous different IDs and separated re-entry. The
later-entry test proves only that a genuinely future interval leaves an earlier query unchanged;
it does not imply immunity to retrospective revisions. No coverage percentage or mutation-test claim.
All implementation checks and the first PDF render passed. No new dependency or licensed data added.

## Limits, progress and publication

Completeness and stable identity remain unauthenticated caller assertions. Missing records cannot
be distinguished from nonmembership; unknown exits must not become assumed continuation. Effective
dates are not announcement dates: the implementation does not establish as-known-at validity. Date
mapping, market sessions, tradability, price availability, terminal events and holdings are separate.
An exit cannot delete a holding or imply zero recovery. The fixture supports no empirical claim.

Updated README, ROADMAP, BACKLOG, CHANGELOG and the Make experiment/note targets. Q009a Done;
Q009b Ready for October 3; parent Q009 incomplete. Q004a lawful data evidence and Q005b integration,
including membership provenance/vintages, remain empirical gates. C003 stays Wednesday October 7.
No input needed for synthetic continuation. Personal review remains Not yet reviewed.
Existing daily 08:00 Europe/London schedule remains ACTIVE; no schedule mutation. Stop new research
after December 31, 2026. Actual publication, remote verification and CI observations are recorded in
automation memory and the user briefing, without inventing personal review or CI outcomes.

Final staged audit: reviewed all 13 task files and extracted PDF text. Automated scans found no
secret, private-contact or unwanted-branding matches; all 32 local Markdown links resolve and all
files are below 1 MB. Staged whitespace checks pass. No unrelated changes or unlicensed data included.
