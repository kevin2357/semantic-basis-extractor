# Slice 2A — Reconciliation activation qualification

## Result

**No SBE runtime, schema, or release change is needed for the first completion
cell.** The existing native-suspension v1 producer already supports interactive
response `provider_reconciliation` at both approved safe points. API must
activate that existing producer by preparing the exact supervision envelope and
control-root request before launching the child, then retain the exact
same-invocation command handoff and parent exit evidence for its own final
transaction.

This is deliberately not a claim that SBE can release capacity. It cannot.
SBE publishes cooperative native evidence only.

## Verified native behavior

`reconcile_authoring_provider_cycle()` accepts `suspension_observer` and
reaches exactly these producer boundaries under its existing single-writer
posture:

| Boundary | Native posture | Required SBE behavior |
| --- | --- | --- |
| `reconciliation_before_provider_get` | Workspace snapshot validated; no response GET has started. | If the exact request validates, publish v1 cooperative result/receipt/command and stop before retrieval. |
| `reconciliation_after_response_checkpoint` | Bounded response GET wave completed; `run.json`, cycle record, and snapshot persisted. | If the request arrived during GET, publish the exact v1 handoff with retained completed-provider evidence and stop before another local cycle. |

`NativeSuspensionControlObserver` validates command-kind/safe-point alignment,
native-run identity, snapshot, precedence, capability/fence/request joins, and
the indexed replay result. Its command result carries the exact result and
receipt identities; an ordinary native result that precedes observation
suppresses cooperative publication.

## API invocation/consumer obligations

For the cooperative proof class, API must:

1. create the capability before child launch, then admit the exact later force
   fence and request;
2. pass the existing supervision-envelope and suspension-control-root inputs
   to the reconciliation child;
3. capture the exact returned command result rather than discover a “latest”
   native result;
4. validate every v1 join against the persisted run/job/attempt/lease/fence,
   native run, launch generation, control/workspace/checkpoint basis, and
   worker boot; and
5. separately prove the exact child/process group exited before transitioning
   the API disposition or releasing the named scheduling allocation.

Missing control input, stale or contradictory identity, unsupported batch
reconciliation, malformed handoff, absent parent exit, or any old-boot
artifact remains an unresolved API escalation. None may be converted into an
SBE capacity or provider fact.

## Provider-free verification

Executed from this checkout with `PYTHONPATH=astrowoof_natal/src`:

```text
python -m unittest astrowoof_natal.tests.test_native_suspension_runtime_slice3
Ran 11 tests ... OK
```

The focused suite covers the before-GET stop with zero retrievals, public
coordinator propagation, a request arriving during the bounded GET wave and
stopping after its checkpoint, ordinary-result precedence suppression,
replay behavior, identity refusal, and exact v1 handoff publication.

## Disposition

SBE's approved runtime-support slice is complete for the first interactive
reconciliation cell. No release candidate is warranted. The next joint gate
is API's provider-free parent/transaction consumer qualification, followed by
the already-planned cross-package transcript gate.
