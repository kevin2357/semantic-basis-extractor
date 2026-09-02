# Crumpet / Baguette post-retry terminal review investigation

## Purpose

Read-only investigation of two fresh QA runs that independently followed the
same path: six initial authoring results and two creative-retry results were
reported, no provider custody remained, and final local work nevertheless
concluded with `FAILED_REQUIRES_REVIEW` / `review_required` because authoring
passes were deemed incomplete. Determine the exact native semantic reason.

No provider activity, workspace mutation, recovery, deployment, release, or
retained-run action is authorized.

## Runs and final evidence

| Pup | API run | Native run | Job | Terminal checkpoint |
| --- | --- | --- | --- | --- |
| Crumpet Comet | `31714355-c528-4494-a49a-ecbb1d4afa17` | `dc647649b110f751e3ad3a5582e51a10d9ec920b3b095e246a90c5266397104f` | `298ca7a5-2989-4547-b991-e33221b1d8d4` | `e8c1a9f6-dc9d-47ce-a998-5ff2a84894d1` |
| Baguette Boolean | `151213e4-c077-419b-94d8-cf876f8c5530` | `68459ce571ae96eafe78c9df20ccf1b89d1170a0ddf1556c5ebb7dc553bd72ed` | `a712321c-dc2d-4818-bb33-a5ec84d135ac` | `c0b2f659-75fd-4976-87d9-a367fd97e5bb` |

Both API jobs are terminal, non-retryable `native.terminal.review_required`;
all capacity is released. Both action inventories are exactly six
`initial:reported` and two `creative_retry:reported`.

### Crumpet checkpoint

- attempt/generation/state: `c46b1041-f855-411b-8be0-b820ad5bf47f` / `17` / `active`
- object/bytes/SHA-256: `154c2e17-4163-489a-ba89-477b9050a52b` / `4459592` / `7945b399917f0b4905f6c2130fa3cc2539be472f36c4d9eb58b4d852f2d7f20b`
- inventory: `16de3b09acfea2bcf8c98e3e2c05ee5d3568d42945d7c3bf7ceff068778082ad`
- contract/compatibility: `astrowoof.sbe-workspace-checkpoint.v1` / `astrowoof.qa.sbe0438-native-review-retained-custody.v2`
- storage/restore: `qa` / `checkpoint` / `protected-operator`; `/work/runs/31714355-c528-4494-a49a-ecbb1d4afa17/sbe`
- native status/provider version: `FAILED_REQUIRES_REVIEW` / `c872b7a29334ac1fb0990dc4bfd32fbc`

### Baguette checkpoint

- attempt/generation/state: `707a9739-7e43-476a-a011-e8eff6da207b` / `17` / `active`
- object/bytes/SHA-256: `060745d1-22d7-4a0a-afaa-8493c0b6332f` / `4501319` / `012aa842c820fb5c10f8e445b2b5e8b6f5685ce46aee47b682637afc5584d822`
- inventory: `c6dabb6505e1710de56a5320f38436125dc085892cf3ec67410a2bd4ef9d42be`
- contract/compatibility: `astrowoof.sbe-workspace-checkpoint.v1` / `astrowoof.qa.sbe0438-native-review-retained-custody.v2`
- storage/restore: `qa` / `checkpoint` / `protected-operator`; `/work/runs/151213e4-c077-419b-94d8-cf876f8c5530/sbe`
- native status/provider version: `FAILED_REQUIRES_REVIEW` / `a304d0f0021f03031489df5daa517386`

## Trace cues

Render SBE worker: `srv-da12sktbedkc73btpu00`. Search native run IDs above.

- Crumpet: 2026-09-02T12:51:00Z–12:52:30Z.
- Baguette: 2026-09-02T13:00:00Z–13:01:30Z.

The observed common sequence is: `authoring_passes_incomplete` finalization
deferral, terminal `FAILED_REQUIRES_REVIEW`, and publication of a
`terminal_review_command_result.v0.1` receipt. Trace logs are diagnostic-only;
protected checkpoints and receipts remain authoritative.

The owner supplied a combined Render export at
`C:\tmp\sbe-worker-render-last-2h-20260902.log` for diagnostic preflight. Its
SHA-256 is `a656b484c0abaab6450ac447546023e028b4fc8e832f043676a81b640f6ab627`
over `2,115,667` bytes. Derived findings are recorded in
[results/SLICE 0 - TRACE PREFLIGHT.md](results/SLICE%200%20-%20TRACE%20PREFLIGHT.md).
