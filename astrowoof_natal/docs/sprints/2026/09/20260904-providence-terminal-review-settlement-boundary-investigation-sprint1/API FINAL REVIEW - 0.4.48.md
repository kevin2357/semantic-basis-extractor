# API final review — SBE 0.4.48 candidate

## Technical decision

**Approved for owner tag-and-publish authorization.** API accepts the exact
candidate defined by release-lock commit
`49f9e2e3b76d71f84a90542f0fedfa2ae06d4e00`, artifact-source commit
`96dd0ef539e1972ce694f75b60eac7bc3491caa8`, and wheel SHA-256
`d1e84055183e2c45eb687aed61c247425008edec53e33f424c57cc89bf89a8e0`.

## Review basis

- The release-lock delta from the artifact source is documentation/evidence
  only; it does not change package sources.
- The package change is additive, enumerable qualification surface: public
  readers/runners, the v1/v2 schemas, fixture, CLI, and tests. It does not
  change native lifecycle selection, custody derivation, denial semantics,
  provider behavior, terminal publication, or API disposition.
- The approved focused gate covers the altered public boundaries (104 passed;
  6 documented optional-schema skips), while two clean builds from both source
  identities are byte-identical under the recorded `SOURCE_DATE_EPOCH`.
- The isolated installed-wheel evidence verifies `0.4.48` with SPC `0.11.1`,
  package provenance, `pip check`, public schema/reader/validator/CLI paths,
  fixture equality, denial/refusal/replay fencing, contiguous final successor,
  and zero provider I/O.
- The candidate preserves the API/SBE ownership boundary: it grants neither
  API terminal cleanup from a native label nor authority to settle Providence
  outside a future exact API implementation.

## Explicit scope limit

This is technical release-pair approval only. It does not tag or publish the
wheel, deploy it, settle/recover Providence, or authorize provider work. Owner
authorization remains required for the immutable tag and publication.
