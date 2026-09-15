# API final pre-tag review — SBE 0.4.62

## Technical decision

Approved for owner authorization to create and publish the exact release below.
No tag or publication is performed by this review.

| Field | Verified value |
| --- | --- |
| Immutable tag target | `e79a67104fb7704c7f9fdc25724c8062ad0042b6` |
| Required annotated tag | `astrowoof-natal-authoring-v0.4.62` |
| Wheel | `astrowoof_natal_authoring-0.4.62-py3-none-any.whl` |
| Wheel byte size | `1,385,622` |
| Wheel SHA-256 | `eea9d74ec0ab39cc804ceedb4b00ce8af8cb17ce99c89d6b6276372ba00ab1bb` |

The proposed tag did not exist at review time.  The target's parent is the
version-bump candidate, and the target itself contains only the expected
release-lock documentation and qualification record.

## Gate assessment

- Full maintained suite: 1,196 passed, 3 expected skips.
- Focused release-bound matrix: 43 passed.
- Exact-lock reproducible builds, required-member inventory, installed
  dependency check, release/lifecycle smokes, and installed editorial
  diagnostics matrix all passed.
- The real API `force=False` host coexistence gate passed against the exact
  installed candidate: API handler preservation, one SBE handler, valid
  nonduplicated records, and distinct internal error phases were verified.
- No provider, network, R2, Better Stack, spend, authoritative workspace,
  deployment, or live-QA work occurred in qualification.

## Publication conditions

If the owner authorizes release, publish only the retained exact wheel under
the canonical filename with matching `SHA256SUMS.txt`, then freshly download
and verify both against the coordinates above.  Any byte, member, filename, or
target-commit mismatch blocks publication and requires a new review.
