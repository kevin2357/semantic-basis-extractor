# Authoring Lifecycle Consumer Handoff

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

astrowoof-authoring-lifecycle --run-dir RUN closeout

astrowoof-lifecycle-smoke --require-installed
```

Each command prints one typed JSON result by default. Add `--stdout-jsonl` to the
lifecycle command for a stream containing only typed event envelopes followed by
one `sbe.command_result.v1` envelope. Add `--events-jsonl PATH` to append events to a
file outside the authoritative run workspace.

The public Python functions are:

- `astrowoof_natal_authoring.lifecycle.inspect_lifecycle`;
- `astrowoof_natal_authoring.lifecycle.deny_providerless_action`;
- `astrowoof_natal_authoring.lifecycle.deny_providerless_actions`;
- and `astrowoof_natal_authoring.lifecycle.closeout_run`.

Python callers may inject an `ExecutionEventEmitter`; execution results remain
normal return values and never depend on event delivery.

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
7. Retain the exact batch request, returned request digest, top-level and per-member
   outcomes, and shared checkpoint as API audit/recovery provenance. Obtain a fresh
   inspection after every first application.
8. Call closeout without a denial request.
9. Persist the mapped API lifecycle state. HTTP status endpoints read only API-owned
   persisted authority; they never execute SBE or depend on a live workspace.
10. Apply API cleanup policy only after evaluating the typed closeout, quiescence,
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

The catalog versions inspection, single and batch negative-authorization
request/results, action inventory, closeout result, execution event, event payload
catalog, and command result. Reject unsupported authoritative document versions deterministically.
Unknown events are ignored or quarantined and never mutate state.

## Batch provider-less denial example

The complete packaged examples are:

- `fixtures/lifecycle/batch-negative-authorization-request.v0.1.json`;
- `fixtures/lifecycle/batch-negative-authorization-result.v0.1.json`;
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
