#include <string>

// Teaching fragment: the verifier places unchanged validated_buy.cpp before it.
// -1 is an invalid decision input; 0 is a valid decision to make no request.
int decide_quantity(int observed_price, int available_event, int decision_event) {
    if (observed_price < 1 || observed_price > 10000 ||
        available_event < 0 || available_event >= decision_event) {
        return -1;
    }
    if (observed_price <= 50) {
        return 2;
    }
    return 0;
}

struct DelayedTrace {
    bool valid;
    int request;
    AccountState at_decision;
    AccountState after_resolution;
    std::string status;
    int fee_charged;
};

// One complete fixed-policy trace, not a persistent order or exchange engine.
DelayedTrace delayed_order(AccountState initial, int observed_price,
                           int available_event, int decision_event,
                           int resolution_event, bool has_fill, int fill_price) {
    DelayedTrace trace{false, -1, initial, initial, "invalid_trace", 0};
    if (initial.cash_units < 0 || initial.cash_units > 10000 ||
        initial.shares < 0 || initial.shares > 10000 ||
        resolution_event <= decision_event ||
        (has_fill && (fill_price < 1 || fill_price > 10000))) {
        return trace;
    }
    trace.request = decide_quantity(observed_price, available_event, decision_event);
    if (trace.request < 0) {
        return trace;
    }
    trace.valid = true;
    if (trace.request == 0) {
        trace.status = "no_order";
    } else if (!has_fill) {
        trace.status = "unresolved";
    } else if (try_buy(trace.after_resolution, trace.request, fill_price, 3)) {
        trace.status = "filled";
        trace.fee_charged = 3;
    } else {
        trace.status = "rejected_by_model";
    }
    return trace;
}
