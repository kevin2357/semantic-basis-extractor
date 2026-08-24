# AstroWoof Natal Authoring 0.4.19

Status: release candidate; immutable publication requires owner authorization

SBE 0.4.19 adds a narrow, provider-free operator-retirement contract for an
exact-Natal workspace that is internally quiescent but otherwise stranded in an
eligible nonterminal state.

The public dry-run and execute boundaries validate the complete native checkpoint,
action closure, logical workspace identity, route, and request digest. Successful
execution transitions native truth to `POLICY_STOPPED / operator_retired`, seals a
native result and receipt, and proves that no provider custody, provider-pending
work, or locally runnable continuation remains. Exact replay and compatible later
inspection are deterministic.

This operation never cancels, retrieves, submits, retries, or otherwise contacts a
provider. It refuses provider evidence or ambiguity, unresolved providerless
actions, stale bindings, runnable local work, unsupported routes, and contradictory
state. API custody, leases, reservations, resource release, and product policy
remain API-owned.

## Qualification

- Complete source suite: 623 passed; 33 environment/opt-in skips.
- Artifact source commit: `3151c4fc15d1436e0c250228c2069e4771be30da`.
- Fixed build epoch: `1787615331`.
- Two byte-identical wheel builds; SHA-256
  `6ccc2a5ba859830e60f9139e4e52e9795602dff30569c1dbb6ba9579b2f38f79`.
- Generic installed release smoke: pass.
- Installed operator-retirement qualification: pass; receipt SHA-256
  `37ff37dd42a0a5cc593ddf10bf645a456904d0f241ae11d5be74ab904f3c413f`.
- External provider/network calls: 0.
- Provider POST/create/submit/retry calls: 0.
- Spend: USD 0.

Tagging and publication remain pending explicit owner authorization.
