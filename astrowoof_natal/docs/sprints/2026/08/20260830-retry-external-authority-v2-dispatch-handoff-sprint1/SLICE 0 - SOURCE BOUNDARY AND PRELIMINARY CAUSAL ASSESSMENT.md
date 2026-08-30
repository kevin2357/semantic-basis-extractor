# Slice 0 — source boundary and preliminary causal assessment

## Status

Source/public-contract characterization complete. Retained Diffie/Hellman R2
inspection subsequently completed. This document preserves the pre-inspection
source assessment; the authoritative retained-evidence conclusion is now recorded
in `SLICE 0 - DIFFIE AND HELLMAN SANITIZED TIMELINES.md`. In particular, Hellman
already had a sealed terminal-review result, so its correct next path was not a
fresh v2 dispatch.

## Released SBE behavior established from source and provider-free fixtures

### Custody and local-work precedence

`lifecycle._capacity_and_custody()` selects, in order relevant here:

1. due provider reconciliation;
2. completed provider evidence as local work;
3. scheduled provider custody as release-until-due;
4. other local work; and only then
5. prepared-action external authority.

The v0.7/v0.8 local-work projection makes completed retry fan-in explicit as
`provider_result_fan_in_and_retry_evaluation`. The prepared successor is not
advertised as the current external-authority inventory until that predecessor
operation is durably consumed.

### Generic authorization is intentionally insufficient

The ordinary semantic-closure CLI inspects authorization documents supplied via
generic `--spend-authorization`. If they would make an ordinary action
create-capable without the exact v2 request/grant boundary, it returns the closed
`astrowoof.generic_provider_dispatch_refusal.v1` result with:

- `outcome = pre_provider_refusal`;
- `reason_code = external_authority_v2_dispatch_required`;
- `new_provider_create_permitted = false`; and
- `next_step = inspect_lifecycle_and_invoke_external_authority_v2`.

It returns before applying the generic authorization. Provider I/O, run state,
snapshot bytes, local-work consumption, and native-result publication remain
unchanged.

### A complete supported handoff already exists

The packaged `astrowoof-post-fan-in-retry-qa` sequence proves:

1. provider retry not due;
2. exactly one scripted retrieval when due;
3. completed evidence selecting local fan-in;
4. durable local-operation consumption;
5. one prepared successor exposed by a fresh v2 request;
6. one exact v2 grant/document/intent;
7. exactly one scripted provider create;
8. detached provider-pending custody; and
9. exact replay with no duplicate create.

The qualification separately reports retrieval count, create count, duplicate
create count, external-network count, and spend.

## Newly frozen characterization

`test_retry_external_authority_v2_handoff_slice0.py` establishes three facts:

1. The same mixed-custody checkpoint projects an `ordinary_resume` local operation
   in lifecycle v0.7 and a coherent authorization-pending retry dependency in
   legacy v0.5. It therefore does **not** reproduce Diffie's strict-consumer
   failure from route shape alone.
2. Supplying the providerless successor's ordinary authorization to generic resume
   returns the typed refusal with zero provider create and byte-identical native
   state/snapshot.
3. The existing public qualification completes the intended retrieval → fan-in →
   fresh v2 authority → one create → replay sequence provider-free.

## Preliminary causal interpretation

### Diffie

The reported API exception—`SBE ordinary resume branch evidence is incomplete`—is
not reproduced by the current production-shaped mixed-custody fixture. Its v0.5
projection has `ordinary_resume`, `continue_local_cycle`, `local_work_ready`, one
blocking authorization-pending retry dependency, and no branch action IDs or
deadline. The corresponding v0.7/v0.8 projection also exposes the completed
predecessor as a closed local operation. Diffie therefore differed in at least one
consumer-critical field, or API consumed a different/stale inspection document.
The exact retained checkpoint and rejected document are needed before assigning
its failure to lifecycle versioning or native construction.

### Hellman

The repeated refusal is consistent with API invoking generic resume while attaching
an API authorization document for the prepared successor. SBE correctly refuses
that combination before consuming the completed predecessor's local fan-in. The
next inspection consequently remains `ordinary_resume`, and repeating the same
invocation produces a safe but capacity-holding loop.

The supported sequence is instead:

- invoke the selected local-only ordinary resume without create authority;
- inspect the successor checkpoint;
- consume the newly exposed v2 request;
- join API's spend decision to a fresh request-bound v2 grant/document set; and
- invoke constrained v2 dispatch.

This is currently the strongest explanation, but retained evidence must establish
that Hellman's first retry was completed native evidence rather than merely pending
dashboard evidence.

## Ownership assessment

No missing SBE schema or dispatcher capability is presently proven. The released
native contracts already express the correct sequence and refuse the unsafe one.
The likely correction class is API lifecycle-version adoption plus command routing:

- consume the newest supported v0.7/v0.8 local-work evidence and validate its
  closed operation inventory rather than inferring work from status alone;
- do not attach create authorizations to a local-only ordinary resume;
- treat generic refusal as a directive to re-inspect and complete the v2 handoff,
  not as a successful no-op or generic retry; and
- release capacity whenever no native local command is currently executable.

This classification remains provisional until the retained timelines and exact API
record joins are frozen.

## Remaining Slice 0 questions

- Which exact Diffie branch/capacity/dependency field violated the API's closed
  ordinary-resume predicate, and was the rejected inspection retained?
- Did Hellman have a native current-basis v2 request/grant, or only API admission?
- Which exact command arguments accompanied each repeated Hellman refusal?
- Were the provider retry results natively retrieved, or only visible in the
  dashboard?
- Did API receive and reject a public v0.7/v0.8 artifact before falling back to
  v0.5 mapping?
