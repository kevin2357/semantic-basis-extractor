# Native Terminal Transition Journal Sprint 1 Plan

Date: 2026-08-17
Status: in progress; Slice 2 complete and awaiting Kevin review
Implementation: Slices 0-2 complete; provider-bound integration not started
Upstream consumer sprint: AstroWoof API Sprint 26, Native Terminal Transition
Ingestion

## Purpose

Close the native handoff gap exposed by the retained Aster qualification route.
SBE durably entered `FAILED_REQUIRES_REVIEW`, but the API observed the nonzero
command exit before ingesting a validated native terminal result and reclaimed the
job. Later provider work could then occur beneath the same logical paid-action
identity.

This sprint gives SBE one compact, versioned, append-only transition and provider-
operation journal plus a native execution result published through a fail-closed
multi-file protocol before command exit. The API can validate and archive that
evidence before applying any generic subprocess fallback. Existing lifecycle
inspection v0.3 and reconciliation-cycle result v0.2 remain compatible projections
of the same native truth.

The historical Aster records remain untouched. This sprint produces a provider-free
reproduction and prevention contract, not a retroactive repair.

## Ownership boundary

SBE owns:

- native state/revision and complete workspace snapshot authority;
- route, mechanism, stage, action binding, and provider-operation evidence;
- append-only native journal ordering and integrity;
- terminal/review interpretation and execution-result publication;
- provider-safe replay, refusal, and fixture generation; and
- packaged schemas, public readers, CLI output, documentation, and smokes.

The API owns:

- PostgreSQL transition/provider-operation persistence and atomic ingestion;
- leases, queue claims, capacity, reservation, quota, and billing authority;
- terminal-first worker classification before exit-code fallback;
- provider-operation cardinality enforcement in API authority;
- transition-oracle evolution and QA worker integration; and
- reader/publication state and cleanup of API/R2 test residue.

SBE never writes AstroWoof PostgreSQL. Logs and lifecycle events remain diagnostic,
redacted, failure-isolated, and non-authoritative.

## Frozen safety direction

The initial contract work will formalize these API-recommended decisions:

1. Append one compact journal record per durable native transition or provider-
   operation observation; retain full workspace snapshots separately.
2. Provide no automatic recovery from `FAILED_REQUIRES_REVIEW`. A future recovery
   model must use explicit new action/operation lineage and authorization.
3. Preserve Aster as forensic history; do not mutate or backfill its records or
   costs.
4. Use an atomic publication protocol for journal/result evidence and the state and
   snapshot boundary it describes, before returning or raising across the public
   command boundary. No individual multi-file write is claimed to be atomic: a
   result is visible and valid only when its journal range, snapshot identity, and
   hashes validate together; interrupted partial publication fails closed.
5. Treat a second provider operation for the same action as refusal unless an
   explicit, versioned supersession relationship is supported. This sprint does
   not invent such a recovery relationship merely to permit continuation.

Slice 0 pauses for API review of the reproduction and crash-window inventory before
contract freeze. Slice 1 then pauses for API review before schemas or runtime
behavior are implemented.

## Contract requirements

### Journal

The journal will be a bounded-authority append-only artifact with:

- explicit schema and journal versions;
- run ID, monotonically increasing sequence, SBE record ID distinct from any
  provider external operation ID, and prior-record hash;
- native state revision and complete snapshot identity;
- `observed_at` timestamp and closed observation kind/outcome vocabulary;
- immutable route family, provider mechanism, native operation, stage, and exact
  action binding where applicable;
- provider operation identity and state observations without treating a local
  deterministic key as provider idempotency;
- submission boundary, identity-recorded, terminal result/failure, cost basis,
  versioned price/usage evidence reference, ambiguity, and predecessor/supersession
  fields as applicable;
- terminal/review transition evidence with machine-readable status and cause; and
- release/resource/profile/contract identities needed to validate the producer.

Payloads must be compact, provider-visible data must not leak into the journal, and
large/raw responses remain referenced immutable workspace artifacts rather than
embedded blobs.

### Native execution result

Every supported ordinary authoring and neutral reconciliation invocation will leave
one immutable, versioned, independently identified result artifact published
through the fail-closed protocol, describing:

- invocation identity and journal range/digest;
- pre/post native revisions and snapshot identities;
- validated route/mechanism/operation identity;
- closed outcome: delivery, review terminal, supported terminal failure,
  provider-pending, continuation, external-authority wait, ambiguity, or malformed
  / unavailable native evidence;
