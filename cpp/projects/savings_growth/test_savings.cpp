#include "savings.hpp"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {
int checks = 0;

void expect_close(double actual, double expected, const std::string& label) {
    ++checks;
    // Check finiteness explicitly: a NaN must never pass an error comparison.
    if (!std::isfinite(actual) ||
        std::abs(actual - expected) > 1e-12 * std::max(1.0, std::abs(expected))) {
        throw std::runtime_error(label + ": incorrect balance");
    }
}

template <typename Error>
void expect_error(double principal, double rate, int years, const std::string& label) {
    ++checks;
    try {
        (void)compound_balance(principal, rate, years);
    } catch (const Error&) {
        return;
    }
    throw std::runtime_error(label + ": expected exception was not raised");
}

void run_tests() {
    // Independent decimal hand arithmetic; no pow-based expected values.
    expect_close(compound_balance(1000.0, 0.05, 1), 1050.0, "C001 regression");
    expect_close(compound_balance(1000.0, 0.05, 2), 1102.5, "interest on interest");
    expect_close(compound_balance(1000.0, 0.05, 3), 1157.625, "unrounded third year");
    expect_close(compound_balance(80.0, 0.25, 3), 156.25, "binary-exact example");
    expect_close(compound_balance(1.0, 1.0, 10), 1024.0, "ten doublings");
    expect_close(compound_balance(2.0, 5.0, 2), 72.0, "500 percent is not 5 percent");
    expect_close(compound_balance(0.01, 0.1, 2), 0.0121, "no annual cent rounding");
    expect_close(compound_balance(1000.0, 0.0, 40), 1000.0, "zero rate");
    expect_close(compound_balance(1000.0, 0.05, 0), 1000.0, "zero years");
    expect_close(compound_balance(0.0, 0.05, 40), 0.0, "zero principal");
    expect_close(compound_balance(0.0, 0.0, 0), 0.0, "all zero");

    const double largest = std::numeric_limits<double>::max();
    const int most_years = std::numeric_limits<int>::max();
    expect_close(compound_balance(largest, largest, 0), largest, "zero-year shortcut");
    expect_close(compound_balance(largest, 0.0, most_years), largest, "zero-rate shortcut");
    expect_close(compound_balance(0.0, largest, most_years), 0.0, "zero-principal shortcut");

    const double inf = std::numeric_limits<double>::infinity();
    const double nan = std::numeric_limits<double>::quiet_NaN();
    for (const double invalid : {-1.0, inf, -inf, nan}) {
        expect_error<std::invalid_argument>(invalid, 0.05, 2, "invalid principal");
        expect_error<std::invalid_argument>(invalid, 0.0, 0, "principal before shortcuts");
        expect_error<std::invalid_argument>(1000.0, invalid, 2, "invalid rate");
        expect_error<std::invalid_argument>(0.0, invalid, 0, "rate before shortcuts");
    }
    expect_error<std::invalid_argument>(1000.0, 0.05, -1, "negative years");
    expect_error<std::invalid_argument>(0.0, 0.0, -1, "years before shortcuts");
    expect_error<std::invalid_argument>(1.0, 0.05, std::numeric_limits<int>::min(),
                                        "minimum integer years");
    expect_error<std::overflow_error>(largest, 1.0, 1, "balance overflow");
    expect_error<std::overflow_error>(1.0, largest, 2, "factor overflow");
    // Explicit limitation: factor can overflow even when scaled wealth could fit.
    expect_error<std::overflow_error>(std::numeric_limits<double>::min(), 1.0, 1100,
                                      "conservative intermediate overflow");

    // A separate repeated-year construction, useful beyond the fixed expected values.
    double yearly = 250.0;
    for (int year = 1; year <= 30; ++year) {
        yearly += yearly * 0.04;
        expect_close(compound_balance(250.0, 0.04, year), yearly, "yearwise cross-check");
    }
}
}  // namespace

int main() {
    try {
        run_tests();
        std::cout << "Savings function checks passed: " << checks << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
