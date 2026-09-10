# Evidence — packaged fixture byte canonicalization

Status: `0.4.57` source correction under focused qualification.

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
