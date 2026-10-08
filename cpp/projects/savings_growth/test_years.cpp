#include "years.hpp"
#include "savings.hpp"

#include <cmath>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {
int checks = 0;

void expect_value(const std::string& text, int expected) {
    ++checks;
    if (parse_whole_years(text) != expected) {
        throw std::runtime_error("accepted years have the wrong value");
    }
}

template <typename Error>
void expect_error(const std::string& text) {
    ++checks;
    try {
        (void)parse_whole_years(text);
    } catch (const Error&) {
        return;
    }
    throw std::runtime_error("invalid years did not raise the required error");
}

void run_tests() {
    expect_value("0", 0);
    expect_value("2", 2);
    expect_value("002", 2);
    expect_value("000", 0);
    expect_value("12", 12);
    const std::string maximum = std::to_string(std::numeric_limits<int>::max());
    expect_value(maximum, std::numeric_limits<int>::max());
    expect_value("000" + maximum, std::numeric_limits<int>::max());
    expect_value(std::string(1000, '0') + "2", 2);

    for (const std::string text : {"", "2.5", "2.0", "-1", "-0", "+2", " 2",
                                   "2 ", "2\t", "2\n", "2 0", "2x", "2e0", "0x2",
                                   "1,000"}) {
        expect_error<std::invalid_argument>(text);
    }
    expect_error<std::invalid_argument>(std::string("2\0x", 3));
    expect_error<std::invalid_argument>(std::string("\0", 1));
    expect_error<std::invalid_argument>(std::string("\xD9\xA2", 2));
    expect_error<std::out_of_range>(maximum + "0");
    expect_error<std::out_of_range>(std::string(1000, '9'));
    // Spelling is checked before representability, even for an enormous prefix.
    expect_error<std::invalid_argument>(std::string(1000, '9') + "x");

    ++checks;
    const double balance = compound_balance(1000.0, 0.05, parse_whole_years("002"));
    if (!std::isfinite(balance) || std::abs(balance - 1102.5) > 1e-9) {
        throw std::runtime_error("parsed years failed the hand-calculated balance");
    }
}
}

int main() {
    try {
        run_tests();
        std::cout << "Passed " << checks << " whole-year parser checks\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
