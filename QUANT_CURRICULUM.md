# C++ quant curriculum: 4 October - 31 December 2026

This revision implements Sidiq's 4 October request. C++ is the default language for new educational
projects, starting with simple syntax and increasing complexity gradually. Existing Python research is
preserved and used for independent checks where useful. No rewrite of tested Python modules is required.
The programme aims for broad understanding of major strategy families, not exhaustive mastery of every
variant or a set of production trading systems by New Year. No strategy is promised to make money.

## Pace and teaching contract

One 45-90 minute session per day. Monday: intuition, financial vocabulary and a hand calculation.
Tuesday: derive the smallest model. Wednesday: implement a small C++ component. Thursday: test boundaries
and compare an independent calculation. Friday: costs, failure scenarios and uncertainty. Saturday: explain
and reproduce, without adding complexity. Sunday: consolidate, repair and prepare the weekly report.
New C++ concepts must be introduced before use, with line-by-line explanations of short examples.
Each step produces a learning note, exercises and separate answers; all productive days retain the verified
PDF requirement. No day must contain three lessons merely because its commit draw is three.

Each weekly project is a small vertical slice, not all the functionality suggested by its title.
If prerequisites fail, repeat and simplify; move the advanced extension to 2027 instead of rushing.
Completion of a build is not evidence of personal mastery; keep Sidiq review status honest and do not wait
for it before ordinary authorised work. Real data remains behind Q004a/Q005b provenance/licence gates.
Synthetic experiments test mechanics and assumptions, never empirical profitability.

## Calendar and acceptance gates

| Dates | Family | Example C++ project | New concepts | Required limitations/checks |
|---|---|---|---|---|
| 2026-10-05 to 2026-10-11 | C++ foundations | Extend savings_growth; start return_statistics | Parsing, vectors, functions, sample mean/variance | Invalid input; zero cases; +10% then -10% equals -1%; no market prediction |
| 2026-10-12 to 2026-10-18 | Backtesting and portfolio accounting | Build a small event-driven single-asset ledger | Structs, headers, enums, cash/positions, delayed trades | Cash conservation; costs; future-price mutation must not alter past decisions |
| 2026-10-19 to 2026-10-25 | Trend and momentum | trend_lab: lagged time-series trend and cross-sectional ranking examples | Rolling windows, sorting, rank ties, volatility scaling | Whipsaw; momentum crashes; leverage; test untouched periods and cost sensitivity |
| 2026-10-26 to 2026-11-01 | Statistical arbitrage I | pairs_lab: spread construction, rolling z-score, training-only hedge ratio | Covariance, regression, windows, two-leg accounting | Correlation is not cointegration; borrow, spread drift, structural breaks; no risk-free claim |
| 2026-11-02 to 2026-11-08 | Statistical arbitrage II | Extend pairs_lab with cointegration diagnostics and break scenarios | Residual stationarity, estimation uncertainty, walk-forward tests | Pair selection bias; repeated testing; p-value validity; train-only fit; losing pair examples |
| 2026-11-09 to 2026-11-15 | Equity factors and portfolio construction | factor_lab: value/quality/low-risk rank fixture and constrained weights | Containers, pure functions, normalisation, exposures | Fundamental release lags; sectors; turnover; crowding; no current-universe shortcut |
| 2026-11-16 to 2026-11-22 | Carry and fixed-income relative value | carry_lab: bond cash flows and futures/FX carry scenarios | Discount factors, duration, curve interpolation, units | Funding, roll conventions, basis widening, leverage and tail losses |
| 2026-11-23 to 2026-11-29 | Options and volatility strategies | volatility_lab: payoffs, binomial pricing and a discrete hedge example | Trees, numerical bounds, finite differences, hedge ledger | Volatility risk premium is not arbitrage; jumps, spread costs, model error and short-convexity losses |
| 2026-11-30 to 2026-12-06 | Market making and execution | execution_lab: small book, inventory policy, TWAP/participation | Maps, queues, deterministic events, cancellation, partial fills | Adverse selection; uncertain queue position; latency; inventory limits; simulated fills are assumptions |
| 2026-12-07 to 2026-12-13 | Event-driven, macro and alternative data | event_lab: announcement-time join plus merger and macro scenario examples | Time alignment, immutable events, feature vintages | Deal breaks; surprise versus level; revised data; unavailable historical text; rights and capacity |
| 2026-12-14 to 2026-12-20 | Machine learning and strategy combinations | model_lab: linear baseline, one regularised model, simple ensemble fixture | Train/test interfaces, frozen parameters, losses, model comparison | Leakage, unstable relationships, tuning budget, selection bias; no deep-learning requirement |
| 2026-12-21 to 2026-12-27 | Risk, allocation and robustness | risk_lab: equal weights versus risk scaling, drawdown/stress/tail examples | Scenario loops, covariance conditioning, error handling | Estimation error; correlation spikes; volatility targeting can deleverage after losses; tail uncertainty |
| 2026-12-28 to 2026-12-31 | Consolidation and New Year handover | Reproduce projects; compare families; write honest year-end report | Build tooling, clean reproduction, clear explanations | List unfinished work, failed hypotheses, data gaps and proposed 2027 research |

