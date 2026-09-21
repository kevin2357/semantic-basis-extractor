module force_fence_completion_hard_stop_v1

// Bounded, content-free model of completion after an active-run force fence.
// Identifiers/digests are equality-bearing atoms.  This deliberately models
// scheduling ownership separately from durable/native/provider custody; it
// does not model bytes, processes, HTTP, or a cloud control plane.

open util/ordering[Moment] as time
sig Moment {}
sig Run {}
sig WorkerBoot {}
sig Invocation { ownerRun: one Run, boot: one WorkerBoot, launchedAt: one Moment }
sig ForceFence { target: one Invocation, at: one Moment }

abstract sig ChildState {}
one sig ChildLive, ChildExited extends ChildState {}
sig ChildObservation { invocation: one Invocation, state: one ChildState, at: one Moment }

// This is SBE's existing same-invocation safe-stop evidence.  It says nothing
// about API allocation or provider cancellation.
sig CooperativeResult { invocation: one Invocation, fence: one ForceFence, at: one Moment }
sig CooperativeReceipt { result: one CooperativeResult, invocation: one Invocation }
sig CooperativeCommand { result: one CooperativeResult, receipt: one CooperativeReceipt,
                         invocation: one Invocation }
sig OrdinaryResult { invocation: one Invocation, at: one Moment }

// Parent proof is exact process-group exit after the force fence.  Replacement
// is platform proof: target scope, worker scope, admission fence, full old-boot
// inventory, retirement/no-overlap, and a distinct replacement boot.
sig ParentExit { invocation: one Invocation, fence: one ForceFence, at: one Moment }
sig AdmissionFence { boot: one WorkerBoot, at: one Moment }
sig Replacement {
  target: one Invocation,
  oldBoot: one WorkerBoot,
  newBoot: one WorkerBoot,
  admission: one AdmissionFence,
  inventory: set Invocation,
  retiredAt: one Moment,
  newBootAt: one Moment
}
sig RecoveryRecord { replacement: one Replacement, collateral: one Invocation }
sig LateArtifact { invocation: one Invocation, at: one Moment }

abstract sig CapacityState {}
one sig AllocationHeld, AllocationReleased extends CapacityState {}
sig Capacity { owner: one Run, state: one CapacityState }

abstract sig Custody {}
one sig ProviderCustody, SpendCustody, WorkspaceCustody, NativeCustody extends Custody {}
sig RetainedCustody { owner: one Run, kind: one Custody }

abstract sig CompletionKind {}
one sig CooperativeFinal, ParentFinal, ReplacementFinal, OrdinaryPrecedence,
        Escalating extends CompletionKind {}
sig Completion {
  fence: one ForceFence,
  kind: one CompletionKind,
  cooperative: lone CooperativeResult,
  parentExit: lone ParentExit,
  replacement: lone Replacement,
  ordinary: lone OrdinaryResult,
  at: one Moment
}

// Peer admission is an API scheduling decision.  It is available after a
// target's final completion only when the peer has no independent global block.
sig GlobalBlock { blockedRun: one Run }
sig PeerAdmission { completion: one Completion, peer: one Invocation, at: one Moment }

fact IdentityAndTime {
  all f: ForceFence | time/lt[f.target.launchedAt, f.at]
  // Mirrors API's idempotency boundary: one active invocation cannot acquire
  // a second independent force-fence history.
  all i: Invocation | lone f: ForceFence | f.target = i
  all o: ChildObservation | time/lte[o.invocation.launchedAt, o.at]
  all c: CooperativeResult |
    c.invocation = c.fence.target and time/lte[c.fence.at, c.at]
  all o: OrdinaryResult | time/lte[o.invocation.launchedAt, o.at]
  all r: CooperativeReceipt | r.invocation = r.result.invocation
  all c: CooperativeCommand |
    c.invocation = c.result.invocation and c.receipt.result = c.result and
    c.receipt.invocation = c.invocation
  all e: ParentExit |
    e.invocation = e.fence.target and time/lte[e.fence.at, e.at]
  all r: Replacement |
    r.oldBoot = r.target.boot and r.newBoot != r.oldBoot and
    r.admission.boot = r.oldBoot and
    time/lt[r.admission.at, r.retiredAt] and time/lte[r.retiredAt, r.newBootAt]
  all a: LateArtifact | time/lte[a.invocation.launchedAt, a.at]
  all c: Completion | time/lte[c.fence.at, c.at]
  all a: PeerAdmission | time/lte[a.completion.at, a.at]
}

