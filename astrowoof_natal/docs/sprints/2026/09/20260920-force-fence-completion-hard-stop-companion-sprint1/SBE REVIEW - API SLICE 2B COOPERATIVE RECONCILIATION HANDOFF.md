# SBE review — API Slice 2B cooperative reconciliation handoff

## Decision

**Revision requested before Joint Slice 3.** The implementation takes the
right narrow route: it prepares reconciliation supervision before `Popen`,
publishes only the exact later fence request, rejects mixed/duplicate stdout,
uses SBE's public v1 reader, and keeps the final capacity transition in API.
It does not need a new SBE schema or wheel.

Two proof details must be made explicit before the provider-free installed-wheel
replay can serve as a completion gate.

## R1 — prove the sealed argv is the argv passed to `Popen`

`build_provider_reconciliation_command_sha256()` and
`provider_reconcile()` both call the same ordered-argv builder with the
expected workspace, observation timestamp, frozen arguments, envelope path,
and control-root path. That is a strong implementation shape.

But SBE receives only `command_sha256`; its public v1 reader validates the
envelope/request/result chain's **agreement** on that digest. It cannot
independently reconstruct or authenticate API's actual subprocess argv.

Add a provider-free runtime regression that intercepts the reconciliation
`Popen` call and asserts, byte-for-byte at the structured canonicalization
level, that:

1. the captured argv is the exact argv whose `{"argv": [...]}` SHA-256 was
   persisted in the pre-launch envelope;
2. it includes the same `--observed-at`, frozen arguments,
   `--supervision-envelope`, and `--suspension-control-root` paths; and
3. changing any one of those components changes the digest and refuses the
   completion path rather than permitting an alternate command.

This is an API launch-boundary proof; it is not an SBE claim that it can
recompute an API process invocation.

## R2 — replace parent-exit booleans with a durable exact receipt

The cooperative completion service presently writes only:

```text
parent_exit_observed: true
child_process_group_alive: false
```

Those are assertions, not the exact same-invocation/same-boot parent-exit
receipt required by Gate B. `Popen` returning does establish the direct child
has exited, but the release record must preserve and validate why it refers to
this child rather than any other process.

Before finalization, have the runtime create a sealed, immutable parent-exit
receipt (it may remain inside the existing immutable completion `evidence_json`
for this first cell) with at least:

- supervision invocation ID, launch generation, worker boot ID, native run,
  command kind, and persisted envelope/command SHA-256;
- the exact named suspension command/result/receipt/request identities;
- direct-child process identifier, observed return code, and parent-observed
  UTC exit time; and
- an explicit proof scope: `direct_child_exit` unless API actually launches
  and observes a separately controlled process group.

The finalizer must compare those fields to the locked persisted invocation,
fence, and validated handoff. A missing, substituted, stale-boot, or malformed
receipt must remain unresolved and retain the allocation. Do not call a direct
`Popen` return a process-group proof unless API has established such a group.

## Joint replay gate after R1/R2

1. Install the immutable SBE `0.4.66` wheel so the seven currently skipped
   package-resource reader cells run.
2. Run the exact provider-free reconciliation replay against that installed
   wheel: pre-launch envelope → exact later request → one v1 command handoff →
   verified direct-child exit receipt → locked final disposition.
3. Include tampered argv digest, wrong/missing parent receipt, stale boot,
   cross-run/fence substitution, duplicate/mixed stdout, ordinary precedence,
   and replay assertions. No provider call, workspace mutation, worker restart,
   or capacity release occurs outside the test database fixture.

## SBE conclusion

The first reconciliation producer cell remains unchanged and correctly bounded.
This is an API proof-recording and provider-free consumer qualification
correction; no SBE release is needed.
