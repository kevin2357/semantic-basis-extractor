# Ambiguous Provider Submission Contract Proposal

Status: Scenic Waypoint 1 candidate; pending joint API review

## Decision

Publish a fresh closed result pair:

- `astrowoof.external_authority_provider_dispatch_result.v3`
- `astrowoof.external_authority_v2_command_result.v2`

The command remains the external-authority **v2 execution command**; `v2` in the
command identity refers to that authority protocol. The command-result schema's
own version advances from v1 to v2 because its embedded dispatch result advances
from v2 to v3 and adds a new outcome.

The existing dispatch v2 and command-result v1 contracts remain readable and
historically truthful. They are not reinterpreted. In particular, historical v2
`ambiguous_submission` never proves provider I/O was absent.

## Closed outcomes

### `pre_provider_refusal`

SBE proved that provider I/O was not attempted for the refused member.

Required joins:

- `provider_io_disposition = not_attempted`
- `grant_invocation_disposition = refused`
- exactly one `refused_action_id`, at the ordered position immediately after any
  previously provider-bound prefix;
- no ambiguous action;
- no provider operation for the refused member;
- a safe prepared-create digest binding the exact failed materialization attempt;
  and
- one closed refusal reason.

The exact grant invocation is sealed as refused and is never replayable. The
action and run are not terminalized by this result. Any later attempt requires a
fresh supported SBE lifecycle inspection and a fresh API authority decision.
There is no implicit retry, regrant, or reuse.

Closed reasons:

- `request_payload_unavailable`
- `request_payload_ambiguous`
- `request_payload_digest_mismatch`
- `provider_configuration_invalid`

### `ambiguous_submission`

SBE durably crossed the exact provider-call fence but lacks a durable unique
provider identity for the selected member.

Required joins:

- `provider_io_disposition = create_entered_unknown`
- `grant_invocation_disposition = create_entered_unknown`
- exactly one ambiguous member immediately after any durable provider-bound
  prefix;
- no refused member; and
- a safe prepared-create digest for the ambiguous member.

The ambiguous member is permanently non-create-eligible. Absence of a provider
ID does not prove absence of provider submission.

Closed reasons:

- `provider_call_interrupted_after_fence`
- `provider_transport_failed_without_identity`
- `provider_returned_invalid_identity`
- `provider_identity_conflict`

The first reason represents interruption immediately after the durable fence,
before a more specific transport result is available. The second represents a
transport-entered error without durable identity. Neither grants retry authority.

### `detached_provider_pending`

Every ordered member has one durable unique provider identity.

Required joins:

- `provider_io_disposition = provider_identity_durable`
- `grant_invocation_disposition = provider_pending`
- provider-bound inventory equals the complete ordered inventory;
- provider-operation count equals the bound-action count;
- no ambiguous or refused member; and
- reconciliation is the only supported continuation.

### `exact_replay`

The command returns an already durable provider-pending conclusion without new
provider I/O or native transition.

Required joins:

- `provider_io_disposition = provider_identity_durable`
- `grant_invocation_disposition = replayed`
- complete provider-bound inventory and provider-operation identities; and
- no ambiguous or refused member.

The result replays the prior durable conclusion; it does not assert that provider
I/O happened during the replay invocation.

## Why the provider-I/O field is not a boolean

`provider_io_performed` cannot represent all safe conclusions:

- `false` could mean proven no attempt or merely no new I/O during replay;
- `true` cannot distinguish durable provider identity from uncertain call entry;
- an unknown create result is neither safely true nor false in the sense needed
  for custody decisions.

The closed `provider_io_disposition` therefore records the native custody fact:

- `not_attempted`
- `create_entered_unknown`
- `provider_identity_durable`

The separate `grant_invocation_disposition` records what happened to the exact
request/grant invocation:

- `refused`
- `create_entered_unknown`
- `provider_pending`
- `replayed`

These fields are jointly constrained by outcome in both JSON Schema and strict
Python semantic validation.

## Prepared-create evidence

`prepared_create_records` is an ordered inventory for the attempted prefix. Each
record carries only:

- `action_id`
- `prepared_create_sha256`

The digest must bind the immutable, locally prepared call material and its
unchanged checkpoint basis. Its precise digest basis will be frozen with the
runtime adapter in Scenic Waypoint 2. It must include enough identity to prevent
substitution of action, request, model/output policy, route, or local request key.
It must not expose payload bytes, prompts, subject data, credentials, protected
provenance, or API-global reservation identity.