- exact provider-operation and action references relevant to the invocation;
- capacity/custody/consumer-authority projections where applicable; and
- whether generic subprocess fallback is permitted because no valid terminal native
  result exists.

The result is native evidence, not an API scheduling or PostgreSQL mutation command.
Exit codes remain secondary observations. A mutable `latest` pointer/index may be
offered only as a derived operator convenience; it is never authoritative and never
the sole API ingestion target. Replay/idempotency binds the immutable invocation-
result identity, journal range/digest, and native run identity.

### Compatibility

- SBE 0.4.4 inspection v0.3 and reconciliation-cycle result v0.2 remain accepted
  and retain their current meaning.
- New journal/result schemas become the required boundary for terminal-first API
  ingestion after consumer adoption.
- Legacy workspaces without the new complete evidence fail closed for the new API
  transition path; they are not silently synthesized into authoritative history.
- Exact Responses, exact Batch, and bounded Responses are supported. Bounded Batch
  remains rejected.

## Slice 0 — Baseline and Aster-shape reproduction

### Outcome

Freeze current behavior and produce a provider-free reproduction showing exactly
which durable evidence is absent or insufficient at the ordinary-command boundary.

### Work

- Trace ordinary exact/bounded authoring and neutral reconciliation exits through
  state write, snapshot publication, public state, lifecycle inspection, result,
  event, and CLI exception/exit handling.
- Inventory every provider submission/identity/result persistence boundary and
  terminal/review transition.
- Build a sanitized Aster-shaped fixture: provider operation observed, native
  `FAILED_REQUIRES_REVIEW`, nonzero command exit, and hypothetical generic reclaim.
- Record which facts are authoritative artifacts and which were historically only
  reconstructable from logs.

### Tests

- Existing lifecycle, spend, reconciliation, terminalization, snapshot, and CLI
  suites.
- A provider-free characterization test that demonstrates the missing ingestible
  terminal execution result without weakening current safeguards.

### Gate

The defect shape is reproducible without OpenAI or historical mutation, and all
affected write/exit boundaries are enumerated before contract design. Pause for API
review: confirm that the observed missing facts and irreducible crash windows are
the exact problem Slice 1 must contractually solve.

## Slice 1 — Cross-repository contract freeze

### Outcome

Publish the smallest strict journal and execution-result proposal and obtain API
agent acceptance before implementing schemas or runtime writes.

### Work

- Freeze closed record kinds, outcomes, cause codes, route/mechanism/stage/action
  binding, provider-operation shape, cost dispositions, and terminal semantics.
- Require each provider observation to carry a distinct SBE record identity,
  closed observation kind, `observed_at`, and versioned price/usage evidence
  reference when an amount is reported; raw provider bodies/prompts remain private.
- Bind actions to the frozen request and generation-profile digests. Provider
  external ID remains absent before identity recording and is never fabricated from
  a deterministic local key.
- Specify sequence/hash integrity, idempotent replay, cursor/range ingestion,
  compaction/retention posture, and maximum bounded record sizes.
- Specify the atomic publication protocol, validation/visibility rule, write
  ordering, and irreducible crash windows. Do not claim literal filesystem,
  cross-process, or provider atomicity across the mutable state, journal, snapshot,
  and result files; every incomplete combination must fail closed.
- Define exact API accept/refuse mappings, including terminal-first precedence,
  malformed evidence, stale revision, gaps, forks, duplicates, and unsupported
  legacy workspaces.
- Reconcile the proposal with inspection v0.3, cycle result v0.2, lifecycle events,
  spend ledger, denial terminalization, and provider reconciliation.
- Keep supersession unsupported in this sprint. The schema may represent an
  explicit predecessor/supersession reference for future evolution, but a second
  distinct external provider ID for one action is refused now.

### Tests

- Schema examples and cross-repository fixture validation only.
- Closed truth tables for terminal/review/pending/continuation/ambiguity/malformed
  outcomes and provider-operation cardinality.

### Gate

Kevin and the API agent approve the contract. Both repositories can distinguish
`FAILED_REQUIRES_REVIEW` from subprocess failure and can prove that one provider
operation cannot silently replace another.

## Slice 2 — Journal schemas, integrity, and public reader

### Outcome

Implement the versioned append-only native journal as a strict packaged contract.

### Work

- Add schemas, contract-catalog identities, typed Python records/results, and
  sanitized canonical fixtures.
