# SBE 0.4.60 release-lock qualification

Status: release-lock source prepared; exact-lock rebuild pending.

## Candidate identity

- package: `astrowoof-natal-authoring`
- version: `0.4.60`
- expected tag: `astrowoof-natal-authoring-v0.4.60`
- branch: `codex/20260910-sbe0460-quarantiner-release`

## Completed gates

- Expanded focused matrix: 139 passed, 3 expected skips.
- Superseding broad/full suite: 1,184 passed, 60 expected skips.
- Test inventory SHA-256:
  `2bd1d2a50c8dc738f5027f24f5989f986d64ac877b7d4bc09748b9d2c6aefb29`.
- Initial clean archive reproducibility and inventory: pass.
- Initial clean installed package, release smoke, adversarial lifecycle, and
  operator-disposition qualification: pass.
- Provider/network operations and spend: zero.

## Lock boundary

The commit containing this document is the proposed release-lock source. Two
fresh clean archive builds must use that commit timestamp as
`SOURCE_DATE_EPOCH`, produce byte-identical canonical wheels, and repeat the
installed qualification. Only those exact retained bytes may be offered to API
for the installed-wheel/real-restore consumer gate.

No tag, GitHub Release, asset publication, live provider operation, retained-QA
read, API mutation, or Render mutation is authorized by this document.
