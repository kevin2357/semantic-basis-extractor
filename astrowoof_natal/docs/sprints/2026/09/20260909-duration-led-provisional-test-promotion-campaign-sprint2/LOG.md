# Log — duration-led provisional test promotion campaign Sprint 2

## 2026-09-09 — sprint handoff

- Created from Sprint 1's clean Batch 11 completion boundary.
- Inherited live manifest: 78 parallel-safe, 18 provisional, 36 serial-only.
- Inherited paired proof: 625 tests, 49 expected skips, matching inventory,
  outcome, and manifest digests, empty stderr.
- Recorded all 18 provisional modules and the concurrent four-module editorial
  family freeze requirement.
- Began no Batch 12 selection, audit, collision run, or manifest change.

## 2026-09-12 — Slice 0 rebaseline and Batch 12 audit

- Rebased the dedicated `codex/test-suite-promotion-sprint2` worktree onto
  current `main` at `c5e6593` before beginning campaign work.
- Reconciled the current manifest to 81 `parallel_safe`, 18 `provisional`, 37
  `serial_only`, and 12 logging-sensitive modules. The difference from the
  handoff baseline is three already-approved parallel-safe modules and one
  deliberately serial/logging-sensitive operator-disposition reader; the
  provisional inventory remains unchanged.
- Ran the manifest/runner guard: 16 tests passed, including exact-once active
  module classification and secret-environment scrubbing.
- Confirmed that the only provisional tests changed since Batch 11 are the four
  editorial-review modules frozen by the completed packet sprint.
- Refreshed their timings from current source: 39 tests, one expected optional
  schema skip, 20.470863 seconds total, all successful.
- Selected those four modules as coherent Batch 12 and completed their
  state-surface audit. All four may proceed to bounded collision qualification.
- Paused before collision execution and manifest mutation for the planned
  campaign paws-point.

## 2026-09-12 — Batch 12 collision qualification

- Incorporated API's independently authored approval at commit `d51e6d5`.
- Ran the approved three repetitions with two independent copies of each of the
  four editorial-review modules, in waves capped at six child processes.
- All 24 worker receipts passed with exact per-module identities and outcomes:
  `9/0`, `7/0`, `12/1`, and `11/0` tests/skips.
- The only skip was the expected optional-`jsonschema` schema check. There were
  zero failures, errors, expected failures, unexpected successes, unexpected
  skips, nonempty coordinator logs, orphaned Batch 12 children, or repository
  changes.
- Retained raw receipts under
  `C:\tmp\sbe-batch12-collision-20260912` for review.
- Paused for the separate manifest-promotion decision. No classification has
  changed and no actual-manifest stress run has begun.
