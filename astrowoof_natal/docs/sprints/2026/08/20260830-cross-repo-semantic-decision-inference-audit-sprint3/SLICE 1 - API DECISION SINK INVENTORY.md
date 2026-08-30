# Slice 1 — API decision-sink inventory

## Audit basis

This inventory enumerates API decisions that consume, or may consume, public
SBE evidence. It does not yet classify a predicate as correct or defective.
Slice 2 will trace each source-to-sink join and assign the exact positive
permission.

Source was inspected on API `main` after Sprint 60 commit `676cb3a`. The native
compatibility basis is installed SBE `0.4.32` with SPC `0.11.1`. Qualification
and operator-only entry points are listed separately from the ordinary worker
path so that recovery predicates cannot silently become production routing
rules.

## Primary worker and runtime sinks

| ID | API decision sink | Source | State-changing effect | Current immediate input | Intended authority owner | Principal tests |
|---|---|---|---|---|---|---|
| W-01 | Claim an SBE job and capacity allocation | `worker/sbe.py:SbeReadingWorker._claim`; `services/execution_queue.py:claim_next_sbe_capacity` | Acquires job lease and one API capacity slot | API queue/run/capacity rows | API | `test_execution_queue.py`, `test_adversarial_installed_vertical_slice.py` |
| W-02 | Restore workspace and accept checkpoint | `worker/sbe.py:_run_claim`; `worker/sbe_runtime.py:_CheckpointPublisher.publish` | Restores/publishes API checkpoint generation | API checkpoint plus validated SBE snapshot | Joint join; API persists | `test_sbe_worker.py`, `test_sbe_runtime.py` |
| W-03 | Preflight an available sealed result | `worker/sbe_runtime.py:ProductionSbeCycleEngine.advance` lines 253–286 | Selects exact-result ingress or continues ordinary inspection | Availability document followed by exact result read | SBE result semantics; API routing | `test_sbe_runtime.py`, API Sprint 60 regression matrix |
| W-04 | Select lifecycle contract version | `worker/sbe_runtime.py:advance`, `_record_lifecycle_inspection`, `_record_local_work_lifecycle_inspection`, `_record_retry_lineage_lifecycle_inspection` | Chooses v0.5/v0.6/v0.7/v0.8 consumer path or fails closed | Installed SBE readers plus current workspace | SBE contract version; API capability | `test_sbe_runtime.py`, `test_sbe_provider_pending_lifecycle.py`, `test_sbe_local_work_lifecycle.py`, `test_sbe_retry_lineage_lifecycle.py` |
| W-05 | Select provider reconciliation | `worker/sbe_runtime.py:_inspection_cycle_result`, `_advance_bounded_reconciliation` | Invokes GET-only reconciliation cycle | Validated branch command and SBE-selected due subset | SBE selects native work; API owns lease | `test_sbe_runtime.py`, `test_sbe_bounded_reconciliation.py`, `test_provider_pending_qualification.py` |
| W-06 | Select ordinary local resume | `worker/sbe_runtime.py:_inspection_cycle_result` and local-work helpers | Invokes native deterministic fan-in/retry preparation | Validated local-work inventory and operation identity | SBE | `test_sbe_runtime.py`, `test_sbe_local_work_lifecycle.py`, post-fan-in qualifications |
| W-07 | Select initial-wave authority admission | `worker/sbe_runtime.py:_advance_initial_wave` | Reserves/authorizes exact initial wave and invokes constrained command | Validated request/bundle plus API policy | Joint: SBE inventory, API admission | `test_sbe_initial_wave_authority.py`, initial-wave qualification |
| W-08 | Select ordinary external-authority v1/v2 admission | `worker/sbe_runtime.py:_advance_external_authority`, `_advance_external_authority_v2` | Persists grant/intake and invokes create-capable constrained command | Exact request, action joins, API reservations/grant | Joint | external-authority v1/v2 tests and qualifications |
| W-09 | Map lifecycle inspection to cycle disposition | `worker/sbe_runtime.py:_inspection_cycle_result` lines 887–931 | Produces `TERMINAL_CLOSED`, `REVIEW_REQUIRED`, or `QUIESCENT` | Validated branch, capacity, custody, and terminal fields | SBE facts; API mapper | `test_sbe_runtime.py`, `test_adversarial_installed_vertical_slice.py` |
| W-10 | Map bounded reconciliation to cycle disposition | `worker/sbe_runtime.py:_bounded_cycle_result` lines 1146–1165 | Produces terminal/review/quiescent worker result | Bounded result outcome plus embedded lifecycle inspection | SBE facts; API mapper | bounded reconciliation and route-matrix tests |
| W-11 | Project workspace readiness | `worker/sbe.py:_run_claim` lines 319–337 | Persists local-continuation flag and provider dependency count | `SbeCycleResult` fields, with fallback based on disposition | API persistence of SBE-derived facts | worker/adversarial tests |
| W-12 | Publish delivery | `worker/sbe.py:_run_claim` delivery branch lines 398–466 | Publishes reading, completes job, cleans workspace, releases capacity | `DELIVERY_ACCEPTED` plus API publication eligibility and lease | Joint; publication remains API-owned | publication and worker tests |
| W-13 | Ingest native terminal result | `worker/sbe.py` terminal branch; `services/sbe_native_terminal_ingress.py:ingest` | Validates/persists exact native result | Invocation-bound result ID, or named preflight exact ID, plus receipt joins | SBE terminal fact; API persistence | `test_sbe_native_terminal_ingress.py`, terminal-review tests |
| W-14 | Terminalize API execution job after native ingress | `worker/sbe.py` terminal branch lines 495–509 | Fails job nonretryably and releases capacity | Accepted native terminal outcome plus lease/capacity rows | API | worker terminal tests, adversarial closeout rollback test |
| W-15 | Handle nonterminal review disposition | `worker/sbe.py` review branch lines 532–575 | Fails local execution job nonretryably, releases capacity, retains workspace | `SbeCycleDisposition.REVIEW_REQUIRED` | API disposition from SBE native review facts | adversarial Muffin tests, retry-lineage tests |
| W-16 | Release provider-pending capacity until due | `worker/sbe.py` quiescent branch; `services/sbe_provider_pending_release.py:release` | Defers job until native time and releases slot | Exact `release_until_due` inspection and API lease/capacity | Joint | provider-pending release/qualification tests |
| W-17 | Release while awaiting external authority | `worker/sbe.py`; `services/sbe_external_authority_v2_awaiting_grant.py` | Moves job to awaiting-authority state and releases slot | Exact validated v2 request/no-grant posture | Joint | v2 awaiting-grant and worker tests |
| W-18 | Generic quiescent defer | `worker/sbe.py` final branch lines 612–622 | Defers job by configured retry interval | Any cycle result not matched by explicit release/authority branches | API fallback mapper | worker and adversarial tests |
| W-19 | Convert exception to retryable/nonretryable job failure | `worker/sbe.py:_record_failure`, `_run_claim` exception path | Fails/defer-equivalent job; may release capacity and clean pre-native workspace | Python exception classification | API | worker/provider-failure qualification tests |
| W-20 | Handle retry-lineage contract contradiction | `worker/sbe.py:_defer_retry_lineage_contract_block` | Defers while retaining review custody/capacity posture | Typed v0.8 contract error | API fail-closed policy | retry-lineage worker tests |

