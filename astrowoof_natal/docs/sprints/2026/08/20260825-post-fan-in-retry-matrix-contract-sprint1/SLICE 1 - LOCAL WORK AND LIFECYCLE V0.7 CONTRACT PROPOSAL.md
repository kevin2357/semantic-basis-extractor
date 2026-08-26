# Slice 1 — Local Work and Lifecycle v0.7 Contract Proposal

Status: implemented as a contract-only proposal; awaiting owner/API review before
runtime selector changes

## Version decision

The released identities are preserved:

- native lifecycle v0.5 remains unchanged/readable;
- temporal/checkpoint lifecycle v0.6 remains unchanged/readable; and
- the richer contract is `astrowoof.authoring_lifecycle_inspection.v0.7`.

v0.7 has the same checkpoint-basis/temporal-decision architecture as v0.6. Its
immutable checkpoint basis adds one exact `astrowoof.local_work_inventory.v1`.
Its temporal decision adds the joined `local_work_inventory_sha256`. No existing
schema is widened or reinterpreted.

## Inventory authority

The inventory is SBE-selected evidence that a run-level `ordinary_resume` command
has concrete executable work. It is not an API-selectable internal command list.

Every inventory binds:

- native run ID;
- exact state revision;
- full workspace snapshot SHA-256;
- stable logical workspace root;
- deterministic SBE execution order; and
- a digest over the complete inventory.

Every member has two identities:

- `operation_key = work_<24 hex>` is basis-independent and derived from kind,
  route, stage, source-action lineage, and reason; and
- `operation_id = local_<24 hex>` additionally includes the exact basis revision
  and snapshot.

The member repeats the basis revision/snapshot and binds one closed operation kind,
route family, paid stage where applicable, exact ordered source action IDs, and a
closed reason.

## Initial closed operation vocabulary

| Kind | Meaning |
| --- | --- |
| `provider_result_fan_in_and_retry_evaluation` | Consume completed provider evidence and atomically decide/prepare the next retry at one durable checkpoint |
| `final_assembly_and_qa` | Assemble accepted pass work and persist deterministic QA disposition |
| `delivery_construction` | Construct native delivery from accepted final evidence |

The first operation is deliberately combined. Current public evidence does not
prove a durable checkpoint between provider-result ingestion and next-retry
evaluation. If Slice 2 discovers such a real boundary, it may split the operation
only through another reviewed contract revision.

## Branch matrix

| v0.7 branch | Inventory rule |
| --- | --- |
| eligible `ordinary_resume` | one or more operations required |
| provider reconciliation | inventory must be empty |
| external authority | inventory must be empty |
| terminal/review/refusal `none` | inventory must be empty |

Both JSON Schema and the Python validator close the public shapes. The Python
validator additionally reconstitutes and validates the complete underlying v0.6
projection, verifies every inventory/checkpoint join, and enforces branch semantics
even when `jsonschema` is unavailable.

## Progress and replay rule

After an eligible ordinary resume:

1. the successor checkpoint basis must differ;
2. no prior basis-independent `operation_key` may remain advertised;
3. `consumed_operation_keys` is cumulative and append-only across the checkpoint
   lineage: every successor contains every key consumed by its predecessor;
4. no current operation key may occur in the cumulative consumed-key set;
5. if the successor remains `ordinary_resume`, its sealed consumed-key set must
   newly include at least one prior current key; or
6. the successor must select a different typed disposition.

Merely incrementing state revision or republishing snapshot/result bytes changes
`operation_id` but not `operation_key`; the no-op is therefore rejected. The
successor inventory's cumulative consumed-key list is digest-bound and becomes the
explicit proof needed before another local operation may be advertised. Because
the list is append-only, work consumed two or more checkpoints earlier cannot be
resurrected after the immediate predecessor changes.

The current helper `validate_local_work_progress(prior, successor)` enforces basis
advancement and non-reuse. Slice 2 will enforce the same rule beneath the native
writer before/after the actual command.

## PREPARED retry decision

The contract fixture treats API-side authorization records as outside SBE native
truth. The reproduced next retry remains native `PREPARED` until an exact compatible
external-authority request/grant is applied through the constrained executor.

Native `AUTHORIZED`, intent-committed, call-entered, ambiguous, and provider-bound
states remain separate fenced states. Generic ordinary resume receives no authority
to infer or advance them.

## Schemas and public Python surface

- `resources/contracts/local-work-inventory.v1.schema.json`
- `resources/contracts/temporal-lifecycle-contracts.v2.schema.json`
- `build_local_work_inventory`
- `validate_local_work_inventory`
- `validate_local_work_inventory_against_v05`
- `build_lifecycle_inspection_v07`
- `validate_lifecycle_inspection_v07`
- `validate_local_work_progress`
- packaged schema readers for both contracts

Proposed sanitized fixture:

- `fixtures/local-work-inventory.ordinary-resume.proposal.json`

## Qualification v2 decision

Slice 4 will publish a new
`astrowoof.provider_pending_lifecycle_qualification.v2` receipt/schema/reader/CLI.
The existing v1 function, CLI, receipt identity, and historical evidence remain
unchanged as first-authority proof.

## Review questions

1. Are the three initial operation kinds sufficiently closed and correctly aligned
   with durable checkpoint granularity?
2. Is repeating the basis on every member useful defense-in-depth, or should the
   member carry only the inventory digest? Recommendation: retain the explicit
   basis fields for simple consumer validation and operator audit.
3. Is the `source_action_ids` inventory sufficient for API audit while remaining
   non-selectable? Recommendation: yes; the API validates it but invokes only the
   run-level command.
4. Approve lifecycle v0.7 / temporal-contracts v2 naming before Slice 2.

API review identified and this revision closes both the snapshot-renaming bypass
and later semantic resurrection: semantic identity is independent of the invocation
basis, continued local work requires explicit sealed consumption evidence, and the
consumed-key history is cumulative and disjoint from current work.

## Focused evidence

- Slice 0 characterization: 4 passed.
- Slice 1 contract tests: 8 passed, 1 optional `jsonschema` skip on the lean runtime.
- Strict Python mutation coverage includes wrong run/snapshot, operation kind,
  action identity, member basis, inventory digest, lifecycle join, empty local
  work, and local work on a non-local branch.
- Provider/network/spend/retained-QA activity: zero.
