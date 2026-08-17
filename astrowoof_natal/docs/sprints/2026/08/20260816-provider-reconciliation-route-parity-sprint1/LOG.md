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
