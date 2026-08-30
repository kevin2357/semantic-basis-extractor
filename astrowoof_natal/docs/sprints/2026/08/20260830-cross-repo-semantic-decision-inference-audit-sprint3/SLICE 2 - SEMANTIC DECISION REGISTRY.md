# Slice 2 — semantic decision registry

## Compatibility and reading rule

Every row below was traced against API `main` after Sprint 60 commit `676cb3a`
and the pinned distribution:

- `astrowoof-natal-authoring==0.4.32`
- wheel SHA-256 `c45cd46ff4d7ffa98024b662c55f840e8f7cbea9682d32e97273f6e451493d6e`
- `semantic-projection-core==0.11.1`
- wheel SHA-256 `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`

“Refuse” below means a typed contract/review path with no inferred permission.
It does not mean ordinary `False`, empty inventory, default routing, retry, or
terminalization. Unknown public versions always refuse; historical recovery is
available only through its separately named, version-bound operator service.

## Core scheduling and command registry

| ID / Slice 1 coverage | API decision and source | Authoritative SBE evidence and joins | Positive permission consumed | Required API facts | Current implementation path | Absent / contradictory / unknown | Replay and concurrency fence |
|---|---|---|---|---|---|---|---|
| R-01 / W-01 | Claim job and SBE slot — `SbeReadingWorker._claim`, `ExecutionQueueService.claim_next_sbe_capacity` | No new SBE semantic evidence; compatible checkpoint identity is input to restoration, not claim permission | API queue job is claimable and one allocation is available | FIFO state, attempts, active lease absence, compatibility identity | Atomic API queue/capacity claim | No claim; DB contradiction rolls back; unknown worker identity is ineligible | Lease token + allocation uniqueness |
| R-02 / W-02 | Restore and publish checkpoint — workspace preparation and `_CheckpointPublisher.publish` | Snapshot manifest/hash, checkpoint contract, logical root, compatibility identity | Exact snapshot is valid continuation basis | Current lease and monotonic generation | Validate/restore, then API checkpoint persistence | Missing/invalid snapshot refuses restoration; version mismatch fails closed | Generation, payload digest, one active checkpoint |
| R-03 / W-03, P-06 | Availability preflight | Availability v0.1 → exact result ID → exact sealed result/receipt/snapshot/journal validation → native run join | Permission only to classify and ingest that exact result; availability itself grants none | No invocation-returned result exists; named cycle preflight | `discover_available_result` then `read_exact_sealed`; outcome tested with `is_terminal_native_outcome` | Normal absence continues inspection; malformed/conflicting refuses; unknown result schema refuses | Exact result ID; discovery cannot replace invocation result |
| R-04 / W-04 | Select lifecycle reader | Exact closed schema v0.5/v0.6/v0.7/v0.8 and native run/checkpoint joins | Permission to interpret only that version’s fact family | Installed feature support and current checkpoint | Version-specific installed reader/validator; legacy v0.5 upgrade predicate is narrow | Absent required inspection refuses; contradictory fails contract; unknown version does not fall back | Persisted inspection digest and checkpoint basis |
| R-05 / W-05 | Invoke provider reconciliation | Branch command `provider_reconciliation_cycle`; provider custody known; temporal eligibility due; SBE-selected ordered due subset; v0.8 conflicts cannot suppress retained custody | Retrieve already-created operations named by SBE | Current lease; provider transport config; no create authority required | Run-level reconciliation command; SBE chooses bounded subset (4) | Not due detaches; contradiction reviews; unknown version refuses | Provider IDs + observation/result receipt; never POST/create |
| R-06 / W-06 | Invoke ordinary local resume | v0.7/v0.8 `ordinary_resume`, exact local operation inventory, operation keys, cumulative consumed keys, basis/snapshot/revision joins | Execute the advertised deterministic native operation once | Current lease and restored exact checkpoint | Normal resume; successor inspection must consume key or change typed disposition | Empty local inventory cannot imply resume; contradiction reviews; unknown version refuses | Stable operation key plus cumulative consumed history |
| R-07 / W-07, W-08, N-06, N-07 | Permit provider creation | Exact external-authority request v1/v2; ordered complete binding joins; API grant and member authorization documents; durable API reservation/admission; constrained SBE command | Create only the exact admitted providerless action inventory | Global spend, per-action reservations, active lease/fence | Initial-wave or ordinary constrained dispatch; generic resume cannot create ordinary actions | No grant is passive waiting; mismatch/stale/refusal blocks; unknown version unsupported | Request/grant digest, action/binding identity, durable native call-entry fence |
| R-08 / W-09 | Map lifecycle to worker-cycle disposition | Exact validated terminal, branch, capacity, custody, and local-work fields | Select one supported API worker branch—no broader authority | Worker supports the contract version | `_inspection_cycle_result` | Absent/contradictory raises; unknown version fails before mapper | Inspection/basis digest; branch IDs joined |
| R-09 / W-10 | Map bounded reconciliation result | Exact bounded result plus embedded validated inspection | Select bounded continuation/review/terminal handling supported by that result contract | Route is bounded and current lease is valid | `_bounded_cycle_result` | Missing/malformed refuses; contradictory outcome/inspection must refuse; unknown unsupported | Result/snapshot identity and persisted reconciliation receipt |
| R-10 / W-18 | Generic quiescent defer | A validated cycle result that selects neither due release nor authority wait nor terminal/review/delivery | Retain ordinary local continuation for one bounded delay | Active lease; attempt budget | Final worker `else` → `queue.defer` | No validated disposition must not reach this fallback; contradiction/unknown refuse | Lease end plus next availability |

