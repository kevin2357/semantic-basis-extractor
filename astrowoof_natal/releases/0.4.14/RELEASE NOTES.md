# AstroWoof Natal Authoring 0.4.14 Release Candidate

Status: qualified candidate; tagging and publication require explicit approval

## Summary

SBE 0.4.14 adds a closed external-authority next-action contract for retained and
fresh provider-capable authoring work. Lifecycle inspection v0.5 now carries either
one complete snapshot-bound `external_authority_request` or one typed
`external_authority_refusal`. A positive aggregate grant joins the exact request,
ordered actions, full bindings, native observation, and initial-wave identity.

Exact and bounded interactive initial waves hold native single-writer authority
through revalidation and one durable six-member pre-submit intent, release it for
provider I/O, and reacquire it for every returned identity or ambiguity checkpoint.
Generic resume is never create authorization for a stored constrained wave.

The installed provider-free qualification uses real native workspaces, lifecycle
inspection, fresh Python processes, constrained execution, retained replay, and
the real reconciliation entry point. It creates exactly six scripted provider
operations and proves replay/reconciliation cannot create a seventh.

No atomicity is claimed across native persistence and the provider API. Provider
acceptance without a durably recoverable identity remains ambiguity and fails
closed.

## Compatibility

- Python: 3.11+
- AGF: 0.8.1
- SPC: 0.11.0
- Exact and bounded interactive initial-wave continuation: supported
- Batch authority remains one paid action/reservation per round
- Lifecycle inspection v0.4: readable but non-authorizing for this continuation
- Lifecycle inspection v0.5: required for the external-authority handoff

Tagging and publication remain pending the explicit Slice 8 release gate.