pred ExactEvidenceAndInventory {
  // A force-fenced invocation can publish at most one cooperative result.
  // Receipt and command envelope are then exact one-to-one consequences.
  all f: ForceFence | lone { c: CooperativeResult | c.fence = f }
  all c: CooperativeResult | one r: CooperativeReceipt | r.result = c
  all c: CooperativeResult | one x: CooperativeCommand |
    x.result = c and x.receipt.result = c
  all r: Replacement |
    r.inventory = { i: Invocation | i.boot = r.oldBoot and
      some o: ChildObservation | o.invocation = i and o.state = ChildLive and
      time/lte[o.at, r.retiredAt] }
  all rr: RecoveryRecord | rr.collateral != rr.replacement.target and
    rr.collateral in rr.replacement.inventory
  all r: Replacement, i: r.inventory - r.target |
    one rr: RecoveryRecord | rr.replacement = r and rr.collateral = i
  // The replacement admission fence closes old-boot launch admission before
  // inventory.  Retirement/no-overlap means no old-boot child is later live.
  all r: Replacement |
    no i: Invocation | i.boot = r.oldBoot and time/gt[i.launchedAt, r.admission.at]
  all r: Replacement | no o: ChildObservation |
    o.invocation.boot = r.oldBoot and o.state = ChildLive and
    time/lte[r.retiredAt, o.at]
  // Once old boot is retired, no artifact from it can establish completion.
  all c: Completion, a: LateArtifact |
    some c.replacement and a.invocation.boot = c.replacement.oldBoot and
    time/lte[c.replacement.retiredAt, a.at] implies
      no c.cooperative and no c.parentExit
}

pred currentExitAt[i: Invocation, t: Moment] {
  some exited: ChildObservation |
    exited.invocation = i and exited.state = ChildExited and time/lte[exited.at, t] and
    no live: ChildObservation |
      live.invocation = i and live.state = ChildLive and
      time/lte[exited.at, live.at] and time/lte[live.at, t]
}

pred replacementSafeNonwritingAt[r: Replacement, t: Moment] {
  time/lte[r.retiredAt, t]
  time/lte[r.newBootAt, t]
  no o: ChildObservation |
    o.invocation.boot = r.oldBoot and o.state = ChildLive and time/lte[r.retiredAt, o.at]
}

pred safeNonwritingAt[c: Completion] {
  c.kind in CooperativeFinal + ParentFinal implies currentExitAt[c.fence.target, c.at]
  c.kind = ReplacementFinal implies replacementSafeNonwritingAt[c.replacement, c.at]
}

pred final[c: Completion] { c.kind in CooperativeFinal + ParentFinal + ReplacementFinal }

fact CompletionClassification {
  all c: Completion |
    (c.kind = CooperativeFinal) iff
      some c.cooperative and some c.parentExit and no c.replacement and no c.ordinary and
      safeNonwritingAt[c]
  all c: Completion |
    (c.kind = ParentFinal) iff
      some c.parentExit and no c.cooperative and no c.replacement and no c.ordinary and
      safeNonwritingAt[c]
  all c: Completion |
    (c.kind = ReplacementFinal) iff
      some c.replacement and no c.cooperative and no c.parentExit and no c.ordinary and
      c.replacement.target = c.fence.target and safeNonwritingAt[c]
  all c: Completion |
    (c.kind = OrdinaryPrecedence) iff
      some c.ordinary and no c.cooperative and no c.parentExit and no c.replacement and
      c.ordinary.invocation = c.fence.target
  all c: Completion |
    (c.kind = Escalating) iff no c.cooperative and no c.parentExit and no c.replacement and no c.ordinary
}

fact OneCapacityPerRun {
  all r: Run | one x: Capacity | x.owner = r
}

