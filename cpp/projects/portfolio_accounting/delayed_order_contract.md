# One delayed order: contract v1

Study date: 22 October 2026. Task L002b. Synthetic teaching fixture only.
Sidiq review status: Not yet reviewed. C++ implementation is L002c, not completed here.

## Domain and known fields

One asset, one fixed order, whole money units and whole shares. Reuse L001d bounds:
cash, shares and fee in 0..10000; price and requested quantity in 1..10000; final
shares at most 10000. The reference rejects non-integer fields, including Boolean values.
No debt, shorts, fractions, partial fills, competing orders or cash reservation.

Event indices are ordered teaching steps, not wall-clock timestamps. Require
0 <= observation_available < decision < resolution. Equal indices are rejected
because this exercise has no within-event tie-breaking policy. Invalid domain,
future/equal observation availability or early/equal resolution invalidates the trace;
it is not a legitimate unfilled order and produces no accounting result.

The decision sees only initial cash/shares, observed price, observation availability,
decision index, fixed threshold 50, requested quantity 2 and fee schedule 3.
It requests two shares when the known observed price is at most 50, otherwise none.
The decision does not read the future fill price or resolution evidence. This is a
teaching rule, not a claim of profitable price predictability. No preliminary cash
reservation or debit occurs. Affordability is checked at the actual proposed fill.

## Resolution policy

A resolution row after the decision carries either a supplied positive fill price
or explicit missingness (JSON null). The fee schedule is known in advance; the fee
is charged once only if all buy checks pass at resolution. A rejected buy leaves
cash/shares unchanged. Cash exactly equal to quantity*price+fee is sufficient.

If no order was requested, the state is no_order and no fee is charged. If an order
was requested but the fill price is missing, the status is unresolved at the fixture
horizon; state is unchanged. Missingness does not mean zero-price execution, a
cancellation, an exchange rejection or proof the order will never fill. Do not copy
the observed price into the missing field. The exercise has no later retry.

If the supplied valid fill is unaffordable or exceeds position capacity, status is
rejected_by_model and state is unchanged; no fee. This is the educational ledger's
rule, not an observed exchange/broker response. Otherwise status is filled, with
C_new = C - n*p - f and q_new = q+n. Initial invalid state is invalid_trace.
No fill price is required for no_order/unresolved outcomes. A malformed supplied
price invalidates a trace even if there is no order, rather than hiding bad input.

## Acceptance examples and boundaries

All prices are synthetic money units per share. Default starting cash/shares are 800/4,
observation price 50 at event 0, decision event 1 and resolution event 2. Fee is 3.

| Case | Change to default | Request | Resolution | Final cash/shares | Fee charged |
|---|---|---|---|---|---|
| Filled | Fill 52 | 2 | filled | 693/6 | 3 |
| Missing fill | Fill missing | 2 | unresolved | 800/4 | 0 |
| Exact cash | Cash 107, fill 52 | 2 | filled | 0/6 | 3 |
| Too little cash | Cash 106, fill 52 | 2 | rejected_by_model | 106/4 | 0 |
| No request | Observed 51, fill 52 | 0 | no_order | 800/4 | 0 |
| Position cap | Shares 9999, fill 52 | 2 | rejected_by_model | 800/9999 | 0 |

The fixture checker compares a separate per-share Decimal reference with these hand-authored
answers, and rejects deliberately corrupted tables. It does not prove that a future C++
implementation obeys this contract. L002d must still test future-price invariance against a
production component and a deliberately leaking control. Whole-unit caps are teaching choices.
