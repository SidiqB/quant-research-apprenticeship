# Historical membership intervals

Q009a, 2 October 2026. All identities and dates are synthetic. The fixture covers calendar labels
2026-01-01 inclusive to 2026-01-09 exclusive, not a sequence of verified exchange sessions.
No source acquisition, index replication, performance estimate or empirical claim is made.

## Question and contract

Can effective-date intervals recover past members, including securities absent from a later roster?
Use one history per universe, stable security IDs and intervals `[entry, exit)`: entry is included,
exit is excluded. `exit=None` explicitly asserts continuation through declared coverage. It does not
mean a security will survive forever, and must not be used to fill unknown exit evidence.
A history declares complete membership coverage `[start, end)`; queries outside it fail. An empty
result inside coverage means no members only if the caller's completeness assertion is correct.
The implementation cannot audit that assertion or distinguish an omitted member from a nonmember.

`MembershipInterval` and `MembershipHistory` are immutable. IDs must be nonempty, printable and
contain no whitespace. Dates must be exact `datetime.date` objects: datetimes and strings fail
rather than silently dropping time/zone information. Intervals must be nonempty and intersect
coverage, but may straddle its boundaries. Same-ID overlap and duplicate intervals fail regardless
of input order. Adjacent intervals and re-entry after a gap are valid. Different IDs may overlap.
The history stores a canonical tuple and returns sorted immutable ID tuples.

`members_on(session_date)` operates on already mapped effective dates. It does not validate an
exchange session or decide whether an after-close change applies today or next session. Map source
conventions and decision timestamps upstream using the documented calendar/decision policy.

## Reproduce and evaluate

Run `make membership-experiment`, `make check` and `make note NOTE_DATE=2026-10-02`.
The script also accepts `--output /tmp/membership.json` without changing the archived JSON.

The experiment compares all eight dates with explicit hand sets. OLD exits on January 5 while NEW
enters. RETURN exits January 4 and re-enters January 7. STAY remains throughout. On January 2 the
correct set is OLD, RETURN, STAY. Intersecting it with the January 8 roster wrongly leaves RETURN,
STAY, removing one of three historical members. Copying the final roster directly would also admit
NEW too early. The counterexample measures a selection error, not the direction or size of return bias.

Fifty-five new tests cover endpoints, invalid IDs/dates, coverage, overlap, duplicates, re-entry,
adjacency, immutability and date extremes. A separate entry/exit event ledger agrees on all eight
dates across all 24 orderings of four intervals (192 comparisons). Two subprocess replays match
archived JSON bytes. A future new identity does not change a query before its entry.

## Limits and next work

This is retrospective effective-date membership, not as-known-at membership. Publication times,
revisions, latency and source vintages are absent. Adding a later correction to an earlier interval
can change historical results; a time-varying roster alone does not prove absence of look-ahead.
Stable-ID authenticity, ticker mappings and complete history require upstream evidence. These
synthetic identifiers are not CRSP identifiers, and no CRSP mapping is implemented.

Membership does not imply tradability, data availability or an executable position. Exit neither
sells nor deletes a holding and implies no recovery value. Q009b will model terminal evidence
separately. Q004a access/sample audit and Q005b provenance integration remain empirical gates.
Construction sorts in O(n log n); queries scan all intervals and sort selected IDs. No speed or
coverage-percentage claim, new dependency, ledger or multi-universe API is included.

## Primary sources consulted on 2 October 2026

- [CRSP Research Data Products: PERMNO and PERMCO](https://indexes.morningstar.com/research-data-products/permno): stable security/company identity and changing tickers. The CRSP URL redirected here. This supports using stable keys, not any claim that our fixture is authentic or licensed.
- [Python datetime documentation](https://docs.python.org/3/library/datetime.html#date-objects): date semantics and the datetime/date subclass relationship. Our strict date-only API and half-open boundaries are explicit project choices.

See [teaching note](../../research_log/2026-10-02.md) and
[validation evidence](../../reports/milestone/2026-10-02-validation.md).
