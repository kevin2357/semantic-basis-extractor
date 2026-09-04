# SBE 0.4.48 release candidate

## Decision state

Released. Candidate construction, exact release-lock verification, API review,
owner authorization, immutable tagging, asset publication, and fresh-download
verification are complete.

## Candidate coordinates

- Artifact-source commit:
  `96dd0ef539e1972ce694f75b60eac7bc3491caa8`
- Distribution version: `0.4.48`
- Expected annotated tag: `astrowoof-natal-authoring-v0.4.48`
- Wheel: `astrowoof_natal_authoring-0.4.48-py3-none-any.whl`
- Wheel bytes: `1,209,061`
- Wheel SHA-256:
  `d1e84055183e2c45eb687aed61c247425008edec53e33f424c57cc89bf89a8e0`
- Recorded `SOURCE_DATE_EPOCH`: `1788559932`
- SPC version: `0.11.1`
- Release-lock commit:
  `49f9e2e3b76d71f84a90542f0fedfa2ae06d4e00`

## Qualification

- Focused affected matrix: 104 passed; 6 expected optional-schema skips.
- Broad/full suite: not run under the approved additive focused-patch gate.
- Two clean committed-source builds: byte-identical.
- Wheel inventory: 262 members; expected package data and entry point present;
  forbidden generated/private members absent.
- Isolated install and `pip check`: pass.
- Generic installed release smoke: pass.
- Installed providerless-denial v1/v2 CLI, schema, reader, validator, fixture,
  refusal, replay, and identity qualification: pass.
- Provider/network/spend activity: zero.
- QA, R2, retained-workspace, API mutation, and live settlement: none during
  release qualification.

## Remaining gate

API approved the exact release-lock commit, wheel SHA, focused-gate scope, and
installed qualification. The annotated tag points to the release lock, and the
published/downloaded wheel and checksum manifest match the qualified artifact.
