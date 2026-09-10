# Native-Side Design Assessment

## Executive assessment

The missing capability is not a more permissive quarantine classifier. It is a
new, exact, cooperative native suspension protocol that can produce stronger
evidence than today's read-only disposition assessment.

The safe sequence is:

```text
API durable stop fence
  -> SBE observes an exact suspension request at a defined safe point
  -> SBE persists checkpoint and custody facts
  -> SBE emits one exact suspension result/receipt
  -> process exits or is separately confirmed absent
  -> API joins fence + native result + process/lease fact
  -> API decides whether local capacity may be released
```

SBE can attest only to work it observed and durably recorded. API remains the
authority for stopping future claims, supervising a process, and releasing API
leases or capacity. A supervisor-forced termination before SBE publishes a
result is evidence of interruption, not evidence of cooperative suspension.

## Why disposition assessment v1 should remain strict

The current assessment correctly marks `native_local_work_ready` and
`completed_unadopted` as `native_prior_action_required`, and marks
`unsupported_or_inconsistent` as prohibited. Those outcomes describe a static,
snapshot-valid workspace. They do not prove that a process is absent, that an
in-flight write has quiesced, or that a provider call boundary was not crossed.

Changing those v1 mappings to `permitted` would collapse two different claims:

1. what custody posture the workspace currently demonstrates; and
2. whether an exact active invocation observed a stop fence and exited at a
   known boundary.

The second claim requires new evidence. It should be additive and independently
validated, not inferred from v1 fields.

## Proposed ownership boundary

### API/control plane owns

- durable stop request, actor, reason, environment confirmation, and
  idempotency identity;
- ordinary-claim and successor-dispatch fencing;
- delivery of the exact request to the exact invocation;
- grace-period timing and exact-process hard-stop supervision;
- job, lease, slot, and capacity accounting;
- provider reservation and spend accounting;
- quarantine/hold visibility and all later resolution requests;
- the final decision to release local resources.

### SBE/native runtime owns

- validation that a presented request targets the current run, workspace,
  checkpoint lineage, and invocation boundary;
- cooperative observation at explicitly enumerated safe points;
- serialization with native workspace mutation;
- preservation of action, provider, result, receipt, local-work, and checkpoint
  facts already known to the invocation;
- publication of one exact suspension result and receipt;
- truthful classification of what native work was quiesced and what remains
  unresolved;
- refusal when identity, freshness, custody, or persistence cannot be proven.

SBE should not report `capacity_released`, `lease_released`, or `process_killed`.
Those are API/supervisor facts. It may report whether its own local mutation loop
reached a durable quiescent boundary and whether native continuation is required.

## Request shape

A future request should be exact and additive, plausibly
`astrowoof.native_suspension_request.v1`. At minimum it should bind:

- native run ID and logical workspace-root identity;
- API run/job identity as opaque caller-owned correlation;
- exact checkpoint ID/generation or an explicit pre-checkpoint posture;
- exact invocation/lease correlation supplied by API;
- request ID, idempotency key, actor, reason code, and environment;
- request creation time and bounded expiry/freshness rule;
- digest over the complete canonical request;
- requested operation fixed to cooperative suspension—not cancel, retire,
  reconcile, or terminalize.

The request must not contain a reconstructed native command, provider payload,
credentials, or permission to discard evidence. A stale request from an earlier
invocation must not suspend a newly resumed worker merely because run ID matches.

## Result shape

A corresponding `astrowoof.native_suspension_result.v1` should bind the exact
request and the exact native invocation. It should include:

- request digest and identity;
- run/workspace/checkpoint lineage observed before suspension;
- last durable checkpoint identity after any permitted checkpoint write;
- whether the native mutation loop reached a quiescent boundary;
- whether checkpoint publication completed and its exact receipt identity;
- custody summary using existing native evidence rather than filename/status
  inference;
- provider call boundary: `not_entered`, `known_identity`, or
  `entry_or_result_ambiguous`;
- local native work posture: none, durable pending, completed-unadopted, or
  ambiguous;
- one closed outcome and reason code;
- exact result/receipt identity suitable for same-invocation handoff;
- explicitly non-authoritative hints about supported later native operations.

The result should not say that a provider operation was cancelled, that spend
was released, that API capacity was released, or that the run is terminal.

## Outcome taxonomy

The top-level outcomes should distinguish at least:

| Outcome | Meaning | API implication |
| --- | --- | --- |
| `suspended_checkpointed` | SBE observed the request, persisted a valid checkpoint, published the result, and exited its mutation loop | Eligible for API's separate process/lease join; not automatically released |
| `suspended_quiescent_no_checkpoint_change` | Existing durable state already represented the exact safe boundary; no new workspace facts were needed | Same join requirement; exact prior checkpoint remains authoritative |
| `suspension_refused` | Target, freshness, custody, or safe-point requirements failed | Keep fenced/held; no native-derived release |
| `suspension_deferred` | Invocation observed the request but was inside a bounded operation that must settle before a truthful result can be produced | Keep fenced and wait only within the declared bound |
| `provider_boundary_ambiguous` | Call entry or result persistence cannot be proved either way | Hold provider/spend custody and route to named reconciliation/review |
| `checkpoint_publication_ambiguous` | Native state may have changed but the exact checkpoint/result receipt is unavailable | Hold; never rediscover or synthesize the missing identity |