## Result ingestion, terminality, review, and delivery registry

| ID / Slice 1 coverage | API decision and source | Authoritative SBE evidence and joins | Positive permission consumed | Required API facts | Current implementation path | Absent / contradictory / unknown | Replay and concurrency fence |
|---|---|---|---|---|---|---|---|
| R-11 / N-01, N-02, N-03, W-13 | Accept a native terminal result | Exact invocation-returned terminal-review envelope when present; otherwise exact preflight ID only in named recovery; validated native result/receipt/journal/snapshot; outcome in closed terminal set | Persist this exact native terminal/editorial conclusion | Native run belongs to API run; all action joins hold | `SbeNativeTerminalIngressService.ingest` then transition ingestion | No ID/envelope does not authorize latest discovery except legacy fallback still to classify; contradiction/unknown refuses transaction | Receipt uniqueness and exact replay equality |
| R-12 / W-14 | Terminalize API job/run/reading | Accepted R-11 result plus API lease, queue job, and capacity allocation | Mark API execution terminal and release its local slot | Atomic API queue/capacity transaction; downstream custody obligations understood | `queue.fail(retryable=False)` calls `_fail_run_and_reading`; capacity released | Missing allocation rolls back; contradictory native result never reaches branch; unknown refuses | Lease token and terminal receipt persisted in same session |
| R-13 / W-15 | Close local job for nonterminal native review | v0.7/v0.8 `command=none`, `retain_for_review`, typed reason, no local action selected | Stop local cycling and retain workspace for review; not native terminal ingress | Current lease/capacity | Queue/job/run/reading are failed nonretryably and capacity is released; workspace retained | Missing review facts cannot select branch; contradiction/unknown refuses | Lease token; no native terminal receipt fabricated |
| R-14 / review question | Interpret v0.2 `outcome=review_required` | v0.2 result requires cause, `new_provider_create_permitted=false`, custody finality, complete action dispositions and joins | End native editorial progression and enter exact result ingestion; custody-specific successor work remains governed per action | API must separately decide job/run finality, capacity, provider custody, reservations, settlement, delivery | R-11 accepts it; R-12 currently terminalizes API job/run/reading | Absent custody projection refuses v0.2; ambiguous disposition refuses; unknown result version refuses | Immutable predecessor result plus traceable reconciliation/denial successors |
| R-15 / W-12, A-01, A-02 | Publish delivery and complete successful run | Native delivery accepted, complete required artifact inventory, publication eligibility, critic policy, exact lease | Publish reader-visible output and mark API success | API delivery policy and publication authority | `publish_delivery`; pipeline transition completes job; capacity release and cleanup | Missing inventory/authority refuses publication; contradiction reviews; unknown artifact contract refuses | Publication authority uniqueness and artifact digests |
| R-16 / A-03 | Delete completed workspace | Required outputs adopted; successor or terminal committed; local continuation released; root identity and cleanup authorization | Delete only exact registered workspace | API cleanup record and no retained custody need | `_cleanup_completed` → workspace cleanup service | Any missing predicate retains workspace; contradiction refuses; unknown cleanup contract retains | Cleanup token/root binding and immutable archive |

