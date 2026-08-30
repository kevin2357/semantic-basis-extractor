# Pre-sprint huddle — retry external-authority v2 dispatch handoff

## Initial assessment

The observed generic refusal is a successful safety fence, not by itself the
defect. SBE 0.4.30 refused a create-capable ordinary resume because the caller did
not provide the exact checkpoint-bound external-authority v2 request, grant, and
authorization documents. No new provider request was created.

The integration failure is that this safe refusal did not lead to a complete
handoff. Hellman was placed back into retry-wait while retaining the only worker
slot. Diffie instead failed strict lifecycle consumption because its
ordinary-resume evidence was incomplete. The two outcomes may share one missing
handoff, but they must be reconstructed independently rather than flattened into
one assumed cause.

The most likely desired sequence is:

1. reconcile any already provider-bound retry selected by SBE;
2. consume its completed result through the required native fan-in/local-work
   checkpoint;
3. inspect the new checkpoint;
4. obtain the exact public external-authority v2 request for the newly prepared
   providerless retry;
5. have API make or reuse its own spend-admission decision and persist a fresh
   request-bound v2 grant and ordinary authorization document;
6. invoke only the constrained v2 dispatcher; and
7. detach into retrieval-only custody after SBE durably records provider identity.

An API-side row described as `authorized` is not an SBE dispatch envelope. It may
prove that API admitted spend, but it cannot replace SBE's exact current-basis
request/grant join or authorize generic resume to create provider work.

## Why Slice 0 remains genuinely investigatory

The current evidence does not yet prove whether the missing boundary is entirely
an API routing/ingestion gap. The native inspection reportedly selected
`ordinary_resume` while the run also had one retained provider action and one
local dependency. Existing SBE invariants say retained provider custody outranks
new authority, while completed evidence may require bounded native fan-in before
the next paid-action inventory can be known. The retained Diffie and Hellman
checkpoints are therefore valuable for establishing:

- whether the provider-bound retry was pending, completed-but-unconsumed, or
  already consumed in each checkpoint;
- whether a valid v2 request was actually published for the second retry;
- whether API had only its own authorization row or also possessed the exact SBE
  request/grant documents;
- whether lifecycle branch fields were internally complete and valid; and
- why Diffie failed strict consumption while Hellman accepted the same general
  situation as retryable.

No conclusion should depend on the OpenAI dashboard. Provider completion is not
native truth until retrieved and durably reconciled through SBE.

## Working posture

- Keep the QA SBE worker suspended.
- Do not resume, reconcile, repair, deny, retire, delete, or recover either run.
- Permit narrowly bounded read-only R2 inspection when exact object coordinates
  are frozen first.
- Use exact object `HEAD` and `GET`; do not list the bucket or discover adjacent
  objects.
- Validate archive, path, snapshot, inventory, result, receipt, and journal joins
  before interpreting retained bytes.
- Keep provider reconciliation and provider creation as separate commands and
  authorities.
- Prefer existing v2 contracts if they already express a single ordinary retry;
  do not create a new schema merely because the consumer did not complete the
  existing handshake.
- Treat any unjoinable historical state as a closed refusal/review outcome, not a
  reason to manufacture a grant or reuse an earlier one.

## Initial concerns to resolve

1. Does the current public lifecycle surface always expose a fresh v2 request at
   the first checkpoint where the retry inventory is stable and providerless?
2. Does mixed completed custody plus prepared successor work select the correct
   bounded local/reconciliation sequence before authority?
3. Can API validate the exact single-action v2 request, grant, authorization
   document, and binding entirely from public artifacts?
4. Is the generic refusal sufficiently explicit about the next supported command
   for API to avoid both failure and slot-holding retry loops?
5. Are Diffie's “incomplete ordinary resume” and Hellman's repeated safe refusal
   two consumer mappings of one state, or evidence of different native
   checkpoints?

The sprint should answer these questions before changing runtime behavior.