`hard_stopped` should not be a native result unless SBE itself durably observed
and published that fact before exit. Ordinarily it is an API supervisor event
joined to the absence of a successful native suspension result.

## Safe-point strategy

A cooperative check should occur only at bounded lifecycle seams where SBE can
serialize it with mutation and custody transitions. Candidate seams include:

- before selecting or consuming a new paid action;
- before entering provider create;
- after durable provider identity persistence;
- after provider retrieval persistence and before local adoption;
- before and after native local fan-in/polish mutation;
- after checkpoint/result publication and before selecting a successor action;
- at detached reconciliation loop boundaries.

Polling a stop flag in the middle of arbitrary file writes or treating an OS
signal handler as a transaction boundary would be unsafe. Signal handling may
set an in-memory observation flag, but the ordinary serialized lifecycle loop
must perform the checkpoint and result publication.

## Provider boundary

The hardest seam is provider create. There are three materially different
facts:

1. the request is observed before call entry: SBE can suspend without provider
   ambiguity;
2. a provider ID is durably persisted: later work is retrieval/reconciliation
   only;
3. call entry may have occurred but no provider identity/result is durable:
   suspension must preserve explicit ambiguity and prohibit resubmission.

The stop protocol must not promise immediate cooperative exit while a provider
SDK call is blocked. API may enforce a grace period and terminate the process,
but that produces the third posture unless stronger durable evidence exists.

## Checkpoint and publication atomicity

The result must derive from the checkpoint publication completed by the same
invocation. Latest-result or latest-checkpoint discovery cannot repair a missing
handoff. If checkpoint bytes were persisted but their publication receipt was
not, the truthful result is ambiguity/refusal, not successful suspension.

The existing exact result/receipt handoff patterns should be reused. Suspension
must not create a parallel identity system or allow API to reconstruct a result
from status fields.

## Hard-stop interpretation

The API sequence should be:

1. persist the stop fence;
2. prevent future ordinary claims and successor dispatch;
3. ask the exact active invocation to suspend cooperatively;
4. wait a bounded grace period;
5. if needed, terminate only the exact supervised process;
6. classify the outcome from durable evidence.

If step 5 occurs without a valid exact native result, API may release the OS
process and eventually its local lease under its own supervision rules, but it
must retain an `operator_interrupted` or equivalent held posture. It cannot
describe native custody as clean or use process death to release provider/spend
authority.

This distinction is important: preventing one process from monopolizing a host
is possible even when lifecycle resolution remains unsafe. Local scheduling
containment and semantic closeout are separate decisions.

## Interaction with retention issue 17

Every suspended, refused, deferred, ambiguous, hard-stopped, or quarantined run
must impose a retention hold over its transitive evidence graph:

```text
run -> checkpoint generations -> workspace members
    -> action/result/receipt evidence
    -> provider identity and spend evidence
    -> operator request and suspension result
```

Neither SBE nor a storage sweeper should infer deletion eligibility from age or
prefix. API's authoritative registry and hold records own eligibility. A future
SBE artifact-role inventory may help describe referenced native members, but it
must remain descriptive and fail closed on unknown references.

## Compatibility and versioning

This should be an additive v1 request/result pair. Existing
`operator_disposition_assessment.v1` remains valid and strict. A later v2
assessment may project a verified suspension result, but only after the new
contract exists; changing v1 quarantine outcomes in place would blur historical
meaning and weaken old consumers.

Ordinary workers that do not support suspension must reject or ignore the new
request according to an explicit compatibility rule while API keeps the run
fenced. Restart must never imply successful suspension or unquarantine.

## Qualification expectations

Provider-free qualification should cover the cross-product of:

- request identity: exact, stale invocation, wrong run, wrong checkpoint,
  expired, duplicate, and digest-corrupt;
- lifecycle seam: pre-action, pre-create, known provider ID, retrieved but
  unadopted, local work ready, terminal result, and unsupported evidence;
- persistence failure: before checkpoint write, during publication, after
  receipt, and before command handoff;
- process outcome: cooperative exit, delayed operation, and supervisor hard
  stop without a native result;
- replay: duplicate request/result handling across fresh worker startup;
- privacy: no prompt, response payload, credentials, subject data, or local
  path leakage;
- authority: zero provider calls/spend in qualification and no mutation from
  logs or descriptive assessment alone.

At least one joined API/SBE test must prove that no single fact is sufficient:
the API stop fence alone, process death alone, disposition assessment alone, or
native suspension result alone must not authorize the complete release path.

## Initial recommendation

Begin with Slice 0 source mapping before freezing field names. In particular,
inventory every provider call-entry persistence seam and detached subprocess
adapter. The recent terminal-handoff investigations show that a sound native
result can still be lost at stdout/adapter boundaries; suspension qualification
must therefore include real CLI/JSONL and detached exit behavior, not callback
tests alone.

The likely smallest useful first implementation is cooperative suspension at
ordinary lifecycle-loop boundaries plus exact result/receipt handoff. Provider
call interruption and supervisor hard-stop classification can then be added as
separate cells without pretending they share the same proof strength.

