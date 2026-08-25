# Slice 4 — Route and Holistic Lifecycle Qualification Review

Date: 2026-08-24
Status: implementation complete; API review requested before installed-wheel packaging

## Outcome

The v2 execution bridge is qualified across the exact-Natal and bounded-Natal
interactive Response routes for every supported ordinary stage:

- `creative_retry`;
- `polish`;
- `qualitative_critic`; and
- `qualitative_candidate`.

Initial six-pass authoring remains on its existing v1 constrained authority path.
The v2 bridge neither accepts nor reinterprets `authoring_initial`.

## Qualified lifecycle chain

For both exact and bounded route families, provider-free source qualification now
executes this same-workspace chain:

1. build a real six-member initial-wave authorization;
2. execute the production initial-wave create coordinator with six distinct
   scripted Response identities;
3. publish a snapshot-valid provider-pending workspace;
4. run the real provider reconciliation implementation in SBE-selected 4+2 cycles;
5. prove six unique retrievals and no duplicate creates/retrievals;
6. prepare a real ordinary paid action;
7. inspect v0.6 and export its exact v2 request;
8. build the exact v2 grant and complete authorization document outside native
   state;
9. commit the writer-fenced v2 intent;
10. dispatch through the public persisted-intent-selected boundary;
11. durably checkpoint the Response identity; and
12. prove the next due v0.6 decision selects `provider_reconciliation_cycle` and
    the exact SBE-selected action inventory.

The existing deployed four-route qualification also passes, including exact and
bounded initial interactive create/detach and both one-round/six-member Batch
routes. The existing provider-pending qualification independently passes the 4+2
retrieval and new-checkpoint-basis assertions.

## Frozen first-release route matrix

| Route/stage | Response | Batch |
|---|---|---|
| Exact initial wave | Existing v1 command | Existing exact Batch path |
| Bounded initial wave | Existing v1 command | Existing bounded Batch path |
| Exact creative retry | v2 supported | v2 deferred/fail closed |
| Bounded creative retry | v2 supported | v2 deferred/fail closed |
| Exact polish/critic/candidate | v2 supported | v2 deferred/fail closed |
| Bounded polish/critic/candidate | v2 supported | v2 deferred/fail closed |
| Any provider-bound action | reconciliation only | reconciliation only |
| Any entered-call/identity-less action | ambiguity/review | ambiguity/review |

Although Slice 0 described initial/retry Batch as parity candidates, this first v2
executor deliberately freezes only interactive Response ordinary-action dispatch.
Batch initial waves remain served by their existing route mechanisms. A v2 Batch
ordinary action is refused as `unsupported_contract` before authorization,
consumption, intent publication, or provider I/O; it is never silently treated as
Response work.

## Fail-closed evidence

- Exact and bounded optional Batch requests refuse before native mutation.
- Bounded route bindings must carry the explicit `bounded_natal.v2:` namespace.
- `authoring_initial`, legacy bounded topology, unsupported contracts, missing
  route identity, and mixed/noninteractive mechanisms cannot enter v2 intent.
- Provider-bound, ambiguous, stale, reordered, or binding-mismatched inputs retain
  the earlier Slice 1–3 zero-I/O refusals.
- The grant remains whole-inventory authority; API cannot select a subset.
- The due retrieval subset remains SBE-selected.

## Evidence

Focused Slice 0–4, temporal lifecycle, deployed-QA, and pending-lifecycle suite:
**59 tests passed** with JSON Schema enabled.

Additional direct receipts:

- deployed four-route qualification: `pass`;
- exact/bounded interactive concurrent create/detach: `pass`;
- exact/bounded one-round six-member Batch cardinality: `pass`;
- provider-pending lifecycle qualification: `pass`;
- first reconciliation cycle: 4 actions;
- second reconciliation cycle: 2 actions; and
- final-QA precedence and duplicate-claim pre-provider refusal: `pass`.

All creates/retrievals were scripted and provider-free. OpenAI/network calls,
credentials, provider spend, and retained-QA workspace access: **0**.

## Slice 5 review questions

1. Does API approve the frozen first-release matrix, specifically deferring all v2
   ordinary Batch dispatch while preserving existing initial-wave Batch routes?
2. Is the same-workspace exact/bounded 4+2-to-v2 trace sufficient before packaging
   the installed-wheel qualification?
3. May Slice 5 expose this as a provider-free installed command/receipt and prepare
   the consumer handoff/release candidate?
