# SBE response to API Slice 2 — terminal-result availability

## Disposition

Accepted. The current `latest_native_transition_result(run_dir)` helper conflates
a normal absence condition with invalid discovery evidence by raising an untyped
`ValueError` when no result ID is present. API must neither match exception text
nor treat every reader failure as absence.

This requires a narrow additive public contract. It does not change lifecycle,
terminal-result authority, provider custody, scheduling, or result ingestion.

## Proposed public surface

Add a provider-free, snapshot-validating reader and CLI backed by a closed schema:

```text
astrowoof.native_transition_result_availability.v1
```

The exact availability outcomes are:

- `none_available`
- `available`

The result carries only discovery evidence:

- schema version;
- native run ID;
- logical workspace root;
- availability outcome;
- bounded result count;
- exact latest result ID or null;
- result-index SHA-256 or null; and
- availability-document SHA-256.

It carries no lifecycle state, action inventory, provider identity, authority,
terminal disposition, or result contents.

## Validation rules

The reader must:

1. validate the restored workspace and run identity before discovery;
2. treat an absent index with no result/publication artifacts as
   `none_available`;
3. accept a closed, correctly versioned empty index with no result/publication
   artifacts as `none_available`;
4. validate the exact index shape, schema, bounded unique ordered result IDs, and
   canonical ID spelling;
5. reject result files or publication receipts that cannot be joined to the
   index;
6. require the selected latest ID to pass the existing explicit sealed-result
   reader before returning `available`;
7. return only that exact ID; and
8. raise a typed public availability error for malformed, conflicting, orphaned,
   snapshot-invalid, or unsealed evidence.

The API may use `latest_result_id` only for discovery. It must then carry that
exact ID into `read_native_transition_result()` and strict terminal ingress. It
must not repeat latest discovery after lifecycle selection or treat the
availability document as transition authority.

## CLI behavior

Add a read-only installed-wheel command which:

- accepts one `--run-dir`;
- accepts no provider, grant, action, lifecycle, or mutation inputs;
- emits the closed availability document;
- refuses output paths inside the native workspace; and
- uses distinct typed/nonzero failure for invalid evidence rather than emitting
  `none_available`.

## Required tests

- absent index and no publication artifacts → `none_available`;
- valid empty index → `none_available`;
- one or more fully sealed results → exact latest ID and count;
- malformed schema/keys/result ID/duplicate ordering → typed refusal;
- orphan/unindexed result or receipt → typed refusal;
- indexed but missing/malformed/unsealed latest result → typed refusal;
- invalid workspace snapshot → typed refusal;
- explicit ID obtained from availability joins the existing strict reader;
- CLI output-inside-workspace refusal; and
- installed-wheel provider-free smoke.

## Compatibility

`latest_native_transition_result()` remains supported for compatibility. API's
terminal-first preflight should use the new availability reader instead. No
existing result, receipt, journal, lifecycle, or command-result schema is widened.
