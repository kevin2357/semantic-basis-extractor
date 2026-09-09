# API response — Slice 3B creative-retry runtime discovery

## Decision

**Approved with one shared-materialization refinement.** Creative retries are
pre-assembly pass attempts, not whole-deck transitions. Do not fabricate a
deck input, candidate, or output for them.

The assembly bridge must select exactly one finally accepted winner for each of
the six released passes. That winner may be the initial attempt or a creative
retry; it must never be inferred from chronological position.

## Adopted relation model

Use one shared closed pass-attempt materialization vocabulary for the common
facts, with stage-specific discriminators or subforms:

- `initial_pass_materialization`: the first attempt for one released pass;
- `pass_retry_materialization`: a later attempt for that same pass.

Both forms carry the released-pass identity, attempt identity/number,
source-basis or source-workspace digest, candidate response-workspace
identity/digest, authored-claim-set digest, acceptance outcome, and exact
action/binding/request-identity-or-digest/provider-response evidence. Raw
provider request bodies remain forbidden.

The retry form additionally requires its exact predecessor decision/attempt
identity and predecessor acceptance/QA-report digest. It must prove that the
retry is a successor for the same released pass, not merely an unrelated
materialization with a familiar-looking pass ID.

## Essential correction to the v2 initial form

The current initial form's unconditional `accepted_workspace` fields cannot
truthfully describe a rejected first attempt. Replace that with candidate
response-workspace facts for every pass attempt. A separate accepted-workspace
identity/digest is permitted **only** when the attempt was accepted, and must
match the bridge's winner for that released pass. A rejected attempt must carry
its real candidate/QA evidence without an invented accepted workspace.

This makes an ordinary “attempt 1 rejected, retry accepted” lineage representable
without hiding the rejection or fabricating pass acceptance.

## Revised bridge requirements

Rename the bridge membership from the now-misleading
`accepted_initial_pass_decision_ids` to a pass-winner form, for example an
ordered `accepted_pass_winners` list. Each member binds:

- one released-pass identity;
- its one winning decision ID; and
- the accepted workspace/claim-set identities carried by that winning attempt.

Validation must require exactly six unique released-pass identities; exactly one
accepted winner for each; no rejected/superseded decision; and an exact match to
the complete pre-assembly pass-attempt population. The bridge output remains
the first whole deck and must equal the first post-assembly optional-stage
input. Only `polish`, `critic`, and `candidate` retain
`whole_deck_transition` in the current ordinary live-exact contract.

## Required fixture and mutation updates

- Add a positive fixture with one rejected initial attempt and an accepted retry
  for the same pass; have the assembly bridge select the retry.
- Prove a retry cannot carry a whole-deck transition.
- Reject missing/mismatched predecessor QA evidence, a retry accepting the
  wrong pass, a false accepted workspace, duplicate winners, a superseded
  attempt in the bridge, and a bridge missing one pass.
- Update schema versions, semantic rules/validator coverage, projections,
  summaries, fixture bytes, qualification receipt, and the optional Alloy model
  together. Preserve explicit v2-reader refusal rather than silently widening
  the old meaning.

## Boundary

This authorizes only the coordinated contract/fixture/validator correction.
The runtime builder remains paused until that correction receives its own
provider-free evidence review. No live workspace access, provider work,
R2/API/network/database activity, Better Stack transport, release, or
lifecycle change is authorized.
