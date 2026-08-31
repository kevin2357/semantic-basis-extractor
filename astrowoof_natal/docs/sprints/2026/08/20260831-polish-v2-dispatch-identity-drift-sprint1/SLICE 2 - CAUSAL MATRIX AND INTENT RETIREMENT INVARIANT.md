# Slice 2 — causal matrix and intent-retirement invariant

## Classification

The incident contains three distinct findings:

1. **Proven SBE runtime lifecycle defect:** normal completion of an ordinary v2
   provider action does not retire its singleton live dispatch intent. A later
   independent ordinary v2 action is therefore rejected before provider I/O.
2. **Proven diagnostic conflation:** adjacent v1 standalone, lifecycle-embedded
   v1, and v2 request digests were all logged as request identities. The v2
   request itself remained stable in every observed constrained attempt.
3. **Adjacent evidence-ceiling issue:** local-work progress failed an append-only
   history check. Generation 11 does not retain the transient prior inspection
   needed to identify the missing historical key, and that failure is not needed
   to explain the stale-intent refusal.

This is not an API grant defect, provider failure, polish-specific binding
problem, or license to clear arbitrary intents.

## Field-level causal matrix

| Evidence plane | Creative-retry predecessor | Polish successor | Meaning |
|---|---|---|---|
| API request/grant | `e35ca8…` / `e09fbc…` | `07300b…` / `bb3aea…` | Two independent, internally coherent authorities |
| Native action | `paid_707…`, `REPORTED` | `paid_c90…`, `PREPARED` | Predecessor provider lifecycle ended; successor is providerless work |
| Provider identity | durable `resp_014d…` | none | No polish create occurred |
| Authorization/consumption | present and bound to predecessor grant | absent | Successor was not mutated before refusal |
| Reconciliation | `last_outcome=completed`, no resume time | not applicable | Predecessor provider custody is resolved |
| Reported evidence | usage and estimated cost present | absent | Predecessor settlement evidence is durable |
| Retained response artifact | exact ID, `status=completed` | none | Completed provider response is snapshot-bound |
| Singleton native intent | still `PROVIDER_PENDING`, inventory `[paid_707…]` | no intent can be committed | Live-slot state contradicts predecessor ledger truth |
| v2 command | old identities do not match supplied new identities | commit deferred; dispatch refused | Mechanical cause of the observed loop |
| Trace-only v0.5 requests | observation-time-bearing identities | observation-time-bearing identities | Not v2 mutation or authority |

## Live intent versus historical dispatch evidence

`external_authority_v2_dispatch_intent` is a live execution-control object. It
must represent at most one currently actionable, provider-pending, or ambiguous
v2 invocation. It must not remain the live authority after every member has
exact terminal predecessor evidence.

A completed intent should not disappear. Retirement converts it into immutable
historical dispatch evidence that remains usable for audit and exact replay, but
cannot block or authorize a new provider action.

## Exact retirement preconditions

Under the native lifecycle writer, retirement is permitted only when all of the
following hold:

1. The intent is strict-valid and its ordered inventory is nonempty, unique,
   lexical, and complete.
2. `next_action_index` equals the inventory length; `active_action_id` and
   `active_create_state` are null.
3. `provider_bound_action_ids` equals the complete ordered inventory and the
   ordered provider-operation inventory is complete and unique.
4. Every intent action resolves to exactly one ledger action whose complete
   binding, authorization document, authorization consumption, and consumer
   identity join the intent request/grant/member evidence.
5. Every ledger action has state `REPORTED`; no member is `PREPARED`,
   `AUTHORIZED`, `SUBMITTING`, `WAITING`, ambiguous, denied, or otherwise
   nonterminal for this dispatch.
6. Every ledger provider identity exactly equals the corresponding intent
   provider-operation identity.
7. Every member has completed reconciliation evidence with
   `last_outcome=completed` and no `resume_not_before`.
8. Every member has durable reported usage/settlement evidence. Unknown usage
   remains representable only through its existing conservative completed
   billing disposition; it must never be converted to zero.