## Native-result, custody, authority, and settlement sinks

| ID | API decision sink | Source | State-changing effect | Current immediate input | Intended authority owner | Principal tests |
|---|---|---|---|---|---|---|
| N-01 | Decide whether a native outcome may enter terminal ingress | `services/sbe_native_terminal_ingress.py:is_terminal_native_outcome` | Enables exact terminal ingestion | Closed outcome string set | SBE semantic contract consumed by API | terminal-ingress and Sprint 60 tests |
| N-02 | Validate invocation-bound terminal-review envelope | `services/sbe_native_terminal_ingress.py:_validated_terminal_review_command`, `_validate_command_against_publication` | Permits exact v0.2 result ingestion | Command result, exact result, receipt, run/invocation/custody joins | SBE evidence; API validates | terminal-review ingress tests |
| N-03 | Persist journal/result/receipt publication | `services/sbe_native_transition_ingestion.py:validate`, `persist` | Creates immutable API native receipt and observation rows | Validated result, receipt, journal range, snapshot | SBE truth; API persistence | native-transition ingestion tests |
| N-04 | Join terminal-review action custody | `services/sbe_native_transition_ingestion.py:_validate_terminal_review_api_action_joins` | Admits or refuses per-action provider/reported/unused custody | v0.2 action inventory plus API actions/bindings | Joint | terminal-review join tests |
| N-05 | Report/reconcile provider cost and release providerless authority | `services/sbe_native_transition_ingestion.py:_project_provider_evidence`, `_report_usage`, `_release_providerless` | Advances paid-action/global-spend state | Exact native observation and API action state | Joint; API owns money | ingestion/accounting tests |
| N-06 | Reserve and authorize paid actions | `services/sbe_authoring_authority.py`; initial-wave and external-authority admission services | Creates reservation and authorization rows | SBE request/binding plus API policy | API | authority/admission tests |
| N-07 | Persist v2 dispatch intake and replay fence | `services/sbe_external_authority_v2_dispatch_intake.py` | Records command result and releases/retains reservation according to typed outcome | Validated v2 command/dispatch result and exact action joins | Joint | v2 dispatch intake tests |
| N-08 | Map dispatch outcome to operator disposition | `services/sbe_provider_dispatch_result.py:ValidatedProviderDispatchResult.operator_disposition` | Selects pending, review, refused, or replay handling | Closed dispatch result fields, including provider-I/O disposition | SBE contract; API mapper | provider-dispatch-result tests |
| N-09 | Reconcile provider operations | `services/sbe_provider_orchestration.py:SbeProviderActionService.reconcile`, native ingestion | Advances provider-created/reported/reconciled action state | Native/provider observation identity and usage | Joint | provider orchestration and accounting tests |
| N-10 | Close providerless denial | `services/sbe_lifecycle_closeout.py` | Persists closeout, denies/release actions, may terminalize native lifecycle projection | Exact denial result and action inventory | SBE outcome; API authority release | lifecycle-closeout tests |

