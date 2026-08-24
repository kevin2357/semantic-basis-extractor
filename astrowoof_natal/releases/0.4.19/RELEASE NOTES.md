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
- External provider/network calls: 0.
- Provider POST/create/submit/retry calls: 0.
- Spend: USD 0.

The committed-source artifact identity, reproducible-build hash, and installed-wheel
receipts are recorded after the artifact-source commit is created.
