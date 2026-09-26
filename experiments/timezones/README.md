# Availability across clock changes

Q005a uses invented records at Europe/London 2026-10-25 01:30, once with fold=0
(00:30 UTC) and once with fold=1 (01:30 UTC). No market observation is used.

Run `make fold-experiment`, or use
`.venv/bin/python scripts/fold_experiment.py --output /tmp/fold-results.json`.
The committed results are deterministic under timezone rules matching the explicit offsets above.

The deliberately invalid legacy predicate compares the raw named-zone timestamps and admits the
later publication at the earlier decision. The fixed selector rejects it. Sixty elapsed minutes
satisfy a 60-minute processing latency; a 59-minute maximum age rejects the older observation,
even if a revision has just arrived. Two releases at the two folds are distinct versions, and
value 2 is the later known revision. Local wall-clock subtraction misleadingly reports zero minutes.

Observation timestamps are now stored as UTC. The selector returns the input Observation object;
source zone labels are not retained on it. A timestamp's instant is preserved by astimezone(UTC),
not by replacing its tzinfo. Naive timestamps remain invalid. Resolving an ambiguous source timestamp,
rejecting nonexistent local times, retaining source-zone metadata and validating clock accuracy
are ingestion responsibilities; Q005 will define those policies.

The 23 new tests cover both London and New York clock changes, equivalent zone representations,
UTC duplicate identity, revision precedence, reversed instants and microsecond boundaries.
An independent integer-minute oracle checks 10,800 selection comparisons: 4 transitions x 3 record
representations x 25 decision times x 2 latencies x 3 age limits x 3 decision representations x
2 input orders. This is deterministic correctness evidence, not market coverage or trading performance.

Primary sources consulted 26 September 2026:

- [Python datetime semantics](https://docs.python.org/3/library/datetime.html): identical tzinfo objects
  trigger local comparisons and subtraction; conversion preserves the instant.
- [PEP 495](https://peps.python.org/pep-0495/): fold disambiguates repeated local times;
  constructors do not reject every invalid local timestamp.
- [Python zoneinfo](https://docs.python.org/3/library/zoneinfo.html): named-zone transitions,
  fold-aware conversion and dependency on system IANA data or tzdata.

The original Q001 six-decision artifact remains unchanged. Canonicalization repairs chronology;
it does not establish historical data availability or licensed market access.
