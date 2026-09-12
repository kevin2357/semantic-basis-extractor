# SBE 0.4.60 release-lock qualification

Status: technically qualified at the pre-tag/release boundary; API installed-
wheel consumer review and owner publication authorization remain required.

## Candidate identity

- package: `astrowoof-natal-authoring`
- version: `0.4.60`
- expected tag: `astrowoof-natal-authoring-v0.4.60`
- branch: `codex/20260910-sbe0460-quarantiner-release`
- recorded `SOURCE_DATE_EPOCH`: `1789089592`
- canonical wheel: `astrowoof_natal_authoring-0.4.60-py3-none-any.whl`
- wheel bytes: 1,383,825
- wheel members: 310
- wheel SHA-256:
  `618caee2c2f338cf868cfb024f764217c7b4ef4c83aff283b2bf78cd6e67d627`
- retained candidate:
  `C:\tmp\sbe-0460-lock-964c6c8\wheel-one\astrowoof_natal_authoring-0.4.60-py3-none-any.whl`

## Completed gates

- Expanded focused matrix: 139 passed, 3 expected skips.
- Superseding broad/full suite: 1,184 passed, 60 expected skips.
- Test inventory SHA-256:
  `2bd1d2a50c8dc738f5027f24f5989f986d64ac877b7d4bc09748b9d2c6aefb29`.
- Initial clean archive reproducibility and inventory: pass.
- Initial clean installed package, release smoke, adversarial lifecycle, and
  operator-disposition qualification: pass.
- Exact-lock two-build byte reproducibility: pass.
- Exact-lock clean installed `pip check`, version/site-packages/export check,
  release smoke, adversarial lifecycle QA, and operator-disposition QA: pass.
- Provider/network operations and spend: zero.

## Lock boundary

The commit containing this completed document is the release-lock source. Its
two clean archive builds use the recorded epoch above. Sprint documentation is
not package data, so the final documentation commit must reproduce the exact
wheel digest above before handoff. Only those exact retained bytes may be
offered to API for the installed-wheel/real-restore consumer gate.

No tag, GitHub Release, asset publication, live provider operation, retained-QA
read, API mutation, or Render mutation is authorized by this document.
