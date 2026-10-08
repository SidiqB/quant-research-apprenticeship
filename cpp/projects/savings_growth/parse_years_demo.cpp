#include "years.hpp"
#include "savings.hpp"

#include <iomanip>
#include <iostream>
#include <stdexcept>

int main() {
    const int years = parse_whole_years("002");
    std::cout << "Synthetic whole-year parser example\n";
    std::cout << "Text 002 -> " << years << " whole years\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "1000 at 5% -> " << compound_balance(1000.0, 0.05, years) << '\n';
    try {
        (void)parse_whole_years("2.5");
        std::cerr << "ERROR: fractional spelling was accepted\n";
        return 1;
    } catch (const std::invalid_argument&) {
        std::cout << "Text 2.5 -> rejected; no year value returned\n";
    }
    return 0;
}
