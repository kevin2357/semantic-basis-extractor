# Slice 2: Durable Reconciliation Timing and Checkpoint Projection

Status: implementation complete; pending Kevin's Slice 2 gate review.

## Native timing evidence

Every newly recorded interactive provider operation now receives durable
`provider_reconciliation` evidence in the paid-action ledger before provider
waiting can be published:

```json
{
  "policy_version": "astrowoof.provider_reconciliation_policy.v0.1",
  "provider_retrieval_attempt_count": 0,
  "last_attempt_at": null,
  "last_outcome": "provider_identity_recorded",
  "resume_not_before": "<provider identity recorded time + 15 seconds>"
}
```

The frozen delay sequence after retrieval attempts is
`15 -> 30 -> 60 -> 120 -> 240 -> 300 -> 300...` seconds. Attempt timestamps
cannot move backwards. Completed/provider-failed outcomes clear the next due time;
pending and transport-warning outcomes retain it. Slice 3 will own the retrieval
operation that advances this evidence.

## Inspection v0.2

`inspect_lifecycle()` and the public CLI now emit lifecycle inspection v0.2. The
projection remains read-only and derives:

- one execution-capacity disposition;
- checkpoint release safety;
- earliest native lower-bound resume time;
- ordered next action IDs, bounded to four;
- immutable action stage and durable provider ID;
- provider-custody and consumer-authority retention classification.

Multiple actions fan in by `(resume_not_before, action_id)`. A due action makes
local execution runnable but never releases provider custody or consumer
authority. A future due time permits `release_until_due` only when the complete
snapshot validates and exclusive access is established or declared.

## Fail-closed boundaries

- A legacy provider-bound action without the new timing evidence produces
  `unsupported_retain_capacity` and retains consumer authority.
- Batch actions cannot opt into interactive parity merely by carrying timing-like
  data; they remain fail-closed pending their explicit Slice 4 classification.
- A state write observed before matching snapshot publication produces
  `retain_for_review`; `checkpoint_safe_for_worker_release` is false.
- Ambiguous provider submission, invalid snapshot, or absent exclusivity cannot
  produce capacity-release authority.
- Lifecycle inspection v0.1 remains packaged as a historical readable schema, but
  cannot authorize capacity release.

SBE describes native custody retention only. The API remains authoritative for
literal reservations, dollar exposure, quotas, and local worker allocation.

## Gate evidence

Focused lifecycle, timing, consumer CLI, and known-provider tests passed 31 tests.
The first complete-suite pass found only two historical v0.1 assertions in the
consumer CLI tests; both were updated to the approved v0.2 public contract and the
focused rerun passed. After adding explicit Batch fail-closed coverage, the final
complete suite passed all 321 tests in 148.808 seconds. No provider operation or
paid work occurred.
