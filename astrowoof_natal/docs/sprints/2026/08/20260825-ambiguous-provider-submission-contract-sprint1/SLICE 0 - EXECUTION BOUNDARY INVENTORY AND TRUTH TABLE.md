# Scenic Waypoint 0 — Execution Boundary Inventory and Truth Table

Status: complete; paused at Waffle Checkpoint 0

## Confirmed production boundary

The external-authority v2 execution bridge currently has two nested concepts of
"create":

1. `dispatch_external_authority_v2_intent()` durably records
   `active_create_state = CALL_ENTERED`, releases the writer, and calls a supplied
   `create(action)` callback.
2. The production CLI's callback then resolves the exact request payload,
   constructs the OpenAI provider, derives the request key, and calls
   `create_response_only()`.

Consequently, callback entry and provider-transport entry are not the same
boundary. The current broad callback exception handler cannot distinguish them.

## Initial provider-free reproduction

The frozen test uses the real public intent commit, production-shaped request
artifacts, snapshot writer, dispatcher, and request-payload resolver.

| Injection/condition | Callback entered | Provider transport called | 0.4.22 native result/state | Correct target classification |
|---|---:|---:|---|---|
| failure immediately before `CALL_ENTERED` persistence | No | No | exception; intent remains replayable | proven pre-provider failure/refusal |
| missing exact request payload, detected inside current callback | Yes | No | `ambiguous_submission`; action becomes `AMBIGUOUS_PROVIDER_SUBMISSION`; `provider_io_performed=true` | `pre_provider_refusal` + `not_attempted` |
| transport callback raises after actual call entry | Yes | Yes/unknown | `ambiguous_submission` | `ambiguous_submission` + `create_entered_unknown` |
| provider returns a valid unique Response ID | Yes | Yes | `detached_provider_pending` | detached + `provider_identity_durable` |
| provider identity was already durably checkpointed | No new call | No | `exact_replay` | replay of sealed prior conclusion |

The second row confirms the motivating SBE defect independently of the frozen QA
cohort: a deterministic local request-materialization failure currently produces
provider ambiguity and asserts provider I/O even though the scripted transport
call count is exactly zero.

The same result is reproduced through the supported public CLI entry point. A
patched local payload resolver fails, the patched OpenAI transport records zero
POSTs, the CLI exits with its current non-success code 3, and the public command
result reports `ambiguous_submission` for the first ordered action.

## Complete boundary truth table

| Boundary/result | Provider transport calls | Durable native evidence | Current public classification | Required vNext classification |
|---|---:|---|---|---|
| snapshot/request/grant/action revalidation refusal | 0 | prior checkpoint unchanged | typed execution error | typed refusal/invalid evidence, not ambiguity |
| before-provider-create injection | 0 | intent remains `INTENT_COMMITTED`; no active action | exception; no sealed dispatch result | `pre_provider_refusal` only if returned as a supported result |
| missing/duplicate/digest-mismatched payload resolution in callback | 0 | action and intent become ambiguous | `ambiguous_submission`; `provider_io_performed=true` | `pre_provider_refusal` + `not_attempted` |
| local provider construction/configuration failure in callback | 0 | action and intent become ambiguous | `ambiguous_submission`; `provider_io_performed=true` | `pre_provider_refusal` + `not_attempted` |
| failure after durable call fence, before/within transport return | 1 or unknowable | action and intent ambiguous | `ambiguous_submission` | `ambiguous_submission` + `create_entered_unknown` |
| provider returns missing/malformed identity | 1 | action and intent ambiguous | `ambiguous_submission` | `ambiguous_submission` + `create_entered_unknown` |
| provider returns identity already bound elsewhere | 1 | earlier bound member remains durable; conflicting member ambiguous | `ambiguous_submission` | ambiguity with exact bound/ambiguous inventories |
| crash after valid return, before identity checkpoint | 1 | durable `CALL_ENTERED`; no identity | replay refuses | ambiguity + `create_entered_unknown` |
| crash after durable identity checkpoint | 1 | identity and cursor durable | resumes only later unentered members | provider identity durable; never recreate bound member |
| all identities durable | one per selected member | all actions `WAITING`; intent provider-pending | `detached_provider_pending` | detached + `provider_identity_durable` |
| exact dispatch replay after all identities | 0 | authoritative bytes unchanged | `exact_replay` | replay + prior durable conclusion |

Existing focused tests already cover malformed return, duplicate identity,
post-return/pre-checkpoint interruption, post-identity interruption, competing
dispatcher exclusion, exact replay, and event-sink failure isolation. The new
Scenic Waypoint 0 tests freeze the missing distinction between callback entry and
transport entry, including the actual public CLI.

## Recommended internal boundary

Introduce an internal prepared-create value produced before the ambiguity fence.
It should contain only the already validated material needed to make exactly one
provider call: action identity, request/binding identities, immutable request
payload, provider/transport configuration, local request key, and safe diagnostic
summary. It must contain no newly authoritative claim and must remain joined to
the unchanged native checkpoint.

The dispatcher should:

1. materialize that value before `CALL_ENTERED`;
2. reacquire the writer and revalidate the unchanged action/intent/checkpoint;
3. durably record call entry for the exact prepared value;
4. release the writer and invoke a transport-only callable; and
5. durably bind the identity or ambiguity before considering another member.

This avoids exception allowlisting and places the fence immediately before the
operation that can actually cross the provider boundary.

## Versioning recommendation

The tri-state provider-I/O/custody assertion and new `pre_provider_refusal`
outcome cannot be expressed truthfully by the current provider dispatch v2
schema, whose validator requires `provider_io_performed=true` for ambiguity and
knows no refusal outcome. Recommend:

- `astrowoof.external_authority_provider_dispatch_result.v3`; and
- `astrowoof.external_authority_v2_command_result.v2`, embedding dispatch v3.

Historical dispatch v2 ambiguity must remain ambiguous. It cannot be upgraded to
pre-provider refusal because the old result did not preserve the required proof.

## Safety conclusion so far

The current behavior is conservative against duplicate work but semantically too
coarse. The correction must move deterministic materialization before the
durable call-entered fence. It must not weaken the existing rule that any crash
after that fence without a durable identity is permanently non-create-eligible.

## Waffle Checkpoint 0 questions

1. Approve the prepared-create/transport-only internal split?
2. Approve dispatch result v3 plus command result v2 as the versioning shape?
3. Should a before-fence refusal consume/terminalize the existing native grant,
   or remain a sealed failed invocation whose later action policy is decided by a
   separate explicit authority transition?
4. Confirm historical v2 ambiguity remains review-only and is never inferred to
   mean pre-provider refusal.
