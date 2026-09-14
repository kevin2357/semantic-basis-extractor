# API Review — Slice 3 Ownership Decision

**Approved.** The bounded persistence audit identifies two API defects and no
native/SBE defect.

- Didot requires an API-owned, exact carry-forward of the already validated
  delivery handoff across a publication retry.
- Erasmus requires the command-bearing `review_required` branch to durably
  execute its non-retryable queue close and capacity release before emitting
  terminal-looking events or attempting best-effort observation.

The observed attempt-12 claim was ordinary expired-lease processing after
attempt 11 omitted the durable queue transition. It is not an operator
reactivation and must not motivate generic terminal-result reconstruction or
review-command persistence for a successor.

## Required API implementation fences

1. Keep the delivery handoff bound to the same API run, job, native run,
   result, receipt, and invocation that strict terminal ingress authenticated.
   Reject missing, conflicting, cross-job, cross-run, and newer-result
   candidates. Never discover a latest result.
2. Commit Erasmus's `queue.fail(retryable=False)` and matching capacity release
   atomically before observer invocation, closeout/failed/released events, or
   cleanup. The observer remains post-commit and best-effort.
3. Preserve ordinary generic sealed-preflight behavior: it may authenticate a
   result but cannot impersonate the earlier invocation-bound review command.
4. Prove both routes with provider-free production-path tests, including
   observer exception/non-2xx/disabled behavior and no effect on authoritative
   terminal state.

SBE is not asked to change schema, runtime, package, or Alloy for this repair.
