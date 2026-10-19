# Slice 0C — bounded alpha: exact same-call handoff and safe containment

**2026-10-18 · proposed Gate A scope refinement; awaiting joint approval.**
The subsequent owner/API/SBE clock-policy agreement is recorded in API sprint
129's `SBE AGENT - GATE A ALPHA SHARED HANDOFF AND FIXTURES.md` and
supersedes any suggestion here that an unmeasured cross-host skew alone must
disable alpha acknowledgement. The assumption and its unbounded risk remain
explicit; detectable invalid timing and ambiguous authority stay contained.
This replaces the durable attempt-binding and crash-reconstruction portions of
[Slice 0B](SLICE%200B%20-%20NATIVE%20COMMAND%20AND%20SUPERVISION%20PROPOSAL.md)
and the Candidate A/B research for this release. Keep those documents as the
history of what was considered, not an additional implementation mandate.
No implementation, live action, provider call, release or deployment is
approved by this planning document.

## Scope and non-goals

Make the real bounded interactive v2 reconciliation command interoperable with
API, safely supervised, and exactly attributable **when its same-call output
is available and valid**. On ambiguity, preserve provider/native evidence and
API custody, prevent unauthorized continuation, and surface the case for
human investigation. Rare failures may strand a run and its capacity; that is
an explicit alpha tradeoff, not a successful recovery or provider settlement.

No singleton active slot, write-ahead anchor, attempt-keyed recovery sidecar,
new journal schema, historic-slot reconstruction or general automatic recovery
of a lost result is required merely to qualify this release. Do not choose a
prior result by `latest`, infer no-publication from missing output, relabel an
older result as a new invocation, or rerun/recreate paid work to escape
ambiguity. A separately authorized and independently proven existing protocol
may be assessed later; none is invented here.

## Proposed normal path

