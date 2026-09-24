# Daily validation - 24 September 2026

## Scope and observed result

Q003 adds a strict schema v1 experiment manifest and exact SHA-256 source checks. This is a retrospective
provenance audit of Q002's synthetic fixture, not an empirical study or a preregistration claim.
The four declared sources all match: archived result, generator, purging implementation and dependency lock.
Missing data kind, question, evaluation protocol and source hash are rejected. An appended space in a
temporary result copy is detected; tracked originals are unchanged. No dependency was added.

## Checks

| Check | Evidence |
|---|---|
| Checkout and lock | Clean existing main; shared atomic directory lock acquired |
| Origin | Approved fetch succeeded; local and remote both at 85ca7bd before this work, no divergence |
| Issues | Authenticated read returned zero open issues; credentials never displayed or stored |
| make check | 94 Python tests passed; 45 new manifest cases |
| Lint and format | Ruff passed; 22 files formatted |
| Types | Strict mypy passed for 14 source files |
| C++ | Warning-clean C++17 compilation and hand-authored expected-output comparison passed |
| Dependencies | pip check reported no broken requirements |
| Audit experiment | Four sources verified; all four metadata omissions and one-byte change rejected |
| Repeatability | Two subprocess runs matched each other and committed result JSON |
| Q002 replay | Regenerated output matched the archived result byte-for-byte |
| Known-answer test | Exact abc bytes matched independently specified SHA-256 digest |
| PDF content | All source text matched extracted text after markup, footer and whitespace normalization |
| PDF structure | Renderer verified four nonblank pages, required headings and text-origin page bounds |
| PDF visual inspection | All four final Poppler PNGs inspected; readable content and tables, no clipping |

Adversarial cases cover missing/invalid metadata, unsupported versions including bool/float, malformed hashes,
duplicate paths and JSON keys, changed/missing files, directories and escaping symlinks. These tests establish
engineering behavior under the declared contract. No coverage percentage, performance benefit or alpha is claimed.
A checksum does not authenticate an author or validate the meaning of data. Four pinned files are a bounded
source inventory, not the entire dependency graph. Files are assumed quiescent while being verified.

## Failures and corrections

The first restricted fetch failed DNS resolution; the approved network fetch succeeded. Previous local commits
were already present remotely, so no backlog of unpublished commits remained. Initial lint found long lines;
formatting and one explicit string wrap fixed them before the full passing check. pip disabled an unwritable
cache and still completed dependency verification. No installation or permission weakening was needed.

The first PDF had a one-word overflow page. Shortening the final limitations sentence removed that spill.
The final four-page PDF was regenerated, text-audited and visually inspected on every page. The normalized
content contains 9,815 non-whitespace characters and matches the Markdown. Poppler emitted no warnings.

## Publication and next work

The staged diff and extracted PDF were reviewed for credentials, personal contact information, unwanted
branding, unauthorized datasets, excessive assets and unsupported claims. Only this task's files are staged.
The repository-local Git author uses the existing no-reply address. Personal review remains Not yet reviewed.
Publication is authorized separately from review. This is a pre-commit record; the final briefing and automation
memory record the actual commit, remote verification and any observed CI outcome without assuming success.

Run make check, make manifest-experiment and make purging-experiment to reproduce the evidence.
Run make note NOTE_DATE=2026-09-24 to rebuild the PDF. Q004 universe and data access is ready next;
Q005a remains open before ingestion, and C002 stays in the Wednesday slot. No new scope decision is required.
