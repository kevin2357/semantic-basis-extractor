# Slice 3 — provider-free sequential-v2 reproduction

## Result

The focused provider-free witness reproduces the general defect through the
real v2 intent-commit and provider-dispatch functions. It is not polish-specific.

1. A first ordinary v2 action set is inspected, granted, committed, and
   dispatched through the production executor.
2. The scripted transport returns one durable provider identity per ordered
   member; the command detaches as provider-pending.
3. The fixture then materializes the same durable post-reconciliation truth
   observed in retained generation 11: every predecessor action is `REPORTED`,
   has completed reconciliation/reporting evidence, and a fresh independent
   polish action is providerless `PREPARED` work.
4. The public temporal inspector exports a coherent fresh singleton v2 request
   for that successor, and an exact grant/document set is built against it.
5. Intent commit refuses with `action_state_or_custody_mismatch` because the
   predecessor singleton still occupies the live slot.
6. Direct dispatch of the successor identities refuses with
   `authorization_mismatch`.
7. The provider-create counter remains exactly the first request's inventory;
   no successor create occurs.

The fixture deliberately stops short of implementing a test-only retirement
algorithm and then presenting it as runtime evidence. The accepted correction
will be proved after the production retirement boundary exists.

## Existing safety coverage composed with the witness

The focused run also includes the existing v2 intent-fence suite. Together the
18 passing tests cover:

- atomic request/grant/inventory/authorization/intent persistence;
- identity durability before the next ordered create;
- exact replay with no duplicate create;
- interruption after a durable identity;
- call-entry ambiguity and non-replayability;
- safely resumable failure before call entry;
- malformed/conflicting provider identity refusal;
- partial member progression; and
- the new terminal-predecessor/fresh-successor stale-slot counterexample.

Pending, partial, ambiguous, conflicting, unjoinable, or malformed evidence
must remain live/refused/reviewed by the correction. Only the exact complete
terminal join may create a retirement record and release the singleton slot.

## Correction boundary proposed for Slice 4

Normal runtime behavior:

- At the writer-fenced checkpoint that first records the complete terminal
  action/reporting/reconciliation join, validate the live intent against that
  inventory.
- Append one immutable retired-intent record and remove the singleton live
  intent in that same checkpoint.
- Preserve request/grant/action/provider identities and a terminal-evidence
  digest sufficient for exact replay.
- Never use the arrival of a successor as the normal retirement trigger.

Compatibility behavior for existing stranded workspaces may retire a prior
intent at successor admission only after the identical exact terminal proof.
This is a repair path, not the lifecycle contract for newly written work.

## Scope and safety

- Provider calls: scripted only.
- External network/provider calls: zero.
- Retained Delerium execution or mutation: zero.
- Additional R2 operations: zero.
- Runtime source mutation: zero.

## Oauf-paws 4

Pause before choosing the exact retired-intent record shape, replay lookup, and
runtime integration sites.
