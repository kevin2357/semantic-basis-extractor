# Slice 3 — Bounded Control-Plane Audit and Ownership Decision

## Audit scope

The owner and API review authorized one read-only audit of Erasmus attempts 11
and 12 and their queue/control-plane history. The audit queried only the exact
QA job, attempts, and leases. No R2 object or workspace was read; no provider,
retry, recovery, queue mutation, or deployment occurred.

## Durable result

Attempt 11 was not durably closed:

- attempt `1fcc8448-79eb-4fe2-87c9-49e7e9e7eda1` started at
  `2026-09-14T16:10:27.551104Z`;
- lease `72727d47-c616-4d43-87c3-acb299bd5ca3` remained active until its
  `16:12:27.551104Z` expiry;
- expired-lease collection finished the attempt as `lease_expired` at
  `16:12:30.350400Z`;
- attempt 12 was ordinarily claimed at `16:12:31.295144Z` under a new lease;
- attempt 12 then committed the durable non-retryable
  `native.terminal.review_required` failure.

This disproves an external operator reactivation. The apparently terminal
attempt-11 events were emitted without a corresponding terminal queue write.

## Exact source defect

In `SbeReadingWorker`, the command-bearing `TERMINAL_CLOSEOUT` /
`review_required` branch validates the exact command and sets
`editorial_closeout_result_id`, but unlike the adjacent terminal branches it
does not call `queue.fail()`. After the ingress transaction commits, it invokes
the observer and unconditionally emits:

- `sbe.closeout.completed`;
- `worker.job.failed` with `retryable=false`;
- `worker.lease.released`.

Those events describe a state transition that never occurred. The active lease
therefore expires, and ordinary expired-lease garbage collection schedules the
next attempt because attempt 11 is below the job's maximum-attempt ceiling.

Attempt 12's generic sealed-terminal preflight then follows the adjacent
ordinary terminal branch, which does call `queue.fail()`, explaining why that
attempt is durably failed.

## Observer implication

The duplicate claim does not justify preserving Erasmus's command for later
observation. Correcting the missing attempt-11 queue close prevents attempt 12.
Observation remains authorized only by the exact invocation-bound command on
attempt 11.

The absence of observer success/failure lines remains a telemetry question, not
evidence that the call was skipped: source control reaches the observer before
the misleading terminal event trio. Qualification must separately prove
function entry and logging/transport outcomes.

## Ownership decision for joint review

Both demonstrated runtime defects are API-owned:

1. Didot needs exact, same-job/same-native-run delivery identity carried across
   publication retry after strict ingress authentication. No latest-result
   discovery is allowed.
2. Erasmus needs the command-bearing review branch to commit the same terminal
   queue/capacity transition its emitted events claim, before post-commit
   best-effort observation. No durable review-command carry-forward is needed
   merely to service the now-eliminated successor claim.

SBE emitted both exact typed handoffs and requires no schema or runtime change.
A pure API queue/observer-ordering correction does not alter SBE's Alloy model.

Stop here for joint approval before API implementation.