## API product, publication, cleanup, and recovery sinks

| ID | API decision sink | Source | State-changing effect | Current immediate input | Intended authority owner | Principal tests |
|---|---|---|---|---|---|---|
| A-01 | Elect publication authority | `services/publication_eligibility.py:elect` | Creates/returns API publication authority | Run state, accepted artifacts, critic policy, terminal/delivery facts | API | `test_publication_eligibility.py` |
| A-02 | Complete pipeline transition | `services/pipeline_transitions.py` | Completes execution job/run and releases capacity | Accepted stage/delivery and API artifact rows | API | pipeline transition tests |
| A-03 | Authorize workspace cleanup | `services/workspace_cleanup.py`; `worker/sbe.py:_cleanup_completed` | Deletes or retains workspace | Required outputs adopted, successor/terminal committed, continuation released | API using validated evidence | workspace-cleanup and worker tests |
| A-04 | Retire operator-abandoned native run | `services/sbe_operator_retirement.py` | Fences job, invokes SBE retirement, ingests result, releases capacity | Exact retirement assessment/request/result plus API pending custody | Joint | operator-retirement tests/qualification |
| A-05 | Dispose exhausted providerless work | `sbe_exhausted_pre_provider_disposition.py`, `sbe_closed_native_terminal_disposition.py` | Marks API work terminal and releases slot | Exact workspace/checkpoint/action closure predicate | API recovery policy consuming SBE facts | operator tests |
| A-06 | Release exhausted provider-pending capacity | `sbe_exhausted_provider_pending_release.py` | Releases local slot without provider custody | Valid lifecycle release predicate plus API exhausted job | Joint | operator tests |
| A-07 | Requeue retained provider reconciliation | `sbe_exhausted_provider_pending_reconciliation_recovery.py`, retained-provider recovery services | Requeues exact retained work | Frozen checkpoint/workspace/custody predicate | API recovery authority | operator tests |
| A-08 | Requeue awaiting-authority handoff | `sbe_external_authority_v2_handoff_recovery.py`, `sbe_pre_provider_v2_authority_recovery.py` | Requeues exact job without creating provider work | Persisted request/grant/intake plus API state | API recovery authority | operator/v2 recovery tests |
| A-09 | Apply historical compatibility disposition | `sbe_legacy_runtime_disposition.py`, legacy bridge/recovery services | Retires or requeues narrowly recognized historical work | Version-bound historical predicates | API operator policy with SBE compatibility facts | legacy bridge/operator tests |
| A-10 | Dispose orphaned terminal/providerless residual | `sbe_orphaned_terminal_disposition.py`, `sbe_orphaned_providerless_release.py` | Releases capacity/authority after lost workspace | Exact failed job/run marker and absence predicates | API operator policy | operator tests |

