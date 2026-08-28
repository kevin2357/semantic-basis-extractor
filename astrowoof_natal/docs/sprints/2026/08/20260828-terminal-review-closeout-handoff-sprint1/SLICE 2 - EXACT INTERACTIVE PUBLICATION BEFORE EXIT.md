# Slice 2 — Exact Interactive Publication Before Exit

## Decision

Exact-Natal interactive ordinary authoring now publishes a sealed terminal-review
handoff before exposing exit code 2. This slice deliberately does not change exact
Batch or either bounded route.

## Runtime boundary

After an authoring or finalization spend boundary persists native state and its
snapshot, the exact-interactive runner performs a fresh v0.7 lifecycle inspection.
If native truth selects `command=none` with
`capacity_disposition=retain_for_review`, the runner:

1. appends a review-required invocation/journal transition;
2. writes the immutable `astrowoof.native_execution_result.v0.2` result;
3. writes and validates the complete workspace snapshot;
4. seals the canonical `astrowoof.native_publication_receipt.v0.1` receipt;
5. emits the non-authoritative publication event;
6. writes one closed `astrowoof.terminal_review_command_result.v0.1` envelope
   carrying the exact invocation, result, and receipt identities/digests; and
7. exits 2.

The ordinary final-QA review path uses the same publication and command-result
surface. The command never asks a consumer to discover “latest” and infer that it
belongs to the invocation it launched.

## Consumer join

The command-result envelope is only an identity transport. API validates it
against the exact sealed v0.2 result and canonical receipt, then joins every
action row to API-owned immutable action/authorization evidence using the full
binding. A compact `binding_sha256` is not independent spend authority.

When custody finality is not `final`, the outer posture is review-required with
retained custody. The only permissible native follow-up is the exact listed
reconciliation or providerless-denial operation. The result never permits a new
provider create and never claims API capacity, reservation, or billing release.

## Corrections found during integration

- Lifecycle observation time is canonical UTC at whole-second precision.
- Journal outcome/cause and sealed v0.2 result outcome/cause are identical.
- Public command-result validation includes an exact publication join, not merely
  closed standalone field validation.

## Scope and gate

Provider-free focused and adjacent tests passed: 63. Provider creates, retrievals,
network calls, spend, and retained-QA access were all zero. Slice 3 remains blocked
on API review of this exact-interactive runtime result and custody mapping.
