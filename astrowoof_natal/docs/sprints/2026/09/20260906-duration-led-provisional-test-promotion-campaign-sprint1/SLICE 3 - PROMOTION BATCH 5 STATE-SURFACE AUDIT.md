# Slice 3 — promotion batch 5 state-surface audit

## Scope and decision

Audit only the next three remaining leaders in the frozen provisional-duration
inventory. All three may advance to bounded collision qualification; none is
promoted by this document.

| Module | Frozen seconds | Initial disposition |
|---|---:|---|
| `test_external_authority_qa.py` | 9.806 | collision candidate with child-process environment surface |
| `test_bounded_product_qa.py` | 7.211 | collision candidate with process-local tracing and helper inheritance |
| `test_terminal_review_interruption_slice4.py` | 5.870 | collision candidate with intentional same-workspace threading |

The cohort represents 22.887 seconds of the original provisional tail and 14
test cases, with one optional `jsonschema` skip.

## State surfaces

### External-authority qualification

- Generated workspaces and optional exported fixtures live below uniquely
  owned temporary roots.
- The module-level CLI check launches a child Python process. It copies the
  already-sanitized runner environment and overrides only `PYTHONPATH`; it does
  not introduce a shared output path, cwd mutation, or external provider.
- Qualification provider calls are local scripted callables with closed call
  counts. Public schemas are read-only package resources.
- Collision qualification must use the supported runner's secret-scrubbed
  child environment and preserve the optional-schema skip identity.

### Bounded-product qualification

- Mutable lifecycle output is confined to one `TemporaryDirectory`; the other
  cases operate on fresh in-memory copies of fixture values.
- `tracemalloc` is global only within its isolated test process. It is started
  and stopped by the measured qualification and cannot collide across runner
  workers.
- Imported admission and portfolio helpers expose maintenance coupling to
  discovered test modules, but each call returns fresh state and worker-process
  isolation contains module globals.
- Provider behavior is local and scripted. Event sinks are in-memory lists;
  no environment, cwd, repository, database, port, network, or fixed output
  path is mutated.

### Terminal-review interruption qualification

- Every case creates a unique temporary workspace. Journal, lock, snapshot,
  result, and receipt files remain below that workspace.
- The two-finalizer case intentionally has two threads contend over the same
  native writer lock. The lock is workspace-local and the expected one-success,
  one-lock-error result is part of the regression's semantics.
- Failure injection and the failing event sink are function-local. No ambient
  environment, cwd, repository, database, port, network, or subprocess state
  is touched.
- Collision must preserve exact single-result publication, immutable predecessor
  bytes, contiguous successor lineage, and protected-value absence.

## Qualification boundary

No pre-collision repair is justified. Run three repetitions containing two
independent process copies of every candidate under the secret-scrubbed harness.
Compare exact tests, skips, failures, and errors—not exit status alone—and retain
the terminal-review concurrency assertions. If green, pause for the separate
promotion decision before changing `test_suite_manifest.json` or running the
actual-manifest stress proof.

This audit grants no production change, semantic-closure movement, or blanket
qualification of later provisional modules.
