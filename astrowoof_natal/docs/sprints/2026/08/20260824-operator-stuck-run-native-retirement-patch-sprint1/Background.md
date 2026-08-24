# Background — Native Stuck-Run Retirement

The API needs a general, auditable way to retire an exact quiescent stuck run
without deleting its history. API can release its own job, lease, capacity, and
unspent authority, but it cannot truthfully terminalize an SBE workspace by
itself.

This patch supplies the native half of the shared control. It is not a generic
resume, retry, or force-transition API. It only accepts a demonstrably
retirement-quiescent, non-provider-pending, non-provider-ambiguous lifecycle
state and records a supported terminal operator retirement. Retirement quiescence
means the checkpoint is stable and contains no active, provider-backed, ambiguous,
or unresolved action; it may still have status-derived future local continuation
that the operator is explicitly abandoning. Provider-pending work remains on
retrieval/reconciliation-specific paths.