pred CapacityAndCustodyBoundary {
  // Each run has exactly one scheduling allocation; a target allocation is
  // released only by final completion.  Retained custody is never released.
  all c: Completion |
    (final[c] iff (one x: Capacity | x.owner = c.fence.target.ownerRun and x.state = AllocationReleased))
  all rc: RetainedCustody | rc.kind in ProviderCustody + SpendCustody + WorkspaceCustody + NativeCustody
}

pred PeerAdmissionBoundary {
  all a: PeerAdmission |
    final[a.completion] and a.peer.ownerRun != a.completion.fence.target.ownerRun and
    (no b: GlobalBlock | b.blockedRun = a.peer.ownerRun) and
    (one x: Capacity | x.owner = a.peer.ownerRun and x.state = AllocationHeld)
}

pred FullContract {
  some Completion
  all f: ForceFence | one c: Completion | c.fence = f
  ExactEvidenceAndInventory
  CapacityAndCustodyBoundary
  PeerAdmissionBoundary
  // An ordinary result committed before a would-be cooperative observation
  // wins the race. SBE therefore publishes no cooperative result; the force
  // fence receives the explicit non-final, non-quarantine disposition.
  no o: OrdinaryResult, cooperative: CooperativeResult |
    o.invocation = cooperative.invocation and time/lt[o.at, cooperative.at]
}

pred ValidCooperativePeerWorld {
  FullContract
  some c: Completion | c.kind = CooperativeFinal
  some PeerAdmission
}

pred ValidParentPeerWorld {
  FullContract
  some c: Completion | c.kind = ParentFinal
  some PeerAdmission
}

pred ValidReplacementPeerWorld {
  FullContract
  some c: Completion | c.kind = ReplacementFinal
  some PeerAdmission
}

pred ValidEscalationWorld {
  FullContract
  some c: Completion | c.kind = Escalating
  no PeerAdmission
}

pred ValidOrdinaryPrecedenceWorld {
  FullContract
  some c: Completion | c.kind = OrdinaryPrecedence
  no PeerAdmission
}

assert UnresolvedNeverReleasesCapacity {
  FullContract implies all c: Completion |
    c.kind = Escalating implies
      (one x: Capacity | x.owner = c.fence.target.ownerRun and x.state = AllocationHeld)
}

assert FinalRequiresExactStoppedChild {
  FullContract implies all c: Completion |
    c.kind in CooperativeFinal + ParentFinal implies currentExitAt[c.fence.target, c.at]
}

assert ReplacementHasIndependentNonwritingProof {
  FullContract implies all c: Completion |
    c.kind = ReplacementFinal implies replacementSafeNonwritingAt[c.replacement, c.at]
}

assert OrdinaryPrecedenceCannotQuarantine {
  FullContract implies all c: Completion |
    c.kind = OrdinaryPrecedence implies not final[c] and no c.cooperative and
    no c.parentExit and no c.replacement
}

assert ReplacementFencesBeforeInventoryAndAccountsForCollateral {
  FullContract implies all r: Replacement |
    time/lt[r.admission.at, r.retiredAt] and
    all i: r.inventory - r.target |
      one rr: RecoveryRecord | rr.replacement = r and rr.collateral = i
}

assert RetiredBootArtifactsCannotFinalize {
  FullContract implies all c: Completion, a: LateArtifact |
    some c.replacement and a.invocation.boot = c.replacement.oldBoot and
    time/lte[c.replacement.retiredAt, a.at] implies
      no c.cooperative and no c.parentExit
}

assert PeerAdmissionNeedsFinalTargetAndNoIndependentBlock {
  FullContract implies all a: PeerAdmission |
    final[a.completion] and (no b: GlobalBlock | b.blockedRun = a.peer.ownerRun)
}

// Deliberately weakened worlds: each should be SAT, demonstrating why the
// corresponding contract condition must remain explicit in implementation.
pred SilenceReleasesCapacityWitness {
  some f: ForceFence, c: Completion, x: Capacity |
    c.fence = f and c.kind = Escalating and x.owner = f.target.ownerRun and
    x.state = AllocationReleased
}

