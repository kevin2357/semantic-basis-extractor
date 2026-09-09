# Slice 3F — native correlation and producer identity discovery

## Decision requested

Correct the remaining packet-level identities to match facts actually persisted
by the native publication and run provenance surfaces before completing the
runtime builder.

## Runtime evidence

The exact native result/receipt/checkpoint-basis join persists:

- `native_result_id` and `native_result_sha256`;
- `receipt_id` and `receipt_sha256`;
- `post_checkpoint.native_state_revision`;
- `post_checkpoint.checkpoint_basis_sha256`; and
- `receipt.snapshot_sha256`.

It does **not** persist a separate `checkpoint_id`, `checkpoint_generation`, or
`snapshot_id`. Checkpoint archive generations are API/R2 transport coordinates,
not native terminal-publication facts. Minting editorial labels from digest
prefixes would repeat the rejected `binding_id` mistake.

Native run provenance persists:

- runtime distribution and version;
- the complete authoring profile with a stable `profile_id`;
- the complete resource inventory with `aggregate_sha256`; and
- each paid action's exact `request_sha256`.

It does **not** persist packet-ready global `compatibility_identity`,
`builder_identity`, or `prompt_identity` values. A single synthetic prompt label
would be especially misleading: prompt-bearing provider work is already bound
per action by its request digest. The runtime also does not know the installed
wheel's artifact digest, so `wheel_sha256` must remain absent unless a future
release-aware surface supplies it.

Different stages may legitimately use different prompt templates or template
versions in one run. Prompt provenance therefore belongs to the exact action,
not the packet producer. Historical action bindings prove the rendered request
digest but do not yet prove a distinct template identity or template version.

## Proposed coordinated v5 correction

Replace `native_correlations` with exactly:

- `native_run_id`;
- `subject_id`;
- `native_state_revision`;
- `checkpoint_basis_sha256`; and
- `snapshot_sha256`.

Replace required producer fields with exactly:

- `package` (`astrowoof-natal-authoring`);
- `version` (joined result release and run-provenance runtime version);
- `profile_id`;
- `profile_sha256` (canonical digest of the complete persisted profile); and
- `resource_set_sha256` (the persisted provenance aggregate digest).

Keep optional `wheel_sha256` only as a future positive fact; runtime construction
must not invent it. Remove the three unsupported producer labels. Retain each
decision's `request_sha256` as the exact request/prompt-bearing action identity.

Add an optional closed `prompt_provenance` object to each action relation with:

- `prompt_template_id`;
- `prompt_template_version`;
- `prompt_template_sha256`; and
- `rendered_request_sha256`.

When present, all four fields are required. `rendered_request_sha256` must equal
the action's existing `request_sha256`; the template SHA identifies the exact
unrendered template bytes, while ID/version provide a stable human-operable
cohort label. Current and historical packets omit the entire object because
native action bindings do not yet persist those template facts. A later native
prompt-versioning change may populate it only from exact validated action
evidence—never from SBE release, resource-set membership, filenames, or a
review-layer lookup.

Update packet-ID derivation, fixtures, projections, transport, semantic manifest,
and rehashed qualification identities together. Add mutations for:

- snapshot/checkpoint-basis substitution;
- state-revision substitution;
- result release versus provenance-version mismatch;
- profile bytes versus `profile_sha256` mismatch;
- resource aggregate substitution; and
- partial prompt provenance, rendered-request mismatch, or template digest
  substitution when the optional object is present; and
- reintroducing any removed decorative ID into a closed object.

## Boundary

This is a native evidence-shape correction, not new authority. Runtime remains
read-only and exact-result-bound. No provider, network, R2, Better Stack, API,
database, installed-wheel, or release operation is authorized or required.
