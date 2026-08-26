# Log — Post-Fan-In Retry Matrix Contract Sprint 1

## 2026-08-25 — Pre-sprint review

- Read the API-provided background and inspected the current lifecycle selector,
  local dependency projection, strict lifecycle validators, and installed
  provider-pending qualification.
- Confirmed that the current qualification ends after initial 4+2 fan-in and first
  external-authority selection.
- Identified the leading contract gap: `ordinary_resume` is supported by generic
  status-derived dependencies rather than a concrete public executable-work
  inventory.
- Drafted the sliced plan, failure matrix, compatibility posture, and open decisions.
- No runtime, schema, fixture, test, retained-run, provider, or release action has
  begun.

## 2026-08-25 — Plan approved

- Owner/API approved Slice 0.
- Froze the rule that `local_work_inventory` requires a new lifecycle version;
  lifecycle v0.5 remains closed, immutable, and readable.
- Froze the progress rule: an advertised ordinary operation must advance the
  checkpoint/basis or produce a different typed disposition. Repeating the same
  eligible ordinary-resume decision on the same basis is an explicit failure.

Current gate: Slice 0 characterization before schema freeze.

## 2026-08-25 — Slice 0 complete

- Added a provider-free production-shaped exact/bounded post-fan-in fixture.
- Reproduced completed retry #1 masking prepared retry #2 behind
  `ordinary_resume`.
- Proved that ingesting retry #1 to `REPORTED` exposes the exact retry-#2 authority
  inventory.
- Proved pending retry precedence and identity-less submission review remain
  fail-closed.
- Exercised the real `SpendController` pre-provider boundary and proved a
  providerless refusal may be followed by a republished revision with the same
  semantic ordinary-resume decision and no consumed local work.
- Inventoried the v1 qualification surface and recommended a new closed v2 while
  retaining v1 history.
- Focused tests: 4 passed. Provider/network/spend/retained-QA activity: zero.

Current gate: owner/API review before Slice 1 schema freeze.

## 2026-08-25 — Slice 1 contract proposal complete

- Preserved released native lifecycle v0.5 and temporal lifecycle v0.6 unchanged.
- Added proposed lifecycle v0.7, whose immutable checkpoint basis carries one
  exact local-work inventory.
- Added the strict `astrowoof.local_work_inventory.v1` JSON Schema, builder,
  validator, lifecycle join validator, and schema reader.
- Added lifecycle v0.7 builder/validator/schema reader and temporal-contracts v2
  structural schema.
- Froze a three-operation durable-checkpoint vocabulary and a combined fan-in /
  retry-evaluation operation for the currently observed native boundary.
- Enforced nonempty local inventory for ordinary resume and empty inventory for
  every non-local branch.
- Enforced successor basis advancement and prior operation-ID non-reuse.
- Added one sanitized, digest-valid exchanged inventory fixture.
- Exported the proposal builders/readers/validators through the package root.
- Focused Slice 0–1 tests: 9 passed, 1 optional-schema skip; public import smoke
  passed; diff check clean.
- No production selector/runtime integration, provider, spend, or retained-QA
  activity occurred.

Current gate: owner/API approval before Slice 2 runtime implementation.

## 2026-08-25 — Slice 1 semantic-identity correction

- API review identified that basis-derived `operation_id` alone could rename the
  same semantic work after a no-op republish.
- Added basis-independent `operation_key` derived from kind/route/stage/source
  lineage/reason.
- Added digest-bound `consumed_operation_keys` successor evidence.
- Tightened progress validation: an ordinary successor must consume a prior key;
  changing only snapshot/revision/operation ID fails.
- Added direct regressions for renamed no-op work, missing consumption evidence,
  valid consumption followed by new local work, and malformed semantic identities.
- Slice 1 focused result: 7 passed, 1 optional-schema skip.

Current gate remains owner/API approval before Slice 2 runtime implementation.

## 2026-08-25 — Slice 4 source qualification complete

- Preserved the historical provider-pending v1 runner/command and receipt.
- Added the closed `astrowoof.provider_pending_lifecycle_qualification.v2`
  receipt, strict Python validator, packaged schema reader, and provider-free
  `astrowoof-provider-pending-qa-v2` command.
- V2 composes the complete v1 six-create/4+2 proof with exact and bounded
  post-fan-in workspaces reopened through the public v0.7 CLI in fresh processes.
- Proved durable local-operation consumption, retry-2 authority selection, no
  post-fan-in provider I/O, and no quiescent ordinary-resume replay.
- Qualification exposed an already-consumed-operation replay edge. Tightened the
  writer-fenced commit path to refuse a prior semantic key already present in
  durable cumulative history before any mutation.
- Focused combined result: 22 tests, 21 passed and 1 expected optional-schema skip.

