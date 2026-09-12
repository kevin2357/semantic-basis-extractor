# Background

## Trigger

API Sprint 90 selected the paused Bodoni Biscuit QA run for an owner-authorized
read-only relocated operator-disposition exercise. Bodoni reached genuine SBE
`provider_pending_known_identity` before the SBE worker was suspended. No
provider call, reconciliation, resume, operator request, quarantine mutation,
or other retained-run mutation has occurred.

## Exact target and immutable coordinate packet

- API run: `e6c9c80f-c163-4c23-8264-a14ce613e0bc` (Bodoni Biscuit)
- native run: `a5ff3cdee621688b79c88c51ea5aef7c54a3edb6db14cb6d80a94a92f22f930f`
- SBE job: `665a5dd5-6c04-417e-9729-46129b32dadb`
- active checkpoint: `61488dc8-87c9-45ab-833d-6fb3fc1bc1f5`, generation `3`
- R2 key: `v1/checkpoint/0042ab9920a647ad909bcd4d31f41b22`
- ETag: `584405fb6d9d46d42ce2637ae909518d`
- archive SHA-256: `d5d94241314e084e0c8375b0de31f432a934689929ad90bc4891abdcd4d882cc`
- inventory SHA-256: `14f28678b45b8f95c114b65c7d01c0c622bcf37d02c8392ead3377a541a7fafc`
- archive byte size: `1795164`
- logical root: `/work/runs/workspace-1abc761d-6c02-4dc3-9dab-434b388caed2/sbe`
- checkpoint contract: `astrowoof.sbe-workspace-checkpoint.v1`
- compatibility identity: `sbe@qa-hokusai-native-root-rollout.v1`

The owner already authorized the exact conditional HEAD/GET. API saved the
verified private archive and local restore:

- `C:\tmp\astrowoof-sprint90-bodoni-sbe-checkpoint-gen3.zip`
- `C:\tmp\astrowoof-sprint90-bodoni-sbe-checkpoint-gen3-workspace`

No additional R2 read or mutation is required for the native reproduction.

## Observed native seam

API invoked the public relocated reader from the exact released SBE 0.4.60
wheel against the isolated local copy. It refused before disposition with:

```text
Relocated workspace snapshot is incomplete or changed
```

This is ordering-only, not byte drift. `workspace-snapshot.json` and a fresh
`snapshot_inventory(..., use_process_cache=False)` both contain 375 entries;
their path sets, sizes, and SHA-256 values are identical. Their lists first
differ at index 16 because the implementation sorts host `Path` objects.
Linux authoring and Windows restore therefore produce a different ordering for
the same relative paths. The checkpoint archive itself uses stable relative
POSIX ordering and restored successfully (387 members, 8,490,671 bytes).

Independent SBE-side inspection reproduced all of those facts and verified the
archive SHA-256. It also found an important compatibility detail: sorting by a
plain relative POSIX string does not reproduce the retained Linux manifest.
The first such divergence is a directory subtree beside a same-prefix `.zip`.
Sorting by `PurePosixPath(relative).parts` exactly reproduces all 375 retained
members while remaining independent of Windows host-path comparison.

## Scope

Sort native snapshot inventories by the case-sensitive component tuple of each
workspace-relative POSIX path and compare in that canonical order. Retain
strict file-identity and duplicate-path checks; do not replace them with an
unordered comparison. Add provider-free cross-platform regression coverage.
When a qualified wheel is available, API can re-run this exact local Bodoni
archive without another R2 call.

## SBE worker logs

Unfiltered Render CLI exports for suspended worker `srv-da12sktbedkc73btpu00`:

- `C:\tmp\sbe-worker-bodoni-snapshot-ordering-01.json` — 1,450,745 bytes,
  active-work window `17:37:23Z`–`17:52:23Z`.
- `C:\tmp\sbe-worker-bodoni-snapshot-ordering-02.json` — 0 bytes.
- `C:\tmp\sbe-worker-bodoni-snapshot-ordering-03.json` — 0 bytes.
- `C:\tmp\sbe-worker-bodoni-snapshot-ordering-04.json` — 0 bytes.

The three empty 15-minute segments are expected after deliberate suspension.
