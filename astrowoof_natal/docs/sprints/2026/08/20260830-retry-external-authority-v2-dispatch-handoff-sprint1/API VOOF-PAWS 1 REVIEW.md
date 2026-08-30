# API Voof-paws 1 review — Slice 0 causal classification

## Disposition

Approved: the leading correction class is **API terminal-result ingestion and
subsequent scheduling/routing**, not an SBE external-authority v2 schema or
native-dispatch change.

The retained checkpoint inspection is appropriately bounded and its evidence
chain is sufficient for Hellman. Diffie remains unresolved rather than being
forced into the same causal explanation.

## Independent API persistence corroboration

Read-only PostgreSQL confirms the decisive Hellman omission:

- API has **no** `sbe_native_execution_receipts` row for sealed native result
  `nres_1087eba75d3c29aba23193d5`.
- API has **no** lifecycle-closeout record and **no** providerless-denial batch
  for Hellman's run.
- The latest API-persisted SBE receipts are earlier `provider_reconciliation`
  results through state revision 63; they predate the archive-proven terminal
  review result/receipt at the active snapshot/state revision 67.

Thus API scheduled lifecycle work without first consuming the immutable,
snapshot-bound review-required result that instructed it to retain/reconcile the
provider-bound retry and deny the providerless successor. The later generic
dispatch refusal was correctly safe, but downstream of that missed ingestion.

## Required API correction qualities

The API companion work must:

1. give a sealed native result/receipt precedence over follow-on lifecycle
   scheduling for the same checkpoint/snapshot;
2. validate the full public result/receipt/journal/snapshot join before acting;
3. map `review_required / local_work_progress_contradiction` through the
   released terminal-review handoff, including the separate reconciliation and
   providerless-denial inventories;
4. never mint a v2 provider-create grant for the denied successor;
5. release capacity or persist the explicit review/retention posture rather than
   loop a nonmutating generic refusal while retaining a slot; and
6. reject missing, stale, conflicting, or unjoinable terminal evidence closed.

Provider-free API tests should reproduce the exact ordering hazard: a sealed
terminal review result coexists with a still-nonterminal lifecycle projection.
The result must win.

## Diffie boundary

Do not expand the SBE contract merely to explain Diffie. Its active archive
predates the API strict-consumer failure and proves only a coherent
provider-pending/not-due state. The API sprint should separately find the exact
rejected inspection/validation path or represent that historical evidence as
unavailable. A synthetic strict-consumer contradiction test is useful, but must
not claim it is a retained Diffie reproduction.

## Next step

SBE may complete Slice 0 and hold this sprint at the causal-review gate. No SBE
runtime/schema implementation or release is presently indicated by these facts.
The API companion sprint should be replanned around the terminal-result-first
consumer correction and then tested against the public SBE fixture/contract.
