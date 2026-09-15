# Slice 0 — Native safe-point and provider-boundary inventory

## Decision

SBE has credible serialized seams for cooperative suspension, but it has no
current suspension request, launch-bound control channel, or stop-aware
coordinator. Existing `ASTROWOOF_INVOCATION_ID` support is logging correlation;
it is not the pre-launch supervision authority required by API Gate A.

The smallest viable implementation can cover exact interactive ordinary-v2
dispatch and reconciliation first. Direct legacy authoring, exact and bounded
initial-wave fan-out, bounded lifecycle, and Batch each have distinct
concurrency or provider mechanisms and must not be claimed merely because a
shared helper can read a request.

No runtime change was made in this slice.

## Current control-surface result

A source search found no suspension/force-fence request reader, control-channel
argument, signal handler, or coordinator stop hook. The only general invocation
binding is diagnostic logging context in
`application_logging.py:39-40, 215-225`. Native result publication separately
mints or reuses a native publication invocation ID in
`native_transitions.py:885-912`; that identity is created at publication time
and therefore cannot serve as API's pre-`Popen` supervision identity.

These three identities must remain distinct unless a future contract joins
them explicitly:

1. API pre-launch supervision invocation;
2. SBE diagnostic logging invocation; and
3. native result-publication invocation.

## Coordinator and safe-point matrix

| Route / seam | Current durable boundary | Candidate cooperative observation | Truthful immediate outcome | Bound / limitation |
| --- | --- | --- | --- | --- |
| Exact interactive ordinary-v2 intent | `commit_external_authority_v2_dispatch_intent()` validates under the lifecycle writer and persists intent plus snapshot before provider I/O (`external_authority_v2_execution.py:1209-1331`) | After writer acquisition and snapshot validation; again after complete intent checkpoint and before dispatch | Pre-provider suspension can preserve a committed, create-capable intent without provider ambiguity | Request observed before intent commit should publish no intent; request observed after commit must retain authorized intent without dispatching it |
| Ordinary-v2 per-action create | Dispatch validates persisted intent, prepares and checkpoints create evidence, calls provider, then records identity (`external_authority_v2_execution.py:1358, 1755-2022`) | Before preparation; after prepared-create checkpoint; immediately before provider create; immediately after provider return before identity persistence | Before create: checkpointed/quiescent suspension. After return without durable ID: `provider_boundary_ambiguous`. After durable ID checkpoint: provider custody known | No cooperative protocol can make the POST-to-ID interval atomic. A kill there remains ambiguous even if the provider actually returned |
| Interactive reconciliation selection | `reconcile_provider_cycle()` owns a single writer, validates the snapshot, and inspects lifecycle before retrieval (`reconciliation.py:375-445`) | After writer acquisition/validation and before selecting retrieval; before each due GET | Suspension before GET preserves known provider custody without performing retrieval | GET is retrieval-only; stopping it never permits resubmission or provider-custody release |
| Interactive retrieval and adoption | Retrieval occurs at `reconciliation.py:614`; result/custody mutations are persisted and snapshotted through `857-880`; ordinary orchestration publishes a result at `reconciliation.py:1965-2098` | After each retrieval response is durably stored; before local adoption; after adoption/checkpoint; before native result publication | Known provider identity, retrieved-unadopted, completed-adopted, or checkpoint-publication ambiguity | A suspension result must bind the exact post-retrieval checkpoint; generic latest discovery is forbidden |
| Direct legacy interactive pass | `OpenAIResponsesProvider.author()` performs POST and polling internally (`closure.py:1455-1602`); `author_one_pass()` persists consumer state around the complete provider call (`closure.py:4498-4760`) | Before provider callback; before each polling GET if provider loop becomes control-aware; after provider returns and before parsing/adoption; after attempt persistence | Clean pre-create, known-ID pending, completed-unadopted, or explicit ambiguity | Currently not bounded at arbitrary points inside transport. Supporting it requires threading a read-only control observer into the provider loop, not an outer-only hook |
| Exact initial-wave fan-out | Six actions cross a barrier after SUBMITTING becomes durable; POST occurs at `closure.py:3833-3941`; each returned ID is serialized into state and snapshot at `3944-4003` | Before any worker enters the pre-POST barrier; per-member immediately before POST; per-member after return; aggregate after all workers join | Aggregate pre-wave suspension, or a mixed member inventory of not-entered/known-ID/ambiguous | A single global stop observed after some members cross the barrier cannot truthfully promise zero remaining creates without coordinated barrier cancellation. Gate B must define partial-wave semantics |
| Bounded initial-wave fan-out | Mirrors the exact barrier/create/persist sequence (`bounded_lifecycle.py:1116-1243`) | Same positions as exact initial wave | Same member-level mixed custody classes | Separate route qualification is mandatory; shared conceptual shape is not proof |
| Optional polish/critic/candidate | Consumers run through `polish_subject()` and `run_qualitative_review()` with exact completed-evidence adoption (`closure.py:6667-7438`) | Before selecting each optional action; before provider create; after durable provider ID; before and after adoption; before saving finalization evidence | Stage-specific prepared, provider-pending, completed-unadopted, adopted, or ambiguous | Existing provider `complete_json()` polls internally (`closure.py:1675-1774`); mid-call responsiveness needs the same bounded observer integration as direct passes |
| Finalization / terminal publication | `finalize_subjects()` and `finalization_conclusion()` feed the main coordinator; finalization evidence is persisted before optional selection and native result publication (`closure.py:7439-7584, 9089-9243`) | After finalization persistence and before optional selection; before result publication; after exact receipt publication and before exit | An already committed terminal/delivery result dominates the stop request | Suspension must never replace an existing terminal/delivery result. API may keep the run fenced while consuming that result normally |
| Exact Batch authoring/reconciliation | Batch authoring persists repeated state transitions (`closure.py:4897-5378`); Batch reconciliation is a distinct writer and transport path (`reconciliation.py:917-1480`) | Before batch create; after durable batch ID; before batch retrieve; after member-result persistence; before local assembly/publication | Batch-not-entered, known batch custody, partial member custody, or ambiguity | Batch has aggregate/member cardinality and partial-result semantics. It is not approved for first implementation by analogy |
| Bounded ordinary lifecycle | `resume_bounded_run()` owns a separate coordinator and terminal short-circuit (`bounded_lifecycle.py:1258+`); CLI publishes native results separately (`cli/bounded_run.py:194-240`) | Entry after snapshot validation; before each stage/create; after provider identity; after local mutation; before CLI publication | Route-specific checkpointed, pending, adopted, terminal-precedence, or ambiguity | Requires explicit route fixture and public command-result proof; no automatic support claim |

