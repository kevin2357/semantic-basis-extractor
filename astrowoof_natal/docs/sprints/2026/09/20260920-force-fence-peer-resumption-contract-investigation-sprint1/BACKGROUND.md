# Background — force-fence peer resumption contract investigation

## Question

Two historical live witnesses show an unfenced SBE peer remaining in
`retry_wait` with retained provider-local dependencies and no later observed
ordinary SBE progress after another run was force-fenced. API owns the likely
scheduling/claim fix surface; this companion begins read-only to determine
whether SBE emitted compatible lifecycle/readiness/resumption information.

No recovery, provider work, workspace mutation, R2 access, or runtime code is
authorized by this investigation opening.

## Primary witness: Q5-003 Baskerville / Bodoni

Baskerville was force-fenced on an unsupported reconciliation route. Its peer
Bodoni remained due in `retry_wait` with four provider-local dependencies and
no later ordinary SBE trace progression.

Evidence is retained in the API repository:

- `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260916-operator-quarantiner-live-qualification-sprint107\testcases\Q5-003-reconciliation-peer-isolation-retry\`
- bounded authoritative packet: `POSTGRES-DIAGNOSTICS-20260920.md`
- bounded SBE/operator log export:
  `betterstack-render-logs-20260920T194700Z-202000Z-pages\`
- external local checkpoint archives:
  `C:\tmp\quarantiner_failed_test_workspaces\Q5-003-reconciliation-peer-isolation-retry\`

## Comparison witness: Q3A-001 Jenson / Mergenthaler

Mergenthaler was an untouched peer that likewise remained in `retry_wait`
after released capacity, with provider-local dependencies and no later
observed SBE progress. It is comparison evidence only; no shared cause is
assumed.

- `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260916-operator-quarantiner-live-qualification-sprint107\testcases\Q3A-001-jenson-jammie\`
- local archives:
  `C:\tmp\quarantiner_failed_test_workspaces\Q3A-001-jenson-jammie\`

## Explicit exclusion

Q3A-003 Plantin / Granjon is not a lost-resumption witness. Plantin's force
fence deliberately retained the sole active SBE allocation under the Q3
contract, so Granjon's inability to claim it is explained by policy.

## API companion

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260920-force-fence-peer-resumption-investigation-sprint109\`

The API sprint maps authoritative claim/availability/capacity state. Neither
side may propose implementation until the paired classification gate.
