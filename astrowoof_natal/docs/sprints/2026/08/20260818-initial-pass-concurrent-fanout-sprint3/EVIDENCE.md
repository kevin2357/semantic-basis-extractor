# Initial Authoring Pass Concurrent Fan-Out Sprint 3 Evidence

Date: 2026-08-18
Status: planning only

No implementation or qualification evidence exists yet.

The retained SBE 0.4.6 bounded interactive live run motivating the observed serial
behavior remains outside Git at:

```text
C:\dev\github\semantic-basis-extractor\.runs\kevin-bounded-live-20260818\run
```

It must remain unmodified diagnostic evidence. Its six initial Responses were
created only after the preceding pass completed; it is not evidence of concurrent
fan-out. Full run and cost details are indexed by the cost-calibration sprint.

## Bounded final-QA defect owned by this sprint

All six pass records reached `PASS_QA_ACCEPTED`. Deterministic assembly then found
nine duplicated normalized body passages. They were the nine density/voice body
variants for two selected foundational claims with equivalent North Node editorial
semantics but distinct upstream source objects:

- `bounded_candidate:foundational_object:4e954709d2409ded004714a1`
  (`True_Node`); and
- `bounded_candidate:foundational_object:3bd9d53c7147e3c17dc64619`
  (`Mean_Node`).

The final validator correctly returned `fail` and the bounded lifecycle assigned
`FINAL_QA_REQUIRES_REVIEW`. Shared `persist_state()` then called generic
pass-derived status recomputation, observed six accepted passes, and overwrote the
state with `AUTHORING_COMPLETE`. The final-QA control flow still returned before
polish, so no optional provider request was made, but native/public status was
misleading.

This sprint owns two SBE-native corrections:

1. final-QA/review state has precedence over pass-derived authoring-complete state
   through every persisted and public projection; and
2. equivalent selected bounded claims are rejected before paid authoring with
   typed diagnostic evidence, without silently merging upstream provenance.

SPC remains authoritative for whether bounded projection emits Mean Node, True
Node, or both. The SBE guard is an editorial admission invariant, not an upstream
projection rewrite.

Each slice will add exact commands, scripted timing records, mutation counts,
provider-operation inventories, failure-injection checkpoints, schema/fixture
hashes, installed-wheel identities, and test results here or in a linked compact
result artifact.

## Slice 0

Full report:
[SLICE 0 - Four-Pipeline Baseline and Seam Inventory.md](results/SLICE%200%20-%20Four-Pipeline%20Baseline%20and%20Seam%20Inventory.md)

- New provider operations: 0.
- Focused tests: 5 passed in 8.738 seconds.
- Full source suite: 423 passed in 321.471 seconds; 10 skipped.
- Exact interactive: cache-warmer-plus-five blocking concurrency when caching is
  enabled; no short create-only detach boundary.
- Bounded interactive: six blocking serial passes.
- Exact Batch: one six-member round.
- Bounded Batch: one six-member round.
- Retained bounded live identity span: 588 seconds across six actions.
- Released interactive reconciliation: four parallel due retrievals per cycle.
- Recommendation: proceed to the versioned wave authorization and create-only
  contract in Slice 1.

API review approved the Slice 0 findings with three Slice 1 emphases:

- explicitly remove full-response cache-warmer latency or prove a nonblocking
  create-only alternative;
- treat complete-wave API reservation/SBE authorization as a real cross-repository
  atomicity boundary; and
- preserve four-at-a-time retrieval independently of six-at-a-time initial create.

The Slice 0 report now also states precisely that per-ID ledger/journal durability
is immediate and serialized; only aggregate wave publication waits for all create
tasks to unwind.

## Slice 1

Full proposal:
[INITIAL WAVE CONTRACT PROPOSAL.md](INITIAL%20WAVE%20CONTRACT%20PROPOSAL.md)

Result:
[SLICE 1 - Initial Wave Contract.md](results/SLICE%201%20-%20Initial%20Wave%20Contract.md)

- Proposal identities: prepared wave v1, authorization envelope v1, result v1.
- Fixed create controls: 6 parallel, 15 seconds each, 20-second provider-I/O wave.
- Fixed retrieval controls: 4 due and 4 parallel per cycle.
- Cache policy: `no_serial_cache_warmer`.
- Exact complete API reservation envelope plus six member authorizations required
  before any create/consumption.
- Per-ID ledger/journal persistence is immediate and serialized.
- Batch remains one round action/reservation with six members.
- Strict proposal tests: 8 passed in 0.026 seconds.
- Related lifecycle/route contract tests: 61 passed in 5.889 seconds.
- Provider operations: 0.
