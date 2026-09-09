module editorial_review_contract_v3

// Content-free relational model for the optional Slice 1δ design audit.
// Hashes are modeled only as equality-bearing atoms. No runtime/API behavior,
// payload text, provider activity, or cryptographic property is represented.

abstract sig Packet {
  assembled: one Deck
}
one sig AcceptedPacket, CloseoutPacket extends Packet {}

abstract sig Ordinal {}
one sig O0, O1, O2, O3, O4, O5, O6, O7, O8 extends Ordinal {}

abstract sig Stage {}
one sig InitialPass, CreativeRetry, Polish extends Stage {}

abstract sig PassIdentity {}
one sig Pass1, Pass2, Pass3, Pass4, Pass5, Pass6 extends PassIdentity {}

abstract sig Materialization {}
one sig Materialized, NotMaterialized extends Materialization {}

abstract sig Adoption {}
one sig Adopted, NotAdopted extends Adoption {}

abstract sig Acceptance {}
one sig Accepted, Rejected extends Acceptance {}

abstract sig SelectionOrigin {}
one sig DecisionSelection, AssemblySelection extends SelectionOrigin {}

sig PayloadDigest {}
sig Deck { payload: one PayloadDigest }
sig WorkspaceDigest {}
sig ClaimSetDigest {}
sig Action {}
sig Binding {}
sig Response {}

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
  response: lone Response,
  sourceBasis: lone WorkspaceDigest,
  acceptedWorkspace: lone WorkspaceDigest,
  authoredClaimSet: lone ClaimSetDigest,
  acceptance: lone Acceptance,
  predecessor: lone Decision
}

sig InitialAssembly {
  packet: one Packet,
  acceptedPasses: set Decision,
  output: one Deck
}

sig Finding extends Projectable { owner: one Decision }

abstract sig ValidationOwnerKind {}
one sig DecisionOwner, TerminalOwner extends ValidationOwnerKind {}

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

sig Projection {
  packet: one Packet,
  member: one Projectable
}

sig Artifact {
  packet: one Packet,
  deck: one Deck
}

sig ApiObservation { observed: one Packet }

fun at[p: Packet, o: Ordinal]: one Decision {
  { d: Decision | d.packet = p and d.ordinal = o }
}

fun selection[p: Packet]: one TerminalSelection {
  { t: TerminalSelection | t.packet = p }
}

fun usedDecks[p: Packet]: set Deck {
  { deck: Deck |
    (some d: Decision |
      d.packet = p and deck in d.input + d.candidate + d.output) or
    deck = selection[p].selected or
    deck = selection[p].delivered
  }
}

pred isInitial[o: Ordinal] {
  o in O0 + O1 + O2 + O3 + O4 + O5
}

fact ExactV1Topology {
  #Decision = 18
  all p: Packet, o: Ordinal | one d: Decision | d.packet = p and d.ordinal = o
  all p: Packet | #{ d: Decision | d.packet = p and d.stage = InitialPass } = 6
  all p: Packet | #{ d: Decision | d.packet = p and d.stage = CreativeRetry } = 1
  all p: Packet | #{ d: Decision | d.packet = p and d.stage = Polish } = 2
}

fact InitialPassIdentityAndNoFalseChain {
  all d: Decision |
    (isInitial[d.ordinal] implies
      d.stage = InitialPass and
      no d.input and no d.candidate and no d.output and
      d.materialization = Materialized and d.adoption = NotAdopted and
      one d.sourceBasis and one d.acceptance and
      one d.authoredClaimSet and one d.action and one d.binding and
      one d.response)

  all d: Decision |
    (d.ordinal in O7 + O8 implies
      d.stage = Polish and no d.initialPass and
      no d.sourceBasis and no d.acceptedWorkspace and no d.authoredClaimSet and no d.acceptance and no d.predecessor and
      one d.input and one d.output and one d.action and one d.binding and
      one d.response)

  all p: Packet |
    at[p, O0].initialPass = Pass1 and
    at[p, O1].initialPass = Pass2 and
    at[p, O2].initialPass = Pass3 and
    at[p, O3].initialPass = Pass4 and
    at[p, O4].initialPass = Pass5 and
    at[p, O5].initialPass = Pass6

  all p: Packet |
    at[p, O0].acceptance = Rejected and no at[p, O0].acceptedWorkspace and
    at[p, O6].stage = CreativeRetry and
    at[p, O6].initialPass = Pass1 and
    at[p, O6].predecessor = at[p, O0] and
    at[p, O6].acceptance = Accepted and
    at[p, O6].materialization = Materialized and
    at[p, O6].adoption = NotAdopted and
    one at[p, O6].sourceBasis and one at[p, O6].acceptedWorkspace and
    one at[p, O6].authoredClaimSet and one at[p, O6].action and
    one at[p, O6].binding and one at[p, O6].response

  all p: Packet, o: O1 + O2 + O3 + O4 + O5 |
    at[p, o].acceptance = Accepted and one at[p, o].acceptedWorkspace
}

fact ExactInitialAssemblyBridge {
  all p: Packet | one bridge: InitialAssembly |
    bridge.packet = p and
    bridge.acceptedPasses = { d: Decision |
      d.packet = p and d.acceptance = Accepted } and
    #bridge.acceptedPasses = 6 and
    bridge.output = p.assembled
}

fact CandidateAndAdoptionAlgebra {
  all d: Decision |
    (d.stage = Polish implies
      (d.materialization = Materialized iff one d.candidate))

  all d: Decision |
    (d.adoption = Adopted implies
      d.materialization = Materialized and d.output = d.candidate)

  all d: Decision |
    (d.adoption = NotAdopted and one d.input implies d.output = d.input)
}

