# Weekly validation - 4 October 2026

## Scope and baseline

Q014 synthesises September 28-October 4 after prior weekly commit 8228415. Inspected eight actual
commits through 5d333193ea724b608e95c9bc77bc130e29a9d30d, seven daily notes and validation records,
experiment inputs/results, current source/test contracts, role evidence, operating instructions and
the October 4 curriculum/cadence revision. No morning implementation was repeated.

Worked in the existing local main checkout, initially clean; acquired atomic .git/research-run.lock
with this weekly automation/session identity. Restricted fetch failed DNS; approved fetch succeeded.
Main and origin/main matched with zero commits ahead/behind. No unrelated edits were present.
Repository-local author identity retains the verified account no-reply address.

The authenticated GitHub read returned zero open issues. The initial Python urllib call failed TLS
certificate verification; system curl with certificate checks enabled succeeded using existing Git
credentials in memory, without printing or saving them. Baseline exact-SHA CI run 37204224669 was
completed/success: https://github.com/SidiqB/quant-research-apprenticeship/actions/runs/37204224669 .
This is evidence for the baseline, not the future synthesis commit. Publication/remote verification
and any subsequently observed CI result are recorded in automation memory and the final briefing.

## Executed checks

| Check | Observed result |
|---|---|
| make check | 608 Python tests pass; 66 C++ checks and golden output pass |
| Ruff lint / format | Pass; 49 files already formatted |
| Strict mypy | Pass on 21 package source files; scripts/tests are not all in this scope |
| make -B cpp-check | Both C++17 executables freshly rebuilt with all warning flags as errors; pass |
| pip --no-cache-dir check | No broken requirements |
| Archived JSON replay | Eleven scripts, twice each to ignored scratch; exact archived bytes |
| C++ replay | Two fresh executable runs equal hand-authored expected.txt bytes |
| Manifest provenance | Existing manifest replay verifies the four original Q003 hashes |
| PDF renderer | Seven nonblank pages; headings and text-origin bounds pass |
| PDF extraction | Exact normalized source/PDF equality: 16,601 characters |
| PDF appearance | All seven final Poppler PNG pages inspected; no clipping, overlap or spill page |
| Poppler diagnostics | Empty render log with a temporary writable font-cache configuration |

The morning Q010 note truthfully recorded 602 Python tests. The later authorised curriculum commit
added six commit-budget cases, giving 608 now: four saved/reused outcomes, a new date and rejection
of invalid saved state. These tests do not measure randomness statistically or enforce daily counting.
No budget draw was executed for October 4; COMMIT_CADENCE.md takes effect October 5. This run is one
coherent report/planning unit. Actual hashes/count and push outcome are recorded after publication.

Replay scripts: calendar_contract_audit.py, calendar_experiment.py, corporate_action_experiment.py,
membership_experiment.py, terminal_experiment.py, lagged_return_experiment.py, manifest_experiment.py,
purging_experiment.py, access_experiment.py, fold_experiment.py and ingestion_experiment.py. Each was
invoked with --output under work/weekly-2026-10-04 and compared against its archived JSON. Scratch
outputs and replay hashes remain ignored. The original availability experiment is also exercised
by the passing suite; it was not an extra standalone two-run replay in this weekly check.

No coverage percentage, general mutation score, numerical universality, performance speedup,
empirical return or personal mastery was measured. Tests use bounded examples and independent
oracles; test counts are not market sample sizes. No production code, dependencies or data changed.
The later document-only edits do not alter the validated executable code or existing experiment bytes.

## PDF verification and sources

Applied the PDF skill and successfully invoked its artifact-operation marker before authoring.
Rendered with scripts/render_note.py. Poppler produced seven PNGs at 1400-pixel long edge; inspected
each individually. Source text and equations are ASCII, and table rows/headers are readable.
The initial standalone text comparator removed all pipe characters, including two literal subtitle
separators, so it reported a two-character mismatch. Corrected the comparator to strip pipes only
from table rows; exact equality passed without altering the PDF or dropping content. The report's
first layout passed every-page visual inspection. No PDF failure was concealed by normalization.

Rechecked the official NYSE schedule on October 4: Thanksgiving closure and November 27 early close
agree with the unchanged fixture. AQR and Jane Street role-page refresh attempts were inaccessible;
the report explicitly uses dated September 21 evidence, not current vacancy claims. Other employer
links are carried from that dated source study. Daily source failures and daily implementation/PDF
corrections are attributed to their original notes rather than claimed as new weekly experiments.

## Backlog and retained gates

Marked Q014 Done. Refined October 5-11 to C003a whole-year text parsing, with C003b full CLI deferred
until readiness. Vectors, returns and sample statistics remain explicit C004/C005 carryover; one
bounded concept per day and repeat-before-advance remain the policy. Reconciled current dispatch
references with the authorised curriculum while preserving dated historical evidence. The October 12
ledger slice is conditional on prerequisites; no later completed status or new lesson was invented.

Split deferred Q005b into source/knowledge contract Q005b1 and two-batch adapter Q005b2. Preserve Q013
and Q004a entitlement/sample requirements before empirical use. The contract must cover source bytes,
source zones/rules, identity, effective versus publication vintages, complete terminal proceeds,
interval/reinvestment basis and entitlement versus settled cash. No source acquisition or narrower
historical claim is approved. Personal review remains Not yet reviewed.

The existing weekly automation remains active on Sundays at 16:00 in the Europe/London programme
context; the prompt retains daylight-saving and December 31 stop instructions. No schedule change
was needed. From October 5 the daily/weekly runs share one persisted draw and actual Git count;
zero or exhausted days retain notes/PDFs/manifests under ignored work/pending without tracked edits.

## Final publication audit

Review the complete staged report/planning diff and extracted PDF text before committing. Only this
run's ten report/planning files are intended; no market dataset, credentials, dependency or executable
change. Automated scan totals and link results are recorded below after execution. Standing user
publication authorisation applies; personal review is separate. Never force-push or rewrite history.

Completed staged audit: all ten files and extracted PDF text reviewed. Automated credential/contact
patterns produced no matches; all 43 local Markdown links resolve, every staged file is below 1 MB,
and staged whitespace checks pass. There are no unstaged or unrelated changes. Two actual programme
commits already exist on October 4 (758d9de and 5d33319); this synthesis is the third if committed.
No retrospective random budget is invented. The scan is repeated after this final audit entry.
