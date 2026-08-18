# Slice 1 — Native Publication and Snapshot Integrity

Status: complete; awaiting Kevin review

## Outcome

Fresh exact and bounded interactive initial-wave preparation now publishes
`initial-authoring-wave-binding-bundle.json` from the same complete binding objects
used to prepare the six native spend-ledger actions and build the public wave.

The implementation adds shared provider-free builders and validators for:

- the closed complete bundle;
- each exact binding and its recomputed digest/action identity; and
- the bundle's complete ordered relationship to the prepared wave.

No prompt/request body is read back or reconstructed to create the bundle.

## Publication protocol

1. Route preparation constructs each complete native binding.
2. `prepare_action()` persists those facts in native ledger authority.
3. `build_initial_wave()` creates the selected-field public wave projection.
4. `build_initial_wave_binding_bundle()` consumes the same in-memory complete
   bindings and cross-validates the resulting bundle against that wave.
5. The root artifact is written atomically before state/checkpoint publication.
6. Existing state/public/spend projections are persisted.
7. The enclosing coordinator publishes the complete workspace snapshot and native
   result/receipt before the worker boundary becomes ingestible.

Filesystem writes across artifact, mutable state, and snapshot are not claimed as
one literal atomic transaction. An interruption before the final snapshot leaves no
valid advertised checkpoint; missing, additional, or changed bundle bytes cause
snapshot validation to fail closed.

## Compatibility

- Fresh exact and bounded interactive waves publish the new artifact.
- Existing in-memory prepared waves are returned unchanged; missing legacy bundle
  bytes are not silently reconstructed on resume.
- Exact and bounded Batch paths are unchanged.
- `spend-authorization-requests.json` remains unchanged.
- No lifecycle, capacity, terminal, event, or transition-oracle vocabulary changed.

## Tests

- Shared builder/validator determinism, exact/bounded route separation, closed
  bundle/binding fields, digest tampering, and cross-wave mismatch.
- Exact integration: artifact publication, ordered action identity, complete
  snapshot validation, changed-byte rejection, restoration, authorization, create,
  and detach.
- Bounded integration: artifact publication, ordered identity, complete snapshot,
  authorization, create, and detach.
- Combined wave/exact/bounded suite: 139 passed in 289.799 seconds.
- Final focused regression: 5 passed in 4.810 seconds.
- Provider operations / spend: 0 / USD 0.

## Residual boundary

The supported snapshot-validating authority-inputs pair reader and CLI are Slice 2
work. Slice 1 establishes the native artifact and integrity substrate only.
