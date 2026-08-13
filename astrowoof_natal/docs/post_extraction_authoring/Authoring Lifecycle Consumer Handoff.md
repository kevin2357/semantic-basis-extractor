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

astrowoof-authoring-lifecycle --run-dir RUN closeout

astrowoof-lifecycle-smoke --require-installed
```

Each command prints one typed JSON result by default. Add `--stdout-jsonl` to the
lifecycle command for a stream containing only typed event envelopes followed by
one `sbe.command_result.v1` envelope. Add `--events-jsonl PATH` to append events to a
file outside the authoritative run workspace.

The public Python functions are:

- `astrowoof_natal_authoring.lifecycle.inspect_lifecycle`;
- `astrowoof_natal_authoring.lifecycle.deny_providerless_action`; and
- `astrowoof_natal_authoring.lifecycle.closeout_run`.

Python callers may inject an `ExecutionEventEmitter`; execution results remain
normal return values and never depend on event delivery.

## Required API sequence

1. Restore the complete workspace at its stable logical absolute path.
2. Hold the API-owned fenced lease. SBE does not validate it.
3. Inspect. Persist the supported projection into API-owned state.
4. If a provider-less action should be denied, construct an exact v0.1 request
   bound to the inspected run/action/binding/revision/snapshot and opaque API
   authority reference.
5. Call denial and consume its typed result.
6. Only `applied` or exact `idempotent_replay` can support API reservation release
   evaluation. SBE never releases the reservation.
7. Obtain a fresh inspection after every mutation.
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

The catalog versions inspection, negative-authorization request/result, action
inventory, closeout result, execution event, event payload catalog, and command
result. Reject unsupported authoritative document versions deterministically.
Unknown events are ignored or quarantined and never mutate state.

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
- API consumers should pin the released wheel and verify its published SHA-256;
  source-tree integration is not supported.
- Unknown-time suppression, variable basis sizes, Quick/Complete policy, hierarchy
  redesign, and critic product policy remain outside this sprint.
