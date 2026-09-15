# Plan

## Status and authority

**Slice 0 complete; paused at Voof-paws A.** This sprint is provider-free by
default and authorizes no live QA/R2/API mutation, provider call, process kill,
service restart, capacity release, package publication, or deployment.

The prior `20260910-operator-quarantiner-native-suspension-sprint1` is closed
around its released relocated-assessment scope. This plan is the sole active
home for prospective native cooperative suspension.

## Slice 0 — Native source and safe-point inventory

- Map direct authoring, ordinary resume, v2 dispatch/reconciliation, bounded,
  and Batch coordinator loops that may own active native mutation.
- Inventory provider call-entry, provider-ID persistence, retrieval, adoption,
  local fan-in, optional-stage mutation, checkpoint/result publication, and
  successor-selection seams.
- Identify which seams already serialize state mutation and can host a bounded
  cooperative request check.
- Inventory CLI/subprocess exit and exact result/receipt handoff behavior.
- Prove current SBE has no hidden API polling, signal-to-checkpoint shortcut, or
  relocated-workspace execution route.
- Record unsupported/unbounded regions explicitly rather than promising prompt
  interruption inside arbitrary writes or provider SDK calls.

**Exit:** a source-linked matrix names each safe point, evidence available
there, maximum bounded deferral where knowable, and truthful result class.

**Result:** recorded in
`SLICE 0 - NATIVE SAFE-POINT AND PROVIDER-BOUNDARY INVENTORY.md`. Exact
interactive ordinary-v2 dispatch and response reconciliation are the strongest
first implementation cells; initial-wave fan-out, bounded, legacy direct, and
Batch require separate contract/qualification decisions.

**Voof-paws A:** API/SBE review of the inventory before contract field names
freeze.

## Slice 1 — Gate B request, channel, and result contract

### 1A — Pre-launch invocation envelope

Freeze the canonical identity created by API before launch: random invocation
ID and generation, run/job/attempt/lease/native-run bindings, worker boot
identity, command digest, request-isolated control identity, timestamps, and
grace deadline. Define exact post-launch PID/start-marker/process-group evidence
as API-owned observations, not SBE authority.

### 1B — Capability-limited control channel

Choose and specify the launch-bound channel. Define atomic request publication,
freshness, idempotency, acknowledgement, duplicate/conflict behavior, parent
crash, child restart, stale channel, and relocated-copy refusal. Prohibit
credentials, provider payloads, arbitrary commands, and generalized workspace
authority.

### 1C — Native request/result pair

Define additive closed schemas and readers for an exact cooperative suspension
request and result. Outcomes must distinguish at least:

- `suspended_checkpointed`;
- `suspended_quiescent_no_checkpoint_change`;
- `suspension_deferred`;
- `suspension_refused`;
- `provider_boundary_ambiguous`; and
- `checkpoint_publication_ambiguous`.

Bind the result to the exact request, invocation, logical workspace,
checkpoint lineage, custody inventory, provider boundary, local-work posture,
and publication receipt. Exclude claims about process death, API lease/capacity,
provider cancellation, spend release, or terminal settlement.

### 1D — Precedence and append-only resolution

- Preserve an ordinary committed result when it precedes stop observation.
- Make request, native result, process observation, and later resolution an
  immutable predecessor/successor chain.
- Define how API selects an exact same-invocation result without generic latest
  discovery.
- Keep typed API `force_fenced` authority loss distinct from every native
  suspension outcome.

### 1E — Resource-specific join table

For each outcome and missing/stale/contradictory evidence case, state whether
API may release only worker execution, retain the run allocation, and retain
provider/spend/workspace/native custody. SBE supplies facts, never the API
release decision.

**Exit:** complete prose contract, schemas/projections proposal, race table, and
provider-free fixture plan.

**Voof-paws B / joint Gate B:** mandatory API/SBE/owner review. No runtime
implementation before approval.

## Slice 2 — Provider-free contract fixtures and readers

- Implement schemas, canonical builders/readers, and privacy-bounded fixtures.
- Cover exact, stale invocation, wrong run/checkpoint/worker boot, expired,
  duplicate, conflicting, and digest-corrupt requests.
- Cover every outcome and ordinary-result-precedence race.
- Prove append-only continuity and reject a recomputed-digest semantic mutation.
- Prove the channel/request grants no relocated assessment, execution, provider,
  publication, or generic filesystem capability.
- Package full public documents so API never reconstructs native joins.

**Exit:** focused contract suite and API-consumable fixture bundle pass with
zero provider/network/spend activity.

**Voof-paws C:** API review of the packaged contract before coordinator changes.

## Slice 3 — Cooperative safe-point integration

- Add request observation only at approved shared coordinator safe points.
- Serialize observation with native mutation and custody transitions.
- Publish checkpoint plus exact result/receipt before cooperative exit when
  truthfully possible.
- Preserve provider-entry and checkpoint-publication ambiguity rather than
  retrying or synthesizing identity.
- Keep ordinary committed results dominant.
- Ensure duplicate request/restart/replay is inert and identity exact.
- Do not add OS hard-kill ownership to SBE.

**Exit:** production-boundary provider-free tests cover direct, ordinary v2,
bounded, and Batch routes only where Slice 0 proved support; exclusions remain
explicit.

**Voof-paws D:** runtime review before packaging.

## Slice 4 — Cross-package supervision qualification

- Exercise the installed SBE CLI from API's real subprocess adapter and
  launch-envelope/control-channel shape.
- Cover cooperative exit, deferred observation, exact process exit without a
  native result, parent crash, child restart, PID reuse simulation, stale
  channel, request replay, and unrelated-run isolation.
- Prove authority revocation is distinct from worker execution reclamation.
- Prove exact child death may release only API-owned execution capacity while
  semantic/provider custody stays held.
- Prove neither fence alone, process death alone, assessment alone, nor native
  suspension result alone grants complete release.
- Record installed SBE/API version and wheel identity in receipts.

**Exit:** joined provider-free qualification passes with zero provider calls,
spend, R2 access, live process termination, or unrelated mutation.

## Slice 5 — Release and operational handoff

- Select regression depth using the release playbook after final diff review.
- Build reproducibly from an exact release-lock commit and run installed-wheel
  qualifications.
- Document deployment compatibility, unsupported routes, diagnostics,
  retention holds, and named later-resolution operations.
- Pause for explicit owner approval before commit/tag/publication if a package
  release is warranted.

**Exit:** immutable release/handoff evidence is complete, or the sprint closes
honestly without a release if no SBE runtime change is needed.
