#include <iostream>

// A single-asset account snapshot, not an order or a market-price record.
struct AccountState {
    int cash_units;
    int shares;
};

int main() {
    const AccountState initial{800, 4};
    const int mark_units_per_share = 50;
    const int holdings_units = initial.shares * mark_units_per_share;
    const int wealth_units = initial.cash_units + holdings_units;
    std::cout << "initial: cash=" << initial.cash_units << "; shares=" << initial.shares
              << "; mark=" << mark_units_per_share << "; holdings=" << holdings_units
              << "; wealth=" << wealth_units << '\n';

    const AccountState empty{};
    std::cout << "empty: cash=" << empty.cash_units << "; shares=" << empty.shares
              << "; wealth=" << empty.cash_units + empty.shares * mark_units_per_share << '\n';
}
