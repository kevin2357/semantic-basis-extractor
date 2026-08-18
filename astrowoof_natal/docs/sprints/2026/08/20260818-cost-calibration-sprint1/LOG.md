# Cost Tracking and Estimation Sprint 1 Log

## 2026-08-18 - Sprint opened for discovery

- Created the sprint directory without starting implementation.
- Recorded the present SBE commitment/settlement behavior and the existing native
  and API persistence boundary in `BACKGROUND.md`.
- Captured a candidate append-only calibration projection, stable cohort/version
  identity, evidence-basis rules, adoption sequence, and unresolved questions.
- Added an introductory `PLAN.md` that deliberately contains no slices or approved
  implementation scope.
- No source, schema, migration, runtime, spend-policy, or release behavior changed.

## 2026-08-18 - Bounded live-run finding added

- Recorded the retained SBE 0.4.6 six-pass interactive bounded-Natal run as
  discovery evidence: all six passes accepted on attempt one with USD 1.9539225
  estimated initial-authoring cost.
- Recorded the cross-pass deterministic QA failure caused by equivalent Mean Node
  and True Node claims producing nine duplicate normalized body passages.
- Identified that shared status recomputation overwrites bounded
  `FINAL_QA_REQUIRES_REVIEW` with `AUTHORING_COMPLETE` after persistence.
- Added future implementation and regression requirements for final-QA status
  precedence, suppression of optional paid work behind the QA gate, and a
  fail-closed SBE equivalence check that preserves SPC's upstream ownership.
- Preserved the diagnostic workspace under `.runs`; no source behavior or paid
  provider state was changed.
