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

## 2026-08-18 — Slice 4 complete; awaiting review

- Adopted the reviewed six-member coordinator for fresh bounded interactive runs.
- Preserved bounded packet/schema bytes, provider minimization, editorial-only
  response trust, deterministic authority hydration, validation, and provenance.
- Added complete-wave authorization to the bounded CLI with the same one-envelope,
  six-ordered-member all-or-none boundary as exact interactive.
- Added create-only bounded request construction and proved it equals the established
  bounded interactive payload for the same frozen logical pass.
- Persisted every returned ID immediately and detached without polling; existing
  four-at-a-time bounded reconciliation remains unchanged.
- Fixed final-QA status precedence through native/public/snapshot/lifecycle/result/
  receipt evidence.
- Added pre-paid typed rejection of editorially equivalent selected Mean/True Node
  claims plus a nearby non-equivalent admissibility regression.
- Combined bounded/provider-pending/lifecycle suite: 119 passed in 118.177
  seconds. Focused final assertions: 4 passed.
- Provider operations and spend: zero. Compile and diff hygiene passed.
- Paused before Slice 5 Batch compatibility/non-regression.

## 2026-08-18 — Slice 5 complete; awaiting review

- Proved exact and bounded Batch still use one paid round action/API reservation
  containing six logical initial members; neither inherits interactive wave state or
  six-reservation authority.
- Reconfirmed route-local interactive/Batch logical-request parity after only the
  documented provider envelope/background normalization.
- Preserved partial-member failure, pass-local retry, terminal provider failure,
  detach/not-due/reclaim, identity conflict, retrieval-only replay, and final
  assembly behavior.
- Found and corrected exact Batch's mixed-usage asymmetry: one member without usage
  can no longer be normalized into a partial aggregate settlement.
- Exact and bounded Batch now both retain consumer financial authority with
  `provider_usage_unavailable_billing_reconciliation_pending` and a null reported
  amount until API-owned reconciliation.
- Focused authority/request parity: 4 passed. Mixed-usage parity: 2 passed.
  Complete Batch-focused four-route suite: 29 passed in 138.277 seconds.
- Provider operations and spend: zero. Compile and diff hygiene passed.
- Paused before Slice 6 failure atomicity, lifecycle, and transition-oracle work.

## 2026-08-18 — Slice 6 complete; awaiting review

- Added one pre-POST barrier checkpoint: all six actions are durably `SUBMITTING`
  before concurrent provider creates begin.
- Added complete snapshot publication after every serialized returned-ID commit for
  exact and bounded interactive waves.
- Proved a crash after one identity checkpoint resumes with that identity, marks
  five identity-less submissions ambiguous, and performs no duplicate POST.
- Added the exhaustive zero-through-six known-ID aggregate custody matrix.
- Proved six-ID detach releases local capacity until due while retaining all six
  provider-custody and API consumer-authority action IDs.
- Kept the existing public lifecycle/oracle vocabulary unchanged and documented the
  irreducible provider acceptance/identity-persistence atomicity gap.
- Combined wave/bounded/capacity/lifecycle/oracle suite: 99 passed in 104.999
  seconds. Native journal/result/receipt and event suite: 29 passed in 3.339
  seconds. Full exact semantic-closure suite: 90 passed in 172.225 seconds.
- The full exact suite caught and fixed an over-broad review-status preservation
  edge: concrete all-subject delivery evidence may close a reviewed run, while
  generic pass-derived persistence still may not erase final QA.
- Provider operations and paid spend: zero.
- Paused before Slice 7 public interfaces and consumer handoff.

## 2026-08-18 — Slice 7 complete; awaiting API review

- Promoted prepared-wave, complete-authorization, and aggregate-result v1 contracts
  into the packaged contract catalog with strict schemas and fixtures.
- Added root-package provider-free builders, validators, resource readers, and the
  `astrowoof-initial-wave-contract` export CLI.
- Added prepared, authorization, six-ID detach, and partial-ambiguity fixtures plus
  a hash-bound API consumer-review manifest.
- Published the API adoption guide covering complete-wave reservation, runner
  arguments, crash outcomes, lifecycle scheduling, event authority, and interactive
  versus Batch reservation cardinality.
- Revalidated provider-visible minimization and event redaction/closed vocabulary.
- Public consumer/lifecycle/event/disclosure tests: 69 passed. Wave/public/proposal
  tests: 23 passed with eight optional `jsonschema` checks skipped.
- Built and installed wheel SHA-256
  `30b91c0d422e1a1e1fd14e1019cc0b9e4bb33b576f00b071b4cf2ffd3132b583`;
  new CLI, root Python validation, and installed lifecycle smoke passed.
- Provider operations and spend: zero.
- Paused at the explicit API review gate before Slice 8.

## 2026-08-18 — Slice 7 API review accepted

- API approved the packaged schemas/fixtures, public Python/CLI surface, consumer
  manifest, and wave-versus-lifecycle authority boundary for Slice 8/release.
- Clarified that `prepared_wave.run_id` binds to
  `SbeAuthoringRun.native_run_id`, never API `GenerationRun.id`.
- Reconciled the consumer-review manifest to `api_approved`.

## 2026-08-18 — Slice 8 complete; awaiting final review

- Added a provider-free installed-route driver covering exact interactive, exact
  Batch, bounded interactive, and bounded Batch from `site-packages`.
- Added deterministic serial/concurrent timing qualification. Windows measured
  451.7/78.1 ms (0.173); Linux measured 451.1/78.9 ms (0.175).
- Built twice at fixed epoch `1787084172`; both wheels are byte-identical SHA-256
  `0609928cbeef837ac8b718b00217b46203a0ce1c119060d41011190ff2e2479b`.
- Wheel inventory: 821,731 bytes, 114 entries, 67 resources, `py.typed`, no tests,
  no bytecode.
- Windows CPython 3.12.13 and network-isolated Linux CPython 3.11.15 passed exact
  pinned-SPC installation, `pip check`, lifecycle/release smokes, and all four
  installed route modes.
- Full repository suite: 438 passed in 428.516 seconds with 18 expected environment
  skips (456 total). Strict installed contract suite: 41 passed without skips.
- Provider operations and spend: zero.
- Recommend a fresh immutable 0.4.7 after final Kevin/API review and explicit
  release authorization; the 0.4.6-named qualification wheel is not publishable.

## 2026-08-18 — Final review accepted; 0.4.7 authorized

- Kevin and the AstroWoof API agent accepted Slice 8 and the release recommendation.
- Authorized a fresh immutable 0.4.7 version, exact-source reproducible rebuild,
  final installed gates, annotated tag, GitHub publication, and authenticated asset
  verification.
- The retained 0.4.6-named qualification artifact remains evidence only and will
  not be published or substituted for the exact 0.4.7 artifact.

## 2026-08-18 — Exact 0.4.7 artifact qualified

- Exact artifact source commit: `e8f5cd74ef600db27c73f12360ec9ea41539e08d`.
- Two fixed-epoch (`1787085282`) builds were byte-identical: 821,729 bytes,
  SHA-256 `8fd5268e69a64517e82a3c33eda700ceeaf13bb4465a9e3efe91aafafacc4ad8`.
- Wheel inventory: 114 entries, 67 resources, `py.typed`, no tests or bytecode.
- Exact installed Windows 3.12 and network-isolated Linux 3.11 gates passed:
  dependency check, lifecycle smoke, release smoke, all four routes, and timing.
- Provider operations and paid spend: zero.