1. API admits an exact bounded profile/release, persists the child supervision
   invocation and lease authority, and launches the route-specific bounded argv
   described in API sprint 129's `SBE AGENT - GATE A ARGV AND DECISION
   EVIDENCE.md`. Compare explicit OpenAI/interactive flags with the installed
   profile, durable workspace and actual bounded v2 mechanism before provider
   I/O or mutation. The same ordered argv is hashed, launched and compared to
   direct-child evidence. Exact-route behavior remains unchanged.
2. For each invocation that **actually produces a new native publication**,
   SBE emits its exact SBE-owned native invocation, result and receipt IDs and
   the necessary digests from that same publication call, for terminal and
   nonterminal results. A closed, typed same-call companion is a proposal to
   freeze jointly; it is not an existing attempt-keyed durable recovery record.
   It must not be fabricated from a generic latest-result lookup or an earlier
   terminal publication. If a publisher repairs or reuses an older result,
   fail closed unless exact same-call ownership can actually be proven; no
   automatic adoption of old results is required for alpha.
3. API joins the output to the exact launched child, saved prelaunch identity,
   argv/profile/run/route/lease and applicable fence authority. It reads the
   **named** result and receipt and validates their closed schemas, hashes,
   journal and snapshot/basis evidence in the workspace. It must not use a
   copied ID, output line, process exit, log or native local file alone as
   authority. Its checkpoint must contain the validated workspace and the
   appropriate result/receipt, and its durable ingestion must match those exact
   facts. Remote checkpoint, native custody ingestion and economics/outer DB
   transaction are separate boundaries; the joint test must settle their real
   safe ordering and failures. A local snapshot is not remote durability.
4. SBE/API freeze the actual result/exit/companion combinations per outcome,
   including early `review_required` with no result checkpoint and mutation-free
   `not_due`. A no-publication result is not automatically `not_due`, success,
   or evidence that a provider request never existed. No invented predecessor
   fields or missing-artifact assumptions. Reconcile at most the existing
   policy's four retrievals per cycle and no provider create; further paid
   work requires the separately authorized existing path.

## Cooperative suspension and clocks

Keep the actual safe points: before a wave is admitted and after its responses
are adopted into a validated local checkpoint. Once a wave is admitted, up to
four GETs may start or finish after a fence arrives; after a valid observed
suspension, do not start a subsequent wave. A hanging GET or forced process
death is not a cooperative acknowledgment. The suspension receipt is local
native evidence; API independently verifies its matching direct-child exit,
lease/fence and required remote checkpoint before any downstream action.

Sample the real observation instant at the safe point, not the frozen launch
decision timestamp; preserve the original observation on replay. Strict
freshness is a separately versioned contract, with exact-route/historical
semantics preserved. **Clock topology check:** current API parent calls
`SbeNativeSupervisionService.build_suspension_request` in
`worker/sbe_runtime.py::_publish_native_suspension_request`; its default
`requested_at` is `datetime.now(UTC)`. The same API worker parent launches
the SBE child through `sbe_provider_orchestration.py::provider_reconcile`.
This is source evidence of parent and child on one worker host for this path,
not a qualification of clock monotonicity, clock namespaces or any externally
originated fence deadline. The fence's `grace_deadline` can have its own
source. Jointly trace that source and define handling of clock steps and
unverifiable freshness; missing/ambiguous evidence means no acknowledgment,
not a guessed clock bound or extended grace. Do not require a generic
cross-host synchronization service merely because the earlier draft assumed
one. Test real boundary instants and clock changes provider-free.

Parent-observed terminal/fence ordering stays API-owned: do not allow a child
seal timestamp or unverified logs to override an observed fence. Where order
is ambiguous or lost, preserve the applicable fence and custody. This scope
does not assume a new durable parent-order journal is already implemented;
API must choose and test a conservative rule it can actually support.

## Failure and outcome matrix

| Case | Expected alpha behavior |
| --- | --- |
| Pending/completed/failed GET; later authorized known-ID repeat GET | Real bounded CLI + API validate exact identities and state; no duplicate paid create, and no new paid stage without separate authority. |
| Normal nonterminal or terminal new publication with complete same-call output | Exact child/output/result/receipt join, validated native workspace, durable checkpoint and API ingestion. Terminal outcome gets at most its matching companion. |
| `not_due` | Explicit result, zero GET and no workspace mutation or successor checkpoint; lost output is unknown. |
| Early integrity `review_required` without checkpoint | Explicit reviewed/refused outcome; API validator must admit only its allowed shape while preserving custody, never turn missing checkpoint into success or automatic settlement. |
| Fence before GET; fence during an admitted GET wave | Before: no wave. During: wave may finish; require local post-response checkpoint, matching suspension evidence and independently proven child exit. No next wave after valid observation. |
| Invalid/stale/uncertain request, wrong identity/profile/route or mismatched output | Reject/fail closed; no fabricated suspension, result, custody disposition or successful ingestion. |
| Lost/truncated stdout; crash before/after seal/receipt or checkpoint; unknown checkpoint/DB acknowledgment | Preserve the applicable fence/hold and provider custody, retain surviving evidence, expose an actionable unresolved condition; do not synthesize success, pick latest, or automatically relaunch paid work. If a previously **API-committed** exact identity can be independently read back and replayed idempotently, test that separate known-evidence path; absent proof stay unresolved. |
| Native receipt exists locally but checkpoint or API intake failed | No assumption of remote durability or API ingestion; retain exact known evidence and custody. Same-call output may support retry only with independently valid lease/fence authority and exact already-known identities; otherwise unresolved. |
| Old terminal result, conflicting attempts, missing direct-child exit, ambiguous parent order | Fail closed; do not reattribute old publication, settle custody, release capacity or grant pre-fence precedence. |
| Economics savepoint failure / outer rollback / committed-but-ack-lost | Inspect authoritative durable records separately; missing economics is not zero cost, native custody settlement, or an independent commit. Preserve unresolved state when outcome is not proved. |
| Six pending operations | Exercise more than one policy-limited cycle/wave, with fake barriers, exact operation IDs, no POST and no duplicate paid create. |
| Existing exact/historical controls | Preserve existing exact-route and historical record interpretation; no silent shared-observer semantic changes. |

Use the installed successor wheel, actual bounded executable, API collector,
validators, checkpoint archive/restore and database transaction path, with
synthetic native workspaces, fake provider transport and blocked provider
network. Test every failure boundary even though the acceptable result in
ambiguous cases is now containment, not automatic recovery. Synthetic storage
and fake transport do not prove production platform behavior.

## Operator reality: what exists, what remains unproven

API's `docs/operations/Operator Run Quarantine Runbook.md` describes its
QA-qualified route: exact operator hold, manual SBE redeploy/stop inspection,
then acknowledged held-run break-glass finalization where its preconditions
are met. `operator_run_hold.py` says the hold denies future admission; it is
not proof that existing work stopped, provider work settled or capacity was
released. The runbook's finalization releases **target schedulable capacity**
while explicitly preserving unresolved provider/native/spend custody; it is
not a general replay/reconciliation command. The runbook marks cooperative
force-fence/worker-replacement recovery as experimental and not reliable for
restoring peer progress. The hold-alert playbook describes an operator-hold
signal, not proof that every new ambiguity is automatically alerted.

Before qualification, API must test which ambiguous bounded outcomes can be
identified and safely held using the actual run/job state, what evidence and
incident signal the operator sees, and when the existing manual procedure is
eligible. A terminal or otherwise ineligible hold, missing stop proof, remote
uncertainty or unresolved provider custody may require investigation or
remaining held; do not promise a magic repair, provider cancellation, spend
release or automatic capacity release. Any manual action or rollout needs its
own authorization.

## Gate A remains open

API and SBE must agree the closed installed command/result/exit fixtures, exact
same-call terminal and nonterminal proof, outcome/checkpoint table, clock and
parent-fence behavior, operator visibility, and provider-free matrix. The
earlier synthetic argv digest and source findings remain useful; earlier
reconstruction proposals are not release criteria. A new bounded profile,
candidate wheel, release, deploy and paid QA remain later, separate gates.
