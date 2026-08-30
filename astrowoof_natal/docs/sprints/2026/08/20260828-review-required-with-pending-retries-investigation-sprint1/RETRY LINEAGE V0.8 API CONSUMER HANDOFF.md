# Retry lineage v0.8 API consumer handoff

## Status

Slice 7 candidate public surface complete; API joint-adoption review pending.
This document does not authorize release, deployment, retained-run recovery, or
provider activity.

## Supported public surface

- Lifecycle root: `astrowoof.authoring_lifecycle_inspection.v0.8`.
- Retry inventory: `astrowoof.retry_lineage_inventory.v1`.
- Qualification receipt: `astrowoof.retry_lineage_qualification.v1`.
- Python readers and validators are exported from `astrowoof_natal_authoring`.
- Runtime inspection:
  `astrowoof-authoring-lifecycle --run-dir RUN inspect-retry-lineage
  --native-exclusive-access declared --observed-at CANONICAL_UTC`.
- Provider-free qualification: `astrowoof-retry-lineage-qa`.

The API must validate the complete v0.8 lifecycle document. It must not graft the
retry-lineage subdocument onto v0.7, infer missing joins, select due members, or
reconstruct actions from counts.

## Selected-command rules

1. A conflicted retry lineage never permits new provider dispatch.
2. If durable provider custody exists, SBE selects the bounded run-level
   `provider_reconciliation_cycle`. The conflict remains visible as secondary
   safety evidence; it does not suppress retrieval of already-created work.
3. After custody clears, the unresolved conflict selects `none` with
   `retain_for_review` and
   `retry_lineage_conflict_requires_review`.
4. The API maps that result to a nonterminal review/blocked posture. It must not
   publish delivery, release authority as if terminal, invoke generic resume, or
   create provider work.
5. Only an SBE-selected command may be invoked. The API never selects the action
   subset.

## Exact authority joins

Every retry member is joined to the checkpoint's complete native action inventory
by native run ID, route family, stage, pass, attempt, action ID, action state,
request digest, complete binding digest, mechanism, provider identity, and the
canonical pass-attempt pointer. Custodial members additionally join the exact
provider-custody record. Missing, fabricated, duplicated, reordered, or mismatched
members fail validation.

The semantic attempt key deliberately excludes request/binding identity. Those
values are evidence about one attempt; changing them cannot mint a second logical
attempt and evade conflict detection.

## Runtime and replay behavior

- First retry preparation persists the attempt/action/binding/request/payload
  relationship as one durable unit.
- Pre-authorization re-entry reuses that relationship.
- Completed predecessors contribute retry feedback; the incomplete current
  attempt does not erase or replace it.
- Whole-ledger lineage validation precedes forward provider dispatch.
- Provider identity remains immediate durable evidence and subsequent result
  observation remains retrieval-only.
- Same workspace basis and observation time produce exact replay.
- Changed native custody evidence creates a successor basis; it is not a temporal
  rewrite of the predecessor.

## Compatibility and applicability

- v0.7 remains an immutable historical contract. Consumers that require the new
  safety evidence must fail closed on v0.7 rather than silently reinterpret it.
- Exact interactive is the primary corrected runtime route.
- Bounded interactive shares and qualifies the same lineage/custody safety shape
  without changing its route-specific bindings.
- Exact Batch and bounded Batch are deliberately outside this correction. No
  Batch topology support may be inferred from the interactive qualification.
- Historical contradictory workspaces are evidence. This contract does not
  authorize repairing them by selecting a preferred row.

## Qualification and privacy boundary

`astrowoof-retry-lineage-qa` is qualification-only. It accepts no run directory,
provider credentials, provider endpoint, request payload, authorization, or
production input. It performs zero network/provider/spend operations and writes
only an optional receipt outside native workspaces.

The receipt contains bounded route/status/count evidence. It contains no logical
workspace paths, prompts, payloads, bindings, provider configuration, credentials,
or subject prose.

## API adoption evidence required

Before pinning a release, API must prove from the installed wheel that it:

- validates lifecycle v0.8 and rejects malformed joins;
- preserves SBE-selected reconciliation custody despite lineage conflict;
- maps post-custody conflict to a nonterminal, non-dispatching review posture;
- invokes only the run-level selected command and never reconstructs members;
- preserves exact request/grant/action/binding authority joins;
- produces no duplicate create, no terminalization, and no capacity-release
  inference from contradictory native evidence; and
- consumes the packaged qualification receipt and fixture manifest exactly.

Release preparation remains blocked until that joint evidence is reviewed.
