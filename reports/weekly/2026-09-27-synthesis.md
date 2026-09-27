# Foundations before performance

Weekly synthesis | 21-27 September 2026 | Q007 | Prepared 27 September

Sidiq review status: Not yet reviewed. Publication is authorised separately.

## Finding and scope

The week established reproducible checks for information timing, label overlap, source integrity,
data-access declarations and timestamp ingestion, plus the first C++ exercise. Six research items
(Q001-Q005 plus Q005a) and C001 are complete. Q006 calendar rules and actual licensed data access
remain open. There is no empirical alpha, market-calibrated execution or option-market result.

This synthesis uses all seven daily notes, their validation records, six experiment result files,
the C++ fixture and ten commits through 5701e70. It consolidates Sunday's ingestion work without
implementing it again. The three September 21 follow-up commits refined role evidence, activated
schedules and added the C++ track; they were not three additional research experiments.

## What actually landed

| Date / commit | Completed work | Decisive evidence |
|---|---|---|
| Sep 21 / 34b1bec | Q001 availability | Final-vintage join wrong at 4 of 6 invented decisions |
| Sep 22 / 981ab66 | Q002 label purging | Retains A,D; removes B,C; overlaps fall from 2 to 0 |
| Sep 23 / 85ca7bd | C001 fixed savings | 1000 at 5%: interest 50.00, balance 1050.00 |
| Sep 24 / fab2f76 | Q003 manifests | Four source hashes match; changed byte rejected |
| Sep 25 / c4c9b41 | Q004 universe/access | Neither candidate admitted; 24 downgrade controls block |
| Sep 26 / 362d52e | Q005a UTC chronology | Future-fold leak fixed; 16 pre-fix failures resolved |
| Sep 27 / 5701e70 | Q005 strict ingestion | Two valid revisions; all eight bad batches rejected |

The other commits are 1ea44bf, b2f1725 and 8e21bdb. Original activity dates and historical notes
are retained. Q003 and Q004 happened later than their original targets because Wednesday became
a C++ slot and the observed fold defect needed its own bounded correction before ingestion.

## The central lesson

A passing component is evidence for its stated contract. It does not validate the next boundary:
correct parsing does not authenticate a release, correct hashes do not establish lawful access,
and correct accounting does not establish a profitable strategy. The week improved those boundaries
by preserving explicit failures and adding independent expected answers.

<!-- pagebreak -->

## Concepts to be able to explain

**Availability:** an observation date describes an economic event; its publication time says when
a version could become known. With decision t, publication a, observation o, latency L and maximum
age M, require a <= t, t - a >= L, and t - o <= M when M is configured. Compare UTC instants.
Choose the newest observation first, then its newest eligible revision. A revision does not reset age.

In Q001 the correct six-day path is missing, missing, 100, 100, 60, 60. Joining the final value 60
onto every earlier date fails four times. This is a constructed failure count, not a measured market
error rate. A fabricated source publication time would still defeat an otherwise correct selector.

**Purging:** a training row can be old while its target needs a future price. For this past-only
holdout starting at a, retain a candidate only when its label end e < a. Equality is removed under
the closed-label convention. The one-row gap removes safe D while leaving unsafe B,C. Purging
removes both unsafe labels, at the cost of reducing training observations from four to two.
It does not make overlapping evaluation outcomes independent or replace uncertainty estimation.

**Fold and gap:** on the London autumn fixture, 01:30 +01:00 is 00:30 UTC and 01:30 +00:00 is
01:30 UTC. Equal clock labels hide 60 elapsed minutes. A fold has two possible instants; a spring
gap has none. Q005a fixes comparisons by converting to UTC; Q005 separately checks that the source
wall fields and explicit offset return unchanged after conversion through UTC into its declared zone.
This distinguishes consistency from truth. The source must still supply the intended interpretation.

