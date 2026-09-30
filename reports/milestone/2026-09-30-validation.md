# Validation evidence - 30 September 2026

Task: C002 reusable C++ savings function. Worked in the existing clean main checkout and acquired
.git/research-run.lock under daily-2026-09-30. Read the daily procedure, operating instructions,
charter, roadmap, backlog, C++ plan, previous note/evidence and automation memory. Initial main and
origin/main both pointed to 3e8140834b6ad04d6a13fa8875a39dde5c89473b after fetch. Restricted DNS failed;
approved fetch succeeded. Authenticated GitHub issue read returned zero open issues. No credentials
were displayed or stored. The local Git identity retains the account's no-reply address.

## Research and implementation

Question: can one reusable function reproduce annual compound growth and reject invalid inputs?
Consulted official Microsoft C++ functions, pow and isfinite references on September 30; exact URLs
are in the teaching note and project README. All inputs are synthetic and have no empirical period.
Contract: finite nonnegative principal/rate; nonnegative whole-year int; effective annual fractional
rate; reinvestment; no intermediate rounding, cash flows, taxes or fees. Invalid inputs raise before
zero shortcuts. Nonfinite computed growth factor or balance raises an overflow error. Explicitly
exclude negative rates and document both intermediate-factor overflow and implicit integer conversion.

Added savings.hpp/savings.cpp and a standalone test harness. The original main now calls the function
and appends a multi-year comparison; its original five output lines remain unchanged. Make tracks the
shared header and implementation for both executables. No new dependency or empirical claim.

## Observed checks

| Check | Evidence |
|---|---|
| Function values and zero cases | 14 pass, including exact hand values and extreme valid zero shortcuts |
| Invalid inputs | 19 pass: negative, NaN, both infinities, negative years and validation before shortcuts |
| Overflow | Three pass: balance, factor and conservative intermediate-factor limitation |
| Independent recurrence | 30 yearly balances match within declared tolerance |
| C++ total | 66 checks pass, plus exact demonstration output comparison |
| Negative control | Temporary simple-interest replacement fails with interest-on-interest error |
| Reproduction | Two separate demo subprocess runs match expected.txt bytes |
| Full suite | make check: 363 Python tests pass; no new Python tests needed |
| Quality | Ruff lint passes; 35 files formatted; strict mypy passes on 17 source files |
| Compiler | Apple Clang 21.0.0; C++17; Wall/Wextra/Wpedantic/Werror; fresh build passes |
| Dependencies | pip --no-cache-dir check reports no broken requirements |
| Prior integrity | Q003 still verifies all four original source hashes |
| PDF text | Exact normalized source/extracted-text match: 9,729 non-whitespace characters |
| PDF structure | Four nonblank pages; all headings and text-origin bounds checked by renderer |
| PDF appearance | Every final Poppler page inspected; no clipping, overlap or layout defect |
| Render diagnostics | Empty log using a temporary writable font-cache configuration |

Commands: make -B cpp-check; make check; make cpp-savings; make manifest-experiment;
.venv/bin/python -m pip --no-cache-dir check; make note NOTE_DATE=2026-09-30.
The test harness does not use assert and remains active with NDEBUG. Numeric tests explicitly reject
nonfinite outputs and use 1e-12 * max(1, abs(expected)) tolerance. This is not a universal error bound.
No coverage percentage, speedup, exact-money precision or personal mastery is claimed.

## Failures, limitations and continuation

All implementation checks passed at first execution. The deliberately mutated scratch build failed
as intended; the repository implementation was not replaced. Restricted DNS was resolved by approved
network access. No permission weakening or suppressed failure. The first PDF render passed all text,
structure and visual checks; no layout revision was needed.

The full staged task diff and PDF text are reviewed for credentials, private contacts, unlicensed
content, large assets, unwanted branding and unsupported claims before commit. The final automated
scan outcome is recorded below. Personal review remains Not yet reviewed. C002 is Done, C003 Ready
for October 7 and Q008 still next on October 1. Lawful entitlement/sample evidence still blocks Q004a;
no input is required to continue synthetic work. No acquisition or narrower empirical claim approved.

Daily scheduling remains active at 08:00 Europe/London; no scheduling changes were needed. New
research stops after December 31, 2026. This is pre-publication evidence; actual commit/push outcome,
remote verification and any observed CI result belong in the final briefing and automation memory.

Final staged audit: all 15 task files and extracted PDF text reviewed. Automated sensitive/contact/
branding scans found no matches; all files are below 1 MB and all 31 local Markdown links resolve.
Staged whitespace checks pass. No unrelated changes, real market data or dependency changes included.
