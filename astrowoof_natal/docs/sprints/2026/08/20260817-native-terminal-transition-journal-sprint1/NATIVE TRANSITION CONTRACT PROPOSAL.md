# Native Transition Journal and Execution Result Contract Proposal

Status: frozen; API-approved after route-parity vocabulary correction
Contract baseline: SBE 0.4.4 inspection v0.3 and reconciliation result v0.2
Provider operations: 0
Paid spend: `$0`

## Decision summary

SBE will publish two new immutable native authorities:

1. an append-only transition journal containing compact durable native
   observations; and
2. one immutable execution-result artifact per command invocation.

Inspection v0.3 and reconciliation-cycle result v0.2 remain current-state and
cycle projections of this truth. They are not replaced. Events, stdout, exit codes,
and any latest-result index remain non-authoritative observations/conveniences.

API ingestion accepts one specified execution result plus its exact bounded journal
range and complete workspace snapshot. PostgreSQL acknowledgement is created only
by the API transaction and never appears as an SBE claim.

## Contract identities and paths

| Artifact | Contract identity | Workspace path |
|---|---|---|
| Journal record | `astrowoof.native_transition_journal_record.v0.1` | `native-transition-journal.jsonl` |
| Execution result | `astrowoof.native_execution_result.v0.1` | `native-results/<result_id>.json` |
| Optional derived index | `astrowoof.native_result_index.v0.1` | `native-result-index.json` |
| Proposal schema | non-packaged Slice 1 draft | `fixtures/native-transition-contracts.proposal.schema.json` |

`result_id`, `record_id`, and `invocation_id` are SBE identities. They are never
provider IDs. Paths are relative discovery labels; embedded identities are
authority.

## Canonical hashing

All contract digests use SHA-256 over UTF-8 canonical JSON:

- object keys sorted lexicographically;
- no insignificant whitespace;
- arrays retain order;
- no NaN or Infinity;
- timestamps normalized to UTC `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`; and
- digest fields excluded from the object whose digest they carry.

### Record identity

`record_sha256` hashes the complete record excluding `record_id` and
`record_sha256`. `record_id` is `ntr_` plus the first 24 lowercase hexadecimal
characters of that digest. `previous_record_sha256` is null only at sequence 1 and
otherwise equals the prior complete record's `record_sha256`.

### Journal range identity

`range_sha256` hashes the ordered array of complete record digests from
`start_sequence` through `end_sequence`, inclusive. Gaps, forks, duplicates, or
order changes therefore fail validation.

### Invocation result identity

`result_sha256` hashes the result excluding `result_id` and `result_sha256`.
`result_id` is `nres_` plus the first 24 lowercase hexadecimal characters of that
digest. Exact replay must reproduce the same bytes and identity; a semantically
similar later invocation is a distinct result.

## Solving the result/snapshot hash cycle

An immutable result cannot contain the SHA-256 of a snapshot manifest that itself
contains that result: that would be self-referential. The contract therefore uses
two jointly required identities:

1. `checkpoint_basis_sha256` is the canonical digest of the snapshot schema,
   logical root, native state revision, and sorted member descriptors after
   excluding only `workspace-snapshot.json`, `native-results/**`, and the derived
   `native-result-index.json` publication namespace.
2. The ordinary full `workspace-snapshot.json` inventories the journal, immutable
   result artifact, state, public state, ledger, and every other authoritative
   member under existing rules.

The result embeds the stable checkpoint-basis digest. The consumer must also
validate the complete full snapshot containing that exact result. A result is
visible/valid only when:

- its own identity validates;
- its journal range/digest validates;
- its post-state revision and checkpoint-basis digest recompute exactly;
- its path and hash appear in the complete full snapshot; and
- the complete snapshot validates at the stable logical absolute path.

Excluding the publication namespace from the *basis calculation* does not exclude
it from the full snapshot or restoration boundary. Missing, extra, changed,
truncated, forked, or relocated publication files invalidate the workspace.

## Atomic publication protocol

One native writer performs the following ordered protocol:

