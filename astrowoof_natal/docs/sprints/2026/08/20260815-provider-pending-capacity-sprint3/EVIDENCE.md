# Provider-Pending Capacity Release Sprint 3 Evidence

## Planning baseline

```text
SBE release baseline: 0.4.2
latest immutable tag: astrowoof-natal-authoring-v0.4.2
implementation started: false
provider operations: 0
paid spend: $0
API key used: no
```

Initial code inspection established:

- public inspection computes provider continuation from necessary native actions;
- `WAITING_FOR_RESPONSE` also creates blocking local dependency
  `provider_result_reconciliation / provider_result_pending`;
- public quiescence is therefore `not_quiescent` while provider work remains;
- interactive Responses persist provider ID and waiting state, then can resume
  polling from a fresh process;
- the main coordinator publishes a complete snapshot after worker threads unwind;
- Batch already supports detach, but interactive Responses use a local polling
  timeout rather than a supported poll-once cycle; and
- no public durable `resume_not_before` currently exists.

No runtime test or mutation has been performed during planning.

## API review disposition

Accepted before implementation:

```text
resume_not_before: durable SBE lower-bound recommendation
early bounded resume: typed not_due, no provider poll
financial authority: API-owned; SBE emits custody-retention action evidence only
bounded cycle: small frozen wall-clock ceiling includes HTTP retrieval timeout
SBE cohort: native fresh-worker/bounded-resume proof
API cohort: actual capacity release and third-reading admission proof
required route: full exact interactive pipeline across every enabled stage
secondary routes: explicit parity-supported or fail-closed/deferred classification
```

## Slice 0: exact baseline

Committed planning baseline:

```text
1b47808 docs: plan provider pending capacity release
```

Provider-free fixture:

```text
run status: WAITING_FOR_RESPONSE
paid actions: 3
action state: WAITING x3
durable provider IDs: resp_provider_pending_1..3
snapshot valid: true
fresh-process inspection: pass, no mutation
provider continuation: true
local continuation: true
quiescence: not_quiescent
closeout: continuation_required
unresolved action IDs: 3
public capacity-release conclusion: absent
public next due time: absent
```

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_background_timeout_preserves_response_for_same_attempt_resume \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_pending_background_response_does_not_consume_a_retry \
  astrowoof_natal.tests.test_provider_pending_capacity -v
Ran 5 tests in 3.883s
OK
```

Complete suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 313 tests in 160.785s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no. Runtime release remains
0.4.2.