## Capacity, custody, spend, and recovery registry

| ID / Slice 1 coverage | API decision and source | Authoritative SBE evidence and joins | Positive permission consumed | Required API facts | Current implementation path | Absent / contradictory / unknown | Replay and concurrency fence |
|---|---|---|---|---|---|---|---|
| R-17 / W-11 | Persist workspace readiness | Explicit `local_continuation_required` and provider dependency count from mapped cycle | Record native readiness facts only | Current lease/workspace row | `record_readiness`; a disposition-based fallback remains when local flag is null | Missing explicit field currently falls back; contradiction handled by upstream validator; unknown should not persist | Workspace row under lease |
| R-18 / W-16 | Release local capacity until provider retrieval due | `release_until_due`, checkpoint safe, `known_operations_pending`, exact `resume_not_before` | Release only local worker allocation and defer exact job | Active lease and allocation | Locked latest lifecycle row → `defer_until` + capacity release | Missing/contradictory refuses transaction; unknown never persisted as eligible | DB transaction, lease token, monotonic due time |
| R-19 / W-17 | Release local capacity awaiting compatible grant | Exact `await_external_authority`, joined v2 request, no local/provider work ready | Enter passive admission wait and release only local slot | API has not granted; queue supports awaiting-authority state | `await_external_authority` + capacity release | Missing request/contradiction refuses; unknown unsupported | Request/basis digest; later admission explicitly requeues |
| R-20 / N-04, N-09 | Retain/reconcile provider custody | Exact action/binding/provider operation joins and journal observations | Retrieve/settle already-created provider operation; no new create | API action row and provider-operation custody | Native transition ingestion and reconciliation services | Missing provider authority refuses; ambiguity requires review; unknown observation refuses | Provider operation uniqueness and journal receipt |
| R-21 / N-05, N-10 | Report usage and settle/release authority or providerless closeout | Provider usage observation, or providerless denial/closeout, exactly bound to action inventory | Advance only the exact cost/authority or closeout transaction evidenced | API price/global-spend policy and action state | `_report_usage`, `_release_providerless`, or `SbeLifecycleCloseoutService`; missing usage remains unsettled | Unknown/unavailable is not zero; contradiction rolls back; unknown schema refuses | Monotonic paid-action/closeout state and immutable observation/result |
| R-22 / W-19, W-20 | Fail or defer on worker/contract error | Typed exception family; v0.8 contradiction is isolated from generic failure | Apply only documented retry/review disposition | API attempt budget, lease, capacity | `_record_failure`; special retry-lineage defer | Unknown generic exception may terminalize after attempts; exact implications require Slice 3 mutation | Attempt/lease state and failure classification |
| R-23 / A-04 | Operator retirement | Exact assessment/request/result/receipt proves quiescent providerless closure and `POLICY_STOPPED/operator_retired` | Retire exact abandoned run | API operator fence and pending state | Plan/fence/invoke/finalize; release capacity after ingest | Any provider/local ambiguity refuses; unknown version unsupported | Request digest, pre/post revisions/snapshots, exact replay |
| R-24 / A-05–A-10 | Historical/operator repair | Each named service has a closed target predicate over exact run/job/workspace/checkpoint/action/version facts | Perform only that named release/requeue/disposition | Explicit operator command, compatibility identity, frozen target | Separate services; no generic recovery inference | Missing/contradictory refuses; unknown versions have no implicit migration | Target snapshot and idempotent disposition record |

## Subprocess and evidence precedence registry

