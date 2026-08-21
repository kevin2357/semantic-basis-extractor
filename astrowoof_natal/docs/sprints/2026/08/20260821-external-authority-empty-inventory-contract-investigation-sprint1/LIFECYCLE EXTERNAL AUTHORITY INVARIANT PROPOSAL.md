# Lifecycle External-Authority Invariant Proposal

Date: 2026-08-21
Status: proposed for API review; not implemented

## Recommendation

Retain lifecycle inspection contract identity
`astrowoof.authoring_lifecycle_inspection.v0.5` and correct its schema and semantic
validator in place.

The proposed change rejects combinations that the v0.5 handoff already describes
as contradictory and that the API already refuses. It does not add a new state,
command, authority, scheduling decision, or valid producer behavior. A v0.6 would
misrepresent this as a newly available semantic choice and require unnecessary
dual-version consumer logic.

The patch release and handoff must explicitly state that strict v0.5 consumers
should upgrade their packaged schema/validator together with the SBE wheel.

## Exact command-conditional invariants

### `await_external_authority`

Every one of these predicates is mandatory:

| Field | Required value |
|---|---|
| `execution_branch.eligible_now` | `false` |
| `execution_branch.reason_code` | `spend_authorization_required` |
| `execution_capacity.disposition` | `await_external_authority` |
| `execution_capacity.reason_code` | `spend_authorization_required` |
| `execution_capacity.local_work_ready_now` | `false` |
| `execution_capacity.resume_not_before` | `null` |
| `execution_branch.action_ids` | 1–32 unique exact paid-action IDs |
| `execution_branch.not_before` | `null` |
| `external_authority_request` | one valid object |
| `external_authority_refusal` | `null` |

The branch IDs must exactly equal the request's ordered IDs. Outer run ID and
observation must exactly equal the request. Request bindings and digest remain
subject to the existing complete external-authority request validator.

For `request_kind == initial_wave_admission`, the existing six-member semantic
order remains required. For `ordinary_action_set`, the existing lexical action-ID
canonicalization remains required.

### `none` with typed external-authority refusal

Every one of these predicates is mandatory:

| Field | Required value |
|---|---|
| `execution_branch.eligible_now` | `false` |
| `execution_branch.reason_code` | `native_review_or_ambiguity` |
| `execution_branch.action_ids` | empty |
| `execution_branch.not_before` | `null` |
| `execution_capacity.disposition` | `retain_for_review` |
| `execution_capacity.local_work_ready_now` | `false` |
| `execution_capacity.resume_not_before` | `null` |
| `external_authority_request` | `null` |
| `external_authority_refusal` | one valid object |

Outer run ID and observation must exactly equal the refusal. An empty inventory is
therefore correct for a non-runnable typed refusal and invalid for an external-
authority request.

### Other commands

Existing v0.4/v0.5 command semantics remain unchanged. Neither an external-authority
request nor refusal may accompany `ordinary_resume`,
`provider_reconciliation_cycle`, or an unrelated terminal/no-continuation `none`
branch.

## Classification outcomes

The native inspection builder must reach exactly one outcome:

1. **Valid request:** publish `await_external_authority` with a fully joined,
   nonempty request.
2. **Typed native refusal:** publish `none`/`retain_for_review` with a closed refusal
   when request construction proves native inconsistency, unjoinable lineage,
   invalid snapshot, provider ambiguity/conflict, or unsupported provider-capable
   route.
3. **Inspection failure:** raise before returning public bytes when the constructed
   outer lifecycle document is internally contradictory and cannot itself be
   truthfully classified as a native refusal.

No case publishes a preliminary empty `await_external_authority` branch. No case
falls through to ordinary provider-capable resume.

## Schema strategy

Add command-conditional JSON Schema constraints to `lifecycleInspectionV05`, not to
the shared `executionBranchV04` definition. This avoids retroactively changing the
standalone v0.4 schema while making the v0.5 request/refusal relationship explicit.

The v0.5 schema should use conditional `if`/`then` branches for:

- the complete `await_external_authority` shape;
- the complete `none` plus refusal shape; and
- exclusion of request/refusal objects on other commands.

Cross-document equality—outer/request observation and ordered IDs—remains a
semantic-validator responsibility because ordinary JSON Schema cannot conveniently
express it.

## Diagnostic proposal

Diagnostics remain non-authoritative, redacted, and failure-isolated.

### Successful classification

Retain `lifecycle.branch_selected` and enrich its data with:

- `branch_action_count`;
- `request_present` and `refusal_present`;
- `request_sha256` when a request exists;
- `refusal_reason_code` when a refusal exists; and
- `failed_predicate_count: 0`.

The existing fields continue to report native status, capacity disposition,
command, eligibility, reason, provider-action count, and local-dependency count.

### Request construction refusal

Reuse `external_authority.refused` with its existing required fields and add only:

- `request_present: false`;
- `refusal_present: true`;
- `refusal_sha256`;
- `evidence_category_count`; and
- `classification_phase: request_construction`.

### Constructed-document validation failure

Use the existing `execution.failed` event rather than expanding the closed v1 event
name vocabulary. Required values:

- `reason_code: lifecycle_branch_contract_invalid`;
- `failure_class: lifecycle_contract_validation`;
- `selected_command`;
- `failed_predicate_count`;
- `failed_predicates`: a sorted subset of the closed vocabulary below;
- `branch_action_count`; and
- request/refusal presence booleans.

Closed failed-predicate vocabulary:

- `eligible_now`;
- `branch_reason_code`;
- `capacity_disposition`;
- `capacity_reason_code`;
- `local_work_ready_now`;
- `capacity_resume_not_before`;
- `branch_action_inventory`;
- `branch_not_before`;
- `request_presence`;
- `refusal_presence`;
- `outer_request_join`; and
- `outer_refusal_join`.

No event contains action bindings, authorization documents, prompts, request or
response bodies, subject data, credentials, or provider payload content. Action IDs
may remain in structured logs for operator correlation, but the event proposal uses
only counts and digests unless API review requests exact IDs.

## Text logging proposal

At classification, emit one concise `✨🐶` line containing:

- run ID and lifecycle function context from the shared formatter;
- command, eligibility, branch/capacity reasons and disposition;
- action count;
- request/refusal presence;
- request digest or refusal reason; and
- sorted failed predicate names on validation failure.

The log must occur before a validation exception escapes, while event/log sink
failure remains unable to alter the returned inspection or native workspace.

## Compatibility

- Valid SBE 0.4.14 inspections remain valid and byte-shape compatible.
- The two Slice 0 contradictions become invalid natively, matching current API
  behavior.
- Empty `command=none` refusals remain valid.
- Lifecycle schema identity remains v0.5; the SBE release/version and packaged
  schema digest identify the corrected validator generation.
- No API migration, state-name change, orchestration change, or provider behavior
  is required.

## Questions for API approval

1. Approve tightening v0.5 in place rather than introducing v0.6?
2. Approve the exact two command-conditional tables above?
3. Approve reuse of `lifecycle.branch_selected`, `external_authority.refused`, and
   `execution.failed` rather than adding a new execution-event name/version?
4. Are counts/digests sufficient in typed events, with exact action IDs retained in
   the lifecycle document and text logs only?
5. Approve the closed failed-predicate vocabulary?
6. Should a constructed-document contradiction raise, as proposed, rather than be
   transformed after the fact into a refusal that could obscure the programming or
   persistence defect?

