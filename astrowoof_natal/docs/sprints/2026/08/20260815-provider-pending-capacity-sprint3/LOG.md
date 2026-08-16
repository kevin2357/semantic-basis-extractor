# Provider-Pending Capacity Release Sprint 3 Log

2026-08-15

- Received the AstroWoof API process-orchestration brief after a two-run staging
  cohort showed remote provider waiting retained scarce API SBE capacity.
- Reviewed SBE 0.4.2 lifecycle inspection, action inventory, interactive Responses
  polling, Batch detach, snapshot publication, local dependency synthesis, and
  fresh-process resume behavior.
- Confirmed that core native state is durable, but the current public projection
  does not distinguish safe local-process release from absence of all native
  continuation. `WAITING_FOR_RESPONSE` currently produces both provider and local
  continuation and public `not_quiescent`.
- Identified bounded poll-once/detach behavior for interactive Responses as the
  main orchestration work beyond an additive schema projection.
- Drafted an eight-slice medium-large SBE sprint with an explicit API review gate,
  one separate API companion sprint, and a shared parallel-cohort qualification.
- No implementation, test mutation, provider operation, build, version bump,
  commit, release, or tag has begun. Status remains proposed for Kevin/API review.
- The API agent approved the overall plan and requested four Slice 1 refinements:
  durable lower-bound `resume_not_before` with typed early `not_due`; native
  custody-retention classification rather than SBE-owned spend exposure; a small
  explicit wall-clock ceiling covering the retrieval HTTP call; and separate SBE
  native versus API operational cohort gates.
- The API agent also cautioned against making Batch, bounded-Natal, and every route
  block the core exact-interactive fix. Kevin and SBE agreed to require the entire
  exact interactive pipeline, including enabled polish/critic/candidate stages,
  while classifying Batch and bounded-Natal explicitly as parity-supported or
  fail-closed/deferred.
- Incorporated all refinements. Kevin approved the revised plan and authorized
  Slice 0. No runtime implementation or provider operation has begun yet.
- Committed and pushed the approved planning package as `1b47808`; Slice 0 began.
- Added a provider-free baseline with three authorized/consumed `WAITING` actions,
  three durable provider Response IDs, parent `WAITING_FOR_RESPONSE` state, and a
  complete valid snapshot.
- Inspection reports provider continuation and blocking local continuation,
  therefore `not_quiescent`, while exposing all three provider identities. It has
  no capacity-release, custody, or next-due projection.
- Fresh-process CLI inspection returned the same provider identities without
  changing any workspace hash. Closeout remained `continuation_required`, listed
  all three action IDs as unresolved, and preserved their provider identities.
- Existing provider regressions prove a pending background Response resumes the
  same attempt through `GET` only and does not consume a retry. Static orchestration
  inspection found no authoritative state intentionally retained only in a worker
  thread after the coordinator returns.
- Focused tests passed all 5 tests. The complete repository suite passed all 313
  tests in 160.785 seconds.
- Slice 0 is complete and paused for review. No production contract, polling
  behavior, provider operation, build, version bump, release, or tag changed.
- Kevin approved Slice 0. Committed and pushed the baseline as `aa65f77`; Slice 1
  began.
- Drafted lifecycle inspection v0.2 with orthogonal execution-capacity and
  provider-custody projections, plus separately versioned frozen reconciliation
  policy and bounded-cycle result contracts.
- Preserved lifecycle v0.1 and existing quiescence semantics. Capacity release
  requires an allowed disposition plus explicit checkpoint safety; absence of v0.2
  always means retain/unknown.
- Proposed durable lower-bound timing, strict nonmutating early `not_due`, bounded
  cycle/HTTP ceilings, native custody-retention wording, exact-interactive
  all-stage coverage, and parity-or-fail-closed secondary-route classification.
- Slice 1 is paused at its required Kevin/API-agent review gate. No packaged schema,
  fixture, runtime polling change, provider operation, build, release, or tag has
  been introduced.
- The API agent conditionally approved the contract and identified an internal
  timing inconsistency. Reduced due actions per cycle from eight to four so one
  four-worker retrieval wave fits within the 20-second cycle and 15-second HTTP
  timeout.
