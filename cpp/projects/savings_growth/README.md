# Savings growth: reusable C++ function

C001 completed 23 September; C002 completed 30 September 2026. Synthetic arithmetic only;
no market data, bank product or empirical investment result. Sidiq review: Not yet reviewed.

## Question and contract

Can a reusable function reproduce annual compounding and reject invalid inputs? C001 established
one year's arithmetic; C002 distinguishes compound interest from simple interest over several years.
The predeclared protocol uses independent hand values, zero cases, invalid inputs, overflow checks,
a yearwise cross-check and exact executable-output comparison. No parameter fitting or speed claim.

`double compound_balance(double principal, double annual_rate, int years)` returns
`P * (1 + r)^n`. Principal and rate must be finite and nonnegative; years must be a nonnegative `int`.
The rate is a fraction: `0.05` means 5%, whereas `5.0` means 500% and is valid under this contract.
Years are whole model years, with a constant effective annual rate, reinvested interest, no cash flows,
fees or taxes and no rounding between years. Negative rates are outside this lesson's scope.

Invalid values raise `std::invalid_argument`, including when another input is zero. After validation,
zero principal, zero years or zero rate returns the principal. A nonfinite computed growth factor or
balance raises `std::overflow_error`. A finite result is an approximation, not exact money accounting.
There is no input parser yet: callers must supply whole-year integers. C++ implicit conversions can
truncate a fractional argument before this function sees it; C003 must validate text before conversion.

## Worked synthetic experiment

| Calculation | Hand result (units) |
|---|---|
| 1000 at 5%, one year | 1050.00; interest 50.00 |
| 1000 at 5%, two years compounded | 1102.50 |
| 1000 at 5%, two years simple interest | 1100.00 |
| Compound minus simple after two years | 2.50 |
| 1000 at 5%, three years, no intermediate rounding | 1157.625 |

Year two earns `1050 * 0.05 = 52.50`, including `50 * 0.05 = 2.50` on year one's interest.
The first five output lines preserve C001's example; the appended comparison distinguishes conventions.
`expected.txt` contains hand-authored results; it is not generated from the implementation.

## Build, run and check

From the repository root with a C++17 compiler:

```sh
make cpp-savings
make cpp-check
make check
make -B cpp-check CXX=clang++
```

The build links `main.cpp` and `savings.cpp`. `savings.hpp` declares the function for both the demo
and `test_savings.cpp`. All files are tracked as Make dependencies, including the shared header.
Products stay in ignored `build/cpp/savings_growth/`. No arguments are parsed by the example.

`cpp-check` runs 66 function checks and compares the demo with `expected.txt`. The function checks
include 14 known/zero cases, 19 invalid-input cases, three overflow cases and 30 yearwise comparisons.
Floating-point comparison requires finite output and absolute error at most
`1e-12 * max(1, abs(expected))`. Output comparison is exact at the declared display precision.
The harness uses exceptions and exit status rather than `assert`, so checks survive `NDEBUG` builds.
A temporary simple-interest mutation fails on the two-year hand value. Two demo runs match expected bytes.

## Beginner C++ guide

A declaration announces a function's name, input types and return type. The definition supplies its
body. Parameters receive values from the caller; `return balance;` gives one result back. This function
performs arithmetic without printing, so the same calculation can serve the demo and tests.
A header shares the declaration; its include guard prevents repeated inclusion. The compiler builds
source files and the linker joins their references. `if` chooses a branch; `throw` reports an error,
and the test runner's `catch` handles it and returns a failing exit status when appropriate.
`std::pow` computes a power and `std::isfinite` rejects infinities and NaN. Display precision affects
printing only. The 5% third-year result is shown with three decimals to preserve the teaching example.

## Numerical and model limitations

This is a basic `double` implementation. `1 + r` can round to 1 for tiny rates; rounding error grows
with the horizon. It has no guaranteed cent-level accuracy over the entire accepted input range.
A growth factor may overflow even when scaling by a tiny principal would make final wealth finite:
`compound_balance(numeric_limits<double>::min(), 1.0, 1100)` deliberately raises. Log-domain scaling
would need a separate precision contract and tests. No numerical extension is claimed here.

The function does not model negative rates, fractional years, varying rates, deposits, withdrawals,
day counts, inflation or contractual bank rounding. Whole-year type conversion and textual parsing
remain the caller's responsibility. C003 introduces validated command-line inputs on October 7.

## Primary sources consulted on 30 September 2026

- [Microsoft C++ functions](https://learn.microsoft.com/en-us/cpp/cpp/functions-cpp?view=msvc-170): declarations, parameters and return values.
- [Microsoft pow reference](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/pow-powf-powl?view=msvc-170): power evaluation and range errors.
- [Microsoft isfinite reference](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/finite-finitef?view=msvc-170): finite-value classification.

These document C++ facilities; financial assumptions are explicitly chosen for this synthetic lesson.
See the [teaching note](../../../research_log/2026-09-30.md),
[PDF](../../../reports/daily/2026-09-30-learning-note.pdf) and
[validation record](../../../reports/milestone/2026-09-30-validation.md).

## C003a intuition: 5 October

Read the [text-versus-value worksheet](text_vs_years.md) and run `make cpp-text-years` from
the repository root. This fixed teaching example demonstrates lost fractional evidence and
reuses C002; it does not parse user input. Grammar and parser implementation remain later steps.
