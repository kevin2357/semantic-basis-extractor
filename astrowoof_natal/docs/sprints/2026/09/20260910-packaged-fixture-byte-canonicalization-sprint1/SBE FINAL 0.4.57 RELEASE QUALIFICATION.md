# SBE final 0.4.57 release qualification

## Outcome

Release `0.4.57` corrects the package-byte identity defect discovered in the
published `0.4.56` wheel. Packaged JSON now has an explicit LF policy, making
Git archive and wheel content independent of host `core.autocrlf` settings.

## Qualification

- all nine catalog fixtures are canonical LF and match their declared raw-byte
  SHA-256 identities;
- all nine parsed JSON values are unchanged from `0.4.56` source;
- focused source matrix: 125 passed, 11 expected skips;
- `core.autocrlf=true` and `false` Git archives: byte-identical;
- installed focused matrix with schema validation: 120 passed, no skips;
- provider-free adversarial QA and installed release smoke: passed;
- API's installed public reader returned all 15 cases; and
- two candidate wheels were byte-identical with clean 307-member inventories.

## Immutable publication

- artifact-source commit:
  `9158e89684adbcef518c843169c2a0236847bc97`;
- annotated tag: `astrowoof-natal-authoring-v0.4.57`;
- tag object: `8c900b55c934318f75c8394959d6b8fc3d00ceee`;
- wheel size: 1,375,422 bytes;
- wheel SHA-256:
  `957f677d46ad01a7a7243e79db611c14fb63763868056aae971d9d50642abc1c`;
- GitHub Release ID: `RE_kwDOToQdE84XBOOW`;
- publication time: `2026-09-10T10:45:43Z`;
- fresh authenticated downloads reproduced both published assets and the
  checksum line; and
- release URL:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.57`.

The immutable `0.4.56` tag and assets were not changed. API follow-up is to pin
this exact 0.4.57 wheel, adopt the six reviewed LF digests, and rerun its broad
gate before deployment.
