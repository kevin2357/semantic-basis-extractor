module native_authority_continuation_counterfactual_v1

// Counterfactual Model B: exact external authority at the provider-create boundary.
//
// Inventory atoms abstract the complete ordered public action/binding projection:
// equality means the same exact inventory. They are not hashes, prompts, payloads,
// or a model of provider behavior. A ProviderCreate is the only externally visible
// effect represented here.

sig Run {}

abstract sig InventoryKind {}
one sig InitialWave, Retry extends InventoryKind {}

sig Inventory {
  owner: one Run,
  kind: one InventoryKind
}

sig PriorInitialLineage {
  owner: one Run,
  inventory: one Inventory
}

sig ExactReusableInitialInventory {
  owner: one Run,
  inventory: one Inventory
}

sig Request {
  owner: one Run,
  inventory: one Inventory
}

sig Grant {
  owner: one Run,
  request: one Request
}

sig Dispatch {
  owner: one Run,
  request: one Request,
  grant: one Grant,
  inventory: one Inventory
}

sig Intent {
  owner: one Run,
  inventory: one Inventory,
  dispatch: one Dispatch
}

sig ProviderIdentity {
  intent: one Intent
}

sig ProviderCreate {
  owner: one Run,
  inventory: one Inventory,
  uses: lone Dispatch
}

sig TerminalReview {
  owner: one Run
}

fact PublicIdentityJoins {
  all p: PriorInitialLineage | p.inventory.owner = p.owner and p.inventory.kind = InitialWave
  all e: ExactReusableInitialInventory | e.inventory.owner = e.owner and e.inventory.kind = InitialWave
  all q: Request | q.inventory.owner = q.owner
  all g: Grant | g.request.owner = g.owner
  all d: Dispatch |
    d.request.owner = d.owner and
    d.grant.owner = d.owner and
    d.grant.request = d.request and
    d.inventory = d.request.inventory
  all i: Intent |
    i.inventory.owner = i.owner and
    i.dispatch.owner = i.owner and
    i.dispatch.inventory = i.inventory
  all p: ProviderIdentity | p.intent.owner in Run
  all c: ProviderCreate |
    c.inventory.owner = c.owner and
    (some c.uses implies c.uses.owner = c.owner and c.uses.inventory = c.inventory)
}

// Historical permissive shapes. They intentionally permit a create with no exact
// dispatch so the Analyzer can exhibit each missing boundary as a minimal witness.

pred LegacyRetainedInitialWaveReanimation {
  some lineage: PriorInitialLineage |
    (no exact: ExactReusableInitialInventory | exact.owner = lineage.owner) and
    (some c: ProviderCreate |
      c.owner = lineage.owner and c.inventory.kind = InitialWave
    )
}

pred LegacyRetryWithoutExactDispatch {
  some g: Grant |
    some c: ProviderCreate |
      c.owner = g.owner and
      c.inventory.kind = Retry and
      no c.uses
}

pred LegacyAmbiguousIntentRecreates {
  some i: Intent |
    (no p: ProviderIdentity | p.intent = i) and
    (some c: ProviderCreate |
      c.owner = i.owner and c.inventory = i.inventory
    )
}

pred LegacyReviewReopensAuthority {
  some review: TerminalReview |
    some c: ProviderCreate | c.owner = review.owner
}

// Corrected boundary. A create consumes exactly one matching request/grant/dispatch
// relation; a dispatch can support at most one create. The lineage, ambiguity, and
// terminal-review rules close the historical ways of manufacturing a continuation.

pred CorrectedBoundary {
  all c: ProviderCreate | one c.uses
  all d: Dispatch | lone d.~uses

  all lineage: PriorInitialLineage | (
    (no exact: ExactReusableInitialInventory | exact.owner = lineage.owner)
    implies (no c: ProviderCreate |
      c.owner = lineage.owner and c.inventory.kind = InitialWave
    )
  )

  all i: Intent | (
    (no p: ProviderIdentity | p.intent = i)
    implies (no c: ProviderCreate |
      c.owner = i.owner and c.inventory = i.inventory
    )
  )

  all review: TerminalReview | no c: ProviderCreate | c.owner = review.owner
}

