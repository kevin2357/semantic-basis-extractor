# SBE 0.4.48 release candidate

## Decision state

Candidate construction from the committed artifact source is green. Exact
release-lock rebuild and repeated installed qualification remain required
before Voof-paws 4. Tagging and publication are not yet authorized.

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

Commit this record as the release lock, rebuild twice from that exact commit
using the recorded epoch, prove the wheel remains byte-identical, and repeat
the installed public qualifications. Then request API technical review and
explicit owner authorization before creating the immutable tag or release.
