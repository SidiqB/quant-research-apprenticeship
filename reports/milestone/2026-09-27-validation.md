# Daily validation - 27 September 2026

## Scope and findings

Q005 adds strict in-memory batch ingestion to the UTC availability selector. One declared IANA source
zone applies to explicit-offset timestamp strings in both fields of all rows. A UTC round trip must
reproduce wall fields and offset. This rejects gaps and inconsistent zones while accepting either
explicit valid fold offset. Source claims are not authenticated. Direct Observation construction is
unchanged and still assumes upstream validation; this adapter is not a global ingestion enforcement layer.

Mappings have exactly five fields, validated identifiers and finite built-in numeric values. Duplicates
use canonical UTC version keys and fail whether values agree or conflict. Revisions remain distinct.
The complete immutable tuple returns in input order only on success; generators are consumed through
failure without external rollback. Raw source/zone metadata must be retained upstream. No market data,
subscription, empirical alpha estimate or new runtime dependency is involved.

## Verification evidence

| Check | Observed result |
|---|---|
| Checkout and lock | Existing clean main; shared atomic lock acquired with session daily-2026-09-27 |
| Remote baseline | Approved fetch: local 362d52e, remote fab2f76; two ahead, zero behind |
| Open issues | Authenticated read returned no open issues; credentials never printed or stored |
| Targeted initial tests | 89 passed; experiment test deselected until artifact existed |
| Complete test suite | 257 passed, including 90 new ingestion cases |
| Quality | Ruff lint passed; 30 files formatted; strict mypy passed on 16 source files |
| C++ | Warning-clean C++17 build and exact golden-output comparison passed |
| Dependencies | pip --no-cache-dir check passed; no new dependency |
| Hand-computed fold instants | London, New York and 30-minute Lord Howe conversions match explicit answers |
| Invalid inputs | Schema, identifiers, types, finite range, format, offsets, gaps and order rejected |
| Batch behavior | Empty/generator input, no mutation, duplicate aliases and no partial return checked |
| Permutations | All 24 orders of four valid rows preserve input order and select revision value 2 |
| Experiment | Two valid versions; decision values 1 then 2; all eight invalid batches rejected |
| Replay | Two subprocess outputs match one another and archived JSON byte-for-byte |
| Prior artifacts | Q003 verifies its four pinned source files; original Q001/Q003 outputs unchanged |
| PDF text | All 9,451 normalized non-whitespace source characters exactly match extracted text |
| PDF structure | Four nonblank pages; renderer heading and text-origin bounds checks pass |
| PDF appearance | All four final Poppler PNGs visually inspected; readable with no clipping or overlap |

## Failures and limitations

Initial restricted fetch failed DNS; approved fetch succeeded. Initial mypy check did not narrow the
runtime-validated numeric object, resolved by an explicit cast after the exact-type guard. The first
full make check passed all tests then found two overlong experiment source lines. Wrapping them resolved
the lint failures; the subsequent complete make check passed. No failures are suppressed.

The first PDF had four correctly laid-out pages and needed no layout correction. Poppler used a temporary
writable font configuration; its render log is empty. Full-text comparison is independent of the renderer's
heading check. No code coverage percentage, CI success or personal review is inferred from these checks.

Clock consistency does not establish entitlement, source authenticity, vintages, exchange sessions or
permanent security identifiers. Input grammar is narrower than Python ISO parsing. Numeric conversion
is floating point, not exact-decimal accounting. One declared representation per batch is intentional:
London summer UTC-encoded records belong in a UTC batch, not a London-local batch. Duplicate checks are
batch-local; combined batches retain the selector's check. Timezone rules come from the available system
IANA database; the tested offsets are explicit but the database is not newly pinned. All data is synthetic.
Primary documentation consulted: PEP 495 and official Python zoneinfo/datetime pages, linked in the note
and experiment README. Q006 handles the separate calendar/decision-time contract.

## Artifact review and continuation

The complete 13-file staged change and extracted PDF text were reviewed for secrets, contact data,
unlicensed content, unwanted branding, large files and unsupported claims. Automated scans found no
matches; all staged files are below 1 MB and all local Markdown links checked resolve. Only today's
adapter, tests, experiment, note/PDF, Make target and progress records are included. Existing unpublished
commits are preserved. The repository-local verified no-reply Git identity remains in use.

This is pre-commit evidence. Actual commit/push verification and any observed CI result belong in the
final briefing and automation memory. Standing publication authorization is separate from personal review,
which remains Not yet reviewed. Q006 is next; Q007 belongs to this afternoon's synthesis; C002 remains
Wednesday 30 September. Q004a needs lawful access/sample evidence before any real acquisition. Programme
end remains 31 December 2026. No scheduling changes are required by this implementation.
