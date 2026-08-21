# SBE 0.4.14 Compatibility

## Runtime boundary

- CPython 3.11 or newer.
- `semantic-projection-core==0.11.0`.
- Qualified upstream identities remain AGF 0.8.1 and SPC 0.11.0.
- Stable logical absolute workspace restoration and complete native snapshot
  validation remain mandatory.

## Consumer boundary

- Lifecycle inspection v0.5 is the authorizing inspection contract for external
  next-action requests and typed refusals.
- Lifecycle inspection v0.4 remains accepted for historical read/retain behavior,
  but cannot authorize constrained provider creation.
- Exact and bounded interactive six-member initial waves support the constrained
  aggregate-grant boundary.
- Exact and bounded Batch retain their existing one-round/one-paid-action model.
- Existing ordinary per-action authorization and providerless-denial contracts
  remain supported.

Consumers must validate the packaged contract catalog and reject unsupported
versions or unknown fields deterministically.