1. Validate the pre-invocation full snapshot and acquire native exclusivity.
2. Mint `invocation_id` and append `invocation.started`.
3. Append action/provider/native observations only after their underlying durable
   state transition is persisted or in the same guarded mutation boundary.
4. Persist final native state/public/ledger files.
5. Append `invocation.closed` with closed outcome/cause and post-state revision.
6. Compute the exact journal range and checkpoint-basis digest.
7. Write the immutable result to a hidden staged file.
8. Promote the staged result to `native-results/<result_id>.json` without overwrite.
9. Optionally refresh the derived latest index.
10. Publish the ordinary complete workspace snapshot last.
11. Revalidate result, range, basis, and full snapshot together before returning,
    printing, emitting an event, or converting to a process exit code.

No multi-file filesystem transaction is claimed. Interruption before step 10 leaves
an invalid/incomplete old snapshot; interruption during/after step 10 either leaves
the old valid checkpoint or the new jointly valid checkpoint under atomic manifest
replacement. Resume and API ingestion fail closed unless the complete protocol
validates.

## Journal record contract

Every record contains:

- schema version, run ID, invocation ID, sequence, SBE record identity/hash, prior
  hash, `observed_at`, native state revision, and closed `record_kind`;
- validated route binding: `route_family`, `provider_mechanism`, and
  `native_operation_ref`;
- exact action binding when relevant: action ID, request digest, profile digest,
  route, stage, maximum output, commitment, and price-book version; and
- exactly one kind-specific observation body.

### Closed record kinds

- `invocation.started`
- `action.prepared`
- `action.authorized`
- `action.consumed`
- `action.denied_providerless`
- `provider.submission_started`
- `provider.identity_recorded`
- `provider.pending`
- `provider.completed`
- `provider.failed`
- `provider.cancelled`
- `provider.expired`
- `provider.usage_reported`
- `provider.usage_unavailable`
- `provider.submission_ambiguous`
- `provider.identity_conflict_refused`
- `native.transitioned`
- `invocation.closed`

Preparation/authorization records are action observations, not provider operations.
`provider.submission_started` has no external provider ID. An external ID appears
only from `provider.identity_recorded` onward and is never synthesized from a local
request or idempotency key.

### Provider operation observation

Each provider record carries an SBE `record_id` distinct from:

- `action_id`, the native paid-action identity; and
- `provider_operation_id`, the external Response or Batch identity.

The operation body contains closed `observation_kind`, provider kind, external ID
when known, status, and optional immutable evidence references. Reported cost uses:

- `cost_disposition`: `provider_usage_reported`,
  `provider_usage_unavailable_billing_reconciliation_pending`,
  `no_provider_work_consumed`, or `not_applicable_provider_pending`;
- versioned `price_book_version` and `usage_evidence_ref` when reported;
- integer `estimated_micro_usd` only with reported usage; and
- no fabricated zero for missing usage.

Raw prompts, provider response bodies, protected subject fields, and credentials are
never journal payloads. They remain separately protected artifacts referenced by
relative path and SHA-256 only where necessary.

### Cardinality and supersession

One action may have many observations of one external provider operation, but no
second distinct external provider ID. Exact replay of the same kind/ID is
idempotent. A different ID produces `provider.identity_conflict_refused`, terminal
review/ambiguity as applicable, and no overwrite.

The v0.1 shape contains no predecessor or supersession fields. Supersession/recovery
is not supported in this sprint and cannot be enabled without a later contract
version and explicit authorization model.

## Execution result contract

Each immutable result contains:

- schema/result/invocation/run/release identities and `published_at`;
- command kind: `ordinary_authoring` or `provider_reconciliation`;
- validated route binding;
- pre-state revision and pre-snapshot SHA-256 when one existed;
- post-state revision and checkpoint-basis digest;
- exact journal start/end/count/range digest and closing record ID;
- closed native outcome and cause;
- ordered action IDs and provider-operation references observed by the invocation;
- inspection v0.3 and, for reconciliation, cycle-result v0.2 artifact/reference
  identities rather than divergent copied semantics; and
API acknowledgement is absent from the SBE schema entirely. The ownership boundary
exists only in documentation; acknowledgement is an API PostgreSQL receipt.

