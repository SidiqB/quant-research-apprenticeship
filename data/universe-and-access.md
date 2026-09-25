# Equity universe and source admission contract v1

Recorded 25 September 2026 for Q004. This is a provisional engineering specification within the
existing equity research scope. It commits no spending and asserts no real dataset access.
The rules below are project choices made before any market-return experiment; they are not vendor claims.

## Research question and decision

Can a source support historical stock selection, total-return accounting and auditable information timing
under the project's actual permissions? Hypothesis: inactive-price coverage alone is insufficient;
missing entitlement, terminal-event evidence or release vintages must prevent empirical admission.

Compare CRSP US Stock and Norgate US Platinum for the first price-based laboratory. First investigate any
existing lawful CRSP entitlement; otherwise consider Norgate only after resolving platform, licence and
revision limitations. Neither source is selected for acquisition today. No login, trial, purchase or market
data download was attempted. Data access is unestablished, not proven absent from Sidiq's other accounts.
Continue synthetic engineering until access and evidence are resolved. Fundamental signals remain deferred.

## Provisional investable universe

| Dimension | Contract |
|---|---|
| Market and period | US-listed, USD-quoted common shares; desired daily study window 2010-01-01 through 2025-12-31, plus 20 earlier exchange sessions for eligibility warm-up |
| Security scope | Ordinary common shares of operating/holding companies on NYSE, Nasdaq or NYSE American at the decision time, including REIT common shares; retain separate qualifying share classes with permanent security identifiers |
| Exclusions | ADRs, preferreds, funds/ETFs/ETNs, units, partnerships, warrants, rights, blank-check companies and OTC-only listings; missing or ambiguous historical classification excludes new entry and is audited |
| Decision | Provisional 09:00 America/New_York on a trading session, using only completed prior sessions whose publication and receipt evidence plus processing latency permit use at that instant |
| Price/liquidity | Prior-session unadjusted close at least USD 5; mean unadjusted close times volume over the prior 20 completed sessions at least USD 1 million per session; all 20 observations must be present, available and valid |
| Volume meaning | USD turnover proxy from close times consolidated shares traded, not exact transaction-level dollar volume; vendor definitions must match or a documented contract revision is needed |
| History | No present-day survival filter and no present-day index list; historical listing, security-type and identifier intervals determine entry eligibility |
| Execution | Eligibility is not a fill: an eventual execution model must use a later executable price, halts and costs; no same-close execution or capacity assertion |

Thresholds are untuned teaching defaults, not evidence of tradability or an optimized strategy. An IPO may
enter only after 20 valid prior sessions. A missing volume, stale price or classification is not zero.
Do not pad missing sessions or carry the last price forward to manufacture eligibility. Q006 will implement
the exchange-session calendar and decision-time contract; Q009 will implement historical membership.
This specification does not claim those components are already implemented.

For security i at decision t, let H_i(t) be verified historical listing/classification eligibility and
A_i(t) mean all required inputs were available by t. Let P_i(d-1) be the prior raw close, and define
L_i(t) = sum(P_i(s) * V_i(s) for the 20 prior sessions s) / 20.
Then E_i(t) = H_i(t) AND A_i(t) AND [P_i(d-1) >= 5] AND [L_i(t) >= 1000000].
All terms must be known. Unknown terms exclude new entry with a reason; they do not erase existing holdings.

## Exits, delistings and corporate actions

Retain inactive securities, identity changes and listing exits. Eligibility loss stops new entry; it does
not remove a held security or invent liquidation proceeds. Distinguish last on-exchange trading date,
OTC migration, cash/stock merger consideration, final payment date and confirmed zero recovery. Missing
terminal proceeds remain unresolved and block a complete realized-return claim. Never replace a missing
terminal return with zero or -100% without evidence. A failed company and an acquired company can have very
different outcomes, so survivor selection need not bias every sample upward.

Store raw closes/volumes separately from adjusted histories and adjustment methodology. Q008 will test
split/dividend arithmetic. A vendor's total-return series must be reconciled before use; do not add a
separate delisting return to a series that already includes it. Legacy CRSPAccess descriptions are useful
for concepts but are not a field mapping for the newer CIZ format. Verify the purchased format explicitly.

## Information availability and vintages

For each input retain observation time, publication time, receipt time, revision identifier, source version,
retrieval time, timezone, units and exact file hash. The availability instant is the later of publication
and receipt, plus the declared processing latency. Retrieval today does not prove receipt years ago.
A blanket one-day lag cannot establish that a revised historical field was available at an old decision.
If source vintages/timing are missing, label any later study as revised-history research under stated
assumptions; it cannot pass this strict point-in-time contract. Such a scope relaxation needs a recorded
decision before empirical work. Q005a's known fold bug must be fixed before general ingestion.

