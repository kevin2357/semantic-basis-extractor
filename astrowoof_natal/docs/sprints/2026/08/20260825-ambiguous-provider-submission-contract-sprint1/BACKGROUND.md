# Ambiguous Provider Submission Contract — Sprint 1 Background

## Trigger

Fresh QA runs Vafle-hund and Zultan of Berliner Borking exercised the current
external-authority v2 continuation after their initial authoring waves had been
reconciled. API granted an exact ordinary-authoring action. SBE invoked the v2
execution bridge and returned `ambiguous_submission` rather than
`detached_provider_pending`.

The public result is schema-valid, but API currently accepts only detached work
or exact replay after a grant. It consequently recasts this meaningful native
outcome as generic artifact-integrity failure. The contract lacks the facts API
needs to preserve ambiguity safely.

## Current code shape to assess

`external_authority_v2_execution.dispatch_external_authority_v2_intent()`
records create-entered state and catches failures from `create(action)` broadly.
The `create` adapter may itself perform deterministic payload/preflight work
before an actual provider request. Thus the broad catch can collapse two
materially different cases:

1. **Proven pre-provider failure** — no provider I/O occurred; safe refusal
   semantics may apply.
2. **Create-entered unknown** — provider invocation may have happened; duplicate
   creation must be prohibited until custody is resolved.

The sprint must verify the exact implementation rather than assume this outline
is complete.

## Required contract properties

- Classify the outcome through a closed, public, versioned vocabulary.
- Preserve a safe, non-secret reason/classification and sealed native evidence.
- Keep original binding, action, run, revision, and checkpoint identities
  joinable.
- Distinguish pre-provider refusal from ambiguous provider submission before API
  sees the result.
- Permit no fresh provider create from an ambiguous action.
- Keep provider I/O outside the single writer while retaining serialized native
  state transitions.
- Never use logs as authority, although logs should make the selection visible.

## Non-goals

- No recovery or retry of Vafle-hund/Zultan in this sprint.
- No redesign of spend policy, batch transport, or initial-wave fanout.
- No payload/protected provenance or provider secrets in public artifacts.