## Subprocess evidence-precedence sinks

| ID | Site | Current branch shape | Required audit question for Slice 2 |
|---|---|---|---|
| P-01 | `ProcessSbeProviderRuntime.resume` | Exit 0 succeeds; otherwise private progress may suppress the subprocess error | Is this path still reachable for current contracts, and does it ever outrank an invocation-returned typed result? |
| P-02 | `HeartbeatingProcessSbeProviderRuntime.resume` | Generic refusal is parsed first; exit 0 returns command result; exit 2 plus terminal-review envelope returns that envelope; private progress is legacy fallback | Are exact envelope/result joins always consumed before any follow-on scheduling? |
| P-03 | `external_authority_v2` | Reads explicit output document; accepts exits 0/3 after strict validation | Does each outcome retain distinct reservation/custody handling? |
| P-04 | `provider_reconcile` | Parses explicit stdout result; malformed output plus nonzero exit raises process error | Is a sealed result identity present in this result and consumed before exit-code fallback? |
| P-05 | `_StdoutJsonlCapture` | Extracts one terminal-review envelope or generic refusal and rejects conflicts/duplicates | Do all invocation-bound result-producing commands use this capture surface? |
| P-06 | Availability preflight | Only when no invocation is in progress; reads discovered exact result before classification | Is it restricted to recovery/preflight and fenced against replacing an invocation-returned ID? |

## `review_required` question frozen for Slice 2

There are at least three distinct review-shaped inputs in the current API:

1. lifecycle `retain_for_review`, mapped to `SbeCycleDisposition.REVIEW_REQUIRED`
   and intentionally excluded from native-terminal ingress;
2. sealed native execution result v0.2 with `outcome=review_required`, admitted by
   the closed terminal-ingress outcome set; and
3. bounded reconciliation result `outcome=review_required`, currently mapped by
   `_bounded_cycle_result()` to `TERMINAL_CLOSED` together with `unsupported`.

The same spelling therefore cannot decide API terminality by itself. Slice 2
must separately trace:

- whether v0.2 `review_required` ends editorial creation while retaining
  provider retrieval/denial/settlement work;
- whether API job failure and capacity release are intentional without claiming
  provider custody release or publication;
- whether outer API run/reading terminalization occurs at the same transaction
  or only after custody/settlement successors;
- whether bounded `review_required` carries equivalent v0.2 terminal evidence;
  and
- whether `unsupported` has any positive permission to enter terminal ingress.

No conclusion is assigned in Slice 1.

## Enumeration completeness check

Searches covered production Python source for direct and indirect uses of:
`sealed`, `terminal`, `review_required`, `retain_for_review`, `returncode`,
availability, lifecycle branch/capacity, local continuation, provider custody,
external authority, reconciliation, queue mutation, capacity release,
publication, cleanup, and operator recovery. Test and qualification files were
used as references but were not treated as production decision owners.

Every enumerated sink now names an owner and intended authoritative input. Slice
2 may split rows further when one call site performs multiple independently
authorized mutations.
