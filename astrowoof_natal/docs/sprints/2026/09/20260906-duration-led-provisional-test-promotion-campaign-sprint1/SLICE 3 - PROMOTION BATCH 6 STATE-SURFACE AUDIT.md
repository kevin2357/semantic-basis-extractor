# Slice 3 — promotion batch 6 state-surface audit

## Scope and decision

Audit the next three remaining modules in the frozen provisional-duration
inventory. Two may advance to collision qualification. The historical
characterization module should not be promoted until its enduring regression
value is decided explicitly.

| Module | Frozen seconds | Audit disposition |
|---|---:|---|
| `test_completed_retry_duplicate_submission_investigation_slice0.py` | 5.822 | hold for retain/archive/replacement decision |
| `test_batch_negative_authorization.py` | 5.513 | collision candidate with intentional native-lock contention |
| `test_external_authority_v2_intent_fence.py` | 4.919 | collision candidate with provider-fence and helper-import surfaces |

The cohort represents 16.254 seconds of the original provisional tail and 36
tests.

## Historical duplicate-submission characterization

- The single test owns a temporary root, copies only that owned workspace, and
  uses context-scoped patches plus a local provider-create inventory.
- Its expected result is intentionally the historical failure: restoring the
  same mixed checkpoint twice produces two scripted creates before the native
  local-progress refusal.
- Later sprint tests cover the corrected create-capable authority fence and
  completed-evidence behavior. Promoting this old-failure witness merely because
  it is process-isolated would preserve cost without first proving unique
  regression value.
- It imports a discovered routing test class and calls its private helpers,
  creating maintenance coupling beyond the extracted semantic-closure fixture.

Disposition: keep provisional and pause for an explicit decision to retain it
as historical characterization, replace it with a present-tense invariant, or
archive it. No deletion or semantic rewrite is authorized by this audit.

## Batch negative authorization

- Every scenario owns a `TemporaryDirectory`; run state, snapshots, denial
  artifacts, journals, and locks remain below it.
- The schema cached by `setUpClass` is immutable read-only package data.
- Threaded cases intentionally contend over one workspace-local native lock;
  mock patches and synchronization events are scoped to the test process.
- File-tree hashes exclude lock files deliberately but preserve all semantic
  bytes. No environment, cwd, repository, database, port, network, subprocess,
  or external provider surface was found.

Disposition: advance to collision qualification. Preserve atomic all-or-none
denial, exact replay/nonmutation, crash recovery, and competing-call assertions.

## External-authority v2 intent fence

- Each case owns a temporary workspace produced by a fixture helper; all intent,
  grant, provider-reference, snapshot, and result mutation stays below it.
- Provider creation is represented by local callables. Tests deliberately cover
  call-entry ambiguity, interruption, duplicate identity, replay, and nested
  competing dispatch without external I/O.
- Event-sink failure is local and diagnostic-only. Package schemas are read-only.
- The module imports `authority_inputs` from a discovered contract-test module;
  worker-process isolation contains its state, but the dependency remains
  maintenance debt.
- No environment, cwd, repository, database, port, network, or subprocess
  surface was found.

Disposition: advance to collision qualification. Preserve exact provider-call
inventories, durable ambiguity/fence states, snapshot validity, and byte-level
nonmutation assertions.

## Next boundary

Pause before collision work. Review should decide whether the historical
duplicate-submission witness stays provisional, is replaced, or is archived,
and whether to run the usual three-repetition/two-copy collision matrix for the
other two modules. No manifest, production, semantic-closure, or test-identity
change is made here.
