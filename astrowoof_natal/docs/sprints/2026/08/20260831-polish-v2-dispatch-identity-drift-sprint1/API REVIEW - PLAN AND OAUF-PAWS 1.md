# API review — plan and Oauf-paws 1

## Decision

**Approved to begin Slice 0.** The investigation-first ordering, protected-access
budget, provider-free posture, and separation from general checkpoint-inspector
product work are all correct. The active QA SBE worker remains suspended; this
review does not authorize recovery, provider work, or any retained-run mutation.

## API-side confirmations

- The API action/admission/request/grant chain supplied in `Background.md` is
  internally coherent: the durable action is `authorized`, its exact request is
  `07300bd27a5f61c592fc6fc7df1a7eee57bcd6bf9d333ca2b3b45a34e20b7fb2`, and the
  grant/member chain is bound to that request.
- No polish provider operation or dispatch receipt exists. The incident is
  therefore a pre-provider native v2 refusal, not a provider, settlement, or
  API spend-admission failure.
- API durable action state is not evidence that the native action was still
  providerless `PREPARED` and dispatchable under the writer. Slice 0/1 must
  preserve that distinction exactly.
- The raw trace export is available only at the local path declared in
  `Background.md`. It is non-authoritative and may contain unrelated large
  command-result records; use it to locate field producers and timing, never to
  select authority over checkpoint/API records.

## Required Slice 0 discipline

1. For each observed short hash, report the exact producing code field and
   document type (for example request, inspection, snapshot, inventory,
   binding, payload, or grant). Do not call a value a request identity until
   the canonical object and its digest rule establish that fact.
2. Keep three propositions separate in the source/trace map:
   (a) one immutable request object changed, (b) multiple lawful observations
   produced multiple request objects, and (c) the logs use incomparable digest
   labels. The trace alone proves none of those.
3. Include observation time, checkpoint/snapshot basis, ordered inventory, and
   state revision wherever current source permits one of them to influence a
   request or inspection identity. This is necessary to distinguish a real
   basis change from a time-only reinspection.
4. Treat the creative-retry ambiguity as a separately labelled possible
   contributing condition until the retained checkpoint establishes a native
   causal path to the polish action posture. It must not be used to explain the
   polish refusal by association alone.
5. Record any parser/validator gap as an input to the dedicated inspector
   sprint, but do not turn this forensic slice into a new public surface.

## Gate

At Oauf-paws 1, provide the source/trace identity map, the concrete retained
facts still needed, and the one-object `HEAD`/`GET` request for generation 11.
The existing Background coordinate packet is sufficient for that next review;
do not request credentials, signed URLs, bucket listings, or broader storage
access.
