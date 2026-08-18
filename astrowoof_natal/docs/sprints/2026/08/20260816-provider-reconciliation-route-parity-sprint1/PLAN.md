# Provider Reconciliation Route Parity Sprint 1 Plan

Date: 2026-08-16  
Status: SBE-native implementation and API consumer review complete  
Implementation: Slices 0-7 complete; release authorized separately

## Purpose

Extend SBE 0.4.3's provider-pending capacity-release contract beyond exact-Natal
interactive Responses work to the two production routes deliberately deferred by
the prior sprint:

1. exact-Natal Batch authoring; and
2. bounded-Natal interactive authoring.

Bounded-Natal Batch remains explicitly unsupported and fail-closed. This sprint
does not create a bounded Batch adapter.

The outcome is route parity at the public lifecycle boundary, not identical
provider mechanics. Exact Batch must reconcile durable Batch/File artifacts using
Batch APIs; bounded interactive must reconcile durable Response IDs using its
bounded route and artifact rules. Both must expose the same safe scheduling,
custody-retention, checkpoint, and terminal/review vocabulary wherever those
semantics are truly equivalent.

## Starting point

SBE 0.4.3 already provides:

- lifecycle inspection v0.2 with orthogonal execution-capacity and provider-
  custody projections;
- durable `resume_not_before` lower-bound advice;
- a strict, nonmutating early `not_due` result;
- one bounded four-action interactive retrieval wave with a 15-second per-request
  timeout and 20-second nominal cycle ceiling;
- exact-Natal interactive continuation across initial authoring, creative retry,
  polish, critic, and qualitative candidate stages;
- durable snapshots, single-writer mutation, provider-ID reconciliation, and
  fail-closed ambiguity/review handling; and
- installed Python/CLI/schema/event consumer surfaces.

The prior release intended to classify exact Batch and bounded Natal as
`unsupported_retain_capacity`. Slice 0 confirmed exact Batch does fail closed, but
also found that real bounded runs share the exact run `schema_version` and carry a
separate `route_contract`; the 0.4.3 predicate checks only the former. Bounded
interactive therefore accidentally inherits exact-interactive scheduling
eligibility before it has a supported route adapter. Correcting that route binding
is an early requirement, not a reason to broaden the existing generic path.

The underlying routes are nevertheless durable:

- exact Batch persists prepared input JSONL, uploaded File ID, Batch ID/status,
  request membership, output/error File IDs, downloaded JSONL, and per-pass
  ingestion state;
- bounded interactive persists paid-action bindings, Response IDs, route-local
  provider results, stage progress, validation evidence, optional-stage state,
  delivery, and workspace snapshots.

The work is therefore an integration and hardening sprint, not a pipeline rewrite.

## Scope and route matrix

| Route | Transport | Sprint disposition | Required stage coverage |
|---|---|---|---|
| Exact Natal | interactive Responses | Existing supported baseline; regression only | Initial, creative retry, polish, critic, candidate |
| Exact Natal | Batch | Add supported parity | Initial and creative retry Batch rounds; subsequent optional stages follow their frozen supported transport |
| Bounded Natal | interactive Responses | Add supported parity | Initial, creative retry, polish, critic, candidate |
| Bounded Natal | Batch | Explicitly deferred and fail-closed | None; no Batch submission or capacity-release claim |

Exact Batch authoring and optional-stage transport must be described precisely at
the Slice 1 gate. The existing runner batches initial/retry authoring while polish,
critic, and candidate use their established provider paths; the plan will not
mislabel those later operations as Batch merely because the run began in Batch
mode.

## Non-goals

- Implementing bounded-Natal Batch submission or claiming Batch pricing for it.
- Replacing the exact and bounded authoring pipelines with one generic pipeline.
- Building an API queue, scheduler, worker lease, or capacity allocator.
- Owning API reservations, quotas, circuit breakers, entitlements, billing, or
  literal dollar exposure.
- Cancelling provider work or introducing provider-side idempotency claims.
- Changing semantic-basis selection, bounded epistemic policy, card schemas, or
  editorial quality policy.
- Making paid provider calls during development or qualification without a later,
  separate authorization.

