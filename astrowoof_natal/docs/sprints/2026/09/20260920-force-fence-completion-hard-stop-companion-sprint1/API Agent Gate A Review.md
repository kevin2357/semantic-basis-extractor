# API Agent Gate A Review

## Reviewed material

- `SLICE 0-1 ROUTE INVENTORY AND CONTRACT PROPOSAL.md`
- `PLAN.md`
- API control-plane discovery in the companion API sprint

## Gate A decision

**Technically aligned.** The proposal correctly refuses the unsafe shortcut:
an absent, malformed, unsupported, or timed-out SBE observation is not proof
that a child exited and provides no capacity-release authority.

The first active-route completion cell should be interactive
`provider_reconciliation`, reusing the existing native-suspension v1 result,
receipt, and command-result family. Do not create an SBE
“unsupported-but-releasable” result.

The two stated safe boundaries are appropriately route-sensitive:

- `reconciliation_before_provider_get` is valid before retrieval starts;
- `reconciliation_after_response_checkpoint` is the required boundary for a
  fence received during GETs, since it binds persisted response state before
  cooperative exit.

Neither asserts provider cancellation/settlement, terminalization, workspace
deletion, or capacity release. Those remain API-owned.

## Required joint integration constraint

API's current reconciliation subprocess route does not yet prepare a
supervision invocation, pass the supervision envelope/control root, or install
the exact force-fence callback used by ordinary v2 dispatch. Therefore an SBE
handoff cannot itself finalize the target.

Before runtime work, Joint Slice 2/Gate B must model the corresponding API
extension and bind it to the exact run/job/attempt/lease/token, native run,
API worker boot, launch generation, command/workspace/control digests,
checkpoint basis, capability, fence, result/receipt, and durable API-parent
exit observation.

## Accepted route treatment

| Route | Gate A classification | Release rule |
| --- | --- | --- |
| `external_authority_v2_dispatch` | Existing cooperative foundation. | API releases only after exact handoff plus durable parent-exit proof. |
| Interactive `provider_reconciliation` | First required cooperative extension. | Same API finalization condition. |
| Batch reconciliation | Unresolved until separately modeled safe proof or API parent/platform proof. | Never release from silence. |
| Missing/stale/contradictory/late evidence | Unresolved escalation. | Never release from SBE evidence alone. |

## Gate B requirements

The joint model/fixtures must cover child liveness separately from allocation,
leases, provider custody, and global budget; ordinary-result precedence;
stale/cross-run/replay substitutions; parent loss; both reconciliation
boundaries; platform-replacement inventory/collateral/retired-boot behavior;
and named-peer admission after every final outcome only.

## Conclusion

Gate A technical review is affirmative. No runtime, schema, reader, or
resource-release implementation is approved until the joint formal model and
adversarial fixture gate is accepted.
