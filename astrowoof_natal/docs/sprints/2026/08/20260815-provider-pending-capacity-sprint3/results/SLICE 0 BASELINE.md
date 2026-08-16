# Slice 0: Provider-Pending Capacity Baseline

## Outcome

The reported native/API seam is reproduced without provider work. SBE 0.4.2
durably preserves several known provider operations and supports byte-stable
inspection from a fresh process, but its public lifecycle contract cannot authorize
release of local execution capacity.

## Exact reproduced state

The baseline fixture contains three authorized and consumed native paid actions,
each in `WAITING` with a distinct durable OpenAI Response ID. Their parent passes
and run are `WAITING_FOR_RESPONSE`; the complete workspace snapshot is valid at its
stable logical absolute path.

Inspection reports:

```text
snapshot inventory_valid: true
terminal: false
provider_continuation_remains: true
local_continuation_remains: true
quiescence.state: not_quiescent
quiescence.reasons:
  - provider_continuation_remains
  - local_continuation_remains
local dependency:
  provider_result_reconciliation / provider_result_pending / blocking=true
provider identities present: 3
execution_capacity projection: absent
provider_custody projection: absent
resume_not_before: absent
```

Closeout returns `continuation_required` and lists all three exact action IDs in
`unresolved_action_ids`. It preserves all three provider IDs. This confirms that
native custody inventory already exists; the missing contract is whether the
fully checkpointed local process may release capacity and when a short resume cycle
is due.

## Fresh-process and process-authority findings

The installed-style lifecycle CLI in a separate Python process reads the same
snapshot and the same three provider identities without changing any workspace
hash. Existing provider tests prove a timed-out background Response:

- preserves its durable Response ID;
- does not consume a creative retry;
- resumes the same attempt with `GET` only; and
- performs no second `POST`.

Static orchestration inspection confirms parallel authoring futures are joined by
the `ThreadPoolExecutor` context before the coordinator's final `save_state()` and
snapshot publication. Provider state, attempts, paid actions, response markers,
and snapshot authority are persisted. No required correctness state was found only
in a resident thread or process after the command returns.

This does not yet constitute a public capacity-release guarantee. Slice 1 must
version that guarantee, and Slice 2 must bind it to explicit checkpoint evidence.

## Authority inventory

| Concern | Current authority | Slice 0 conclusion |
|---|---|---|
| Provider operation identity | SBE action/provider marker | Durable and fresh-process readable |
| Provider action necessity | SBE lifecycle action inventory | Durable; all waiting actions remain necessary |
| API reservation/dollar amount | API PostgreSQL ledger | Not represented or claimed by SBE |
| Snapshot/path integrity | SBE snapshot/workspace contract | Valid and required on fresh resume |
| Local work dependency | SBE lifecycle inspection | Provider reconciliation currently labeled blocking local work |
| Local capacity release | API allocation policy consuming SBE evidence | No supported SBE evidence exists yet |
| Next due time | Neither supported public contract | Absent |
| Event `native.quiescent` | Non-authoritative operational observation | Not equivalent to lifecycle quiescence |

## Verification

Focused provider-pending ladder:

```text
python -m unittest \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_background_timeout_preserves_response_for_same_attempt_resume \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_pending_background_response_does_not_consume_a_retry \
  astrowoof_natal.tests.test_provider_pending_capacity -v
Ran 5 tests in 3.883s
OK
```

Complete repository suite:

```text
python -m unittest discover -s astrowoof_natal/tests -p "test_*.py"
Ran 313 tests in 160.785s
OK
```

Provider operations: 0. Paid spend: `$0`. API key used: no.

## Gate assessment

Slice 0 passes. The throughput problem is reproduced precisely; durable provider
custody and fresh-process safety are present; public capacity release, due timing,
and bounded interactive polling are absent. No unrelated native correctness defect
or hidden process-only authority was found.

No production lifecycle behavior or public contract changed in this slice.
