#include <iostream>

// Fixed synthetic snapshots. Every monetary input is a whole money unit.
// No trade, external input, fee, liability or fractional share is modelled.
int main() {
    const int cash = 800;
    const int shares = 4;
    const int initial_mark = 50;
    const int higher_mark = 55;
    const int lower_mark = 45;

    const int initial_holdings = shares * initial_mark;
    const int higher_holdings = shares * higher_mark;
    const int lower_holdings = shares * lower_mark;

    std::cout << "initial: cash=" << cash << "; shares=" << shares
              << "; mark=" << initial_mark << "; holdings=" << initial_holdings
              << "; wealth=" << cash + initial_holdings << '\n';
    std::cout << "higher mark: cash=" << cash << "; shares=" << shares
              << "; mark=" << higher_mark << "; holdings=" << higher_holdings
              << "; wealth=" << cash + higher_holdings << '\n';
    std::cout << "lower mark: cash=" << cash << "; shares=" << shares
              << "; mark=" << lower_mark << "; holdings=" << lower_holdings
              << "; wealth=" << cash + lower_holdings << '\n';
}