## Shared publication seams

`checkpoint_spend_boundary()` (`closure.py:2885-2967`) is the strongest existing
ordinary coordinator seam. It already unwinds known spend/provider exceptions,
persists state, optionally commits local progress, and publishes a native
result. It is a good integration point for a cooperative request observed after
the protected mutation completes; it is not a safe mechanism for asynchronously
interrupting the mutation inside the context.

`publish_native_execution_result()` already supplies exact result/receipt
atomicity and same-invocation terminal command-result handoff. Suspension should
reuse its publication discipline but needs an additive closed result rather than
pretending an existing lifecycle result means “stopped.”

Reconciliation's `_emit_terminal_command_result()`
(`reconciliation.py:2098+`) correctly emits only exact delivery/review results.
A future suspension command result must likewise be emitted from the exact
result returned by the current invocation, never from latest-result discovery.

## Provider call-entry truth table

| Observation point | Durable evidence | Permitted native statement |
| --- | --- | --- |
| Before create eligibility or prepared-create commit | No provider entry | `suspended_checkpointed` or `suspended_quiescent_no_checkpoint_change`, with create explicitly not entered |
| After prepared-create/intent checkpoint, before POST | Exact authorized action and request evidence; no provider identity | Same successful outcomes, retaining the undelivered intent and prohibiting dispatch by this invocation |
| POST may have begun, no provider identity durable | Call-entry uncertainty | `provider_boundary_ambiguous` only |
| Provider ID durable, response incomplete/not retrieved | Exact provider custody | Successful suspension may report known provider custody; API must retain reconciliation authority and prohibit new create |
| Retrieval durable, adoption not durable | Completed provider evidence | Successful suspension may report completed-unadopted local work; no provider resubmission |
| Adoption/checkpoint durable | Exact native progress | Successful suspension may bind the new checkpoint and remaining work |
| Workspace mutation occurred, publication receipt absent/uncertain | State/publication mismatch | `checkpoint_publication_ambiguous` only |

## Safe-point implementation requirements discovered

1. The request observer must be read-only, deterministic, non-throwing for
   absence, and fail closed for malformed/stale/conflicting presence.
2. Observation must happen under the same lifecycle writer or coordinator
   serialization that protects the adjacent mutation.
3. Each observed request must be joined to the API pre-launch supervision
   envelope. The current logging invocation ID is insufficient.
4. A request noticed by one fan-out worker needs an aggregate cancellation/state
   protocol; a bare shared boolean can strand peers at barriers or misstate
   partial provider entry.
5. Provider polling can be cooperatively shortened only between HTTP calls.
   There is no truthful bounded stop inside a blocked transport call.
6. After ordinary native result/receipt publication, result precedence wins;
   the stop request becomes an API settlement/fence fact rather than a new
   native suspension result.
7. Suspension publication must not use relocated assessment authority, and a
   relocated workspace must reject the control channel before reading a request.

## Support classification for Gate B

| Route | Contract readiness | Recommended first implementation |
| --- | --- | --- |
| Exact interactive ordinary-v2 dispatch | High | Yes |
| Exact interactive response reconciliation/fan-in | High | Yes |
| Direct legacy interactive authoring/polling | Medium | Contract now; implement only with bounded provider-loop observer |
| Exact initial-wave fan-out | Medium/complex | Contract partial-wave behavior before implementation |
| Bounded interactive | Medium | Separate qualification after exact route |
| Exact/Bounded Batch | Low/complex | Defer unless Gate B explicitly scopes aggregate/member semantics |
| Terminal/delivery publication | High | Precedence rule required in first implementation |

## Voof-paws A questions

1. Does API agree that the first cooperative implementation may be exact
   interactive ordinary-v2 plus response reconciliation, while other routes
   fail closed as unsupported rather than pretending shared coverage?
2. For initial-wave fan-out, should a stop observed after any POST entry produce
   a mixed-custody suspension result after all in-flight member calls reach a
   bounded return, or should initial-wave cooperative suspension be deferred in
   v1 entirely?
3. Will API's pre-launch envelope expose one stable supervision invocation ID
   separately from SBE's native publication invocation ID, with both included in
   a suspension result?
4. Does API prefer a request-isolated atomic file channel for the first
   provider-free implementation, or is it prepared to own an inherited pipe
   across all subprocess adapters?
5. What exact observation proves a worker execution resource reclaimable after
   cooperative exit, while leaving run allocation and native/provider custody
   untouched?

Slice 1 contract field names remain paused until these questions and the route
scope are jointly reviewed.
