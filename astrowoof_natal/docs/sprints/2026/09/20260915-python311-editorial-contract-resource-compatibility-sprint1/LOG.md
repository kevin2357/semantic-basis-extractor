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

## 2026-09-15 — Slice 1 approval and release block

- API approved Slice 1 as implemented and confirmed its byte/failure
  preservation on Python 3.11 and 3.12.
- API prohibited candidate-wheel or Gate B advancement while the broader
  Python 3.11 editorial-contract suite retains eight errors.
- Control Room child `astrowoof-api#23` was designated as the companion
  packaged-resource compatibility sweep.
- Opened sibling SBE sprint
  `20260915-python311-packaged-resource-traversal-compatibility-sweep-sprint1`.
- This live-defect sprint remains paused before Slice 2 until that sweep passes
  the declared-minimum-runtime qualification gate.

## 2026-09-15 — Compatibility sweep handback received

- Companion sweep qualified and pushed exact source commit `235791de`.
- Four proven namespace-package readers were corrected; six compatible
  regular-package controls remained unchanged.
- Focused source tests passed on Python 3.11.15 and 3.12.14: 29 tests with 2
  optional skips on each.
- Original Slice 2 may resume with the combined broad/full-suite, wheel, and
  installed-wheel/API-host gates after review of the handoff.

## 2026-09-15 — Release playbook review and identity freeze

- Re-read `Maintainer Release Playbook.md` before release-bound work.
- Confirmed local tag and GitHub release identity
  `astrowoof-natal-authoring-v0.4.63` are unused.
- Selected fresh distribution version `0.4.63` and updated `pyproject.toml`
  before beginning the release-bound full suite, as required by the playbook.
- Repository search found no non-sprint version-derived fixture or test
  expectation requiring an accompanying `0.4.62` to `0.4.63` update.
- Tag, publication, deployment, and live witness remain unauthorized.

## 2026-09-15 — Slice 2A source regression

- Focused editorial capture matrix passed on Python 3.11.15 and 3.12.14: 45
  tests with 1 optional skip on each runtime.
- Manifest-controlled full suite passed on Python 3.12.14: 1,200 tests, 60
  expected skips, zero failures, 1,133.50017 seconds.
- Test inventory SHA-256:
  `3831ed792e633b43128e611e93738d8da0af9a0ed4b22f192faa853828ce9b9e`.
- Recorded compact source-regression evidence under `results/` as required by
  the release playbook.
- No provider, application-network, R2, Better Stack, or authoritative
  workspace operation occurred.

## 2026-09-15 — Artifact-source wheel and installed gates

- Committed artifact source `3e065e759ab8cb92b88cd9415b4e9d6254c114ad`
  with epoch `1789481170` before wheel construction.
- Two detached clean worktrees produced byte-identical 0.4.63 wheels:
  1,385,639 bytes, 310 members, SHA-256
  `fe0fba0c0be87ec25257a9b9c8c5f6e0166f9544df99fc8f940b20109ea1e355`.
- Package inventory contained required contracts/fixtures and zero forbidden
  tests, caches, bytecode, or private members.
- Exact build-A wheel passed clean installed gates on Python 3.11.15 and
  3.12.14: version/site-packages origin, `pip check`, release smoke, lifecycle
  smoke, editorial QA, and 15 public capture/diagnostics tests.
- Retained the exact qualification recipe as
  `qualify_installed_candidate.sh`.
- Prepared the release-lock candidate record; no tag or publication occurred.

## 2026-09-15 — Exact-lock epoch correction

- First exact-lock diagnostic pair used release-lock timestamp `1789481675` and
  produced mutually identical 1,385,639-byte wheels at SHA-256
  `f5a0846d78846b539639201289405e6a58c629ddb31edf1d21fcc2efe30e4d00`.
- This differed from the artifact-source candidate solely because the build
  epoch changed, contradicting the same record's frozen SHA requirement.
- Corrected the normative exact-lock epoch to artifact-source epoch
  `1789481170`, consistent with the established 0.4.62 procedure.
- The `f5a0846d...` diagnostic wheels are nonpublishable. Runtime, tests,
  resources, and package-affecting content did not change; the full suite was
  not rerun under the playbook's release-metadata correction policy.

## 2026-09-15 — Exact-lock qualification complete

- Corrected immutable release target:
  `ceb0dc5a28b81cff91a4a985edb4cf6ff3217e24`.
- Two clean target worktrees built with normative epoch `1789481170` and both
  reproduced the artifact-source candidate exactly: 1,385,639 bytes, 310
  members, SHA-256
  `fe0fba0c0be87ec25257a9b9c8c5f6e0166f9544df99fc8f940b20109ea1e355`.
- Exact lock build A passed the full installed qualification recipe on Python
  3.11.15 and 3.12.14.
- Prepared final SBE pre-tag coordinates for API consumer review.
- No tag, publication, deployment, or live witness occurred.
