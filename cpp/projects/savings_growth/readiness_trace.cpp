#include "savings.hpp"
#include "years.hpp"

#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

// A fixed teaching trace: preserve rejection instead of replacing it with zero.
void trace(const std::string& label, const std::string& text, double rate) {
    int years = 0;
    try {
        years = parse_whole_years(text);
    } catch (const std::invalid_argument&) {
        std::cout << label << ": spelling; calculation skipped\n";
        return;
    } catch (const std::out_of_range&) {
        std::cout << label << ": range; calculation skipped\n";
        return;
    }
    std::cout << label << ": years=" << years << "; ";
    try {
        const double balance = compound_balance(1000.0, rate, years);
        std::cout << "balance=" << balance << '\n';
    } catch (const std::overflow_error&) {
        std::cout << "calculation overflow; no balance\n";
    }
}

int main() {
    std::cout << std::fixed << std::setprecision(2);
    const std::string maximum = std::to_string(std::numeric_limits<int>::max());
    trace("blank", "", 0.05);
    trace("zero", "0", 0.05);
    trace("leading zeros", "002", 0.05);
    trace("fraction", "2.5", 0.05);
    trace("suffix", "2x", 0.05);
    trace("beyond range", maximum + "0", 0.05);
    trace("maximum positive rate", maximum, 0.05);
    trace("maximum zero rate", maximum, 0.0);
}