- Accepted durable 15-second deferral for excess due actions without incrementing
  provider-attempt count, immutable stage context, the reviewed backoff sequence,
  strict nonmutating `not_due`, runnable-local-work precedence, v0.2-only capacity
  release, and exact-stage/secondary-route boundaries.
- Added delivery precedence for nonblocking critic/candidate custody: reader
  delivery remains publishable while provider custody and consumer authority are
  retained through bounded reconciliation.
- Published the accepted inspection v0.2, policy v0.1, and cycle-result v0.1 as
  strict packaged schemas with sanitized fixtures. Preserved v0.1 inspection as
  historical and as the unchanged current runtime emission until Slice 2.
- Focused lifecycle-contract validation passed all 19 tests, including frozen
  one-wave timing, strict capacity/custody vocabulary, immutable stage, v0.1/v0.2
  separation, and mutation-free `not_due`.
- The complete repository suite passed all 316 tests in 156.752 seconds. Slice 1 is
  paused for Kevin's gate review; no provider operation, runtime polling change,
  build, version bump, release, or tag occurred.
- Kevin approved Slice 1. Committed and pushed the contract package as `513614f`;
  Slice 2 began.
- Added durable per-action provider reconciliation timing when an interactive
  provider identity is first recorded. Frozen exponential delay is capped at 300
  seconds and rejects backwards attempt timestamps.
- Promoted public lifecycle inspection to v0.2 and derived execution capacity,
  checkpoint safety, earliest due time, bounded next-action ordering, immutable
  stage, provider custody, and consumer-authority retention from native bytes.
- Preserved fail-closed behavior for legacy timing-free provider work, incomplete
  snapshots, absent exclusivity, and ambiguous submission. A stale snapshot can
  never advertise a releasable checkpoint.
- Focused Slice 2 coverage passed 30 tests. The first complete-suite pass ran 320
  tests and found two expected historical v0.1 consumer assertions; both were
  updated to the approved v0.2 contract and the focused rerun passed.
- The corrected complete repository suite passed all 320 tests in 154.782 seconds.
  Slice 2 is paused for Kevin's gate review; no provider operation, build, version
  bump, release, or tag occurred.
- Added an explicit Batch guard so timing-like bytes cannot accidentally claim
  interactive scheduling parity. Focused coverage passed 31 tests and the final
  complete suite passed all 321 tests in 148.808 seconds.
- Kevin approved Slice 2. Committed and pushed durable timing and projection as
  `150d396`; Slice 3 began.
- Added the GET-only bounded reconciliation engine: strict early `not_due`, one
  four-action parallel wave, 15-second per-GET timeout, zero transport retries,
  durable pending/completed/warning timing, response identity validation, private
  completed-response evidence, and typed checkpoint results.
- Added local pass continuation from cached completed evidence. Initial/retry
  reconstruction and QA run without a second GET or POST; reconciliation-only
  spend control prevents a subsequent provider submission.
- Added fail-closed identity-conflict and snapshot-publication behavior. Provider
  custody/authorization/consumption remain intact across ordinary transport
  warnings, while identity mismatch becomes native review.
- Focused Slice 3 coverage passed 17 tests. The initial complete suite passed all
  328 tests in 155.167 seconds before the final parallel/snapshot guard additions.
- The final complete repository suite passed all 330 tests in 156.238 seconds.
  Slice 3 is paused for Kevin's gate review; no provider operation, build, version
  bump, release, or tag occurred.
- Kevin approved Slice 3. Committed and pushed bounded reconciliation as
  `d994a4a`; Slice 4 began.
- Extended bounded reconciliation through exact interactive polish, qualitative
  critic, and qualitative candidate stages. Completed response evidence is
  consumed through each ordinary stage path without another GET or any POST.
- Exact-stage support is bound to the native exact-run schema, interactive service
  level, action stage, and frozen optional-stage enablement. Batch, bounded Natal,
  and disabled optional stages fail closed and cannot advertise capacity release.
- Preserved publishable delivery while a nonblocking critic remains in provider
  custody: local capacity may release, but the exact action continues to require
  consumer authority retention.
- Focused Slice 4 coverage passed all 22 tests in 5.164 seconds. The complete
  repository suite passed all 335 tests in 158.131 seconds.
- Slice 4 is complete and paused for Kevin's gate review. No provider operation,
  build, version bump, release, or tag occurred.
