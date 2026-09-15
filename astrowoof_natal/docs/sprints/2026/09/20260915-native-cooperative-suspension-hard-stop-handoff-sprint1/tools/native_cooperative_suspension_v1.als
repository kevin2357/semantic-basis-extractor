module native_cooperative_suspension_v1

// Content-free bounded model for the joined API/SBE cooperative-suspension
// protocol. Digests and identifiers are equality-bearing atoms only. This does
// not model bytes, cryptography, filesystem behavior, subprocesses, or provider
// timing.

open util/ordering[Moment] as time
sig Moment {}
sig Run {}
sig Job { ownerRun: one Run }
sig Attempt { job: one Job }
sig Lease { attempt: one Attempt }
sig WorkerBoot {}
sig LaunchGeneration {}
sig ControlRoot {}
sig RequestKey {}
sig Digest {}

abstract sig Route {}
one sig OrdinaryV2Dispatch, ProviderReconciliation, UnsupportedRoute extends Route {}

sig Checkpoint {
  ownerRun: one Run,
  predecessor: lone Checkpoint
}

sig Invocation {
  ownerRun: one Run,
  job: one Job,
  attempt: one Attempt,
  lease: one Lease,
  boot: one WorkerBoot,
  generation: one LaunchGeneration,
  controlRoot: one ControlRoot,
  route: one Route
}

sig ForceFence {
  invocation: one Invocation,
  observedCheckpoint: one Checkpoint,
  at: one Moment
}

abstract sig Freshness {}
one sig Current, Stale extends Freshness {}

sig SuspensionRequest {
  invocation: one Invocation,
  fence: one ForceFence,
  key: one RequestKey,
  digest: one Digest,
  admissionCheckpoint: one Checkpoint,
  freshness: one Freshness,
  at: one Moment
}

sig SuspensionObservation {
  request: one SuspensionRequest,
  checkpoint: one Checkpoint,
  at: one Moment
}

abstract sig SuspensionOutcome {}
one sig Suspended, Deferred, Refused, ProviderAmbiguous,
        PublicationAmbiguous extends SuspensionOutcome {}

sig SuspensionResult {
  invocation: one Invocation,
  request: one SuspensionRequest,
  observation: one SuspensionObservation,
  observedCheckpoint: one Checkpoint,
  outcome: one SuspensionOutcome,
  at: one Moment
}


sig SuspensionReceipt {
  invocation: one Invocation,
  result: one SuspensionResult
}

sig SuspensionCommandResult {
  invocation: one Invocation,
  result: one SuspensionResult,
  receipt: one SuspensionReceipt
}

sig OrdinaryResult {
  invocation: one Invocation,
  checkpoint: one Checkpoint,
  at: one Moment
}

sig ProcessExit {
  invocation: one Invocation,
  at: one Moment
}

abstract sig Resource {}
one sig WorkerExecution, RunAllocation, ProviderCustody, SpendCustody,
        WorkspaceCustody, NativeCustody extends Resource {}

sig Resolution {
  fence: one ForceFence,
  predecessor: lone Resolution,
  released: set Resource,
  selectedSuspension: lone SuspensionResult,
  selectedOrdinary: lone OrdinaryResult,
  exitEvidence: lone ProcessExit,
  at: one Moment
}

sig OrdinaryAuthorityGrant {
  invocation: one Invocation,
  at: one Moment
}

fact IdentitySpine {
  all i: Invocation |
    i.job.ownerRun = i.ownerRun and
    i.attempt.job = i.job and
    i.lease.attempt = i.attempt

  all f: ForceFence | f.observedCheckpoint.ownerRun = f.invocation.ownerRun
  all q: SuspensionRequest |
    q.fence.invocation = q.invocation and
    q.admissionCheckpoint = q.fence.observedCheckpoint
  all x: SuspensionObservation |
    x.checkpoint.ownerRun = x.request.invocation.ownerRun
  all s: SuspensionResult |
    s.request.invocation = s.invocation and
    s.observation.request = s.request and
    s.observedCheckpoint = s.observation.checkpoint and
    s.observedCheckpoint.ownerRun = s.invocation.ownerRun
  all o: OrdinaryResult | o.checkpoint.ownerRun = o.invocation.ownerRun
  all r: Resolution |
    (some r.predecessor implies r.predecessor.fence = r.fence) and
    (some r.selectedSuspension implies
      r.selectedSuspension.request.fence = r.fence) and
    (some r.selectedOrdinary implies
      r.selectedOrdinary.invocation = r.fence.invocation) and
    (some r.exitEvidence implies
      r.exitEvidence.invocation = r.fence.invocation)
}

fact ImmutableIdentityUniqueness {
  all disj i1, i2: Invocation |
    i1.ownerRun = i2.ownerRun implies
      i1.generation != i2.generation and i1.controlRoot != i2.controlRoot
  all disj f1, f2: ForceFence | f1.invocation != f2.invocation
}

