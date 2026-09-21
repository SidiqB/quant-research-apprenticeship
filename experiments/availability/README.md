# Experiment 001: observation time versus availability

Question: can a join on economic observation time introduce future information?
Hypothesis: final revised values used before publication disagree with the contemporaneously available value.
Data: two explicitly synthetic versions of one earnings observation. No market data, licence or randomness involved.
Observation period: 1-6 January 2026, UTC; six daily decisions at midnight.
Feature: earnings, originally 100, revised to 60. Observation date January 1; releases January 3 and 5.
Target: agreement with the known release schedule, not future returns.
Protocol: exhaustive enumeration of the six decisions; no training or fitting.
Assumptions: instantaneous availability at equality; zero processing latency; no age limit.
Metric: number of decisions differing from a deliberately invalid final-vintage join.
Results: see results.json; regenerate with `make experiment`.
Limitations: hand-built counterexample, not a prevalence estimate or evidence of alpha. Accurate vendor timestamps remain essential.
Next: add interval-aware validation splitting and purge training labels that overlap test decisions.
