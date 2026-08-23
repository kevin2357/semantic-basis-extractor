# Provider Economics Transaction Revision Contract Proposal

Date: 2026-08-21
Status: Slice 1 proposal; awaiting joint SBE/API schema and ownership review

## Decision summary

SBE should publish an append-only tape of individual provider-economics
transactions. It should not publish deck, stage, model, profile, or cohort
aggregates.

The proposed contract identity is:

`astrowoof.provider_economics_transaction_revision.v1`

One document is one cumulative revision of one native paid transaction:

- interactive Responses: one paid action for one route/stage/pass/attempt;
- Batch: one paid round, one provider operation, and one global/API authority,
  with ordered member evidence nested below that round; and
- no provider operation is invented for a providerless denial, skipped optional
  stage, or ambiguous identity-less submission.

The existing `native_run_id` plus `native_action_id` is the stable transaction
identity. A redundant content-addressed `transaction_id` may be exposed for
convenience, but it must be derived from those two fields and must not become an
independent identity source.

## Why revisions are required

Provider settlement and editorial disposition occur at different boundaries. A
Response can have durable usage before its pass has been validated, accepted, or
sent to a creative retry. A critic can settle after reader delivery. Therefore a
single final-only row either loses useful early facts or encourages mutation of
previously accepted evidence.

Each revision is a complete cumulative observation. It repeats immutable identity
and cohort fields and adds newly durable facts. This is deliberately not a delta:
an independently validated revision is safer to ingest, replay, retain, and merge
than a patch whose meaning depends on hidden database state.

## Identity and ordering

Required envelope fields:

| Field | Rule |
|---|---|
| `schema_version` | Exact closed value above. |
| `transaction_id` | `pe_txn_` plus a canonical digest of native run/action identity. |
| `native_run_id` | Exact SBE native run identity, never API `GenerationRun.id`. |
| `native_action_id` | Exact paid-ledger action ID. |
| `revision_number` | Positive contiguous integer beginning at 1. |
| `previous_revision_id` | Null for revision 1; exact preceding revision otherwise. |
| `revision_id` | Content-addressed ID computed with this field omitted. |
| `observed_at` | UTC publication observation time; not provider execution time. |

Exact replay means identical canonical bytes and the same `revision_id`. A second
document at the same revision number with different bytes is a contradiction.
Skipped predecessors, stale predecessors, transaction identity changes, and
revision-number regression fail closed.

## Closed top-level shape

The revision contains these closed sections:

1. `transaction_identity`
2. `cohort_identity`
3. `authority_and_commitment`
4. `provider_operation`
5. `usage_and_cost`
6. `timing`
7. `editorial_outcome`
8. `native_outcome`
9. `provenance`

Unknown keys are rejected. Nullable facts are explicit; absence is never encoded
as zero, an empty string, or a guessed default.

## Transaction identity and cardinality

`transaction_identity` includes:

- `route_family`: `exact_natal` or `bounded_natal`;
- `paid_stage`: `authoring_initial`, `creative_retry`, `polish`,
  `qualitative_critic`, or `qualitative_candidate`;
- `provider_mechanism`: `response` or `batch`;
- immutable native operation/route reference;
- pass, attempt, and round identity when applicable; and
- `cardinality_kind`: `single_action` or `batch_round`.

For `single_action`, `members` is empty. For `batch_round`, members are the exact
ordered logical request inventory and do not become separately reservable paid
transactions. Each member contains only its stable member ID, pass/attempt/stage,
request digest, provider custom/member ID, terminal member disposition, and usage
availability/reference. It contains no prompt, output, subject data, full binding,
or authorization document.

## Cohort identity

`cohort_identity` is descriptive comparison evidence, never authority. It includes:

- SBE release and route-contract identity;
- generation/authoring profile ID and profile-manifest digest;
- packaged resource/prompt-bundle digest;
- prompt/request-geometry contract version and digest;
- model, reasoning configuration, service level, and maximum-output policy;
- price-book version; and
- `cohort_completeness`: `complete` or `legacy_unknown`.

The subject-specific request digest remains provenance, not a default aggregation
key. `legacy_unknown` observations must be excluded from automatic calibration and
may be used only for explicitly labeled exploratory reporting.

## Authority and monetary semantics

`authority_and_commitment` records the exact native commitment and safe references
to the external authorization/consumption evidence. It does not reproduce the
authorization document or full request binding.

`usage_and_cost` separates:

- provider-reported token usage;
- SBE-estimated cost computed from that usage and the pinned price book;
- provider-reported monetary cost, only when the provider explicitly supplies it;
- no-provider-work-consumed; and
- usage unavailable / billing reconciliation pending.

The closed settlement disposition is initially proposed as:

- `provider_pending`
- `provider_usage_reported`
- `provider_usage_unavailable_billing_reconciliation_pending`
- `no_provider_work_consumed`
- `submission_ambiguous`

Unavailable or partial Batch usage is never zero. A Batch round is
`provider_usage_reported` only when usage is complete for every potentially
billable member. Otherwise it remains billing-reconciliation-pending.

SBE-estimated money uses integer micro-USD, states its price-book version and
rounding basis, and is not provider-reported or account-authoritative. API-
reconciled billing is intentionally absent. `provenance.api_reconciliation_join`
supplies only the stable native run/action join that lets the API attach its own
account-authoritative reconciliation.