fact CheckpointLineage {
  no c: Checkpoint | c in c.^predecessor
  all c: Checkpoint | lone predecessor.c
  all c: Checkpoint |
    some c.predecessor implies c.predecessor.ownerRun = c.ownerRun
}

fact EventOrdering {
  all q: SuspensionRequest | time/lte[q.fence.at, q.at]
  all x: SuspensionObservation | time/lte[x.request.at, x.at]
  all s: SuspensionResult |
    time/lte[s.observation.at, s.at]
  all r: Resolution |
    time/lte[r.fence.at, r.at] and
    (some r.predecessor implies time/lt[r.predecessor.at, r.at]) and
    (some r.selectedSuspension implies time/lte[r.selectedSuspension.at, r.at]) and
    (some r.selectedOrdinary implies time/lte[r.selectedOrdinary.at, r.at]) and
    (some r.exitEvidence implies time/lte[r.exitEvidence.at, r.at])
}

pred sameOrContiguousSuccessor[anchor, observed: Checkpoint] {
  observed = anchor or observed.predecessor = anchor
}

pred supported[i: Invocation] {
  i.route in OrdinaryV2Dispatch + ProviderReconciliation
}

pred exactReplay[q1, q2: SuspensionRequest] {
  q1.invocation = q2.invocation and q1.key = q2.key and q1.digest = q2.digest
}

pred conflictingReplay[q1, q2: SuspensionRequest] {
  q1.invocation = q2.invocation and q1 != q2
}

pred canonicalRequest[q: SuspensionRequest] {
  no earlier: SuspensionRequest |
    earlier.invocation = q.invocation and time/lt[earlier.at, q.at]
}

pred BaseWorld {
  some ForceFence
  all i: Invocation | one f: ForceFence | f.invocation = i
  all f: ForceFence | some q: SuspensionRequest | q.fence = f
  all q: SuspensionRequest | one x: SuspensionObservation | x.request = q
  all f: ForceFence | some r: Resolution | r.fence = f
}

pred FullContract {
  BaseWorld

  // Only a current, identity-exact request on a supported route can produce a
  // non-refusal result, and observation is limited to the admission checkpoint
  // or its exact contiguous successor.
  all s: SuspensionResult |
    (s.outcome != Refused implies
      canonicalRequest[s.request] and
      s.request.freshness = Current and supported[s.invocation] and
      sameOrContiguousSuccessor[s.request.admissionCheckpoint, s.observedCheckpoint])

  // Exact replay is the same canonical request atom. Every distinct later
  // request for the invocation is a conflict regardless of idempotency key.
  all disj q1, q2: SuspensionRequest |
    q1.invocation = q2.invocation implies
      q1.at != q2.at and not exactReplay[q1, q2]
  all q: SuspensionRequest |
    not canonicalRequest[q] implies
      all s: SuspensionResult | s.request = q implies s.outcome = Refused

  // One canonical request can publish at most one semantic native result.
  all q: SuspensionRequest | lone { s: SuspensionResult | s.request = q }
  all s: SuspensionResult | one p: SuspensionReceipt |
    p.result = s and p.invocation = s.invocation
  all s: SuspensionResult | one c: SuspensionCommandResult |
    c.result = s and c.invocation = s.invocation and
    c.receipt.result = s and c.receipt.invocation = s.invocation
  all p: SuspensionReceipt | p.invocation = p.result.invocation
  all c: SuspensionCommandResult |
    c.invocation = c.result.invocation and
    c.receipt.result = c.result and
    c.receipt.invocation = c.invocation

  // A resolution history is a single append-only chain per fence, not merely
  // an acyclic predecessor graph.
  no r: Resolution | r in r.^predecessor
  all r: Resolution | lone predecessor.r
  all f: ForceFence | one r: Resolution |
    r.fence = f and no r.predecessor

  // Evidence cannot be mixed across runs/invocations. Process exit is enough
  // only for worker-execution reclamation; every other custody class remains.
  all r: Resolution |
    (some r.released implies some r.exitEvidence) and
    r.released in WorkerExecution

  // An already-published ordinary result dominates later suspension evidence.
  all r: Resolution |
    (some r.selectedOrdinary implies no r.selectedSuspension)
  all o: OrdinaryResult, x: SuspensionObservation |
    o.invocation = x.request.invocation and time/lt[o.at, x.at] implies
      no s: SuspensionResult | s.observation = x
  all r: Resolution, o: OrdinaryResult, x: SuspensionObservation |
    x.request.fence = r.fence and time/lte[x.at, r.at] and
    o.invocation = r.fence.invocation and time/lt[o.at, x.at] implies
      r.selectedOrdinary = o and no r.selectedSuspension

  // A fence is irreversible for the exact invocation.
  no g: OrdinaryAuthorityGrant, f: ForceFence |
    g.invocation = f.invocation and time/gt[g.at, f.at]
}

