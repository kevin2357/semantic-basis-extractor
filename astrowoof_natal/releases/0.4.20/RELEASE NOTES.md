# AstroWoof Natal Authoring 0.4.20

Status: qualified and authorized for immutable publication

SBE 0.4.20 completes the executable external-authority v2 bridge introduced by
temporal lifecycle inspection v0.6. A validated ordinary-action request can now be
joined to a closed API grant and complete authorization documents, committed as one
writer-fenced native intent, dispatched outside the writer, and checkpointed one
provider identity at a time before later reconciliation.

The release preserves the existing v1 initial-wave paths and existing Batch
mechanisms. Ordinary external-authority v2 Batch dispatch is deliberately deferred
and refuses with `unsupported_contract`; consumers must not infer an adapter or
convert those actions to Response transport.

## Qualification

- Artifact source commit: `706f8cddf07cc79aaf394d1741031b3f3f927359`.
- Fixed build epoch: `1787636319`.
- Two byte-identical wheels; SHA-256
  `37fc4220fcaa3f003ab0171cd5c6542bb203287c780c953bd882ca96a10e65c8`.
- Fast focused source gate: 33 passed; 2 optional-schema skips.
- Generic installed release smoke: pass.
- Installed external-authority v2 qualification: pass; receipt SHA-256
  `cb1d813d781b751982031d4dd91528d12128c5eb35aac79dd52bcdb95185509e`.
- Real provider/network calls and spend: 0.

The complete source suite was exercised before final cleanup: 654 tests passed,
35 expected tests skipped, and its sole failure exposed a Windows CRLF checkout
issue in a pre-existing frozen-artifact hash assertion. The test was corrected to
hash canonical LF bytes and its focused regression passed. No production behavior
or frozen evidence changed.
