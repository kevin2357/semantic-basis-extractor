# Completed retry duplicate-submission investigation — sprint plan

## Status

Sprint complete. SBE `0.4.30` is committed, tagged, published, downloaded, and
hash-verified. API companion ingestion remains required before the affected
legacy-generic live path may be enabled. No retained-run mutation, real
provider operation, recovery, release, deployment, or affected-worker resume
occurred.

## Objective

Determine how one exact-Natal interactive creative-retry action acquired two
different OpenAI Response identities after the first identity had already been
durably recorded and completed. Establish the exact native and API transition
sequence, identify the first violated invariant, and define a general correction
that prevents provider creation from being re-enabled by any post-provider local
failure.

The sprint begins as an evidence-led investigation. Runtime, public-contract,
recovery, and release slices are provisional until Slice 0 establishes the real
failure boundary.

## Frozen incident identity

| Field | Value |
| --- | --- |
| API run | `f84b3524-659a-4b86-83b4-7deb5b7c59a6` |
| Native run | `42407f1f4386eb0fcd387de9feb305a932d6626949dea247750f785bd1851920` |
| Native action | `paid_fb28a0c3a7e2a44743d65b8d` |
| Stage | `creative_retry` |
| First provider identity | `resp_0a83dca212896636006a93ae4a599087d0ae269439ce29c1d8` |
| Second provider identity | `resp_00ecec3e2a02b87b006a93aed2cb2887d0912ecce39fcef0a4` |
| SBE release | `0.4.29` |
| Environment | QA |

Scone Ranger (`a587c4fa00f22e57ca9b4177c58783918a2ca991cd16a562769b7a978359f8d0`)
is a comparison run, not the duplicate-submission case. It may be inspected only
if its exact evidence is separately frozen and needed to distinguish normal from
faulted behavior.

## Immediate containment

- Keep `astrowoof-qa-sbe-worker` suspended.
- Do not resume, reconcile, deny, retire, repair, delete, or republish the affected
  run.
- Do not select either provider response as canonical during investigation.
- Preserve both native provider identities and the API row disagreement as
  contradictory evidence requiring review.

## Scope

### In scope

- Read-only inspection of the exact retained QA checkpoint and its declared
  snapshot, journal, ledger, result, receipt, and lifecycle evidence.
- Read-only correlation with the exact API paid-action, authorization, invocation,
  provider-operation, lease, and command-result records supplied by the API owner.
- Sanitized worker/event-log correlation for the bounded incident window.
- Source-path analysis of creative-retry preparation, authorization consumption,
  call entry, provider-identity durability, completion, fan-in, local-work progress,
  command-result publication, and re-entry.
- Provider-free reproduction and failure injection after Slice 0 freezes the
  observed boundary.
- A general correction covering any post-provider local failure if a defect is
  proven.

### Out of scope unless a later reviewed slice adds it

- Any real provider call, GET, POST, retry, or spend.
- Mutation or recovery of the affected QA run.
- Resuming the suspended QA SBE worker.
- Choosing a canonical response or reconciling API reservations for the duplicated
  historical action.
- Editorial retry-policy, prompt, QA, cost, or attempt-limit changes.
- Batch or bounded-Natal changes unless the proven primitive is shared and parity
  work is separately justified.
- Deployment, release, or paid QA.

## Safety and authority invariants

1. One native paid-action authority may cross provider call entry at most once.
2. `CALL_ENTERED` without a durable identity is ambiguity, never replayable create
   work.
3. A durable provider identity makes the action retrieval-only; later local faults
   cannot restore create eligibility.
4. Provider completion changes only result/fan-in work. It cannot reopen provider
   submission for the same action.
5. A post-provider local-work failure may block progress, require review, or be
   retried locally, but must preserve provider custody and immutable history.
6. SBE native evidence—not an API row, lease retry, subprocess exit, or missing API
   ingestion—must independently fence duplicate provider creation.
7. API authority records must converge from sealed SBE evidence exactly once, but
   SBE does not assert API-global reservation, lease, or capacity facts.
8. No investigation conclusion may infer absence from a missing log line or action
   count alone.
9. Missing, stale, contradictory, providerless, ambiguous, pending, completed, and
   consumed are distinct states.
10. Retained evidence remains immutable throughout this sprint unless the owner
    later authorizes a separate recovery operation.

## Evidence hierarchy

Resolve disagreements without flattening them, in this order:

1. Snapshot-validated native action ledger, run state, immutable journal, sealed
   result, receipt, and command-result envelope.
2. API-owned paid-action, authorization/admission, provider-operation, invocation,
   lease, and ingestion records.
3. SBE structured events and sanitized worker logs.
4. Source-path reconstruction and provider-free reproduction.

## Slice 0 — Freeze and reconstruct the duplicate-submission boundary

### Purpose

Prove what durable native and API state existed at each provider boundary and
identify the first transition that made a completed/provider-bound action appear
create-capable again. Slice 0 is diagnostic only; it does not choose or implement a
fix.

### 0A — Freeze the evidence map

