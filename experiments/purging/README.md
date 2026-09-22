# Forward-label purging experiment (Q002)

## Question and protocol

Can a chronological split include training targets that use evaluation-period information?
Hypothesis: ordering decisions alone is insufficient; removing every pre-evaluation label
whose closed interval touches or crosses the evaluation boundary eliminates that overlap.
This follows Q001: correct feature availability does not establish training-target eligibility.

Data are deliberately constructed synthetic timestamps, 1-10 January 2026, all at 00:00 UTC.
There are eight sample decisions on January 1-8 and no market prices or returns. The evaluation
decision window is January 5 inclusive to January 8 exclusive. Labels use closed information
intervals; the retained training endpoints must be strictly earlier than January 5.
The model, if one existed, would be fit before the evaluation window and held fixed throughout it.

Predeclared evaluation: compare decision-only chronology, a one-row trailing gap, and interval
purging on identical rows. Report original sample IDs, retained count, purged count and count of
training intervals intersecting the evaluation decision window. Check the partition against hand
arithmetic. No fitting, tuning, accuracy or performance metrics are involved. A row gap is a
comparison rule written locally, not a run of scikit-learn's multi-fold splitter.

| ID | Decision day | Label end day | Expected purged-holdout role |
|---|---:|---:|---|
| A | 1 | 3 | Train |
| B | 2 | 5 | Purged: touching |
| C | 3 | 7 | Purged: overlapping |
| D | 4 | 4 | Train: zero-duration interval |
| E | 5 | 6 | Evaluation |
| F | 6 | 8 | Evaluation |
| G | 7 | 10 | Evaluation |
| H | 8 | 9 | Excluded: at window end |

Expected counts: decision-only chronology retains A-D with two overlaps. A one-row gap removes D
but leaves both B and C, retaining three rows with two overlaps. Interval purging retains A,D,
removes B,C and leaves zero overlaps. These constructed counts are not market frequencies.

## Reproduction

Run `make purging-experiment`, or `.venv/bin/python scripts/purging_experiment.py`.
Use `--output /path/to/results.json` for a separate output. Run `make check` for unit tests,
independent interval-oracle checks, lint, formatting, types and deterministic artifact reproduction.
See [results.json](results.json) for observed counts and [the learning note](../../research_log/2026-09-22.md)
for equations, limitations and worked answers.

## Scope and references

An empty retained training set is returned explicitly; model callers must skip or reject that fold.
An empty evaluation set is rejected. Global sample IDs support tied decisions across different assets.
UTC normalization handles repeated daylight-saving times. Callers still own valid timestamp provenance,
label receipt/publication delays, feature timing, training-only preprocessing and market calendars.
No later training rows are used, so post-evaluation embargo and arbitrary K-fold purging are out of scope.

Primary technical documentation consulted on 22 September 2026:

- [scikit-learn TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html):
  chronological folds and a gap expressed as a number of samples. Our variable-horizon counterexample
  motivates checking timestamps directly; it is not a claim that all configured gaps fail.
- [MLFinLab cross-validation implementation documentation](https://random-docs.readthedocs.io/en/latest/implementations/cross_validation.html):
  distinguishes purging overlapping training information from embargo. This implementation is deliberately
  a smaller past-only holdout, not a reproduction of PurgedKFold or combinatorial cross-validation.
- [Python datetime](https://docs.python.org/3/library/datetime.html): aware timestamps, UTC conversion
  and comparison behavior when timezone objects are identical, including the ignored fold attribute.