The Python datetime documentation and PEP 495 were rechecked for this synthesis. Same-zone
comparisons can ignore fold, and constructing a datetime does not itself reject every invalid local
label. These are the reasons for separate chronology and ingestion contracts, not universal vendor rules.
https://docs.python.org/3/library/datetime.html
https://peps.python.org/pep-0495/

## Important negative results

Q004's invented holdings start at 100 each and finish at 120, 90 and confirmed zero recovery.
The full return is 210 / 300 - 1 = -30%; survivors alone give 210 / 200 - 1 = +5%, a 35-point
difference. Dropping failures changes the population. Missing terminal prices must never be treated
as confirmed zero recovery. These numbers establish arithmetic, not the size or sign of real bias.

The archived CRSP/Norgate assessment admits zero of two candidates: each has eight unresolved
project gates. Public product descriptions did not establish entitlement or audited sample quality.
The September 25 source review also identified a historical-vintage limitation in current Norgate
histories. No source was purchased, downloaded or newly reassessed in this weekly run.

<!-- pagebreak -->

## Actual quality evidence and its limits

| Evidence | Observed result / scope |
|---|---|
| Daily final Python totals | 25, 49, 49, 94, 144, 167, 257; cumulative, not additive |
| Weekly make check | 257 passed; no added tests or production changes this afternoon |
| Ruff / formatting / mypy | Passed; 30 formatted files; 16 strictly checked package files |
| C++ check | Existing executable matches independent expected output |
| Dependencies | pip --no-cache-dir check: no broken requirements |
| Archived experiments | Five scripts replayed twice to scratch; every byte matches |
| Q001 replay | Full-suite artifact test reproduces its archived release schedule |
| Historical strong controls | 100 interval fixtures; 10,800 UTC oracle comparisons; 24 row permutations |
| Code coverage | Statement and branch percentages not measured; no percentage claimed |

The September 21 note reports an initial 21-case core run; its final validation records 25 cases
including artifacts. The unchanged 49 on Wednesday excludes the separate C++ executable check.
The 10,800 comparisons are cases inside an oracle test, not 10,800 additional pytest tests.
Local validation uses the existing Python 3.12 environment on macOS. This run reused the built C++
executable; the daily records separately document warning-clean compilation and a wrong-rate mutation.

At the weekly baseline, authenticated GitHub reads returned zero open issues and a successful
workflow for 5701e70. The workflow configures Python 3.11/3.12/3.13. This observation is tied to that
commit, not a prediction about the new synthesis commit. Publication status is recorded separately.
https://github.com/SidiqB/quant-research-apprenticeship/actions/runs/36303053768

## Failures that changed the work

The important correctness failure was observed on September 22: a later-fold publication entered
an earlier-fold decision. A UTC workaround was documented while C001, manifests and access work
continued. September 26 reproduced 16 failing regressions before correcting availability. September 27
then rejected inconsistent offsets and missing local times, which UTC conversion alone did not settle.

Daily checks also caught long source lines and a type-narrowing issue. They were corrected before
the reported successful runs. Earlier PDFs spilled tables or answers onto almost empty pages;
notes were shortened or given deliberate breaks and inspected again. These are recorded repairs,
not evidence that the first attempts passed. One C++ mutation used 5.0 instead of 0.05 and correctly
failed the output comparison, demonstrating a percentage-unit error rather than general correctness.

This weekly run initially hit restricted-network DNS failure; an approved fetch succeeded and main
was already current. A shell inspection accidentally reused zsh's path variable, causing command lookup
failures in that subprocess; repeating it with a task-specific variable recovered. No project files
were affected. pip disabled an unwritable cache; the explicit no-cache dependency check passed.
The GitHub CLI is absent, so the read-only API check used existing authentication without logging it.

<!-- pagebreak -->

## Employer-skill connections

The stored September 21 cohort contains 49 deduplicated postings across eight firms. It is purposive,
includes junior and senior jobs and is not a census or an eligibility assessment. Python appears in
37 postings, statistics and communication in 29 each, and C++ in 13. These are explicit mentions,
not counts of mandatory requirements. No vacancy availability was refreshed this week.