## Strategy atlas: coverage beyond the deep projects

| Family / variation | Small example | Distinguishing assumption and limitation |
|---|---|---|
| Time-series trend; breakouts; moving-average rules | Lag yesterday's signal before today's trade | Directional persistence; whipsaw and parameter dependence |
| Cross-sectional momentum; sector momentum | Rank six synthetic assets with ties | Relative ranking differs from own-price trend; concentration and crashes |
| Short-term reversal | Buy prior losers in a cost-aware fixture | Bid-ask bounce can imitate predictability; turnover can erase gains |
| Pairs trading; cointegration | Two-leg residual and break scenario | Statistical convergence is uncertain; regression is not proof of stationarity |
| Basket/residual statistical arbitrage | Remove a known synthetic common factor | Estimated factors drift; correlated crowding and hidden exposures |
| Value, quality, size, low volatility, multifactor | Rank a release-timestamped fundamental fixture | Definitions, delayed releases, distressed stocks, industry biases and capacity |
| FX carry; futures carry; commodity term structure | Carry decomposition with financing and roll | Yield/roll is not guaranteed total return; crash and liquidity risk |
| Fixed-income curve / spread relative value | Duration-matched two-bond shock | Hedge ratios and curve shifts imperfect; financing and basis risk |
| Cash-and-carry; ETF/index arbitrage | Price-gap versus full-cost example | Creation/redemption access, financing, borrow and execution simultaneity |
| Convertible arbitrage | Bond-plus-option stylised decomposition | Credit/equity/volatility coupling; borrow and complex terms; survey-level only |
| Volatility risk premium; delta-hedged options | Long/short option hedge P&L scenario | Gap losses, discrete hedging, vol surface/model mismatch; tail risk |
| Dispersion / correlation trading | Two-asset variance identity fixture | Index versus components is not a free trade; changing implied correlation and costs |
| Market making; order-flow signals | Inventory quotes and adverse-selection event | Fill/queue assumptions, latency, information disadvantage and capital limits |
| Execution algorithms: TWAP, VWAP, participation | Same parent order on identical events | Execution minimises cost/risk; it is not independently an alpha strategy |
| Merger arbitrage; earnings-event strategies | Deal-break loss and announcement surprise | Event timing, financing, deal completion and post-selection bias |
| Systematic macro; seasonality; calendar effects | Vintage-aware release and placebo calendar | Revisions, sparse samples, many hypotheses and unstable regimes |
| Alternative data / text signals | Timestamped synthetic document scores | Coverage, publication/receipt times, licence rights and historical availability |
| Linear/regularised ML; ensembles | Frozen chronological baseline comparison | ML is a modelling method, not its own economic edge; overfitting and drift |
| Risk parity; volatility targeting; defensive allocation | Equal-weight versus risk-scaled scenarios | Construction overlays, not guaranteed alpha; unstable covariance and leverage |
| Crypto funding/basis; cross-venue relative value | Funding-plus-basis stress worksheet in C++ | Venue/custody/counterparty risk, liquidation and transfer delays; no live trading |

Survey examples can share a weekly project's tested calculation kernel. Each family receives an explanatory
note and small worked example; only the calendar's selected projects receive a full implementation cycle.
Advanced Heston/local-volatility, deep learning, production HFT and large factor models are 2027 candidates.

## Minimum strategy report

Question and economic mechanism; terminology; equations and units; data source/period and availability;
entry/exit/sizing rules; financing/shorting assumptions; benchmark; chronological fit/evaluation;
parameter-search budget; gross and net results; turnover, drawdown and relevant uncertainty; at least
one losing or invalid scenario; licence/data limitations; what the result cannot show; interview questions.
Distinguish alpha claims, risk premia, arbitrage under ideal assumptions, execution and allocation methods.
Do not annualise tiny synthetic samples into impressive-looking performance statistics.

## Reading anchors

Accessed 4 October 2026. Read full primary sources before implementing empirical claims; summaries do not
establish replicability today. Later weekly work adds directly relevant primary literature to each report.

- Gatev, Goetzmann and Rouwenhorst, Pairs Trading: Performance of a Relative Value Arbitrage Rule:
  https://www.nber.org/papers/w7032 (bibliographic record found; direct retrieval was blocked this session).
- Moskowitz, Ooi and Pedersen, Time Series Momentum:
  https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum
- Asness, Moskowitz and Pedersen, Value and Momentum Everywhere:
  https://www.aqr.com/Insights/Research/Journal-Article/Value-and-Momentum-Everywhere

These sources motivate separate treatment of own-return trend, relative momentum and relative-value
research. The teaching order and projects above are editorial choices, not claims made by the papers.
