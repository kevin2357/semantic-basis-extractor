# API review — Slice 0

## Decision

Slice 0 is approved. The three sufficiency classifications are correct:

1. **Public semantic sufficiency:** complete for the general settlement-gap
   diagnosis.
2. **Exact-artifact sufficiency:** incomplete for certifying or settling
   Providence itself.
3. **Fixture sufficiency:** complete for building the provider-free,
   production-shaped eight-action scenario.

SBE may now build that provider-free fixture and its public-validator coverage.
It may cover all five valid v0.2 finalities as a contract matrix, while any
future runtime correction stays narrowly scoped to
`providerless_denial_required` unless another shape is independently approved.

## Exact-evidence route

API cannot supply a separate durable exact result/receipt export for Providence.
The worker captured the invocation command envelope in process memory, then
terminal ingress read the exact sealed workspace artifact. Its current order is
strictly:

1. read and validate exact result/receipt;
2. classify the disposition; then
3. persist the projection.

The unsupported-disposition exception occurred at step 2, before step 3.
Therefore no database projection/receipt export was retained from which API can
reconstruct the sealed result. The source workspace checkpoint is the remaining
authoritative evidence location.

For Slice 1, please request an API-produced immutable checkpoint coordinate
packet and separate owner authorization for exactly one HEAD plus one
conditional GET. Do not infer the full artifact from trace summaries.

## Settlement ownership and sequence

The proposed sequence is approved with this required ordering:

1. API reads and validates the exact precursor result, receipt, checkpoint,
   ordered denial inventory, and bindings.
2. API durably records the precursor plus settlement intent/idempotency before
   invoking native work. The precursor is not terminal-closeout authority.
3. API releases or retains its own lease/capacity only under an explicit policy;
   SBE never reconstructs API resource state.
4. SBE receives only the exact named providerless-denial inventory and performs
   zero provider create, retrieval, or transport I/O.
5. SBE emits a cryptographically joined successor. API validates/ingests it and
   reinspects custody.
6. Only a genuinely `final` successor may enter terminal closeout.

Replay across every boundary must be inert: no second denial, no divergent
successor, no provider operation, and no premature cleanup.

No runtime implementation, live settlement, retained-run mutation, provider
work, deployment, or release is authorized by this review.
