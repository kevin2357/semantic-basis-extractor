module editorial_review_counterexamples_v1

// Slice 1δ.1 counterexample model. Rules are predicates rather than global
// facts so each high-risk rule can be removed deliberately while retaining the
// rest of the contract. Payload hashes remain equality-only atoms.

abstract sig Packet { assembled: one Deck }
one sig AcceptedPacket, CloseoutPacket extends Packet {}

abstract sig Ordinal {}
one sig O0, O1, O2, O3, O4, O5, O6, O7 extends Ordinal {}
abstract sig Stage {}
one sig InitialPass, Polish extends Stage {}
abstract sig PassIdentity {}
one sig Pass1, Pass2, Pass3, Pass4, Pass5, Pass6 extends PassIdentity {}
abstract sig Materialization {}
one sig Materialized, NotMaterialized extends Materialization {}
abstract sig Adoption {}
one sig Adopted, NotAdopted extends Adoption {}
abstract sig SelectionOrigin {}
one sig DecisionSelection, AssemblySelection extends SelectionOrigin {}
abstract sig ValidationOwnerKind {}
one sig DecisionOwner, TerminalOwner extends ValidationOwnerKind {}

sig PayloadDigest {}
sig Deck { payload: one PayloadDigest }
sig Action {}
sig Binding {}
sig Response {}
sig ArtifactIdentity {}

abstract sig Projectable { packet: one Packet }
sig Decision extends Projectable {
  ordinal: one Ordinal,
  stage: one Stage,
  initialPass: lone PassIdentity,
  input: lone Deck,
  candidate: lone Deck,
  output: lone Deck,
  materialization: one Materialization,
  adoption: one Adoption,
  action: lone Action,
  binding: lone Binding,
  response: lone Response
}
sig Finding extends Projectable { owner: lone Decision }
sig Validation extends Projectable {
  ownerKind: one ValidationOwnerKind,
  decisionOwner: lone Decision,
  terminalOwner: lone TerminalSelection
}
sig TerminalSelection {
  packet: one Packet,
  selected: one Deck,
  delivered: lone Deck,
  origin: one SelectionOrigin,
  selectedBy: lone Decision
}
sig Projection { packet: one Packet, member: one Projectable }
sig Artifact {
  packet: one Packet,
  deck: one Deck,
  identity: one ArtifactIdentity
}
sig ApiObservation { observed: one Packet }
one sig ContractAssessment { eligible: set Packet }

fun at[p: Packet, o: Ordinal]: one Decision {
  { d: Decision | d.packet = p and d.ordinal = o }
}
fun selection[p: Packet]: one TerminalSelection {
  { t: TerminalSelection | t.packet = p }
}
fun usedDecks[p: Packet]: set Deck {
  { deck: Deck |
    deck = p.assembled or
    (some d: Decision |
      d.packet = p and deck in d.input + d.candidate + d.output) or
    deck = selection[p].selected or deck = selection[p].delivered
  }
}
pred isInitial[o: Ordinal] { o in O0 + O1 + O2 + O3 + O4 + O5 }

pred CoreTopology {
  #Decision = 16
  all p: Packet, o: Ordinal | one d: Decision | d.packet = p and d.ordinal = o
  all p: Packet | #{ d: Decision | d.packet = p and d.stage = InitialPass } = 6
  all p: Packet | #{ d: Decision | d.packet = p and d.stage = Polish } = 2
  all p: Packet | one t: TerminalSelection | t.packet = p

  all d: Decision |
    (isInitial[d.ordinal] implies
      d.stage = InitialPass and no d.input and no d.candidate and no d.output and
      d.materialization = NotMaterialized and d.adoption = NotAdopted and
      no d.action and no d.binding and no d.response)
  all d: Decision |
    (not isInitial[d.ordinal] implies
      d.stage = Polish and no d.initialPass and one d.input and one d.output and
      one d.action and one d.binding and one d.response)

  all p: Packet |
    at[p,O0].initialPass=Pass1 and at[p,O1].initialPass=Pass2 and
    at[p,O2].initialPass=Pass3 and at[p,O3].initialPass=Pass4 and
    at[p,O4].initialPass=Pass5 and at[p,O5].initialPass=Pass6

  at[AcceptedPacket,O6].materialization=Materialized
  at[AcceptedPacket,O6].adoption=Adopted
  at[AcceptedPacket,O6].candidate != at[AcceptedPacket,O6].input
  at[AcceptedPacket,O7].materialization=Materialized
  at[AcceptedPacket,O7].adoption=NotAdopted

  at[CloseoutPacket,O6].materialization=NotMaterialized
  at[CloseoutPacket,O6].adoption=NotAdopted
  at[CloseoutPacket,O7].materialization=Materialized
  at[CloseoutPacket,O7].adoption=NotAdopted
  at[CloseoutPacket,O7].candidate != at[CloseoutPacket,O7].input

  selection[AcceptedPacket].origin=DecisionSelection
  selection[AcceptedPacket].selectedBy=at[AcceptedPacket,O6]
  selection[AcceptedPacket].delivered=selection[AcceptedPacket].selected
  selection[CloseoutPacket].origin=AssemblySelection
  no selection[CloseoutPacket].selectedBy
  no selection[CloseoutPacket].delivered

  selection[AcceptedPacket].selected != selection[CloseoutPacket].selected
  selection[AcceptedPacket].selected.payload =
    selection[CloseoutPacket].selected.payload

  all p: Packet | some f: Finding | f.packet=p
  all p: Packet | some v: Validation | v.packet=p and v.ownerKind=TerminalOwner
  all p: Packet | some v: Validation | v.packet=p and v.ownerKind=DecisionOwner
  some Artifact
  some ApiObservation
}

