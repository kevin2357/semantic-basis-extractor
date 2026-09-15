# Log — Python 3.11 editorial contract-resource compatibility

## 2026-09-15 — Sprint initialization

- Inspected only the latest local Render exports for the two named native runs.
- Left Better Stack exports untouched at the owner's direction.
- Joined the 0.4.62 phase diagnostics to the exact approved SBE source frame.
- Classified both witnesses as the same deterministic
  `typed_status_construction` / `_resource_bytes:221` `TypeError`.
- Identified the Python 3.11 versus 3.12 runtime difference and the
  multi-descendant `Traversable.joinpath(...)` call as the leading cause.
- Created this sprint's background, evidence register, log, and plan.
- Made no source, test, manifest, package, workspace, provider, API, or remote
  change.
- Paused at Review Gate A before reproduction or implementation.

## 2026-09-15 — API initial-plan review

- API approved the provider-free Slice 0 reproduction on real Python 3.11,
  with a Python 3.12 contrast and related-call-site inventory.
- API required proof that chained traversal returns byte-identical resource
  content and that missing or malformed resources remain failures.
- API confirmed no API contract, packet, lifecycle, transport, or Alloy change
  is indicated by the current evidence.
- Production source, version, package, release, deployment, and live witness
  remain unauthorized pending review of the reproduction.

## 2026-09-15 — Slice 0 complete

- Pulled official Python 3.11.15 and 3.12.14 slim container images.
- Mounted the repository read-only and ran the retained provider-free probe.
- Reproduced `TypeError` from the current two-descendant call on Python 3.11;
  the same call succeeds on Python 3.12.
- Proved chained traversal returns byte-identical semantic-contract content on
  both runtimes: 11,604 bytes and SHA-256
  `306fcf0e55c56f5fe48b18eaced64dbb3338ab783a5722a801f7759af96e52e5`.
- Proved missing and malformed resources remain `FileNotFoundError` and
  `ValueError`, respectively.
- Inventoried ten explicit multi-argument `joinpath` calls and one dynamic
  starred-component call across seven source modules.
- Made no production source, test, manifest, version, package, or remote
  runtime change.
- Paused at Gate A for review of the reproduction and correction scope.

## 2026-09-15 — Gate A approval and Slice 1 implementation

- API approved the exact live helper correction and required the eleven latent
  call sites to remain a separate tested compatibility sweep.
- Replaced only `editorial_review_contracts._resource_bytes()` with chained
  single-component traversal.
- Added focused byte-identity and missing-resource coverage to the already
  manifested `test_editorial_review_contract_foundation.py` module.
- Corrected that focused test's own Python 3.11-incompatible resource lookup.
- Left all eleven separately inventoried production/qualification call sites
  unchanged.
- Focused foundation tests passed on Python 3.11.15 and 3.12.14: 13 run with 1
  optional skip on each runtime.
- Broader editorial-contract tests passed on Python 3.12.14: 29 run with 1
  optional skip.
- The same broader suite on Python 3.11.15 produced eight errors, all at the
  separately inventoried `editorial_review_fixtures.py:628` variadic resource
  lookup.
- Stopped without broadening source scope. Candidate-wheel qualification is
  blocked pending review and the separately requested compatibility sweep.
