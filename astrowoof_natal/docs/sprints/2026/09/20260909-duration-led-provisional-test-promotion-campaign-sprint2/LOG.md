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
