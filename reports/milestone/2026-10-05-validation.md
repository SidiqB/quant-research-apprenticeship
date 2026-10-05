# Validation evidence - 5 October 2026

Task: C003a intuition, text versus whole-year values. Existing local main started clean at
90526983398f3ec564229c6499f80f5ae0e1c253. Acquired the shared atomic research lock with session
daily-2026-10-05. Read daily and weekly memories, operating/daily instructions, charter, curriculum,
backlogs, C++ plan, latest daily/weekly notes and validation. No unrelated edits were present.
Restricted fetch failed DNS; approved fetch succeeded and main equalled origin/main. Authenticated
GitHub read found zero open issues; baseline exact-head CI run 37212974066 succeeded. No credentials
were displayed or persisted. Repository-local identity retains the account no-reply address.

## Question and bounded improvement

Can a function with an int years parameter detect a fraction lost before the call? Hypothesis:
it cannot; original text must be checked before constructing the integer. Microsoft primary
documentation on standard conversions and string literals was consulted on October 5 and is linked
in the teaching note and worksheet. No empirical finance or language-standard compliance claim.

Added text_vs_years.cpp, text_vs_years_expected.txt and text_vs_years.md beneath the existing savings
project. One safe fixed conversion, static_cast<int>(2.5), produces 2, then C002 produces 1102.50.
Original text and numeric literal are separately written, not parsed. The five input classifications
are hand decisions, not automated parser tests. C003a remains incomplete beyond this intuition slot.
C003b full CLI, future parser grammar/range and subsequent curriculum work are not brought forward.
The savings function and all previous evidence remain unchanged. No new dependency or market data.

## Observed checks

| Check | Result |
|---|---|
| New demonstration | Five exact output lines match the hand-authored fixture |
| Repeatability | Two fresh executable invocations match expected bytes |
| Independent arithmetic | Decimal updates 1000 to 1050 to 1102.50 without the C++ function |
| make check | 608 Python tests, 66 C++ checks and both demonstration comparisons pass |
| Quality | Ruff lint, 49 formatted files and strict mypy on 21 package files pass |
| make -B cpp-check | Three executables rebuild warning-clean under C++17; all checks pass |
| Dependencies | pip --no-cache-dir check passes |
| PDF structure | Four pages, headings present and text origins inside page bounds |
| PDF text | Exact normalized source/extraction match: 9,853 non-whitespace characters |
| PDF appearance | All four 1400-pixel Poppler PNGs visually inspected; no defects |
| Render diagnostics | Empty Poppler log using the existing writable font-cache configuration |

The independent verification used Decimal('1000'), adding wealth*Decimal('0.05') twice, and compared
1102.50 to the expected display. The new Make comparison runs in the existing CI make check command.
No new Python test count, parser rejection coverage, general mutation score, performance result or
personal mastery is claimed. The implementation checks and first PDF render passed. The publication link audit caught an extra parent traversal
in the worksheet note link after an earlier doubled slash was removed; corrected and rechecked.
No validation failure is hidden.

Reproduce with make cpp-text-years, make check, make -B cpp-check and
.venv/bin/python -m pip --no-cache-dir check. Render with make note NOTE_DATE=2026-10-05.
Ignored work/2026-10-05 holds output replays, the text comparator, extracted PDF text and page PNGs.
The PDF operation marker succeeded before authoring; the final PDF received both text and visual review.

## Cadence, progress and publication

While holding the lock, scripts/daily_commit_budget.py persisted budget 1 for 2026-10-05 in
Europe/London. Actual Git committer timestamps converted to London dates showed zero programme
commits today before this unit; both automation memories confirmed no earlier October 5 run.
There was no pending integration manifest. One coherent lesson/evidence commit is intended, with
no artificial split or added lesson. Recheck history immediately before committing. Actual hash,
count, push verification and CI observation are recorded in automation memory and the briefing.

Updated README, ROADMAP, BACKLOG, CURRICULUM_BACKLOG, CPP_LEARNING_PLAN, CHANGELOG and project README.
Only October 5's intuition slot is Done; C003/C003a remain in progress. Tomorrow defines grammar/range.
The Q004a entitlement/sample and Q005b integration gates remain; no input is needed for synthetic
continuation. Sidiq review remains Not yet reviewed. Standing publication authorisation is separate.
The existing ACTIVE daily schedule remains 08:00 Europe/London with daylight-saving changes. New
programme research stops after December 31, 2026; request the next scope then. No schedule mutation.

Final publication audit reviewed all 14 task files and extracted PDF text. All 51 local Markdown
links resolve after the worksheet-link correction. Credential/private-contact/branding scans found
no matches; every staged file is below 1 MB and whitespace checks pass. No unlicensed data,
unrelated changes or unsupported empirical/review claims are included.
