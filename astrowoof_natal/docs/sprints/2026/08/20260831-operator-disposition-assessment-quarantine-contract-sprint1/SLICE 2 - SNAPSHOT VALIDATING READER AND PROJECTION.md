# Slice 2 — snapshot-validating reader and projection

## Status

Complete.

## Public surface

The package root now exports:

- `build_operator_disposition_assessment`
- `logical_workspace_root_id`
- `read_operator_disposition_assessment`
- `read_operator_disposition_assessment_schema`
- `validate_operator_disposition_assessment`

## Read boundary

`read_operator_disposition_assessment`:

1. resolves one explicitly named run root;
2. validates the current workspace snapshot;
3. acquires the existing native spend-consumption lock without creating or
   changing it;
4. constructs the highest supported v0.8 lifecycle evidence where possible;
5. uses a strict v0.5 fallback only for historical evidence that cannot be
   losslessly widened;
6. reads terminal evidence only by exact result ID or the explicitly enabled
   bounded availability-recovery reader;
7. revalidates the snapshot while the read fence remains held; and
8. returns the closed assessment without writing any workspace member.

If the existing writer lock is absent, empty, or held, the reader does not
create/repair it. It returns `unsupported_or_inconsistent` / `prohibited` with
`writer_exclusivity_unestablished`.

## Terminal join

Terminal classification binds two different, intentionally non-interchangeable
checkpoint identities:

- the lifecycle temporal checkpoint basis for the current assessment; and
- the native result/receipt retained checkpoint basis and snapshot digest.

The exact reader validates result, receipt, journal, retained snapshot, and
retained basis. The assessment additionally requires the result's post-state
revision and receipt snapshot digest to equal the exact current workspace.
A valid historical or nonterminal result is not projected as the current
`sealed_terminal` disposition.

Availability recovery remains discovery only. The discovered ID is passed to
the exact result reader before it can contribute evidence.

## Historical v0.5 fallback

Some valid historical terminal states (notably operator retirement) are valid
under v0.5 but cannot be widened through every later local-work/lineage
validator. The reader may use their validated v0.5 evidence for exact terminal
and custody facts. It may not claim positive local-work absence from v0.5:
without an exact terminal join, a would-be quiescent fallback becomes
`unsupported_or_inconsistent` with `local_work_inventory_unavailable`.

## Focused proof

- exact six-member provider-pending assessment;
- byte-identical replay;
- no workspace-byte mutation;
- missing-lock fail-closed behavior without lock creation;
- provider-free quiescent assessment under an existing read fence;
- exact operator-retirement result/receipt/current-checkpoint join; and
- root-level import/export smoke.