## Contract principles

1. **One public lifecycle meaning, route-specific adapters.** Capacity,
   custody, timing, checkpoint, and outcome vocabulary should remain shared.
   Retrieval and ingestion remain explicitly Responses- or Batch-specific.
2. **Durable identity prevents resubmission.** A known Response ID or Batch ID is
   retrieval-only. SBE never submits replacement work through reconciliation.
3. **Provider custody is not local capacity.** A complete, valid, writer-free
   checkpoint may release a worker while the API retains authority for exact
   provider-bound actions.
4. **SBE does not claim financial authority.** SBE reports action IDs and custody
   classifications. The API alone decides reservations and dollar exposure.
5. **Early resume is harmless.** A cycle attempted before the durable lower bound
   returns typed `not_due`, performs no provider call, and creates no checkpoint.
6. **Bounded work stays bounded.** The cycle has a frozen action/round limit,
   retrieval timeout, and wall-clock policy. Excess due work receives durable
   non-immediate advice rather than spinning.
7. **Local work is exhausted before detach.** Completed provider evidence is
   ingested and all deterministically unblocked local work runs before another
   capacity-release checkpoint is advertised.
8. **Delivery and custody remain orthogonal.** A nonblocking critic/candidate may
   remain in provider custody after publishable delivery without holding a worker,
   while its API authority must remain retained.
9. **Ambiguity and conflicts fail closed.** Missing/changed provider identity,
   mismatched Batch membership, malformed output, stale snapshots, unsafe writers,
   and incomplete route bindings cannot advertise release eligibility.
10. **No accidental bounded Batch support.** The unsupported combination remains
    rejected in construction, inspection, reconciliation, CLI, schema examples,
    and installed-wheel tests.

## Expected contract decisions for Slice 1 review

Slice 1 must freeze or explicitly reject these details before runtime changes:

1. Whether inspection v0.2 can represent Batch custody without a schema revision,
   and the exact immutable projection for Batch round, stage, and action members.
2. Whether the existing cycle-result v0.1 remains sufficient or needs an additive
   version for mechanism-specific evidence such as `batch_id`, output-file custody,
   and ingested request IDs.
3. A frozen Batch polling schedule and per-cycle ceiling consistent with a short
   worker claim. A Batch cycle should normally retrieve at most one due Batch
   round, because one round can represent many paid action members.
4. The exact distinction between Batch-level provider custody and its member paid
   actions; action IDs remain the consumer authority keys.
5. How input File upload without a durable Batch ID is classified. It is not safe
   provider-pending capacity-release evidence and must remain local continuation or
   ambiguity according to actual provider guarantees.
6. Terminal Batch states and handling of output/error File download, malformed or
   partial JSONL, unknown/duplicate `custom_id`, provider failure, expiry, and
   cancellation.
7. Bounded interactive route/stage binding, cached-response location, and local
   continuation evidence for every enabled stage.
8. Whether one route-neutral dispatcher is added to the public Python/CLI surface
   or existing commands gain explicit supported-route selection. No caller should
   need to inspect private `run.json` to choose safely.
9. Compatibility behavior for retained 0.4.3 workspaces that lack route-parity
   timing. Legacy state must fail closed unless a narrowly proven, deterministic
   migration can add timing without changing provider or semantic evidence.

## Authority boundary

SBE remains authoritative for:

- native workspace bytes, route identity, state revision, snapshot validity, and
  single-writer mutation;
- provider-operation identity and native action membership;
- whether a provider operation is safely retrieval-only;
- due-time recommendation, bounded native retrieval, result ingestion, local
  continuation, and native terminal/review state; and
- the exact action IDs whose provider custody remains unresolved.

AstroWoof API remains authoritative for:

- job leases, queues, worker slots, admission, and retry scheduling;
- PostgreSQL state and HTTP status;
- cross-run reservations, account quotas, global circuit breakers, product
  entitlements, and billing reconciliation; and
- deciding how long to retain consumer authority after reading SBE evidence.

API transition-oracle and QA-render evidence are companion validation, not SBE
authority and not substitutes for native tests.

## Slice 0: Baseline and route inventory

