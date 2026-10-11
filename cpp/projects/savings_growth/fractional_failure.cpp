// Synthetic fixed fixtures only; WRONG_ADAPTER is a deliberate negative control.
#include "savings.hpp"
#include "years.hpp"

#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

int selected_parser(const std::string& text) {
#ifdef WRONG_ADAPTER
    // Intentionally wrong: full floating conversion does not enforce whole-year text.
    std::size_t consumed = 0;
    const double value = std::stod(text, &consumed);
    // A narrow bound keeps this teaching cast defined; this is not a general parser.
    if (consumed != text.size() || !std::isfinite(value) || value < 0 || value > 10) {
        throw std::invalid_argument("outside fixed demonstration scope");
    }
    return static_cast<int>(value);
#else
    return parse_whole_years(text);
#endif
}

bool examine(const std::string& text, bool should_accept) {
    int years = 0;
    try {
        years = selected_parser(text);
    } catch (const std::invalid_argument&) {
        std::cout << text << "\trejected\t-\tno calculation\n";
        return !should_accept;
    }
    const double balance = compound_balance(1000.0, 0.05, years);
    std::cout << text << "\taccepted\t" << years << "\t" << balance << '\n';
    return should_accept;
}

int main() {
    std::cout << std::fixed << std::setprecision(2);
    int failures = 0;
    if (!examine("002", true)) { ++failures; }
    if (!examine("0", true)) { ++failures; }
    if (!examine("2.5", false)) { ++failures; }
    if (!examine("0.5", false)) { ++failures; }
    if (!examine("2.0", false)) { ++failures; }
    std::cerr << "contract mismatches: " << failures << '\n';
    return failures == 0 ? 0 : 1;
}
