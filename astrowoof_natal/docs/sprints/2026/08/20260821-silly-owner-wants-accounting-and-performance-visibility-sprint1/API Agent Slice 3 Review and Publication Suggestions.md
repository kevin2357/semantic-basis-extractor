# API Agent Slice 3 Review and Publication Suggestions

Date: 2026-08-24  
Status: approved to proceed to timing semantics and public-export preparation

## Decision responses

1. **One authority per Batch round — approved.** A Batch round is the native
   provider/settlement transaction. Ordered members are evidence beneath that
   one transaction, never six API reservations, six independently billed facts,
   or six inferred cost allocations.

2. **Provider-supplied member usage only — approved.** Null is the correct
   representation when the provider does not attribute member usage. The API
   must not proportionally allocate round usage/cost across members, including
   for dashboards or calibration; that would turn an analytic convenience into
   false financial evidence.

3. **Bounded v1 refusal — approved.** Refusing legacy bounded v1 is safer than
   reconstructing topology after the fact. Such work may remain observable as
   `legacy_unknown`, but it must not silently become calibration-grade evidence.

4. **Four-route matrix — sufficient for the next slices.** Exact/bounded ×
   interactive/Batch is the right parity boundary. The next timing and export
   work should preserve route-specific topology while holding the shared
   transaction/revision semantics invariant.

## API ingestion requirements to retain in the handoff

- Treat `(transaction_id, revision_number)` as the immutable revision key and
  retain every validated revision append-only.
- Maintain a separate current projection only as a transactional derivative;
  it must never replace immutable revision history.
- Require exact predecessor for a new revision and make byte-identical replay
  idempotent. Refuse skipped, conflicting, or identity-changing revisions.
- Preserve semantic nulls: unknown provider usage/money/timing is not zero and
  is not eligible for automatic cost calibration.
- Keep `sbe_estimated_micro_usd`, `provider_reported_micro_usd`, and future
  API-reconciled account billing separate. No one field substitutes for another.
- Keep native transaction identity separate from API policy authority. The
  projection cannot approve, settle, release, deny, or reconstruct spend.

## Export recommendation

Provide both the packaged Python reader/validator and a provider-free CLI export
or validation path in Slice 5. Python is the primary ingestion integration; the
CLI is valuable for reproducible operator diagnostics, fixture qualification,
and examining an installed wheel without writing a one-off consumer script.

## Additional qualification cases

Before publication, include explicit tests that:

- member ordering changes refuse even where the enclosing Batch-round identity
  is unchanged;
- a missing/partial provider-usage case remains unknown through later editorial
  revisions unless native evidence genuinely changes;
- a later editorial/native revision cannot alter accepted provider settlement
  identity, usage, cost basis, or timing evidence; and
- public artifacts exclude prompts, response text, subject/location data,
  headers, credentials, full authority bindings, and provider payloads.

This gives API a stable data-source contract for later PostgreSQL persistence and
analytics work without prematurely deciding API dashboards, calibration policy,
or billing reconciliation.
