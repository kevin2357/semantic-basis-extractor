# Slice 3 — promotion batch 7 state-surface audit

## Scope and decision

Audit the next three remaining leaders in the frozen provisional-duration
inventory. All three may advance to bounded collision qualification; none is
promoted by this document.

| Module | Frozen seconds | Audit disposition |
|---|---:|---|
| `test_sbe_v03.py` | 4.656 | collision candidate with class fixture, subprocess, and read-only example surfaces |
| `test_negative_authorization.py` | 4.649 | collision candidate with workspace locks and fail-closed historical control |
| `test_operator_retirement_contract.py` | 3.637 | collision candidate with subprocess and intentional writer contention |

The cohort represents 12.942 seconds of the original provisional tail and 98
tests, including two optional-schema skips in operator retirement.

## SBE v0.3 product and package tests

- `TestBrePacket.setUpClass` compiles one process-local packet from read-only
  repository examples. Test mutations use deep copies or owned temporary files;
  runner worker isolation prevents cross-process fixture sharing.
- Story workspaces, copied validator source, reports, subject packages, and
  archives are created only under `TemporaryDirectory` roots.
- Child Python validators inherit the already secret-scrubbed worker environment
  and operate only on paths below those roots.
- Module-level `sys.path` insertion is process-local maintenance debt. The
  repository `examples` tree and package resources are read-only inputs.
- No database, port, network, provider, cwd mutation, or fixed shared output
  path was found.

Disposition: advance to collision qualification. Preserve the exact 52-test
inventory, class-fixture behavior, archive round trips, validator return codes,
and deterministic packet/selection assertions.

## Negative authorization

- Every mutable case owns a temporary workspace; state, snapshots, denial
  artifacts, delivery files, and native locks stay beneath it.
- The class-cached schema is immutable read-only package data. Mock patches and
  event sinks are test/process-local.
- The sequential two-action stale-seam case remains useful negative coverage:
  it proves the second stale single-action request fails closed without mutation
  while the separately promoted Batch module proves the current atomic route.
  Unlike the archived duplicate-create witness, its success condition is a
  present safety invariant rather than occurrence of unsafe provider work.
- No environment, cwd, repository, database, port, network, subprocess, or
  provider-I/O surface was found.

Disposition: advance to collision qualification. Preserve exact stale/race
precedence, nonmutation hashes, provider-evidence refusal, and denial replay.

## Operator-retirement contract

- Each scenario owns a temporary run root. Requests, snapshots, results,
  receipts, and injected unrelated bytes remain below it.
- CLI checks launch child Python processes with the already sanitized worker
  environment plus a local `PYTHONPATH`; inputs and outputs are temporary-root
  paths.
- The concurrent-writer case deliberately coordinates one thread and one
  workspace-local native lock. Events, patches, failure injectors, and sentinels
  are process-local.
- Public schemas and packaged fixtures are read-only. No database, port,
  network, provider, cwd mutation, or fixed shared output path was found.

Disposition: advance to collision qualification. Preserve exact publication,
interruption repair, one-writer behavior, replay, schema, and protected-sentinel
assertions, including the two optional-schema skips.

## Next boundary

No pre-collision repair is justified. Run three repetitions containing two
independent process copies of every candidate under the supported
secret-scrubbed harness. Require exact 52/0, 20/0, and 26/2 test/skip inventories,
empty failure/error sets, and unchanged substantive assertions. Then pause for
the separate promotion decision before any manifest change or actual-manifest
stress proof.

This audit grants no production/package change, semantic-closure movement, or
blanket qualification of later provisional modules.
