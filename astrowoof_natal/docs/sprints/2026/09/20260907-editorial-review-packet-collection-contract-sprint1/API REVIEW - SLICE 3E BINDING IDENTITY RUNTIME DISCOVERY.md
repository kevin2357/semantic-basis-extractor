# API review — Slice 3E binding identity runtime discovery

## Decision

Approved. Advance the coordinated editorial-review resources from the proposed
editorial-only `binding_id` to canonical `binding_sha256`, then resume the
strictly read-only runtime builder.

API durable authority supports exactly that correction. Paid-action records
persist the immutable binding document and `immutable_binding_sha256`; native
terminal action dispositions carry `binding_sha256`; and ingestion recomputes
the digest from the decoded persisted binding before accepting the native row.
There is no persisted `binding_id` field or alternate native identity namespace
for the packet to report.

## Required v4 meaning

- `binding_sha256` is the sole concrete binding identity. It is a 64-character
  SHA-256 digest of the exact canonical binding projection; it is not a label,
  digest prefix, or editorially minted surrogate.
- Keep the complete binding document only where the approved packet/artifact
  contract calls for it, and require a recomputation that exactly equals the
  carried digest. Do not accept a digest that merely looks syntactically valid.
- An action relation remains an exact compound join: native/paid `action_id`
  plus `binding_sha256`, with `request_sha256`, provider-response identity, and
  provider-operation/disposition fields retaining their own distinct roles.
  A matching digest alone must not select a different action or disposition.
- Where a terminal action disposition exists, join it to that same exact action
  and digest and reject absent, duplicate, changed-byte/rehashed, or
  wrong-action/wrong-disposition evidence. Do not use a later result as a
  substitute for the action's persisted binding.
- Derive `decision_id` using the digest rather than the removed field, and
  rehash all enclosing identities/receipts accordingly. The v3 identifiers are
  not compatible merely because a synthetic label happened to be deterministic.

## Mutation and runtime boundary

The listed mutation coverage is the right minimum: binding-byte/digest
mismatch, duplicate digest, wrong result-disposition join, and unchanged
decision identity after a binding change. Include the complementary proof that
the valid persisted binding recomputes to its carried digest and joins exactly
one action/disposition.

This remains a packet-contract correction and a provider-free, read-only
collection change. It grants no API/R2/database mutation, Better Stack write,
release, or claim of eligibility for the already-fenced v0.3 result neighbors.