- Implement deterministic record identity, sequence, prior-hash chaining, journal
  digest, crash-safe append publication, strict validation, and single-writer
  enforcement.
- Add a public read/validate API that returns one specified immutable invocation
  result and its bounded journal evidence without exposing private mutable
  internals. Any latest index is explicitly derived/non-authoritative.
- Define snapshot membership and restoration behavior so incomplete, forked,
  truncated, additional, or changed journal evidence cannot resume or ingest.

### Tests

- Empty/initial journal, ordered append, exact replay, duplicate ID, sequence gap,
  hash fork, truncation, corruption, stale writer, concurrent writer, relocation,
  and schema/size-limit cases.
- Package-resource and `py.typed` checks.

### Gate

The journal is deterministic, append-only, snapshot-bound, independently
validatable, and available from the installed public package.

## Slice 3 — Provider-operation observation integration

### Outcome

Every paid-operation lifecycle boundary appends durable evidence without replacing
earlier provider-operation history.

### Work

- Journal prepare/authorize/consume, submission-started, provider-ID-recorded,
  pending retrieval, completed/failed/cancelled/expired result, reported or
  unavailable usage, ambiguity, and provider-safety refusal.
- Cover initial authoring, creative retries, polish, critic, candidates, exact
  Batch rounds/members, and bounded Responses.
- Bind every operation to the exact action/request digest and journal the closed
  cost disposition while leaving account-wide billing authority to the API.
- Reject a conflicting second provider identity/operation for one action unless it
  is exact replay of already durable evidence.

### Tests

- Route/stage matrix, exact replay, conflicting IDs, duplicate callbacks, missing
  usage, Batch member integrity, ambiguity, and single-writer races.
- Failure injection before/after provider call, identity persistence, journal
  append, state write, and snapshot publication. No live provider call.

### Gate

Native state preserves append-only provider-operation history, and no supported
path can silently overwrite or resubmit an action after durable provider evidence.

## Slice 4 — Terminal transition and execution-result publication

### Outcome

Ordinary authoring and reconciliation commands publish validated terminal/native
results before returning or raising, making native meaning primary to exit status.

### Work

- Journal delivery, `FAILED_REQUIRES_REVIEW`, budget exhaustion, policy stop,
  provider terminal failure, ambiguity, provider pending, and local continuation.
- Atomically publish the invocation result with its journal range, state revision,
  snapshot identity, and lifecycle projections.
- Route both ordinary exact/bounded command execution and neutral provider
  reconciliation through the same result-finalization boundary.
- Ensure error formatting or CLI exit conversion occurs only after durable result
  and snapshot publication.
- Keep optional-stage skip distinct from required-stage terminal failure.

### Tests

- Delivery, review terminal with nonzero exit, provider failure, pending detach,
  malformed result, external denial terminalization, and exact replay.
- Failure injection at journal/state/result/snapshot ordering boundaries and fresh-
  worker recovery after every durable cut.

### Gate

A `FAILED_REQUIRES_REVIEW` workspace contains a complete validated terminal result
before command exit; a consumer needs neither stderr nor text logs to classify it.

## Slice 5 — Consumer fixtures, CLI/Python surface, and handoff

### Outcome

Give the API a packaged, route-neutral ingestion boundary and canonical fixtures
for its persistence and worker slices.

### Work

- Expose typed public inspection of a specified immutable invocation result and its
  journal range. Any latest-result lookup is a derived convenience only.
- Add a neutral CLI inspection/export mode that performs no provider work or native
  mutation.
- Publish exact Responses, exact Batch, and bounded Responses fixtures for
  delivery, review terminal, provider failure, pending, ambiguity, malformed
  refusal, replay, and conflicting second-operation refusal.
- Publish API mapping, atomic-ingestion expectations, cursor/idempotency guidance,
  backward compatibility, redaction, and recovery limitations.
- Update lifecycle smoke, contract catalog, event catalog, and installed-resource
  assertions.

### Tests

- Strict Python/CLI/schema parity and fixture round trips.
- Provider-call sentinels prove read/export cannot submit, retrieve, or authorize.
- Consumer examples validate from an installed wheel outside the checkout.

### Gate

The API can implement Sprint 26 Slices 2 and 4 without parsing private run state,
stderr, or logs and without forking SBE orchestration. Pause for API review and
explicit fixture-contract acceptance before Slice 6 joint qualification begins.

## Slice 6 — Cross-platform and cross-repository qualification

