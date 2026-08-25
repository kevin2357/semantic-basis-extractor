# Slice 5 — Public Export and API Ingestion Handoff

Status: SBE implementation and focused qualification complete; API fixture-adoption
review pending before release qualification.

## Supported boundary

The primary consumer seam is:

```python
read_provider_economics_export(
    run_dir,
    observed_at="2026-08-25T12:00:00Z",
    previous_revisions=accepted_revisions,
)
```

It validates the complete stable-path workspace snapshot, accepts only exact-Natal
v0.9 or bounded-Natal v2 native state, and returns newly durable transaction
revisions in lexical native-action order. It performs no provider I/O and cannot
authorize, submit, retrieve, settle, deny, close, or release work.

The installed CLI is equivalent:

```text
astrowoof-provider-economics-export \
  --run-dir <restored-native-workspace> \
  --observed-at 2026-08-25T12:00:00Z \
  --previous-revisions <prior-export-or-revision-array.json> \
  --output <path-outside-workspace>
```

Omitting `--output` writes JSON to stdout. Output inside the native workspace is
refused so an observation cannot invalidate the snapshot it is validating.
`observed_at` is a publication-observation timestamp in canonical whole-second UTC;
it is not provider completion time or billing settlement time.

## Transaction-tape ingestion

The export is intentionally a list of individual native paid transactions, not a
deck/stage/model/cohort rollup. API should:

1. validate the export and every transaction revision;
2. group by `transaction_id`, whose authority is the pair
   `(native_run_id, native_action_id)`;
3. require exact predecessor continuity and insert immutably on
   `(transaction_id, revision_number)`;
4. treat byte-identical replay as idempotent;
5. reject skipped predecessors, conflicting replay, changed identity, or regressing
   accepted facts; and
6. optionally maintain an API-owned latest-revision projection without replacing
   the immutable revision tape.

API can merge a provider-settlement revision and a later editorial/native outcome
revision naturally. SBE emits no revision for unchanged polling or a later
publication timestamp alone.

## Money and usage semantics

- SBE commitment/estimate, provider-reported usage or money, and API-reconciled
  billing remain separately typed facts.
- Null/unavailable never means numeric zero.
- One Batch round is one transaction and one paid authority. Ordered members are
  evidence only.
- Provider-supplied member usage is retained when present. Missing member usage
  remains unavailable; SBE never allocates round cost proportionally.
- Partial Batch usage remains
  `provider_usage_unavailable_billing_reconciliation_pending`.
- `legacy_unknown` cohorts are reportable but unsafe for automatic calibration.

## Timing semantics

The transaction may expose durable create HTTP duration, bounded retrieval counts
and durations, SBE-observed provider-pending span, native action span, or an actual
provider-reported duration. Unknown timing remains null. SBE-observed pending wall
time is not provider compute time and includes scheduling/polling delay.

The retrieval reference inventory retains the first 16 references plus an explicit
overflow count. Retrieval attempts are diagnostics beneath the transaction, not
independent accounting transactions.

## Privacy inventory

The export contains identifiers, hashes, closed classifications, usage/cost,
timing, settlement, and bounded provenance references. It excludes prompts,
provider response text, cards, claims, subject birth data, coordinates, location
evidence, credentials, headers, provider request payloads, and complete spend
authorization bindings.

## Qualification

Run the provider-free installed-wheel check with:

```text
astrowoof-provider-economics-qa --require-installed
```

Its closed receipt covers exact/bounded × interactive/Batch, snapshot validation,
unchanged replay, privacy minimization, and zero external provider I/O. It creates
only temporary sanitized workspaces and accepts no provider credentials or input.

## Compatibility and ownership

This surface is additive. It does not change provider execution, lifecycle state,
native settlement, capacity, spend authorization, or publication. SBE owns the
validated native transaction evidence. API owns PostgreSQL/R2 transactionality,
retention, current projections, billing reconciliation, global policy, and product
reporting.

Before release qualification, API should ingest the packaged fixtures/receipt and
confirm predecessor, replay, semantic-null, Batch, and privacy behavior.
