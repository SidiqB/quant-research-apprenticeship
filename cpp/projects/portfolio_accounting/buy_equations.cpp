#include <iostream>

int main() {
    // Synthetic whole money units; one known affordable buy, with fill equal to mark.
    const int cash_before = 800;
    const int shares_before = 4;
    const int price = 50;
    const int buy_shares = 2;
    const int fee = 3;

    const int wealth_before = cash_before + shares_before * price;
    const int notional = buy_shares * price;
    const int cash_after = cash_before - notional - fee;
    const int shares_after = shares_before + buy_shares;
    const int holdings_after = shares_after * price;
    const int wealth_after = cash_after + holdings_after;

    std::cout << "before: cash=" << cash_before << "; shares=" << shares_before
              << "; mark=" << price << "; wealth=" << wealth_before << '\n';
    std::cout << "buy: shares=" << buy_shares << "; fill=" << price
              << "; notional=" << notional << "; fee=" << fee << '\n';
    std::cout << "after: cash=" << cash_after << "; shares=" << shares_after
              << "; holdings=" << holdings_after << "; wealth=" << wealth_after << '\n';
    std::cout << "reconcile: cash_debit=" << cash_before - cash_after
              << "; holdings_increase=" << holdings_after - shares_before * price
              << "; wealth_change=" << wealth_after - wealth_before << '\n';
}
