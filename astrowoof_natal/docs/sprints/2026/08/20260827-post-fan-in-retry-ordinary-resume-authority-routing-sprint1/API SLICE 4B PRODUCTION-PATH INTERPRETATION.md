# API Slice 4B Production-Path Interpretation

Status: approved to implement after this clarification.

## Decision

The API confirms SBE's aggregate-member interpretation. The earlier phrase
"each successor requires its own distinct ordinary v2 authority request" was
imprecise. The API's actual public boundary is deliberately
`ordinary_action_set`: one exact, sealed request/grant can authorize an ordered
set of co-ready ordinary actions.

Therefore, after both completed-evidence local operations have been consumed
and retained provider custody has cleared, the two successors may be members of
one aggregate ordinary-v2 action-set request/grant. Each member must still have
its own exact action ID, binding, API paid-action reservation, authorization
document, and ordered grant member. This is the preferred topology; it preserves
the established rule that retained provider custody cannot be outranked by a
fresh provider create.

## Required invariants

- Do not expose or dispatch the successor action set while either original
  provider operation remains pending.
- Keep the ordered action inventory deterministic and seal the complete set in
  the request/grant digest. API admission is all-or-none for the set; it must
  never silently grant or dispatch a subset.
- Preserve distinct member bindings and validate them against the checkpoint
  inventory. A common envelope does not make the member identities fungible.
- The fixture must make the authority topology observable: request kind,
  request/grant digest, deterministic ordered member action IDs, and the fact
  that the exact request is an aggregate action set. It need not reveal private
  workspace state, prompts, provider payloads, or protected provenance.
- Keep reconciliation retrieval-only and local fan-in authority-free. No API
  reconstruction of a native command or provider create is authorized by this
  witness.

## Selector correction and downstream witness

The characterized mixed-custody result is a genuine selector gap, not a reason
to weaken custody precedence. Selecting `ordinary_resume` when retained provider
custody contains validated completed evidence is the narrow correction required
to surface the v0.7 local operation. The still-pending action remains retained
until its own reconciliation and local consumption.

For retry-to-polish, use polish only after the normal accepted-pass and
final-assembly prerequisites make it a real selected action. Do not manufacture
a polish action beside an incomplete retry workspace merely to make the fixture
interesting.

## API follow-through

API Sprint 54 will distinguish its generated per-action simulations from the
installed SBE witness. The simulator can model sequential one-action admissions;
that is not a claim that real SBE must emit separate temporal envelopes when
multiple ordinary actions are co-ready.
