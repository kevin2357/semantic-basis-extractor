# Slice 3 — promotion batch 10 state-surface audit

## Scope and decision

Audit the next six remaining leaders in the frozen provisional-duration
inventory. Five may advance to bounded collision qualification. One module is
held for an explicit historical-witness disposition before it can be promoted.

| Module | Frozen seconds | Tests | Audit disposition |
|---|---:|---:|---|
| `test_external_authority_public.py` | 1.257 | 12 | collision candidate with restoring CLI patches and helper import |
| `test_post_fan_in_mixed_custody_slice4b.py` | 1.194 | 1 | collision candidate with injected retrieval callback |
| `test_post_fan_in_retry_matrix_slice0.py` | 1.138 | 4 | hold: one historical failure characterization remains routine-discoverable |
| `test_operator_disposition_reader_slice2.py` | 1.043 | 6 | collision candidate with read-only helper imports and availability patch |
| `test_post_fan_in_retry_matrix_slice3.py` | 1.029 | 3 | collision candidate with imported workspace helper |
| `test_polish_authority_handoff_qa.py` | 1.026 | 4 | collision candidate with provider-free qualification and one optional-schema skip |

The five clean candidates represent 5.549 frozen seconds and 26 tests, with one
expected optional-schema skip. The held module represents another 1.138 seconds
and four tests.

## External-authority public contract

- All wave state, request artifacts, snapshots, and CLI outputs live under
  owned temporary roots. `sys.argv`, stdout redirection, and coherent-read race
  patches restore through context managers.
- Imported initial-wave fixture builders and package schemas are read-only;
  module-level source-path insertion is process-local.
- No subprocess, environment, cwd, database, port, network, provider I/O,
  repository write, or fixed shared output was found.

Disposition: advance to collision qualification. Preserve exact binding/order,
snapshot fences, mutation refusal, unsafe-output refusal, and installed public
surface assertions.

## Mixed provider custody

- The sole scenario owns its complete workspace and uses an instance-local
  retrieval callback returning scripted pending/completed responses.
- It performs no external retrieval or creation and retains exact mixed-custody
  ordering, local fan-in, and due-time precedence assertions.

Disposition: advance to collision qualification.

## Post-fan-in retry Slice 0 historical witness

- Filesystem and lock surfaces are process-isolated beneath temporary roots;
  collision itself is unlikely to expose a technical race.
- However,
  `test_ordinary_retry_cycle_can_republish_same_decision_without_progress`
  intentionally succeeds when legacy v0.5 republishes the same semantic
  ordinary-resume decision after only snapshot/revision change. The later v0.7
  runtime tests now prove that this condition is refused and consumed-operation
  history is append-only.
- The module's remaining three tests are useful compatibility/precedence
  regressions, and its `_workspace` helper is imported by current tests.

Disposition: hold outside Batch 10 collision and promotion. Review should choose
a surgical archival/extraction of the obsolete one-test characterization while
retaining the helper and three enduring tests, or explicitly justify keeping
the historical behavior in routine discovery. Do not promote the module merely
because it is process-isolated.

## Operator-disposition reader

- Every assessment workspace and native lock is temporary-root owned. Imported
  pending/retirement modules provide builders only; no shared mutation occurs.
- Exact-result and default-no-discovery paths are nonmutating. The availability
  reader patch restores through its context manager.
- No environment, cwd, subprocess, database, port, network, provider I/O,
  repository write, or fixed shared output was found.

Disposition: advance to collision qualification. Preserve snapshot binding,
writer-fence refusal, exact-result ingress, recovery-default disablement, and
workspace byte identity.

## Post-fan-in retry matrix Slice 3

- Every exact/bounded matrix cell owns a temporary workspace. The imported
  `_workspace` helper has no import-time mutation or shared path.
- All provider states are fixture documents; the packaged matrix asserts zero
  create and retrieval counts.

Disposition: advance to collision qualification. Preserve the closed A–H
matrix, route parity, custody/local-work precedence, and zero provider I/O.

## Polish-authority handoff qualification

- Qualification creates caller-owned temporary workspaces and performs no
  provider creation, network call, or spend. CLI output is a temporary receipt.
- Packaged schema/resource reads are immutable; mutation checks use deep copies.
  Module-level source-path insertion is process-local.
- The fourth test retains one expected skip when optional `jsonschema` is not
  installed.

Disposition: advance to collision qualification. Preserve exact identity join,
six closed negative cases, mutation refusal, packaged schema, and zero-I/O
assertions.

## Next boundary

Review must first decide the held Slice 0 witness disposition. Collision
approval may independently cover the five clean candidates: run three
repetitions with two copies apiece in controlled waves capped at six workers,
requiring exact inventories of 12/0, 1/0, 6/0, 3/0, and 4/1 tests/skips, no
failure/error/unexpected outcome, and no coordinator stderr. No manifest change
is authorized by this audit.

This audit grants no production/package change, semantic-closure movement, or
blanket qualification of the remaining provisional tail.
