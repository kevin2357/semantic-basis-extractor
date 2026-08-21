# Retained Initial-Wave Next-Action Fence Sprint 1 Plan

Date: 2026-08-20
Status: Slice 4 complete; awaiting review before cross-route classification
Starting release: SBE 0.4.13
Expected release: fresh immutable patch version after joint qualification

## Purpose

Close the pre-invocation authority gap exposed by AstroWoof API Sprint 33. SBE
0.4.13 can classify `await_external_authority`, but its lifecycle inspection does
not identify the exact native action inventory that a provider-capable continuation
would consume. A retained run was therefore resumed through a generic path that
prepared and submitted a distinct six-member initial wave before the API could
reject the incompatible publication.

This sprint will add a closed, run-specific external-authority request and bind the
continuation command to that exact request under native single-writer validation.
It will also strengthen initial-wave admission so prior initial-wave/provider
lineage can never be silently reinterpreted as a fresh wave.

## Frozen incident safety

- Aster and its original and duplicate provider operations are evidence only.
- Do not resume, reconcile, authorize, deny, retrieve, cancel, or resubmit Aster.
- Do not edit its API rows, R2 capture, native workspace, or provider identities.
- Reproduce only with generated workspaces and scripted provider transports.
- This sprint does not promise that Aster is recoverable. If its retained native
  evidence cannot prove one exact consumable action inventory, it must remain a
  typed fail-closed review case.

## Ownership boundary

SBE owns:

- native action preparation and requiredness;
- exact native run/revision/snapshot/logical-root identity;
- the ordered action inventory and bindings eligible for authorization;
- initial-wave identity, digest, membership, and prior-lineage detection;
- single-writer preflight and the decision whether provider create is permitted;
- refusal before mutation or provider I/O when evidence has changed.

The API owns:

- transactional cross-run reservations and global spend policy;
- persisted initial-wave authority and paid-action/provider-operation records;
- validation of the SBE request against that API authority;
- issuance and retention of authorization documents;
- queue, lease, capacity, product-state, and recovery policy.

Neither side may reconstruct the other's authority from logs or private state.

## Approved contract direction

The API review resolved the five planning questions. Slice 1 will freeze the exact
schemas and fixtures within these approved boundaries:

- publish lifecycle inspection v0.5 rather than changing strict v0.4 in place;
- embed the complete, closed `external_authority_request` in lifecycle inspection
  v0.5 when external authority is needed; use `null` for every other branch;
- add the mutually exclusive closed companion `external_authority_refusal` object;
  it is non-null when SBE cannot safely publish an authority request and null when
  a request is present or no external-authority decision applies;
- version the request independently, provisionally
  `astrowoof.external_authority_request.v1`;
- support the closed request kinds `ordinary_action_set` and
  `initial_wave_admission`;
- bind run ID, state revision, complete snapshot identity, logical root, ordered
  action IDs, each complete public binding plus binding digest, aggregate request
  digest, and a closed provider-create permission;
- for initial-wave admission, also bind wave ID, wave SHA-256, ordered member
  binding digests, assignment/profile identity, and member count;
- order `ordinary_action_set` members by ascending lexical `action_id`, explicitly
  as canonicalization rather than execution or dependency order;
- preserve the prepared wave's semantic six-member order for
  `initial_wave_admission`; never sort wave members by action ID;
- expose a packaged schema, strict semantic validator, snapshot-validating reader,
  provider-free export/validation CLI, and sanitized fixtures;
- require a closed aggregate API grant, provisionally
  `astrowoof.external_authority_grant.v1`, that binds the exact request digest,
  native run/revision/snapshot/logical root, request kind, ordered actions, each
  member authorization document/reference and digest, API decision identity, and
  canonical grant digest;
- for an initial wave, additionally bind the wave ID/digest and ordered member
  binding digests; reject partial, missing, extra, reordered, or mismatched grants;
- constrain continuation with that exact aggregate grant and revalidate it under
  native single-writer control before authorization mutation or provider I/O.

The request is an authorization input, not authorization itself. A value such as
`provider_create_permitted_after_authorization=true` means only that SBE may create
after every native and API authorization check succeeds. It never bypasses spend
authority or promises provider idempotency.

The aggregate grant makes the API decision all-or-none; it does not make local
state persistence and a remote provider create one atomic transaction. SBE will
continue to report the irreducible identity-less post-intent crash window as typed
ambiguity rather than treating an absent local provider ID as permission to retry.

## Critical native admission rule

A fresh initial wave may be prepared only when native evidence proves all of the
following:

- no stored initial-wave object or result exists;
- no `authoring_initial` spend-ledger action exists in any historical state;
- no initial-pass attempt, provider identity, consumption, response artifact, or
  ambiguity evidence exists; and
