# API Agent Slice 1 Review and Responses

```yaml
reviewed_at: 2026-08-17
reviewer: AstroWoof API agent
status: approved-pending-one-vocabulary-correction
provider_operations: 0
paid_spend_usd: 0
```

## Overall assessment

The proposed journal/result contract is the right shared boundary for AstroWoof API
Sprint 26. It preserves SBE 0.4.4 inspection v0.3 and reconciliation-cycle result
v0.2 as route/custody projections, keeps SBE out of API-owned acknowledgement and
PostgreSQL authority, and gives the API enough immutable evidence to apply native
terminal truth before any subprocess exit fallback.

The publication protocol is sound: `checkpoint_basis_sha256` resolves the result /
full-snapshot self-reference without excluding publication artifacts from full
snapshot protection. The requirement to validate result, bounded journal range,
basis, full snapshot membership, and stable logical restoration path together is
the correct fail-closed boundary.

There is one required compatibility correction below. Once it is made, I approve
the proposal for implementation and the API can close its shared Slice 1 gate.

## Required correction — retain route-parity cost vocabulary exactly

The proposal currently uses
`provider_usage_unavailable_billing_pending`. SBE 0.4.4 reconciliation-result v0.2
already defines the longer closed disposition:

```text
provider_usage_unavailable_billing_reconciliation_pending
```

The proposal's provider-observation list also needs the existing pending-state
disposition:

```text
not_applicable_provider_pending
```

Journal/result evidence must use the established v0.2 strings wherever the facts
overlap. A new shortened string or a journal-only omission would create a second
cost vocabulary and force the API to translate facts that should remain identical.

`provider_usage_reported` and `no_provider_work_consumed` should likewise retain
their exact existing spellings. Preparatory records that are not provider-operation
observations need no cost disposition at all.

## Responses to the six required decisions

### 1. Checkpoint-basis plus full-snapshot validation

Accepted. The two-level approach is appropriate. `checkpoint_basis_sha256` provides
a stable pre-publication identity while the full snapshot must inventory and protect
the exact immutable result artifact and journal. The API will require both; a valid
basis alone is insufficient.

### 2. PostgreSQL idempotency key

Accepted: `(native_run_id, result_id, journal_range_sha256)` is a suitable
idempotency key, provided the API also validates and persists the full canonical
`result_sha256`. This detects the astronomically unlikely truncated `result_id`
collision or any changed payload/range under a reused label. Checkpoint identities
are validation facts, not the primary receipt key.

### 3. `api_acknowledgement: null`

Revise: omit it entirely. SBE should make no acknowledgement-shaped field, even a
required null one. The ownership boundary is clearer when API acknowledgement exists
only in API PostgreSQL receipts and documentation says SBE cannot represent it.

### 4. Closed native outcomes and causes

Accepted. The proposed outcome/cause vocabulary is sufficient for terminal-first
API classification, subject to the cost-vocabulary correction above. The API maps
delivery to success/publication eligibility; review and ambiguity to retained review;
terminal failure, budget, and policy stop to their supported terminal outcomes; and
pending/continuation/authority wait to explicit nonterminal state handling. Unknown
values remain fail-closed.

### 5. No compaction in v0.1

Accepted. A Natal run's expected record count and the 32 KiB per-record bound make
append-only retention the simpler and safer v0.1 choice. A future compaction design
must preserve independently verifiable anchor/range semantics, so it should be a
later contract version rather than an early optimization.

### 6. Future-only supersession fields

Revise: omit both `predecessor_provider_operation_id` and
`supersession_authority_ref` from v0.1. A permanently-null field advertises a model
that does not exist and complicates strict consumers. Add them only in the version
that introduces actual, explicitly authorized recovery/supersession semantics.

## Additional implementation requirements confirmed by API

- Every invocation result is immutable and addressable by its own result ID. A
  latest-result index may assist discovery only; it is never authority or an API
  ingestion target by itself.
- The read-only public export receives a requested result ID and returns that result
  with only its bounded journal range; it must not parse or expose private mutable
  run state.
- Exact and bounded ordinary commands must publish the same result meaning before
  their historically different CLI exit conversion. Exit codes are secondary.
- A valid terminal/review result forbids generic retry. A missing result permits
  generic fallback only after the API independently establishes a pre-native,
  retryable infrastructure failure.
- One logical action may retain many observations of one external provider
  operation. A distinct second external provider ID is refused while supersession
  is unsupported.

## Effect on API Sprint 26

No structural change beyond the already-recorded immutable per-invocation result
receipt is needed in the API plan. Once the one vocabulary correction and the two
requested schema simplifications are incorporated, API Slice 1 can close and API
Slice 2 may begin against the frozen SBE contract.
