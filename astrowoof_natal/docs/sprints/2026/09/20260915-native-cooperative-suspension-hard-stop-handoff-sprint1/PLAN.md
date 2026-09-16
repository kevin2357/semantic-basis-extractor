# Plan

## Status and authority

**Slice 4B opened; joined intake is blocked on API suspension-result
discrimination.** API Slice 3B discovered that the
original candidate incorrectly required an operator force fence before child
launch. The corrected v1 chronology binds a pre-launch supervision capability
in the immutable envelope and binds the later real operator force fence in the
suspension request. This sprint is provider-free by
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

**Voof-paws A:** approved. v1 scope is exact interactive ordinary-v2 dispatch
and response reconciliation; initial-wave fan-out and all other routes remain
fail-closed/deferred.

## Slice 1 — Gate B request, channel, and result contract

### 1A — Pre-launch invocation envelope

Freeze the canonical identity created by API before launch: random invocation
ID and generation, run/job/attempt/lease/native-run bindings, worker boot
identity, command digest, request-isolated control identity, timestamps, and
grace deadline. Define exact post-launch PID/start-marker/process-group evidence
as API-owned observations, not SBE authority.

Treat API's admission checkpoint as an anchored predecessor. Observation may
occur at the same checkpoint or an exact contiguous successor in the same
authoritative lineage; do not require observation-time equality.

### 1B — Capability-limited control channel

Choose and specify the launch-bound channel. Define atomic request publication,
freshness, idempotency, acknowledgement, duplicate/conflict behavior, parent
crash, child restart, stale channel, and relocated-copy refusal. Prohibit
credentials, provider payloads, arbitrary commands, and generalized workspace
authority.

v1 uses an atomic request-isolated control-file channel outside the executable
workspace. Bind its canonical absolute control-root identity into the pre-launch
envelope and reject relocated workspaces before request parsing.

Pass the immutable envelope-file path and control-root path through dedicated
ordered CLI arguments. Validate canonical location as well as bytes/digests.

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

**Result:** recorded in
`SLICE 1 - GATE B COOPERATIVE SUSPENSION CONTRACT.md`. It freezes the proposed
four-document identity split, atomic control-file channel, exact safe points,
ordinary-result precedence, append-only evidence chain, resource join, and
provider-free race matrix.

**Voof-paws B / joint Gate B:** mandatory API/SBE/owner review. No runtime
implementation before approval.

## Slice 1A — Shared Alloy protocol spike

**Position:** begin only after the prose Gate B contract is jointly approved;
complete before Slice 2 implementation.

SBE owns one canonical bounded Alloy model for the joined API/SBE protocol.
Do not create independent per-repository models. API reviews the shared model
against its force-fence and supervision transitions and records the exact model
commit and SHA-256 in its sprint evidence.

Model the minimum relational system needed to exercise:

- runs, jobs, attempts, leases, worker boots, supervision invocations, control
  roots, force fences, requests, native results, process observations, and
  append-only resolution successors;
- ordinary authority revocation versus exact process exit;
- provider, spend, workspace/native, worker-execution, and run-allocation
  custody as distinct facts;
- request freshness, launch generation, exact identity joins, duplicate replay,
  stale channels, and unrelated-run isolation;
- provider-call entry, durable provider identity, native publication, ordinary
  terminal/delivery publication, and suspension observation ordering; and
- supported ordinary-v2 dispatch/reconciliation versus unsupported routes.

Assert at minimum:

1. a force fence cannot be undone into ordinary authority;
2. stale or mismatched requests cannot affect a successor invocation;
3. fence, request, result, process observation, and resolution history is
   append-only and contiguous;
4. process exit alone cannot release run allocation or provider/spend/workspace/
   native custody;
5. no partial evidence combination grants complete settlement authority;
6. an ordinary terminal/delivery result committed before suspension observation
   remains dominant;
7. exact replay is inert while conflicting replay refuses; and
8. no event for one run changes another run's authority or custody.

Run bounded checks across deliberately small but nontrivial scopes and retain
every counterexample or unsat assertion receipt. Translate any counterexample
into a prose-contract correction and a provider-free implementation fixture.
Record the scope limits explicitly: Alloy does not prove filesystem atomicity,
path/reparse behavior, Python subprocess supervision, provider timing, hashes,
JSON validation, packaging, or deployed topology.

**Exit:** one reviewed `.als` source, analyzer command/version, scenario and
assertion inventory, bounded result receipt, model SHA-256, API reciprocal
review, and a mapping from each assertion/counterexample to Gate B clauses and
future provider-free tests.

**Voof-paws B2:** joint API/SBE review of the exact Alloy model and results.
No schema/reader or runtime implementation begins before this checkpoint.

**Result:** the bounded shared model is recorded in
`tools/native_cooperative_suspension_v1.als`, with stable receipt, rule mapping,
and findings in `SLICE 1A - SHARED ALLOY PROTOCOL SPIKE.md`. Four valid worlds
are satisfiable, ten assertions have no bounded counterexample, and seven
weakened rules each admit the intended bad world. The spike tightened
one-result-per-request cardinality, observation-time ordinary-result
precedence, non-branching resolution history, invocation-wide request conflict,
publication suppression after prior ordinary results, and exact receipt/output
cardinality.

