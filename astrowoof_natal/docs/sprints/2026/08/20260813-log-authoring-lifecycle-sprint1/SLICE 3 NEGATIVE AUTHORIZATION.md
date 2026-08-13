# Slice 3 Negative Authorization

Status: complete, 2026-08-13

`astrowoof_natal_authoring.lifecycle.deny_providerless_action()` applies one exact
negative authorization under SBE's existing cross-process spend-consumption lock.
The operation has no provider parameter or provider-client access.

## Applied boundary

An action may become `DENIED_PROVIDERLESS` only when all of these remain true under
the acquired single-writer lock:

- the request schema and closed denial reason are supported;
- the run ID and action ID identify one exact native action;
- the complete immutable binding matches;
- the request observation still identifies the same revision, snapshot, logical
  root, and validation facts, with only documented exclusivity strengthening;
- the action is `PREPARED`, or `AUTHORIZED` without consumption;
- no provider identity, provider evidence, consumption, or ambiguous submission
  boundary exists; and
- the workspace snapshot is complete and valid.

The mutation preserves the original positive authorization when one existed,
records that fact explicitly, appends the native negative-authorization record to
the action, writes a durable result artifact under
`lifecycle/negative-authorizations/`, advances the native state revision, and
publishes a complete validated snapshot.

`release_eligible` is evidence for the API. SBE does not release an API reservation,
interpret the opaque external authority reference, or validate API lease semantics.

## Refusal and races

Refusals are strict `astrowoof.provider_negative_authorization_result.v0.1`
documents with `applied: false`, no result checkpoint, a closed outcome, and closed
review reasons. Authoritative workspace bytes remain unchanged. The lock file is
intentionally non-authoritative and excluded from the snapshot contract.

Provider consumption, identity, and reported evidence take precedence over a
generic stale-observation classification. This makes a submission race
machine-distinguishable and prevents release even when the provider transition also
advanced the revision/snapshot. `SUBMITTING` without identity is explicitly
ambiguous and can never be denied providerlessly.

Failure to acquire the spend lock returns `exclusivity_not_established`. Binding,
run/action, revision, snapshot, and workspace mismatches fail closed without native
mutation.

## Replay and multiple actions

Repeating the exact original request after a successful denial returns
`idempotent_replay`, the preserved semantic disposition, and the existing durable
artifact/checkpoint without another state write. A changed denial reason, authority
reference, request observation, or binding is not considered the same request.

In a multi-action ledger, denial targets only the exact bound action. Presentation
order does not authorize execution, and unrelated prepared actions remain unchanged.

## Durable-write boundary

The native result spans `run.json`, public/request projections, the result artifact,
and `workspace-snapshot.json`; the filesystem does not provide one atomic commit
across all of these files. Atomic individual-file replacement prevents torn JSON,
and the snapshot contract makes interruption between files fail closed rather than
silently blessing a partial mutation. Slice 4's required crash/restart tests will
exercise every durable-write boundary and define supported closeout recovery for
interrupted mutations. This slice does not claim stronger multi-file atomicity.
