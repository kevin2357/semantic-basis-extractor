# Slice 1 — Initial Wave Contract

Date: 2026-08-18
Status: proposed contract complete; awaiting Kevin and API review
Runtime admission: none
Provider operations: 0

## Outcome

The initial interactive wave is specified as one deck-owned, six-member native
orchestration unit with two authority layers:

- the API transactionally reserves or refuses the complete six-action set; and
- SBE validates one content-addressed wave envelope plus all six existing exact
  member authorizations before any create or authorization consumption.

After successful preflight, provider I/O may overlap while native mutation remains
single-writer. Each returned Response ID is durably persisted immediately. Only the
aggregate snapshot/result/receipt waits for all create tasks to unwind.

Full proposal:
[INITIAL WAVE CONTRACT PROPOSAL.md](../INITIAL%20WAVE%20CONTRACT%20PROPOSAL.md)

## Frozen proposal identities

- `astrowoof.initial_authoring_wave.v1`
- `astrowoof.initial_authoring_wave_authorization.v1`
- `astrowoof.initial_authoring_wave_result.v1`
- `astrowoof.initial_authoring_wave_contract_proposal.v1`

These are proposal identities only. They are not yet in the packaged contract
catalog and no 0.4.6 runtime accepts them.

## Frozen timing and cache policy

| Control | v1 value |
|---|---:|
| initial member count | 6 |
| maximum concurrent creates | 6 |
| provider create timeout | 15 seconds |
| provider-I/O wave bound | 20 seconds |
| maximum due retrievals per cycle | 4 |
| maximum parallel retrievals | 4 |
| cache policy | `no_serial_cache_warmer` |

The wave bound covers provider create I/O. Aggregate checkpoint publication is
bounded operational work but is not mislabeled as provider I/O. Retrieval remains
independently capped at four; six members may reconcile through two short subwaves.

## All-or-none boundary

One locked SBE prepare mutation creates six immutable action bindings against a
shared preparation basis revision. The content-addressed prepared wave inventories
those actions and their aggregate maximum commitment.

The API envelope repeats the exact wave/run/route/profile/basis/price-book/member/
aggregate identity, contains the ordered hashes of all six member authorization
documents, and carries one opaque reservation-set reference. The API remains the
only authority claiming its database reservation transaction.

SBE preflight rejects the whole wave with zero creates and zero consumption for:

- partial/missing authority;
- unknown or duplicate members;
- stale preparation basis;
- order, binding, digest, profile, route, price-book, or aggregate mismatch;
- denial or native budget failure;
- provider/consumption evidence;
- ambiguity, terminal/review state, or competing work; or
- invalid snapshot/path/run contract.

Provider-safety conflict outranks generic staleness in refusal presentation.

## Partial provider execution

Provider execution itself is explicitly non-atomic. Members close as:

- `provider_bound`;
- `authorized_unstarted`;
- `ambiguous_submission`; or
- `create_refused`.

Known IDs are reconcile-only. Ambiguous members are fail-closed. Definitely
unattempted members retain exact authority but are not automatically replayed by an
unrelated command. Provider refusal is not an automatic retry signal in v1.

## Batch preservation

Exact and bounded Batch remain one paid action/API reservation with six logical
members. The interactive wave envelope is not accepted as six Batch reservation
authorities. Partial usage, output/error membership, retry-round, retrieval custody,
and billing-pending behavior do not change.

## Public lifecycle composition

No new public state is proposed. Existing outcomes remain sufficient:

- `awaiting_external_authority`;
- `detached_provider_pending`;
- `not_due`;
- `progressed_local`;
- `ambiguous_submission`; and
- existing review, budget, policy-stop, provider-failure, and delivery outcomes.

Inspection v0.3 remains unchanged in the proposal. A separate versioned wave
projection/result is preferred over changing its strict top-level shape. Runtime
implementation must pause if this proves insufficient.

## Proposal fixtures and tests

Fixtures:

- `fixtures/initial-wave-contract.proposal.schema.json`
- `fixtures/prepared-initial-wave.proposal.json`
- `fixtures/initial-wave-authorization.proposal.json`

The canonical prepared wave and envelope are content-addressed. The schema closes
field sets, member cardinality, action/binding shapes, route/service/stage values,
and timing constants. Cross-document semantic tests enforce exact ordered inventory,
aggregate sum, common preparation basis, and copied authority identity.

Test commands and results:

```text
python -m unittest astrowoof_natal.tests.test_initial_wave_contract_proposal
Ran 8 tests in 0.026s
OK

python -m unittest \
  astrowoof_natal.tests.test_initial_wave_contract_proposal \
  astrowoof_natal.tests.test_lifecycle_contracts \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_bounded_topology_contract_proposal
Ran 61 tests in 5.889s
OK
```

The strict runs used the retained Python 3.11 qualification environment containing
`jsonschema 4.26.0`. The lean workspace runtime correctly skips proposal-schema
tests when `jsonschema` is absent.

## Review gate

Slice 2 runtime work must not begin until Kevin and the API agent answer or approve
the ten questions in the contract proposal, particularly:

- the envelope/member authorization split;
- the shared preparation basis;
- numeric timing limits;
- no serial cache warmer;
- member outcome vocabulary;
- four-at-a-time reconciliation;
- separate wave projection versus inspection v0.3 changes; and
- one-reservation Batch preservation.

