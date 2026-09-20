# Evidence register — force-fence peer resumption contract investigation

| Witness | Role | Evidence location |
| --- | --- | --- |
| Q5-003 Baskerville / Bodoni | Primary | API Sprint 107 testcase and local verified archives named in `BACKGROUND.md`. |
| Q3A-001 Jenson / Mergenthaler | Comparison | API Sprint 107 testcase and local verified archives named in `BACKGROUND.md`. |
| Q3A-003 Plantin / Granjon | Single-slot positive control | Policy-explained retained-allocation block; not a lost-resumption witness. |

## Slice 0 — exact SBE chronology

### Q5-003: Baskerville / Bodoni

- QA's recorded rollout profile sets `ASTROWOOF_SBE_ACTIVE_SLOT_LIMIT=1`.
- Baskerville's force-fence record retains active allocation
  `dca7e8f2-4ebb-49cc-828d-efff59585c97` in slot 1.
- Bodoni's prior allocation is **released**, also recorded against slot 1; it
  is historical state, not a competing active holder.
- Bodoni's last ordinary SBE cycle selected provider reconciliation, advanced
  its checkpoint from four pending dependencies to two completed/two pending,
  published exact native result
  `nres_3aa16...`, and declared `local_continuation_required=true` with
  `capacity_disposition=continue_local_cycle`.
- API then correctly held Bodoni in due `retry_wait`. It was queue due but not
  capacity admissible: the retained target allocation occupied the sole slot.
  The admission path intentionally leaves an unadmittable head unclaimed;
  therefore no later ordinary Bodoni SBE event is expected.

### Q3A-001: Jenson / Mergenthaler

- Jenson's force-fence record likewise retains its active slot-1 allocation.
- Mergenthaler's retry-wait allocation was released, and it remained due with
  five provider-local dependencies but no remaining slot admission.
- This is the same queue-due / capacity-inadmissible shape as Q5-003, not
  evidence of a missing native readiness or continuation signal.

### Source boundaries

All findings above derive from retained API PostgreSQL diagnostics, bounded
worker-log exports, the documented rollout manifest, and read-only source
inspection. No R2 read, provider request, workspace execution, or runtime
mutation occurred.
