# Daily validation - 22 September 2026

## Scope and result

Q002 implements one fixed-model past-only chronological holdout with closed label intervals.
Decision-only chronology retains A-D with two overlapping labels. A one-row gap retains A-C,
still with two overlaps. Interval purging retains A,D, purges B,C, evaluates E,F,G and excludes H.
These are synthetic engineering counts, not market frequencies or performance estimates.

| Check | Observed result |
|---|---|
| Initial repository inspection | Clean local main; shared atomic run lock acquired |
| Origin synchronization | Fetch succeeded with network access; main already up to date |
| Open GitHub issues | Authenticated read returned zero open issues |
| Targeted boundary run | 23 purging unit cases passed before artifact test was added |
| Final make check | 49 tests passed, including 24 new purging/artifact cases |
| Independent interval oracle | 100 seeded fixtures; complete partition and future-row invariance checked |
| Ruff lint and formatting | Passed; 19 Python files formatted |
| Strict mypy | Passed; 13 package source files |
| Dependency consistency | pip check found no broken requirements |
| Experiment | make purging-experiment matched the hand-worked partition and overlap counts |
| Repeatability | Two temporary outputs matched each other and the durable JSON byte-for-byte |
| Existing Q001 regression | Existing release-schedule artifact test passed as part of make check |
| PDF text and geometry | Renderer verified five pages and all headings/text origins within page bounds |
| PDF full-content audit | Extracted text exactly matched source after whitespace, markup and footer normalization |
| PDF visual audit | All five Poppler-rendered pages inspected; tables, equations, footers and page breaks intact |

Environment remains the project's existing Python 3.12 virtual environment on macOS. No dependency was added.
No percentage coverage claim is made. Remote CI for this change is not yet observed in this pre-commit record;
publication and remote status are reported in the daily briefing and automation memory.

## Failures and recovery

The initial fetch in the restricted environment failed to resolve github.com. A network-authorized fetch
succeeded before edits. The GitHub CLI is unavailable. Python's HTTPS issue read failed local issuer
certificate verification; a system-curl request using its trusted certificate store succeeded. Credentials
were read through the existing Git helper, kept in memory, and never displayed or written into project files.
TLS verification was not disabled.

The first complete make check passed all tests but failed Ruff on three long string lines. Those lines were
formatted and the full suite reran successfully. The first PDF had a split table and answers on nearly empty
spill pages; shortening the introduction and explicitly separating the exercise page produced five clean pages.
The initial Poppler invocation emitted font-cache warnings. A temporary font configuration used installed
system fonts and a writable temporary cache; the final render completed with an empty diagnostic log.

## Newly observed limitation in the existing component

Q005a records a separate Q001 defect. With Europe/London timestamps, an observation published on
2026-10-25 at 01:30 fold=1 was selected at decision 01:30 fold=0, one hour earlier in UTC. Python's
same-zone datetime comparisons ignore fold. The existing availability selector therefore requires
UTC-normalized inputs pending its focused correction; the new Q002 splitter converts timestamps to UTC
and has a passing repeated-hour regression. Q005a is scheduled before timestamp ingestion, not marked done.

## Reproduction and next step

Run `make check`, `make purging-experiment`, and `make note NOTE_DATE=2026-09-22`.
PDF previews used `pdftoppm -scale-to 1400 -png` with a temporary font configuration in ignored work/.
The full teaching note is research_log/2026-09-22.md. Its review status remains Not yet reviewed.
Wednesday 23 September selects C001; Q003 is ready for the next non-C++ research slot.