### Closed native outcomes

- `delivery_complete`
- `review_required`
- `terminal_failure`
- `provider_pending`
- `continuation_required`
- `awaiting_external_authority`
- `budget_exhausted`
- `policy_stopped`
- `ambiguous_submission`
- `native_evidence_invalid`

### Initial cause codes

- `delivery_complete`
- `delivery_complete_with_warnings`
- `final_qa_requires_review`
- `authoring_attempts_exhausted`
- `provider_terminal_failure`
- `provider_output_invalid`
- `provider_identity_conflict`
- `provider_operation_pending`
- `local_continuation_ready`
- `spend_authorization_required`
- `external_spend_authority_denied`
- `native_budget_ceiling_exhausted`
- `external_product_policy_denied`
- `ambiguous_provider_submission`
- `snapshot_or_journal_invalid`
- `unsupported_route_or_legacy_evidence`

Unknown values fail schema validation. Optional-stage policy skip is journaled as
local continuation and never mapped to terminal failure.

## API acceptance and refusal mapping

| Native evidence | API ingestion disposition | Generic exit fallback |
|---|---|---|
| Valid `delivery_complete` result | Atomically ingest result/operations/checkpoint; apply delivery transition | Forbidden |
| Valid `review_required` result, including exit 2 | Atomically ingest and transition to API review terminal | Forbidden |
| Valid supported terminal failure/budget/policy result | Atomically ingest and apply mapped terminal outcome | Forbidden |
| Valid provider-pending result | Ingest operations/custody/checkpoint; schedule no earlier than native advice | Forbidden |
| Valid continuation/wait result | Ingest checkpoint/result; apply explicit native continuation/wait mapping | Forbidden |
| Valid ambiguity result | Retain authority and transition to review/ambiguity | Forbidden |
| Missing result after fully adopted producer contract | Retain workspace; classify native evidence unavailable | Allowed only if independently proven pre-native transient failure |
| Invalid hash/range/snapshot, gap, fork, stale result, route/action mismatch | Reject atomically; retain for review | Forbidden as retry authority |
| Historical pre-contract SBE workspace | Legacy fail-closed mapping; no synthesized journal | Governed by explicit legacy policy, never new-route authority |

The API transaction keys idempotency to `(native_run_id, result_id,
journal_range_sha256)`. Replaying the exact result returns the prior receipt without
duplicating provider-operation children or state transition. A reused result ID with
different bytes/range is a hard integrity conflict.

## Compatibility with current contracts

- Inspection v0.3 remains the strict current-state route/capacity/custody view.
- Reconciliation-cycle result v0.2 remains the bounded cycle projection.
- Journal/result records reference their identities and must agree with them where
  overlapping; disagreement invalidates publication.
- Existing lifecycle events may mirror successful publication only after joint
  validation. They do not establish it.
- SBE 0.4.4 and older workspaces have no authoritative journal history. They fail
  closed for the new ingestion route rather than receiving reconstructed records.
- Exact Responses, exact Batch, and bounded Responses share this contract. Bounded
  Batch remains unsupported.

## Retention and bounds

- Journal sequence is monotonically increasing and never compacted in v0.1.
- One record is at most 32 KiB canonical JSON; one execution result is at most
  256 KiB; strings and arrays have schema-specific bounds.
- Public export requires a specified `result_id` and returns only that result and
  its bounded journal range. No unbounded journal dump is a public worker contract.
- Full snapshots and raw referenced artifacts retain their existing cleanup and
  restoration policy. A published journal/result needed for ingestion is not
  reconstructable scratch.

## API review resolution

The API approved the checkpoint-basis/full-snapshot protocol, closed native
outcomes/causes, permanent v0.1 no-compaction posture, and PostgreSQL idempotency key
`(native_run_id, result_id, journal_range_sha256)`, with full canonical
`result_sha256` additionally validated and persisted.

The frozen correction retains the exact reconciliation v0.2 cost vocabulary,
including `not_applicable_provider_pending` and
`provider_usage_unavailable_billing_reconciliation_pending`. It omits API
acknowledgement and future supersession fields entirely. The contract is approved
for implementation.
