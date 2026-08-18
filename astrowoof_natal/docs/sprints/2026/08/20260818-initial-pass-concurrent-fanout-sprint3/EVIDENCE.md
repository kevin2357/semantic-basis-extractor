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
