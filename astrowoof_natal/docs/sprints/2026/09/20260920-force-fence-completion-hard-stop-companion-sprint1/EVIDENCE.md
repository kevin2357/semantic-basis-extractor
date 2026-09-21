# Evidence register — force-fence completion hard-stop companion

| Item | Purpose | Status |
| --- | --- | --- |
| API Sprint 109 Slice 0 | Current force-fence/capacity admission facts. | Baseline. |
| SBE 0.4.66 qualification | Existing exact cooperative-suspension evidence and non-release scope. | Baseline. |
| Sprint 107 Q5-003 | Live unresolved retained-allocation/peer-block witness. | Diagnostic only. |
| Focused native suspension suite | `test_native_suspension_runtime_slice3`: 11 passing tests with checkout `src` on `2026-09-20`. | Slice 0 provider-free verification. |
| Slice 0-1 route/contract record | `SLICE 0-1 ROUTE INVENTORY AND CONTRACT PROPOSAL.md`. | Gate A input. |
| Joint Gate A reviews | API review in this sprint and `SBE Agent Gate A Review.md` in API Sprint 110. | Approved. |
| API Slice 1 provider-free model | `API Slice 1 Provider-Free Model Handoff.md`, API commit `f01a0c1`, focused model suite: 17 passed. | Joint Gate B input. |
| SBE Slice 2 bounded model | `tools/force_fence_completion_hard_stop_v1.als`. | Gate B approved; direct one-fence-per-invocation refinement added before runtime work. |
| API Gate B re-review | `API Agent Gate B Re-review.md`, API commit `a69fb9a`. | Approved; proof-specific runtime/schema design authorized. |
| Slice 2A reconciliation activation | `SLICE 2A - RECONCILIATION ACTIVATION QUALIFICATION.md`; focused native suspension suite: 11 passed on 2026-09-20. | SBE first-cell producer support complete; no source/release change. |
| API Slice 2B handoff | API commit `e2ae114`; SBE review `SBE REVIEW - API SLICE 2B COOPERATIVE RECONCILIATION HANDOFF.md`. | Revision requested: exact argv/parent-exit proof, then installed-wheel joint replay. |

## Design clarification — completion proof classes

| Class | Exact evidence | Capacity consequence |
| --- | --- | --- |
| Cooperative native stop | SBE safe-point result/receipt bound to exact capability, fence, request, invocation, and native run. | API may complete quarantine and release only local SBE capacity. |
| Supervisor-proven hard stop | API worker parent proves the exact supervised child/process group has exited after approved containment escalation. | API may complete quarantine and release only local SBE capacity. |
| Platform-proven worker replacement | API records the exact worker-replacement operation, old boot retirement/no-overlap proof, new boot identity, and old-boot artifact exclusion. | API may complete quarantine and release only local SBE capacity after collateral policy is satisfied. |
| Unresolved escalation | SBE cannot safely stop, or evidence is stale, missing, contradictory, or silent. | Not final; no release. It names the exact next safe-stop or parent-exit proof required. |
