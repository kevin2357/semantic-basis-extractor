# Completed creative retry cannot cross the external-authority v2 boundary

## Status

Investigation and contract-planning only. The paired API sprint is
`20260830-retry-external-authority-v2-dispatch-handoff-sprint58`.

## Triggering QA cohort

On 2026-08-30, a fresh two-run QA qualification cohort ran against the
reset/attested SBE `0.4.30` fleet. The owner-approved ceilings were USD 50 per
run, USD 100 per cohort, USD 150 rolling 24-hour, USD 49 per active stage, and
USD 0 for qualitative candidate.

The relevant API/native pairs are:

| Pup | API run | Native run |
| --- | --- | --- |
| Diffie 05d454e6 | `9cbc3c0c-9a5f-42ff-8fc0-cc23f08b75df` | `ee69cb149c4e533ff9e1341355ef2ce13246a5e8a2617b387da903ecfd58fa60` |
| Hellman ded0b618 | `bababdec-3f3d-4315-8dfc-e70c46dd6288` | `856e9c41085e954a964edc2963d2de64ccafbedfee81c5805a779abee2faf550` |

Both initial six-member waves reached authoritative API `reported` state.
Diffie then created two creative-retry provider actions; Hellman created one
creative-retry provider action and later acquired a second `authorized` retry
action with no provider identity. The owner observed all three retry Responses
as complete in the OpenAI dashboard. Those dashboard observations are useful
diagnostic evidence, but they do not authorize state mutation.

## Observed failure

Diffie failed at `2026-08-30T08:56:52Z`:

```text
reason_code: sbe.contract.provider_lifecycle
exception: SbeProviderContractError
detail: SBE ordinary resume branch evidence is incomplete
```

Hellman did not fail, but repeatedly made no forward progress. The current
SBE trace reports:

```text
status=AWAITING_SPEND_AUTHORIZATION
execution_branch=ordinary_resume
branch_reason=ordinary_local_continuation_ready
provider_actions=1
local_dependencies=1
```

The resulting generic provider dispatch then refuses, without provider I/O:

```text
reason_code: external_authority_v2_dispatch_required
new_provider_create_permitted: false
ordered_action_ids: [paid_bfce7b3ea385abe55a5045d1]
```

The same refusal repeated at least at `09:04:37Z` and `09:05:34Z`. The API
records Hellman's SBE job as `retry_wait`, while it retains the only active
capacity slot. This is a safe pre-provider refusal, but it is not a useful
self-cleaning outcome.

## Containment and facts

The QA SBE worker `srv-da12sktbedkc73btpu00` was suspended through Render's
supported service API after evidence capture. Render accepted the request with
HTTP `202`, and a programmatic service read reported `suspended`. No run,
provider action, reservation, lease, allocation, R2 object, or provider result
was mutated during containment.

At containment:

- Diffie: failed SBE job; its slot was released; two retry provider identities
  remained retained/unreported.
- Hellman: `retry_wait`; slot 1 active; one retry provider identity retained
  and one exact retry action authorized but undispatched.

## Problem statement

External-authority v2 currently protects a provider-create boundary. The
post-fan-in creative-retry path can nevertheless reach an ordinary-resume
selection with an API-side authorization already persisted, but without the
exact v2 dispatch envelope needed by SBE. SBE correctly refuses provider I/O.
The API then treats that receipt as quiescent/retryable instead of completing
the exact authority handoff or taking a typed, stable refusal path.

This sprint must determine the canonical public handoff for a retry action that
is already API-authorized but not yet provider-created. It must preserve these
boundaries:

- API remains the authority for spend admission and durable authorization.
- SBE remains the single writer for native lifecycle/dispatch validation.
- The API must not reconstruct private SBE branch state or synthesize a generic
  resume command.
- SBE must not create a provider request from an API authorization absent the
  exact validated v2 request/grant.
- Provider reconciliation and provider creation remain separate paths.
- Any unjoinable historical state remains typed review/refusal, not a made-up
  recovery.

## Initial questions for the SBE plan

1. Which public lifecycle inspection/request identifies the exact already-
   authorized retry action, binding and snapshot/revision for this path?
2. Is a new aggregate grant required, or can the existing v2 request/grant
   schema support a single ordinary retry with an explicit dispatch intent?
3. At what point does SBE distinguish retrieval-only reconciliation of the
   completed first retry from creation of the second authorized retry?
4. Which terminal/typed refusal must API persist if the next authority request
   cannot be joined exactly?
5. What provider-free matrix proves initial wave, retry-result reconciliation,
   fresh retry admission, and a no-duplicate resumption under the real public
   boundary?

No provider work, retained-run recovery, deployment, or release is authorized
by this background document.
