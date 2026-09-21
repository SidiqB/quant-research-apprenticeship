# Daily and weekly operating procedure

## Daily cycle

1. Work in this repository's main checkout. Inspect Git status, branch, origin, roadmap, backlog,
latest notes, issues (if accessible) and previous validation. Do not absorb unrelated user changes.
2. Acquire the repository run lock; if another session owns it, report contention and leave its files alone.
Use `mkdir .git/research-run.lock` as an atomic lock, record the process/session in it, and remove it on exit.
A stale lock requires checking that its owner is no longer active before removal.
3. Fetch origin and fast-forward main only when clean. Stop on divergence; never force-push or rewrite history.
4. Select the oldest feasible bounded dependency from BACKLOG.md. State the question, hypothesis,
data source/period, metrics and evaluation protocol before implementation. Inspect relevant primary research
or official documentation and cite it. Record why the task follows from previous results.
5. Implement one complete improvement with input validation, tests and reproducible commands. Clearly label
synthetic fixtures; unavailable real data is a blocker to empirical claims, never permission to fabricate data.
6. Run targeted checks and `make check`; run the experiment, inspect results and record failures honestly.
7. Write research_log/YYYY-MM-DD.md and render reports/daily/YYYY-MM-DD-learning-note.pdf using
scripts/render_note.py. Include question, motivation, beginner explanation, mathematics, term definitions,
implementation, checks, results, example/chart, limitations, interview explanation, 3-5 questions,
answers in a separate final section and next task. Set Sidiq review status to Not yet reviewed unless
Sidiq has explicitly confirmed a different status. Never infer review from elapsed time or successful tests.
8. Verify PDF text and page bounds using the renderer, render pages with Poppler and visually inspect them.
Use the PDF skill. Regenerate and recheck after changes. Do not claim PDF correctness from file existence.
9. Update roadmap, backlog, changelog and README progress only for actual completed work.
10. Review the complete staged diff for credentials, private contact information, unlicensed data,
large assets and misleading claims. Only stage files from this task. Keep personal email out of file contents;
use the verified account no-reply address in repository-local Git configuration.
11. Commit only meaningful validated work. Push main without force only when authentication and network
permit; verify the remote commit. If push fails, retain the local commit and report the exact blocker.
Do not change dates, create empty commits, reset unrelated work or manufacture activity.
12. Brief the user on changed files, checks, result, commit/push state, key lesson and necessary input.
No review approval is needed for ordinary validated daily work. Stop programme execution after 31 December 2026
and request the next programme scope; do not continue an unapproved new direction.

## Weekly synthesis

Sunday at 16:00 Europe/London, use the same lock and clean-checkout rules. Inspect the week's notes,
commits, experiments, failures and test evidence; do not repeat the morning task. Write a weekly Markdown
report and verified PDF under reports/weekly. Cover completed work, concepts learned, positive and negative
results, actual coverage/code-quality evidence, role-skill connections, revision topics and next priorities.
Do not invent a coverage percentage when coverage was not measured. Reorder/split backlog items from findings,
record changed assumptions, and document material direction questions. Validate, commit and push meaningful changes.
If there is no new evidence to synthesise, say so without generating a token commit.

## Runtime requirements

Local scheduled work requires this folder, its environment, the computer and the desktop application to be
available and running. A switched-off machine will not execute these local tasks. Unattended network or filesystem
approvals can block a run; record that condition and do not weaken permissions automatically.
Schedule times follow Europe/London, including the October daylight-saving transition.

## Learning-note renderer

`python scripts/render_note.py INPUT.md OUTPUT.pdf` supports paragraphs, headings, simple pipe tables,
inline code/bold, and `<!-- pagebreak -->`. Equations should use clear ASCII notation or a reviewed image;
unsupported Markdown is rejected where it would silently lose content. All source text is escaped before PDF markup.
