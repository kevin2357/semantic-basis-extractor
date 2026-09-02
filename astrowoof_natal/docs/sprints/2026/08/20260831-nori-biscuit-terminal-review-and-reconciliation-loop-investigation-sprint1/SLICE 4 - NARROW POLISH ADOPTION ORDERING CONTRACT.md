# Slice 4 — narrow polish-adoption ordering contract

## Decision

Correct only the confirmed Nori ordering defect. No lifecycle, native-result,
authority, or receipt schema changes are required.

Biscuit remains evidence-insufficient and receives no creative-retry runtime
change in this slice.

## Frozen invariants

1. A local-work operation backed entirely by an optional-stage consumer
   (`polish`, `qualitative_critic`, or `qualitative_candidate`) is not tested for
   consumption at the earlier authoring-pass checkpoint.
2. The operation remains durably advertised until the existing finalization
   boundary runs its stage-specific consumer.
3. The normal finalization checkpoint then applies the existing strict
   `commit_local_work_progress()` rule:
   - the operation disappeared because native truth changed; or
   - a custody-preserving `local_work_progress_contradiction` is sealed.
4. Mixed or authoring/creative-retry work is not silently deferred by this
   rule. The narrow deferral applies only when every advertised operation has a
   supported optional-stage consumer.
5. After `commit_local_work_progress()` persists cumulative consumed-operation
   history under its writer, the coordinator reloads that committed state
   before any later checkpoint. Older in-memory bytes may not erase progress.
6. Completed evidence adoption performs no provider create or retrieval. The
   response identity and body come from already-durable reconciliation evidence.
7. A resulting editorial review remains legitimate when custody is final. It
   is distinct from the former contradiction result that retained provider
   reconciliation custody.

## Public compatibility

- Lifecycle v0.5/v0.7/v0.8 shapes are unchanged.
- Native terminal-review result v0.2 is unchanged.
- Local-work inventory/progress v1 is unchanged.
- API routing does not gain a new command or status.
- API must still separately fix its disposition bug: `review_required` alone
  cannot authorize terminal cleanup when the complete result retains custody.

## Required proof

The production-shaped public resume regression must use real
`finalize_subjects()` and `polish_subject()` behavior with:

- one completed reconciled polish response;
- a real persisted response artifact and background identity;
- the real `SpendController` adoption/settlement callbacks;
- provider transport configured to fail if called;
- disappearance of the prior polish operation;
- cumulative consumed-key persistence;
- no `local_work_progress_contradiction`; and
- a truthful successor decision/result.

The not-due custody and creative-retry controls remain unchanged.
