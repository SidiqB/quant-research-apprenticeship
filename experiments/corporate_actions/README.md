# Synthetic corporate-action returns

Q008 asks whether explicit share and cash units reconcile a single holding interval across a split
and cash dividend. These eight invented cases have no empirical dates, vendor data or alpha claim.
The reusable implementation is [corporate_actions.py](../../src/quant_research/data/corporate_actions.py).
Run `make corporate-action-experiment`; `results.json` is a deterministic record of inputs, component
returns, eight hand totals and three deliberately wrong calculations. Run `make check` for validation.

## Contract and derivation

Start with one share, raw opening price P0 and raw closing price P1. Let s denote ending shares per
opening share: 2 for a 2-for-1 split, 0.2 for a 1-for-5 reverse split. Let C denote known dividend
entitlement per **opening** share. Ending equity is s*P1; ending wealth is s*P1+C.

- Raw price change: P1/P0-1. This compares differently sized share units when a split occurs.
- Capital return excluding cash: s*P1/P0-1.
- Income contribution: C/P0.
- Total holding-period return: (s*P1+C)/P0-1.

All returned numbers are fractions, not percentages. The function requires explicit keyword action
inputs; s=1 and C=0 assert known absence, never unknown evidence. All four inputs must be finite
Python int/float values (excluding bool); prices/ratio must be positive and cash nonnegative. Missing,
nonfinite, zero-price and invalid values raise. Nonfinite intermediates and complete underflow of
positive quantities also raise. Outputs are immutable. Floating-point rounding remains; numeric range
checks conservatively reject some rescalable cases. No exact-money guarantee or universal error bound.

## Eight hand cases

| Case | P0 | P1 | s | C | Total return |
|---|---|---|---|---|---|
| No action, gain | 100 | 110 | 1 | 0 | 10% |
| No action, loss | 100 | 90 | 1 | 0 | -10% |
| Split only | 100 | 50 | 2 | 0 | 0% |
| Reverse split | 20 | 100 | 0.2 | 0 | 0% |
| Cash offset | 100 | 98 | 1 | 2 | 0% |
| Dividend and gain | 100 | 103 | 1 | 2 | 5% |
| Split and dividend | 100 | 49 | 2 | 2 | 0% |
| Split, dividend and gain | 100 | 54 | 2 | 2 | 10% |

In the combined zero-return case, a dividend quoted as 1 per ending share converts to C=2 per
opening share. Passing 1 without conversion produces -1%. Multiplying C by s again incorrectly
produces +2%. Omitting the split in the split-only case produces -50%; inverting it produces -75%.
These are deliberate negative controls, not observed market returns.

## Timing and scope

Assume the holder owns the opening share through the relevant event and is entitled to the declared
cash. C is a receivable valued at par as of the endpoint, not necessarily settled cash available to
trade. Ex-date, announcement, record and payment dates serve different purposes. This function does
not determine entitlement, infer event order or decide when an observation becomes available.
The fixture defines its normalized action inputs explicitly; upstream event evidence is still required.
No cash is reinvested within the interval. Compounding these interval returns into a strategy would
require a separate reinvestment/financing policy and ledger, especially before payment.

Pass unadjusted prices only. Already split-adjusted prices plus s double-count a split; total-return
adjusted prices plus C can double-count dividends. The scalar API cannot identify the price basis,
currency or provenance: these are caller obligations, not enforced admission gates. Fractional shares
are permitted mathematically. Cash in lieu, rounding, fees, taxes, FX, spin-offs, rights, mergers and
terminal proceeds are outside scope. Zero prices and missing terminal evidence are not mapped to a
-100% return; Q009b will address terminal-event evidence separately. Q004a/Q005b still block empirical use.

## Validation and primary sources

52 tests cover hand components, invalid inputs, required action arguments, overflow/underflow,
immutability, unit conversion and two byte-identical subprocess replays. An independent exact-Fraction
ledger starts with 15 shares over 54 configurations and three currency scales: 162 comparisons.
It checks total return and component reconciliation with absolute/relative tolerance 1e-12.
Full project checks pass with 415 Python tests and 66 C++ checks; no dependency was added.

Consulted 1 October 2026: SEC Investor.gov [Stock Split](https://www.investor.gov/introduction-investing/investing-basics/glossary/stock-split)
explains the share-count/price relation; [Ex-Dividend Dates](https://www.investor.gov/introduction-investing/investing-basics/glossary/ex-dividend-dates-when-are-you-entitled-stock-and)
distinguishes entitlement dates and special cases. The one-share wealth equations above are derived
for our stated synthetic contract; this is not a replication of any vendor's return methodology.
