# Slice 2 — Exact-Route Projection Handoff

Status: implemented and qualified; consumer review requested before Slice 3

## Supported boundary

`project_exact_provider_economics_revision()` accepts validated native exact-run
state, one native spend-ledger action, an explicit publication-observation time,
and optionally that transaction's immediately preceding revision. It is a pure,
read-only projection: it performs no provider I/O, persistence, settlement, or
orchestration.

The return value is either one closed v1 transaction revision or `None`. `None`
means that the supplied native evidence adds no consumer-relevant fact to the
predecessor. In particular, a new polling/publication time by itself does not mint
accounting history.

## Cardinality and authority

- Exact interactive: one transaction per native paid action/pass attempt.
- Exact Batch: one transaction per paid Batch round. Its ordered logical members
  are audit and attribution evidence beneath that one authority; they are not six
  transactions or six API reservations.
- `(native_run_id, native_action_id)` remains authoritative. `transaction_id` is
  derived convenience identity only.

## Settlement distinctions

The projector never converts missing data to zero. It keeps provider pending,
complete usage, terminal provider work with unavailable usage, providerless
no-work, and ambiguous submission separate. A Batch round cannot settle as fully
reported when its durable round disposition says usage remains unavailable.

## API expectation

The API should ingest immutable revisions append-only, enforce predecessor
continuity with the packaged sequence validator semantics, and maintain any
current projection separately. PostgreSQL may merge later revisions into an
API-owned current view, but must retain the individual native transaction/revision
evidence. Provider-reported money, SBE estimates, and API-reconciled billing remain
separate facts.

Slice 2 intentionally does not yet publish a workspace reader/CLI or bounded-route
projection. Those remain Slices 3 and 5.
