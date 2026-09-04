# SBE 0.4.47 release candidate

## Decision state

Released. Candidate construction, release-lock rebuild, installed SBE
qualification, API Sprint 76 release-pair qualification, immutable tagging,
publication, and fresh-download verification are complete.

## Immutable candidate coordinates

- Artifact-source commit:
  `31a09e472bae871a0105d7a5e5719592b9a92407`
- Distribution version: `0.4.47`
- Expected annotated tag: `astrowoof-natal-authoring-v0.4.47`
- Wheel: `astrowoof_natal_authoring-0.4.47-py3-none-any.whl`
- Wheel bytes: `1,199,948`
- Wheel SHA-256:
  `4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875`
- Recorded `SOURCE_DATE_EPOCH`: `1788547986`
- SPC version: `0.11.1`
- SPC wheel SHA-256:
  `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`

## Qualification

- Full maintained suite: 1,035 passed; 52 expected skips.
- Two clean committed-source builds: byte-identical.
- Wheel inventory: 258 members; no absolute paths.
- Isolated install and `pip check`: pass.
- Generic installed release smoke: pass.
- Installed mixed-custody v1 qualification: pass.
- Installed terminal-review v2 qualification: pass.
- Installed finalization-boundary v2 qualification: pass.
- Provider/network/spend activity: zero.
- QA, R2, retained-workspace, and API mutation: none.

## Final disposition

API consumed this exact wheel SHA-256 through the previously failing Sprint 76
release-pair command and passed. The release-lock commit was rebuilt twice and
requalified before the annotated tag was created. Published and downloaded
assets match the qualified wheel and checksum manifest exactly.
