# Slice 0 — Failure-Shape Reconnaissance

Date: 2026-08-21
Status: complete; awaiting API review

## Result

The retained incident's exact failed predicate remains unproven because the rejected
raw lifecycle inspection is not present in the available sprint evidence. The
provider-free production-shaped reproducer does, however, narrow the problem and
identify two concrete native validation gaps.

Empty inventory is no longer the only leading explanation. SBE's ordinary request
builder and request validator already prevent it, while lifecycle v0.5 currently
accepts two other contradictions that the API correctly refuses:

- an `await_external_authority` branch reason other than
  `spend_authorization_required`; and
- a non-null `execution_branch.not_before` on that branch.

These are proven contract-hardening defects. Neither is proven to be the retained
run's exact causal predicate.

## Real inspection-path findings

The new provider-free test constructs complete exact and bounded initial-wave
workspaces using the existing production-shaped fixture builder, writes their full
workspace snapshots, and enters through real `inspect_lifecycle()`.

Both routes produced:

- command `await_external_authority`;
- `eligible_now == false`;
- reason `spend_authorization_required`;
- capacity disposition `await_external_authority`;
- six nonempty ordered action IDs exactly equal to the embedded request;
- `not_before == null`; and
- byte-identical `run.json` and workspace snapshot before/after inspection.

Thus the supported normal 0.4.14 path satisfies every API predicate.

## Inadmissible inventory finding

A production-shaped stored initial wave with one ledger member changed from
`PREPARED` to `AUTHORIZED` was inspected through the same public path. SBE emitted:

- command `none`;
- capacity `retain_for_review`;
- no request;
- a closed refusal with reason `native_state_inconsistent`; and
- no native state or snapshot mutation.

This confirms the intended request-failure conversion works for that representative
inadmissible inventory. It does not emit an empty create-capable request.

## Five-predicate mutation matrix

The API incident message combines five predicates. Starting from the valid exact
inspection and changing one field at a time produced:

| Mutation | API-equivalent guard | SBE v0.5 validator |
|---|---|---|
| `eligible_now = true` | refuses | refuses |
| wrong branch reason | refuses | **accepts — gap** |
| wrong capacity disposition | refuses | refuses |
| empty branch action IDs | refuses | refuses through request/branch join |
| non-null `not_before` | refuses | **accepts — gap** |

The explicit nonempty branch rule remains worth adding directly even though current
request validation and join validation reject it transitively.

## Root-cause boundary

Available evidence supports these statements:

1. The API correctly failed closed on at least one contradictory scheduling fact.
2. The normal exact and bounded SBE 0.4.14 inspection builders emit all five facts
   coherently in provider-free production-shaped workspaces.
3. SBE v0.5 has two independent semantic-validation omissions that can produce the
   same API error if contradictory bytes reach the consumer.
4. No available raw inspection proves empty IDs, wrong reason, non-null timing, or
   another predicate was the retained incident's exact cause.

The sprint must therefore fix all explicit branch invariants while describing the
incident root cause as unresolved unless the exact rejected inspection is recovered.

## Provider-safety evidence

- Retained QA workspace access: none
- Provider create calls: 0
- Provider retrieval calls: 0
- Authorization/consumption changes: 0
- Native runtime changes in Slice 0: none
- API/database changes: none

## Slice 0 gate

PASS for reproduction and gap discovery. Pause for API review before freezing the
Slice 1 contract and diagnostic vocabulary.

