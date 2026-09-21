# Slice 2 — Joint completion model and fixture proposal

## Result

The bounded model is inhabited for all four intended scheduling outcomes and
has no counterexample in scope for the five release-safety rules.  It also
produces four deliberately bad worlds when those rules are not applied.  This
is a design artifact only: it does not add a wire schema, SBE runtime action,
API capacity release, deployment, provider operation, or workspace access.

The model incorporates API's provider-free handoff (`f01a0c1`) and its crucial
refinement: the existing SBE v1 cooperative result/receipt/command binding is
evidence that SBE reached its exact safe stop, but it is **not** enough to
release API capacity.  Cooperative finality additionally requires API-parent
proof that the exact supervised child/process group exited.

## Model boundary

[`tools/force_fence_completion_hard_stop_v1.als`](tools/force_fence_completion_hard_stop_v1.als)
is a compact, content-free Alloy model.  It represents:

- target invocation, force fence, worker boot, and child liveness separately;
- existing same-invocation SBE cooperative result/receipt/command identity;
- API-parent exact exit and platform replacement as distinct proof classes;
- target scheduling allocation separately from retained provider, spend,
  workspace, and native custody;
- no-new-child admission fencing, old-boot active-child inventory, collateral
  recovery records, old-boot retirement/new-boot readback, and late artifacts;
- an independent global-budget block, so peer admission never asserts that
  unrelated capacity is free; and
- ordinary-result precedence as a normal-lifecycle outcome that precludes
  recharacterizing the same invocation as cooperative quarantine completion.

It does not claim byte equivalence, process-tree enumeration, API transaction
atomicity, Render behavior, SBE provider cancellation, or provider-side
terminalization.  Those remain implementation and integration obligations.

## Completion rule

| Outcome | Required exact evidence | Target allocation | Peer admission |
| --- | --- | --- | --- |
| Cooperative final | Existing v1 result/receipt/command for the exact invocation **and** API-parent exact child/process-group exit. | Release only this API/SBE scheduling allocation. | Eligible, subject to the peer's own allocation and no global block. |
| Parent final | API-parent exact child/process-group exit after the exact fence. | Release only this allocation. | Same condition. |
| Replacement final | Target/old boot join; no-new-child fence before inventory; collateral-safe inventory/recovery; old boot retired/no overlap; new boot readback. | Release only this allocation. | Same condition. |
| Ordinary precedence | Ordinary result wins before the native safe-stop observation. | Normal lifecycle, not a quarantine completion. | Outside this completion transition. |
| Escalating | Missing, stale, contradictory, unsupported, blocked, or silent proof. | Held. | No admission caused by this completion. |

No completion proof releases provider, spend, workspace, or native custody.

## Bounded campaign

- Analyzer: Alloy Analyzer CLI `6.2.0`, solver `sat4j`.
- Model SHA-256:
  `29ba974351d198d3724174527a5f61cd7a1db015483b23ccf6bc0483072cf07b`.
- Scope: up to eight atoms, with exactly eight ordered moments in every
  explicit run.
- Private machine-local output: `tools/.tmp-alloy-output/receipt.json`.

The four required worlds are satisfiable:

1. cooperative result/receipt/command plus parent exit, then peer admission;
2. parent-only exact exit, then peer admission;
3. collateral-safe worker replacement, then peer admission; and
4. unresolved escalation retaining the target allocation with no peer
   admission induced by it.

The following checks returned `UNSAT` (no counterexample at the stated bounded
scope):

- unresolved escalation cannot release the target allocation;
- final completion needs an exact stopped-child observation;
- replacement fences admission before retirement and records every live
  collateral child;
- a late old-boot artifact cannot establish a replacement completion; and
- peer admission requires final target completion and no independent global
  block.

The intentionally weakened model admits `SAT` witnesses for premature
silence-release, un-inventoried collateral replacement, an old-boot late
artifact treated as cooperative finality, and peer admission despite a global
block.  Those witnesses are a guard against accidentally dropping a rule in a
future implementation.

## Deterministic fixture matrix for Gate B

The runtime/API integration must materialize these without provider calls:

| Fixture | Expected completion | Required negative assertion |
| --- | --- | --- |
| Cooperative reconciliation before external GET | Cooperative final only after exact v1 handoff plus parent exit. | Handoff alone leaves allocation held. |
| Cooperative reconciliation after response checkpoint | Same as above with the later permitted safe point. | No provider cancellation or synthetic terminalization. |
| Parent exit after blocked external call | Parent final. | No SBE result invented. |
| Parent loss / missing exact process group | Escalating. | Allocation held. |
| Unsupported or stale/replayed capability | Escalating. | No child launch or release. |
| Ordinary result before SBE observation | Ordinary lifecycle wins. | No quarantine completion from the later request. |
| Replacement with target only | Replacement final after all platform evidence. | Late old-boot events non-authoritative. |
| Replacement with live collateral | Refuse or require exact recovery record. | No release while any collateral is unclassified. |
| Global budget block on peer | Target may finish. | No peer admission claim. |

Each fixture must bind run, job, attempt, lease, force-fence token, native run,
worker boot, launch generation, command/workspace/control digests, checkpoint
basis, SBE result/receipt/command identities where applicable, and API-parent
exit or platform-replacement record where applicable.  A different run, old
boot, stale token, or alternate checkpoint is a fail-closed mismatch.

## Gate B request

Approve or correct the model and matrix before any runtime/schema work.  In
particular, Gate B needs joint confirmation that API's concrete process-group
exit evidence can be bound to the same invocation identities that SBE v1
already binds, and that the platform replacement receipt can satisfy every
listed control-plane proof without treating old-boot artifacts as authority.