pred ValidInitialAdmission {
  CorrectedBoundary
  some c: ProviderCreate |
    c.inventory.kind = InitialWave and
    (no lineage: PriorInitialLineage | lineage.owner = c.owner)
}

pred ValidAuthorizedRetry {
  CorrectedBoundary
  some lineage: PriorInitialLineage |
    some c: ProviderCreate |
      c.owner = lineage.owner and
      c.inventory.kind = Retry and
      one c.uses
}

pred ValidAmbiguityRetention {
  CorrectedBoundary
  some i: Intent |
    (no p: ProviderIdentity | p.intent = i) and
    (no c: ProviderCreate | c.owner = i.owner and c.inventory = i.inventory)
}

assert RetainedUnjoinableInitialWaveCannotCreate {
  CorrectedBoundary implies
    all lineage: PriorInitialLineage | (
      (no exact: ExactReusableInitialInventory | exact.owner = lineage.owner)
      implies (no c: ProviderCreate |
        c.owner = lineage.owner and c.inventory.kind = InitialWave
      )
    )
}

assert ProviderCreateNeedsExactDispatch {
  CorrectedBoundary implies all c: ProviderCreate | one c.uses
}

assert DispatchCannotCreateTwice {
  CorrectedBoundary implies all d: Dispatch | lone d.~uses
}

assert AmbiguousIntentCannotCreateAgain {
  CorrectedBoundary implies
    all i: Intent | (
      (no p: ProviderIdentity | p.intent = i)
      implies (no c: ProviderCreate |
        c.owner = i.owner and c.inventory = i.inventory
      )
    )
}

assert TerminalReviewCannotCreate {
  CorrectedBoundary implies
    all review: TerminalReview | no c: ProviderCreate | c.owner = review.owner
}

run LegacyRetainedInitialWaveReanimation for exactly 1 Run, exactly 2 Inventory,
  exactly 1 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 0 Request, exactly 0 Grant, exactly 0 Dispatch, exactly 0 Intent,
  exactly 0 ProviderIdentity, exactly 1 ProviderCreate, exactly 0 TerminalReview

run LegacyRetryWithoutExactDispatch for exactly 1 Run, exactly 1 Inventory,
  exactly 0 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 1 Request, exactly 1 Grant, exactly 0 Dispatch, exactly 0 Intent,
  exactly 0 ProviderIdentity, exactly 1 ProviderCreate, exactly 0 TerminalReview

run LegacyAmbiguousIntentRecreates for exactly 1 Run, exactly 1 Inventory,
  exactly 0 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 1 Request, exactly 1 Grant, exactly 1 Dispatch, exactly 1 Intent,
  exactly 0 ProviderIdentity, exactly 1 ProviderCreate, exactly 0 TerminalReview

run LegacyReviewReopensAuthority for exactly 1 Run, exactly 1 Inventory,
  exactly 0 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 0 Request, exactly 0 Grant, exactly 0 Dispatch, exactly 0 Intent,
  exactly 0 ProviderIdentity, exactly 1 ProviderCreate, exactly 1 TerminalReview

run ValidInitialAdmission for exactly 1 Run, exactly 1 Inventory,
  exactly 0 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 1 Request, exactly 1 Grant, exactly 1 Dispatch, exactly 0 Intent,
  exactly 0 ProviderIdentity, exactly 1 ProviderCreate, exactly 0 TerminalReview

run ValidAuthorizedRetry for exactly 1 Run, exactly 2 Inventory,
  exactly 1 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 1 Request, exactly 1 Grant, exactly 1 Dispatch, exactly 0 Intent,
  exactly 0 ProviderIdentity, exactly 1 ProviderCreate, exactly 0 TerminalReview

run ValidAmbiguityRetention for exactly 1 Run, exactly 1 Inventory,
  exactly 0 PriorInitialLineage, exactly 0 ExactReusableInitialInventory,
  exactly 1 Request, exactly 1 Grant, exactly 1 Dispatch, exactly 1 Intent,
  exactly 0 ProviderIdentity, exactly 0 ProviderCreate, exactly 0 TerminalReview

check RetainedUnjoinableInitialWaveCannotCreate for 4
check ProviderCreateNeedsExactDispatch for 4
check DispatchCannotCreateTwice for 4
check AmbiguousIntentCannotCreateAgain for 4
check TerminalReviewCannotCreate for 4
