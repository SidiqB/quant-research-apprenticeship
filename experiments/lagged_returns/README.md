# Availability-aware lagged returns

Q010 asks whether valid future observations or later revisions can change an earlier feature.
The hypothesis is that a fixed session window plus per-interval availability selection prevents this.
This is synthetic engineering validation, with invented returns on the prospective pinned NYSE
October 29-November 30, 2026 calendar. It is not an empirical momentum or performance result.

## Contract

`lagged_return` in [the package](../../src/quant_research/alpha/lagged_returns.py) takes an explicit
asset, return-field name, valid pre-open decision, positive integer `periods`, nonnegative integer
`skip` and nonnegative elapsed `latency`. It requires `periods + skip + 1` covered prior sessions,
including the starting close. The latest `skip` completed sessions are excluded from the window.
Each included return must end at its exact scheduled core close; no calendar-day shifting is used.

A target `Observation` asserts a complete return from the preceding session's close to its
`observed_at`. Its `available_at` must reflect all inputs and computation, including any revised
corporate-action information. The caller establishes consistent identity, interval, currency,
actions, costs and reinvestment/wealth basis. Field names and timestamps cannot authenticate this.
Do not pass price levels, multi-session returns or future-adjusted prices labelled as old returns.

For each required close, use Q001's selector to take the latest revision available at the decision
after elapsed processing latency. Equality is eligible. Missing/delayed intervals produce `None`
for both gross and fractional return, with ordered selected records and explicit `missing_at`.
No filling, gap compression or other-asset substitution is allowed. Unknown calendar history raises.
Skipped intervals need no return values; their session boundaries must still be covered.

Complete windows calculate `G = product(1 + r_i)` and `R = G - 1`. A frozen result retains settings,
UTC boundaries and selected original records. Targets require finite built-in numbers >= -1;
identifiers, counts, latency, record types and duplicate versions are checked. Other assets/features
are ignored for calculation. Off-grid observations cannot fill a required close. Duplicate versions
anywhere, even future/unrelated rows, fail. Input iterables are fully consumed.

## Reproduce and observed evidence

```sh
make lagged-return-experiment
.venv/bin/python -m pytest -q tests/test_lagged_returns.py
make check
make note NOTE_DATE=2026-10-04
```

The November 4 decision uses November 2 +10% and November 3 -10%: 100 becomes 110 then 99, so -1%.
Adding a November 4 +20% return and November 3 revision to +50% published November 5 leaves that
entire earlier result unchanged. November 5 with `skip=1` selects the same historical window and
can use the revision: +65%. One microsecond of latency excludes the exactly-at-decision revision
and restores -1%. Removing the November 3 interval yields unknown, not zero.

Wrong controls sum +10% and -10% to zero, or take the latest vintage regardless of publication and
report +65% at the earlier decision. Both contradict the declared feature protocol.

Sixty-two new tests pass: 24 fixture input permutations; 125 exact Fraction wealth paths; 420
independent calendar/window/latency comparisons with prefix and added-future-revision invariance;
hand windows across clock changes, Thanksgiving and early closing; missing/delayed inputs; explicit
skip semantics; identity/field isolation; invalid input, numeric limits and immutable evidence.
Two subprocess replays match [archived JSON](results.json) byte-for-byte. Comparison tolerance for
floating arithmetic is relative/absolute 1e-12 in the exact-ledger test; selection/missingness and
future-invariance compare exactly. Full project validation passes 602 Python tests and 66 C++ checks.

## Limits and integration prerequisites

Geometric linking presumes consistent subperiod wealth accounting. Q008's total return can be an
input under a declared reinvestment convention, but cash entitlement does not establish spendable
cash or executable reinvestment. A synthetic integration test demonstrates arithmetic only. A -100%
interval keeps abstract linked wealth at zero, without validating subsequent security observations.
Q009b's unresolved terminal evidence must not be zero-imputed or removed to complete a window.

The invariance guarantee assumes valid batches, unchanged original records and truthful availability.
Invalid future data or an input-generator failure can abort a past query. Membership, provenance,
source adapters, settlement, ranks, targets and strategy evaluation remain outside this function.
Q004a licensed samples and Q005b interval/basis/availability integration remain empirical prerequisites.

Floats are approximate. Intermediate overflow and complete positive underflow raise, conservatively
before any later factor can restore mathematical range. Twenty minimum positive gross factors here
remain representable at `2^-1060`; subtracting one rounds to -1, so inspect `gross_return` as well.
The pinned calendar cannot cover a 21-interval window with a known starting boundary. No complete
underflow test is claimed; the original mistaken 20-factor expectation was corrected. No coverage
percentage, measured speed, compliance or empirical alpha claim is made.

## Primary sources

- [CFA Institute 2020 GIPS Standards for Firms](https://www.gipsstandards.org/wp-content/uploads/2021/03/2020_gips_standards_firms.pdf), glossary "link", printed page 77: geometric linking arithmetic only; no compliance claim.
- [NYSE hours and calendars](https://www.nyse.com/trade/hours-calendars): Thanksgiving, early closing and regular core schedule.
- [Python datetime](https://docs.python.org/3/library/datetime.html): aware instants and timezone conversion.

Consulted October 4, 2026. The Investor.gov total-return URL returned an empty glossary entry and
was not relied upon. [Teaching note](../../research_log/2026-10-04.md) and
[validation evidence](../../reports/milestone/2026-10-04-validation.md) record results and failures.