Current gate: build an isolated wheel and invoke the packaged v2 command.

## 2026-08-25 — Slice 4 installed gate and Slice 5 handoff complete

- Built a wheel from the current source and installed it into a fresh Python 3.11
  virtual environment.
- Invoked the installed `astrowoof-provider-pending-qa-v2` console command.
- Closed receipt status: `pass`; receipt SHA-256
  `24ebfbc47d4f46966c473ba8e46377115849b7441617348c0522638dd04ca43b`.
- Recorded explicit API mappings for ordinary resume, reconciliation, external
  authority, and terminal/review branches.
- Documented that v0.5/v0.6 remain historical/readable but intentionally fail
  closed for concrete local work; API must adopt v0.7 before routing it.
- No external network, real provider work, spend, credentials, or retained QA
  access occurred.

Current gate: final owner/API review before version bump, deterministic release
builds, tag, or publication.

## 2026-08-25 — Slice 2 truthful runtime selection complete

- Added a real workspace reader that derives v0.7 local-work inventory from the
  validated v0.5 lifecycle and native ledger state.
- Completed retry evidence now selects one route-bound
  `provider_result_fan_in_and_retry_evaluation` operation with exact source action
  lineage; pending provider custody selects no local work.
- Added writer-fenced progress commitment. It revalidates the snapshot, refuses
  unchanged/reappearing semantic work without mutation, and persists cumulative
  consumed keys only after native truth advances.
- Proved exact and bounded completed-retry → consumed fan-in → exact retry-#2
  authority selection. The prepared retry remains providerless and unmodified.
- Added failure-isolated, redacted typed selection/consumption events and aligned
  the packaged event catalog/schema.
- Focused Slice 0–2 result: 16 passed, 1 optional-schema skip. Broader lifecycle,
  contract, and event result: 54 passed, 1 optional-schema skip.
- External provider calls/retrievals/spend and retained QA access: zero.

Current gate: Slice 2 complete; proceed to the provider-free Slice 3 matrix.

## 2026-08-25 — Slice 3 provider-free retry matrix complete

- Published the closed A–H matrix fixture and consumer handoff.
- Covered exact and bounded interactive no-retry, authority, pending custody,
  completed fan-in, exhaustion, native authorization, and ambiguity states.
- Covered provider reconciliation both before and after `resume_not_before`.
- Corrected v0.7 so a released status-only ordinary branch with no constructible
  operation becomes an explicit terminal or review disposition.
- Corrected native `AUTHORIZED`/providerless state to remain non-dispatching and
  require its exact constrained executor.
- Preserved PREPARED external authority, provider-custody precedence, ambiguity,
  and route-specific Batch authority.
- Matrix result: 3 tests passed with route/case subtests; combined Slice 0–3 and
  lifecycle/event suite: 58 tests, 57 passed and 1 optional-schema skip.
- Provider/network/spend/retained-QA activity: zero.

Current gate: voof-paws 3 API review before Slice 4 packaging.

## 2026-08-25 — Production-path integration correction

- API review correctly found that the first Slice 2/3 implementation was reachable
  only through direct helpers/tests and therefore could not change QA scheduling.
- Added public `astrowoof-lifecycle ... inspect-local-work` v0.7 inspection.
- Preserved v0.5/v0.6 shapes. Their public CLI/temporal readers now fail closed with
  `local_work_contract_upgrade_required` rather than advertise an inventory-less
  `ordinary_resume`.
- Added normal exact semantic-closure checkpoint integration. On success or a spend
  boundary, it seals progress only after the underlying native mutation is durable.
- Added the equivalent bounded resume checkpoint hook; reconciliation-only and
  initial/external-authority paths remain outside local execution.
- Added a public CLI/runtime regression: read v0.7 → invoke normal `--resume` →
  perform real native fan-in mutation → detach at retry #2 authority → verify
  cumulative consumption and no provider identity/create.
- Focused Slice 0–3/lifecycle/event result after integration: 59 tests, 58 passed
  and 1 optional-schema skip.
- Bounded lifecycle resume regression subset: 5 passed.

Current gate: renewed API review before Slice 4 packaging.

## 2026-08-25 — Slice 1 cumulative-consumption hardening

- API review identified that immediate-predecessor consumption alone could permit
  a semantic operation consumed two checkpoints earlier to reappear later.
- Made `consumed_operation_keys` cumulative and append-only across successors.
- Forbid any currently advertised `operation_key` from appearing in the cumulative
  consumed set.
- Added a three-checkpoint regression covering dropped consumption history and
  attempted resurrection of previously consumed work.
- Slice 1 focused result: 8 passed, 1 optional-schema skip; combined Slice 0–1
  result: 12 passed, 1 optional-schema skip.

Current gate remains owner/API approval before Slice 2 runtime implementation.
