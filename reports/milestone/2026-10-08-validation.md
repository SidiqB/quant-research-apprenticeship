# Validation evidence - 8 October 2026

Task: C003a parser implementation, completing the original October 7 slot after the prerequisite
recovery. Existing local main began clean at c77c6af65439393abd0afd26d1dfba832fdd87ae. Read the
operating/daily rules, charter, curriculum, cadence, backlogs, roadmap, C++ plan, previous note and
validation, and daily/weekly memories. Acquired the shared atomic lock for this run. No pending units.

## Operational evidence

Restricted fetch failed DNS; approved fetch succeeded. Local main matched origin/main without a
merge or checkout change. Authenticated read returned zero open issues and successful baseline CI.
Credentials were neither displayed nor persisted; existing local no-reply identity was retained.
Publication is authorised separately from Sidiq's personal review, which stays Not yet reviewed.
Existing daily schedule remains ACTIVE at 08:00 Europe/London; no schedule change was needed.
Stop new research after December 31 and request next scope. Q004a/Q005b empirical gates remain.

## Question and implementation

Question: can one function enforce the complete whole-year text contract before returning an int?
Hypothesis: grammar validation followed by checked decimal conversion and complete consumption
prevents silently accepting malformed requests. Consulted Microsoft's official from_chars and
exception references, linked in the daily note. Synthetic inputs only; no market data or dependency.

Added years.hpp/cpp, test_years.cpp, parse_years_demo.cpp and hand-authored expected output. Make
includes the tests and demo, including header/source dependencies. Empty/non-digit strings throw
invalid_argument; digit-only overflow throws out_of_range. Grammar has precedence over range.
The complete std::string length is scanned; embedded NUL and UTF-8 digit encodings fail. Leading
zeros work. ASCII-compatible execution targets are assumed. No transport/input-size protection,
performance claim or exhaustive coverage is asserted. Resource failures can raise other exceptions.

C002 is unchanged. The fixed example parses 002 to 2, then produces 1102.50 from 1000 at 5%; 2.5
raises before a year value returns. No CLI arguments are parsed. Parser success does not guarantee
finite financial output. Model assumptions, costs and limitations are explicit in the teaching note.

## Checks and results

| Check | Observed result |
|---|---|
| Parser harness | 30 pass: 8 accepted values, 21 required errors, 1 hand balance |
| Full make check | 608 Python tests, 66 prior C++ checks, 30 parser checks, four output comparisons pass |
| Quality checks | Ruff lint; 49 formatted files; strict mypy on 21 package files pass |
| make -B cpp-check | Six executables compile warning-clean under C++17; all checks pass |
| pip --no-cache-dir check | No broken requirements |
| Fixed parser demonstration | Two runs equal each other and the full expected bytes |
| Independent financial check | Python Decimal credits 50 then 52.50; balances 1050 then 1102.50 |
| Final PDF structure | Four pages; renderer checks headings and page origins |
| Final PDF text | Exact normalized source match: 10,508 non-whitespace characters |
| Final PDF visual check | All four 1400-pixel Poppler pages inspected; no layout defects |
| Render log | Empty with existing writable font-cache configuration |

Implementation checks passed first run. The initial PDF spilled the sources onto a short fifth
page. Shortened repeated prose, regenerated, repeated text/geometry verification and visually
inspected all four final pages. No PDF change followed final inspection. The PDF operation marker
succeeded once before authoring. No hidden test failure or branch-coverage percentage is claimed.
The post-digit-scan defensive conversion guard has no separately exercised failure path. The
independent Python boundary oracle remains the next lesson; today's Python check is financial only.

Reproduce with make cpp-parse-years; make check; make -B cpp-check;
.venv/bin/python -m pip --no-cache-dir check; make note NOTE_DATE=2026-10-08.
Ignored work/2026-10-08 retains logs, two output replays, Decimal results, PDF audit, extracted text
and PNGs. The Decimal check starts at Decimal('1000') and adds balance*Decimal('0.05') twice;
it does not call compound_balance. The PDF audit normalizes Markdown decoration and whitespace,
removes per-page footers and compares all remaining source/extracted characters in order.

## Progress and publication cadence

While locked, scripts/daily_commit_budget.py persisted October 8 London-date draw 3. Actual Git
committer dates and both memories show zero earlier commits today. One independently meaningful
unit is ready, with no saved pending work to integrate. Plan one coherent commit; unused allowance
is not a reason to split the lesson or add workload. Recheck history before committing. Final actual
count, hash, verified remote and CI outcome are recorded in automation memory and the briefing.

Updated README, ROADMAP, BACKLOG, CURRICULUM_BACKLOG, CPP_LEARNING_PLAN, CHANGELOG and savings docs.
Only the implementation slot is complete. Boundary oracle is next on October 9, followed by
failure, reproduction and consolidation in order. C003a/C003 remain in progress; C003b and ledger
readiness remain conditional. No user input is required for the next synthetic lesson.

Final publication audit reviewed all 17 staged task files and the extracted PDF text. All 54 local
Markdown links resolve; scans found no sensitive/contact/branding matches, each file is below 1 MB,
and staged whitespace checks pass. No unrelated changes or unsupported review/empirical claims
are included. Re-reading the persisted draw returned 3; pre-commit London history still had zero
programme commits today. Push/CI outcomes are recorded after publication, not assumed here.
