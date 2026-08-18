# Initial Authoring Pass Concurrent Fan-Out Sprint 3 Log

## 2026-08-18 — Sprint proposed

- Opened the sprint at Kevin's request; no implementation has started.
- Recorded the target as within-run fan-out: one deck-level SBE run owns six
  separately prompted and validated initial passes.
- Distinguished interactive concurrent Response creation from Batch's existing
  one-round/six-member transport.
- Identified the safety-critical implementation seam: prepare and authorize the
  bounded wave, create concurrently, serialize immediate provider-ID persistence,
  detach, then reconcile through fresh short-lived workers.
- Added explicit API review pauses after the baseline, contract freeze, public
  fixture handoff, and final qualification.
- Added the bounded final-QA status-preservation regression discovered in the
  retained Kevin live run.
- Accepted ownership of that defect and the defensive duplicate-selection guard
  from the cost-calibration sprint; the cost sprint now retains only usage evidence.
- No provider operation, source change, schema change, version bump, or release
  action is authorized or performed by this planning slice.

## 2026-08-18 — API planning review incorporated

- API review approved the deck-level run, six-action interactive fan-out, immediate
  provider-ID durability, detach/reconcile, and one-round Batch topology.
- Clarified the all-or-none authorization boundary: the API transactionally owns
  the complete reservation set; SBE requires a complete exact wave envelope and all
  six member authorizations before performing any create.
- Clarified that provider submission is not transactionally atomic. Once creation
  begins, partial known, untouched, or ambiguous outcomes are recorded per action.
- Required Slice 1 to freeze numeric per-create and total submission-cycle limits
  from baseline evidence, with qualification against slowest-create time plus
  bounded overhead rather than six sequential durations.

## 2026-08-18 — Slice 0 complete; awaiting review

- Audited exact interactive, exact Batch, bounded interactive, and bounded Batch
  provider-free submission and reconciliation seams.
- Confirmed exact interactive defaults to six workers but serializes one cache
  warmer when caching is enabled and keeps worker threads polling until completion.
- Confirmed bounded interactive executes all six passes serially.
- Confirmed exact and bounded Batch already use one six-member paid round and one
  provider identity/reservation.
- Measured the retained bounded live run's first-to-sixth provider-ID span at 588
  seconds, with 104–131 second gaps between identities.
- Confirmed the released bounded reconciliation substrate retrieves up to four due
  Responses concurrently without new commitment.
- Ran five focused topology/custody tests; all passed in 8.738 seconds with zero new
  provider operations.
- Ran the complete source suite: 423 passed in 321.471 seconds with 10 expected
  skips and no failures.
- Published the complete baseline and seam recommendation in the Slice 0 result.
- Paused before Slice 1 contract/schema work as planned.

## 2026-08-18 — API Slice 0 review incorporated

- API review approved the baseline and progression to Slice 1.
- Elevated cache-warming into an explicit Slice 1 contract decision. Leading policy
  removes full-response warm-up serialization; any create-only alternative must be
  nonblocking and empirically justified.
- Kept six-create submission fan-out distinct from the released four-retrieval
  reconciliation cap. Six members may reconcile through two short subwaves.
- Clarified immediate durability: each returned provider ID receives its serialized
  ledger/journal write immediately. Only the aggregate wave snapshot/result/receipt
  waits for all create tasks to unwind.
- Reconfirmed the complete-wave API reservation/SBE authorization boundary and the
  bounded final-QA/duplicate-admission scope.

## 2026-08-18 — Slice 1 contract complete; awaiting review

- Published the route-neutral prepared-wave, API authorization-envelope, and wave-
  result proposal identities.
- Froze six creates, 15-second per-create timeout, 20-second provider-I/O wave
  bound, four-at-a-time retrieval, and `no_serial_cache_warmer`.
- Defined one locked native preparation mutation against a shared basis revision and
  zero-create/zero-consumption complete-authority preflight.
- Defined immediate serialized per-ID durability and aggregate publication only
  after all create tasks close.
- Defined provider-bound, authorized-unstarted, ambiguous, and definitively refused
  member outcomes without claiming provider atomicity.
- Preserved existing lifecycle vocabulary, inspection v0.3, and one-reservation
  Batch authority.
- Added strict proposal schema, content-addressed canonical fixtures, and cross-
  document semantic validation tests.
- Strict proposal tests: 8 passed. Related lifecycle/route contract tests: 61
  passed. Provider operations and paid spend: zero.
- Paused before Slice 2 runtime implementation for Kevin/API review.

## 2026-08-18 — Slice 2 complete; awaiting review

- Added the internal transport-neutral `initial_wave` module without switching any
  production route or public API.
- Implemented deterministic exact/bounded wave construction, content addressing,
  fixed timing/cache policy, complete envelope/member preflight, and typed refusal.
- Made complete preflight mandatory inside execution so no internal create path can
  bypass full-wave authority.
- Implemented six-way external create overlap with coordinator-thread-only outcome
  persistence and canonical aggregate ordering.
- During review, corrected an initial all-futures fan-in that delayed persistence;
  the final completion-queue design persists each returned ID while other creates
  may remain active.
- Added conservative unstarted/refused/ambiguous classifications and fail-closed
  handling when create tasks violate the wave deadline.
- New focused tests: 9 passed. Related strict spend/lifecycle/contract tests: 66
  passed. Compile and diff hygiene passed.
- Provider operations, paid spend, production route changes, and public contract
  catalog changes: zero.
- Paused before Slice 3 exact-interactive integration.

## 2026-08-18 — Slice 3 complete; awaiting review

- Integrated the transport-neutral coordinator into fresh exact-Natal interactive
  authoring only; Batch and bounded routes remain unchanged in this slice.
- Added one canonical interactive request builder and proved byte equality with the
  established provider transport payload.
- Added one-revision six-action preparation, aggregate frozen-budget validation,
  complete wave/member authorization preflight, and all-or-none ledger authority.
- Added six create-only Response calls with no cache-warmer wait and no response
  polling in the submission threads.
- Serialized every native mutation and persisted each returned provider ID,
  reconciliation clock, marker, pass state, ledger state, and journal projection
  immediately as creates complete.
- Made recovery reuse durable IDs and fail closed on identity-less `SUBMITTING`
  actions rather than POSTing again.
- Added the public `--initial-wave-authorization` seam and documented the exact six
  ordered member-document requirement.
- Focused integration/coordinator tests: 12 passed. Full exact/coordinator suite:
  96 passed before the final all-or-none regression, which passed in focus.
- Provider operations and spend: zero. Compile and diff hygiene passed.
- Paused before Slice 4 bounded-interactive adoption.
