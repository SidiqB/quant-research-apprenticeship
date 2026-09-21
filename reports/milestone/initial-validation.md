# Initial validation - 21 September 2026

Environment: Python 3.12 on macOS. Dependency versions are captured in requirements-lock.txt;
pyproject.toml defines supported ranges. No numerical packages were added before they were needed.

| Check | Result |
|---|---|
| Editable package install | Passed |
| Unit and artifact tests | 25 passed |
| Ruff lint and format | Passed for 15 Python files |
| Strict mypy | Passed for 11 package source files |
| Dependency consistency | No broken requirements |
| Experiment repeatability | Identical JSON on rerun |
| Expected release schedule | Missing, missing, 100, 100, 60, 60 |
| Invalid join mismatches | 4 of 6 synthetic decisions |
| Role matrix integrity | 49 unique postings, eight firms; source links and access dates present |
| Daily plan | 102 dated tasks, 21 September-31 December 2026 |
| PDF verification | Three pages; headings/text extracted; page origins checked; all rendered pages visually inspected |

The initial PDF layout spilled its table and final answer onto nearly empty pages. Typography and spacing
were adjusted, then all three final pages were rendered and inspected. Poppler produced font-cache warnings
in the restricted environment, but completed rendering; final images showed readable text, intact tables,
page numbers and no clipped content. No percentage test-coverage claim is made.

GitHub command-line tooling was unavailable and SSH authentication failed. Existing HTTPS Git authentication
was verified as SidiqB. The account's existing no-reply email was verified through GitHub settings and configured
only for this repository, avoiding publication of a private contact address. Global configuration was not changed.

The GitHub workflow is configured for Python 3.11, 3.12 and 3.13. Local validation covers Python 3.12;
remote status must be checked after push before claiming those additional versions passed.

Current empirical limitation: all market-related values are explicitly synthetic. There is no tested alpha,
market-calibrated execution result, live order placement or real option-chain study.