### Outcome

Record reproducible provider-free baselines for exact Batch and bounded
interactive waiting states before changing contracts.

### Work

- Trace exact Batch preparation, File upload, Batch creation, detach, retrieval,
  output/error download, per-request ingestion, retry preparation, and snapshot
  ordering.
- Trace bounded interactive initial/retry/polish/critic/candidate submission,
  identity persistence, route-local resume, validation, optional-stage skipping,
  delivery, and snapshot ordering.
- Create compact scripted fixtures for one detached Batch round and one bounded
  Response-pending action without making provider calls.
- Capture current lifecycle inspection, closeout, resume, and CLI behavior,
  including exact Batch's intentional `unsupported_retain_capacity` result and
  any discrepancy in the real bounded-route classification.
- Identify all state that is native authority versus derived observation.

### Tests

- Snapshot-valid fresh-process inspection and resume baselines.
- Hash-before/after proof that inspection is nonmutating.
- Known-ID no-resubmission regressions for Batch and bounded interactive.
- Full repository baseline.

### Gate

Both omitted routes have deterministic, reviewable fixtures and a complete state-
transition inventory. No production contract or behavior has changed.

## Slice 1: Contract freeze and API review

### Outcome

Freeze the route-parity semantics before schemas or runtime behavior change.

### Work

- Resolve every contract decision listed above.
- Publish a route/transport/stage truth table covering capacity disposition,
  custody, due timing, local continuation, optional delivery, terminal failure,
  ambiguity, and review.
- Define Batch round-to-action membership and per-cycle evidence.
- Define bounded interactive cached-result and continuation evidence.
- Specify exact compatibility and fail-closed behavior for 0.4.3 workspaces.
- Prepare concrete Python, CLI, inspection, event, and result examples.
- Obtain Kevin and API-agent review before implementation.

### Tests

- Review exact JSON examples and closed vocabularies against the current strict
  contract boundary. Because Slice 0 changed the proposed route shape, encode and
  validate new strict schemas/fixtures at the start of Slice 2 after approval,
  before runtime dispatch changes.
- Run current lifecycle contract, invalid-combination, and bounded-Batch rejection
  regressions unchanged.

### Gate

Kevin and the API agent approve the contract, timing limits, migration posture,
and route matrix. Runtime implementation remains paused until approval.

## Slice 2: Route-aware lifecycle projection and dispatch

### Outcome

Make lifecycle inspection and reconciliation dispatch route-aware without
weakening the exact-interactive 0.4.3 contract.

### Work

- Extract only the shared custody/timing/checkpoint decisions needed by all
  supported routes; keep provider mechanics in route adapters.
- Project eligible exact Batch and bounded interactive provider work into strict
  inspection v0.3 native-route, provider-mechanism, custody, and separate
  consumer-authority contracts.
- Add supported route dispatch that does not require consumers to read private
  state.
- Preserve exact-interactive behavior byte-for-byte where its contract is
  unchanged.
- Keep legacy or malformed state `unsupported_retain_capacity`/review as approved.

### Tests

- Exact-interactive golden regressions.
- Provider custody versus billing-reconciliation-pending consumer-authority tests;
  unavailable terminal usage must never become reported zero usage.
- Exact/Batch/bounded route matrix and dispatcher tests.
- Early `not_due`, stale snapshot, absent exclusivity, writer contention, legacy
  timing, ambiguity, and bounded-Batch refusal.
- No provider call during inspection or classification.

### Gate

Only explicitly supported route states can advertise safe capacity release, and
the dispatcher cannot route an unsupported workspace into provider activity.

## Slice 3: Exact-Natal Batch bounded reconciliation

### Outcome

Reconcile one due exact-Natal Batch round in a short, retrieval-only worker cycle
and detach or continue from one coherent checkpoint.

### Work

- Add durable timing when a Batch ID becomes authoritative.
- Retrieve only known Batch IDs through a small frozen timeout and zero submission
  path.
- Persist Batch status/request counts and terminal object evidence.
- On completion, safely download and validate output/error files, enforce exact
  `custom_id` membership, ingest each response once, settle native actions, and
  run newly unblocked QA/retry/local continuation.
