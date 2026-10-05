# Text is evidence; a converted value can lose it

C003a intuition lesson, 5 October 2026. Synthetic fixed examples only.
Sidiq review status: Not yet reviewed.

A whole-year savings model needs a nonnegative count of completed model years.
First classify the complete original text by hand. These are desired decisions,
not the results of an implemented parser. Quotes show text boundaries, not input characters.

| Text | Hand decision | Reason |
|---|---|---|
| `"2"` | Accept as 2 years | Nonnegative whole count |
| `"2.5"` | Reject | Fractional years are outside this model |
| `"-1"` | Reject | Negative count is outside this model |
| `""` (blank) | Reject | No count was supplied; missing is not zero |
| `"2x"` | Reject | A numeric prefix is not a complete count |

Whitespace, optional signs, leading zeros and the precise upper range are tomorrow's
grammar decisions. Do not infer their policy from this five-case table.

## Read the small example slowly

`#include <string>` supplies the standard text type. `std::string` stores characters;
`"2.5"` is text, whereas unquoted `2.5` is a numeric literal of type double.
The existing includes supply the savings declaration and output formatting.

In [text_vs_years.cpp](text_vs_years.cpp), `int main()` starts the demonstration.
`const std::string original_text = "2.5";` stores text without changing it.
`const double fractional_years = 2.5;` separately creates a numeric value; it does not parse that text.
`const int converted_years = static_cast<int>(fractional_years);` explicitly requests conversion.
For this finite, representable value, conversion discards the fraction, giving 2.
`const` means these named values cannot be reassigned. A semicolon ends each statement.

The first three `std::cout` statements display the original text, separate numeric value
and resulting integer. `<<` sends each piece to the output stream; `\n` ends a line.
The formatting statement selects two decimals for the balance, as in C001/C002.
The function call uses 1000 units, annual rate 0.05 and the already converted count.
The last statement explains the lost evidence. The braces enclose the function body;
reaching the end of main returns success.

The cast is a visible counterexample, not validation to copy into a future parser.
Only this safe fixed conversion is executed; out-of-range floating-to-int conversions
can have undefined behaviour and must not be used as a range check.

## Hand arithmetic and reproduction

Year 1: 1000 + 1000*0.05 = 1050. Year 2: 1050 + 1050*0.05 = 1102.50.
That is a valid two-year result, not a validated answer to a 2.5-year request.
Annual compounding over whole years does not specify a partial-year convention.
Assume fixed effective annual interest, no deposits/withdrawals, fees, taxes or inflation.
Real costs reduce wealth and a real rate need not remain fixed. No investment return is observed here.

Run `make cpp-text-years` to display the example. `make cpp-check` compiles it with
C++17 warnings treated as errors and compares every output line against the hand-authored
[expected output](text_vs_years_expected.txt), alongside the unchanged C002 checks.
`make check` also runs the Python suite and quality checks. Python Decimal can independently
update 1000 by two annual 5% credits to verify 1102.50 without calling the C++ function.

This is the October 5 teaching slice only. The years parser, command-line interface and
other input policies remain unimplemented. See the [daily note](../../../research_log/2026-10-05.md).

## Primary sources

Consulted 5 October 2026: Microsoft's [standard conversions](https://learn.microsoft.com/en-us/cpp/cpp/standard-conversions?view=msvc-170)
documents fractional truncation and representability restrictions. Its
[string and character literals](https://learn.microsoft.com/en-us/cpp/cpp/string-and-character-literals-cpp?view=msvc-170)
explains quoted string literals. Our whole-year acceptance policy and teaching example are project choices.
