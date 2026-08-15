# Slice 1 Batch Contract

Status: complete; API-agent approved

## Public contract identity

The proposed packaged contracts are:

- request: `astrowoof.provider_negative_authorization_batch_request.v0.1`;
- result: `astrowoof.provider_negative_authorization_batch_result.v0.1`; and
- batch event: `authorization.denied_providerless_batch` within
  `sbe.execution_event.v1`.

The public Python/CLI implementation is intentionally deferred until the contract
gate passes.

## Request

One request contains exactly:

- `schema_version`;
- one `run_id`;
- one complete original lifecycle `observed` identity; and
- an ordered array of 1 through 32 action members.

Each member contains the exact `action_id`, complete immutable spend binding,
closed denial reason, and bounded opaque external authority reference. Unknown
fields fail strict schema validation. Duplicate IDs are valid JSON shapes but are
an explicit locked-preflight refusal; JSON Schema cannot express uniqueness by one
object property without incorrectly treating otherwise distinct objects as equal.

Thirty-two is a conservative hard contract bound comfortably above the current
maximum expected authoring-stage action count while bounding request, result,
event, and preflight work. It is not caller-configurable.

## Canonical request identity and replay

`batch_request_sha256` is SHA-256 over UTF-8 canonical JSON of the complete request:
object keys sorted, no insignificant whitespace, Unicode retained, and array order
preserved. It therefore binds:

- schema version and run ID;
- the original state revision, snapshot, logical root, validation/exclusivity facts,
  and observation timestamp;
- exact ordered action membership;
- every immutable binding, including request digest, profile, route, model, output
  maximum, commitment, and price book; and
- every denial reason and external authority reference.

The digest is returned, not supplied as self-asserted authority. Exact replay means
the entire canonical request matches a durable successful batch record. Reordering,
adding, removing, or changing any member produces a different request identity.

## Successful result

An applied result includes:

- `applied: true` and `outcome: applied`;
- exact `batch_request_sha256` and original `request_observation`;
- the locked pre-mutation `decision_basis`;
- ordered action results with exact binding, denial disposition/reason, whether
  authorization was previously recorded, release-eligibility evidence, and the
  opaque external authority reference;
- one complete `post_mutation_observation`; and
- one shared `result_checkpoint` with the resulting revision/snapshot and durable
  batch-result artifact identity.

Exact replay returns `applied: false`, `outcome: idempotent_replay`, and per-action
`idempotent_replay` outcomes while preserving the original decision basis,
post-mutation observation, and shared result checkpoint. It performs no new native
mutation and does not duplicate events.

Only successful applied/replay members expose `release_eligible: true`. This is SBE
native evidence for API evaluation, not a release of API reservations.

## Refused result

A refusal has `applied: false`, no post-mutation observation, no result checkpoint,
and no member with release eligibility. It contains the original request
observation, current actual observation when safely available, a closed batch
outcome, ordered per-member validation outcomes, and bounded review reasons.

Batch outcomes distinguish:

- `stale_observation`;
- `immutable_binding_mismatch`;
- `unknown_action` and `duplicate_action`;
- `provider_identity_appeared`, `provider_evidence_appeared`, and
  `consumption_evidence_appeared`;
- `ambiguous_submission_boundary`;
- `action_ineligible`;
- `native_state_inconsistent`;
- `exclusivity_not_established` and `writer_race_possible`; and
- `review_required`.

Per-member outcomes identify an exact refusal or report `eligible` when that member
passed but another member refused the all-or-none batch. `not_evaluated` is reserved
for a shared precondition failure that prevents safe action lookup. Ordinary
unsupported schemas and malformed documents remain input/programming errors.

Provider-bound safety takes precedence over generic staleness, matching the
existing single-action contract. For several member failures, implementation will
choose one deterministic batch outcome by documented severity order while retaining
every per-member outcome.

## Compatibility and terminal semantics

- The existing single-action request/result and `deny_providerless_action()` remain
  unchanged and supported.
- `DELIVERY_COMPLETE` is a supported context. Each requested action must still be
  independently eligible and providerless at the locked decision basis.
- The operation never changes accepted deck/delivery bytes and never reopens
  editorial work.
- The operation accepts no provider object and performs no submission, polling,
  cancellation, or reconciliation.
- A complete retained workspace restored at its stable logical absolute path can be
  inspected, batch-denied, and exactly replayed.

## Events

Successful first application will emit ordered existing per-action
`authorization.denied_providerless` observations followed by one
`authorization.denied_providerless_batch` event. The batch event requires only the
request digest, outcome, and action count. Exact replay will emit the batch replay
observation only, avoiding duplicate per-action transition events. Refusal event
policy will be finalized with implementation, but events remain non-authoritative,
redacted, and failure-isolated.

## Review questions

The API agent should confirm:

1. the 32-action bound is adequate;
2. the top-level and per-action outcomes are sufficient for reservation-release and
   audit mapping;
3. exact replay binding to the original observation timestamp is desired;
4. `eligible` versus `not_evaluated` is sufficient for non-causal members of a
   refused batch;
5. provider-safety precedence over stale observation should remain unchanged; and
6. the proposed initial/replay event policy is useful and unambiguous.

## API review disposition

The AstroWoof API agent approved all six points without requested schema changes.
The API will treat only exact successful/replay member evidence as a basis for its
own reservation-release decision and will release nothing for any refused batch.
It will retain the exact request, digest, outcomes, member evidence, and checkpoint
as API-owned audit/recovery provenance.

An optional batch-level refusal event with only digest, outcome, count, and reason
category was endorsed for diagnostics. It remains non-authoritative and is not
required for correctness.
