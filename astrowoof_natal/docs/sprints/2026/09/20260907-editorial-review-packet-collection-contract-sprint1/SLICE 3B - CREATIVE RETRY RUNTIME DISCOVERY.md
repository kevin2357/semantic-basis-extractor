# Slice 3B — Creative-retry runtime discovery

Status: paused before runtime implementation for one narrow joint contract
correction.

## Outcome first

Slice 3A correctly removed fictional whole-deck transitions from the six first
attempts, but the approved v2 union still assigns `whole_deck_transition` to
`creative_retry`. Production creative retries also occur inside one released
pass workspace before subject assembly. They therefore have neither a whole
deck input nor a whole deck candidate/output at that point.

The runtime builder cannot honestly populate the current creative-retry branch.
Implementation stopped before inventing deck evidence.

## Production evidence

- `closure.run_authoring_pass` creates every attempt's response workspace at
  `passes/<pass_id>/attempt-<n>/response/<pass_id>` (lines 4553 onward).
- The same per-pass acceptance operation evaluates first attempts and retries
  (`run_pass_acceptance`, line 4626).
- An accepted attempt is copied into `passes/<pass_id>/accepted` (line 4636).
- `assemble_subject` refuses to assemble until all six pass records are accepted
  (lines 5424–5438), then performs the first whole-subject `assemble` operation
  (line 5462).

Consequently, attempt 2/3 for a pass is a new candidate materialization for that
same pass, selected using predecessor QA feedback. It is not a mutation of an
assembled deck.

## Recommended correction

Extend the stage-discriminated decision union with a
`pass_retry_materialization` relation for `creative_retry`. It should bind:

- exact pass/released-pass identity and retry attempt;
- predecessor attempt identity plus its acceptance/QA report digest;
- source or predecessor workspace digest used to construct the retry request;
- candidate response-workspace identity/digest and authored-claim-set digest;
- whether that candidate became the pass's accepted workspace;
- exact paid action, binding, request, and provider response evidence.

The single `initial_assembly` bridge should continue to bind the six finally
accepted pass decisions—whether each winner was attempt 1, 2, or 3—to the first
assembled whole deck. It must not be hard-wired to the first six chronological
decisions.

Only post-assembly optional stages (`polish`, `critic`, and `candidate`) should
retain `whole_deck_transition`.

## Required fixture implications

At least one positive fixture should include a rejected initial attempt and an
accepted creative retry so the assembly bridge demonstrably selects the winning
decision rather than attempt 1 by position. Mutations should reject:

1. a retry masquerading as a whole-deck transition;
2. missing or mismatched predecessor QA evidence;
3. a retry candidate that falsely claims acceptance;
4. assembly membership pointing at a superseded attempt; and
5. duplicate accepted winners for one pass.

## Boundary retained

This is another contract-shape correction, not lifecycle or provider behavior.
No runtime builder, provider/network/R2/API/database operation, workspace
mutation, installed-wheel work, or release work occurred.
