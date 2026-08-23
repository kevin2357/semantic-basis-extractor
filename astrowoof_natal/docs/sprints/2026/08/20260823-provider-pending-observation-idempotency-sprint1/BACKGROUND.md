# Background — Provider-Pending Observation Idempotency

Fresh QA runs proved SBE's initial create route and API external-authority
admission can produce exact six-member wave provider identities. The later
failure is at the persistence/interpretation seam: the API currently treats one
immutable native snapshot as capable of producing only one byte-identical full
lifecycle inspection.

That assumption is incompatible with SBE's existing provider-pending scheduler.
`inspect_lifecycle()` is provider-free and read-only. It projects an inspection
from immutable native evidence plus a caller-supplied `observed_at`. The same
valid snapshot can therefore produce:

- a not-due scheduling decision before `resume_not_before`; and
- a due reconciliation decision after `resume_not_before`.

The provider identities, action inventory, route, binding, and native authority
have not changed. Only the clock-relative command recommendation has changed.
The API currently keys one persisted inspection by snapshot SHA-256 and rejects
the later full document because it is not byte-identical to the first.

## Critical semantic distinction

An unchanged native snapshot does **not** learn that a provider result exists.
Ordinary lifecycle inspection performs no OpenAI retrieval. Actual provider
status, result, usage, failure, or identity evidence changes only through a
supported reconciliation/retrieval operation, after which SBE must durably
checkpoint the new native evidence.

This sprint therefore distinguishes:

1. immutable native checkpoint basis;
2. clock-relative temporal scheduling decision; and
3. newly retrieved provider evidence, which requires a new checkpoint.

The evolving object should be described as a temporal lifecycle/scheduling
observation, not as provider evidence evolving outside native state.

## Current API mismatch

The API's `sbe_lifecycle_inspections` persistence currently has one unique row
per `(authoring_run_id, snapshot_sha256)`. Exact replay compares the complete
inspection JSON. That protects against contradictions in a static model, but it
also rejects the valid `not_due -> due` evolution described above.

SBE must expose the stable and temporal portions explicitly enough that the API
can retain decision-relevant scheduling observations under a defined retention
policy, select a validated current decision using its trusted monotonic clock,
and continue rejecting changed provider identity, action inventory, route,
binding, authority, custody schedule, or regressive time evidence.

## Adjacent external-authority consideration

Lifecycle v0.5 embeds `observed_at` in the observation joined to an
`external_authority_request`. Reinspection can therefore mint a different
request digest for the same prepared actions even when native evidence is
unchanged. The preferred correction is to bind the request to the immutable
checkpoint basis and exact ordered action inventory. Reinspection of one basis
then reproduces the same request digest. A grant remains bound to one exact
request and stale grants fail closed; genuinely time-sensitive authority must
use an explicit validity/expiry field rather than incidental observation time.

## Trusted time and concurrency

Persisted `observed_at` uses one canonical normalized-UTC representation and is
supplied by the API's trusted clock. SBE deterministically evaluates an exact
basis/time pair but does not establish cross-worker ordering with its wall clock.
Repeated identical due decisions are legal and idempotent; API lease and custody
controls prevent duplicate invocation. Provider retrieval that changes native
facts produces a new snapshot and checkpoint basis.
