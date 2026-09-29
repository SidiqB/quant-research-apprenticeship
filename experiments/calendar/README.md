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

## Q006b implementation - 29 September

The fixture and Q006a results above are preserved. The new package API in
[calendar.py](../../src/quant_research/data/calendar.py) loads exactly this reviewed fixture version,
checks its SHA-256 and verifies its explicit instants against installed New York rules. It exposes
immutable session values and distinguishes known closure from unknown coverage. This intentionally
bounded loader is not a generic calendar parser; even a formatting-only fixture change is rejected.

```python
from datetime import date, datetime
from pathlib import Path
from quant_research.data.calendar import NyseAutumn2026Calendar

calendar = NyseAutumn2026Calendar(Path("experiments/calendar/nyse-2026-autumn-v1.json"))
session = calendar.validate_decision(datetime.fromisoformat("2026-11-27T14:00:00+00:00"))
assert not calendar.is_core_time(session.decision_at)
assert calendar.session_on(date(2026, 11, 26)) is None
assert len(calendar.previous_sessions(session.day, 20)) == 20
```

session_on requires a New York date, rejecting datetime arguments. validate_decision accepts equivalent
aware instants only at the exact 09:00 local policy time. is_core_time uses the half-open core interval.
Both timestamp APIs identify the date in New York after UTC normalization. Outside coverage raises
CalendarCoverageError, never False/None. previous_sessions requires a covered session anchor and positive
integer count, excludes the anchor and returns exactly that many sessions in ascending order. Insufficient
history raises; the first session's valid decision does not imply any usable prior-session history.

Reproduce with make calendar-experiment, or run scripts/calendar_experiment.py with --output PATH.
[The result](decision-validation.json) accepts all 22 decisions, passes 132 microsecond core-boundary
checks and rejects nine invalid decisions. A core-only decision rule incorrectly rejects all 22.
November 25 has only 19 prior sessions; November 27 and 30 have complete 20-session windows. The
[71 new tests](../../tests/test_calendar.py) also check all 11 closed dates, a hand-listed history
window, input types, timezone equivalence, local/UTC date boundaries, immutable outputs, fixture/rule
mismatch rejection and two byte-identical subprocess replays. All 363 project tests pass.

The API validates scheduling only. It cannot establish observation completeness, receipt times,
source-clock validity or fills. Generic ingestion remains independent of exchange hours; a holiday
publication still passes. Actual data access, broader calendars and provenance integration remain pending.
