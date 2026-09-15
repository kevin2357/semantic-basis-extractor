# Plan — Python 3.11 packaged-resource traversal compatibility sweep

## Objective

Remove unsupported variadic `Traversable.joinpath(...)` use from every
supported SBE Python 3.11 resource path, backed by real-caller, exact-byte, and
failure-preservation evidence on Python 3.11 and 3.12.

## Frozen fences

- Classify callers and resource ownership before changing each accessor.
- Use real packaged resources and concrete traversables; mocks alone are
  insufficient.
- Preserve selected resource identity and exact bytes.
- Preserve missing-resource, malformed-content, digest, and validation
  failures; do not add fallback discovery.
- Treat `resource_access.py` as high-reach and require explicit caller coverage
  before correction.
- Keep the predecessor live helper as a corrected control; do not modify it
  again without new evidence.
- Add every new test module to `test_suite_manifest.json` immediately.
- No provider, network application, R2, Better Stack, API, lifecycle, queue, or
  workspace mutation.
- No package/release action until the predecessor and this sweep jointly reach
  their release gates.

## Slice 0 — Exact inventory and caller classification

1. Re-run AST inventory for explicit multi-argument and starred `joinpath`
   calls across source and tests.
2. Trace every source call to its public or internal callers and classify it as
   production, generic accessor, contract qualification, packaged fixture, or
   adversarial-only.
3. Exercise each real accessor on Python 3.11 and 3.12 to record current
   success/failure and exact resource digest.
4. Identify calls whose arguments intentionally contain path separators and
   freeze their component semantics before rewriting.
5. Define caller-specific missing/malformed controls and test placement.

Acceptance: every inventoried call has a disposition, real witness, expected
resource identity, and proposed test boundary; no production source has
changed.

Status: complete. Ten call shapes remain after the predecessor fix. Concrete
Python 3.11/3.12 execution classifies four namespace-package calls for repair
and six regular-package calls as already compatible no-change controls. The
full caller, resource digest, path-semantics, and test matrix is recorded in
`SLICE 0 - CONCRETE TRAVERSABLE CALLER MATRIX.md`.

## Review Gate A — Inventory and sweep scope

Joint API/SBE review approves the complete inventory, supported-path ruling,
test matrix, and treatment of the generic accessor before implementation.

Status: reached with the completed concrete-runtime matrix. No production or
test source has changed.

## Slice 1 — Blocking editorial fixture reader

1. Correct `editorial_review_fixtures.py` using component-by-component
   traversal.
2. Add real packaged accepted-delivery and closeout fixture byte/digest tests on
   Python 3.11 and 3.12.
3. Preserve unknown-kind, missing-resource, malformed-content, digest, and
   strict-schema failures.
4. Rerun the 29-test editorial-contract suite on both runtimes.

Acceptance: the predecessor release block is removed without changing fixture
bytes or validation semantics.

## Slice 2 — Generic accessor and remaining justified callers

1. Correct the external-authority v2 fixture reader and both provider-economics
   readers according to the approved namespace-package inventory.
2. Add caller-specific real-resource and missing/malformed preservation tests.
3. Retain `resource_access.py` and the adversarial readers unchanged as
   concrete Python 3.11-compatible controls.
4. Prove no supported Python 3.11 namespace-package path retains variadic or
   dynamically multi-component `joinpath` use.
5. Run source-tree focused suites, manifest enforcement, provider-free broad
   qualification, and the final static inventory on Python 3.11 and 3.12.
6. Hand back the exact reviewed compatibility commit and qualification evidence
   to the predecessor live-defect sprint.

Acceptance: every changed accessor has two-runtime byte/failure evidence and
the static inventory is empty for supported paths. This companion sprint does
not build a release candidate. The predecessor sprint's Slice 2 exclusively
owns wheel construction, installed-wheel/package/API qualification, and the
release decision.

## Alloy ruling

Expected outcome is no Alloy update because this sweep changes implementation
compatibility only. Stop and reassess if any resource identity, contract,
authority, lifecycle, custody, packet, or transition semantic changes.
