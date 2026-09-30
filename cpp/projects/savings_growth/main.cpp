#include "savings.hpp"

#include <iomanip>
#include <iostream>

int main() {
    // Synthetic teaching example: one year, no cash flows, fees or taxes.
    const double principal = 1000.0;
    const double annual_rate = 0.05;
    const double closing_balance = compound_balance(principal, annual_rate, 1);
    const double interest = closing_balance - principal;

    std::cout << "Synthetic savings example: one year\n"
              << std::fixed << std::setprecision(2)
              << "Opening balance (units): " << principal << '\n'
              << "Annual rate (percent): " << annual_rate * 100.0 << '\n'
              << "Interest (units): " << interest << '\n'
              << "Closing balance (units): " << closing_balance << '\n';
    const double two_year_balance = compound_balance(principal, annual_rate, 2);
    const double simple_two_year_balance = principal * (1.0 + 2.0 * annual_rate);
    std::cout << "\nSynthetic annual compounding comparison\n"
              << "Two-year compound balance (units): " << two_year_balance << '\n'
              << "Two-year simple balance (units): " << simple_two_year_balance << '\n'
              << "Interest-on-interest difference (units): "
              << two_year_balance - simple_two_year_balance << '\n'
              << std::setprecision(3)
              << "Three-year unrounded balance (units): "
              << compound_balance(principal, annual_rate, 3) << '\n';
    return 0;
}
