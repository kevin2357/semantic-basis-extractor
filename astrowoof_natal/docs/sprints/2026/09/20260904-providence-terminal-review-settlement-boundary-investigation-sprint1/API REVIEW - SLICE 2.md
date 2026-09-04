# API review — Slice 2 provider-free settlement qualification

## Decision

**Approved.** This is sufficient as the public SBE fixture and identity surface
for API's providerless-denial settlement implementation. It represents the
actual Providence seam without recreating an API-private state machine.

## Why the fixture is sufficient

- The v1 receipt is a stable semantic consumer fixture: it freezes the exact
  eight-action topology, singleton polish denial inventory, empty
  reconciliation inventory, prohibited provider creation, and final-custody
  successor.
- The v2 receipt supplies the identity material API needs to bind its durable
  precursor and settlement record: precursor/successor result and receipt IDs
  and digests, action-inventory, snapshot, checkpoint-basis, denial request,
  action binding, denial artifact, and denial snapshot identities.
- Refusal coverage is correctly pre-mutation for wrong action/binding and stale
  observation. Exact replay is inert; changed replay authority refuses. Those
  are the native half of API's interruption/replay fence.
- The qualification distinguishes editorial `review_required` from custody
  `final`: native editorial review is preserved, but the successor's full
  action inventory is settled. That is exactly the distinction API needs before
  it can consider its own terminal closeout policy.
- Zero create, retrieval, and transport counts prevent this fixture from
  accidentally normalizing an unsupported retry/reconciliation path.

## API consumer guardrails

API will treat the fixture's `inspection_terminal` and `closeout_terminal` as
native-qualification facts only. They never independently authorize API run/job
terminalization, lease release, reservation cleanup, or spend handling. API
must first validate and persist the precursor, record an idempotent exact
settlement intent, invoke SBE using the full exact authority, validate and
ingest the successor, and independently apply its own closeout policy.

The API implementation must reject any v2 identity mismatch, stale predecessor,
or replay whose persisted settlement identity differs. It must also make zero
provider calls on this route.

## Release qualification

Installed-wheel qualification is approved. This is additive package surface,
but it is a necessary release-pair dependency for API's forthcoming consumer
and should be exercised from the built wheel before any release decision.

No live Providence settlement, recovery, deployment, or runtime semantic change
is authorized by this approval.
