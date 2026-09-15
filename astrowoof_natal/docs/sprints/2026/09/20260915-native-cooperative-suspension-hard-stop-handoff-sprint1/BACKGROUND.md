# Background

AstroWoof API Sprint 92 is designing an emergency containment operation for an
exact actively leased SBE job. Its first deliverable is an API-owned durable
force fence: revoke future ordinary authority immediately while preserving an
honest `ambiguous_fenced` posture when process and native outcomes are unknown.

The existing SBE `0.4.60` operator-quarantiner sprint delivered a different
capability: read-only disposition assessment of an exact checkpoint restored at
a non-authoritative path. That sprint is closed. Assessment cannot prove that
an active invocation observed a stop request, reached a safe native boundary,
or exited.

This companion sprint owns the prospective native half of cooperative
suspension and its exact handoff to API supervision. It does not make SBE the
owner of API jobs, leases, queue eligibility, process termination, capacity
accounting, provider cancellation, spend release, or retention policy.

## Frozen API inputs

API Gate A and Slice 1 establish these constraints:

- a raw PID or Render service operation is not exact-run authority;
- future-progress fencing is useful even without a native result;
- a supervision/invocation envelope must be created before `Popen`;
- a typed API `force_fenced` response means ordinary authority was revoked,
  not that SBE suspended or the child exited;
- job execution, run allocation, and provider/spend/workspace custody have
  distinct release rules; and
- cooperative signaling or exact forced termination remains behind joint Gate
  B review.

The authoritative API review materials are in:

- `astrowoof-api/docs/sprints/2026/09/20260910-forceable-run-quarantine-sprint92/SLICE 1 - DURABLE FORCE FENCE CONTRACT PROPOSAL.md`;
- `.../API RESPONSE - SBE GATE A FEASIBILITY REVIEW.md`; and
- `.../SBE POST SLICE 1 REVIEW.md`.

## Native problem

SBE can publish a truthful cooperative result only when the exact invocation
receives a canonical request through a launch-bound control channel and observes
it at a serialized lifecycle safe point. It cannot poll API database state,
retrofit semantic identity onto an already-running PID, or make an OS signal
handler into a checkpoint transaction.

The hard boundary is provider call entry. Suspension before entry can be clean;
a durably recorded provider ID preserves reconciliation custody; possible entry
without durable identity is explicit ambiguity. Process death cannot erase
that distinction.

## Governing invariant

```text
API durable force fence
  -> exact launch-bound request delivery
  -> SBE observes request at a native safe point
  -> SBE preserves/publishes exact checkpoint and custody evidence
  -> SBE emits one immutable suspension result/receipt
  -> API separately observes exact child exit
  -> API joins fence + native result + process fact
  -> API applies resource-specific release policy
```

No single item in that chain grants complete settlement authority.
