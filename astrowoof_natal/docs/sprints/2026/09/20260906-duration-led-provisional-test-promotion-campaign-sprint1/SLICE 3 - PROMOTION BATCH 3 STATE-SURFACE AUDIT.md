# Slice 3 — promotion batch 3 state-surface audit

## Scope and decision

Audit only the next three remaining duration leaders. All three may advance to
collision qualification; none is promoted by this document.

| Module | Frozen seconds | Initial disposition |
|---|---:|---|
| `test_post_fan_in_retry_qa_slice4.py` | 19.633 | collision candidate |
| `test_post_fan_in_retry_composed_runtime_slice3.py` | 19.516 | collision candidate with helper-coupling observation |
| `test_optional_stage_completed_evidence_adoption_slice2.py` | 17.683 | collision candidate with internal provider-fence/concurrency sensitivity |

The cohort represents 56.832 seconds of the original provisional tail.

## Post-fan-in retry qualification

- Production-shaped qualifications create owned prefixed temporary roots.
- CLI outputs are written only to each test's `TemporaryDirectory`.
- Public schemas/fixtures are read-only package resources.
- Provider counts are scripted and asserted zero for external network/spend.
- No environment, cwd, repository artifact, database, port, or logger mutation
  was found.

No repair is justified. Qualify two independent copies plus a neighboring
qualification-heavy module.

## Composed runtime

- The single scenario owns one `TemporaryDirectory` and all checkpoint,
  response, snapshot, payload, and result artifacts remain below it.
- Provider retrieval/create are local callables with exact call inventories.
- The patch of `closure.author_pending_passes` is context-scoped.
- Internal lifecycle and replay behavior are the substance of the test and must
  not be mocked away.
- It inherits helpers from a discovered authority-routing test module. This is
  maintenance coupling, but separate runner processes isolate import state.

No pre-collision refactor is justified. If collision exposes helper-state
coupling, extract only the affected helpers to a non-discovered support module.

## Optional-stage completed-evidence adoption

- Every case owns a temporary workspace and stage-specific response/marker
  paths below it.
- The semantic-closure packet is the approved process-local template with a
  fresh per-test deep copy.
- Provider calls are patched to fail if attempted or routed through deliberately
  local fake behavior; the real provider fence is part of the assertion.
- A per-test `threading.Lock` belongs to its local `SpendController`.
- Patches are context-scoped; no environment, cwd, repository, database, port,
  or subprocess surface was found.
- It imports Nori reproduction helpers from a discovered module. As above,
  process isolation contains import state, but helper ownership remains
  maintenance debt.

No pre-collision refactor is justified. Collision must preserve provider-I/O
refusals, exact marker/action identities, and per-test packet ownership.

## Qualification boundary

Run three repetitions with two copies of every candidate. Because the cohort
contains provider-fence assertions and helper inheritance, compare exact
failures/errors/skips—not exit status alone. Then run the actual two-worker
parallel group repeatedly before any classification change is finalized.

This audit does not authorize semantic-closure movement, production changes,
or blanket promotion of composed-runtime/qualification tests.
