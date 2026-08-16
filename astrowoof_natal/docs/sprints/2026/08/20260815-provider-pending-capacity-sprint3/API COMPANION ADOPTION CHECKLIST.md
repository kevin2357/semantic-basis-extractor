# AstroWoof API Companion Adoption Checklist

Use only the installed public Python/CLI interfaces and packaged strict contracts.

- [ ] Require lifecycle inspection v0.2 before releasing local capacity; treat
  v0.1 or unknown versions as retain/unknown.
- [ ] Validate and persist the complete inspection and cycle result into API-owned
  PostgreSQL state before acknowledging the worker result.
- [ ] Release a short capacity allocation only when SBE reports an allowed closed
  disposition and `checkpoint_safe_for_worker_release: true`.
- [ ] Retain the API reservation/financial authority for every exact action with
  `custody_classification: retain_consumer_authority`.
- [ ] Schedule one delayed reconciliation per native run at or after
  `resume_not_before`; do not create one API queue task per provider action.
- [ ] Treat `not_due` as a successful nonmutating detach and retain the prior
  checkpoint.
- [ ] Invoke bounded reconciliation with the original frozen provider routing,
  model, reasoning, output, polish, critic, and candidate configuration.
- [ ] Never turn a known provider ID into a new submission. Retain identity-less
  ambiguity for review.
- [ ] Persist each returned checkpoint before releasing the worker lease.
- [ ] Keep HTTP status endpoints on API-persisted authority only; never execute SBE
  or read a live worker filesystem during a status request.
- [ ] Allow reader delivery when SBE says delivery is publishable, even if a
  nonblocking critic/candidate remains in custody; retain its authority separately.
- [ ] Treat Batch, bounded Natal, unsupported stages, invalid snapshots, identity
  conflicts, and timing-free legacy work as retain/review rather than release.
- [ ] Preserve API ownership of leases, admission, capacity allocation,
  reservations, global spend policy, billing reconciliation, cancellation, and
  publication.
- [ ] Qualify two provider-pending API runs releasing local slots while a third
  reading proceeds, with reservations and native provider IDs unchanged.
- [ ] Test crash/restore after API persistence and before/after capacity release,
  plus stale lease, duplicate delayed message, and later-than-due scheduling.
