# Slice 3 — promotion batch 4 state-surface audit

## Scope and decision

Audit only the next three remaining duration leaders. All three may advance to
collision qualification; none is promoted by this document.

| Module | Frozen seconds | Initial disposition |
|---|---:|---|
| `test_final_qa_mixed_custody_qa.py` | 16.625 | collision candidate |
| `test_post_fan_in_retry_routing_runtime_slice2.py` | 14.857 | collision candidate with test-helper inheritance |
| `test_external_authority_v2_route_qualification.py` | 12.966 | collision candidate with multi-workspace copy surface |

The cohort represents 44.448 seconds of the original provisional tail.

## State surfaces

### Final-QA mixed-custody qualification

- All generated state and CLI output live below owned temporary roots.
- Package schemas are read-only; provider activity is scripted and asserted
  absent.
- The test imports private fixture constructors from production qualification
  modules, but mutates only newly created state.
- No environment, cwd, repository, database, port, logger, or subprocess
  mutation was found.

### Post-fan-in routing runtime

- The only mutable scenario uses one owned `TemporaryDirectory`.
- It inherits workspace/main helpers from a discovered test module; runner
  process isolation contains import state, but this remains maintenance debt.
- The assertion explicitly preserves native bytes across unsupported-state
  refusal; collision must not weaken that byte-equivalence check.
- No provider, environment, repository, database, port, logger, or subprocess
  surface was found.

### External-authority v2 route qualification

- Every exact/bounded scenario owns a temporary root.
- Per-stage `copytree` operations copy only an owned base workspace into unique
  child paths under the same root.
- Provider create/retrieve functions are local callables with exact call
  inventories; no network adapter is used.
- No ambient environment/cwd mutation, repository write, database, port,
  logger, subprocess, or fixed shared output path was found.

## Qualification boundary

No pre-collision repair is justified. Run three repetitions with two copies of
all candidates, preserving exact skip/failure/error identities and the
routing test's byte-level nonmutation assertion. If green, promotion may be
proposed, followed by repeated actual-manifest two-worker stress proof.

This audit grants no semantic-closure movement, production change, or blanket
qualification of later provisional modules.
