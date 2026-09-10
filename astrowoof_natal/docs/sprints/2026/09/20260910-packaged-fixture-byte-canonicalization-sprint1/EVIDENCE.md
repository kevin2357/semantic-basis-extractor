# Evidence — packaged fixture byte canonicalization

Status: complete through immutable `0.4.57` publication and authenticated
fresh-download verification.

## Failure facts

- `ambiguous_provider_submission`: source/catalog SHA-256
  `2e2d5de510f4141d30309b0a35082eda27a7fd3c0477f976c3eca351c5ad1395`;
  published-wheel SHA-256
  `e951ba3e86eec4837b36ed03f7dd34a3328dcdb10941052e934a497b0720835f`.
- JSON values are equal; the wheel has one additional carriage return before
  the final newline.
- `providerless_denial_terminalization` and `providerless_batch_denial` fail
  for the same LF-to-CRLF export conversion.
- Six other catalog entries currently match CRLF bytes accidentally and would
  not be portable to a non-Windows or `core.autocrlf=false` release builder.

## Correction boundary

- Explicit LF policy for packaged JSON.
- Canonical LF bytes and regenerated raw-byte digests for all nine catalog
  fixtures.
- No JSON values, schemas, runtime logic, lifecycle behavior, provider custody,
  or external authority semantics change.

## Qualification evidence

- Source focused matrix: 125 passed, 11 expected skips.
- Installed focused matrix with jsonschema: 120 passed, no skips.
- `core.autocrlf=true` and `false` Git archives: byte-identical at SHA-256
  `a2614283a96a39197773959948fc1db36c1bb27346e736d498f5437738c22eab`.
- Candidate wheels: byte-identical; 1,375,422 bytes; SHA-256
  `957f677d46ad01a7a7243e79db611c14fb63763868056aae971d9d50642abc1c`.
- Installed provider-free adversarial QA and release smoke: passed.
- API imported installed version `0.4.57` from the isolated `site-packages` and
  the public catalog reader succeeded. Remaining selected-test failures are
  strict API consumer expectations for the six changed LF digests.

## Immutable publication evidence

- artifact-source/tag target:
  `9158e89684adbcef518c843169c2a0236847bc97`;
- annotated tag: `astrowoof-natal-authoring-v0.4.57`;
- tag object: `8c900b55c934318f75c8394959d6b8fc3d00ceee`;
- GitHub Release ID: `RE_kwDOToQdE84XBOOW`;
- published at: `2026-09-10T10:45:43Z`;
- wheel asset ID: `554812481` / `RA_kwDOToQdE84hEcRB`;
- wheel: 1,375,422 bytes; SHA-256
  `957f677d46ad01a7a7243e79db611c14fb63763868056aae971d9d50642abc1c`;
- checksum asset ID: `554812480` / `RA_kwDOToQdE84hEcRA`;
- checksum asset: 116 bytes; SHA-256
  `f2cc9e33e78b3f7a3a81962d9a01f67bad808c62b7a8b61929ea553141c8fede`;
- GitHub-reported digests, qualified local assets, fresh authenticated
  downloads, and the downloaded checksum line all agree; and
- release URL:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.57`.
