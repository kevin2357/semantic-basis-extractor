# Plan — Python 3.11 editorial contract-resource compatibility

## Objective

Reproduce and narrowly correct the Python 3.11 resource-traversal failure that
prevents otherwise valid editorial runtime capture from returning its typed
status, while preserving all native identities, packet bytes, capture
semantics, and fail-closed behavior.

## Frozen fences

- Treat the Render diagnostics as localization evidence, not authorization to
  infer or alter persisted native state.
- Reproduce on Python 3.11 before changing production code.
- Preserve the exact resource package, contract prefix, filename, and returned
  bytes; change only path-component traversal if the hypothesis is confirmed.
- Do not catch, translate, or suppress unrelated resource errors.
- No public schema or behavior change outside restoring declared Python 3.11
  compatibility.
- No provider, network, R2, Better Stack, API, queue, lifecycle, or workspace
  mutation.
- Add every new test module to `test_suite_manifest.json` immediately.
- Release, publication, deployment, and live witness require later explicit
  review and authorization.

## Slice 0 — Reproduce and freeze the compatibility boundary

1. Run the exact packaged-resource read shape under CPython 3.11 using the
   supported package/runtime environment.
2. Record the exact exception class and call boundary without retaining unsafe
   exception prose in structured runtime contracts.
3. Run the same probe under CPython 3.12 to confirm the qualification gap.
4. Verify that chained single-component traversal resolves the identical
   resource and returns byte-identical content under both versions.
5. Search the package for other multi-descendant `Traversable.joinpath(...)`
   calls and classify them without broad mechanical edits.

Acceptance: the live failure is reproduced provider-free on Python 3.11, the
3.12 contrast is demonstrated, and the narrow compatible expression returns
identical contract bytes.

Status: complete. The exact live call shape raises `TypeError` on Python
3.11.15 and succeeds on 3.12.14. Chained traversal returns the same 11,604
bytes and SHA-256 on both; missing and malformed inputs remain failures. The
related-call inventory found eleven potentially incompatible sites across
seven modules.

## Review Gate A — Reproduction and correction fence

Joint API/SBE review confirms the runtime diagnosis, affected surface, and
byte-preserving correction before production implementation.

Status: reached again with Slice 0 evidence. Production implementation remains
gated on review of the reproduction and a scope ruling for the ten additional
explicit multi-argument calls plus one starred-component call.

## Slice 1 — Narrow source correction and focused regression

1. Replace only the incompatible multi-descendant resource traversal confirmed
   by Slice 0.
2. Add focused tests that read every affected packaged editorial contract and
   compare exact bytes/digests to the checked-in resources.
3. Add an explicit Python 3.11 regression using the real installed/package
   resource implementation, not a permissive Python 3.12-only mock.
4. Prove malformed or missing resources continue to fail rather than being
   converted into successful capture.
5. Update `test_suite_manifest.json` for any new test module.

Acceptance: Python 3.11 and 3.12 read identical resource bytes, while genuine
resource failures retain their prior behavior.

Status: narrow implementation and focused qualification complete. Only the
live helper and its focused existing test module changed. No new test module
was created; `test_editorial_review_contract_foundation.py` was already present
in `test_suite_manifest.json`. The focused module passes on Python 3.11 and
3.12. The broader editorial-contract suite exposes eight Python 3.11 errors at
the separately inventoried `editorial_review_fixtures.py:628` call, so package
qualification is paused rather than silently widening this slice.

## Slice 2 — Public capture and package qualification

Prerequisite: complete and review the separately scoped Python 3.11 resource
compatibility sweep sufficiently to make the required provider-free package
qualification executable. Slice 2 must not absorb those changes without their
own evidence and review.

Companion sprint:
`../20260915-python311-packaged-resource-traversal-compatibility-sweep-sprint1/`.
Control Room parentage: `kevin2357/astrowoof-api#23`.

1. Exercise the public delivery and terminal-review capture routes through
   typed-status construction on Python 3.11.
2. Prove exact result/root binding, eligibility, packet assembly, validation,
   and typed status are otherwise unchanged.
3. Build and install a fresh candidate wheel in a Python 3.11 environment and
   repeat the public regressions against installed bytes.
4. Run focused suites, manifest enforcement, provider-free broad
   qualification, package-content checks, and build-twice identity according
   to the release playbook.
5. Obtain API installed-wheel/host review before any release decision.

Acceptance: the declared minimum Python runtime can complete both public
capture routes from the installed candidate without changing contracts or
performing provider operations.

## Review Gate B — Release decision

Review source, Python 3.11/3.12, installed-wheel, package-byte, and API-host
evidence before any version bump, tag, publication, deployment, or live
witness.

## Alloy ruling

Expected outcome is no Alloy update: this restores an implementation-level
Python compatibility property without changing modeled lifecycle, authority,
selection, custody, packet, or transition semantics. If investigation reveals
a semantic change, stop and reassess before implementation.
