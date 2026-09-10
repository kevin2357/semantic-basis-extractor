# Slices 1–2 — exact runtime capture-status implementation

## Outcome

The runtime no-packet branch now constructs
`editorial_review_capture_status.v1` only after proving exact native run,
subject, and selected-result identity. Fixture sentinels remain isolated to an
explicit fixture-only wrapper and cannot enter runtime output.

## Implementation

- New public `build_editorial_review_runtime_capture_status` requires explicit
  native run, subject, and result IDs and rejects empty correlation values.
- Its `capture_id` follows semantic contract v5 exactly: run ID, result ID,
  reason, and detail code. Subject remains required payload content but does not
  alter the ID.
- The backwards-compatible `build_editorial_review_capture_status(reason)`
  remains the explicitly synthetic fixture helper and owns the three fixture
  values used by provider-free contract qualification.
- `validate_editorial_review_capture_status_against_native` validates closed
  schema/identity bytes and joins selected/result/receipt IDs, result/receipt run
  IDs, and the sole expected subject.
- The runtime uses one local `_exact_capture_source` guard. It rejects
  caller/result/receipt mismatch, result/receipt run mismatch, restored-state
  run mismatch, and zero/multiple/empty subject identities before constructing
  any status.
- Unsupported result and route classifications retain typed public statuses but
  defer their construction until the exact source guard succeeds.
- Unsupported service level is separate from invalid subject cardinality and
  emits `ineligible_route` only after one subject is proven.
- Every later incomplete/contradictory refusal uses the same immutable
  correlation context.
- The shared native exact reader, schemas, semantic manifest, packet builder,
  terminal delivery handoff, lifecycle, and workspace state are unchanged.
- The existing public fixture helper signature remains compatible; the runtime
  correction is exposed through the separately named explicit constructor.

## Regression evidence

The focused tests prove:

- two distinct real-ish inputs produce different capture IDs and exact native
  correlations;
- runtime output contains no fixture sentinel;
- repeated construction remains deterministic through equality-based tests;
- caller/result/receipt mismatch raises without a status;
- run mismatch and zero/multiple subjects raise without a status;
- unsupported service with one proven subject emits the correct typed status;
- subject-only changes retain the frozen capture ID but fail exact-source
  validation against the selected subject;
- all six reason/detail-code combinations remain closed-schema valid; and
- public package exports include the explicit builder and exact-source
  validator.

## Source qualification

- editorial-review modules: 39 passed, 1 expected optional-`jsonschema` skip;
- release-contract and release-smoke modules: 19 passed, 1 expected skip;
- terminal-review and native-transition adjacency: 38 passed, 4 expected
  optional-schema skips;
- focused core during implementation: 27 passed, no skips;
- API source-overlay consumer guard: 5 passed;
- changed Python modules/tests compile successfully; and
- `git diff --check`: clean.

No provider, network, API sender, Better Stack, database, retained-run,
lifecycle, workspace-mutation, package-version, tag, push, or release operation
occurred.

## Review boundary

This is a source-qualified candidate for API/Vafflemutt review. A fresh package
version and installed-wheel qualification remain the next explicit gate.
