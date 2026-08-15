# Atomic Providerless-Denial Batch Lifecycle Sprint 1 Log

2026-08-15

- Received the AstroWoof API request after paid two-slot qualification exposed a
  sequential-mutation lifecycle seam.
- Reviewed the existing public lifecycle plan, single-action negative-
  authorization implementation, CLI, contracts, tests, and consumer handoff.
- Confirmed the observed stale refusal is the intended result of binding two
  sequential mutations to one original observation; this sprint proposes a new
  batch boundary rather than weakening stale-observation protection.
- Drafted the sprint plan, semantic decisions, slices, testing ladder, gates, and
  honest multi-file atomicity boundary.
- No implementation, test execution, provider call, build, commit, tag, or release
  has begun. Status is `proposed`, pending Kevin's review.
- Kevin approved the plan. Committed and pushed the planning package as `92cebbc`;
  Sprint 1 entered `in_progress` and Slice 0 began.
- Added a provider-free regression baseline shaped like the API observation:
  terminal accepted delivery plus two independently eligible authorized,
  unconsumed creative-retry actions. It asserts first denial application, exact
  replay, stale refusal for the second action when the original observation is
  reused, zero mutation on that refusal, and unchanged delivery bytes.
- Slice 0 focused qualification passed all 12 negative-authorization tests. The
  complete repository suite passed all 275 tests in 114.487 seconds.
- The baseline establishes that terminal `DELIVERY_COMPLETE` and providerless
  eligibility can coexist in current SBE. The seam is observation granularity,
  not terminal-state rejection, provider behavior, or delivery mutation.
- Slice 0 is complete and paused at its review gate. No batch contract or
  implementation has begun; no provider operation or paid work occurred.
- Kevin approved Slice 0. Committed and pushed it as `8442aa3`; Slice 1 began.
- Added strict v0.1 batch request/result schemas, a 32-member bound, canonical
  ordered request hashing, closed batch/per-action outcomes, four sanitized
  fixtures, contract-catalog entries, and a batch-level execution-event contract.
- Documented terminal-delivery support, all-or-none semantics, exact replay,
  provider-safety precedence, single-action compatibility, and the API review
  questions in `results/SLICE 1 CONTRACT.md`.
- The first full-suite run exposed the expected catalog synchronization guard: the
  new event name was present in the vocabulary and packaged catalog but absent from
  the code-owned required-payload map. Added the matching three-field definition;
  this was a contract-wiring omission, not a runtime mutation issue.
- Focused contract/event tests then passed all 21 tests. The corrected complete
  repository suite passed all 278 tests in 108.805 seconds.
- Slice 1 is implementation-complete and paused at its planned API-agent contract
  review gate. No lifecycle mutation function, CLI operation, provider call, or
  paid work was introduced in this slice.
- AstroWoof API-agent review approved Slice 1 without requested contract changes:
  the fixed 32-action bound, result/release mapping, exact observation-timestamp
  replay binding, `eligible` versus `not_evaluated`, provider-safety precedence,
  and initial/replay event policy are all accepted. An optional bounded batch-level
  refusal event is useful diagnostically but remains non-authoritative.
- The API will release nothing for a refused batch and will retain exact request,
  digest, per-member evidence, outcome, and shared checkpoint as audit/recovery
  provenance. Slice 1's consumer gate is complete.
- Committed and pushed the API-approved Slice 1 contract as `e2f31ac`; Slice 2
  began.
- Implemented strict batch request validation plus a one-lock, read-only preflight
  that evaluates every requested action against one native state, inspection, and
  validated snapshot. The helper returns resolved ordered actions only when every
  member passes, otherwise a typed all-or-none refusal.
- Added provider-free coverage for success, stale observation, mixed ineligibility,
  duplicate/unknown/binding mismatch, provider evidence and ambiguous submission,
  snapshot invalidity, lock contention, and programmer misuse. Each normal refusal
  proves authoritative workspace hashes are unchanged.
- Focused batch/contract tests passed all 21 tests. The complete repository suite
  passed all 285 tests in 119.423 seconds.
- Slice 2 is complete and paused at its review gate. The preflight remains internal
  until Slice 3 can expose a complete supported mutation/replay operation.