### Outcome

Qualify the SBE artifact and support the API's provider-free Aster-shaped seam test.

### Work

- Run the full SBE suite and fixed-seed route/stage/failure matrices.
- Build twice at a fixed epoch and inspect wheel contents.
- Run clean Windows and Linux Python 3.11 installed Python/CLI/resource/type smokes,
  recording exact available platform versions truthfully.
- Validate packaged fixtures against the API ingestion/oracle consumer when its
  companion slices are ready.
- Support the API QA test while preserving ownership: SBE validates native
  evidence; API proves transaction, terminal-first classification, no re-lease,
  slot release, PostgreSQL/R2 cleanup, and no second provider operation.

### Tests

- Provider-free exact-Response Aster-shaped end-to-end fixture.
- Contract parity for exact Batch and bounded Responses without route inference.
- Concurrent/fresh-worker replay, interrupted persistence, and immutable snapshot
  restore.
- `pip check`, installed lifecycle smoke, diff hygiene, repository cleanliness,
  zero-provider proof, and zero durable QA residue assertions.

### Gate

SBE's artifact is pinnable and the joint provider-free trace is explainable from
durable records alone. API operational claims are reported only from API-owned
evidence.

## Slice 7 — Closeout and release recommendation

### Outcome

Lock evidence, obtain final API consumer review, and recommend or withhold the next
pinnable SBE patch.

### Work

- Record source commits, schemas, fixture hashes, commands, test counts, platform
  versions, wheel hashes, provider-operation count, and spend.
- Publish final API response and adoption checklist, including known limitations
  and any irreducible provider/filesystem atomicity gaps.
- Reconcile plan, log, evidence, results index, contract catalog, consumer docs,
  compatibility, and release guidance.
- Remove temporary qualification trees and verify a clean repository boundary.

### Gate

Every SBE-native exit criterion passes and Kevin/API review has no blocker. Version
bump, tag, and publication require separate explicit authorization.

## Sprint-wide testing and gating strategy

1. Provider-free first: scripted transports use durable fake Response, File, and
   Batch IDs. No OpenAI operation is authorized by this plan.
2. Model closed truth tables before implementation; reject unknown values rather
   than treating them as retryable.
3. Exercise exact Responses, exact Batch, and bounded Responses at every applicable
   boundary. Keep bounded Batch rejected.
4. Inject failures around every state/journal/result/snapshot write and every
   provider submission/identity/result boundary.
5. Test exact replay, stale observations, journal forks/gaps, concurrent writers,
   fresh-process restore, and malformed consumer inputs.
6. Run focused tests at each slice and the complete suite before qualification.
7. At every gate update `LOG.md`, `EVIDENCE.md`, and one compact result document;
   link the complete plan/log/evidence/results set and pause for approval before
   committing.
8. Require API review after Slice 0, at the Slice 1 contract freeze, after the Slice
   5 fixture handoff, and at final closeout.
9. Require fixed-epoch reproducible builds and installed-wheel smokes before a
   release recommendation.

## Exit criteria

The sprint is complete only when:

1. ordinary authoring and reconciliation both publish the new native result;
2. terminal/review evidence is durable before subprocess exit handling;
3. journal records are append-only, ordered, hash-linked, snapshot-bound, and
   strictly validated;
4. every provider operation remains visible beneath its exact paid action;
5. conflicting second operations are refused unless exact replay;
6. inspection v0.3 and cycle result v0.2 remain compatible projections;
7. exact Responses, exact Batch, and bounded Responses pass; bounded Batch rejects;
8. stale, malformed, incomplete, forked, ambiguous, and legacy-unsafe evidence
   fails closed;
9. events/logs are unnecessary for correctness and remain non-authoritative;
10. public Python/CLI/schema/fixture/type/resource surfaces work installed;
11. the API can atomically ingest terminal truth before generic exit fallback;
12. the provider-free Aster-shaped route cannot be reclaimed for a second provider
    operation;
13. API and SBE evidence preserve their separate authority boundaries;
14. the complete suite and cross-platform reproducible-wheel gates pass;
15. historical Aster records remain untouched; and
16. provider operations and paid spend remain zero unless separately authorized.

## Review posture

This document creates the SBE sprint boundary only. No runtime implementation,
schema mutation, provider operation, version bump, build, tag, or release begins
until Kevin approves the plan. API-agent pauses are mandatory after Slice 0, after
Slice 1, after Slice 5, and at Slice 7 closeout.
