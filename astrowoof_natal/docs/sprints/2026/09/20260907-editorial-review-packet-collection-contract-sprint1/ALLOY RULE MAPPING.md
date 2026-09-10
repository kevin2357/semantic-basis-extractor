# Alloy rule mapping — Slice 1δ.0

Status: feasibility mapping, not the final semantic manifest. Rule IDs are
proposed stable identifiers and must remain one-to-one across adopted prose,
Alloy, the future Python validator, and fixture/mutation tests.

## Post-sprint maintenance status — 2026-09-10

This file preserves the Slice 1δ feasibility and counterexample-campaign
mapping. It is useful design lineage, but it is not a complete map of the
released editorial-review v5 contract and MUST NOT be treated as current
executable authority.

The current enforcement hierarchy is:

1. approved prose defines the intended contract;
2. the packaged semantic manifest enumerates the released rule IDs and their
   validator/test ownership;
3. schemas, the Python validator, positive fixtures, rehashed mutations, and
   consumer tests enforce the contract; and
4. Alloy supplies optional bounded relational evidence for the subset modeled.

Future editorial-review changes follow the mandatory impact-assessment process
in the
[Native Worker Change Playbook](../../../../post_extraction_authoring/Native%20Worker%20Change%20Playbook.md#assess-relational-contract-and-alloy-impact).
That assessment prevents silent model drift without turning Alloy into a
production dependency, CI requirement, or universal release gate.

## Retained model lineage

- `editorial_review_counterexamples_v1.als` is the model used by the stable
  `alloy-counterexample-receipt.v1.json` campaign. Its recorded results and
  exact finite scope remain historical evidence.
- `editorial_review_contract_v3.als` is the later design model updated after
  runtime discovery showed that initial attempts and creative retries are
  pre-assembly pass materializations rather than whole-deck transitions.
- The v3 model adds eighteen decisions across two packets, an explicit creative
  retry and predecessor relation, six accepted pass winners per assembly, and
  post-assembly whole-deck transitions.
- For v3, the inhabited world was `SAT` and `NoResponseReuse` was `UNSAT` (no
  bounded counterexample). Two broader checks were stopped after prolonged
  solving and are intentionally not claimed as evidence; their executable
  equivalents passed.

The v3 model covers the relational shape of the following later manifest rules:

| Released rule ID | v3 Alloy coverage | Executable authority |
| --- | --- | --- |
| `lineage.initial_pass.materialization.v1` | `InitialPassIdentityAndNoFalseChain` models initial attempts as pass materializations with acceptance-specific workspace presence | semantic manifest, schema, validator, fixtures, mutations |
| `lineage.pass_retry.predecessor_exact.v1` | `InitialPassIdentityAndNoFalseChain` models same-packet retry/pass/predecessor shape; concrete attempt identity and QA-report digest equality remain outside Alloy | semantic manifest, schema, validator, fixtures, mutations |
| `assembly.pass_winner.exact_six.v1` | `ExactInitialAssemblyBridge` selects exactly six accepted pass decisions and joins their output to the assembled deck | semantic manifest, schema, validator, fixtures, mutations |
| `deck.transition.discriminated.v1` | stage facts separate pre-assembly pass materialization from post-assembly polish transitions | semantic manifest, discriminated schema, validator, fixtures, mutations |

Later v4/v5 additions involving concrete native correlation, producer identity,
artifact bytes/digests, request provenance, serialization, and transport were
not added to this relational model unless already represented by an abstract
equality or ownership relation. Their absence is deliberate only where an Alloy
impact assessment says the relationship is unchanged or executable evidence is
the more faithful boundary.

| Rule ID | Adopted relationship | Alloy element | Future validator target | Future fixture/mutation target |
| --- | --- | --- | --- | --- |
| `lineage.initial_pass.exact_six.v1` | Ordinary v1 has exactly six released initial passes | `ExactV1Topology`, `InitialPassIdentityAndNoFalseChain` | `validate_chronology` | omit/duplicate/swap pass identity |
| `lineage.ordinal.total_contiguous.v1` | One decision at every packet-local ordinal | `ExactV1Topology`, `at` | `validate_chronology` | duplicate/skip/reorder ordinal |
| `lineage.initial_pass.no_false_chain.v1` | Parallel initial passes are not serialized deck transitions | `InitialPassIdentityAndNoFalseChain` | `validate_chronology` | fabricate initial input/output chain |
| `deck.transition.candidate_iff_materialized.v1` | Candidate exists iff materialization succeeded | `CandidateAndAdoptionAlgebra` | `validate_deck_transitions` | candidate with failed materialization / missing candidate |
| `deck.transition.output_matches_adoption.v1` | Adoption chooses candidate; non-adoption retains input | `CandidateAndAdoptionAlgebra` | `validate_deck_transitions` | swap input/candidate output |
| `deck.transition.next_input_contiguous.v1` | Next sequential input equals preceding output | `SequentialDeckContinuity` | `validate_deck_transitions` | next input drift |
| `deck.selection.reachable.v1` | Selected deck equals native current deck after last decision | `TerminalSelectionRules`, `SelectedDeckReachable` | `validate_deck_transitions` | unreachable selected deck |
| `deck.delivery.equals_selected.v1` | Delivery uses the selected deck; closeout does not imply delivery | `TerminalSelectionRules` | `validate_deck_transitions` | delivered/selected mismatch |
| `provider.response.unique_decision.v1` | Response is not reused across v1 decisions | `ExactProviderJoinV1`, `NoResponseReuse` | `validate_action_response_joins` | reuse Response across actions |
| `ownership.finding.same_packet.v1` | Finding has exactly one same-packet decision owner | `FindingOwnership` | `validate_ownership` | orphan/cross-packet owner |
| `ownership.validation.discriminated.v1` | Validation has exactly one decision or terminal owner | `ClosedValidationOwnership` | `validate_ownership` | dual/missing/wrong-kind owner |
| `projection.member.same_packet.v1` | Projection and exact projected member share a packet | `ProjectionEquivalenceShape`, `ProjectionStaysInPacket` | `validate_projections` | cross-packet projection member |
| `artifact.identity.packet_scoped.v1` | Artifact uniqueness is packet plus deck, while payload equality may cross packets | `PacketScopedArtifactIdentityShape`, `RequiredScopeWitnesses` | `validate_manifest_and_artifacts` | global artifact-ID collision |
| `artifact.absence.non_signaling.v1` | A used deck may lack an artifact observation without invalidating its packet | `PacketScopedArtifactIdentityShape`, `validTwoPacketWorld` | artifact-independent packet validation | remove artifact event from valid packet |
| `observation.api.non_authoritative.v1` | API observation presence/identity does not define native validity | `ApiObservation`, `validTwoPacketWorld` | transport/native ownership boundary | mutate/omit API observation annotations |

## Deliberate abstraction limits

- Payload digests are equality-bearing atoms; the model makes no cryptographic
  claim.
- Ordinals are eight named atoms because the feasibility scope uses exactly six
  initial decisions and two post-initial decisions per packet.
- The first model represents `polish` as the post-initial stage solely to prove
  transition relationships. Creative retry, critic, and candidate stages belong
  in Slice 1δ.1 only if they change the relation rather than merely the label.
- JSON value equality, canonical serialization, field-context populations,
  request compression, and byte limits remain Python/schema fixture concerns.
- `Projection` proves packet/member ownership shape here, not byte equality;
  digest/value equivalence remains an executable validator obligation.
- `Artifact` models packet-scoped wrapper identity and permitted absence, not
  Better Stack delivery.

## Slice 1δ.1 counterexample-campaign mapping

The campaign model keeps each adopted rule ID tied to one named relational
predicate or to the exact topology predicate that supplies the closed finite
shape. Several rule IDs intentionally share one predicate only when they are
separate clauses of the same algebra; the future semantic manifest and mutation
tests remain one rule ID per independently reported violation.

| Rule ID | Campaign model element |
| --- | --- |
| `lineage.initial_pass.exact_six.v1` | `CoreTopology` initial-pass clauses |
| `lineage.ordinal.total_contiguous.v1` | `CoreTopology`, `at` |
| `lineage.initial_pass.no_false_chain.v1` | `CoreTopology` initial-pass input/output clauses |
| `deck.transition.candidate_iff_materialized.v1` | `CandidateMaterializationRule` |
| `deck.transition.output_matches_adoption.v1` | `AdoptionOutputRule` |
| `deck.transition.next_input_contiguous.v1` | `ContinuityRule` |
| `deck.selection.reachable.v1` | `SelectionReachabilityRule` origin/owner clauses |
| `deck.delivery.equals_selected.v1` | `CoreTopology` accepted/closeout terminal clauses |
| `provider.response.unique_decision.v1` | `ResponseUniquenessRule` |
| `ownership.finding.same_packet.v1` | `FindingOwnershipRule` |
| `ownership.validation.discriminated.v1` | `ValidationOwnershipRule` |
| `projection.member.same_packet.v1` | `ProjectionRule` |
| `artifact.identity.packet_scoped.v1` | `ArtifactIdentityRule` |
| `artifact.absence.non_signaling.v1` | `ArtifactAbsenceRule` plus `ObservationNonAuthorityRule` |
| `observation.api.non_authoritative.v1` | `ObservationNonAuthorityRule` |
