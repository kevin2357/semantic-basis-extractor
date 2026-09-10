# Evidence — packaged fixture byte canonicalization

Status: `0.4.57` source and installed-wheel qualification passed; API digest
review remains pending.

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
