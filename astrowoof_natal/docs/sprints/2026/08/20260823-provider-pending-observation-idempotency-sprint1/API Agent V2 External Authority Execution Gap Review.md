# API Agent V2 External Authority Execution Gap Review

Date: 2026-08-24  
Status: implementation follow-up requested; no provider operation is authorized by this document

## What the fresh QA cohort proved

The fresh Juniper/Pepper cohort successfully completed the six-member initial
authoring-wave creates and later provider reconciliation. The API's capacity
head-of-line scheduler defect was corrected independently: the retained
slot-holder reclaimed its turn and reached the expected post-reconciliation
native lifecycle decision without a duplicate provider create.

The next decision for Pepper is:

```text
execution_branch_command = await_external_authority
reason_code = spend_authorization_required
external_authority_request.schema_version =
  astrowoof.external_authority_request.v2
```

That is correct temporal-lifecycle evidence. It also exposes an incomplete
release pair: API can validate and persist the v2 *reference*, but no supported
SBE provider-capable command consumes a v2 request plus an exact v2 grant.

The current API deliberately fails closed rather than fabricate a v1 grant from
v2 inspection material. That is the right safety behavior. It currently returns
an inert result, however, and the worker then reclaims the same retained slot on
its normal retry cadence. No new provider work or spend is created, but this is
not a stable waiting state: it consumes attempts and blocks that capacity slot.
The QA SBE worker was suspended after this was established.

## Review conclusion

`external_authority_request.v2` must not be treated as an executable authority
contract until SBE supplies the corresponding constrained execution boundary.
The API must not:

- reconstruct a v1 authorization from a v2 request or raw inspection;
- choose its own due members or provider operation identities;
- treat the request reference alone as an authorization;
- run generic resume as a substitute for the missing v2 command; or
- re-create, retrieve, cancel, or otherwise mutate retained provider work while
  implementing this seam.

This is a narrow paired-contract patch, not a reason to revert the v0.6
checkpoint-basis/temporal-decision separation.

## Requested SBE public boundary

Add one explicit provider-capable continuation command for the v2 request.
Naming is SBE's choice, but its contract should include all of the following.

1. **Exact inputs**
   - a previously validated `external_authority_request.v2`;
   - a closed, versioned API grant/authorization envelope bound to the request
     digest, checkpoint-basis digest, run identity, exact ordered action IDs,
     and complete public bindings; and
   - the usual native exclusive-access declaration.

2. **Single-writer revalidation fence**
   Before any native mutation or provider I/O, reread and validate the current
   snapshot and prove it still joins to the exact v2 request and grant. Reject
   stale basis, changed ordered inventory, changed binding, changed route,
   changed provider identity, changed action status, missing custody, or a
   mismatched grant with typed refusals.

3. **No long provider call under the fence**
   The fence may atomically record the durable authorization/dispatch intent,
   then release exclusive access before slow provider create/retrieval. A later
   supported reconciliation command remains the only path that observes and
   checkpoints provider results.

4. **Explicit waiting semantics**
   When no compatible v2 grant is present, native lifecycle should expose a
   quiescent/blocked `await_external_authority` state that does not cause a
   worker to repeatedly consume attempts or retain execution capacity merely by
   reinspection. API admission should make it runnable only when it has a
   compatible grant to present.

5. **Provider-free qualification**
   Include fixtures proving initial wave -> pending release -> reconciliation ->
   v2 request -> exact v2 grant -> constrained dispatch, plus stale/changed
   basis, action-order, binding, grant, and replay refusals. The fixture must
   prove no duplicate provider create and must cover a four-of-six
   reconciliation followed by the remaining two actions.

## Matching API work, after SBE is released

API will:

- use SBE's packaged v2 reader/validator rather than reconstructing fields;
- persist the exact request reference under API-owned spend/capacity policy;
- create a closed grant with ordinary admission, reservation, lease, and
  custody evidence;
- invoke only the supported v2 constrained command;
- persist the returned native result and terminal/next lifecycle decision; and
- distinguish `awaiting grant` from retryable worker failure so capacity and
  attempts are not churned while an operator or policy decision is pending.

The initial paired QA exercise should be provider-free. A retained paid run may
only be resumed after the exact execution contract, installed-wheel fixtures,
and the explicit owner authorization for that run have all been reviewed.

## Suggested release gate

Do not declare a v2 lifecycle release pair production-ready until the installed
SBE wheel and API integration demonstrate:

```text
v2 inspection
  -> exact request/basis join
  -> API admission and exact grant
  -> SBE fenced v2 execution
  -> provider-pending release
  -> supported reconciliation
  -> new checkpoint / next decision
```

with no duplicate create, no raw-state inference, no leaked protected payload,
and no capacity/attempt loop while awaiting authority.
