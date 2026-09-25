# Data policy

No real market dataset is included yet. Experiment 001 constructs synthetic values explicitly in code.
Raw, interim and processed data are ignored by Git. Never substitute generated prices for an unavailable feed.

Before ingestion, record source URL, access date, licence/redistribution rights, download command,
SHA-256 hash, units, timezone, observed time, publication time, vendor receipt time and revision policy.
Use the latest of publication and receipt time for actual availability. Record processing latency separately.
Keep delisted securities and time-varying membership; a present-day constituent list is not a historical universe.
Store split/dividend methodology and release vintages. Unavailable timestamps must block point-in-time claims.
Free adjusted price histories alone cannot substantiate survivorship-free fundamental research.
Keep large datasets outside version control and distribute only permitted small samples or download instructions.

## Universe and admission

[The Q004 contract](universe-and-access.md) defines the provisional US common-stock universe, desired
2010-2025 study period, decision-time inputs and source comparison. CRSP and Norgate remain unverified
for project use; no real dataset is admitted. The dated evidence registry is
configs/data-access-2026-09-25.toml. Run `make access-experiment` to reproduce its declaration assessment
and separately labelled synthetic controls. The checker does not authenticate rights or enforce ingestion.
Q004a tracks entitlement and sample verification; independent engineering continues while it is blocked.
