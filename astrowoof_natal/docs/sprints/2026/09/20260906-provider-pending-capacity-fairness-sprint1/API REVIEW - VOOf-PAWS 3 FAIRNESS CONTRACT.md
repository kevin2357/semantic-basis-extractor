# API review — Voof-paws 3 fairness contract

## Decision

Approved with implementation guardrails below. The causal classification is
correct: this is an API scheduling-policy issue over legitimate, distinct
native permissions, not an SBE contract gap. The first release should remain
API-only and closed to exact-interactive due reconciliation and completed-
evidence local work.

`N=1` is the right structural initial bound. It is intentionally a command-turn
bound, not a fabricated elapsed-time SLA. Capacity rotation releases no SBE
workspace, provider custody, authorization/grant/action identity, spend
reservation, checkpoint, or readiness.

## Required API implementation guardrails

1. **Do not identify local work from `ordinary_resume` alone.** The compact
   worker result carries `execution_branch`, but `ordinary_resume` is broader
   than the intended first-release case. Rotation for that branch must require
   the exact persisted, validated `SbeLocalWorkLifecycleDecision` whose reason
   is `local_work_ready`, whose native/run/checkpoint basis matches the command
   successor, and whose positive permission remains deterministic local work.
   Due retrieval must analogously use its exact validated provider-pending
   lifecycle decision; neither route may be inferred from status prose or a
   dependency count.
2. **Bind successor evidence to this command.** “Newer checkpoint” means an
   accepted checkpoint for the claimed API job/run, with generation strictly
   greater than the claim's checkpoint generation, accepted after the command
   returned normally. A merely latest/stale checkpoint is not enough. Missing,
   unchanged, contradictory, or unpersisted evidence is a no-rotation case.
3. **Make the rotation transition atomic and prove the peer can win.** Under
   the current queue ordering, defer A to the ordinary configured boundary and
   release only A's allocation in one transaction. Select from durable
   compatible ready peers, never from a log/elapsed-time observation. Tests
   must show B actually claims before A's ordinary defer matures; release alone
   is insufficient evidence of fairness.
4. **Keep the bound conditional and idempotent.** Rotation is evaluated only
   after a successfully completed actionable command when a compatible
   unallocated peer is already ready. If no peer is ready, A may retain/reclaim
   normally. Duplicate result delivery, release/reclaim races, and an atomic
   rollback must not consume a second turn, create duplicate provider work, or
   leave a stranded allocation.
5. **State the due-work bound precisely.** The first release promises no more
   than one successfully completed peer command plus queue handoff overhead
   *in the controlled compatible-peer scenario*. It is not a universal
   wall-clock guarantee and must not hide additional higher-priority work or
   unavailable peers in the qualification result.

## Required qualification additions

In addition to the proposed matrix, include direct production-boundary cells
for an `ordinary_resume` result whose persisted local-work decision is absent,
wrong-reason, stale, or checkpoint-mismatched: each must retain/fail closed,
not rotate. Include the same exact-binding negative for provider reconciliation.

With those constraints frozen, API is approved to begin Slice 4 implementation.
No SBE schema, runtime behavior, or release is required for this first API-only
correction.