pred CandidateMaterializationRule {
  all d: Decision | (d.materialization=Materialized iff one d.candidate)
}
pred AdoptionOutputRule {
  all d: Decision |
    (d.adoption=Adopted implies
      d.materialization=Materialized and d.output=d.candidate)
  all d: Decision |
    (d.adoption=NotAdopted and one d.input implies d.output=d.input)
}
pred ContinuityRule {
  all p: Packet | at[p,O6].input=p.assembled
  all p: Packet | at[p,O7].input=at[p,O6].output
}
pred SelectionReachabilityRule {
  all p: Packet |
    (selection[p].origin=DecisionSelection implies
      one selection[p].selectedBy and
      selection[p].selectedBy.packet=p and
      selection[p].selected=selection[p].selectedBy.output)
  all p: Packet |
    (selection[p].origin=AssemblySelection implies
      no selection[p].selectedBy and selection[p].selected=p.assembled)
  all p: Packet | selection[p].selected=at[p,O7].output
}
pred ResponseUniquenessRule {
  all disj d1,d2: Decision |
    (some d1.response and some d2.response) implies d1.response != d2.response
  all disj d1,d2: Decision |
    (some d1.action and some d2.action) implies d1.action != d2.action
  all disj d1,d2: Decision |
    (some d1.binding and some d2.binding) implies d1.binding != d2.binding
}
pred FindingOwnershipRule {
  all f: Finding | one f.owner and f.owner.packet=f.packet
}
pred ValidationOwnershipRule {
  all v: Validation |
    (v.ownerKind=DecisionOwner implies one v.decisionOwner and
      no v.terminalOwner and v.decisionOwner.packet=v.packet)
  all v: Validation |
    (v.ownerKind=TerminalOwner implies no v.decisionOwner and
      one v.terminalOwner and v.terminalOwner.packet=v.packet)
}
pred ProjectionRule {
  all m: Projectable | one pr: Projection |
    pr.member=m and pr.packet=m.packet
  all pr: Projection | pr.packet=pr.member.packet
}
pred ArtifactIdentityRule {
  all p: Packet, digest: PayloadDigest |
    lone a: Artifact | a.packet=p and a.deck.payload=digest
  all disj a1,a2: Artifact | a1.identity != a2.identity
  all a: Artifact | a.deck in usedDecks[a.packet]
}
pred ArtifactAbsenceRule {
  all p: Packet | some d: usedDecks[p] |
    no a: Artifact | a.packet=p and a.deck=d
}
pred ObservationNonAuthorityRule { ContractAssessment.eligible=Packet }

pred FullContract {
  CoreTopology
  CandidateMaterializationRule
  AdoptionOutputRule
  ContinuityRule
  SelectionReachabilityRule
  ResponseUniquenessRule
  FindingOwnershipRule
  ValidationOwnershipRule
  ProjectionRule
  ArtifactIdentityRule
  ArtifactAbsenceRule
  ObservationNonAuthorityRule
}

assert FullSelectionReachability { FullContract implies SelectionReachabilityRule }
assert FullAdoptionOutput { FullContract implies AdoptionOutputRule }
assert FullContinuity { FullContract implies ContinuityRule }
assert FullResponseUniqueness { FullContract implies ResponseUniquenessRule }
assert FullFindingOwnership { FullContract implies FindingOwnershipRule }
assert FullValidationOwnership { FullContract implies ValidationOwnershipRule }
assert FullProjectionRelation { FullContract implies ProjectionRule }
assert FullArtifactIdentity { FullContract implies ArtifactIdentityRule }
assert FullArtifactAbsence { FullContract implies ArtifactAbsenceRule }
assert FullObservationNonAuthority { FullContract implies ObservationNonAuthorityRule }

