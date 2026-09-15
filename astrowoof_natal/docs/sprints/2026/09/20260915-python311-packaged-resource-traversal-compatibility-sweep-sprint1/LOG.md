# Log — Python 3.11 packaged-resource traversal compatibility sweep

## 2026-09-15 — Sprint initialization

- Read the predecessor API Slice 1 approval and release-block ruling.
- Read Control Room child `astrowoof-api#23` and aligned this sprint to its full
  acceptance criteria.
- Preserved the predecessor's narrow live correction and release block.
- Created the companion background, evidence register, log, and plan.
- Made no change to the eleven inventoried resource call sites.
- Paused at Review Gate A before caller tracing, tests, or implementation.

## 2026-09-15 — Qualification ownership correction

- Removed the companion sprint's redundant candidate-wheel slice.
- Assigned source-tree qualification, static-inventory closure, and exact-commit
  handback to this sweep's final implementation slice.
- Preserved the predecessor live-defect sprint as the sole owner of candidate
  wheel construction, installed-wheel/API gates, and release qualification.

## 2026-09-15 — Slice 0 complete

- Re-ran AST inventory after the predecessor fix: nine explicit variadic calls
  and one starred-component call remain.
- Traced the real source callers and public exports.
- Ran nine representative real accessors with independent resource digests on
  Python 3.11.15 and 3.12.14 from a read-only repository mount.
- Confirmed four namespace-package calls fail on Python 3.11 and succeed on
  3.12.
- Confirmed the generic accessor and five adversarial calls already succeed on
  both runtimes because they use a regular-package `pathlib` traversable.
- Corrected the inherited count: eleven total original shapes included the
  predecessor's now-fixed helper; ten remain, only four requiring changes.
- Made no production or test change and paused at Gate A.

## 2026-09-15 — Gate A approval and Slices 1–2

- API approved repairs only for the four proven namespace-package failures and
  approved the other six calls as no-change controls.
- Chained each affected resource component without changing names, bytes,
  parsing, validation, or failure translation.
- Extended three existing manifested test modules; no manifest change was
  required.
- Focused tests passed on Python 3.11.15 and 3.12.14: 29 tests with 2 optional
  skips on each runtime.
- Final static inventory reports six known-compatible regular-package calls and
  zero unsupported namespace-package paths.
- Owner assigned broad/full-suite and wheel qualification to the predecessor
  release-driving sprint, so neither was duplicated here.
- Prepared the source-only compatibility handback.

## 2026-09-15 — Exact commit handback

- Committed and pushed the qualified four-repair source boundary as
  `235791de` (`fix: support namespace resources on Python 3.11`).
- Recorded its exact two-runtime focused evidence and returned release-gate
  ownership to the predecessor sprint.
- Companion sprint complete; no wheel or release action occurred here.
