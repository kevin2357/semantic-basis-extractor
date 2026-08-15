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
- Kevin approved Slice 2. Committed and pushed it as `64aba07`; Slice 3 began.
- Added public `deny_providerless_actions()`. It uses one locked preflight, stages
  one batch record, dispositions every member in memory, persists one native
  revision, promotes one shared artifact, and publishes one validated snapshot.
- Added exact digest-keyed replay verification against the complete request,
  durable artifact, snapshot, and every action-local batch reference. Changed,
  reordered, or partial requests are not replay and fail closed normally.
- Tests prove two terminal actions transition together, positive authorization and
  unrelated action evidence remain, accepted delivery bytes do not change, exact
  replay is byte-stable, and the public operation exposes no provider parameter.
- Focused batch tests passed all 11 tests. The complete repository suite passed all
  289 tests in 122.062 seconds.
- Slice 3 is complete and paused at its review gate. Exhaustive interrupted-write
  recovery is intentionally reserved for Slice 4.
- Kevin approved Slice 3. Committed and pushed it as `166b177`; Slice 4 began.
- Added failure injection after artifact staging, state/projection persistence,
  artifact promotion, and snapshot publication. Restart safely reruns before native
  mutation, narrowly completes the exact known write set after mutation, or replays
  after a completed snapshot.
- Added constrained recovery checks for exact request/digest, result revision,
  action-local batch references, artifact content, and allow-listed changed paths.
  Missing/changed staged or promoted artifacts and unrelated workspace bytes fail
  closed without snapshot blessing.
- Added deterministic batch-versus-batch and batch-versus-single contention. Both
  competitors receive typed exclusivity refusal while the lock holder applies the
  complete batch; no split action state is observed.
- Focused batch tests passed all 14 tests. The complete repository suite passed all
  292 tests in 114.603 seconds.
- Slice 4 is complete and paused at its review gate. The evidence explicitly avoids
  claiming filesystem-wide or external-provider transactionality.
- Kevin approved Slice 4. Committed and pushed it as `d230dc0`; Slice 5 began.
- Added the `deny-providerless-batch` CLI operation, wired approved ordered
  per-action/batch/replay/refusal events, extended installed smoke to cover legacy
  single denial plus two-action batch/replay, and expanded the API handoff with
  exact integration and migration rules.
- Added consumer tests for the documented batch CLI and event tests for ordering,
  replay suppression of duplicate action transitions, bounded refusal diagnostics,
  redaction, and sink-failure isolation.
- Focused batch/consumer/event/contract tests passed all 39 tests. The complete
  repository suite passed all 294 tests in 124.812 seconds.
- Built a temporary 0.4.0 source-checkpoint wheel, installed it into a fresh venv
  outside the repository, and passed lifecycle smoke from `site-packages` with the
  two-action batch and replay. The installed CLI lists the batch subcommand and all
  four batch fixtures are packaged.
- Slice 5 is complete and paused at its review gate. The temporary wheel is
  qualification evidence only and was neither promoted nor published.
- Removed the external temporary wheel/venv tree after retaining compact hashes and
  installed-runtime evidence; no qualification build tree remains in the repository.
- Kevin approved Slice 5 and reported that the AstroWoof API agent also considers
  the completed consumer surface sound. The Slice 5 consumer gate is complete.
- Committed and pushed the accepted Slice 5 consumer surface as `0c15893`; Slice 6
  began from a clean `main` matching `origin/main`.
- Final focused qualification passed all 39 tests. The complete repository suite
  passed all 294 tests in 149.030 seconds.
- Built two independent wheels from exact commit
  `0c158932a6138051ea6904c515a04fc0ec905635` with fixed
  `SOURCE_DATE_EPOCH=1786805826`; both were byte-identical at SHA-256
  `0bdcb2e1e28f35dc9d922fdfa540aa68768460fcbf4a513f7e97d87520713a5d`.
- The exact wheel contained 82 entries, zero cache/bytecode entries, and all four
  batch fixtures. Fresh installed smoke passed on Windows CPython 3.12 and cached
  Linux CPython 3.11, and installed CLI help exposed the batch operation.
- Produced the final API response with confidence levels and reconciled sprint
  acceptance. The sprint is complete.
- Recommend a separately authorized `0.4.1` patch release so consumers can pin the
  new additive interface. No version bump, tag, promotion, publication, or API pin
  occurred here.
- Removed the final external qualification build/venv tree after evidence capture;
  no temporary artifact tree remains in the repository or retained closeout path.
