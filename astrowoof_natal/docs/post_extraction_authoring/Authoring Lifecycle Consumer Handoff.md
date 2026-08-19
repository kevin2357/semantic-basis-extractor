# Authoring Lifecycle Consumer Handoff

For route-neutral scheduling of exact Responses, exact Batch, and bounded-Natal
Responses, see [Provider Reconciliation Route Parity Handoff](Provider%20Reconciliation%20Route%20Parity%20Handoff.md).

This document defines the supported API-worker boundary for SBE lifecycle
inspection, provider-less denial, closeout, and structured events. Consumers use an
installed pinned wheel and these public surfaces; they do not import SBE internals,
edit `run.json`, parse exception prose, or infer authority from events.

## Installed commands

```text
astrowoof-authoring-lifecycle --run-dir RUN inspect \
  --native-exclusive-access declared

astrowoof-authoring-lifecycle --run-dir RUN deny-providerless \
  --request NEGATIVE_AUTHORIZATION.json

astrowoof-authoring-lifecycle --run-dir RUN deny-providerless-batch \
  --request BATCH_NEGATIVE_AUTHORIZATION.json

astrowoof-authoring-lifecycle --run-dir RUN reconcile-required-denial

astrowoof-authoring-lifecycle --run-dir RUN closeout

astrowoof-lifecycle-smoke --require-installed

astrowoof-provider-pending-qa

astrowoof-semantic-closure --run-dir RUN --resume --provider openai \
  --service-level interactive --bounded-provider-reconciliation
```

Each command prints one typed JSON result by default. Add `--stdout-jsonl` to the
lifecycle command for a stream containing only typed event envelopes followed by
one `sbe.command_result.v1` envelope. Add `--events-jsonl PATH` to append events to a
file outside the authoritative run workspace.

The public Python functions are:

- `astrowoof_natal_authoring.lifecycle.inspect_lifecycle`;
- `astrowoof_natal_authoring.lifecycle.deny_providerless_action`;
- `astrowoof_natal_authoring.lifecycle.deny_providerless_actions`;
- `astrowoof_natal_authoring.lifecycle.reconcile_required_providerless_denial`;
- `astrowoof_natal_authoring.lifecycle.closeout_run`; and
- `astrowoof_natal_authoring.reconciliation.run_bounded_authoring_reconciliation`.

Python callers may inject an `ExecutionEventEmitter`; execution results remain
normal return values and never depend on event delivery.

## Provider-pending capacity release

Lifecycle inspection v0.4 separates short-lived local execution capacity from
durable provider custody. The API may release its worker claim only when
`execution_capacity.checkpoint_safe_for_worker_release` is true and the closed
disposition permits release. It must retain its separately owned reservation and
financial authority for every `provider_custody.actions` member whose
`custody_classification` is `retain_consumer_authority`.

The closed `execution_branch` is the command-selection authority. A provider-only
wait has `provider_continuation_remains=true`,
`local_continuation_remains=false`, and no `local_dependencies`. Before due, its
branch names `provider_reconciliation_cycle` with `eligible_now=false` and the
exact `not_before`. At or after due it names the same command with
`eligible_now=true`; `action_ids` is SBE's bounded next subset (at most four), not
permission for the API to choose members or reconstruct a command. Ordinary local
work alone names `ordinary_resume`. Consumers must reject contradictory branch,
capacity, custody, and continuation fields.

`resume_not_before` is SBE's durable lower-bound recommendation. The API may
schedule later. An earlier bounded cycle returns `not_due`, performs no provider
retrieval, mutates no native bytes, and returns no new result checkpoint.

The bounded command is supported only for exact interactive OpenAI runs. It polls
at most four due, already-known Response IDs in one parallel wave, gives each GET
a maximum 15-second transport timeout, permits no transport retry, and reserves a
20-second total native cycle allowance. It then exhausts newly unblocked local
work and publishes one complete checkpoint before detaching. A known provider ID
is retrieved only; this mode cannot submit a replacement or create a new spend
commitment.

The command must receive the run's frozen authoring and optional-stage provider
configuration through the existing model/routing/polish/critic CLI options. Exact
request binding prevents mismatched configuration from consuming evidence or
submitting work. Consumers should retain their original launch configuration with
the workspace. Batch and bounded-Natal runs return the typed `unsupported`
classification and must not infer capacity release.

Capacity result handling is:

- `detached_provider_pending`: persist the inspection/checkpoint, release local
  capacity, retain every listed provider authority, and schedule no earlier than
  `resume_not_before`;
- `progressed_local`: persist the new checkpoint and consume its fresh inspection;
- `not_due`: release the short claim without replacing the existing checkpoint;
- `awaiting_external_authority`: retain the action and use the existing exact
  authorization or providerless-denial lifecycle operation;
- `review_required`: retain workspace, provider custody, and authority for review;
- `terminal`: consume the native terminal state and follow closeout policy; and
- `unsupported`: retain capacity or enter consumer review.

