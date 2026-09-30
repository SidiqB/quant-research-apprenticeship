#ifndef QUANT_RESEARCH_SAVINGS_HPP
#define QUANT_RESEARCH_SAVINGS_HPP

// Effective annual rate as a fraction; whole model years; no intermediate rounding.
// Finite nonnegative principal/rate and nonnegative years are required.
// Throws invalid_argument for invalid inputs; overflow_error for a nonfinite
// computed growth factor or balance. This is educational floating-point arithmetic.
double compound_balance(double principal, double annual_rate, int years);

#endif