- route/profile/request preparation is otherwise valid.

If prior initial-wave or provider lineage exists but no exact resumable wave can be
validated, SBE must return `initial_wave_lineage_unjoinable` before
preparation, authorization consumption, or provider create. It must not reconstruct
a new wave from incomplete historical evidence. The refusal is review-required,
sets `external_authority_request=null` and `provider_create_permitted=false`, and
publishes a closed `external_authority_refusal` object containing the reason and a
closed redacted evidence-category vocabulary. Consumers must not infer the refusal
from a null request plus unrelated branch fields.

## Slices

### Slice 0 — Provider-free incident reproduction and mutation map

Status: complete; API review pending.

- Build a sanitized retained exact-Natal workspace with prior initial-wave paid
  actions/provider lineage but no safely reusable current wave object.
- Reproduce the 0.4.13 generic-resume re-entry path with a scripted create counter.
- Map every mutation and provider-I/O boundary from resume through wave preparation,
  authorization application, and `execute_initial_wave_creates`.
- Freeze a fresh-run control and an ordinary single-action authorization control.

Gate: reproduce the unsafe path with no network and identify the last safe native
preflight point. Pause for API review of the reproduction before schema freeze.

### Slice 1 — External-authority request v1 and lifecycle v0.5 contract

Status: complete; API review pending.

- Freeze exact request fields, vocabularies, ordering, digest construction, and
  cross-field semantic invariants.
- Define when `external_authority_request` is present versus null.
- Define the mutually exclusive `external_authority_refusal` object, its closed
  reason/evidence vocabularies, and request/refusal/null cross-field invariants.
- Define ordinary-action-set and initial-wave-admission examples.
- Define closed refusal reasons for stale snapshots, changed revisions, mismatched
  bindings, duplicate/unknown members, provider evidence, ambiguity, and
  legacy/conflicting initial-wave lineage.
- Define the aggregate grant v1 schema and its exact join to the six ordinary
  authorization documents for an initial wave.
- Publish schemas and sanitized positive/negative fixtures.

Gate: explicit API review confirms it can validate, reserve, persist, and respond
using only public artifacts. No runtime implementation before approval.

### Slice 2 — Snapshot-validating reader and provider-free CLI

Status: complete.

- Build the request only from validated native state under a complete workspace
  snapshot.
- Join prepared actions to complete public bindings and, for a wave, to the existing
  prepared-wave and binding-bundle contracts.
- Add a supported Python reader/validator and CLI export/validation operation.
- Reject output paths inside the run workspace.
- Keep prompts, request bodies, subject data, provider payloads, and credentials out
  of the artifact.

Gate: installed-style consumer tests obtain the exact request without reading
`run.json`, logs, packet files, or snapshots directly.

### Slice 3 — Single-writer constrained continuation fence

Status: complete; awaiting review.

- Add the public continuation argument/operation selected in Slice 1.
- Acquire native single-writer control, revalidate the complete snapshot and exact
  request identity, validate the aggregate grant and member authorization documents,
  apply authorization, and durably record exact pre-submit intent before provider
  create.
- Release native single-writer control during slow provider I/O, then reacquire it
  to persist the returned provider identity/result; a replay that sees durable
  in-flight intent may not create again.
- Refuse generic provider-capable resume from `await_external_authority` when no
  compatible request identity is supplied.
- Ensure provider reconciliation remains a separate command and cannot consume an
  external-authority request.
- Publish one coherent checkpoint/result for success or typed refusal.

Gate: stale or mismatched requests cause zero state mutation, zero authorization
consumption, and zero provider calls.

### Slice 4 — Initial-wave anti-reentry and lineage policy

Status: complete; awaiting review.

- Replace the current “all pass attempts are empty” fresh-wave inference with the
  complete native admission rule above.
- Preserve exact replay of a valid stored wave and its already durable provider IDs.
- Refuse historical/conflicting lineage that cannot be joined to one exact wave
  with `initial_wave_lineage_unjoinable`, distinct from stale observation and
  provider-submission ambiguity.
- Cover partial provider identity, identity-less ambiguity, prior reported actions,
  missing binding bundle, and changed packet/request bytes.

Gate: a run can admit at most one distinct initial-wave inventory; every replay is
either exact/idempotent or refused before provider I/O.

### Slice 5 — Cross-route and ordinary-action safety matrix

Status: complete; awaiting review.

- Exact interactive fresh initial wave: supported through the constrained request.
- Exact interactive retained exact wave: exact replay/reconciliation only.
- Exact Batch, bounded interactive, bounded Batch, retries, polish, critic, and
  candidates: explicitly classify each as supported through ordinary action set,
  already covered by a route-specific authority boundary, or fail-closed deferred.
