# API review — Slice 3 cooperative safe-point integration

## Decision

**Voof-paws D approved.** SBE may proceed to the separately gated Slice 4
cross-package supervision qualification. This approval does not authorize a
live suspension request, provider call, R2 access, API lease/capacity release,
process termination, packaging, release, or deployment.

## Review

The runtime hook remains inside the existing native writer-held mutation
windows and is restricted to the previously approved exact-interactive
ordinary-v2 cells. In dispatch it observes only after durable intent, before
provider POST, and after durable provider identity or ambiguous-return state;
in reconciliation it observes before provider GET and after a durable response
checkpoint. The result path preserves the required ordering: the observation
checkpoint precedes result/index, receipt, retained snapshot/basis, and the
exact command handoff.

The implementation preserves the essential ownership boundary. A cooperative
publication exits the native command with an exact result/receipt envelope, but
does not signal or kill a process, fence API authority, or release API,
provider, spend, workspace, or native custody. Unsupported bounded and Batch
routes reject an attached observer rather than silently accepting it. Existing
ordinary terminal/delivery evidence remains dominant when it validates through
the normal native reader.

## Verification

Ran the focused provider-free Slice 3 source cell against the reviewed source,
with bytecode writes disabled:

```text
Ran 11 tests
OK
```

Slice 4 must prove the real API subprocess adapter supplies the exact
pre-launch envelope/control-root pair, handles the cooperative exit as an
evidence handoff rather than generic child death, and keeps worker-execution
reclamation separate from every remaining custody class.