| ID / Slice 1 coverage | Evidence order | Positive permission | Current site | Fail-closed behavior | Open trace question |
|---|---|---|---|---|---|
| R-25 / P-01, P-02, P-05 | Invocation-returned typed envelope → exact sealed result joins → exit code as diagnostic | Consume only the exact invocation result | `HeartbeatingProcessSbeProviderRuntime.resume`, `_StdoutJsonlCapture` | Duplicate/conflicting envelopes refuse; exit 2 without valid envelope does not authorize terminal ingress | Non-heartbeating legacy `resume` still consults private progress and `read_latest_sealed` remains a no-ID fallback in terminal ingress |
| R-26 / P-03 | Explicit v2 output file → strict command-result validator → accepted exit set | Consume exact constrained dispatch outcome | `external_authority_v2` | Missing/malformed output refuses even if exit appears successful | Verify every outcome’s reservation effect in Slice 3 |
| R-27 / P-04 | Explicit reconciliation stdout result → strict parser/validator → exit code diagnostic | Consume retrieval result only | `provider_reconcile` | Malformed output refuses; nonzero plus invalid JSON raises process failure | Confirm exact result ID/receipt is always carried or immediately discovered under a named result contract |
| R-28 / P-06 | No invocation result → named availability preflight → exact read/validation | Discover and ingest only exact available result | runtime preflight | Normal absence continues; malformed/contradictory refuses | Prove no “latest” substitution after a command returned an ID |

## Source-to-decision trace summaries

### Provider-pending retrieval

```text
installed lifecycle/temporal reader
  → strict version validator
  → run + checkpoint + custody + due-subset joins
  → persisted lifecycle/temporal decision
  → _inspection_cycle_result
  → provider_reconcile (GET only)
  → exact native transition ingestion
  → new checkpoint basis
  → defer/release or next native branch
```

### External-authority provider creation

```text
installed lifecycle inspection + external_authority_request
  → strict request/inspection validator
  → API action/binding/reservation/admission join
  → immutable grant/member documents
  → constrained command only
  → durable native call-entry/provider identity
  → dispatch result intake
  → provider reconciliation only
```

### Invocation-bound terminal review

```text
SBE command emits terminal_review_command_result.v0.1 and exits 2
  → JSONL capture extracts exactly one envelope
  → read_exact_sealed(result_id)
  → command/result/receipt/invocation/custody join
  → native transition + action custody persistence
  → API queue.fail(retryable=false)
  → GenerationRun.failed + Reading.failed + capacity release
  → provider reconciliation/denial/settlement remains action-specific
```

The final two arrows are distinct decisions. The trace proves what the current
API does; it does not yet establish that outer API terminalization is authorized
for every v0.2 `review_required` custody finality.

## Factual tensions reserved for joint classification

These are not yet labeled defects:

1. `review_required` is terminal in the v0.2 ingress outcome set, nonterminal in
   the lifecycle `retain_for_review` worker branch, and terminalized alongside
   `unsupported` in bounded reconciliation mapping.
2. Both native terminal ingress and the nonterminal review branch call
   `queue.fail(retryable=false)`, which terminalizes the API job, generation run,
   and reading. Their distinction is therefore preserved in native-ingress and
   workspace cleanup behavior, but not in the outer product status.
3. A v0.2 terminal-review result can explicitly retain provider reconciliation
   or providerless-denial custody after the outer API run/reading becomes failed.
4. `SbeNativeTerminalIngressService.ingest` still has a `read_latest_sealed`
   fallback when neither invocation-bound nor explicit preflight result ID is
   supplied. Current ordinary callers appear to supply one, but the fallback is
   broader than the registry’s preferred evidence rule.
5. `_bounded_cycle_result` maps `review_required` and `unsupported` to the same
   `TERMINAL_CLOSED` cycle disposition without an evident exact v0.2 terminal
   result identity at that mapping site.
6. Workspace readiness retains a disposition-derived fallback when the explicit
   local-continuation field is absent.

Slice 3 should mutate these seams before Slice 4 assigns ownership or severity.

## Coverage statement

Registry rows R-01 through R-28 cover every Slice 1 sink. Where multiple Slice 1
sites implement the same independently authorized decision, the row lists all
covered IDs. Native terminal-result acceptance (R-11), API terminalization
(R-12), capacity release (R-18/R-19), custody/settlement (R-20/R-21), and delivery
(R-15) remain separate.