**Research infrastructure:** the stored AQR data-scientist evidence names validation, Git, PyTest and
CI/CD; Jane Street's research-engineer evidence emphasises reproducibility and research infrastructure.
Manifests, negative controls and source-zone validation supply relevant repository examples. They do
not establish production-scale experience. Sources from the dated cohort:
https://careers.aqr.com/jobs?gh_jid=8088184
https://www.janestreet.com/join-jane-street/apply/7437779002/

**Research judgement and communication:** the changing-universe counterexample and interval proof
show how to explain a failed assumption with a hand-worked example. This is useful preparation for
systematic research and model-validation discussions. There is still no fitted model, uncertainty
estimate, out-of-sample alpha or independent personal reproduction to present as completed evidence.
The stored Citi model-validation role is a future benchmark for accuracy and independent comparison:
https://jobs.citi.com/job/new-york/model-validation-2nd-lod-sr-lead-analyst/287/100430304704

**C++ development:** C001 connects compilation, numeric units and a known-answer check. C002 should
add a reusable function with a declared compounding convention. One fixed example does not demonstrate
low-latency systems, ownership design or performance engineering. The dated IMC role is a skill benchmark:
https://job-boards.eu.greenhouse.io/imc/jobs/4945420101

The role-analysis wording is corrected to distinguish Sidiq's authorised beginner C++ learning track
from replacing research components for speed. Only the latter still needs a measured bottleneck,
a validated reference and evidence of benefit. The employer sample and its historical counts are unchanged.

## What remains unproven

No admitted market dataset, historical receipt audit or verified current-source entitlement exists.
The adapter returns UTC observations without retaining raw source text or zone provenance and checks
duplicates within a batch. Calendar membership, persistent cross-batch uniqueness and vendor-file
integration remain separate work. Named-zone tests rely on installed timezone rules; the dependency
lock does not capture the whole operating system or IANA database. A manifest's four hashes identify
selected files, not a complete environment or authenticated authorship.

No personal review or independent understanding is inferred from automatic test success. Sidiq should
be able to derive one counterexample and reproduce it before describing it as personal interview work.

<!-- pagebreak -->

## Revised priorities: 28 September-4 October

| Slot | Task / dependency | Acceptance focus |
|---|---|---|
| Mon Sep 28 | Q006a, after Q005 | Calendar source, bounded session fixture, 09:00 decision policy |
| Tue Sep 29 | Q006b, after Q006a | Session lookup, holidays, shortened sessions, boundary tests |
| Wed Sep 30 | C002, after C001 | Reusable compounding function, zero cases, invalid inputs |
| Thu Oct 1 | Q008, after Q006b | Hand-check split and dividend total-return arithmetic |
| Fri Oct 2 | Q009a, after Q008 | Historical membership intervals; no current-list filtering |
| Sat Oct 3 | Q009b, after Q009a | Known terminal proceeds versus unresolved exit evidence |
| Sun Oct 4 morning | Q010, after Q009b | Lagged returns invariant to added future observations |
| Sun Oct 4 at 16:00 | Q014 synthesis | Reassess data readiness and conditional phase dates |

These are targets, not promised completion dates. Each is one 45-90 minute daily step; unfinished
work retains precedence and Wednesday keeps its C++ slot. Q011 and Q012 move to October 5 and 6;
Q013 moves to October 8 around C003 on October 7. Q015 onward retains original phase markers only,
with actual dispatch following dependencies. Phase 1's first week now builds synthetic mechanics;
its empirical portion remains blocked. Later phase windows are conditional, not silently compressed.

## Backlog changes and changed assumptions

Q006 is split into a documented calendar/decision contract (Q006a) and implementation (Q006b).
A timestamp can be valid before the exchange opens: the provisional 09:00 New York decision must
be defined separately from regular-session execution. Do not reject it merely for being pre-open
or imply that a decision-time close is an executable fill. Holidays and early closes need source evidence.