For a refused member, the digest identifies the failed prepared-create attempt's
safe basis even when complete provider-ready material could not be produced. The
runtime design must define a canonical failure-basis digest rather than hashing
an exception message.

## Ordered inventory rules

- Ordinary external-authority v2 action sets remain lexically ordered by
  canonical `action_id`.
- Provider-bound actions form an exact prefix.
- The one refused or ambiguous action, when present, is exactly the next ordered
  member after that prefix.
- Provider operation IDs correspond one-to-one with the bound prefix.
- Prepared-create records correspond exactly to the processed prefix: bound
  members followed by the refused or ambiguous member, if any.
- Members after a refusal or ambiguity are provably unentered by this invocation.

## Command result

`astrowoof.external_authority_v2_command_result.v2` embeds one dispatch v3 result
and, when the same invocation committed intent, its existing intent result v2.
The command and dispatch outcomes must match. When intent is present, request,
grant, and ordered action inventory must join exactly.

CLI exit status remains non-authoritative. The supported reader/validator and
sealed result bytes determine consumer behavior.

## Consumer disposition

| Native outcome | API capacity | API reservation/custody | Provider-create authority |
|---|---|---|---|
| pre-provider refusal | release | release exact unspent reservation only after validating `not_attempted`; retain grant audit | none; fresh inspection and grant required |
| ambiguous submission | release | retain specific ambiguity/review custody | permanently prohibited for ambiguous member |
| detached provider pending | release | retain retrieval-only custody | prohibited |
| exact replay | unchanged | unchanged | none |
| malformed/contradictory bytes | API fail-closed policy | preserve relevant authority for review | none |

API joins its reservation/admission identity from its own durable record. SBE
does not assert that API-global fact.

## Validation boundary

JSON Schema closes fields, primitive types, vocabularies, and outcome-dependent
field combinations. Python semantic validation additionally enforces:

- canonical action IDs and lexical order;
- exact bound/refused/ambiguous prefix position;
- provider-operation cardinality;
- prepared-create record ordering and digest shape;
- outcome/reason/disposition agreement;
- request/grant/intent/command joins; and
- canonical result and command digests.

This strict Python layer is required because `jsonschema` remains optional in a
supported lean environment.

## Fixtures

The packaged provider-free fixture bundle contains:

- missing payload;
- duplicate payload;
- payload digest mismatch;
- invalid provider configuration;
- interruption immediately after the call fence;
- transport-entered failure;
- malformed provider identity;
- conflicting provider identity;
- detached provider-pending;
- exact replay; and
- contradictory public evidence expected to fail validation.

The fixtures contain no request payload, prompt, subject parameters, credential,
authorization header, or protected provenance.

## Aggregate invocation refusal

An ordinary-action-set grant is one ordered invocation. If preparation refuses
member `i`, the exact old grant invocation is sealed and cannot execute any
remaining member. The result records the provider-bound prefix and the single
causal refused action; the untouched suffix is derivable from the ordered
inventory. SBE preserves the bound prefix in retrieval custody and restores
every provably unentered suffix member to `PREPARED` only after archiving its
exact authorization/consumption evidence with the refused invocation.

If a provider-bound prefix exists, its reconciliation has native precedence.
Once that custody is resolved, a fresh lifecycle inspection may expose a fresh
ordinary-action request for the eligible suffix. Neither generic resume nor the
old request/grant can create again.

`checkpoint_changed_before_create` is a closed pre-provider refusal: the
prepared-create digest remains bound to the actual preparation snapshot, the
second writer observes that the snapshot changed, and no call fence or provider
I/O occurs.

## Questions for Waffle Checkpoint 1

1. Approve the dispatch v3 and command-result v2 field/vocabulary set?
2. Approve the distinction between provider-I/O disposition and exact grant
   invocation disposition?
3. Approve the four pre-provider and four ambiguity reason codes?
4. Approve the ordered prepared-create digest inventory, subject to freezing its
   exact digest basis in Scenic Waypoint 2?
5. Confirm a pre-provider refusal is nonterminal but permanently consumes/seals
   that exact grant invocation.
6. Confirm the fixture matrix is sufficient for API consumer implementation.
