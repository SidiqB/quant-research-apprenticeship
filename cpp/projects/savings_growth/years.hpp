#ifndef QUANT_RESEARCH_YEARS_HPP
#define QUANT_RESEARCH_YEARS_HPP

#include <string>

// Nonempty ASCII decimal digits, leading zeros allowed, value in [0, INT_MAX].
// Throws invalid_argument for spelling; out_of_range for a digit-only overflow.
// The supplied string's full length is checked, including embedded NUL bytes.
int parse_whole_years(const std::string& text);

#endif
