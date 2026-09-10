# SBE 0.4.58 Release-Lock Qualification

## Decision

SBE `0.4.58` is technically qualified for API review at the pre-tag/release
boundary.

## Immutable candidate coordinates

- release-lock/tag-target commit:
  `ae993c68013b3a9a31b70f95e8eac51dd7f8a52c`
- component tag, if later authorized:
  `astrowoof-natal-authoring-v0.4.58`
- `SOURCE_DATE_EPOCH`: `1789054729`
- wheel: `astrowoof_natal_authoring-0.4.58-py3-none-any.whl`
- size: `1,376,041` bytes
- SHA-256:
  `a8b131e36accb6bead912f208271bc81b76827cddcc94f77de5fc8bcbbf61871`
- wheel members: `307`

Two independent clean archives of the exact lock commit produced identical
filenames, sizes, member inventories, and bytes. The wheel contains no detected
cache, build, bytecode, private-key, or test members.

## Release gates

- focused release-bound suite: 82 passed, 7 skipped
- supported broad/full coordinator: 1,163 passed, 60 skipped
- clean exact-wheel `pip check`: pass
- installed import/version/site-packages boundary: pass
- installed release smoke: pass, 193 resources
- installed adversarial qualification: pass, zero provider/network activity or
  spend
- installed polish-authority qualification: pass
- installed failed-QA exact-request probe: pass
- installed duplicate-attempt closed control: pass
- Alloy impact: none; no model change or rerun required

## Tag fence

If approved, tag only
`ae993c68013b3a9a31b70f95e8eac51dd7f8a52c`. This later qualification record
must not become the tag target. Upload only the exact wheel identified above;
do not rebuild or substitute another `0.4.58` artifact.

No tag, push, GitHub release, controlled live run, or publication has occurred.
