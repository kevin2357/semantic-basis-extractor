# API response — Slice 3 initial-pass runtime discovery

## Decision

The discovery is correct. **Do not fabricate six assembled-deck transitions.**
Approve the proposed stage-discriminated correction before any runtime builder
implementation.

Production's six parallel initial passes are per-pass authored-claim
materializations. They are not whole-subject deck mutations, and a later
assembled deck must not be retroactively represented as their output merely to
satisfy the current v1 shape.

## Adopted shape

Use a closed discriminated transition union:

1. `initial_pass` has exactly an `initial_pass_materialization` relation.
   It records the released pass identity, source-basis/input-workspace digest,
   exact accepted response-workspace identity/digest, and authored-claim-set
   digest, together with the existing exact action/binding/Response and
   acceptance facts. It has **no** `input_deck`, `candidate_deck`, or
   `output_deck` member.
2. `creative_retry`, `polish`, `critic`, and `candidate` retain the existing
   whole-deck transition relation and its materialization/adoption algebra.
3. Add one explicit assembly-owned `initial_assembly` bridge outside the
   decision sequence. It must bind the six ordered accepted initial-pass
   materializations to the first assembled whole-subject deck. A later
   whole-deck decision may use that deck as its input, and terminal selection
   may select it when there is no later adopted deck.

That explicit bridge is required; it prevents a hidden inference that the first
whole deck came from an arbitrary initial pass or a fabricated sequential chain.
It is not a seventh initial decision, a provider action, or a lifecycle event.

## Digest/artifact decision

Keep initial-pass source and authored-output digests **directly in the initial
pass materialization relation**. Do not add an initial-pass workspace or
claim-set artifact kind in this iteration.

Reasons:

- The canonical editorial packet needs exact provenance and lineage joins, not
  mandatory delivery of whole pass-workspace payloads.
- Existing artifact records are intentionally for independently useful full
  decks and exact joined provider responses. Treating every pass workspace as
  an artifact would add transport/partial-availability complexity without a
  defined editorial-review query need.
- A direct digest/identity is sufficient to bind the eventual runtime reader
  to the accepted workspace and authored claim set. If a future review need
  justifies pass-workspace delivery, it can introduce a separately versioned,
  explicitly optional artifact role rather than silently widening this packet.

Use domain-specific field names such as `source_basis_sha256`,
`accepted_workspace_sha256`, and `authored_claim_set_sha256`; avoid the generic
`input_deck`/`output_deck` names, which would invite exactly the false
whole-deck interpretation being corrected.

## Required coordinated updates

- Bump/version the affected closed decision, packet, projection, artifact
  manifest, and semantic-contract schemas together; retain strict rejection of
  an initial pass carrying the whole-deck transition form.
- Update native rule IDs/validator stages and the Alloy mapping where the
  current initial-pass deck topology is assumed.
- Replace the synthetic initial-pass deck fiction in both positive fixtures.
  Add an initial-assembly bridge and make post-initial deck transitions begin
  only from its assembled deck.
- Add rehashed negative cases for: an initial pass claiming a deck transition;
  missing/duplicate/reordered pass materialization; a bridge not bound to all
  six accepted pass outputs; a bridge whose assembled deck mismatches the first
  post-initial input; and terminal selection of an unreachable assembled deck.
- Preserve exact six initial passes, contiguous decision ordinals,
  action/binding/Response joins, result/receipt/checkpoint provenance, and all
  existing no-I/O/no-latest-result/no-authority fences.

## Boundary

This authorizes the contract correction and its provider-free fixture and
validator work only. It does not authorize a runtime builder, a live workspace
read, artifact expansion, Better Stack transport, release, or API lifecycle
change.
