# Plan

## Slice 0 — Reproduce and freeze the terminal boundary

Run the installed/source provider-free release smoke; identify the exact fixture
state, terminal result schema, publication call, and validator path. Prove whether
the fixture truly contains zero action lineage rather than malformed/omitted data.

## Slice 1 — Close the zero-action terminal-review contract

Define a versioned, machine-readable no-action disposition for terminal fixtures
which failed before any paid action existed. Preserve strict exact inventory
requirements whenever action lineage exists. Add negative tests preventing absent
inventory from masking real paid lineage.

The positive case is deliberately narrow: the native state must carry an
explicit present `spend_ledger.actions: []` inventory. Missing, null, malformed,
or nonempty inventories must not be recast as action-free. The result must use a
closed versioned disposition rather than silently overloading ordinary paid-action
terminal review, and mutations must prove a real one-action run cannot claim it.

**Slice 0 result:** the installed fixture reaches terminal review with no
`spend_ledger` key, confirming that fixture construction must first materialize
an explicit empty ledger before the new no-action contract can apply.

## Slice 2 — Release-smoke and public-reader qualification

Update the provider-free release smoke and terminal-result validator/reader tests.
Prove terminal publication, receipt validation, and final smoke exit succeed without
provider I/O while real paid-action cases remain strict.

**Slice 1 result:** approved v0.3/v0.2 sibling result and command schemas now
seal only the smoke fixture's explicit empty ledger. Existing v0.2 paid-action
results remain unchanged and reject the zero-action schema.

**Slice 2 result:** a disposable installed wheel carried both new schema
resources and passed the real provider-free release-smoke command with
`--require-installed`. Slice 3 is the next gate: a fresh-version patch release.

## Slice 3 — Patch release

Run the appropriate suite, freeze wheel SHA/provenance, tag and publish a patch
release. Leave API deployment and QA reset to the API companion sprint.

**Release candidate version:** `0.4.43` (fresh patch; `0.4.42` is immutable).