## Timing semantics

Timing facts carry a named basis. The contract must not flatten all latency into
one `duration_ms`.

Proposed fields include:

- native prepared, authorized, submission-intent, provider-ID-durable, provider-
  terminal-observed, reconciliation-complete, and native-settled timestamps;
- create HTTP attempt duration;
- an ordered inventory of retrieval-attempt diagnostic references and durations;
- observed provider-pending interval;
- native action span; and
- provider-reported duration only when supplied by the provider.

Derived durations require both endpoints and must be nonnegative. The observed
pending interval is explicitly an upper bound containing polling/scheduling lag;
it is not represented as provider compute time. Open/null boundaries remain null.

## Outcome separation

Three concepts remain independent:

- `provider_operation`: provider state such as pending, completed, failed,
  cancelled, expired, ambiguous, or identity conflict;
- `editorial_outcome`: not-yet-evaluated, accepted, rejected-invalid,
  retry-prepared, advisory-only, or skipped; and
- `native_outcome`: run/delivery context such as in-progress, delivery-complete,
  delivery-with-warning, review-held, budget-exhausted, policy-stopped, or failed.

A completed provider operation does not imply editorial acceptance. A delivered
deck does not imply that a nonblocking critic has settled. Revisions may fill later
outcome facts without rewriting provider settlement.

## Revision monotonicity

Semantic validation across revisions requires:

- immutable identity, binding digest, provider identity, cohort, commitment, and
  provenance facts remain byte-equal;
- nullable facts may move only from unknown to known;
- accepted usage/cost/timestamp facts may not disappear, decrease, or change;
- provider, editorial, and native states follow their documented partial orders;
- Batch member inventory/order is immutable and member facts only become more
  complete;
- a contradiction produces review/refusal evidence rather than silently minting a
  corrected history; and
- API billing corrections remain API-owned reconciliation revisions joined to the
  native transaction, not mutations of SBE evidence.

If the provider later supplies contradictory usage rather than merely more complete
usage, SBE must retain both raw artifacts and surface a typed integrity/review state.
Version 1 does not permit an in-place native accounting correction.

## Publication and revision milestones

A new revision is emitted only when a durable, consumer-relevant fact changes—not
for every unchanged poll.

Recommended milestones are:

1. durable provider identity or durable ambiguous/no-work terminal fact;
2. provider terminal/usage settlement;
3. editorial disposition;
4. native delivery/closeout disposition; and
5. a newly durable timing fact when it cannot be included in one of the above.

Emission occurs only after the cited ledger, journal, diagnostic, result, snapshot,
and receipt evidence is durable. The observation path is read-only with respect to
provider work and cannot authorize, submit, retrieve, deny, settle, or release an
action.

## Provenance and privacy

Safe provenance references include:

- paid-ledger action and binding digest;
- provider-operation kind/ID;
- native transition journal range/hash;
- immutable execution-result ID/hash;
- snapshot SHA-256 and publication-receipt ID/hash;
- usage artifact and reconciliation diagnostic references; and
- exact Batch round/member manifest digest.

The observation must exclude prompts, model outputs, subject/provider-visible
views, birth data, protected parameters, location evidence, authorization documents,
credentials, HTTP headers, provider request bodies, and full action bindings. A
sentinel privacy test is required.

## API ingestion recommendation

SBE does not choose the API table design. The supported semantics are:

1. validate native publication evidence and the observation schema/semantics;
2. insert the immutable revision using `(transaction_id, revision_number,
   revision_id)` as an idempotency boundary;
3. under a database transaction, require the exact predecessor for revisions after
   1;
4. retain every accepted revision;
5. merge the cumulative revision into an API-owned current transaction projection;
6. join account-authoritative billing by native run/action identity; and
7. derive stage/deck/model/cohort summaries in views or analytics jobs.

The current projection is convenience state. The immutable revision tape and cited
native publication remain the audit evidence.

## Proposed Slice 1 fixtures and validation

Slice 1 implementation should package:

- a Draft 2020-12 closed schema;
- a semantic validator for identities, cardinality, cost/timing bases, and one
  revision in isolation;
- a sequence validator for predecessor and monotonicity rules;
- interactive settlement and editorial-finalization revisions;
- a Batch-round fixture with six members and partial-usage conservative handling;
- providerless, ambiguous, and legacy-unknown fixtures; and
- mutations for identity, predecessor, usage, cost basis, timing, member order,
  provenance, and protected-data leakage.

The accompanying JSON files in `results/` are proposal examples only. They are not
packaged schemas or accepted consumer fixtures.

## Questions for joint review

1. Approve the contract name and cumulative-revision model?
2. Approve native `(run_id, action_id)` as the stable transaction authority, with
   `transaction_id` only a deterministic alias?
3. Approve the proposed emission milestones and no-revision-on-unchanged-poll rule?
4. Should retrieval attempts remain bounded referenced observations, or should each
   attempt also be an independent economics revision? SBE recommends references.
5. Approve round-level Batch transactions with ordered member evidence and
   conservative incomplete-usage settlement?
6. Approve `legacy_unknown` as reportable but excluded from automatic calibration?
7. Does the API require any additional immutable cohort identity before selecting
   its PostgreSQL revision/current-projection design?