// Inhabited worlds guard the checks against vacuity.
pred ValidTwoRunWorld {
  FullContract
  #Run = 2
  #Invocation = 2
  #ForceFence = 2
  #Resolution >= 3
  some s: SuspensionResult | s.outcome = Suspended
  some OrdinaryResult
  some r: Resolution | r.released = WorkerExecution
  some q: SuspensionRequest | q.freshness = Current
}

pred ValidConflictReplayWorld {
  FullContract
  some disj q1, q2: SuspensionRequest |
    canonicalRequest[q1] and time/lt[q1.at, q2.at] and
    conflictingReplay[q1, q2] and
    some s1, s2: SuspensionResult |
      s1.request = q1 and s2.request = q2 and s1.outcome = Suspended and
      s2.outcome = Refused
}

pred ValidSuccessorObservationWorld {
  FullContract
  some s: SuspensionResult |
    s.outcome = Suspended and
    s.observedCheckpoint.predecessor = s.request.admissionCheckpoint
}

pred ValidPriorOrdinaryDominanceWorld {
  FullContract
  some r: Resolution, o: OrdinaryResult, x: SuspensionObservation |
    x.request.fence = r.fence and time/lte[x.at, r.at] and
    o.invocation = r.fence.invocation and time/lt[o.at, x.at] and
    r.selectedOrdinary = o and no r.selectedSuspension and
    no s: SuspensionResult | s.observation = x
}

assert FenceNeverRestoresOrdinaryAuthority {
  FullContract implies no g: OrdinaryAuthorityGrant, f: ForceFence |
    g.invocation = f.invocation and time/gt[g.at, f.at]
}

assert StaleOrMismatchedRequestCannotSuspend {
  FullContract implies all s: SuspensionResult |
    (s.request.freshness = Stale or not supported[s.invocation] or
     not sameOrContiguousSuccessor[s.request.admissionCheckpoint, s.observedCheckpoint])
      implies s.outcome = Refused
}

assert ResolutionHistoryIsContiguousAndUnforked {
  FullContract implies
    no r: Resolution | r in r.^predecessor and
    all r: Resolution | lone predecessor.r
}

assert ExitReleasesOnlyWorkerExecution {
  FullContract implies all r: Resolution |
    r.released in WorkerExecution
}

assert PartialEvidenceCannotSettleCustody {
  FullContract implies no r: Resolution |
    some (r.released & (RunAllocation + ProviderCustody + SpendCustody +
                       WorkspaceCustody + NativeCustody))
}

assert PriorOrdinaryResultDominates {
  FullContract implies all o: OrdinaryResult, x: SuspensionObservation |
    o.invocation = x.request.invocation and time/lt[o.at, x.at] implies
      no s: SuspensionResult | s.observation = x
}

assert OneCanonicalResultPerRequest {
  FullContract implies all q: SuspensionRequest |
    lone { s: SuspensionResult | s.request = q }
}

assert ExactReceiptAndCommandResultBinding {
  FullContract implies
    (all s: SuspensionResult | one p: SuspensionReceipt | p.result = s) and
    (all s: SuspensionResult | one c: SuspensionCommandResult |
      c.result = s and c.receipt.result = s and c.invocation = s.invocation)
}

assert ReplayIsInertOrRefused {
  FullContract implies all disj q1, q2: SuspensionRequest |
    q1.invocation = q2.invocation implies
      (not exactReplay[q1, q2] and
       (time/lt[q1.at, q2.at] implies
         all s: SuspensionResult | s.request = q2 implies s.outcome = Refused) and
       (time/lt[q2.at, q1.at] implies
         all s: SuspensionResult | s.request = q1 implies s.outcome = Refused))
}

assert CrossRunIsolation {
  FullContract implies all r: Resolution |
    r.selectedSuspension.invocation.ownerRun in r.fence.invocation.ownerRun and
    r.selectedOrdinary.invocation.ownerRun in r.fence.invocation.ownerRun and
    r.exitEvidence.invocation.ownerRun in r.fence.invocation.ownerRun
}

// Deliberately weakened probes: each should be SAT and exhibit why the named
// full-contract rule must remain explicit.
pred ForkedResolutionWitness {
  BaseWorld
  some disj r1, r2: Resolution |
    one r1.predecessor and r1.predecessor = r2.predecessor
}

pred ExitSettlesAllCustodyWitness {
  BaseWorld
  some r: Resolution |
    some r.exitEvidence and r.released = Resource
}

pred StaleRequestSuspendsWitness {
  BaseWorld
  some s: SuspensionResult |
    s.request.freshness = Stale and s.outcome = Suspended
}

