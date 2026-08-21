# SBE 0.4.15 Compatibility

## Runtime boundary

- CPython 3.11 or newer.
- `semantic-projection-core==0.11.0`.
- Qualified upstream identities remain AGF 0.8.1 and SPC 0.11.0.
- Stable logical absolute workspace restoration and complete native snapshot
  validation remain mandatory.

## Consumer boundary

- Lifecycle inspection v0.5 remains the authorizing inspection contract.
- `await_external_authority` requires reason `spend_authorization_required`, a
  nonempty exact action inventory, no local-ready work, and null timing fields.
- A typed external-authority refusal requires `command=none`, empty action IDs,
  retain-for-review capacity, and no embedded request.
- Outer inspection, observation, logical root, request, and ordered action identity
  must join exactly.
- Lifecycle inspection v0.4 remains historical read/retain evidence and cannot
  authorize constrained provider creation.

Consumers must validate the packaged contract catalog and reject unsupported or
contradictory documents rather than repairing or inferring them.
