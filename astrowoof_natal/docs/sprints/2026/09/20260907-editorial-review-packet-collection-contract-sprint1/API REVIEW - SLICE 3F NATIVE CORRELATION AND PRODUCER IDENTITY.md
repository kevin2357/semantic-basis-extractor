# API review — Slice 3F native correlation and producer identity

## Decision

Approved. Apply the coordinated v5 correction, then complete the existing
read-only, exact-result-bound packet/projection builder.

The proposed fields correctly distinguish durable native publication truth from
API/R2 transport and rollout evidence. API does retain compatibility and
checkpoint/archive coordinates elsewhere, but native terminal publication does
not make them part of this packet's native provenance. They must not be
renamed, reduced to prefixes, or imported as invented checkpoint/snapshot IDs.

## Required v5 interpretation

- `native_correlations` is exactly `native_run_id`, `subject_id`,
  `native_state_revision`, `checkpoint_basis_sha256`, and `snapshot_sha256`.
  The result/receipt pair must bind those facts exactly; substitution of any
  one is a hard failure.
- Producer provenance is exactly the concrete package/version, `profile_id`,
  digest of the complete persisted profile, and persisted resource aggregate
  digest. The result release and provenance runtime version must agree before
  emitting the one `version` value; do not select one side when they differ.
- Keep compatibility, builder, and global prompt labels absent. Their existence
  in other API rollout/custody contexts does not turn them into native
  producer facts for this record.
- `request_sha256` remains action-scoped and must stay distinct from binding,
  provider-response, result, profile, and resource identities. It is the
  available exact rendered-request evidence, not proof of a universal prompt
  template identity.
- The optional `prompt_provenance` object is sound only as all-or-none,
  independently validated action evidence. Require its rendered-request digest
  to equal that action's existing `request_sha256`; omit the entire object when
  the native binding lacks template facts. Never infer it from filenames,
  package/version, resource inventory, or review-layer lookups.

## Mutation and side-effect boundary

The proposed mutations cover the important substitutions and omissions. Also
rehash every packet/projection/transport/qualification identity after the v5
shape change, so an old v4 identity cannot be presented as a v5 packet.

This approval grants no API/R2/database/provider/network/Better Stack action,
installed-wheel claim, or release work. Unsupported result variants and all
previous exact-reader eligibility fences remain fail-closed.
