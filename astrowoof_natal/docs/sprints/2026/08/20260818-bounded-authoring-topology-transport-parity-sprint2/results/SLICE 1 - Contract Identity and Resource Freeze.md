# Slice 1 — Contract, Identity, and Resource Freeze

Date: 2026-08-18
Status: complete; awaiting API contract review
Provider operations: 0
Spend: USD 0

## Outcome

The proposed contract freezes bounded six-pass identity and authority without
admitting it into runtime. The API can review strict fixtures before either
repository changes production state interpretation.

No new public lifecycle vocabulary is proposed. Bounded interactive and Batch add
route-specific trajectories through existing waiting, pending, `not_due`, local-
continuation, delivery, review, budget, policy-stop, ambiguity, provider-failure,
custody, consumer-authority, and cost-disposition meanings.

## Identities

| Concern | Proposed identity |
|---|---|
| Six-pass bounded run | `astrowoof.bounded_natal.authoring_run.v2` |
| Assignment | `astrowoof.bounded_natal.split_assignment.v1` |
| Logical pass request | `astrowoof.bounded_natal.logical_pass_request.v1` |
| Authority aggregation | `astrowoof.bounded_natal.authority_aggregation.v1` |
| Route-parity oracle | `astrowoof.route_parity_transition_oracle.v2` |

Existing bounded run v1 is one-operation state. It remains readable as historical
evidence but is not resumable through the new topology. A future v2 runner must
return normal terminal evidence with outcome `terminal_failure`, cause
`legacy_bounded_topology_unsupported`, and the observed v1 contract identity before
mutation or provider work.

## Assignment contract

The strict proposal requires:

- one frozen subject and source claim-deck hash;
- deterministic `stratified-v1` policy and `bounded-stratified-v1` implementation;
- explicit 16-hex replay seed and declared seed basis;
- 50 unique canonical claim IDs;
- five ordered card passes, numbered 1-5, with ten unique IDs each;
- one empty-membership summary/theme pass numbered 6; and
- a 64-hex assignment digest.

JSON Schema enforces local shape/cardinality and closed fields. Runtime specialized
validation will additionally prove cross-pass referential closure and digest
correctness because JSON Schema cannot express all global invariants.

## Authority aggregation

Interactive:

```text
paid action = one pass attempt
API reservation reference = that exact paid action
binding = route + assignment + pass + attempt + stage + request digest
```

Batch:

```text
paid action = one Batch round
API global reservation = one Batch round
member authority = audit and ingestion only
settlement = aggregate round with member evidence
round evidence = aggregate maximum commitment + member count
               + ordered member inventory + settlement basis
```

Member rows never multiply API reservations. A later pass-local retry Batch is a new
round/action/reservation. Both mechanisms remain beneath the immutable aggregate and
stage ceilings of the SBE run.

## Request parity

The parity target is bounded interactive versus bounded Batch for one frozen bounded
pass/attempt. Normalization is restricted to interactive background/cache controls
and the outer Batch JSONL wrapper. Every editorial and schema-bearing byte beneath
that envelope must match.

Exact and bounded resource content may intentionally match. Their route-specific
packets, invariant authority notices, and output schemas need not and should not be
compared as interchangeable bytes.

## Resource freeze

Two separately named bounded resources now exist but are not runtime-admitted:

- `Bounded Natal Story Workspace Authoring Brief.md`;
- `Bounded Natal Authoring Guiding Lights.md`.

Their bytes equal the corresponding exact resources. The proposal manifest records:

| Role | Entry SHA-256 |
|---|---|
| Story-workspace brief | `8cd6ebf406b288bdc0897cac9b55a811523e89f91d3c8508a038b5767273c09e` |
| Guiding lights | `39f3d75f6e3df58d36c20b74c073c7d4b8d0697f64bda313df6b1258d6e01fc8` |

Later bounded divergence requires a new resource/prompt-geometry identity and
qualification. Slice 2 will begin consuming the separate bounded copies.

## Oracle evolution

Packaged v1 is unchanged and continues to say bounded Batch is unsupported. The v2
proposal contains:

- authorization waiting;
- pending and capacity release until due;
- nonmutating `not_due`;
- reclaim/local progress;
- mixed-member continuation;
- retry pending;
- usage unavailable with billing authority retained;
- ambiguity;
- provider failure;
- typed legacy-topology and pre-native/provider-evidence terminal failures; and
- final delivery.

The fixture asserts `public_vocabulary_change: false`. Slice 7 will replace this
proposal with packaged, runtime-derived traces accepted by the API's route-neutral
oracle.

## Verification

The local Python 3.11 SBE worker image ran six strict tests successfully, covering:

- Draft 2020-12 schema validity and canonical examples;
- exact five-by-ten assignment and summary-pass identity;
- additional-field, duplicate, and wrong-cardinality refusal;
- closed interactive/Batch authority units;
- exact/bounded resource-byte hash parity; and
- immutable v1 refusal plus closed-vocabulary v2 scenarios.

The desktop lean Python run passed 31 runtime baseline tests and skipped five schema
tests because `jsonschema` is absent. These skips are disclosed and are not counted
as strict validation evidence.

No runtime source, provider operation, authorization, run state, public schema, or
release artifact was changed by this contract slice.

## API review requested

Please answer the six questions in the contract proposal, with particular attention
to run-contract v2, one reservation per Batch round, interactive pass/attempt
bindings, parity normalization, legacy refusal cause, and route-parity oracle v2.

## API review response

The API agent approved the identities, one-reservation-per-round rule, interactive
binding, parity normalization, and reuse of existing states. Its requested additions
are incorporated:

- each Batch round exposes aggregate maximum commitment, member count, ordered
  inventory, and settlement basis;
- legacy v1 topology refusal is normal terminal evidence with cause
  `legacy_bounded_topology_unsupported`; and
- oracle v2 includes a typed terminal failure before native/provider evidence exists.
