# Daily 0-3 commit draw

Requested 4 October 2026; applies to scheduled runs from 5 October. Today's existing research commit
and this explicit replanning task are not rewritten to fit a number retrospectively.

After acquiring the shared research lock, run `.venv/bin/python scripts/daily_commit_budget.py`.
It draws uniformly from 0, 1, 2, 3 once per Europe/London date and saves the draw inside .git.
Retries and the weekly run reuse the same draw. Never redraw to obtain a preferred result.
Record the draw, completed commit hashes and actual count in the daily briefing and automation memory.
Before committing, inspect today's real Git history and both run memories to calculate remaining slots.
The cap is shared across morning and weekly runs, not a separate draw per automation. Do not change timestamps.

Aim for that many independently meaningful, validated commits when such units are actually ready. Treat
it as a ceiling, not a requirement to manufacture changes. One coherent change stays together with its tests
and explanation. Never create empty commits, split a file or documentation mechanically, or relabel old work.
Report fewer commits honestly if there are fewer completed units, validation fails, or publishing is blocked.
Maintain the same slow learning workload on a three-commit day; available previously completed units can
be committed only after their current validation and provenance have been checked.

On zero days, continue reading, hand calculations, experiments and teaching material in ignored
work/pending/YYYY-MM-DD/, including the learning note and verified PDF where productive. Do not alter
tracked files merely to leave a dirty checkout. Keep a manifest there listing purpose, inputs, checks,
intended destination and original work date. On a later positive day, inspect and validate pending material,
then integrate it with its true work date and current commit date. Do not backdate. For nonzero days with
exhausted slots, use the same pending area for extra reporting, including Sunday synthesis.

On positive days, write the normal research_log and reports paths when publishing the corresponding unit.
A zero-commit day does not remove prior unpushed commits: retry an already authorised validated push and
report that separately from new commits. Never reset existing user changes or stash unrelated work.
This random cadence changes publication timing, not research honesty or the evidence needed for a claim.