- Record exact R2 object key, object version/generation where available, size,
  ETag/checksum, archive SHA-256, snapshot generation, logical workspace root, and
  expected native run ID before download.
- Freeze the exact API export/receipt and log-window identities used for
  correlation. Hash every supplied evidence file.
- Record SBE 0.4.29 wheel/tag/source identities and the deployed worker image/profile
  identities supplied by API evidence.
- Distinguish evidence retained in the checkpoint from later event/API observations.
  Do not write later facts into an earlier snapshot timeline.

### 0B — Bounded read-only workspace inspection

- Use exact object `HEAD`/metadata read and exact object `GET`; do not list the
  bucket or discover neighboring workspaces.
- Download into a fresh temporary directory outside the repository.
- Validate archive checksum, safe paths, logical-root identity, complete snapshot
  inventory, member hashes, receipt namespace, and journal/result joins before
  interpreting state.
- Read only the minimum declared members needed to answer the investigation:
  `run.json`, snapshot/inventory metadata, action ledger, native journal, result
  index/results/receipts, lifecycle/public command results, retry/pass lineage,
  authorization/consumption records, and provider identity/status evidence.
- Do not read prompts, authored card text, provider payload bodies, credentials, or
  unrelated subject artifacts unless a digest-only join is impossible and a
  separate review explicitly authorizes it.
- Produce an access receipt listing exact object/member hashes and proving zero
  writes, provider operations, recovery commands, or workspace mutation.
- Remove temporary credentials and downloaded protected bytes after the sanitized
  evidence products and hashes are verified.

### 0C — Reconstruct the native transition timeline

For `paid_fb28…`, join and order:

- logical pass/attempt identity, complete binding/request digest, preparation, and
  retry-feedback predecessor;
- API grant/reference and native authorization consumption;
- pre-submit intent and call-entry checkpoint;
- first provider identity durability, retrieval/completion, usage/cost settlement,
  provider output persistence, and fan-in state;
- `AUTHORING_COMPLETE` transition and the exact advertised local-work operation;
- `semantic_work_not_consumed` failure, including whether the command had already
  published a sealed result or snapshot;
- the next inspection/request/grant/command invocation;
- every native mutation that preceded the second provider create and identity;
- any stale in-memory state save, snapshot publication, or action-ledger replacement
  capable of erasing the first provider identity or restoring `PREPARED`/
  `AUTHORIZED`/`CALL_ENTERED` eligibility.

### 0D — Reconstruct the API handoff timeline

- Join the exact API action row to the native action and complete binding—not only
  run, stage, or action count.
- Determine which SBE command-result/result/receipt identities the API received,
  validated, rejected, or failed to ingest after each invocation.
- Record whether the second invocation reused an old authority/grant, minted a new
  grant for the same native action/binding, or lacked a public SBE fence that API
  could validate.
- Explain why the API row remained `authorized` without a provider operation ID,
  while preserving the distinction between an API ingestion defect and native
  duplicate-create permission.

### 0E — Trace the relevant production source paths

Create a function-level map for:

- ordinary-resume lifecycle selection and `prior_local_lifecycle` capture;
- retry action preparation/idempotent reuse;
- v2 grant application and provider call-entry fencing;
- immediate identity durability and completion settlement;
- provider output/fan-in consumption;
- `commit_local_work_progress()` semantic-consumption checks;
- exception/nonzero-exit handling and native-result publication;
- subsequent inspection and external-authority request construction.

For every save/publication point, record whether it uses freshly reloaded native
state or a potentially stale in-memory state object.

### Competing hypotheses to test, not assume

1. A stale whole-state save after provider completion overwrote durable provider
   identity/custody and restored create eligibility.
2. Provider completion was durable, but fan-in/local semantic work was not consumed;
   the local-progress wrapper treated that mismatch as a command failure whose
   re-entry path incorrectly replayed provider submission.
3. The native action remained provider-bound, but a later request/grant or dispatcher
   failed to revalidate that custody under the writer fence.
4. Native sealed evidence was correct, but API failed to ingest it and invoked a
   command that the SBE public boundary insufficiently refused.
5. Retry attempt/action identity was recreated or joined incorrectly across the
   completion/fan-in checkpoint.
6. The evidence reveals a different boundary; record it rather than forcing one of
   the above explanations.

### Provider-free characterization

After the retained timeline identifies the exact boundary, add the smallest
production-shaped characterization fixture that can demonstrate:

- one creative-retry action and one accepted grant;
- one scripted provider create and durable identity;
- scripted completion and durable provider result/usage evidence;
- the observed post-completion local failure;
- re-entry through the same public command boundary;
- whether current code permits a second create.

This test freezes current behavior. It must not yet encode a speculative fix.

### Slice 0 deliverables

- `SLICE 0 - EVIDENCE MAP AND READ-ONLY INSPECTION PROTOCOL.md`
- `SLICE 0 - SANITIZED DUPLICATE-SUBMISSION TIMELINE.md`
- machine-readable sanitized action/checkpoint timeline
- read-only inspection receipt with exact accessed hashes and zero-side-effect
  assertions