## Licensed-source comparison

The following are summaries of public primary documentation consulted on 25 September 2026, not tests of
licensed samples. Statuses in configs/data-access-2026-09-25.toml distinguish documentation from project verification.

### CRSP

The [official product page](https://indexes.morningstar.com/research-data-products/crsp-us-stock-databases)
describes daily/monthly prices, corporate actions, active/inactive securities and permanent PERMNO/PERMCO
identifiers. It offers research data to institutional and practitioner licensees. This makes it a candidate
for longitudinal equity research, but does not establish this project's entitlement or redistribution rights.

The [CRSPAccess data descriptions](https://www.crsp.org/crsp_pdf/crsp-us-stock-indexes-databases-data-descriptions-guide-crspaccess/)
distinguish post-delisting amounts and missing-return codes. We must test the actual delivered format's
terminal-return convention, historical type/exchange mapping, period coverage and event timing. Historical
release vintages, local extraction and permitted storage/output remain unverified. No price quote is assumed.

### Norgate

The [US subscription table](https://norgatedata.com/prices.php) lists Platinum history from 1990 with inactive
securities and historical constituents. The [content definitions](https://norgatedata.com/data-content-tables.php)
distinguish exchange-to-OTC migration from securities no longer tradeable and disclaim complete delisting
coverage. A vendor's delisted flag therefore cannot directly implement this project's exchange exit rule.

The [access overview](https://norgatedata.com/) requires a Windows database or Windows VM; this macOS checkout
has no verified compatible setup. The [data FAQ](https://norgatedata.com/data-package-faq.php) documents price
adjustment choices and continuous historical corrections without a versioning mechanism. Its current-history
product alone therefore fails our strict historical-vintage requirement. Unadjusted and adjusted histories
still require sample-level reconciliation and an audit of terminal proceeds.

The [EULA dated 20260825](https://norgatedata.com/subscribe/eula.php), sections 8 and 21, restricts redistribution
and requires content deletion after subscription expiry while permitting retention of defined derived data.
Project decision: no vendor content in Git, including a private repository, and no assumed right to publish
samples or keep raw archives indefinitely. Applicable use, storage and output permissions must be recorded
before access; these summaries do not grant permission. Check current terms again at acquisition.

## Eight evidence gates

| Gate | What project verification must establish |
|---|---|
| licence_entitlement | Actual authorized user, product/tier, purpose, active term and approved processing environment, without recording credentials |
| local_access | Successful lawful sample extraction in the intended environment, reproducible instructions and hashes |
| historical_identity | Permanent security mapping and historical type/exchange intervals, including ticker reuse and share classes |
| inactive_coverage | Sample audit of inactive/OTC exits and coverage over the proposed window; catalog claims alone are insufficient |
| corporate_actions | Raw/adjusted conventions, units and split/dividend reconciliation against known events |
| terminal_events | Last trade, proceeds, payment timing and missing-event policy; no silent zero fill or double counting |
| availability_vintages | Historical publication/receipt and version evidence consistent with the declared decision instant |
| permitted_outputs | Documented storage, retention and distribution plan for the intended artifacts, including subscription expiry |

The reusable assess_access function rejects incomplete/unknown fields and invalid status/reference values.
It admits a declared record only when all eight gates say verified. Documented means a vendor statement;
unknown means not established; failed means conflicting evidence for this contract. All three block.
Nonblank references are required even for unknowns, so the unresolved question is traceable.

This is an evidence checklist, not a permission service. It does not fetch references, test credentials,
validate a licence, detect false assertions or automatically gate any ingestion implementation. A fabricated
all-verified record could pass. Human examination and subsequent ingestion checks remain necessary.
Each assessment is dated; future evidence belongs in a new dated record so this run remains reproducible.

## Observed result and unresolved input

Zero of two candidates passes; each has eight unverified gates. That is the state of evidence in this
project, not a ranking of vendor quality. make access-experiment reproduces the assessment and the synthetic
controls in experiments/data_access. No observed market return, complete coverage or alpha is claimed.

Before real-data acquisition, Sidiq should identify any existing licensed entitlement and its permitted
research environment; otherwise a budget/source choice will be needed. Do not send credentials. No answer
is needed to continue Q005a, Q005 or the synthetic corporate-action/membership fixtures. Q004's specification
and comparison are complete; obtaining and auditing a licensed sample remains a separate open task Q004a.
