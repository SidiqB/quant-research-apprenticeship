# Versioned experiment provenance

Q003 asks whether an archived result can be bound to declared source bytes and a written protocol.
The hypothesis is that unchanged sources verify, while missing required metadata and a one-byte change fail.
This is a synthetic engineering audit, not a market-data study or preregistered performance experiment.

Run `make manifest-experiment` and `make check`. The experiment checks four files pinned in
`purging-v1.json`: Q002's archived synthetic result, fixture generator, splitter and dependency lock.
It rejects four missing-metadata cases and a one-byte change in a temporary copy. The originals are untouched.
The JSON output is deterministic; the regression compares two runs with the checked-in result.
To reproduce Q002 independently, run `make purging-experiment`; its result must still match the archived hash.

## Schema version 1

The top-level keys are exactly `schema_version` (integer 1), `experiment_id`, `data_kind`, `question`,
`hypothesis`, `information_period`, `evaluation_protocol`, and `sources`. Text fields must be nonblank;
`data_kind` is `synthetic` or `real`. Mixed datasets must be separated into explicit records for now.
Each source contains exactly `path` and `sha256`. Source paths are unique, normalized relative POSIX paths;
source digests are 64 lowercase hexadecimal characters. At least one source is required.

`load_manifest` rejects duplicate JSON keys. `validate_manifest` checks metadata without file access.
`verify_sources(manifest, root)` separately resolves paths beneath the supplied root, requires regular files,
and compares exact byte hashes. Missing sources, directories, escaping symlinks and mismatches fail.
`manifest_bytes` emits sorted-key, two-space-indented ASCII JSON with a final newline. Object-key order is
normalized; source-list order remains meaningful. This is a project encoding, not universal JSON canonicalization.

## Interpretation and maintenance

Hashes identify declared byte content, including whitespace and line endings; they do not prove authenticity,
licensing, absence of leakage, a complete dependency graph, or empirical validity. The synthetic classification
and protocol are authored assertions. Files must remain quiescent while verified; the resolver is not a
security boundary against a concurrently hostile filesystem. A party able to replace both manifest and data
can replace both hashes and contents. There is no signature or remote timestamp.

The manifest records Q002 retrospectively on 24 September. Its dependency lock describes declared packages,
not a captured operating system, compiler, hardware or fully isolated environment. The archived result includes
its own fixture rows. Four declared files are verified; whole-repository closure is not claimed.

A changed pinned source intentionally fails the provenance regression. Investigate before changing a hash.
For intentional research revisions, retain the previous experiment via Git history and add a new versioned
record with a distinct ID and documented reason; never silently refresh hashes to make a failing audit pass.
Historical records can be verified against their corresponding Git checkout. Schema changes require explicit
version support; schema version and experiment version are different concepts.

## Sources

- [Python hashlib](https://docs.python.org/3/library/hashlib.html): binary file hashing and SHA-256.
- [Python json](https://docs.python.org/3/library/json.html): duplicate-key handling and serialization controls.
- [W3C PROV overview](https://www.w3.org/TR/prov-overview/): provenance concepts; this small schema is not a PROV implementation.
