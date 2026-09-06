# Slice 2 — SBE Native Replay Input

## Status

SBE's provider-free half of Slice 2 is complete. The historical API revision
replay and one-slot allocation/claim result remain API-owned and pending. No
runtime policy or public contract changed.

## Frozen native boundary

The focused production-path tests establish the exact documents the API replay
must consume:

| Native condition | Final disposition | Positive permission |
|---|---|---|
| Known provider identities; none due | `release_until_due` | Defer to exact `resume_not_before`; no native work now |
| Provider retrieval is due | `continue_local_cycle / provider_reconciliation_due` | Retrieve only the ordered `execution_branch.action_ids` |
| Completed provider evidence is durable | `continue_local_cycle / local_work_ready` | Perform the advertised deterministic local operation |
| Six provider actions due; cycle cap four | `continue_local_cycle / provider_reconciliation_due` | Retrieve the canonical four-member subset; retain the two-member due suffix |

The six-member fixture makes the bounded case concrete. Due-time ordering and
then action identity select provider responses `1,4,5,6`; actions `2,3` remain
immediately due. The final public inspection names exactly `2,3` as the next
branch. It would be false to translate that result to `release_until_due`.

## Safety and determinism evidence

- A not-due inspection and reconciliation attempt perform zero retrievals and
  do not mutate the workspace.
- A due cycle addresses durable provider identities only; it has no provider
  create surface.
- Repeated inspection at the same observation time is byte-for-byte stable and
  nonmutating.
- Moving the observation clock across the due boundary changes only the
  documented time-relative projection fields.
- The four-member cap is deterministic and leaves the exact two untouched
  actions visible in both native state and the final public branch.
- Existing parallel-workspace characterization proves no cross-run native
  process dependency; SBE does not own the API allocation or next-claim choice.

## Focused verification

```text
python -m unittest \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_provider_pending_observation_idempotency

Ran 66 tests in 13.635s
OK (skipped=1 expected optional-schema test)
```

## Joint replay handoff

The API harness must now consume these validated final meanings while recording
allocation owner, eligible set, `available_at`, next claim, provider-operation
counts, and due-time lateness. Its required historical comparisons remain:

1. Sprint 58 parent versus release tree as an equality/terminal-precedence
   negative control.
2. `d451a88` versus `8c389b3`, with separate healthy provider-pending and
   retry-ceiling cells.

The SBE evidence neither grants a cooperative fairness yield during
`continue_local_cycle` nor forbids API from rotating capacity at some other
jointly proven durable boundary. That policy question remains intentionally
open until the API replay result is reviewed.