pred WithoutSelectionCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and ResponseUniquenessRule and FindingOwnershipRule and
  ValidationOwnershipRule and ProjectionRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and
  not SelectionReachabilityRule
}
pred WithoutAdoptionCounterexample {
  CoreTopology and CandidateMaterializationRule and ContinuityRule and
  SelectionReachabilityRule and ResponseUniquenessRule and FindingOwnershipRule
  and ValidationOwnershipRule and ProjectionRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and not AdoptionOutputRule
}
pred WithoutContinuityCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  SelectionReachabilityRule and ResponseUniquenessRule and FindingOwnershipRule
  and ValidationOwnershipRule and ProjectionRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and not ContinuityRule
}
pred WithoutResponseUniquenessCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and FindingOwnershipRule and
  ValidationOwnershipRule and ProjectionRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and
  not ResponseUniquenessRule
}
pred WithoutFindingOwnershipCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and ResponseUniquenessRule and
  ValidationOwnershipRule and ProjectionRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and not FindingOwnershipRule
}
pred WithoutValidationOwnershipCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and ResponseUniquenessRule and
  FindingOwnershipRule and ProjectionRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and
  not ValidationOwnershipRule
}
pred WithoutProjectionCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and ResponseUniquenessRule and
  FindingOwnershipRule and ValidationOwnershipRule and ArtifactIdentityRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and not ProjectionRule
}
pred WithoutArtifactIdentityCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and ResponseUniquenessRule and
  FindingOwnershipRule and ValidationOwnershipRule and ProjectionRule and
  ArtifactAbsenceRule and ObservationNonAuthorityRule and not ArtifactIdentityRule
}
pred ArtifactCompletenessControlsEligibilityCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and ResponseUniquenessRule and
  FindingOwnershipRule and ValidationOwnershipRule and ProjectionRule and
  ArtifactIdentityRule and ArtifactAbsenceRule and
  ContractAssessment.eligible={p:Packet | all d:usedDecks[p] |
    some a:Artifact | a.packet=p and a.deck=d} and
  not ObservationNonAuthorityRule
}
pred ApiObservationControlsEligibilityCounterexample {
  CoreTopology and CandidateMaterializationRule and AdoptionOutputRule and
  ContinuityRule and SelectionReachabilityRule and ResponseUniquenessRule and
  FindingOwnershipRule and ValidationOwnershipRule and ProjectionRule and
  ArtifactIdentityRule and ArtifactAbsenceRule and
  ContractAssessment.eligible=ApiObservation.observed and
  not ObservationNonAuthorityRule
}

run FullContract for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation

check FullSelectionReachability for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullAdoptionOutput for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullContinuity for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullResponseUniqueness for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullFindingOwnership for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullValidationOwnership for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullProjectionRelation for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullArtifactIdentity for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullArtifactAbsence for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
check FullObservationNonAuthority for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation

run WithoutSelectionCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutAdoptionCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutContinuityCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutResponseUniquenessCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutFindingOwnershipCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutValidationOwnershipCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutProjectionCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run WithoutArtifactIdentityCounterexample for exactly 16 Decision, exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 22 Projection,
  12 Deck, 12 PayloadDigest, exactly 4 Action, exactly 4 Binding,
  exactly 4 Response, exactly 2 Artifact, exactly 2 ArtifactIdentity,
  exactly 2 ApiObservation
run ArtifactCompletenessControlsEligibilityCounterexample for exactly 16 Decision,
  exactly 2 TerminalSelection, exactly 2 Finding, exactly 4 Validation,
  exactly 22 Projection, 12 Deck, 12 PayloadDigest, exactly 4 Action,
  exactly 4 Binding, exactly 4 Response, exactly 2 Artifact,
  exactly 2 ArtifactIdentity, exactly 2 ApiObservation
run ApiObservationControlsEligibilityCounterexample for exactly 16 Decision,
  exactly 2 TerminalSelection, exactly 2 Finding, exactly 4 Validation,
  exactly 22 Projection, 12 Deck, 12 PayloadDigest, exactly 4 Action,
  exactly 4 Binding, exactly 4 Response, exactly 2 Artifact,
  exactly 2 ArtifactIdentity, exactly 2 ApiObservation
