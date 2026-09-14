# Plan — Didot / Erasmus Terminal Observation Handoff Investigation

## Working classification

The paired absence of observer logs is one symptom with two different native
handoff histories.

- Didot: SBE emitted an exact terminal-delivery command for result
  `nres_fd73a016721dcf725d6a5449`. API's first publication attempt was rejected
  and scheduled one retry. The retry entered `delivery_validation`, published
  successfully, but its cycle result carried no sealed result ID; the observer
  guard therefore skipped. This is provisionally an API retry-lineage handoff
  loss, not missing native evidence.
- Erasmus: SBE emitted an invocation-bound terminal-review command for result
  `nres_68c273587d4363fe3d150cb9`. The first API terminal close should reach the
  observer under current source, yet no completion or failure log exists. A
  later `sealed_terminal_preflight` can authenticate the sealed result but does
  not recreate the original command handoff; current API code consequently
  skips ordinary-review observation on that later path. The first-close runtime
  behavior and the unexpected second claim remain unclassified.

Do not combine these into a generic "find the latest terminal result" repair.
Delivery and review retain their distinct authority contracts.

## Slice 0 — Freeze exact paired timelines and transport inventory

**Status: authorized.** API approved investigation through Slice 2.

- Reduce the three unfiltered worker exports into ordered, hashable timeline
  evidence for the two API run IDs, job IDs, and native run IDs.
- Record the exact Didot delivery result/receipt/invocation and exact Erasmus
  review result/receipt/invocation.
- Map each SBE JSONL command envelope through API parsing, cycle projection,
  terminal ingress, publication or closeout, observer eligibility, queue
  disposition, and lease release.
- Distinguish the first Erasmus reconciliation close from its later
  sealed-terminal-preflight close; record attempt and lease identities rather
  than treating duplicate outcome lines as one event.
- Confirm from source that SBE emitted both typed handoffs and identify every
  point where API retained, discarded, or could not lawfully recreate them.

**Exit:** one evidence table for each route with no inferred identity and an
explicit first-loss boundary.

## Slice 1 — Faithful provider-free API route reproduction

Use checked-in SBE fixtures or sealed synthetic publications only; perform no
provider, Better Stack, R2, retained-workspace, or live QA operation.

Reproduce three separate paths:

1. Didot: terminal delivery with exact result authority, publication
   eligibility failure, retry, then successful `delivery_validation`.
2. Erasmus A: reconciliation returns the exact terminal-review command and
   closes normally.
3. Erasmus B: a successor claim enters `sealed_terminal_preflight` with only
   the exact sealed result ID for `review_required`.

For each path, capture:

- `SbeCycleResult` fields at the worker boundary;
- terminal-ingress disposition and persisted native receipt;
- observer call count, arguments, return/failure branch, and log emission;
- queue state, retryability, attempt/lease lineage, capacity release, and
  workspace cleanup ordering.

The Erasmus A fixture must use the production constructor and logging setup,
not inject a shortcut worker or call `_observe_editorial_terminal()` directly.
Each reproduction must independently record function entry with a recording
observer; an ordinary logger line is not sufficient proof. The Didot case must
also prove the retry cannot cross-bind another job, native run, or newer result.

**Exit:** provider-free tests either reproduce each missing observer call or
prove a deployment/configuration/telemetry difference from current source.

## Slice 2 — Deployed-runtime and claim-lineage reconciliation

**Status: authorized if its entry condition is met.**

Run this slice only if Erasmus A passes locally or if the second claim remains
unexplained.

- Bind the QA rollout image/profile to its exact API commit and SBE wheel
  digest using already-retained rollout evidence; do not redeploy.
- Compare that source to the current observer call site and logger
  initialization.
- Determine why the same Erasmus job produced a normal non-retryable terminal
  close and then a later sealed-preflight close. Check for duplicate queue
  records, explicit recovery selection, transaction rollback, or overlapping
  claims using existing database/log evidence only if separately authorized.
- Establish whether the absent first-close observer line means the call was
  skipped, the call ran but its logger was filtered, or the relevant transaction
  never committed.

**Exit:** Erasmus is classified as code-path omission, deployed-version skew,
claim-lineage defect, or telemetry-only loss. No live mutation is required.

## Slice 3 — Narrow contract and ownership decision

- Didot: define an exact API-owned carry-forward for the already-ingested
  delivery result across publication retry. It must remain bound to the same
  native run/job and must not use latest-result discovery.
- Erasmus: preserve the stricter invocation-bound review command contract.
  Decide whether observation must occur exactly during the first command-bearing
  close or whether API may persist that validated command as durable observation
  authority for a later preflight. Do not derive it from generic terminal state.
- Preserve post-authoritative, best-effort semantics: observer success or
  failure cannot change publication, terminal closeout, custody, queue state,
  capacity, spend, or cleanup.
- Assign each correction to API or SBE only where the first-loss boundary
  proves ownership. Current evidence does not justify an SBE schema bump.
- Check Alloy impact explicitly. A pure observer/retry handoff repair should not
  change lifecycle semantics; any queue-claim or durable-authority change must
  be assessed against the model.

**Exit:** joint review approves the minimal correction and its cross-package
fixtures before implementation.

## Slice 4 — Implementation and qualification proposal

Implementation is not authorized by this opening plan. If Slice 3 is approved,
the implementation slice should include:

- production-path regressions for all three Slice 1 routes;
- exact identity, duplicate, missing, conflicting, and wrong-native-run
  fail-closed cases;
- observer exception/non-2xx/disabled branches proving terminal outcomes stay
  unchanged;
- a paired installed SBE-wheel/API consumer gate if any native package surface
  changes; otherwise an API-only rollout gate;
- manifest registration for every new SBE test module.

Stop at the Slice 3 joint-review gate before changing runtime code, packaging,
deployment, or live state.

## Investigation boundaries

- No retained-workspace read, R2 access, provider call, Better Stack write,
  replay, recovery, resubmission, deployment, queue mutation, or lifecycle
  mutation is authorized.
- Logs and observer artifacts are evidence only, never lifecycle authority.
- Do not invent or discover a latest result to compensate for a missing exact
  handoff.
- Preserve the unrelated untracked historical-recovery sprint.
