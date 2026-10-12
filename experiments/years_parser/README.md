# Whole-year parser boundary oracle

Synthetic engineering fixture, completed 9 October 2026. No market data or performance claim.

Run `make cpp-years-oracle` from the repository root. The C++ test probe reports its target
`int` maximum, then Python supplies 75 complete byte strings and compares exact results with
an independent regex-plus-Python-integer reference. The test runs inside `make check`.

The cases comprise 26 numeric values, the same values with three leading zeros, and 23 long or
malformed inputs. They include zero, the inclusive maximum, its predecessor and two successors,
whitespace, signs, fractional/trailing text, NUL and non-ASCII bytes. Spelling errors take precedence
over range errors. The transport preserves input length and does not append a newline.

`boundary-oracle.json` is the observed Apple Clang 21 C++17 result from 9 October: maximum
2147483647; 47 accepted, 21 spelling errors and seven range errors; zero mismatches. Two runs
matched byte for byte. Other C++ targets query their own maximum; the archived value is not a
portable hard-coded acceptance requirement. The reference uses no floating-point conversion.

Two compiled scratch mutations were detected: rejecting the inclusive maximum, and truncating
at NUL before parsing. See the [validation record](../../reports/milestone/2026-10-09-validation.md).
These are two fault checks, not a coverage percentage. The test trusts the target-limit report,
shares the written contract, and covers finitely many inputs. The 1000-significant-digit fixture
is within the tested Python interpreter's conversion limit; no resource protection is disabled.

The probe is test plumbing. It does not implement the deferred principal/rate CLI or establish
financial realism. Read the [teaching note](../../research_log/2026-10-09.md) and
[verified PDF](../../reports/daily/2026-10-09-learning-note.pdf).

## Fractional-input failure

Studied October 10; integrated October 11 after a zero-budget day. Run `make cpp-fractional-failure`
(or `make check`). Two separate builds use the unchanged parser or a deliberately wrong adapter;
only the latter is compiled with WRONG_ADAPTER. Its narrow finite [0,10] guard keeps the teaching
cast defined; it is not an alternative production parser. Both are fixed synthetic experiments.

The verifier runs each binary twice, checking exact stdout/stderr bytes and exit status, and
compares combined output to the archived text fixtures. The correct build accepts 002 and 0,
rejects 2.5, 0.5 and 2.0 before savings, and exits 0. The wrong build accepts all five and exits 1
with exactly three mismatches. The verifier succeeds only when both behaviours match expectations.
It checks Decimal balances independently and writes no tracked output. Build first before running
`.venv/bin/python scripts/verify_fractional_failure.py` directly. Standard checks use ordinary Python
without optimization, so the verifier's assertions are active.

`fractional-failure.json`, `fractional-correct.txt` and `fractional-negative-control.txt` preserve
the October 10 result bytes. See the [note](../../research_log/2026-10-10.md),
[PDF](../../reports/daily/2026-10-10-learning-note.pdf) and
[validation](../../reports/milestone/2026-10-10-validation.md). No fractional-year accrual, loss
estimate, exhaustive correctness, empirical performance or personal mastery is established.

## Fresh reproduction

Run `.venv/bin/python scripts/reproduce_years_evidence.py` from the repository root, without `-O`.
It compiles six temporary executables and checks each evidence path twice, including exact expected
wrong-adapter failure. Original October 11 results are preserved in
`experiments/years_parser/reproduction-2026-10-11.json`; the recipe reports the current Git baseline.
This uses the installed compiler/environment and does not prove cross-platform or all-input correctness.