- If another Batch round requires external authorization or submission, stop at
  that existing boundary; reconciliation never creates it.
- Preserve one run-level due recommendation for a round with many action members.
- Persist excess/remaining due advice without immediate-spin behavior.

### Tests

- Pending, completed, failed, expired, cancelled, and transport-warning Batch.
- Multi-member completion, partial errors, reordered JSONL, missing/unknown/
  duplicate `custom_id`, mismatched Batch ID, and missing output file.
- Initial authoring and creative-retry rounds.
- Crash injection after retrieval, terminal-object persistence, output download,
  member ingestion, local continuation, state persistence, and snapshot publish.
- Fresh-worker restore, concurrent resume/single-writer contention, replay, and
  proof of zero File upload/Batch create/Response POST.

### Gate

A durable Batch ID can be polled and ingested exactly once without a resident
worker or any submission route; unsafe Batch evidence fails closed with intact
custody and snapshot evidence.

## Slice 4: Bounded-Natal interactive reconciliation

### Outcome

Provide the same bounded worker-release/resume semantics for the complete bounded
interactive pipeline.

### Work

- Attach durable reconciliation timing to bounded paid actions when Response IDs
  become authoritative.
- Retrieve known bounded Response IDs through the approved GET-only adapter.
- Persist completed raw response evidence before route-local interpretation.
- Re-enter bounded orchestration from cached evidence and exhaust validation,
  retry preparation, optional-stage progression/skipping, and delivery work before
  detach.
- Cover initial authoring, creative retry, polish, critic, and qualitative
  candidate stages under frozen generation-profile rules.
- Preserve bounded claim authority, four-context provenance, provider-minimized
  disclosure, selected evidence, disposition, and delivery schemas.

### Tests

- Every bounded stage pending/completed/failed/transport-warning matrix.
- Accepted and rejected initial attempts, creative retry, all optional stages,
  disabled stages, optional budget skip, and delivery-complete nonblocking custody.
- Multiple due bounded actions and mixed completed/pending outcomes where native
  state permits them.
- Provider-ID conflict, cached-response mismatch, invalid editorial output,
  immutable-field reattachment, and provider-disclosure regression.
- Crash injection around retrieval, raw evidence, cards/reports, stage checkpoint,
  delivery, and snapshot publication.
- Fresh-worker restore, concurrent resume, and proof of zero POST/resubmission.

### Gate

Every enabled bounded interactive provider stage can detach and resume safely from
a complete checkpoint while preserving bounded semantic and provenance authority.

## Slice 5: Public interfaces, contracts, events, and handoff

### Outcome

Ship route parity through supported installed consumer interfaces.

### Work

- Update public Python and CLI entry points, strict schemas, fixtures, resource
  catalog, typing surface, and installed lifecycle smoke.
- Emit redacted, failure-isolated route/mechanism observations only where useful;
  events remain non-authoritative.
- Document exact Batch and bounded interactive scheduling sequences, custody
  mapping, timing, errors, replay, and cleanup restrictions.
- Publish a compatibility/migration note and explicit bounded-Batch deferral.
- Provide API transition-oracle fixture inputs and a companion adoption checklist.

### Tests

- Consumer-shaped Python and CLI tests using installed public surfaces only.
- Strict result/inspection/event schema validation and resource enumeration.
- Event ordering, redaction, replay, and sink-failure isolation.
- `py.typed` and public type-checker packaging regression.
- 0.4.3 exact-interactive consumer compatibility.

### Gate

The API can schedule either new route from installed contracts without parsing
private state, and unsupported bounded Batch cannot be mistaken for parity.

## Slice 6: Cross-platform, cohort, and API companion qualification

### Outcome

Prove native route parity under fresh workers and prepare evidence for the API's
separate operational qualification.

### Work

- Run provider-free exact Batch and bounded interactive cohorts through detached,
  not-due, due, partial-progress, and terminal/review cycles.
- Mix exact interactive, exact Batch, and bounded interactive workspaces to prove
  no hidden resident-process or cross-run dependency.
