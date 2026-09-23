# Savings growth: first C++ example

C001, 23 September 2026. Synthetic arithmetic exercise, with no market data or bank product.
Sidiq review status: Not yet reviewed.

## Question and predeclared protocol

Can a compiled C++ program reproduce one year of interest on an invented 1,000-unit opening balance
at a fixed 5% effective annual rate? Hypothesis: interest is 50 units and closing wealth is 1,050 units.
The period is exactly one model year; there are no calendar dates, deposits, withdrawals, fees or taxes.
The inputs are deliberately fixed, finite, nonnegative literals. There is no external input interface;
general input validation belongs to C002/C003 when functions and parsing are introduced.

The acceptance test compiles with warnings treated as errors, runs the executable, and compares every
output line with the independently hand-calculated `expected.txt`. Compiler or process failure fails
the check. A display mismatch fails the check. No fitted parameters, tuning or empirical evaluation.

## Hand arithmetic

Five percent means five per hundred: `r = 5 / 100 = 0.05`.
For one year, `interest = P * r = 1000 * 0.05 = 50`.
The closing balance is `B = P + interest = 1000 + 50 = 1050`.
As an independent check, divide the opening amount into 100 equal pieces of 10 units and take five.
Expected absolute error in each displayed amount is zero units; output precision is two decimal places.

## Build, run and test

From the repository root, using a C++17-capable Clang or GCC compiler and Make:

```sh
make cpp-savings
make cpp-check
make check
```

The first command builds and runs the example. The second compares it with `expected.txt`, and is
included in `make check`. Build products and captured output stay in ignored `build/`.
To choose another compiler, use `make -B cpp-check CXX=clang++` (or `CXX=g++`).

Equivalent manual build and run:

```sh
mkdir -p build/cpp/savings_growth
c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror cpp/projects/savings_growth/main.cpp -o build/cpp/savings_growth/savings
./build/cpp/savings_growth/savings
```

Do not pass amounts on the command line: this lesson always uses the constants in `main.cpp`.

## Read the syntax

`#include <iostream>` declares stream facilities, and `<iomanip>` supplies `std::setprecision`.
`int main()` is the program entry point; braces enclose its body and semicolons end statements.
`const double principal = 1000.0;` creates a named floating-point value that cannot be reassigned.
`*` multiplies, `+` adds, `std::cout <<` sends values to standard output, and `'\n'` starts a new line.
`std::fixed` with `std::setprecision(2)` displays two digits after the decimal point.
`return 0;` reports successful completion to the operating system.

Formatting changes the display, not the stored number. Binary floating-point can approximate decimal
inputs; two displayed decimal places do not provide a general exact-money accounting contract.

## Limits and next lesson

The golden-output check verifies this one fixture at display precision. It cannot establish behaviour
for other balances, rates, horizons or rounding boundaries. No speedup or investment return is claimed.
One period does not distinguish simple from compound interest; multi-year use needs a stated convention.
C002 will introduce a reusable function, annual compounding, zero-rate/zero-year cases and invalid inputs.

## Official sources consulted on 23 September 2026

- [Microsoft C++ built-in types](https://learn.microsoft.com/en-us/cpp/cpp/fundamental-types-cpp?view=msvc-170): floating-point types and precision limits.
- [Microsoft stream formatting](https://learn.microsoft.com/en-us/cpp/standard-library/ios-functions?view=msvc-170#fixed) and [setprecision](https://learn.microsoft.com/en-us/cpp/standard-library/iomanip-functions?view=msvc-170#setprecision): display convention.
- [Clang user manual](https://clang.llvm.org/docs/UsersManual.html): language mode and warning flags.

See the [teaching note](../../../research_log/2026-09-23.md) and
[PDF](../../../reports/daily/2026-09-23-learning-note.pdf) for definitions and exercises.
