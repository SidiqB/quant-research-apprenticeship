# Bounded exchange calendar and decision contract v1

Q006a | Recorded 28 September 2026 | Project policy version 1.

## Question and scope

Can the provisional 09:00 New York equity decision coexist with correct session dates, early closes and
UTC timing? Hypothesis: session-date eligibility, information availability and executable market time
are separate predicates. Requiring every decision to fall inside core trading would reject valid pre-open
research decisions; assuming every weekday trades would admit a holiday.

Q005 validates source-clock syntax and chronology. It does not establish whether an exchange has a
scheduled session. This contract supplies a bounded fixture for Q006b, not a production calendar or a
change to observation ingestion. NYSE cash-equity core hours are the reference for this engineering
exercise. The wider provisional NYSE/Nasdaq/NYSE American universe still requires appropriate venue and
security-level evidence before empirical use. Options, extended sessions, auctions, halts and fills are
outside this fixture. Calendar dates are planned exchange facts; decision cases are synthetic scenarios.

## Source, version and reproducibility

Primary sources consulted on 2026-09-28:

- [NYSE Holidays and Trading Hours](https://www.nyse.com/trade/hours-calendars): 2026 holiday column,
  Thanksgiving early-close footnote and NYSE Tape A core-session section.
- [NYSE estimated trading-day counts](https://www.nyse.com/publicdocs/Trading_Days.pdf): the 2026 US
  Cash Equities column gives 20 November sessions, an independent count cross-check.
- [Python zoneinfo documentation](https://docs.python.org/3/library/zoneinfo.html): named-zone conversion
  uses external IANA rules, so calendar-source version and timezone-rule provenance must be separate.

Neither NYSE page exposes a stable release identifier. The source edition is therefore described as
"2026 schedule consulted 2026-09-28", not an invented exchange version or archived source-file hash.
[The fixture](../experiments/calendar/nyse-2026-autumn-v1.json) is our versioned transcription of the
bounded schedule. Its exact bytes are hashed in the diagnostic output and retained in Git. A fixture
hash proves file identity, not exchange endorsement, past publication availability or future certainty.
The original pages are linked, not redistributed. Their schedules remain subject to change.

The local rule database identifies itself as IANA 2026c. The fixture metadata records the consulted
America/New_York TZif SHA-256 separately. It does not bundle that database or require byte-identical
system files elsewhere. Expected UTC instants are explicit fixture values; checks compare them against
the installed rules. A mismatch must be investigated, not silently updated to pass. Preserve old fixture
versions and result hashes when correcting a source transcription or adopting a later exchange notice.

## Fixture boundary and record contract

Coverage is every calendar date from 2026-10-29 through 2026-11-30, inclusive: 33 records. The fixture
contains 22 scheduled sessions (21 regular and one early close), 10 weekend dates and one holiday.
November contributes 20 sessions. October 29 is included to supply the previous session for October 30;
a request needing a session before October 29 must fail for insufficient coverage.

Each record has an ISO date and one status: regular, early_close, weekend or holiday. Session records
also carry explicit expected decision_utc, core_open_utc and core_close_utc instants. Closed dates have
no timestamps; the holiday also has its name. Every date is listed exactly once in ascending order.
The diagnostic validates the fixture's exact bounded rules and fields; it is not a generic vendor parser.
Absence outside coverage means unknown, never "closed" and never permission to extrapolate weekdays.

## Decision, inputs and execution

A policy decision occurs exactly at 09:00:00 America/New_York on a listed session date, including an
early-close date. Normalize any aware input to that zone to identify its local date and clock, and compare
instants in UTC. Reject naive inputs, nonzero fractional seconds, other local times, weekends, holidays,
missing dates and out-of-range dates. Equivalent aware UTC representations are valid. A wrong fixed
UTC hour is not equivalent after a daylight-saving change. These are Q006b implementation requirements.

For session s, let D(s) be the decision, O(s) the scheduled open and C(s) the scheduled close. Let P(s)
be the greatest listed session date strictly before s. Here D(s) < O(s) < C(s). A decision at D(s) is
valid even though it is outside core trading. A generic core-time predicate will use O(s) <= t < C(s),
including open and excluding close. A daily bar labelled at C(s) is still a valid completed-session
summary; its publication need not occur within that half-open interval. Calendar closure must not reject
legitimate after-hours publications or their ingestion.

For daily price/volume features, use only completed sessions no later than P(s). The 20-session liquidity
window means 20 listed sessions, not 20 weekdays or calendar days. Require every needed value and its
publication/receipt evidence; do not pad missing sessions. Eligibility additionally requires
max(publication, receipt) + processing_latency <= D(s), applying existing staleness limits if configured.
Session completion alone does not establish availability. At exact latency equality an input is usable;
any later instant is unavailable. Later revisions cannot change earlier decisions.

Decision validation must not imply execution. The planned same-session execution opportunity cannot
precede O(s); an actual fill still needs an explicit auction/continuous-market model, prices, halts,
liquidity and costs. The half-open core-time predicate is a scheduling convention, not a fill simulator.
Opening and closing auction events require separate modelling; do not infer a fill at either boundary.

## Hand-calculated acceptance examples

| Session | Decision UTC | Core open UTC | Core close UTC | Previous listed session |
|---|---|---|---|---|
| 2026-10-30 | 13:00 | 13:30 | 20:00 | 2026-10-29 |
| 2026-11-02 | 14:00 | 14:30 | 21:00 | 2026-10-30 |
| 2026-11-27 | 14:00 | 14:30 | 18:00 | 2026-11-25 |
| 2026-11-30 | 14:00 | 14:30 | 21:00 | 2026-11-27 |

All times are on the row's date. UTC = New York wall time minus its UTC offset. October 30 uses -04:00;
November 2 and later listed sessions use -05:00. Regular duration is 390 minutes and the early close is
210 minutes. The decision remains 30 minutes before the open. The 25-to-27 November gap is not a missing
trading session; the 27 November bar ends at the early close, not the regular close.

Q006b must test holiday/weekend rejection, exact decision/open/close boundaries and adjacent microseconds,
UTC equivalence, daylight-saving offsets, early-close duration, missing predecessors, insufficient history,
naive timestamps and dates outside the fixture. It must preserve valid 09:00 decisions and leave generic
observation ingestion independent of exchange opening hours. It must not silently fill unknown dates.

## Limits and continuation

This is a prospective scheduled-calendar teaching fixture, not realised evidence that trading occurred.
Emergency closures, instrument halts, historical revisions and the desired 2010-2025 empirical period
are not covered. Two October warm-up dates do not promise 20 prior sessions at every decision. The
bounded audit establishes internal consistency and selected official facts, not full calendar accuracy.
Q006b is next; Q006 remains incomplete until its implementation passes. Q004a access/sample evidence and
Q005b provenance integration still gate empirical research. No user decision is needed for Q006b.
