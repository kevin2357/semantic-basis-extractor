# Slice 4 — Provider-Free Regression Matrix

Date: 2026-08-21
Status: complete

## Outcome

The external-authority lifecycle boundary now has a provider-free matrix spanning
valid request production, typed refusal, malformed inventories, contradictory
cross-object identities, invalid snapshots, writer races, historical lineage, and
constrained execution safety.

## Matrix coverage

| Case | Expected native result | Covered |
|---|---|---|
| Exact six-member initial wave | nonempty joined request | yes |
| Bounded six-member initial wave | nonempty joined request | yes |
| Ordinary prepared action set | nonempty lexically ordered request | yes |
| No prepared actions | never external-authority command | yes |
| Empty request inventory | request validation refusal | yes |
| Duplicate action | request validation refusal | yes |
| Unknown/mismatched ordered ID | request validation refusal | yes |
| Changed binding | request validation refusal | yes |
| Inadmissible stored-wave action | typed native refusal | yes |
| Unjoinable historical initial lineage | typed lineage refusal | yes |
| Wrong eligibility/reasons/capacity/timing | lifecycle validation refusal | yes |
| Outer/request run mismatch | lifecycle validation refusal | yes |
| Outer/request observation mismatch | lifecycle validation refusal | yes |
| Branch/request ordering mismatch | lifecycle validation refusal | yes |
| Request digest mutation | request validation refusal | yes |
| Incomplete workspace snapshot | no request; retain/review | yes |
| Writer exclusivity absent | no request; retain/review | yes |
| Request/grant replay and failure boundaries | no duplicate provider create | yes |

## Read-only and provider-safety assertions

Inspection tests retain byte-identical `run.json` and snapshot evidence. Invalid
read-only states do not authorize, consume, submit, retrieve, deny, or reconcile
provider work. Existing constrained execution tests continue to prove stale,
partial, replay, and interruption behavior around actual provider-capable boundaries
using scripted transports only.

Source-tree fixture reuse remains confined to tests. Slice 5 installed-wheel
qualification will not import source-tree test classes.

## Verification

- Authority inspection/public/schema group: 42 passed, 5 skipped.
- Constrained authority execution: 11 passed.
- Historical lineage fence: 7 passed.
- Lifecycle consumer/closeout/events: 45 passed.
- Total focused: 105 passed, 5 environment-dependent schema checks skipped.
- Provider calls/spend/retained workspace access: 0 / USD 0 / none.

## Gate

PASS. Every planned Slice 4 class is explicitly covered through a public or real
native boundary, and invalid evidence cannot become provider-capable execution.

