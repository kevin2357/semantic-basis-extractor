# Slice 1 — Provider Economics Consumer Handoff

Status: SBE contract candidate ready for API review

## Public contract

Contract identity:

`astrowoof.provider_economics_transaction_revision.v1`

Packaged schema:

`provider-economics-transaction-revision.v1.schema.json`

Public Python readers and validators:

- `read_provider_economics_schema()`
- `read_provider_economics_fixture(name)`
- `read_provider_economics_mutation_corpus()`
- `validate_provider_economics_revision(value)`
- `validate_provider_economics_revision_sequence(values)`
- deterministic transaction, cohort, and revision identity helpers

Python validation is authoritative even when optional `jsonschema` is unavailable.

## Ingestion semantics

One observation is one cumulative revision of one native paid transaction. The
transaction is one interactive paid action or one Batch round. Batch members are
ordered settlement/quality evidence beneath that one authority; they are not
separate API reservations or native transactions.

The API should retain every accepted revision and may transactionally maintain a
current projection. For revisions after 1 it must require the exact predecessor.
Exact replay is byte-identical. A revision-number collision, skipped predecessor,
identity change, or contradiction fails closed.

Provider settlement may be revision 1 and editorial/native finalization later
revisions. Later cumulative documents repeat accepted evidence and add newly
durable facts. PostgreSQL merge-updates are appropriate for the current projection;
they must not replace immutable revision retention.

## Money and usage

- `sbe_estimated_micro_usd` is SBE's estimate from provider-reported usage and the
  named price book.
- `provider_reported_micro_usd` exists only when the provider reports money.
- API-reconciled account billing remains API-owned and joins through exact native
  run/action identity.
- Unknown/unavailable is never represented as zero.
- Partial Batch usage remains billing-reconciliation-pending.
- Member usage/cost appears only when provider-supplied; v1 performs no allocation.

## Timing

`observed_at` is revision publication observation time. It is not provider
completion, settlement, or compute time. Observed provider-pending time includes
polling and scheduling lag. Retrieval summary exposes count, first/last observation,
bounded aggregate HTTP duration, up to 16 references, and explicit overflow.

## Cohorts and privacy

The canonical cohort digest covers release, route contract, generation profile,
resource/prompt bundle, request geometry, execution topology, model, reasoning,
service level, output policy, and price book. `legacy_unknown` is reportable but not
eligible for automatic calibration.

The contract has no place for prompts, responses, subject views, birth/location
data, protected parameters, headers, credentials, authorization documents, or full
bindings. The mutation corpus proves unknown protected-data fields fail closed.

## Fixture inventory

- interactive settlement → editorial finalization → native finalization sequence;
- partial-usage Batch round;
- providerless/no-work;
- ambiguous submission;
- legacy-unknown cohort; and
- seven closed refusal mutations covering shape, identity, cohort, member
  allocation, false settlement, retrieval accounting, and canonical time.

Fixture hashes are frozen in `results/slice1-consumer-fixture-manifest.json`.

## Review questions

1. Does the API accept the exact field vocabulary and cumulative merge semantics?
2. Are the fixture and mutation surfaces sufficient for API schema/persistence work?
3. Does API require a CLI export in Slice 5 in addition to the public Python reader?

No runtime projection occurs until later route slices. This Slice 1 surface cannot
perform provider I/O, mutate a workspace, or create execution/account authority.
