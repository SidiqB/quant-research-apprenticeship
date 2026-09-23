# Daily validation - 23 September 2026

## Scope and result

C001 is the first scheduled Wednesday C++ lesson. With fixed synthetic principal 1000.0 and fractional
annual rate 0.05 for exactly one model year, the executable prints 50.00 interest and 1050.00 closing wealth.
There are no market observations, dated investment returns, deposits, withdrawals, fees or taxes.
Displayed numerical differences from the hand-worked benchmark are zero.

## Checks and evidence

| Check | Observed result |
|---|---|
| Checkout and lock | Clean main, one existing unpushed commit preserved; shared atomic run lock acquired |
| Origin synchronization | Fetch succeeded with network access; origin/main unchanged at 8e21bdb; no divergence |
| Open issues | Authenticated GitHub read returned zero open issues |
| make check | 49 Python tests, Ruff lint/format, strict mypy and new C++ output check all passed |
| Compilation | Apple Clang 21.0.0, arm64 macOS; C++17; Wall, Wextra, Wpedantic, Werror; no diagnostics |
| Golden-output check | Executable output exactly matched the independent hand-authored expected.txt |
| Repeatability | Two further runs matched each other and expected.txt byte-for-byte |
| Wrong-rate diagnostic | Temporary copy with rate 5.0 printed 5000.00 interest and failed the comparison |
| Python quality evidence | 19 files formatted; mypy passed for 13 package files |
| Dependency consistency | pip check found no broken requirements; no new dependency installed |
| PDF renderer | Verified four nonblank pages, headings and text-origin page bounds |
| PDF content audit | Full extracted text exactly matched source after markup, footer and whitespace normalization |
| PDF visual audit | All four Poppler PNGs inspected; legible tables, code, references and exercises; no clipping |

The C++ regression is an executable output comparison, not another pytest case. The expected fixture is
hand-authored; it is never regenerated from the implementation. It detects errors in displayed values,
labels and units for this one case. It does not validate unseen inputs or sub-cent numerical errors.
No coverage percentage, throughput, speedup, or out-of-sample performance is claimed.

The existing CI workflow calls make check, so it will also compile and check C++ when run on the remote.
Remote CI for the new commit has not been observed in this pre-commit record; publication and CI status
are reported in the daily briefing and automation memory. Sidiq review remains Not yet reviewed.

## Failures and recovery

The initial fetch could not resolve github.com inside the network-restricted environment; the approved
network fetch succeeded. Existing authentication was used for a read-only issue request without displaying
or writing its credential. The repository-local author email is the verified no-reply account address.

The first two full-text PDF audit attempts had normalization mistakes: the extractor emits footer text
before page content, and literal pipe separators in the title must be preserved while table pipes are
removed. Correcting only the audit normalization produced an exact full-content match. The PDF itself
needed no layout revision. Poppler used the existing temporary font configuration and emitted no diagnostics.
pip warned about an unwritable cache and disabled it; its dependency consistency check still passed.

## Reproduction and next work

Run make check and make cpp-savings from the repository root. The project README includes a standalone
compiler command and compiler override. Rebuild the PDF with make note NOTE_DATE=2026-09-23.
Temporary mutation sources, binaries and page previews remain in ignored work/; ordinary build output
is in ignored build/. No generated executable is committed.

Q003 resumes Thursday. C002 is ready for the next Wednesday slot; the Q005a availability fold bug remains
open with UTC-normalized input as the documented workaround. No scope decision is needed for these tasks.
