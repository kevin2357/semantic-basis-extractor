# AstroWoof Natal Authoring 0.4.16

Status: qualified artifact; immutable tag and publication pending

## Summary

SBE 0.4.16 introduces lifecycle inspection v0.6, which separates an immutable
native/provider checkpoint basis from the trusted-time temporal decision derived
from that basis. Re-inspecting byte-identical provider-pending state at a later
API-supplied canonical UTC time can now progress from not-due to due without
pretending the underlying checkpoint changed. Provider retrieval and persisted
provider evidence still create a new checkpoint basis.

The release adds strict packaged schemas and Python semantic validators for the
v0.6 lifecycle and v2 external-authority request. The Python validators remain
closed and complete even when the optional `jsonschema` package is unavailable.
Authority requests bind the exact checkpoint basis, ordered action inventory, and
public authorization bindings rather than incidental observation time.

The supported `inspect-temporal` CLI/API requires explicit trusted time. Exact and
bounded interactive and Batch routes share the contract; legacy bounded-v1 Batch
state fails closed. Lifecycle v0.5 remains available unchanged for existing
consumers but must not be silently reinterpreted as v0.6.

## Compatibility

- Python: 3.11+
- AGF: 0.8.1
- SPC: 0.11.0
- New lifecycle identity: `astrowoof.lifecycle_inspection.v0.6`
- New external-authority request identity: v2, joined to one validated v0.6 inspection
- Existing lifecycle v0.5 reader remains supported unchanged
- API owns trusted observation time, lease/capacity admission, global spend policy,
  persistence, and command invocation

## Qualification

- Complete source suite: 583 passed; 28 existing environment-dependent skips.
- Focused lifecycle/capacity suite: 55 passed; one optional-schema skip.
- Installed release smoke: passed with 50 cards and four summaries.
- Installed provider-pending qualification: passed with six creates, bounded 4+2
  retrieval, no duplicate create/retrieval, same-basis temporal progression, and a
  new basis after reconciliation.
- Fixed-epoch double build: byte-identical.
- Wheel inventory: 136 entries, 80 resources, `py.typed` present, no bytecode.
- Provider network calls/spend during qualification: 0 / USD 0.

Candidate wheel SHA-256:
`56e26d82bb4689907dc830903721acf34a4c385557c7825c3ece19297f48d339`.
