#include "savings.hpp"

#include <iomanip>
#include <iostream>
#include <string>

// Fixed synthetic teaching example. This is deliberately NOT an input parser.
int main() {
    const std::string original_text = "2.5";
    const double fractional_years = 2.5;  // Separately written; no text conversion.
    const int converted_years = static_cast<int>(fractional_years);

    std::cout << "Original text: " << original_text << '\n';
    std::cout << "Separate numeric value: " << fractional_years << '\n';
    std::cout << "After explicit int conversion: " << converted_years << '\n';
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Balance C002 computes for the converted years: "
              << compound_balance(1000.0, 0.05, converted_years) << '\n';
    std::cout << "The function received 2 years; it cannot recover the lost fraction.\n";
}
