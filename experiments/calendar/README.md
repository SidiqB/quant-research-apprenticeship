# Bounded calendar contract audit

Q006a, 28 September 2026. See [the policy](../../data/calendar-and-decisions.md) for source references,
scope and Q006b acceptance requirements. This is a prospective scheduled-calendar fixture with synthetic
decision cases, not market observations, execution evidence or a general calendar implementation.

## Reproduce

```sh
make calendar-audit
.venv/bin/python scripts/calendar_contract_audit.py --output work/calendar-replay.json
make check
```

The versioned JSON fixture explicitly lists all 33 dates from October 29 through November 30, 2026.
It transcribes the bounded 2026 NYSE cash-equity core schedule consulted on September 28, and stores
hand-calculated expected UTC instants. Its metadata identifies the official schedule, source consultation
date, separate trading-day-count source, local decision policy and consulted timezone-rule provenance.
The exact fixture hash is in contract-audit.json. No source webpage hash or exchange release ID is invented.

The diagnostic checks every date, record fields, closure status and expected UTC instant against the
installed America/New_York rules, and November's session count against the official total of 20.
It derives prior listed sessions and durations for review; it exposes no public decision-validation API.
Missing metadata/schema support, external vendor adapters and a production calendar are outside its scope.

## Observed evidence

There are 22 sessions: 21 regular and one early close; 10 weekend days and one holiday are explicit.
A weekday-only November count incorrectly gives 21 rather than 20. All session decisions are 30 minutes
before their core open. Regular sessions last 390 minutes; the early close lasts 210. The prior session
for November 27 is November 25, and for November 30 it is November 27. October 29 has no known predecessor.
The November 2 decision is 14:00 UTC; October 30 is 13:00 UTC. The local policy stays at 09:00.

Tests check a hand-listed weekend set, independently calculated boundary instants, all 22 session
intervals, six corrupted copies (missing/duplicate dates, holiday opened, wrong DST hour, early close lost,
and unexpected fields), and two subprocess replays against archived bytes. The full suite has 292 tests.
The fixture audit fails on each corruption. It does not yet reject user decision timestamps; that is Q006b.

The JSON's explicit calendar facts are not synthetic prices or proof of future realised sessions.
Halts, emergency changes, auction fills, other venues and the empirical 2010-2025 study remain unmodelled.
Timezone metadata records the consulted database; portability checks compare relevant instants rather than
requiring a host's TZif byte hash to match. A rule mismatch needs investigation and versioned correction.
