# Strict timestamped observation ingestion

Q005 is an in-memory boundary for the existing availability selector. All fixture values are synthetic;
clock-transition dates are test inputs, including future dates, not observed market activity.

Question: can explicit offsets plus one declared source zone prevent silent timestamp guessing?
Hypothesis: checking each source wall label and offset against its UTC round trip rejects gaps and
inconsistent zones while preserving both explicitly identified fold occurrences.

## Contract

`quant_research.data.ingestion.ingest_observations(rows, source_zone=...)` accepts an iterable of mappings.
Every row has exactly `asset`, `feature`, `observed_at`, `available_at`, and `value`. Identifiers must be
nonempty printable strings with no leading/trailing whitespace; spelling/case and internal spaces are
preserved. Values must be finite built-in integers/floats, excluding booleans, and are converted to float.
This conversion is not exact-decimal accounting and can round large integers or decimal fractions.

Both timestamp strings in every row must represent the declared IANA source zone's local clock, using
`YYYY-MM-DDTHH:MM:SS[.ffffff]Z` or the same form with `+/-HH:MM`. Fractional seconds have 1-6 digits.
Seconds and an explicit known offset are mandatory. Unknown offset `-00:00`, naive strings, leap seconds,
excess precision, malformed dates and invalid offset components fail. No truncation, imputation or guessing.
`Z` and `+00:00` are equivalent. A London summer record encoded in UTC belongs in a `source_zone="UTC"`
batch; declaring `Europe/London` requires its local clock and matching summer offset. Different offsets
across a transition are valid under the same zone. This policy intentionally rejects mixed representations.

Convert the supplied offset timestamp to UTC, then convert back into the declared named zone. Both wall
fields and offset must match. A spring gap cannot round-trip. An autumn fold accepts either of its two
valid explicit offsets; the adapter never chooses an occurrence for an offset-free ambiguous label.
Check `available_at >= observed_at` in UTC. Return an immutable tuple of UTC `Observation` objects in
input order only after validating the entire batch. No partial return on failure, although an input iterator
has been consumed up to the failing row; there is no external transaction or rollback mechanism.

Duplicate `(asset, feature, observed_at UTC, available_at UTC)` versions fail whether values agree or not.
Later publication times are distinct revisions. Duplicate checks cover this batch only; callers combining
batches must retain the existing selector check or add persistent uniqueness. Errors give the one-based
row number and rule without echoing raw source values. Inputs are not modified. Retain raw source files,
source identifiers, zone declarations and timezone-database provenance upstream; returned records do not
retain those fields. This adapter does not establish data entitlement or authenticate publication truth.

## Reproduce and expected results

Run `make ingestion-experiment`, `make check`, and `make note NOTE_DATE=2026-09-27`.
The experiment also accepts `--output PATH` for independent scratch replays. The archived JSON records
2 accepted versions at 00:30 and 01:30 UTC on 25 October 2026, and decision values 1 then 2.
All eight invalid controls are rejected: duplicate, missing identifier, missing ambiguous-time offset,
both spring-gap offsets, inconsistent zone, nonfinite value and reversed instants.

The 90 new test cases include explicit UTC answers for London, New York and the half-hour Lord Howe fold;
gaps in all three zones; microsecond spring-transition continuity; equivalent-instant duplicate encodings;
reversed chronology; invalid schemas, identifiers and scalars; 24 input permutations; generator/empty-batch
behavior; no partial return or raw-source-value echo; and two exact experiment replays. Full suite: 257 tests.

## Sources and limits

Primary sources consulted 27 September 2026: [PEP 495](https://peps.python.org/pep-0495/) describes fold and
gap semantics and why constructors alone are not strict invalid-time validators;
[zoneinfo](https://docs.python.org/3/library/zoneinfo.html) describes IANA rules and fold-aware conversions;
[datetime](https://docs.python.org/3/library/datetime.html) documents ISO parsing and timezone conversion.
The accepted timestamp grammar and whole-batch contract are project choices, narrower than Python's parser.

No new dependency is added. Named zones use the available system/IANA database, not a pinned embedded
snapshot; explicit expected-offset tests expose changes in these fixtures, not all possible historical rule
changes. There is no exchange-calendar validation, persistent ingestion service, raw-file parser, market data,
alpha estimate or source-vintage proof. Q006 must specify calendar and decision-time rules independently.
