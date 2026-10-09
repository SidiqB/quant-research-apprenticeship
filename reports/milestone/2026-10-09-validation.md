# Validation evidence - 9 October 2026

Task: C003a independent boundary oracle, completing the original October 8 slot on October 9.
Existing local main began clean at 57da84bdb835d85452adfec9cbdf22c8692ecaff. Read the daily prompt,
operating rules, charter, curriculum, cadence, both backlogs, roadmap, C++ plan, previous note and
validation, plus daily and weekly memories. Acquired the shared atomic run lock with the current
session recorded. No pending units or earlier London-date programme commits were found.

## Operations and research protocol

Restricted fetch failed DNS; approved fetch succeeded. Local main equalled origin/main. Authenticated
read found zero open issues and successful CI on the starting head. Existing authentication stayed
in memory; no credentials were displayed or stored. Existing no-reply Git identity was retained.
The active daily schedule remains 08:00 Europe/London, with DST and the December 31 stop unchanged.
Standing publication authority is separate from personal review, which remains Not yet reviewed.

Question: does the C++ parser agree with an independent reference at zero, its target int limit,
neighbouring values and malformed complete inputs? Hypothesis: exact values and error categories
agree, while deliberately broken boundary/transport implementations fail. The fixed evaluation
uses synthetic strings, no historical period, fitting, market data, dependency or empirical claim.
Consulted official Python integer/type documentation and Microsoft's numeric_limits reference;
links and the rationale are in the daily note. The target reports M; Python safely forms M+1.

## Implementation and checks

Added years_probe.cpp, scripts/years_boundary_oracle.py, a Make target included in cpp-check,
and experiments/years_parser with an archived host result. The C++ driver preserves all bytes
from stdin, including NUL and newlines. Its target-limit option is test plumbing, not C003b's CLI.
The independent reference uses a complete byte regex then Python integer conversion/comparison;
it does not call from_chars, convert through float or derive expectations from parser outputs.
Spelling precedes range. The target-limit report and the shared written contract remain trusted.

| Check | Observed result |
|---|---|
| Fixed differential fixture | 75 exact matches: 47 accepted, 21 spelling errors, 7 range errors |
| Target boundary | 2147483647 accepted; 2147483648 and 2147483649 rejected as range |
| Independent replay | Two direct JSON runs are byte-identical to the archived result |
| Exclusive-limit mutation | Verifier fails at 2147483647, expected accepted but observed range |
| NUL-truncating mutation | Verifier fails on three-byte 2/NUL/x, expected invalid but observed 2 |
| Full make check | 608 Python tests, 66 savings checks, 30 parser checks, four output fixtures pass |
| Quality | Ruff lint and 50 formatted files; strict mypy on 21 package files pass |
| C++ compilation | Seven executables freshly built, warning-clean Apple Clang 21 C++17 |
| Dependency consistency | pip --no-cache-dir check passes |
| PDF structure | Four pages, renderer checks all headings and page origins |
| PDF text | Exact normalized Markdown/extracted match: 10,105 non-whitespace characters |
| PDF appearance | Every final Poppler page inspected; no clipping, overlap or spill |

The probe was built by the targeted check; Makefile dependency changes caused make check to
rebuild the six existing executables. No repeated forced rebuild was needed. Production parser
and savings sources are unchanged. The first implementation checks passed; the negative-control
failures were expected and confirmed to arise from the intended mismatches, not compile failures.
Two controls do not establish mutation coverage, and no line/branch coverage was measured.

The initial PDF had a short fifth-page answer spill. Shortened repeated prose, regenerated, then
repeated exact text/geometry and visual verification. Initial Poppler rendering logged missing
font configuration/cache warnings; a temporary writable font configuration resolved them for the
final render. The PDF operation marker succeeded once before authoring. No PDF content change
followed final inspection. All final source text appears in order after Markdown/footer normalization.

Reproduce: make cpp-years-oracle; make check; .venv/bin/python scripts/years_boundary_oracle.py;
.venv/bin/python -m pip --no-cache-dir check; make note NOTE_DATE=2026-10-09.
Ignored work/2026-10-09 retains full check logs, replay JSON, mutation sources/binaries/runner,
PDF audit, extracted text and page PNGs. Only validated programme deliverables are published.

## Progress and publication

The persisted shared London-date draw is 1. Actual Git committer dates and daily/weekly memories
show zero earlier programme commits today. This coherent lesson uses one slot; no artificial split
or extra lesson is needed. Recheck the persisted draw and history before committing. Final actual
count, hash, verified remote and CI observation are recorded in run memory and the daily briefing.

Updated README, ROADMAP, BACKLOG, CPP_LEARNING_PLAN, CURRICULUM_BACKLOG, CHANGELOG and project docs.
Only independent boundary verification is complete. Next on October 10 is fractional-truncation
failure, then reproduction and consolidation; C003a/C003 remain in progress. Full CLI and later
projects remain conditional. Q004a/Q005b still gate empirical work; no input blocks synthetic study.

Final publication audit reviewed all 15 staged task files and extracted PDF text. All 57 local
Markdown links resolve; credential/contact/branding scans found no matches, every file is below
1 MB, and staged whitespace checks pass. The final Poppler log is empty. Re-reading the draw
returns 1; pre-commit London history still contains zero programme commits today. No unrelated
changes or unsupported review/empirical claims are included. Push and CI results are observed
and recorded after publication, not assumed here.
