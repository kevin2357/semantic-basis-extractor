# Pre-Slice 0 source and trace assessment

## Preliminary verdict

Providence appears to be a live reachability proof for a known API settlement
gap, not a malformed SBE terminal-review result.

At `2026-09-04T20:31:47.736Z`, SBE emitted an invocation-bound public command
result for:

- native invocation `ninv_7440ab2c75754ac3a5fb35f0`;
- result `nres_0f3d3b6a3cc256db4b7a9c1b`;
- receipt `nreceipt_2b0e8df6e0278a32ff245d61`;
- `outcome=review_required`;
- `custody_finality=providerless_denial_required`;
- `new_provider_create_permitted=false`; and
- exit code 2.

Immediately before publication, the sanitized native-state summary reported
seven `REPORTED` actions and one `PREPARED` polish action,
`paid_f5a73dc0325db8a8aedafe05`. It reported seven provider identities, zero
provider custody, one prepared action, no ambiguity, and no live v2 intent.

## Why the finality is source-consistent

The released terminal-review v0.2 contract maps:

- `REPORTED` to `terminally_accounted`;
- `PREPARED` without provider identity to `providerless_denial_only`; and
- an inventory containing providerless-denial custody but no provider or
  ambiguity custody to `providerless_denial_required`.

The Python validator recomputes the denial inventory and aggregate finality from
the ordered action rows. API's native-transition validator independently
recognizes the same five-value finality vocabulary and performs the same
derivation.

API then failed at its later disposition property, whose implemented branches
are only:

- `final` -> terminal closeout; and
- `provider_reconciliation_required` with a nonempty reconciliation inventory
  and empty denial inventory -> retained reconciliation.

Every other valid nonfinal custody shape currently raises the observed
`unsupported settlement boundary` error.

## Prior cross-repo decision

API Sprint 67 already recorded `providerless_denial_required` as a typed
nonterminal refusal pending a supported denial-settlement boundary. It explicitly
prohibited terminal cleanup, provider creation, and inferred denial. Providence
is consistent with that frozen decision.

## Remaining evidence question

The logs expose the result/receipt identities, aggregate finality, complete
action/state/stage summaries, and the failing API branch. They do not expose
every sealed action row, binding digest, journal field, projection reference,
or the result's cause code.

Those fields should first be requested through an existing API-owned exact
artifact/export. If no such evidence exists, a separately authorized exact
checkpoint read may be used after API supplies an immutable coordinate packet.

No retained workspace access or runtime mutation occurred during this
assessment.

