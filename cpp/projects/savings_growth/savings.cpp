#include "savings.hpp"

#include <cmath>
#include <stdexcept>

double compound_balance(double principal, double annual_rate, int years) {
    // Validate before shortcuts: even a zero-year request must have valid inputs.
    if (!std::isfinite(principal) || principal < 0.0) {
        throw std::invalid_argument("principal must be finite and nonnegative");
    }
    if (!std::isfinite(annual_rate) || annual_rate < 0.0) {
        throw std::invalid_argument("annual rate must be finite and nonnegative");
    }
    if (years < 0) {
        throw std::invalid_argument("years must be nonnegative");
    }
    if (principal == 0.0 || years == 0 || annual_rate == 0.0) {
        return principal;
    }
    const double growth_factor = std::pow(1.0 + annual_rate, years);
    const double balance = principal * growth_factor;
    if (!std::isfinite(growth_factor) || !std::isfinite(balance)) {
        throw std::overflow_error("compound growth exceeds finite double arithmetic");
    }
    return balance;
}
