# Slice 2 — native fence implementation and API review

## Status

Implemented provider-free and paused for API review. No release preparation or
retained-run recovery has begun.

## Implemented boundaries

### Typed generic refusal

An exact-interactive ordinary action presented through generic
`--spend-authorization` is identified before `apply_spend_authorizations()`.
Instead of consuming authority or entering provider code, SBE emits
`astrowoof.generic_provider_dispatch_refusal.v1` and returns exit 0.

The result is closed and content-digested. It binds the exact native run,
lifecycle-v0.8 checkpoint basis, snapshot SHA-256, state revision, and canonical
action inventory. It directs API to obtain a fresh lifecycle inspection. It does
not publish a native result because no native fact changed.

### Writer-fenced local-progress contradiction

`LocalWorkProgressContradiction` distinguishes semantic non-consumption from a
generic programming/transport exception. While `commit_local_work_progress()`
still holds the native writer, it seals:

- native execution result v0.2;
- cause `local_work_progress_contradiction`;
- complete ordered action dispositions and inventory digest;
- `new_provider_create_permitted=false`;
- journal range, full snapshot, and immutable publication receipt.

Only after publication completes does the command emit the exact terminal-review
command-result envelope and exit 2. A failing semantic-consumption check therefore
remains fail-closed without becoming an untyped queue retry.

### Existing real call-entry fence retained

No second call-entry implementation was added. Existing v2 dispatcher tests prove:

- aggregate intent is durable before provider work;
- `CALL_ENTERED` is checkpointed before adapter entry;
- interruption after entry is ambiguity, not replay;
- each returned identity is durable before the next member;
- exact replay performs no additional create.

## Applicability

- Included: exact-Natal interactive ordinary actions other than initial-wave
  members.
- Unchanged: initial-wave v1.
- Deferred: ordinary Batch, bounded-Natal, and historical duplicated-run recovery.
- Provider reconciliation remains retrieval-only.

## Focused evidence

36 tests passed; two optional `jsonschema` checks skipped on the lean interpreter.
The set covers:

- three new generic-refusal/local-contradiction tests;
- real external-authority v2 intent and dispatcher tests;
- provider-capable v2 CLI and replay;
- terminal-review schema, receipt, immutable action joins, interruption repair,
  writer contention, and event-sink isolation;
- the Slice 0 two-restore characterization.

External provider calls and retained-QA access: zero.

## Requested API review

1. Confirm exit-0 typed generic refusal maps to fresh lifecycle inspection and
   never `command_failed` or generic resume retry.
2. Confirm the refusal carries enough exact identity for API audit/routing without
   pretending it is a grant-bound v2 dispatch result.
3. Confirm `local_work_progress_contradiction` maps to stable operator review while
   API retains exact provider/reservation custody.
4. Confirm Slice 3 should publish API-shaped fixtures for both outcomes before
   installed-wheel qualification.
