# Validation - 22 October 2026

Task L002b specifies one delayed-order contract. Synthetic whole-unit examples only; no C++
event component or generic timing proof is claimed. Primary sources, question, hypothesis,
protocol, arithmetic, costs and limitations are in the teaching note and event_contract.md.

Six hand-authored examples match the separate per-share Decimal reference exactly. Outcomes:
filled 693/6, unresolved 800/4, exact-cash fill 0/6, insufficient-cash rejection 106/4,
no-order 800/4 and position-cap rejection 800/9999. The decision state is unchanged in each.
Only accepted fills charge the fee 3. Ten invalid traces reject with intended diagnostics;
five corrupt tables reject premature debit, fee on missingness, invented old-price fill,
fee on rejection and trade without request. Two result executions are byte-identical.
A real Python -O invocation refuses to run. Final Ruff lint and formatting pass. Initial
long-string lint and subsequent format failures were corrected; no runtime arithmetic failure.

Current shared make check passes 608 Python tests, Ruff/59 files, mypy/21 files and all existing
C++ checks including boundary and fresh-accounting reproduction; pip consistency passes.
Existing standard Make binaries are reused, while relevant verifiers compile temporary drivers.
The pending contract/reference is checked separately, not in tracked Make checks or remote CI.
No dependency, market sample, alpha result, measured coverage percentage or review status added.

The four-page PDF passes renderer headings/origins, exact normalized source/text comparison
(10372 characters), and visual inspection of every final Poppler page. No layout defects;
empty final rendering log. Existing writable font configuration used. No PDF revision needed.
QA evidence is under work/run-2026-10-22/. Final content scans include pending files and PDF text.

Today's draw of one is allocated to the separate October 18 weekly integration. This complete
lesson remains ignored under work/pending/2026-10-22/, with an integration manifest and truthful
local progress. Next learning is L002c, the bounded C++ component; inspect this pending package
before dispatch. October 20 L002a is also pending. No October 21 lesson package was found.
L002d-f, C003b/C004/C005, Q011/Q012/Q013 and Q004a/Q005b remain. Personal review: Not yet reviewed.
