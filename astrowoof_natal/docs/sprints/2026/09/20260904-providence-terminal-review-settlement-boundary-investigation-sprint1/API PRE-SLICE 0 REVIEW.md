# API pre-Slice 0 review

## Decision

Approved for SBE Slice 0 provenance reconstruction and the provider-free
cross-repository fixture design. No runtime implementation, protected
checkpoint access, provider action, retained-run mutation, or release is
approved by this review.

## What the current evidence establishes

The sanitized worker trace, the released SBE public terminal-review contract,
and API's current validators/disposition mapper are enough to establish the
**leading architectural finding**:

- a `providerless_denial_required` result is a public, structurally valid
  terminal-review finality vocabulary value;
- the public derivation is consistent with seven `REPORTED` actions plus the
  one providerless `PREPARED` polish action described in the trace; and
- API rederives that vocabulary in transition validation but its later
  disposition mapper handles only `final` and the retained-provider
  reconciliation case. The observed refusal is therefore source-consistent
  with a known unimplemented API settlement boundary.

That is sufficient to begin a provider-free fixture that represents the public
shape and to complete Slice 0's causal/source provenance.

## What the current evidence does *not* establish

It does not independently validate Providence's complete sealed action rows,
binding and inventory digests, receipt/journal range, projection references,
or native cause code. Therefore it is not sufficient to declare the exact
retained artifact valid or to implement/operate a live settlement solely from
the logs.

First prefer an API-owned exact-result/receipt export. If unavailable, a
separate owner-authorized immutable checkpoint packet and one bounded HEAD/GET
remain appropriate for Slice 1. Do not download a checkpoint merely to repeat
the already-proven architectural diagnosis.

## API ownership of the proposed settlement

The proposed sequence is directionally correct with these frozen constraints:

1. The precursor `review_required` result is evidence, **not** terminal
   closeout authority. API must validate and durably bind its exact result,
   receipt, checkpoint, action inventory, and denial IDs before attempting
   any successor path.
2. API owns the durable settlement-intent/idempotency record, job posture,
   lease/capacity policy, and final terminalization. The native package must
   not reconstruct API leases, allocations, or database state.
3. The only permitted native settlement is an exact providerless-denial
   operation over the ordered named denial inventory (for Providence, the
   prepared polish action). It performs zero provider create, retrieval, or
   transport I/O. No inference from a finality label may add, remove, or
   substitute an action.
4. That native operation must publish a cryptographically joined successor.
   API must validate and ingest that successor, then reinspect. Only a
   successor whose sealed custody state is genuinely `final` may use ordinary
   terminal closeout.
5. Replay after any interruption must be inert: no second denial, divergent
   successor, provider I/O, or premature resource cleanup.

The phrase “denial -> successor ingestion -> terminal closeout” matches API
ownership only with those predecessor binding and idempotency guarantees.

## Additional request for Slice 0

Please make the provenance table distinguish:

- public semantic sufficiency for the gap diagnosis;
- exact-artifact validation sufficiency for a real Providence settlement; and
- fixture sufficiency for a provider-free API implementation gate.

This avoids treating logs as either weaker or stronger than they are.
