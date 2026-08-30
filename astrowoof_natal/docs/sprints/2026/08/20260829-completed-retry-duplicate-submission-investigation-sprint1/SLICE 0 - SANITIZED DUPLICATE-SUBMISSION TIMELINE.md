# Slice 0 — sanitized duplicate-submission timeline

## Finding

The retained generation-11 checkpoint is a valid, internally hash-complete
checkpoint that predates both duplicate provider submissions. It contains a mixed
creative-retry state:

- attempt 2 is still `AMBIGUOUS_PROVIDER_SUBMISSION` at the pass layer, while its
  paid action is `WAITING`, has a durable provider identity, and has a completed
  reconciliation observation that has not been reported/fanned in;
- attempt 3 already exists as a distinct `PREPARED` action awaiting authority;
- the most recent sealed result is older than attempt 3 and names only the
  provider-pending predecessor;
- no sealed native result or API checkpoint after attempt 3's preparation was
  retained.

This makes generation 11 a stable replay basis: restoring it always restores the
same new action as providerless and create-capable after ordinary authorization,
while the predecessor's semantic fan-in work remains outstanding.

## Ordered evidence

| UTC | Evidence | Meaning |
| --- | --- | --- |
| `04:10:51–04:10:55` | journal sequences 71–75 | Attempt 2 was authorized, consumed, entered submission, received one durable provider ID, and became pending. |
| `04:13:39` | result `nres_baa071ce080d1201658cb3ec` | Last sealed result is `provider_pending` and includes attempt 2, not attempt 3. |
| `04:14:06.617729` | journal sequence 82 | Attempt 3 / `paid_fb28…` was prepared. This is its only journal record in generation 11. |
| `04:14:46.121770` | API checkpoint coordinate | Generation 11 was stored after preparation but before either affected provider submission. |
| `04:15:03.827783` | API paid-action row | API recorded the affected action as authorized, with no direct v2 admission FK. |
| `04:15:07` onward | sanitized structured logs, outside checkpoint | First identity and completion occurred, followed by `semantic_work_not_consumed`. |
| `04:17:22` onward | sanitized structured logs, outside checkpoint | Restore/retry authorized the same native action and created a second provider operation, followed by the same local-progress refusal. |

The two later provider identities are intentionally retained as contradictory
observations. Neither is selected as canonical.

## Cross-boundary join

The only run-scoped v2 admission in the supplied API evidence belongs to attempt 2
(`paid_258…`). The affected attempt-3 action has neither an ordinary nor v2 direct
admission foreign key. Consequently, the affected invocation did not use the
v2 constrained-dispatch identity that would durably fence `CALL_ENTERED` before
provider I/O. It used the generic ordinary resume / spend-authorization boundary.

The API row never adopted either provider identity and no post-action native
execution receipt exists. Therefore API retry restored generation 11 rather than
the worker's later scratch state. Local `SUBMITTING` and provider-ID persistence in
that discarded scratch could not fence a subsequent invocation.

## Provider-free characterization

`test_completed_retry_duplicate_submission_investigation_slice0.py` exercises the
real `closure.main()` ordinary-resume boundary from a production-shaped mixed
checkpoint. It patches authorization application and ordinary authoring to isolate
the restore/replay seam; it does not claim to exercise the unpatched
`SpendController` or provider adapter. A scripted provider completion is followed
by the real `commit_local_work_progress()` refusal. Restoring the identical
checkpoint and reinvoking the same public boundary produces a second scripted
create for the same action. No network/provider call occurs.

The characterization proves two creates across two restores. It does not claim
that an API retry is itself a native provider identity, nor that the historical
workspace can be repaired automatically. A later regression must exercise the
real call-entry fence and immediate provider-identity durability.

## First violated invariant

The first cross-boundary invariant violation is:

> A create-capable generic ordinary-resume invocation crossed provider call entry
> without first producing an API-retainable native checkpoint/result that fenced
> the exact action against another create after worker scratch was discarded.

The subsequent `semantic_work_not_consumed` is real and causally important: it
prevented normal command-result publication, so API never adopted the first
provider identity. But it is not permission to create again. The unsafe replay
requires both sides of the seam: generic create-capable dispatch without a retained
pre-I/O fence, plus API restoration/reinvocation from the older checkpoint after a
nonzero exit.

## Confidence

- **High:** retained generation-11 native shape, hashes, journal ordering, result
  cutoff, and v2-admission mismatch.
- **High:** provider-free public-boundary reproducer creates twice across two exact
  restores and fails both times at semantic progress.
- **High:** the defect is a combined handoff seam, not evidence that either later
  provider response is canonical.
- **Medium:** the exact API wrapper branch/arguments used for both live invocations;
  this is inferred from the absence of v2 admission and supplied logs and should be
  confirmed from invocation records at Voof-paws 1.
