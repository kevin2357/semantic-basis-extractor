# Slice 3 Provider-Operation Observation Integration

Date: 2026-08-17
Status: complete; awaiting Kevin review

## Outcome

Every supported paid-operation lifecycle now projects durable, append-only native
evidence from SBE's authoritative spend ledger. The integration covers exact
interactive Responses, exact Batch rounds, and bounded interactive Responses across
all five paid stages. It performs no provider submission and does not transfer
account-wide billing authority from the API.

## Implemented boundary

`persist_state()` first writes native run, public, and authorization-request state.
It then synchronizes all newly visible paid-action facts into the native transition
journal. An enclosing spend or command boundary subsequently publishes the complete
workspace snapshot. Thus a journal fact never precedes its authoritative ledger
fact.

If execution is interrupted after ledger persistence but before journal publication,
the next synchronization deterministically reconstructs the missing observations.
Exact semantic observations are emitted once even when callbacks or persistence are
replayed with a newer state revision or observation timestamp.

## Observation coverage

- action prepared, authorized, consumed, and providerlessly denied;
- provider submission started and durable identity recorded;
- provider pending retrieval;
- provider completed, failed, cancelled, or expired;
- provider usage reported or unavailable with billing reconciliation pending;
- identity-less ambiguous submission; and
- refusal of conflicting provider identity evidence.

Every provider observation is bound to the action ID, stage, request/profile hashes,
maximum output, commitment, versioned price book, route family, mechanism, and native
operation reference. The journal never invents a provider ID before it exists.

## Safety and compatibility

- Public mutation retains the established native cross-process writer lock.
- Internal ledger projection uses a journal publication lock so it cannot recursively
  acquire the spend lock already held by consumption or reconciliation.
- Unsupported legacy run schemas do not acquire a partial journal contract.
- Bounded Batch remains unsupported and fail-closed.
- Missing provider usage remains explicitly unsettled; it is not converted to a
  reported zero-dollar cost.
- Existing execution events remain non-authoritative.

## Verification

- Focused native transition suite: 14 passed in 1.412 seconds.
- Broad spend/provider-capacity/bounded-provider/semantic-closure gate: 145 passed in
  182.359 seconds.
- The matrix includes every paid stage, Response and Batch mechanisms, bounded route,
  exact replay, ambiguity, unavailable usage, public-writer contention, and injected
  journal-publication interruption/recovery.
- Live provider operations: 0.
- Paid spend: `$0`.

## Deferred to Slice 4

Invocation-level terminal/native transitions and immutable execution-result
publication remain intentionally outside this slice.