Q009 is split into membership intervals (Q009a) and terminal-event treatment (Q009b). The -30%/+5%
fixture shows why population membership and exit proceeds must not be collapsed into one shortcut.
Q004a becomes an explicit parent of Q004a1 entitlement/output permissions and Q004a2 licensed sample
audit. Both remain blocked in sequence; no declared gate becomes verified just because it has a subtask.

Q005b adds provenance retention and a two-batch integration check after Q013, before empirical use.
Q005 remains complete within its in-memory scope. Preserve source hashes, zone, rule version and
duplicate behavior at integration; this split does not authorise a vendor acquisition.

## Input needed from Sidiq

Before acquisition, identify existing licensed access or a source/budget preference; do not send
credentials. If historical vintages are unavailable, should a narrower retrospective study be considered?
That change needs explicit agreement. Also identify the separate finance project mentioned September 21
when convenient. Neither answer blocks the next synthetic step or authorised pushes.

<!-- pagebreak -->

## Revision exercises

1. A value belongs to January 1 but is published January 3 and revised January 5. Explain the value
available on January 2, January 4 and January 6, and why the final-vintage join is invalid.

2. Evaluation starts January 5. Why must a January 2 training label ending exactly January 5 be
removed here? Why did removing the latest training row fail in the eight-row fixture?

3. Map London's two October 25 01:30 labels to UTC. At the later instant, does a first-fold release
meet a 60-minute latency, and can a new revision rescue a 59-minute maximum observation age?

4. What do a matching hash, a valid source-zone round trip and a passing access declaration each
prove? Identify one thing each leaves unproven.

5. Why can the 1000-at-5%-for-one-year C++ fixture not distinguish simple interest from compounding?
State the two-year outcomes and the convention C002 must declare.

## Suggested answers

1. Missing, 100 and 60 respectively. An economic date is not an information-arrival date. The revised
value cannot be supplied to decisions before publication. Adding genuinely future data must not alter
earlier valid snapshots.

2. Under the declared closed-label boundary, the target's last input is not established before the
first evaluation decision. Retain only e < a. Row D is recent but safe; B and C are older decisions
with later endpoints. A fixed row count therefore removed the wrong information in this fixture.

3. The offsets +01:00 and +00:00 map to 00:30 and 01:30 UTC. Exactly 60 elapsed minutes satisfies
the inclusive latency boundary. The observation is still 60 minutes old and fails the 59-minute age
limit even after revision; publication time does not reset economic age.

4. The hash matches selected bytes against a stored digest, not authorship or truth. A round trip
checks clock-rule consistency, not actual publication. A declaration checker validates required
statuses and references, not whether the supplied entitlement or sample evidence is authentic.

5. Both formulas equal P * (1 + r) at one year. At two years, simple interest gives 1100 and annual
compounding gives 1102.50. C002 must declare the period/rate and horizon contract and validate it;
formatting to two decimals does not provide exact decimal-money arithmetic.

## Evidence trail and reproduction

Read research_log/2026-09-21.md through 2026-09-27.md alongside reports/milestone/initial-validation.md
and the six dated validation records. Results are experiments/availability, purging, manifests,
data_access, timezones and ingestion/results.json (each directory contains its own results.json).
C++ evidence is cpp/projects/savings_growth/expected.txt. Role sources and caveats are in
career_research/role_skill_analysis.md and career_research/research_methodology.md.

Run make check and .venv/bin/python -m pip --no-cache-dir check. The five newer experiment scripts
accept --output PATH for scratch reproduction; Q001's artifact test verifies its default result.
Render this report with .venv/bin/python scripts/render_note.py
reports/weekly/2026-09-27-synthesis.md reports/weekly/2026-09-27-synthesis.pdf.
Weekly artifact checks are recorded in reports/weekly/2026-09-27-validation.md.

Programme scope still ends on 31 December 2026. After that date stop and request the next scope;
do not infer permission for a 2027 programme. The existing Europe/London schedule is unchanged.
