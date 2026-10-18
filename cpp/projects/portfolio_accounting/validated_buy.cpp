// Fixed educational domain: whole units, one asset, no debt or short selling.
struct AccountState {
    int cash_units;
    int shares;
};

// A false result preserves both fields. Bounds also keep int arithmetic safe.
bool try_buy(AccountState& state, int quantity, int price_units, int fee_units) {
    const int limit = 10000;
    if (state.cash_units < 0 || state.cash_units > limit ||
        state.shares < 0 || state.shares > limit ||
        quantity <= 0 || quantity > limit ||
        price_units <= 0 || price_units > limit ||
        fee_units < 0 || fee_units > limit) {
        return false;
    }
    if (fee_units > state.cash_units) {
        return false;
    }
    const int available_units = state.cash_units - fee_units;
    if (quantity > available_units / price_units || quantity > limit - state.shares) {
        return false;
    }
    const int debit_units = quantity * price_units + fee_units;
    state.cash_units -= debit_units;
    state.shares += quantity;
    return true;
}
