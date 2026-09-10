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
