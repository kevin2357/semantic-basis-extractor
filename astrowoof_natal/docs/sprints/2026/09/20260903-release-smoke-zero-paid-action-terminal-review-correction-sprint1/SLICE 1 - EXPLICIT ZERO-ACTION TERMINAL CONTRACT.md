# Slice 1 — explicit zero-action terminal contract

**Status:** implemented and API-reviewed; ready for Slice 2 packaged/installed
qualification.

## Boundary

`astrowoof.native_execution_result.v0.2` remains the strict paid-action
terminal-review result. Its action-disposition inventory continues to require a
complete binding-backed row for every ledger action.

The provider-free release-smoke fixture is not a degenerate paid run. It fails
editorially before an OpenAI ledger was created, so it needs a separate closed
result shape rather than an omitted inventory pretending to be empty.

## Implemented v0.3 result

Publish `astrowoof.native_execution_result.v0.3` only when all conditions hold:

1. the native state has a present `spend_ledger` object;
2. `spend_ledger.actions` is a present list with exactly zero members;
3. no action, provider operation, authorization, consumption, or custody
   projection is supplied; and
4. the terminal cause is one of the closed pre-provider editorial/validation
   causes permitted for the release-smoke fixture.

The result retains the same invocation/run/route/checkpoint/journal/result and
receipt bindings as v0.2, but uses these explicit fields instead of a paid
action-disposition inventory:

```json
{
  "action_inventory_kind": "explicit_zero_paid_actions",
  "paid_action_count": 0,
  "provider_operation_count": 0,
  "new_provider_create_permitted": false
}
```

The schema is exact-key and versioned. A v0.2 reader fails closed on v0.3; the
release-smoke reader validates v0.3 directly. No API lifecycle or worker
consumer is asked to reinterpret v0.2. Its corresponding v0.2 command envelope
also carries the exact result/receipt identities without a custody projection.

## Refusals / negative cases

The builder and validator must refuse:

- omitted or null `spend_ledger` / `actions`;
- a non-list `actions` field;
- any nonempty inventory, even if its action looks terminally accounted;
- any provider ID, authorization, consumption, custody, or action-disposition
  evidence attached to the zero-action result; and
- an unsupported cause, result schema, digest, checkpoint, journal, receipt, or
  invocation join.

## Qualification

1. Update only the provider-free smoke fixture to declare an explicit empty
   ledger at its creation boundary.
2. Run the installed smoke through terminal publication and receipt validation.
3. Prove zero provider I/O and no synthetic paid ID/binding.
4. Prove the existing v0.2 one-action fixture remains strict and cannot be
   recast as v0.3.
5. Prove both validators reject the other result version directly.
