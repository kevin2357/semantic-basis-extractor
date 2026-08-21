# AstroWoof Natal Authoring 0.4.15

Status: published and independently verified

## Summary

SBE 0.4.15 tightens lifecycle inspection v0.5 so the external-authority branch can
no longer publish combinations that the API already had to reject. A valid
`await_external_authority` selection now requires one nonempty, completely joined,
snapshot-bound request with the exact branch/capacity reasons, no local work ready,
and no timing recommendation. A typed native-review refusal requires `command=none`,
empty action IDs, no request, and the corresponding closed refusal projection.

The patch also adds redacted predicate diagnostics through existing typed event
names and operator logs. Diagnostics remain non-authoritative and failure-isolated.
No new public state, scheduling choice, provider action, or ownership transfer is
introduced.

The provider-free installed qualification advances to the closed
`astrowoof.external_authority_qualification.v2` receipt and proves both request and
refusal lifecycle conditionals against real workspace, snapshot, fresh-process,
constrained-execution, replay, and reconciliation boundaries.

## Compatibility

- Python: 3.11+
- AGF: 0.8.1
- SPC: 0.11.0
- Lifecycle inspection v0.5 identity is retained and tightened in place.
- Valid v0.5 request/refusal documents retain their existing shape and meaning.
- Lifecycle inspection v0.4 remains readable but non-authorizing here.
- API queue, lease, reservation, billing, and product authority remain API-owned.

## Qualification

- Complete source suite: 531 passed; 27 existing environment-dependent skips.
- Installed release smoke: passed with 50 cards and four summaries.
- Installed external-authority qualification v2: passed; all assertions true.
- Installed provider-pending 4+2 qualification: passed.
- Fixed-epoch double build: byte-identical.
- Wheel inventory: 133 entries, 78 resources, `py.typed` present, no bytecode.
- Provider network calls/retrievals/spend: 0 / 0 / USD 0.

Candidate wheel SHA-256:
`f557b439fa3096bb1c33f020adc4be40fb3bb749857bc8c3c7a4715cc131a052`.

The immutable annotated tag points to
`807f9377fe54239d9311026835e38941fa22f898`. GitHub reports the published wheel at
883238 bytes with the same SHA-256 as the qualified local artifact. This
post-publication record does not move the tag.