- Preserve optional-stage skipping and providerless denial semantics.
- Prove no new public status names are needed unless Slice 1 finds an irreducible
  distinction.

Gate: every provider-capable route is classified; none silently falls back to an
unfenced generic resume.

### Slice 6 — Failure atomicity, replay, and observability

- Inject failures before/after request validation, authorization persistence,
  pre-submit checkpoint, provider return, identity persistence, and final snapshot.
- Prove exact replay where provider identity is durable and ambiguity where it is
  not; deterministic keys are not treated as provider idempotency.
- Emit concise ✨🐶 logs and redacted typed events for request selection, fence
  validation, refusal reason, provider-create permission, and selected command.
- Keep logs/events non-authoritative and failure-isolated.

Gate: no crash window can convert stale or mismatched authority into new provider
work, and diagnostics explain every refusal without leaking protected bytes.

### Slice 7 — Installed-wheel joint handoff qualification

- Add a self-contained provider-free installed-wheel command/API covering fresh
  admission, retained exact replay, retained conflicting-lineage refusal, stale
  request refusal, ordinary action authorization, and reconciliation separation.
- Produce closed receipts and public fixtures for API Sprint 33 Slice 4.
- Exercise a fresh worker/restore between request export and constrained execution.
- Update lifecycle, initial-wave, spend-authorization, recovery, release, and API
  consumer documentation.

Gate: pause for API fixture adoption and joint transition-oracle review before any
version bump, tag, or release recommendation.

### Slice 8 — Release closeout

- Run the affected native suites, installed-wheel qualification, release smoke,
  fixed-epoch reproducible build, resource/catalog checks, and checksum validation.
- Record exact compatibility and retained-workspace limits.
- Recommend a fresh immutable patch only after Kevin and API approval.

Gate: explicit authorization before tag and publication.

## Testing strategy

Required provider-free scenarios:

- fresh six-member preparation/export/authorization/create;
- retained exact wave with six durable IDs and no duplicate create;
- retained prior lineage without a joinable wave: typed pre-I/O refusal;
- ordinary prepared action set with exact ordered bindings;
- stale state revision, snapshot, logical root, request digest, binding, wave digest,
  member order, authorization reference, and profile/price-book mismatch;
- missing/extra/duplicate action IDs and mixed applicability;
- provider identity/consumption/ambiguity appearing after request export;
- generic resume without request identity;
- partial aggregate grant, changed API decision identity, authorization-document
  digest mismatch, and exact aggregate-grant replay;
- reconciliation command supplied an authority request and constrained-authority
  command supplied reconciliation inputs;
- interruption at every preparation/authorization/submission persistence boundary;
- repeated inspection/export is read-only and deterministic;
- exact replay is idempotent and never creates a second wave;
- installed Python and CLI surfaces from an isolated wheel.

Counters must prove zero network/provider calls in every refusal case and exactly
the intended scripted calls in success cases. The retained Aster workspace is not a
test fixture.

## Resolved Slice 1 decisions and remaining precision

API review selected an inline snapshot-validated request, a mutually exclusive
closed `external_authority_refusal`, an aggregate all-or-none grant, lexical
ordinary-action ordering, semantic initial-wave ordering, the typed
`initial_wave_lineage_unjoinable` refusal, and a writer boundary ending after the
durable pre-submit intent checkpoint. These are now requirements rather than open
design options.

Slice 0 must still locate and prove the exact last safe preflight point in current
code. Slice 1 must specify the closed evidence-category vocabulary and grant digest
construction. Neither task may claim atomicity across local persistence and the
remote provider API: failure after durable intent but before durable provider
identity remains ambiguity/review unless provider identity can be reconciled.

## Exit criteria

- The API can identify the exact native authorization request before invocation.
- No provider-capable continuation can run from `await_external_authority` without
  a current matching request identity and compatible authorization.
- Initial-wave admission cannot create a distinct second inventory when any prior
  initial-wave/provider lineage exists.
- Provider reconciliation remains separate and retrieval-only.
- Unsupported retained evidence fails closed before provider I/O.
- Public schemas, fixtures, readers, CLI, installed qualification, logs/events, and
  API handoff are complete.
- No real provider work or retained-Aster mutation occurs during the sprint.

## Review pauses

1. Now: Kevin/API review of this plan.
2. After Slice 0: API confirms the reproduction and unsafe boundary.
3. After Slice 1: API freezes the public request/response and refusal contract.
4. After Slice 7: API adopts the installed fixtures before release qualification.
5. Before Slice 8 publication: final Kevin/API release authorization.
