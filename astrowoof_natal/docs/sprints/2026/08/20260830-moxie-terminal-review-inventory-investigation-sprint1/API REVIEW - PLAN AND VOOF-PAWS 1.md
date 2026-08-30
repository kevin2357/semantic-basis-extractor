# API review — plan and Voof-paws 1

## Decision

Approved to begin Slice 0, including the planned source/contract map and the
strictly bounded retained-checkpoint access preparation. The plan correctly
keeps three questions independent:

1. whether SBE's terminal-review v0.2 result is full-ledger or has a public
   bounded scope;
2. whether the retained native/API inventories actually diverged; and
3. the API worker containment defect that converted a typed ingress refusal
   into a later `lease_expired` retry.

The API companion is correcting only (3). It does not relax the exact action
join or claim an unproven snapshot-subset rule.

## Exact protected-object coordinate

For the single approved Moxie target, use only:

| Field | Value |
| --- | --- |
| environment | `qa` |
| namespace | `checkpoint` |
| object UUID | `429d43b2-6dc0-4ad9-ac31-ee68c9d32878` |
| exact object key | `v1/checkpoint/429d43b26dc04ad9ac31ee68c9d32878` |
| expected ETag/version | `"43ecac806938556e1bf16e6b63952130"` |
| expected archive SHA-256 | `aa6b472e3b865242f93c388a8664828a292ff05953e835211f90a70567132920` |
| expected bytes | `3924276` |
| expected inventory SHA-256 | `88d6e44341ade8d21fccf3c2964f721e03f45e089a510c4859f3ca9f8bc61509` |

This is a deterministic rendering of the public API storage reference
(`v1/{namespace}/{object_id.hex}`), not a guessed key or a bucket listing.
It is approved only for the plan's one `HEAD` and one `GET`, followed by the
listed identity/hash/archive-safety checks. No provider access, native writer
command, database mutation, R2 listing/write/delete, or retained-run recovery
is authorized.

## Slice-0 refinements

- Include the API-owned seventh action's status as `provider_created`, not as
  evidence that it was reported/adopted by SBE. The resulting matrix must keep
  API custody and native-ledger presence separate.
- If a result or receipt is found, bind its declared inventory to the exact
  checkpoint/generation and lifecycle basis before comparing action sets.
- If no sealed result is recoverable, conclude only the retained ledger and
  checkpoint facts. Do not reconstruct the lost rejected payload from API
  records or treat an absence as an SBE defect.

## Gate

Voof-paws 1 and the pre-access review are satisfied. Slice 1 is approved to
perform exactly the manifest's one `HEAD` and one `GET`, then validate the
specified ETag, bytes, archive hash, inventory hash, archive containment, and
logical restore root before reading the listed native metadata. Pause at
Voof-paws 2 before causal interpretation or any next operation.

The absent six initial API IDs/full immutable bindings do **not** block this
read-only native inspection. They do block any claim of a completed exact
seven-row field-level API/native join; record that limitation plainly and ask
API for a separately scoped packet only if Slice 2 genuinely needs it.
