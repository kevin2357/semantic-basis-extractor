# Slice 1 — Lifecycle v0.6 Contract Proposal

Date: 2026-08-23
Status: candidate schema and semantics for SBE/API review

## Contract identities

- `astrowoof.authoring_lifecycle_inspection.v0.6`
- `astrowoof.external_authority_request.v2`

Packaged schemas:

- `temporal-lifecycle-contracts.v1.schema.json`
- `temporal-external-authority-contracts.v2.schema.json`

Public builders and validators are exported from `astrowoof_natal_authoring`.

## Structural split

The lifecycle document contains two separately canonicalized and hashed objects:

1. `checkpoint_basis`, with `checkpoint_basis_sha256`; and
2. `temporal_decision`, with `temporal_decision_sha256` and an exact join to the
   checkpoint digest.

The basis contains native observation identity without `observed_at`, terminal
and quiescence facts, dependencies, ordered action inventory without its copied
observation, provider custody without `next_due_action_ids`, route, consumer
authority, checkpoint release safety, reconciliation policy version, and a
closed external-authority state.

The Python semantic validator closes every projected child shape and vocabulary,
then validates joins among native identity, route, ordered inventory, complete
public action bindings, provider custody operations and schedule, consumer
authority, terminal/quiescence facts, and external-authority inventory. The JSON
Schema is the structural layer; a rehashed but malformed nested basis is not a
valid public contract.

Because JSON Schema support is optional in some lean installed environments,
the Python validator independently enforces primitive schema constraints:
nonempty run identity, lowercase SHA-256 digests, closed request kinds, and the
canonical `paid_[0-9a-f]{24}` action-ID form everywhere those IDs occur in the
checkpoint, custody, consumer-authority, due-subset, or request contracts.

The temporal decision contains only canonical `observed_at`, native/local
capacity disposition, local readiness, reason, supported command, eligibility,
the SBE-selected due subset, and derived `not_before`.

Thus the two formerly hidden temporal copies are structurally excluded from the
basis:

- `action_inventory.observation.observed_at` is absent because the entire copied
  observation is absent from the basis inventory; and
- `provider_custody.next_due_action_ids` exists only as
  `temporal_decision.due_action_ids`.

## Canonical time

The canonical representation is whole-second UTC:
`YYYY-MM-DDTHH:MM:SSZ`.

The builder normalizes an equivalent aware offset spelling. The public validator
requires the canonical representation and refuses naive timestamps and
fractional seconds. The API supplies the trusted instant used for persisted
ordering; SBE does not claim clock authority.

## Transition semantics

For one checkpoint basis:

- same time must reproduce the exact same decision;
- later not-due to due is allowed;
- later identical due evidence is allowed and idempotent;
- backward time, same-time changed decision, eligibility regression, and due to
  not-due refuse with closed reason names;
- changed basis is not a temporal transition and returns
  `checkpoint_basis_changed`; and
- provider retrieval/persistence creates a new basis.

API lease/custody controls remain responsible for ensuring that repeated due
observations do not cause duplicate invocation.

## Stable external authority

The v2 request contains the run ID, checkpoint-basis digest, request kind, and
exact ordered action IDs. Its digest therefore remains identical when only
`observed_at` advances. It changes when the native basis or exact inventory
changes. It intentionally has no incidental inspection timestamp. A future
time-sensitive rule requires an explicit validity/expiry field.

Every requested action's complete public binding remains in the strictly
validated checkpoint-basis inventory. The supported
`validate_external_authority_request_v2_against_inspection()` operation proves
run identity, basis digest, request kind, exact order, member presence, and every
binding join. The standalone v2 request is only an identity/reference; it is not
enough to reconstruct or authorize any action.

This Slice 1 artifact freezes request identity. Applying the new request through
the constrained runtime remains later-slice implementation work; existing v1
grants are not silently reinterpreted.

## Compatibility

Lifecycle v0.5 and older documents are not accepted as v0.6. Consumers must not
invent the split by maintaining mutable-path allowlists. The v0.6 builder is an
explicit native projection from a currently validated v0.5 inspection while the
runtime adoption is implemented and qualified.

## Review questions

1. Approve the two contract identities and canonical whole-second UTC format?
2. Approve complete removal of copied observation from the basis inventory?
3. Approve the closed same-basis transition refusal vocabulary?
4. Approve the v2 authority request as basis/inventory-bound and time-free?
5. Approve retaining API lease/custody as the command-invocation concurrency
   authority?
