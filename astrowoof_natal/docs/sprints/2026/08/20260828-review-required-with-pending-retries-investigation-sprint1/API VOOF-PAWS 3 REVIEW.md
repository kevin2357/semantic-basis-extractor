# API Voof-paws 3 review — retry lineage and custody correction

## Decision

**Approved in direction: proceed with the proposed correction as an SBE-led
contract/runtime sprint after incorporating the conditions below.** The API will
plan its companion ingestion/queue-mapping work from the frozen Slice 3 fixtures
and public v0.8 contract, but must not infer equivalent facts from retained v0.7
inspection documents.

Slice 2 establishes two general, provider-free reproduced defects: re-entry can
prepare divergent actions for one logical pass attempt, and post-fan-in can mask
retained provider custody with a providerless-authority review projection. The
historical QA issue vocabulary is not causal.

## Required contract refinement

### Keep attempt identity separate from binding identity

The canonical **attempt key** must exclude the mutable/detectable value it is
meant to protect. Define it from the immutable logical attempt coordinates, for
example:

`native_run_id + route_family + stage + pass_id + attempt_number`

Treat the action ID, exact request/binding digest, model/service mechanism, and
persisted request artifact as the immutable evidence *attached to that one key*.
Then a second action or a changed request digest for the same attempt key is a
closed lineage contradiction. If the request binding is part of the uniqueness
key, a changed binding becomes a different identity and the primary defect is
not detectable.

The final contract should define the exact pass/route spelling and a canonical
serialization/digest for the attempt key rather than leaving either consumer to
compose it ad hoc.

### Make the mixed-custody result explicit and internally consistent

For a workspace with durable provider custody plus a separate providerless
lineage conflict, v0.8 must state all of the following together:

- selected command is `provider_reconciliation_cycle`;
- its ordered due action IDs name exactly the provider-bound reconciliation
  members;
- provider-custody count/identity is nonzero and agrees with those members;
- the providerless contradiction is separately exposed as a closed safety fact;
- no provider create/ordinary/external-authority dispatch is allowed for the
  conflicted lineage; and
- after custody settles, the only successor is the typed non-dispatching
  review/refusal path unless an exact, unconflicted action pointer/binding is
  established.

`none / retain_for_review` together with nonzero provider custody must be an
invalid v0.8 document, not a valid review disposition. Preserve v0.7 as a
historical reader boundary and make the API reject that contradictory v0.7
combination rather than silently treating it as terminal.

### Reconciliation remains a narrow exception to fail-closed progression

Slice 4's fail-closed rule and Slice 5's retrieval-only reconciliation need an
explicit relationship: a lineage conflict blocks *new authorization consumption
and provider create*, but it must not block retrieval/reconciliation of an exact
already-durable provider identity. The preflight needs a typed distinction
between `no-forward-dispatch` and `reconciliation-permitted`; otherwise a broad
lineage refusal could strand the very provider result that makes resolution safe.

## Runtime/fixture conditions

- First preparation must persist the attempt key, chosen action ID, binding
  digest, and exact request-artifact identity atomically under the native writer
  boundary. Re-entry validates and reuses those facts; it does not regenerate
  feedback or request bytes.
- Completed-predecessor selection must be specified by attempt number/state, not
  list position. The incomplete current attempt is never evidence that prior
  rejected attempts lack feedback.
- Whole-ledger validation must run before any forward provider create, including
  after process restart. It must also validate the pass attempt's action pointer
  against the unique attempt lineage.
- Regression coverage should include the exact ``prepared -> authorized ->
  restart -> re-entry`` boundary that produced the incident, plus retained
  provider identity + conflicting providerless authority. Both generic and
  historical QA rejection codes are appropriate only as input modalities.
- v0.8 examples should include the API-visible fields necessary to distinguish
  normal providerless review from a contradiction that still has provider
  custody. API does not need private request bodies, prompts, or workspace
  internals.

## API companion boundary

The API will:

1. validate the closed v0.8 document and its cross-field custody constraints;
2. invoke only the SBE-selected exact command;
3. preserve/reject an impossible review-plus-provider-custody projection before
   queue failure or capacity release; and
4. never choose reconciliation members, rebuild retry feedback, repair a native
   action pointer, or consume a conflicting authorization.

This is sufficient to begin Slice 3 contract work. Pause at Voof-paws 4 before
runtime mutation so the API can review the actual v0.8 schemas, fixtures, reason
vocabulary, replay semantics, and compatibility behavior.
