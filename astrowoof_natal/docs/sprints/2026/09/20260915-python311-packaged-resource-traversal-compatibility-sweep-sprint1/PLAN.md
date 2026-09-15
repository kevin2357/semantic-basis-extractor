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

## Review Gate A — Inventory and sweep scope

Joint API/SBE review approves the complete inventory, supported-path ruling,
test matrix, and treatment of the generic accessor before implementation.

Status: reached for initial-plan review. No inventory execution or source
change has started.

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

1. Correct `resource_access.py` only after exercising representative callers
   for contracts, schemas, fixtures, references, and nested paths.
2. Correct remaining supported fixture, adversarial, authority, and economics
   readers according to the approved inventory.
3. Add caller-specific real-resource and missing/malformed preservation tests.
4. Prove no supported Python 3.11 source path retains variadic or dynamically
   multi-component `joinpath` use.
5. Explicitly document rather than silently alter any unsupported historical
   path.

Acceptance: every changed accessor has two-runtime byte/failure evidence and
the static inventory is empty for supported paths.

## Slice 3 — Installed-wheel and release-pair qualification

1. Build and install the candidate wheel in clean Python 3.11 and 3.12
   environments.
2. Exercise the changed public/resource surfaces from installed bytes.
3. Rerun focused suites, manifest enforcement, provider-free broad suite,
   package-content checks, and build-twice identity under the release playbook.
4. Return to the predecessor sprint's public delivery and terminal-review
   capture Gate B qualification.
5. Obtain API installed-wheel review before any tag/publication decision.

Acceptance: the declared minimum runtime has no supported variadic-resource
traversal dependency and both sprints can jointly enter release review.

## Alloy ruling

Expected outcome is no Alloy update because this sweep changes implementation
compatibility only. Stop and reassess if any resource identity, contract,
authority, lifecycle, custody, packet, or transition semantic changes.