A publishable delivery can coexist with nonblocking critic/candidate provider
custody. Reader delivery may proceed, but the pending action and its API-owned
authority remain retained until native reconciliation or denial resolves it.

Events remain non-authoritative observations. A bounded CLI checkpoint may emit
`run.detached` followed by `checkpoint.committed`; HTTP status endpoints must read
only the API's validated, persisted mapping of the typed result and inspection.
Lifecycle inspection may additionally emit `lifecycle.branch_selected`, containing
only the native status, capacity disposition, selected command, eligibility,
reason, and bounded counts.

## Required API sequence

1. Restore the complete workspace at its stable logical absolute path.
2. Hold the API-owned fenced lease. SBE does not validate it.
3. Inspect. Persist the supported projection into API-owned state.
4. If exactly one provider-less action should be denied, construct the existing
   single-action v0.1 request. If several actions must share one decision, construct
   one batch v0.1 request containing the shared observation and 1 through 32 exact
   ordered members. Each member binds its complete action identity, closed denial
   reason, and opaque API authority reference.
5. Call the matching single or batch operation and consume its typed result.
6. For a batch, release API authority only when the top-level outcome is `applied`
   or `idempotent_replay`, the exact returned member matches the requested action,
   binding, and authority reference, and that member has `release_eligible: true`.
   Release nothing for every refused batch, including members labeled `eligible`.
   SBE never releases the reservation itself.
7. Retain the exact request, returned digest where applicable, top-level and
   per-member outcomes, `run_transition`, and shared checkpoint as API
   audit/recovery provenance. For newly admitted behavior, require the v0.2 success
   result; v0.1 remains historical-reader compatibility only.
8. Interpret `run_transition` directly. A required external spend refusal yields
   `BUDGET_EXHAUSTED` with an external-spend terminal reason; product denial or
   cancellation yields `POLICY_STOPPED`. Obtain a fresh inspection after every
   first application and require terminal, quiescent, dependency-free native state
   before releasing worker capacity.
9. Call closeout without a denial request.
10. Persist the mapped API lifecycle state. HTTP status endpoints read only API-owned
   persisted authority; they never execute SBE or depend on a live workspace.
11. Apply API cleanup policy only after evaluating the typed closeout, quiescence,
    dependencies, unresolved actions, API lease, and product policy.

Normal lifecycle races are typed results. Exceptions are reserved for unsupported
schema/programmer misuse, unreadable or invalid workspaces where a typed projection
cannot safely be formed, failure to establish closeout exclusivity, or unexpected
implementation failure.

## Packaged contracts and fixtures

Use `astrowoof_natal_authoring.resource_access.read_resource_text()` for installed
resources:

- `contracts/contract-catalog.json`;
- `contracts/authoring-lifecycle-contracts.schema.json`;
- `contracts/execution-event-payload-catalog.v1.json`; and
- sanitized examples under `fixtures/lifecycle/`.

`fixtures/lifecycle/inspection.v0.4.json` is the provider-only not-due example.
`astrowoof-provider-pending-qa` is a provider-free, qualification-only installed-
wheel command; its receipt is diagnostic evidence, never production authority.

The catalog identifies v0.2 as the current single and batch successful
negative-authorization result and identifies v0.1 explicitly as historical reader
compatibility. It also versions inspection, negative-authorization
request/results, action inventory, closeout result, execution event, event payload
catalog, and command result. Reject unsupported authoritative document versions deterministically.
Unknown events are ignored or quarantined and never mutate state.

## Batch provider-less denial example

The complete packaged examples are:

- `fixtures/lifecycle/negative-authorization-result.v0.2.json`;
- `fixtures/lifecycle/batch-negative-authorization-request.v0.1.json`;
- `fixtures/lifecycle/batch-negative-authorization-result.v0.1.json`;
- `fixtures/lifecycle/batch-negative-authorization-result.v0.2.json`;
- `fixtures/lifecycle/batch-negative-authorization-replay.v0.1.json`; and
- `fixtures/lifecycle/batch-negative-authorization-refused.v0.1.json`.

The request shape is:

```json
{
  "schema_version": "astrowoof.provider_negative_authorization_batch_request.v0.1",
  "run_id": "native-run-id",
  "observed": {"operator_state_revision": 21, "snapshot_sha256": "..."},
  "actions": [
    {
      "action_id": "paid_...",
      "binding": {"run_id": "native-run-id", "route": "ella:creative_retry:001"},
      "denial_reason": "reservation_unavailable",
      "external_authority_reference": "api-fence:slot-001"
    }
  ]
}
```

The abbreviated objects above omit required observation and binding fields only for
readability; copy the complete fields from `inspect_lifecycle()` and the packaged
fixture. Unknown fields, empty/oversized batches, invalid values, and unsupported
versions are rejected.

Successful results return the exact canonical `batch_request_sha256`, original
request observation, locked decision basis, ordered action outcomes, complete
post-mutation observation, and shared result checkpoint. A refused result has
`applied: false`, no checkpoint, no release-eligible member, a typed top-level
outcome, and an ordered member assessment. `eligible` means only that the member
passed independently while the batch failed elsewhere; it is never release evidence.

