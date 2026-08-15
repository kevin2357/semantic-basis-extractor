# Slice 3 Durable Mutation and Replay

Status: complete; pending review and commit

## Public Python operation

The supported implementation now exists at:

```python
astrowoof_natal_authoring.lifecycle.deny_providerless_actions(
    run_dir,
    request,
    *,
    decision_at=None,
    event_emitter=None,
)
```

It accepts no provider/client parameter and has no path to submission, polling,
cancellation, or reconciliation. CLI exposure and event emission remain scheduled
for Slice 5.

## Successful transition

Under one acquisition of the existing cross-process lock, the operation:

1. strictly validates the request;
2. validates the complete current workspace snapshot;
3. recognizes an exact durable replay before ordinary stale evaluation;
4. otherwise performs Slice 2's all-members preflight against one decision basis;
5. constructs every action-local denial and one versioned batch record in memory;
6. stages the batch record;
7. persists `run.json`, `public-run.json`, and the authorization-request projection
   through one `persist_state()` call and therefore one revision advance;
8. promotes the batch artifact;
9. publishes and validates one new complete workspace snapshot; and
10. returns ordered member results plus the shared post-mutation observation and
    result checkpoint.

Every selected action becomes `DENIED_PROVIDERLESS`. Existing positive
authorization evidence is retained, and each action points to the exact batch
request digest and shared durable artifact. Unrelated actions are unchanged.

## Exact replay

The native state maintains a digest-keyed batch registry containing the complete
canonical request, locked decision basis, exact member evidence, result revision,
artifact path, and commit time. Replay requires:

- the same complete canonical request and digest;
- a currently valid complete workspace snapshot;
- the exact durable batch artifact bytes; and
- every member still carrying the corresponding native batch-denial evidence.

An exact replay returns `applied: false`, top-level and per-member
`idempotent_replay`, and no additional write or revision advance. Immediate replay
is byte-stable and returns the same shared checkpoint. If later legitimate native
mutations advance the workspace, replay reports the then-current verified snapshot
checkpoint while preserving the original request and decision basis; the API's
retained first-application result remains the historical checkpoint authority.

Reordered, partial, changed-reason, changed-authority, or changed-binding requests
produce a different digest and are not replay. They are evaluated normally and
fail closed when the targeted actions are already denied.

## Terminal and provider boundaries

The regression fixture remains `DELIVERY_COMPLETE` throughout. Exact deck and
delivery SHA-256 values are unchanged after mutation and replay. This is disposition
of unused authority, not reopening or rewriting accepted delivery.

No provider object is accepted by the public signature, no provider implementation
is constructed, and all qualification is provider-free.

## Durable-write qualification boundary

This slice proves correct uninterrupted mutation and replay. The protocol already
uses staging, atomic individual-file replacement, one revision transition, and one
final snapshot. It does not yet claim recovery from interruption at every write
boundary. Slice 4 will inject failures after staging, state persistence, artifact
promotion, and snapshot publication, then add constrained exact recovery.

## Gate evidence

- Focused batch suite: 11 passed.
- Full repository suite: 289 passed.
- Existing single-action lifecycle tests remain green.
- Provider operations: 0.
- Paid spend: $0.
- API key: not used.
