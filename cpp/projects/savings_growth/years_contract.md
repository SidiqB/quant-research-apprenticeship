# C003a whole-year text contract

Defined 7 October 2026, completing the unfinished October 6 prerequisite. Sidiq review: Not yet reviewed.
This contract specifies a future parser; only the fixed library demonstration is implemented today.
The existing C002 savings function remains unchanged. All examples are synthetic.

## Acceptance and rejection

Accept a nonempty sequence containing only ASCII digits `0` through `9`, interpreted in base ten,
whose mathematical value lies in `0..std::numeric_limits<int>::max()` inclusive. Leading zeros are
allowed and have no octal meaning. Every byte belongs to the input and must satisfy the grammar.
Reject all signs (including `+2` and `-0`), whitespace anywhere, decimal points, exponent notation,
separators, suffixes, embedded NUL bytes and non-ASCII digit encodings. Do not trim, round or truncate.
Missing text is an error, not zero. There is no additional length cap in this contract; transport
limits, memory exhaustion and input-size protection belong to a future external-input interface.

For digits d1..dk, start n0 = 0 and interpret nj = 10 * n(j-1) + dj mathematically.
This recurrence defines meaning, not permission to overflow a C++ int while checking it.
A future parser must detect out-of-range input before unsafe arithmetic or use checked conversion.
Invalid input must report failure without returning a usable year value; error API is the next lesson.

| Text or explicit byte description | Expected contract decision | Reason |
|---|---|---|
| `0` | Accept, 0 | Zero whole years |
| `2` | Accept, 2 | Two whole years |
| `002` | Accept, 2 | Decimal leading zeros allowed |
| `000` | Accept, 0 | Still zero |
| Empty string | Reject | No digits |
| `2.5` or `2.0` | Reject | Decimal point forbidden, even when value is whole |
| `-1` or `-0` | Reject | Minus sign forbidden |
| `+2` | Reject | Plus sign forbidden |
| Space then 2; 2 then space; tab; newline | Reject | No whitespace normalization |
| `2x`, `2e0`, `0x2`, `1,000` | Reject | Not entirely decimal digits |
| Digit 2 then NUL then x | Reject | NUL does not end this input range |
| UTF-8 encoding of Arabic-Indic digit two | Reject | Outside ASCII digits |
| Decimal representation of int maximum | Accept, maximum | Inclusive type boundary |
| Decimal representation of maximum plus one | Reject | Not representable as int |

These are hand-authored acceptance requirements, not observed parser-test results. The maximum is
queried from the compilation target, not hard-coded. The local October 7 probe reported 2147483647;
2147483648 is therefore the first too-large nonnegative value on this target. Do not calculate
`INT_MAX + 1` in an int. Parsing success also does not promise a finite savings balance: C002 may
separately reject financial overflow. Neither boundary is a realistic investment horizon.

## Why library success is insufficient

Run `make cpp-conversion-contract`. The hand-authored expected output records two distinct gaps:
`2x` gives a successful numeric-prefix conversion but leaves the suffix; `-1` gives a successful,
complete integer conversion but violates our whole-year policy. This is a library experiment,
not a reusable parser or a demonstration that the complete contract has been implemented.

Read conversion_contract.cpp in order. The includes provide conversion, output, text and error
codes. `int main()` starts execution. `const std::string` retains fixed text, and `int ... = 0`
initializes the receiving number. `auto` asks the compiler to infer the returned result type.
`data()` locates the first character; `size()` counts characters; their sum marks the position
just after the input. The range includes the first position and excludes the end position.
`std::from_chars` tries to convert that range into the supplied integer, using decimal base by default.
It writes through its integer reference parameter. No floating-point conversion occurs here.

`ec` is the result's error code. Comparing it with `std::errc{}` asks whether conversion succeeded.
`ptr` is the position where conversion stopped. Comparing it with the end asks whether the complete
input was consumed. Equality `==` produces a Boolean; `std::boolalpha` prints true/false words.
The output streams join these observations and the value. The second block repeats the same
operations on `-1`; the final statement explains that neither case satisfies the intended contract.
These observations alone do not enforce digit-only input (consider `-0`). Next session implements
one small function using the contract, with explanation before introducing its branches.

## Worked financial connection and limits

Text `002` means n = ((0 * 10 + 0) * 10 + 0) * 10 + 2 = 2 years. With P = 1000 units and r = 0.05
per model year, B = P * (1 + r)^n = 1102.50 units. This assumes reinvestment, a constant effective
annual rate, no fees, taxes, inflation, deposits or withdrawals. Fees would lower wealth. Text `2.5`
is outside this whole-year model; no fractional-year convention or forecast follows from the example.
No market data, profitability claim, input-security proof or exhaustive parser coverage is asserted.

## Sources and reproduction

Consulted 7 October 2026: [Microsoft from_chars documentation](https://learn.microsoft.com/en-us/cpp/standard-library/charconv-functions?view=msvc-170)
explains conversion result/error/stop position and non-skipped whitespace;
[Microsoft numeric_limits documentation](https://learn.microsoft.com/en-us/cpp/standard-library/numeric-limits-class?view=msvc-170)
explains querying type bounds. Our digit-only, sign and leading-zero rules are project policy.
The host runs Clang with its C++ standard library; local observations are independently checked.

Run `make cpp-conversion-contract`, `make check` and `make -B cpp-check`. The exact output comparison
is included in the normal C++ checks and CI. See the [daily note](../../../research_log/2026-10-07.md)
and [validation evidence](../../../reports/milestone/2026-10-07-validation.md).
