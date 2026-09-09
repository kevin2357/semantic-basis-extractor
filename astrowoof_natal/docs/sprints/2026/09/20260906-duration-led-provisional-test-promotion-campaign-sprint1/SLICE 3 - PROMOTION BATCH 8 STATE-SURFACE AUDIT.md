# Slice 3 — promotion batch 8 state-surface audit

## Scope and decision

Apply the campaign's adaptive batching rule to the next four medium-duration
leaders in the frozen provisional inventory. All four may advance to bounded
collision qualification; none is promoted by this document.

| Module | Frozen seconds | Tests | Audit disposition |
|---|---:|---:|---|
| `test_post_fan_in_retry_runtime_slice2.py` | 3.386 | 5 | collision candidate with process-global CLI patches and shared test-helper import |
| `test_payload_recovery_qa.py` | 3.126 | 2 | collision candidate with provider-free in-process qualification callbacks |
| `test_operator_disposition_packaging_slice4.py` | 2.868 | 4 | collision candidate with nested fresh-process CLI replay |
| `test_lifecycle_consumer.py` | 2.662 | 4 | collision candidate with three fresh-process public CLI checks |

The cohort represents 12.042 seconds of the original provisional tail and 15
tests. This is the first four-module medium-duration cohort under the adaptive
batching policy; physical collision concurrency remains bounded rather than
launching every copy at once.

## Post-fan-in retry runtime

- Every native workspace is rooted in an owned `TemporaryDirectory`; run state,
  snapshots, locks, and retry evidence do not escape it.
- `sys.argv`, `sys.stdout`, and authoring callbacks are patched only within
  restoring context managers. The module imports `_workspace` from another test
  module, but that helper has no import-time mutation or shared output path.
- The fake provider name is argument evidence only. Provider fan-in and retry
  preparation are locally scripted, and the pending-custody case performs no
  retrieval or creation.
- The intentionally failing event emitter checks that diagnostic emission does
  not undo durable native progress; it has no shared sink.
- No environment, cwd, subprocess, database, port, network, repository-write,
  or provider-I/O surface was found.

Disposition: advance to collision qualification. Preserve the exact v0.5/v0.7
boundary, exact/bounded route matrix, append-only consumed-operation history,
no-op refusal, pending-custody precedence, and zero provider work.

## Payload-recovery qualification

- Qualification materializes one owned temporary workspace and uses injected
  `prepare`/`create` callbacks. Its recorded provider-create count describes the
  fake callback invocation, not external provider I/O; the contract also
  asserts zero network calls and zero spend.
- Replay/refusal histories and all state mutations remain under the temporary
  root. The second test writes only its caller-owned receipt path.
- Package metadata and the packaged JSON Schema are read-only inputs.
- No process-global patch, environment, cwd, subprocess, database, port,
  network, repository-write, or fixed shared-output surface was found.

Disposition: advance to collision qualification. Preserve exact refusal and
fresh-request identity behavior, inert exact replay, history preservation,
closed validation, and the distinction between a scripted create callback and
external provider activity.

## Operator-disposition packaging

- Direct CLI checks own separate temporary workspace and output paths and prove
  the inspected workspace remains byte-identical. Output-inside-workspace is
  refused before publication.
- Qualification launches two child Python processes against one temporary
  workspace to prove deterministic, read-only replay. Under the campaign
  harness they inherit the already secret-scrubbed worker environment.
- Packaged schemas and fixture bundles are read-only. Mutation checks operate on
  deep copies; parser construction is process-local.
- The helper's subprocesses do not set a fixed cwd or output path and perform no
  provider or external network work.

Disposition: advance to collision qualification. Preserve exact public CLI
surface, workspace nonmutation, recovery-default-disabled posture, byte-identical
replay, protected-sentinel exclusion, and closed mutation refusal.

## Lifecycle consumer

- Each case owns a temporary run root. Requests, snapshots, denial records,
  event envelopes, and lifecycle results stay below it.
- Three checks launch child Python interpreters with a source-tree `PYTHONPATH`.
  The campaign worker has already scrubbed secret-bearing AstroWoof variables,
  so the inherited child environment remains provider-safe.
- Module-level `sys.path` insertion is process-local. Package/source resources
  are read-only, while all lifecycle writes target the owned run root.
- No cwd change, database, port, external network, repository write, fixed
  shared output, or provider-I/O surface was found.

Disposition: advance to collision qualification. Preserve the provider-free
smoke event sequence, v0.5 inspection inventory, typed batch denial,
reconciliation command-result precedence, and terminal inspection assertions.

## Next boundary

No pre-collision refactor is justified. Run three repetitions with two
independent process copies of each candidate, scheduled in controlled waves so
no more than six child workers contend at once. Require exact module inventories
of 5, 2, 4, and 4 tests, no unexpected skips, empty failure/error sets, empty
worker stderr, and unchanged substantive assertions. Then pause for the
separate promotion decision before any manifest change or actual-manifest
stress proof.

This audit grants no production/package change, semantic-closure movement, or
blanket qualification of later provisional modules.