- Exercise the API transition oracle against sanitized SBE fixtures.
- Exercise API QA rendering only where output artifacts change and visual evidence
  adds value; lifecycle correctness remains artifact/schema based.
- Build a reproducible wheel and run clean Windows/Linux Python 3.11 installed
  smokes.
- Compare eventual completed artifacts against blocking-mode/scripted baselines.

### Tests

- Deterministic-clock parallel cohort and fresh-worker restore.
- Concurrent claim and stale-checkpoint races.
- Full route/stage/failure matrix from prior slices.
- Complete repository suite, fixed-epoch double build, wheel content inspection,
  `pip check`, installed Python/CLI/type/resource smokes, and diff hygiene.

### Gate

SBE proves all three supported route/transport combinations can release and
reclaim native worker capacity safely. The API companion gate separately proves
its queue slots and reservations behave correctly; SBE makes no API capacity or
financial claim.

## Slice 7: Closeout and release recommendation

### Outcome

Lock evidence, obtain consumer review, and recommend or withhold the next pinnable
patch.

### Work

- Record commands, test counts, hashes, source commit, compatibility, and zero-
  provider evidence.
- Publish the final API response, route support matrix, adoption checklist,
  limitations, and bounded-Batch deferral.
- Reconcile plan, log, slice results, consumer documentation, contract catalog,
  and release guidance.
- Remove temporary qualification trees and verify a clean repository boundary.

### Gate

Every exit criterion passes and Kevin/API review has no blocker. Version bump,
tag, and publication require separate explicit authorization.

## Sprint-wide testing and gating strategy

1. Use scripted transports with durable fake Response, File, and Batch IDs plus
   deterministic clocks. No real provider operation is authorized.
2. Validate closed truth tables for route, transport, stage, capacity, custody,
   timing, checkpoint, optional delivery, terminal, ambiguity, and review states.
3. Prove submission methods are unreachable from reconciliation with call counters
   and failure sentinels.
4. Inject failures at every provider-evidence/state/snapshot ordering boundary.
5. Test exact replay, fresh-process restore, stale observations, concurrent writers,
   and multiple provider-pending workspaces.
6. Run focused tests at each slice, then the complete repository suite.
7. At every gate: inspect the complete diff, run `git diff --check`, update
   `LOG.md`, add a compact result document, link plan/log/evidence, and pause for
   approval before committing.
8. Require API review at Slice 1 and final closeout. Use the API transition oracle
   as companion evidence without transferring native authority.
9. Require reproducible wheel contents and Windows/Linux Python 3.11 installed
   smokes before recommending release.

## Exit criteria

The sprint is complete only when:

1. exact interactive remains fully compatible and supported;
2. exact Batch initial/retry work has durable due advice, retrieval-only bounded
   cycles, exact member ingestion, local continuation, and safe detach;
3. bounded interactive supports initial, retry, polish, critic, and candidate
   reconciliation under its frozen profile;
4. bounded Batch remains explicitly rejected and cannot advertise worker release;
5. every known provider identity is reconciled rather than resubmitted;
6. early `not_due` is strictly nonmutating and provider-free;
7. completed evidence and all newly unblocked local work are checkpointed before
   capacity release;
8. ambiguous, conflicting, malformed, legacy-unsafe, stale, and incomplete states
   fail closed;
9. provider custody and API authority-retention action IDs survive worker release,
   without SBE claiming reservations or dollar exposure;
10. delivery-complete nonblocking provider work remains publishable while custody
    is retained;
11. public Python, CLI, schemas, events, typing, fixtures, catalog, and installed
    smoke expose the approved contract;
12. mixed-route fresh-worker cohorts pass without a resident-process dependency;
13. API transition-oracle companion evidence accepts the published fixtures;
14. the complete suite and reproducible Windows/Linux wheel qualification pass;
15. documentation clearly states the bounded-Batch deferral and API-owned gates;
    and
16. no provider operation or paid spend occurred unless separately authorized.

## Review posture

This document creates the sprint boundary only. No runtime implementation, test
mutation, provider operation, version bump, build, tag, or release begins until
Kevin approves the plan. Slice 1 additionally pauses for API-agent contract review.