Every newly applied successful single or batch denial returns a v0.2
`run_transition`. `denied_action_ids` identifies every accepted member;
`required_action_ids` is the exact causal subset whose native requiredness produced
terminalization. Do not infer causality from the full denied set.

Exact replay requires the identical complete request, including member order and
original observation timestamp. First application emits ordered per-action denial
events followed by one batch event. Replay emits only the batch replay event. A
refusal may emit one bounded batch diagnostic event. Events contain no bindings or
authority references and remain non-authoritative and failure-isolated.

`DELIVERY_COMPLETE` is a supported context for denying authorized but unconsumed,
never-provider-bound actions. The operation preserves accepted delivery bytes and
does not reopen editorial work. It can run or replay on a complete retained
workspace restored at its stable logical absolute path and never accepts a provider
client.

## Migration from sequential denial

Consumers that currently inspect once and loop over several single-action denial
calls must replace that loop with one batch request. Do not reuse one observation
across sequential mutations: the first successful single-action call correctly
makes that observation stale. The original `deny_providerless_action()` operation
remains supported unchanged for true one-action decisions.

If a batch is interrupted, retry the exact request against the complete restored
workspace. SBE either restarts before mutation, narrowly completes its exact known
write set, or returns idempotent replay. Missing/changed protocol artifacts,
unrelated workspace changes, provider evidence, and ambiguous submission fail
closed. SBE does not provide general snapshot repair.

## Required-action terminal outcomes

An accepted providerless denial is final. `reservation_unavailable` is not a
temporary wait once submitted to SBE; an API intending to wait must retain its
authority and not deny the native action.

| Native condition | Status / terminal outcome | Delivery |
|---|---|---|
| Required `external_authority_denied` or `reservation_unavailable` | `BUDGET_EXHAUSTED` / `budget_exhausted`, with an external-spend reason | Non-publishable unless already accepted |
| Required `product_policy_denied` or cancellation | `POLICY_STOPPED` / `policy_stopped` | Non-publishable unless already accepted |
| Optional stage with frozen `skip` behavior | Nonterminal stage skip | Continue normally |
| Accepted delivery with unused providerless action | Preserve `DELIVERY_COMPLETE` | Publishability unchanged |
| Provider identity, consumption, report, or ambiguity exists | Denial refused or review required | Retain workspace |

`BUDGET_EXHAUSTED` alone does not identify who owned the ceiling. Consume the
closed terminal reason to distinguish API/global authority refusal from SBE's
frozen per-run spend ceiling. Dollar spend remains unrelated to the fifty-claim
semantic-selection budget.

## Retained 0.4.1 recovery

Affected retained 0.4.1 workspaces can be restored at their stable logical
absolute path and passed to normal closeout, normal route resume, or the explicit
provider-free command:

```text
astrowoof-authoring-lifecycle --run-dir RUN reconcile-required-denial \
  --reconciled-at 2026-08-15T23:30:02Z
```

The command prints a fresh typed lifecycle inspection. The Python reconciler
returns the updated native state. Both operate under the lifecycle single-writer
lock and emit `terminal.transitioned` only on the first successful reconciliation;
replay emits no duplicate transition event.

Reconciliation requires a complete valid snapshot, exact v0.4.1 single or batch
denial artifact and binding, no provider/consumption/report/ambiguity evidence,
frozen native requiredness, and no competing delivery/review condition. It writes
`lifecycle/required-denial-terminal-reconciliation.json`, one coherent state
revision, and one snapshot. Interrupted recovery may complete only that declared
write set. Missing, changed, contradictory, optional-only, provider-bound, or
unrelated bytes fail closed; retain those workspaces for review and do not edit
native files.

## Ownership boundary

SBE owns native action state, immutable binding verification, provider identity,
snapshot integrity, provider-less disposition, closeout evidence, and append-only
reconciliation references. The API owns transactional reservations across runs,
account quotas, global circuit breakers, entitlements/product policy, lease fencing,
workspace deletion authority, authoritative billing reconciliation, and HTTP status.

Dollar spend remains distinct from SBE's semantic claim/card-selection budget.
Polling an existing provider operation is not a new commitment. Known or ambiguous
provider work is never providerlessly released or resubmitted by lifecycle closeout.

## Compatibility and limitations

- Current contracts apply to exact-time SBE operator schema v0.9 workspaces.
- Legacy paid runs fail closed unless explicitly migrated through a supported path.
- Workspace restoration requires the original stable logical absolute path.
- Events are at-least-observational and tolerate loss, duplication, delay, and
  reordering.
- Closeout is a verified recoverable multi-file protocol, not filesystem-wide
  atomicity.
- Batch denial is likewise a locked, recoverable all-or-none native protocol, not
  one filesystem transaction across every workspace file.
- API consumers should pin the released wheel and verify its published SHA-256;
  source-tree integration is not supported.
- Unknown-time suppression, variable basis sizes, Quick/Complete policy, hierarchy
  redesign, and critic product policy remain outside this sprint.
