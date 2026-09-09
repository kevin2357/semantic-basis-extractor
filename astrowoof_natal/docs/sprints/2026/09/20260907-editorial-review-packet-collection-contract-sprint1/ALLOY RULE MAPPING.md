# Alloy rule mapping — Slice 1δ.0

Status: feasibility mapping, not the final semantic manifest. Rule IDs are
proposed stable identifiers and must remain one-to-one across adopted prose,
Alloy, the future Python validator, and fixture/mutation tests.

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