fact SequentialDeckContinuity {
  all p: Packet | at[p, O7].input = p.assembled
  all p: Packet | at[p, O8].input = at[p, O7].output
}

fact ExactProviderJoinV1 {
  all disj d1, d2: Decision |
    (some d1.response and some d2.response) implies d1.response != d2.response

  all disj d1, d2: Decision |
    (some d1.action and some d2.action) implies d1.action != d2.action

  all disj d1, d2: Decision |
    (some d1.binding and some d2.binding) implies d1.binding != d2.binding
}

fact FindingOwnership {
  all f: Finding | f.owner.packet = f.packet
  all p: Packet | some f: Finding | f.packet = p
}

fact ClosedValidationOwnership {
  all v: Validation |
    (v.ownerKind = DecisionOwner implies
      one v.decisionOwner and no v.terminalOwner and
      v.decisionOwner.packet = v.packet)

  all v: Validation |
    (v.ownerKind = TerminalOwner implies
      no v.decisionOwner and one v.terminalOwner and
      v.terminalOwner.packet = v.packet)

  all p: Packet | some v: Validation |
    v.packet = p and v.ownerKind = TerminalOwner
  all p: Packet | some v: Validation |
    v.packet = p and v.ownerKind = DecisionOwner
}

fact TerminalSelectionRules {
  all p: Packet | one t: TerminalSelection | t.packet = p
  selection[AcceptedPacket].origin = DecisionSelection
  selection[AcceptedPacket].selectedBy = at[AcceptedPacket, O7]
  selection[AcceptedPacket].selected =
    selection[AcceptedPacket].selectedBy.output
  selection[CloseoutPacket].origin = AssemblySelection
  no selection[CloseoutPacket].selectedBy
  selection[CloseoutPacket].selected = CloseoutPacket.assembled
  all p: Packet | selection[p].selected = at[p, O8].output
  selection[AcceptedPacket].delivered = selection[AcceptedPacket].selected
  no selection[CloseoutPacket].delivered
}

fact ProjectionEquivalenceShape {
  all m: Projectable | one pr: Projection |
    pr.member = m and pr.packet = m.packet
  all pr: Projection | pr.packet = pr.member.packet
}

fact PacketScopedArtifactIdentityShape {
  all p: Packet, d: Deck | lone a: Artifact | a.packet = p and a.deck = d
  all a: Artifact | a.deck in usedDecks[a.packet]
  all p: Packet | some d: usedDecks[p] |
    no a: Artifact | a.packet = p and a.deck = d
}

fact RequiredScopeWitnesses {
  // Accepted: first polish adopted, second materialized but retained prior.
  at[AcceptedPacket, O7].materialization = Materialized
  at[AcceptedPacket, O7].adoption = Adopted
  at[AcceptedPacket, O7].candidate != at[AcceptedPacket, O7].input
  at[AcceptedPacket, O8].materialization = Materialized
  at[AcceptedPacket, O8].adoption = NotAdopted

  // Closeout: one malformed/non-materialized result, then a non-adopted
  // materialized candidate.
  at[CloseoutPacket, O7].materialization = NotMaterialized
  at[CloseoutPacket, O7].adoption = NotAdopted
  at[CloseoutPacket, O8].materialization = Materialized
  at[CloseoutPacket, O8].adoption = NotAdopted
  at[CloseoutPacket, O8].candidate != at[CloseoutPacket, O8].input

  // Cross-packet byte equality is payload equality, not wrapper identity.
  selection[AcceptedPacket].selected != selection[CloseoutPacket].selected
  selection[AcceptedPacket].selected.payload =
    selection[CloseoutPacket].selected.payload
}

pred validTwoPacketWorld {
  some ApiObservation
  some Artifact
}

assert NoResponseReuse {
  all disj d1, d2: Decision |
    (some d1.response and some d2.response) implies d1.response != d2.response
}

assert SelectedDeckReachable {
  all p: Packet | selection[p].selected = at[p, O8].output
}

assert ProjectionStaysInPacket {
  all pr: Projection | pr.packet = pr.member.packet
}

run validTwoPacketWorld for exactly 18 Decision, exactly 2 InitialAssembly,
  exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 24 Projection,
  12 Deck, 12 PayloadDigest, 14 WorkspaceDigest, 7 ClaimSetDigest,
  exactly 18 Action, exactly 18 Binding,
  exactly 18 Response, 6 Artifact, exactly 2 ApiObservation

check NoResponseReuse for exactly 18 Decision, exactly 2 InitialAssembly,
  exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 24 Projection,
  12 Deck, 12 PayloadDigest, 14 WorkspaceDigest, 7 ClaimSetDigest,
  exactly 18 Action, exactly 18 Binding,
  exactly 18 Response, 6 Artifact, exactly 2 ApiObservation

check SelectedDeckReachable for exactly 18 Decision, exactly 2 InitialAssembly,
  exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 24 Projection,
  12 Deck, 12 PayloadDigest, 14 WorkspaceDigest, 7 ClaimSetDigest,
  exactly 18 Action, exactly 18 Binding,
  exactly 18 Response, 6 Artifact, exactly 2 ApiObservation

check ProjectionStaysInPacket for exactly 18 Decision, exactly 2 InitialAssembly,
  exactly 2 TerminalSelection,
  exactly 2 Finding, exactly 4 Validation, exactly 24 Projection,
  12 Deck, 12 PayloadDigest, 14 WorkspaceDigest, 7 ClaimSetDigest,
  exactly 18 Action, exactly 18 Binding,
  exactly 18 Response, 6 Artifact, exactly 2 ApiObservation
