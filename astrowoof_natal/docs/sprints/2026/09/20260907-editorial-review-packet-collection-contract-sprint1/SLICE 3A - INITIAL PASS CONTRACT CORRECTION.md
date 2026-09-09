# Slice 3A — Initial-pass contract correction

## Outcome

The executable editorial-review contract now represents the six initial passes
as parallel, stage-specific materializations rather than fictitious whole-deck
transitions. A separate assembly-owned bridge joins exactly those six accepted
initial-pass decisions to the first assembled whole deck consumed by the first
post-initial decision.

This is a contract, fixture, validator, and design-model correction only. The
runtime packet builder remains unimplemented pending joint review.

## Closed v2 shape

- `editorial_review_decision.v2` is a discriminated union:
  - `initial_pass_materialization` records released-pass identity, source-basis
    digest, accepted response-workspace identity/digest, authored-claim-set
    digest, and the existing exact action/binding/provider-response evidence;
  - `whole_deck_transition` retains the input/candidate/output deck relation for
    creative retry, polish, critic, and candidate decisions.
- `editorial_review_packet.v2` contains one `initial_assembly` bridge whose six
  unique decision IDs must equal the packet's complete initial-pass population.
- The bridge output is the exact input deck of the first post-initial decision.
- Projection and transport resources advance to v2 so consumers cannot silently
  interpret the corrected decision/packet shape through v1 readers.
- The semantic contract advances to v2 and owns the new materialization,
  assembly, and discriminated-transition rules. Unchanged atomic artifact,
  finding, validation, capture-status, fixture-wrapper, and qualification
  schemas remain at v1.

## Negative evidence

Five rehashed mutations supplement the original 24:

1. an initial pass falsely claims a whole-deck transition;
2. two passes reuse one materialization identity;
3. a decision and transition disagree on released-pass identity;
4. the assembly bridge omits one accepted pass; and
5. the assembly output disagrees with the first post-initial input deck.

Each is rejected by the public validator after recomputing affected digests.

## Qualification

- Focused executable-contract suite: 23 passed, 1 expected optional-schema skip.
- Alloy v2 model: inhabited two-packet world is SAT.
- Alloy assertions for response uniqueness, selected-deck reachability, and
  projection packet ownership are UNSAT (no bounded counterexample).
- Provider/network/R2/API/database/subprocess/workspace operations: zero.

## Review boundary

Joint review must approve this v2 correction before Slice 3 may implement the
ordinary-live-exact runtime builder.
