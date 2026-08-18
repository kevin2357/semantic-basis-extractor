# Bounded Batch Slice 5 Consumer Handoff

## Supported boundary

Bounded Batch is supported only for native route contract
`astrowoof.bounded_natal.authoring_run.v2`, provider mechanism `batch`, and stages
`authoring_initial` and `creative_retry`. Legacy v1 one-operation workspaces remain
machine-readably unsupported and are not reinterpreted.

The command surface remains `astrowoof-run-bounded-natal --service-level batch`.
Pending ordinary authoring and reconciliation return exit code 3; consumers must use
the public lifecycle/result state rather than exit code alone.

## Authority aggregation

- One Batch round equals one SBE paid action.
- The action route is `bounded_natal.v2:batch-round-NNN`.
- One API global reservation should bind that action/round.
- `aggregate_maximum_output_tokens` equals the sum of member maxima.
- `aggregate_commitment_micro_usd` copies the immutable SBE action commitment.
- Members bind `custom_id`, pass, attempt, stage, request digest, packet digest,
  model, and maximum output. They are audit and usage-settlement evidence, not
  separate global-reservation authority.

## Restart and custody

Before Batch identity exists, submission remains subject to exact authorization and
ambiguity rules. After `batch_id` is durable, normal resume or neutral reconciliation
may only retrieve that Batch. It must not upload or create another Batch.

The reconciliation adapter requires both `bounded_batch_provider` and
`bounded_batch_transport`. Retrieval is bounded by the existing Batch 40-second
cycle contract. Early cycles return `not_due` without mutation.

## Member and cost outcomes

- Successful members are hydrated and accepted independently.
- Error-file or locally rejected members become pass-local creative-retry members.
- A provider-terminal failed/expired/cancelled round fails its affected members and
  permits policy-bounded pass-local retry.
- Member inventory or identity conflict is `output_invalid`/review behavior and
  retains consumer authority; it does not imply endless provider polling after
  terminal files are durable.
- Usage complete for every potentially billable member:
  `provider_usage_reported`.
- Usage absent for any potentially billable member, including an error-file member
  or one member in an otherwise reported round:
  `provider_usage_unavailable_billing_reconciliation_pending`.
- Before provider work: `no_provider_work_consumed`.

SBE never settles an aggregate action from a partial member total. The API must
never treat unavailable usage as reported `$0.00`; it owns authoritative billing
reconciliation and decides when its reservation may settle or release.

## Optional stages

Polish, qualitative critic, and qualitative candidate remain interactive Responses
operations even when initial authoring used Batch. This Slice does not batch them.

## Review request

Please verify the review fixture's route/action/round cardinality, cost and custody
semantics, partial-member retry trace, and historical v1 refusal. Slice 6 will not
begin until this handoff is accepted.