- `SLICE 0 - SOURCE BOUNDARY AND CAUSAL ASSESSMENT.md`
- provider-free characterization fixture/test if the exact boundary is reproducible
- updated `LOG.md` and `EVIDENCE.md`

### Slice 0 gates

- Exact retained object identity is frozen before any download.
- No broad R2 listing, write, repair, resume, provider call, or affected-workspace
  mutation occurs.
- Every causal statement cites a native member/hash, API record, event/log identity,
  or source location and declares its confidence.
- Both provider identities remain recorded; neither is silently selected as
  authoritative.
- The first violated invariant is identified, or the evidence is explicitly marked
  insufficient/contradictory.
- A provider-free reproducer, when feasible, reaches the same public production
  boundary and proves the exact create count.
- `git diff --check` and focused investigation tests pass.

## Voof-paws 1 — Causal review before contract or runtime work

Pause for owner/API review after Slice 0. The review must decide which class the
evidence supports:

- native stale-state overwrite or custody rewind;
- native dispatch-fence/revalidation failure;
- native post-provider fan-in/local-progress failure with unsafe re-entry;
- API ingestion/reinvocation failure safely refused by native SBE;
- combined API/SBE seam defect;
- contradictory or insufficient retained evidence.

No public schema, recovery posture, or release version is frozen before this gate.

## Provisional later slices

These are placeholders and may be replaced after Voof-paws 1.

### Slice 1 — Contract and invariant freeze

- Freeze constrained external-authority v2 dispatch as the only supported
  create-capable boundary for applicable exact-interactive ordinary action sets;
  generic spend authorization may prepare/inspect but must not cross provider I/O.
- Reuse the existing v2 `CALL_ENTERED` tri-state evidence and command-result v2
  outcomes; do not create a parallel call-entry model.
- Define a typed local-work progress contradiction that seals a terminal-review
  v0.2 result with `new_provider_create_permitted=false`, rather than escaping as
  an untyped `ValueError` before publication.
- Define the durable post-provider action/custody state and the exact local-work
  successor contract, including immutable predecessor/successor result continuity.
- Define exact API joins for request, grant, ordered authorization documents,
  dispatch intent/result, native result, publication receipt, and checkpoint.
- Define historical duplicate posture as review-only with both provider
  observations retained and no canonical selection or automatic recovery.
- Publish `SLICE 1 - DUPLICATE CREATE FENCE CONTRACT PROPOSAL.md` and pause for API
  contract review before mutation.

### Slice 2 — Native correction

- Enforce the correction under the native single-writer fence.
- Preserve provider identity/completion evidence across every local failure.
- Prohibit a second create after call entry or durable provider identity.
- Keep retrieval/fan-in and new-provider authority distinct.

Gate: pause for API review of the typed generic refusal, writer-fenced terminal
review publication, and real v2 call-entry regression evidence before Slice 3.

### Slice 3 — API-shaped fixtures and failure injection

- Provider completion followed by local fan-in failure.
- Failure before and after identity durability.
- Crash/restart at every persistence boundary.
- Stale and repeated command/grant invocation.
- API result-ingestion interruption and exact replay.
- Historical duplicate typed review without automatic recovery.

Deliver a strict packaged bundle containing both distinct consumer outcomes:

- generic exit-0 refusal: API must capture it, perform a fresh lifecycle
  inspection, and follow SBE's selected v2 dispatch boundary; it must not treat
  exit 0 as ordinary-resume success or requeue the generic command;
- local-progress contradiction: API must join the exit-2 envelope to the exact
  v0.2 native result and canonical v0.1 receipt, ingest `review_required`, and
  retain provider-bearing custody rather than reducing it to command failure.

Gate: pause for API review and fixture ingestion before installed-wheel/joint
qualification.

### Slice 4 — Installed-wheel and joint qualification

- Package public schema/readers/fixtures/CLI or qualification command as needed.
- Prove one provider create, durable completion, local failure, safe fresh-worker
  continuation, and no second create.
- Hand off exact artifact and fixture hashes to API for its companion ingestion and
  capacity tests.

### Slice 5 — Regression, release review, and publication

- Run focused and broad suites proportionate to the proven change.
- Build deterministic wheels and run isolated installed-wheel qualification.
- Pause for final API/owner review before fresh immutable release.

## Testing strategy

Use three layers, increasing only after the causal boundary is known:

1. **Evidence tests:** snapshot/member/hash/join validation and sanitized timeline
   determinism.
2. **Native model/runtime tests:** scripted provider, writer-fence interruption,
   stale-state saves, command replay, create-count assertions, and immutable result
   continuity.
3. **Consumer/joint tests:** exact API action/binding/result joins, interrupted
   ingestion, idempotent replay, capacity release, and historical-review posture.

All tests are provider-free until a later separately approved paid QA campaign.

## Release posture

There is no release recommendation at sprint start. A fresh immutable SBE version is
required only if the investigation proves and implements a runtime or public-contract
change. Documentation or API-only findings do not justify an SBE release by
themselves.
