# Provider Reconciliation Route Parity Sprint 1 Log

2026-08-16

- Kevin approved planning for the routes omitted from SBE 0.4.3 provider-pending
  reconciliation: exact-Natal Batch and bounded-Natal interactive.
- Kevin approved explicit deferral of bounded-Natal Batch.
- Reviewed the 0.4.3 reconciliation engine, lifecycle projection, exact Batch
  round/File/Batch persistence, bounded interactive route-local resume, sprint
  conventions, and the prior provider-pending sprint's route classification.
- Drafted an eight-slice contract-first sprint with a required API review gate,
  route-specific provider adapters, failure-injection coverage, mixed-route
  fresh-worker qualification, and Windows/Linux installed-wheel gates.
- No implementation, test mutation, provider operation, build, version bump,
  commit, tag, or release has begun. Status remains proposed for Kevin review.
- Kevin approved the plan. Committed and pushed the planning package as `e977163`;
  Slice 0 began.
- The system drive was at zero free bytes during the first commit attempt. Removed
  only the ignored, reproducible repository `build/` directory and the prior
  sprint's generated `C:/tmp/astrowoof-natal-pipeline-sprint6` qualification tree;
  committed compact evidence from that completed sprint remains in Git.
- Traced exact Batch round preparation, File upload, Batch creation, detach,
  retrieval, output/error download, member ingestion, and retry continuation.
- Traced bounded interactive paid-action creation, Response identity persistence,
  route-local resume, validation, optional stages, delivery, and snapshot order.
- Added provider-free baselines that inspect complete snapshots without mutation,
  freeze exact Batch's intentional 0.4.3 `unsupported_retain_capacity`
  classification, and prove both routes resume their durable provider identity
  without a replacement submission.
- The first focused run found a real bounded classification defect. Production
  bounded runs share `astrowoof.semantic_closure_run.v0.9` and distinguish their
  route through `route_contract`, while the capacity predicate checks only the
  shared schema. Bounded interactive therefore inherits exact scheduling
  eligibility before a bounded adapter exists. The older negative test used a
  synthetic bounded `schema_version` that production does not emit.
- Recorded the discrepancy without changing runtime behavior in Slice 0 and made
  explicit route-contract binding a prerequisite for the parity dispatcher.
- Focused provider-free coverage passed all 6 tests in 6.237 seconds. It includes
  bounded-Batch construction rejection, exact Batch inspection and same-ID
  retrieval, and bounded interrupted-submission inspection and same-ID resume.
- The complete repository suite passed all 339 tests in 141.686 seconds.
- Slice 0 is complete and paused for review. No production runtime, public
  contract, provider operation, build, version bump, release, or tag changed.
- Kevin approved Slice 0. Committed and pushed it as `df75c2e`; Slice 1 began.
- Corrected a planning assumption from the implementation inventory: one exact
  Batch round is one paid SBE action/authorization containing several `custom_id`
  request members, not several independently authorized paid actions.
- Drafted the route-parity contract proposal. It retains inspection v0.2, proposes
  policy/cycle-result v0.2 with route/mechanism summaries, freezes distinct
  Responses and Batch timing limits, binds real bounded `route_contract`, keeps
  bounded Batch deferred, and defines atomic Batch output preflight.
- Defined one neutral public reconciliation dispatcher/CLI mode, with the current
  exact-only spelling retained temporarily as a compatibility alias.
- Chose fail-closed handling for timing-free 0.4.3 Batch workspaces rather than
  inventing a historical identity timestamp. Existing valid bounded timing can be
  admitted only through the new bounded route adapter.
- Clarified that bounded delivery currently follows enabled optional stages; this
  sprint will not invent exact Natal's nonblocking post-delivery critic state for
  the bounded pipeline.
- Per the plan's learning-checkpoint rule, deferred strict encoding of the new
  examples until after API review. The Slice 0 route-identity discovery materially
  affects schema shape, and the same gate prohibits runtime/schema implementation
  before approval.
- Current lifecycle contract, provider-pending, bounded provider, and bounded
  lifecycle regressions passed all 58 tests in 17.575 seconds.
- The complete repository suite passed all 339 tests in 142.210 seconds.
- Slice 1 is paused at the required Kevin/API-agent review gate. No production
  runtime, packaged schema, provider operation, build, version bump, release, or
  tag changed.
- The API approved the overall Slice 1 direction and required two corrections:
  strict native route/mechanism identity in lifecycle inspection, and a
  machine-distinguishable terminal Batch usage-unavailable disposition rather
  than estimated zero settlement.
- Revised the proposal to inspection v0.3 with top-level native route identity,
  per-action provider kind and native operation/round binding, and a separate
  consumer-authority projection. Provider retrieval custody may now end while
  financial authority remains retained for billing reconciliation.
- Added four closed cost dispositions. Terminal Batch usage absence is represented
  as `provider_usage_unavailable_billing_reconciliation_pending`, with no fabricated
  usage or amount; `no_provider_work_consumed` is forbidden once a Batch ID exists.
- Runtime and strict packaged schema work remain paused pending Kevin acceptance
  and API confirmation of the revised contract.
- The API approved all seven revised contract questions. Clarified the final
  distinction between unresolved provider identity/File retrieval, which retains
  provider custody, and integrity review after terminal provider bytes are already
  durable, which retains consumer authority without further polling.
- Slice 1 is approved and ready to commit. Provider operations remain 0 and paid
  spend remains `$0`.