## Slice 2 — Provider-free contract fixtures and readers

- Implement schemas, canonical builders/readers, and privacy-bounded fixtures.
- Derive fixtures from the approved Alloy assertions and any counterexamples;
  retain a traceability map without claiming the bounded model proves runtime
  behavior.
- Cover exact, stale invocation, wrong run/checkpoint/worker boot, expired,
  duplicate, conflicting, and digest-corrupt requests.
- Cover every outcome and ordinary-result-precedence race.
- Cover admission checkpoint C1 to safe-point successor C2, plus forked and
  non-successor lineage; exact CLI path substitution; and all deferred
  continuation modes.
- Prove append-only continuity and reject a recomputed-digest semantic mutation.
- Prove the channel/request grants no relocated assessment, execution, provider,
  publication, or generic filesystem capability.
- Package full public documents so API never reconstructs native joins.

**Exit:** focused contract suite and API-consumable fixture bundle pass with
zero provider/network/spend activity.

**Result:** closed Python readers, one complete schema family, the public
contract catalog entries, and a packaged joined fixture bundle are implemented.
Focused source and neighboring release-contract tests pass. The executable
translation also resolved the result/receipt circular-hash wording by following
the existing result-then-receipt-then-command-envelope publication pattern.

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

**Result:** exact-interactive ordinary-v2 dispatch and response reconciliation
now observe the capability-limited request only under their existing native
writer lock. Observation occurs before provider entry and after durable intent,
provider-identity, ambiguous-return, or retrieved-response checkpoints. The
request observation itself is checkpointed before immutable result, receipt,
retained evidence, and exact command-result publication. Exact restart/replay
repairs or returns the same result; a distinct request conflicts; a prior valid
ordinary result dominates. Bounded and Batch reconciliation remain explicitly
unsupported. Focused Slice 3: 11 passed. Neighboring v2/reconciliation matrix:
112 passed, 2 expected skips.

**Voof-paws D:** runtime review before packaging.

## Slice 4A — SBE packaged-candidate supervision qualification

Break the release-pair dependency cycle by qualifying SBE's packaged boundary
before API wires that exact candidate into its subprocess adapter.

- Build/install a controlled candidate wheel from the reviewed Slice 3 commit.
- Exercise the installed SBE CLI with the approved immutable
  envelope/control-root shape, without importing source-tree modules.
- Cover cooperative exit, absent request, stale/relocated control identity,
  duplicate replay, conflicting request, interruption/restart repair, prior
  ordinary-result precedence, and unrelated-run isolation where the public
  installed boundary can prove them.
- Prove the installed artifact contains all schemas, readers, fixtures, and
  public command surfaces required by API Slice 3B.
- Prove zero provider calls, spend mutation, R2 access, live process
  termination, or API resource release.
- Record the candidate wheel SHA-256, installed version, source commit, command
  lines, receipts, and explicit limits. This is candidate evidence, not release
  authorization.

**Exit:** API can bind Slice 3B to one exact packaged SBE candidate and add the
real supervision/control/result adapter without reconstructing SBE semantics.

**Superseded result:** candidate source commit `5f5d9aa6`, prospective SBE `0.4.65`, wheel
SHA-256 `6c5db7b3134805f74343b841ea50ace128c313ab8ac292196fdf483fa6b1ce6b`.
Clean installed qualification, public receipt validation, packaged JSON Schema,
and `pip check` passed with pinned SPC `0.11.1`, but API Slice 3B correctly
rejected its impossible launch chronology. This wheel is not eligible for
adapter integration, tagging, or publication. No tag/publication occurred.

**Correction gate:** rebuild the package under fresh prospective version
`0.4.66` only after the envelope/request/schema/fixture family proves the
capability-then-fence ordering provider-free. Every result, receipt, and command
result must bind both identities independently.

**Corrected result:** renewed Gate B2 approved the refreshed Alloy campaign.
Prospective `0.4.66` was built reproducibly from committed source with the
recorded epoch, installed into a clean environment, and passed its packaged
schema/fixture/public qualification boundary provider-free. API must bind only
the corrected wheel recorded in the Slice 4A result.

## API companion Slice 3B — Real adapter integration

API owns this intervening step. It creates the pre-launch supervision envelope
and request-isolated control root, passes the two dedicated SBE arguments,
consumes the exact suspension command result, joins exact child exit, and
retains all non-execution custody. SBE does not implement or simulate these API
decisions.

**Exit:** the real API subprocess adapter is available for joined qualification.

**Status:** corrected candidate ready for API intake; API must consume only the
`0.4.66` candidate and must not substitute the superseded `0.4.65` wheel.

## Slice 4B — Joined cross-package supervision qualification

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

**Current gate (2026-09-16):** API revision `e2e9d32` closes the first joined
intake blocker with a schema-discriminated public suspension reader. The real
joined subprocess then exposed a request-builder mismatch: API writes the
effective earlier fence expiry into both `expires_at` and `grace_deadline`,
while the approved v1 contract requires `grace_deadline` to repeat the
immutable envelope bound and uses only `expires_at` for the tighter effective
deadline. SBE therefore correctly refuses the request as not joining its
supervision invocation. Slice 4B remains open pending that narrow API builder
correction; neither validator should be weakened.

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