pred PriorOrdinaryResultLosesWitness {
  BaseWorld
  some r: Resolution, o: OrdinaryResult, s: SuspensionResult |
    s.request.fence = r.fence and time/lte[s.at, r.at] and
    o.invocation = r.fence.invocation and time/lt[o.at, s.observation.at] and
    r.selectedSuspension = s and no r.selectedOrdinary
}

pred ConflictingResultsForOneRequestWitness {
  BaseWorld
  some disj s1, s2: SuspensionResult |
    s1.request = s2.request and s1.outcome != s2.outcome
}

pred DuplicateReceiptWitness {
  BaseWorld
  some s: SuspensionResult | #{ p: SuspensionReceipt | p.result = s } > 1
}

pred CrossInvocationCommandResultWitness {
  BaseWorld
  some c: SuspensionCommandResult |
    c.invocation != c.result.invocation or
    c.receipt.result != c.result or
    c.receipt.invocation != c.invocation
}

run ValidTwoRunWorld for 8 but exactly 2 Run, exactly 2 Invocation,
  exactly 2 ForceFence, exactly 2 SuspensionRequest, exactly 2 SuspensionResult,
  exactly 2 SuspensionObservation, exactly 2 SuspensionReceipt,
  exactly 2 SuspensionCommandResult, exactly 1 OrdinaryResult,
  exactly 1 ProcessExit, exactly 3 Resolution,
  exactly 2 Checkpoint, exactly 8 Moment
run ValidConflictReplayWorld for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 2 SuspensionRequest, exactly 2 SuspensionResult,
  exactly 2 SuspensionObservation, exactly 2 SuspensionReceipt,
  exactly 2 SuspensionCommandResult, exactly 1 Resolution,
  exactly 1 Checkpoint, exactly 8 Moment
run ValidSuccessorObservationWorld for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest, exactly 1 SuspensionResult,
  exactly 1 SuspensionObservation, exactly 1 SuspensionReceipt,
  exactly 1 SuspensionCommandResult, exactly 1 Resolution,
  exactly 2 Checkpoint, exactly 8 Moment
run ValidPriorOrdinaryDominanceWorld for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest,
  exactly 1 SuspensionObservation, exactly 0 SuspensionResult,
  exactly 0 SuspensionReceipt, exactly 0 SuspensionCommandResult,
  exactly 1 OrdinaryResult, exactly 1 Resolution,
  exactly 1 Checkpoint, exactly 8 Moment

check FenceNeverRestoresOrdinaryAuthority for 8
check StaleOrMismatchedRequestCannotSuspend for 8
check ResolutionHistoryIsContiguousAndUnforked for 8
check ExitReleasesOnlyWorkerExecution for 8
check PartialEvidenceCannotSettleCustody for 8
check PriorOrdinaryResultDominates for 8
check ReplayIsInertOrRefused for 8
check CrossRunIsolation for 8
check OneCanonicalResultPerRequest for 8
check ExactReceiptAndCommandResultBinding for 8

run ForkedResolutionWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest, exactly 3 Resolution,
  exactly 1 Checkpoint, exactly 8 Moment
run ExitSettlesAllCustodyWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest, exactly 1 ProcessExit,
  exactly 1 Resolution, exactly 1 Checkpoint, exactly 8 Moment
run StaleRequestSuspendsWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest, exactly 1 SuspensionResult,
  exactly 1 Resolution, exactly 1 Checkpoint, exactly 8 Moment
run PriorOrdinaryResultLosesWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest, exactly 1 SuspensionResult,
  exactly 1 SuspensionObservation, exactly 1 OrdinaryResult,
  exactly 1 Resolution, exactly 1 Checkpoint, exactly 8 Moment
run ConflictingResultsForOneRequestWitness for 8 but exactly 1 Run,
  exactly 1 Invocation, exactly 1 ForceFence, exactly 1 SuspensionRequest,
  exactly 1 SuspensionObservation, exactly 2 SuspensionResult,
  exactly 1 Resolution, exactly 1 Checkpoint, exactly 8 Moment
run DuplicateReceiptWitness for 8 but exactly 1 Run, exactly 1 Invocation,
  exactly 1 ForceFence, exactly 1 SuspensionRequest,
  exactly 1 SuspensionObservation, exactly 1 SuspensionResult,
  exactly 2 SuspensionReceipt, exactly 1 Resolution, exactly 1 Checkpoint,
  exactly 8 Moment
run CrossInvocationCommandResultWitness for 8 but exactly 2 Run,
  exactly 2 Invocation, exactly 2 ForceFence, exactly 2 SuspensionRequest,
  exactly 2 SuspensionObservation, exactly 1 SuspensionResult,
  exactly 1 SuspensionReceipt, exactly 1 SuspensionCommandResult,
  exactly 2 Resolution, exactly 2 Checkpoint, exactly 8 Moment
