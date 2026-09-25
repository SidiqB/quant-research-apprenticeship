# Daily validation - 25 September 2026

## Scope and findings

Q004 completes the provisional equity universe and public primary-source comparison of CRSP US Stock and
Norgate US Platinum. The source contract distinguishes historical identity, inactive coverage, terminal
proceeds, corporate actions and historical availability from entitlement, local access and permitted outputs.
A new reusable declaration checker requires all eight gates to be verified; public documentation alone
cannot pass. Both candidates remain unverified, with eight blockers each. No licensed data was downloaded,
no purchase or trial was initiated, and no vendor access is claimed.

The separate invented three-holding experiment starts each holding at 100 and ends at 120, 90 and confirmed
zero recovery. Full-population return is -30%; restricting the sample to the two survivors gives +5%, a
35-percentage-point difference. This is an arithmetic counterexample, not an empirical estimate.
No implementation of membership selection, ingestion or trade execution is claimed.

## Verification evidence

| Check | Observed result |
|---|---|
| Checkout and lock | Clean existing main; shared atomic lock acquired with session/time ownership |
| Remote baseline | Approved fetch confirmed local main and origin/main at fab2f76; no divergence |
| Issues | Authenticated read returned zero open issues; credentials not logged or saved |
| Full check | make check passed: 144 Python tests, including 50 new cases |
| Lint / format / types | Ruff passed; 25 files formatted; strict mypy passed for 15 source files |
| C++ | Warning-clean C++17 compilation and existing golden-output comparison passed |
| Dependencies | pip --no-cache-dir check passed; no new dependency added |
| Positive control | Synthetic complete declaration passed |
| Negative controls | 8 gates times 3 non-verified statuses: all 24 blocked; eight missing gates rejected in tests |
| Invalid input | Malformed records, unknown keys, nontext/blank references and invalid statuses rejected |
| Determinism | Reversed input gate order preserves blocker ordering; input record not mutated |
| Experiment replay | Two subprocess runs matched each other and archived JSON byte-for-byte |
| Independent arithmetic | Literal expected -0.30, +0.05 and 35.0 values matched; Decimal used in experiment |
| PDF content | All 9,570 normalized non-whitespace source characters matched extracted text exactly |
| PDF structure | Renderer checked headings, five nonblank pages and text-origin page bounds |
| PDF appearance | All five final Poppler PNGs inspected: readable tables/text, no clipping or overlap |

## Failures and corrections

Restricted fetch failed DNS resolution; an approved fetch succeeded. The first full check found one
101-character string line. Splitting the literal corrected lint without changing the result; the full
suite then passed. Poppler's default font configuration emitted missing-config/unwritable-cache warnings.
A temporary configuration using system fonts and a writable temporary cache eliminated warnings; the final
render log is empty. The initial automatic overflow placed answers alone on page five. An explicit break
before next work now groups next work, questions and answers on the final page; the PDF was regenerated,
text-audited and visually checked after that change. No repository renderer or system configuration changed.
The staged whitespace check found a trailing blank line in the TOML record; it was removed before commit.

## Source evidence and limitations

Primary references and access date appear in data/universe-and-access.md and the teaching note. The official
CRSP product page and legacy data guide establish candidate features, not actual entitlement or compatibility
with a purchased current format. Norgate's FAQ explicitly reports corrections without historical versioning;
its current database alone fails the declared strict vintage requirement. Its EULA constrains redistribution
and post-expiry retention. A private Git repository is not treated as permission to upload vendor content.

The checklist evaluates declared statuses and nonblank references. It does not authenticate the evidence,
read credentials, contact vendors or enforce a downstream ingestion gate. The dated registry is a human
assessment, while gate controls and return arithmetic are explicitly synthetic. An all-verified invented
record is used only as a positive control. No data coverage percentage, backtest performance, timing benefit
or alpha claim is supported by these checks. Personal review remains Not yet reviewed.

## Publication and continuation

All 16 staged files and extracted PDF text were reviewed for secrets, personal contact information,
unauthorized market data, unwanted branding, large assets and unsupported claims. Automated scans flagged
none; all 21 local Markdown links resolve and no staged file exceeds 1 MB. Only Q004 files and progress
updates are staged. The existing repository-local no-reply
Git identity is retained. This is the pre-commit evidence record; actual commit, push/remote verification
and observed CI outcome belong in the final briefing and automation memory.

Q005a is next before ingestion; Q004a tracks actual entitlement and sample verification. Sidiq's existing
licensed access or a source/budget decision is needed only before acquisition, not for the next engineering
tasks. C002 remains Wednesday 30 September. No publication approval or personal review is required to proceed.
Reproduce with make check, make access-experiment and make note NOTE_DATE=2026-09-25.
