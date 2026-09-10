# Log — packaged fixture byte canonicalization

## 2026-09-10 — API broad-suite finding reproduced

- Confirmed the published `0.4.56` wheel differs from tagged/source bytes only
  by Windows CRLF conversion for the first reported fixture.
- Expanded the inventory and found three immediate catalog failures; six other
  entries passed only because both checkout and wheel happened to use CRLF.
- Root cause is `core.autocrlf=true` combined with `.gitattributes` declaring
  only `* text=auto`, allowing Git archive bytes to depend on host policy.
- Selected the Maintainer Release Playbook's focused packaged-fixture patch
  gate. No immutable `0.4.56` tag or asset was changed.

## 2026-09-10 — Source correction

- Froze corrective candidate version `0.4.57` before release-bound testing.
- Added explicit `*.json text eol=lf` repository policy.
- Canonicalized all nine digest-bearing catalog fixtures to LF and regenerated
  the six digests that had previously described accidental CRLF checkout bytes.
- Added a public-reader regression requiring every catalog fixture to contain
  no CRLF sequence.
- No JSON value or runtime semantic changed.

## 2026-09-10 — Focused source and package qualification

- Focused source matrix passed 125 tests with 11 expected optional/install-gate
  skips; semantic comparison proved all nine fixture JSON values unchanged.
- Commit `9158e89` was pushed as the reviewable `0.4.57` source candidate.
- Git archives made with `core.autocrlf=true` and `false` were byte-identical.
  Every catalog fixture was LF and matched its declared digest in both.
- Two fixed-epoch wheels were byte-identical at 1,375,422 bytes and SHA-256
  `957f677d46ad01a7a7243e79db611c14fb63763868056aae971d9d50642abc1c`.
- The 307-member inventories were identical and contained no forbidden cache,
  bytecode, build, or distribution residue.
- Clean installed qualification passed `pip check`, 120 focused tests with
  schema validation enabled, provider-free adversarial QA, and installed
  release smoke.
- API loaded installed SBE `0.4.57` and its public reader returned all 15 cases,
  proving the published-0.4.56 integrity failure is corrected. API's two
  selected tests then failed only at its frozen six old digest expectations,
  which is the intended consumer review/update gate.

## 2026-09-10 — 0.4.57 immutable publication

- API technically approved the candidate and independently confirmed the
  canonicalization boundary; the owner explicitly authorized tag/release.
- Per owner direction, no approval or publication document was committed before
  immutable identity was established.
- Created annotated tag `astrowoof-natal-authoring-v0.4.57` directly at artifact
  source `9158e89684adbcef518c843169c2a0236847bc97`.
- Remote tag object `8c900b55c934318f75c8394959d6b8fc3d00ceee` peels exactly to that
  artifact-source commit.
- Published GitHub Release `RE_kwDOToQdE84XBOOW` at
  `2026-09-10T10:45:43Z` with only the exact wheel and checksum manifest.
- Fresh authenticated download reproduced the wheel and checksum asset sizes
  and hashes, and the downloaded checksum line matched the qualified wheel.
- No tag movement, asset substitution, API deployment, Better Stack write,
  provider call, database operation, or retained-run mutation occurred.
