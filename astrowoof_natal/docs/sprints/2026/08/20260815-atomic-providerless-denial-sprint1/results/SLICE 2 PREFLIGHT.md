# Slice 2 Locked All-or-None Preflight

Status: complete; pending review and commit

## Result

SBE now has an internal batch preflight used to prove the decision boundary before
Slice 3 adds mutation. It:

- validates the strict request shape, values, closed reasons, immutable bindings,
  authority-reference bounds, and 1-through-32 member count before workspace access;
- acquires the existing cross-process lifecycle/spend lock exactly once;
- loads one native state and derives one validated inspection/decision basis while
  holding that lock;
- resolves and evaluates every requested member without mutation;
- returns the ordered resolved native action set only when every member is eligible;
  and
- otherwise returns one schema-valid typed batch refusal with zero release-eligible
  members and no mutation checkpoint.

The helper remains internal in this slice. The supported public
`deny_providerless_actions()` surface will wrap the same under-lock preflight and
mutation in Slice 3; exposing an incomplete preflight-only public operation would
create the wrong consumer contract.

## Refusal behavior

Tests cover:

- stale revision/snapshot observation;
- one ineligible member among otherwise eligible members;
- duplicate and unknown action IDs;
- cross-run/immutable binding mismatch;
- provider consumption, provider identity, provider evidence, and identity-less
  ambiguous submission;
- incomplete/changed workspace snapshot;
- failure to establish the single-writer lock; and
- malformed request/programmer errors before workspace access.

Provider-bound evidence is evaluated before shared observation staleness and
therefore retains its more specific safety outcome. A member that independently
passes while another refuses is `eligible` but never release eligible. A shared
precondition failure marks members `not_evaluated`.

## Mutation proof

Every normal refusal test hashes all authoritative workspace files before and after
preflight. Hashes are identical. The lock file is intentionally non-authoritative
and snapshot-excluded, consistent with the existing lifecycle contract.

The successful preflight is also byte-read-only. It confirms that a terminal
`DELIVERY_COMPLETE` workspace with two authorized, unconsumed creative retries can
produce one eligible ordered decision set under established exclusivity.

## Gate evidence

- Focused batch/contract suite: 21 passed.
- Full repository suite: 285 passed.
- Provider operations: 0.
- Paid spend: $0.
- API key: not used.
