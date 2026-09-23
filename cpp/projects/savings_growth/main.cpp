#include <iomanip>
#include <iostream>

int main() {
    // Synthetic teaching example: one year, no cash flows, fees or taxes.
    const double principal = 1000.0;
    const double annual_rate = 0.05;
    const double interest = principal * annual_rate;
    const double closing_balance = principal + interest;

    std::cout << "Synthetic savings example: one year\n"
              << std::fixed << std::setprecision(2)
              << "Opening balance (units): " << principal << '\n'
              << "Annual rate (percent): " << annual_rate * 100.0 << '\n'
              << "Interest (units): " << interest << '\n'
              << "Closing balance (units): " << closing_balance << '\n';
    return 0;
}