pred UninventoriedCollateralReplacementWitness {
  some r: Replacement, i: Invocation |
    i.boot = r.oldBoot and i != r.target and
    some o: ChildObservation | o.invocation = i and o.state = ChildLive and
    time/lte[o.at, r.retiredAt] and i not in r.inventory
}

pred LateOldBootArtifactFinalizesWitness {
  some r: Replacement, c: Completion, a: LateArtifact |
    c.kind = CooperativeFinal and some c.cooperative and
    a.invocation.boot = r.oldBoot and c.cooperative.invocation = a.invocation and
    time/lte[r.retiredAt, a.at]
}

pred BlockedPeerAdmissionWitness {
  some a: PeerAdmission, b: GlobalBlock | b.blockedRun = a.peer.ownerRun
}

pred EarlierExitLaterLiveReleasesWitness {
  some c: Completion, exited, live: ChildObservation |
    final[c] and exited.invocation = c.fence.target and live.invocation = c.fence.target and
    exited.state = ChildExited and live.state = ChildLive and
    time/lt[exited.at, live.at] and time/lte[live.at, c.at]
}

run ValidCooperativePeerWorld for 8 but exactly 2 Run, exactly 2 Invocation,
  exactly 1 ForceFence, exactly 1 CooperativeResult, exactly 1 CooperativeReceipt,
  exactly 1 CooperativeCommand, exactly 1 ParentExit, exactly 0 Replacement,
  exactly 1 Completion, exactly 1 PeerAdmission, exactly 0 GlobalBlock,
  exactly 8 Moment
run ValidParentPeerWorld for 8 but exactly 2 Run, exactly 2 Invocation,
  exactly 1 ForceFence, exactly 0 CooperativeResult, exactly 0 CooperativeReceipt,
  exactly 0 CooperativeCommand, exactly 1 ParentExit, exactly 0 Replacement,
  exactly 1 Completion, exactly 1 PeerAdmission, exactly 0 GlobalBlock,
  exactly 8 Moment
run ValidReplacementPeerWorld for 8 but exactly 2 Run, exactly 2 Invocation,
  exactly 1 ForceFence, exactly 0 CooperativeResult, exactly 0 CooperativeReceipt,
  exactly 0 CooperativeCommand, exactly 0 ParentExit, exactly 1 Replacement,
  exactly 1 AdmissionFence, exactly 1 Completion, exactly 1 PeerAdmission,
  exactly 0 GlobalBlock, exactly 8 Moment
run ValidEscalationWorld for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 0 CooperativeResult, exactly 0 CooperativeReceipt,
  exactly 0 CooperativeCommand, exactly 0 ParentExit, exactly 0 Replacement,
  exactly 1 Completion, exactly 0 PeerAdmission, exactly 8 Moment
run ValidOrdinaryPrecedenceWorld for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 0 CooperativeResult, exactly 0 CooperativeReceipt,
  exactly 0 CooperativeCommand, exactly 0 ParentExit, exactly 0 Replacement,
  exactly 1 OrdinaryResult, exactly 1 Completion, exactly 0 PeerAdmission,
  exactly 8 Moment

check UnresolvedNeverReleasesCapacity for 8
check FinalRequiresExactStoppedChild for 8
check ReplacementHasIndependentNonwritingProof for 8
check OrdinaryPrecedenceCannotQuarantine for 8
check ReplacementFencesBeforeInventoryAndAccountsForCollateral for 8
check RetiredBootArtifactsCannotFinalize for 8
check PeerAdmissionNeedsFinalTargetAndNoIndependentBlock for 8

run SilenceReleasesCapacityWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 Completion, exactly 8 Moment
run UninventoriedCollateralReplacementWitness for 8 but exactly 2 Run, exactly 2 Invocation,
  exactly 1 Replacement, exactly 8 Moment
run LateOldBootArtifactFinalizesWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 Replacement, exactly 1 Completion, exactly 1 LateArtifact, exactly 8 Moment
run BlockedPeerAdmissionWitness for 8 but exactly 2 Run, exactly 2 Invocation,
  exactly 1 Completion, exactly 1 PeerAdmission, exactly 1 GlobalBlock, exactly 8 Moment
run EarlierExitLaterLiveReleasesWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 Completion, exactly 2 ChildObservation,
  exactly 8 Moment
