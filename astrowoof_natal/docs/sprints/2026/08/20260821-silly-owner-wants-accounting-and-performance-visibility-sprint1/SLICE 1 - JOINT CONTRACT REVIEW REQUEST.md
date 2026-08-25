# Slice 1 — Joint Provider-Economics Contract Review Request

Date: 2026-08-24
Status: API approved with conditions; SBE implementation in progress

## Review boundary

SBE proposes a closed, append-only, transaction-grained observation contract:

`astrowoof.provider_economics_transaction_revision.v1`

One transaction is one interactive paid action or one Batch round. Batch members
remain ordered evidence beneath one round-level paid authority. SBE will not emit
deck, stage, model, profile, or cohort aggregates; the API may derive those from the
immutable transaction tape.

The observation is evidence only. It cannot authorize, submit, retrieve, deny,
settle, retry, close, publish, release capacity, or alter account billing.

## Decisions requested

Please approve or revise these seven points before SBE packages the schema:

1. The contract name and cumulative-revision model.
2. Native `(native_run_id, native_action_id)` as stable authority, with
   `transaction_id` only a deterministic alias.
3. Emission only for newly durable consumer-relevant facts; unchanged polls mint no
   revision.
4. Retrieval attempts remain bounded referenced timing observations rather than
   independent economics transactions/revisions.
5. Batch is one round-level transaction with ordered member evidence and
   conservative incomplete-usage settlement.
6. `legacy_unknown` cohorts are reportable but excluded from automatic calibration.
7. Whether the API needs another immutable cohort dimension before selecting its
   revision/current-projection persistence design.

## Proposed revision join

- `revision_number` starts at 1 and is contiguous.
- `previous_revision_id` is null only for revision 1 and otherwise names the exact
  accepted predecessor.
- `revision_id` is content-addressed canonical identity.
- Exact replay is byte-identical.
- Later revisions are cumulative: accepted provider identity, usage, money, timing,
  cohort, authority, cardinality, and provenance facts cannot disappear or change.
- Provider settlement may be followed by editorial and native-finalization
  revisions without rewriting the earlier settlement evidence.

API ingestion should retain every accepted revision and may transactionally merge
it into an API-owned current projection. Account-authoritative billing remains a
separate API-owned reconciliation joined by native run/action identity.

## Closed semantic distinctions

- unavailable usage is not zero usage or zero cost;
- partial Batch usage is billing-reconciliation-pending;
- SBE-estimated micro-USD is not provider-reported money or account billing;
- provider completion is not editorial acceptance;
- delivery does not imply a nonblocking critic has settled;
- observed provider-pending time includes scheduler/polling lag and is not provider
  compute time; and
- no provider operation is invented for providerless denial, optional skip, or an
  identity-less ambiguous submission.

## Privacy and authority

The observation excludes prompts, outputs, subject views, birth/location data,
protected parameters, credentials, headers, request bodies, authorization
documents, and complete action bindings. It carries bounded identities, digests,
usage/cost/timing facts, outcome classifications, and immutable evidence references.

The implementation gate remains closed until SBE, API, and owner agree on the
contract and ownership decisions above.

## Review disposition

API approved all seven decisions with these binding refinements:

- retrieval diagnostics expose count, first/last observation, bounded aggregate
  HTTP duration, up to 16 ordered references, and explicit overflow;
- Batch members retain provider-supplied usage/cost only when genuinely available;
  v1 performs no proportional allocation;
- cohort identity explicitly commits to execution topology and carries a canonical
  digest of the complete cohort section;
- publication time, provider settlement time, provider completion time, and
  provider-pending wall time remain semantically distinct; and
- fixtures must prove editorial/native follow-up revisions, replay, predecessor
  gaps, contradictions, partial Batch usage, and privacy-sentinel exclusion.

The joint gate is therefore open for the Slice 1 schema, validators, and fixtures.
