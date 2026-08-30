# Slice 3 — Retry lineage and mixed-custody contract proposal

## Status

Contract implementation complete; runtime mutation deliberately not begun.
Paused at Voof-paws 4 for API review.

## The identity rule

The canonical logical-attempt coordinates are exactly `native_run_id`,
`route_family`, `stage`, `pass_id`, and `attempt_number`. They are encoded as
canonical UTF-8 JSON with sorted keys and compact separators. The public key is
`attempt_` plus the first 24 lowercase hexadecimal characters of that SHA-256.

Request and binding digests are deliberately **not** part of this key. They are
evidence attached to the key; disagreement is therefore detected rather than
renamed into a second logical attempt. Action ID, mechanism, provider operation
ID, and persisted pass-attempt pointer are also evidence, not alternate logical
identities. Attempts and actions use lexical canonical order.

## Closed lineage result

`astrowoof.retry_lineage_inventory.v1` groups evidence by logical attempt. Each
attempt is `consistent` or `conflict`. The closed conflict vocabulary is:

- `multiple_actions_for_attempt`
- `request_binding_conflict`
- `pass_attempt_pointer_conflict`
- `multiple_active_actions_for_attempt`

A conflict always sets `forward_dispatch_permitted=false`. The separate
`reconciliation_permitted` assertion is true only when the inventory contains a
durable provider operation ID. A contradiction therefore forbids new authority
consumption/create without erasing or stranding already-paid provider work.

The inventory also exposes the closed aggregate classification
`retry_lineage_conflict_requires_review` (or `null` when consistent). This and
the per-attempt `reason_codes` are the authoritative machine-readable cause;
consumers do not infer lineage conflict from a generic review state.

## Lifecycle v0.8

`astrowoof.authoring_lifecycle_inspection.v0.8` is a closed extension of v0.7.
It adds the complete retry-lineage inventory to immutable checkpoint basis and
its digest to the temporal decision. Validation reconstructs and validates the
underlying v0.7 document, then enforces the new joins.

For conflict plus nonempty provider custody, the selected command must be
`provider_reconciliation_cycle`; its due IDs remain SBE-selected and must join
custody. Forward dispatch stays forbidden while reconciliation stays permitted.

For conflict after custody is empty, the only valid projection is `none` with
`retain_for_review`, no due IDs, and no local or authority/create implication.
Thus `none / retain_for_review` with nonzero provider custody is invalid v0.8.
Historical v0.7 remains readable but is not silently reinterpreted as v0.8.

Every lineage action joins exactly one v0.7 `action_inventory` member, and every
checkpoint creative-retry action appears exactly once. The join covers action
ID, native run/route family, stage, canonical pass and attempt parsed from the
binding route, request and complete-binding SHA-256 values, state, mechanism,
provider operation identity, and canonical pass-attempt pointer. Custodial retry
actions additionally join the exact custody member/provider identity.

The older action-inventory `attempt` presentation field is not attempt authority:
its released parser reports `1` for routes spelled `attempt-003`. v0.8 therefore
uses the canonical binding route's explicit attempt component. This historical
compatibility fact is explicit rather than silently assigning the old field new
semantics.

## Replay, compatibility, and the next slice

Same validated v0.7 basis plus the same lineage inventory produces the same v0.8
basis. Changed action, binding, request, pointer, or provider evidence changes
the lineage inventory and basis. API validates v0.8 and invokes only the selected
run-level command; it never chooses retrieval members or repairs native lineage.

This slice adds projection builders, strict Python validators, the complete
packaged `temporal-lifecycle-contracts.v3.schema.json` root schema and reader,
the retry-lineage sub-schema, public exports, source-level complete example
construction, and mutation tests only. Slice 4 proposes to persist attempt key,
action, binding/request digests, and request-artifact identity atomically under
the writer; select feedback by completed predecessor attempt number/state; reuse
that exact evidence on re-entry; and run whole-ledger validation before create.
