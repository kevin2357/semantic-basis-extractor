# API review — Slice 2 same-checkpoint witness

## Decision

Approved with the precedence refinement and an additive packaging request for
Slice 3.

The three-version witness establishes the intended narrow seam and confirms
that the SBE 0.4.31 readers/validators can represent it. It also correctly
refines the earlier overly broad “provider custody wins” shorthand:

- due provider custody selects bounded reconciliation;
- unrelated **not-due** custody may remain retained while exact deterministic
  fan-in consumes separately completed evidence; and
- neither case authorizes provider creation or permits API to invent work.

That is a better, more precise custody rule for the API adapter.

## Slice 3 request

Please add one small, closed, packaged provider-free qualification receipt (and
reader/validator/fixture support as appropriate) for this same-checkpoint v0.5,
v0.7, v0.8 witness. It should expose only public documents and their stable
identity joins/declared selected operation—no workspace archive, prompts,
provider payloads, or private state.

Reason: API must not import SBE test helpers or construct a production-shaped
workspace to reproduce the case. A released immutable fixture lets the API
exercise the real reader/validator boundary and protects the regression from
drifting into a parallel miniature.

The receipt should make both safe branches visible:

1. completed fan-in alongside unrelated **not-due** custody → exact local
   operation, retained custody, no provider create; and
2. due custody or lineage conflict → the v0.8-selected reconciliation/review
   outcome.

If adding package material is necessary, a fresh SBE release is appropriate;
it remains additive qualification material, not a lifecycle semantic change.

No retained-QA operation, provider work, deployment, or release is authorized
by this review beyond the normal later release gate.
