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
