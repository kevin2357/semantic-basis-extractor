# Slice 2 — Reconciliation Checkpoint Qualification

Date: 2026-08-23
Status: complete; cross-route gate pending

## Proven sequence

The provider-free qualification now exercises this production-shaped sequence:

1. Six separately authorized initial actions create exactly six scripted provider
   identities and detach.
2. A not-due inspection and later due inspection share one exact v0.6 checkpoint
   basis.
3. SBE selects the bounded four-member due subset.
4. The real supported reconciliation operation retrieves those four completed
   responses and durably checkpoints provider evidence.
5. The resulting inspection has a different checkpoint-basis digest.
6. Deterministic local ingestion is checkpointed, a fresh worker retrieves the
   remaining two, and all six response artifacts become durable.
7. No provider identity is created twice and no provider identity is retrieved
   twice.

The receipt records both pre- and post-reconciliation basis hashes. Provider
availability is never represented as changing merely because time advanced; it
becomes native fact only through retrieval and checkpointing.

## Focused direct regressions

- Real three-action reconciliation changes the basis and records completed
  provider evidence.
- A second reconciliation against completed evidence makes zero retrieval calls.
- A fresh Python process reconstructs the exact post-reconciliation v0.6 bytes.
- A rehashed but reordered due subset is refused because it is not SBE's native
  selection.
- Existing backward-time, due-to-not-due, malformed-basis, request-join, and
  canonical-time refusals remain green.

## Authority conclusion

An API consumer may treat temporal evolution only within one basis digest.
Provider retrieval crosses into a new basis and must be ingested as a new native
checkpoint. A prior temporal decision cannot be rewritten to contain the newly
observed provider facts.

Repeated due observations remain evidence-only and idempotent. API lease/custody
still controls whether the supported run-level reconciliation command is invoked;
the API never chooses members or reconstructs the retrieval call.

## Safety

- Provider credentials/network: absent.
- Paid provider work: none.
- Retained QA workspaces: untouched.
- Scripted creates: six unique.
- Scripted retrievals: six unique in bounded four-plus-two waves.
