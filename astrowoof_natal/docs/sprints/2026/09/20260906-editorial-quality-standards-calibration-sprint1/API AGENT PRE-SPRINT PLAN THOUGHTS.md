# API agent pre-sprint plan thoughts — routine editorial corpus companion

## Overall assessment

The companion relationship is now well drawn. This calibration sprint should
remain free to reconstruct and judge the full private evidence needed to decide
whether editorial policy is sound. The API companion should separately build a
small, rotating, ordinary-terminal diagnostic corpus. Neither should distort
the other:

- a Better Stack row must not become an editorial, queue, custody, settlement,
  provider, recovery, or replay authority; and
- a routine packet byte ceiling must not cause this calibration effort to omit
  private evidence that a real reviewer needs to reach a judgment.

The added **Relationship to the joint retention companion** section and the
Slice 3 size-feedback loop accurately preserve that distinction. I approve the
calibration plan to continue through its existing evidence/replay work under
its documented pause points.

## What should feed the joint packet decision

The calibration work is uniquely positioned to supply the right empirical
inputs before the routine schema is frozen. Please return these from Slice 3 in
a compact, sanitized contract note rather than silently treating the private
review packet as `editorial_review_packet.v1`:

1. canonical UTF-8 size for a complete ordered lineage with finding-local
   context, for both an accepted control and an editorial-rejection case;
2. incremental canonical size of including the complete selected deck;
3. what minimum selected-deck material allowed a reviewer to assess a finding
   in context, including the accepted-control case where no rejected field is
   naturally highlighted;
4. which fields were actually judgment-relevant versus provenance-only; and
5. evidence that is indispensable to private calibration but inappropriate for
   routine Better Stack capture.

The existing four private lineage packet sizes are useful feasibility evidence,
but they do not alone decide whether complete decks belong in the rotating
corpus. Kevin will make that content/ceiling decision at the joint contract
pause.

## Native/API boundary to retain

When the companion implementation starts, SBE should own a pure,
reader-validated native packet builder. It should consume already available
ordinary-terminal evidence and perform no provider, R2, Better Stack, API, or
generic-result-discovery I/O. It must return canonical native packet bytes,
packet digest/ID, and typed construction outcomes.

API will add API-owned correlations and observation metadata only in a transport
envelope after its authoritative terminal persistence/sealing succeeds. API must
not infer native meaning or mutate the native packet bytes/digest. The normal
routine hook must use the exact sealed result produced by that terminal
invocation, never a “latest result” lookup.

## Specific contract fences worth carrying forward

- Freeze exact eligible ordinary-live-exact result predicates, including
  negative near-neighbors. Status labels alone must never grant capture.
- Make a full packet all-or-none. Oversize, incomplete, excluded, contradictory,
  or unsupported native evidence should yield a small typed capture-status
  observation, not a partial packet.
- Keep raw prompts, model reasoning, full provider envelopes, credentials,
  local workspace paths, and unrelated workspace contents out of the routine
  packet.
- Require deterministic replay: the same exact sealed native result must yield
  byte-stable canonical packet bytes, digest, and packet ID. Wall-clock API or
  Better Stack times belong outside the canonical native packet.
- Preserve an ordered decision lineage: all six initial pass decisions,
  present creative retries and polish attempts, final validation/lint,
  selected-deck disposition, applicable action/binding/Response joins,
  candidate/report hashes, and exact finding details necessary to understand a
  decision.

## Scope recommendation

No SBE runtime/schema implementation should begin from this calibration-plan
review alone. The next joint Slice 0 should first measure the two packet content
shapes, inventory exact eligibility predicates, and return to Kevin for the
complete-deck versus finding-local-context and byte-ceiling decision. That
sequence is proportionate: ordinary editorial terminal paths are stable enough
for a harmless future hook, while every exotic lifecycle route remains
intentionally out of scope.