9. Every member's retained provider-response artifact is snapshot-bound,
   strict-readable, has the exact provider ID, and carries the supported
   completed status.
10. No contradictory provider identity, call-entry ambiguity, partial dispatch,
    duplicate action, or mismatched request/grant/inventory evidence exists.

The retirement proof should bind a digest of the complete joined terminal
inventory, not rely on the string `REPORTED` alone.

## Atomic writer boundary

Normal retirement occurs under the writer in the same durable checkpoint that
first makes the complete terminal reconciliation/reporting evidence true. That
checkpoint must append the immutable retired-intent record and remove the live
slot atomically with the terminal action/evidence mutation. The live slot is
therefore truthful between actions; it is not lazily cleaned only when a future
action arrives.

At that terminal checkpoint SBE may do one of two things:

- leave the existing live intent untouched and refuse/retain/reconcile/review;
  or
- validate complete terminal predecessor evidence, append one immutable retired-
  intent record, and remove the live slot in one valid checkpoint.

A later independent request is then admitted through its ordinary constrained
writer fence and commits its own exact grant, inventory, authorizations, and
submission intent. It does not participate in normal predecessor retirement.
For older workspaces that predate retirement, successor admission may perform a
defensive compatibility repair only after revalidating the same complete
terminal join and recording the immutable predecessor retirement; that repair
must never become the steady-state timing model.

No valid checkpoint may expose the predecessor as retired without its retirement
record, expose terminal reported actions while their exactly joined intent still
occupies the live slot in newly written work, or expose authorizations for the
successor without the successor intent.
Provider I/O remains outside the writer and begins only after that checkpoint.

## Refusal precedence

Before considering retirement:

1. Call-entry or submission ambiguity → preserve ambiguity and require review;
   never clear or create.
2. Provider identity conflict or intent/ledger inventory mismatch → typed native
   evidence review; never clear or create.
3. Any `SUBMITTING`, `WAITING`, or provider-pending member → retain provider
   custody and use reconciliation only when SBE selects it.
4. Partial completion or missing terminal evidence → retain/refuse as incomplete;
   never infer completion.
5. Only the complete exact terminal join permits retirement and successor intent
   admission.

These safety facts outrank stale-basis or generic authorization errors.

## Replay rule

The immutable retirement record must retain at least the predecessor request and
grant digests, ordered action and provider-operation inventories, terminal
evidence digest, retirement revision, and post-checkpoint digest. A later exact
request/grant replay resolves to `exact_replay` from that record and performs no
authorization consumption, state reopening, or provider create.

A different request/grant may proceed only through a fresh current inspection,
fresh API authority decision, and the ordinary constrained writer fence.

## Compatibility and API boundary

- API continues to supply exact v2 inspection/request/grant/member documents;
  it does not select intent retirement or reconstruct terminal native evidence.
- SBE does not assert API reservations, leases, slots, or global admission.
- Existing pending/ambiguous intents remain fail-closed.
- Retained SBE 0.4.33 workspaces such as Delerium are diagnostic evidence, not
  authorized recovery targets.
- A public schema addition is not yet justified. Slice 3 must first prove the
  sequential production-path failure and the proposed retirement behavior
  provider-free.

## Oauf-paws 3 decision and Slice 3 proof target

Before runtime mutation, reproduce through real public boundaries:

1. first ordinary v2 dispatch → one scripted provider identity;
2. provider-free completed reconciliation and durable `REPORTED` evidence;
3. second independent ordinary v2 request/grant;
4. current behavior → exact stale-intent refusal and zero second create;
5. proposed retirement model → immutable predecessor retirement, exactly one
   successor create, and zero creates on replay;
6. pending, partial, ambiguous, identity-conflict, and malformed-artifact
   perturbations → no retirement and zero successor creates.

API Oauf-paws 3 approved this invariant with the timing correction above:
normal retirement belongs to the terminal reconciliation/reporting checkpoint,
while successor-time cleanup is compatibility repair only.
