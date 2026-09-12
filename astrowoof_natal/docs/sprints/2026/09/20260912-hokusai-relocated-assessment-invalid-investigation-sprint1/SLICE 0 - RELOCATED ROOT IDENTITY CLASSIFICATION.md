# Slice 0 — Relocated root identity classification

## Result

Provider-free reproduction identifies SBE's original-logical-root binding as
the exact compatible failure phase. The released `0.4.60` reader accepts a
relocated, byte-stable, provider-pending workspace when relocation authority
hashes the logical root preserved by `run.json.workspace_contract`. The same
workspace is refused with `Original logical root does not match relocation
authority` when authority instead hashes `/work/deterministic-domain`.

API's subsequent exact job-bound join closes the historical identity gap. The
operator restored checkpoint `c1726aeb-f091-45d4-956a-4f628bb96439`, generation
`3`, whose checkpoint and authoring-row root was
`/work/runs/00667fb9-c068-415e-a045-8d4059ac549e/sbe`. API used that root in
the authority. It is not equal to the native durable allocation root, so the
live request failed at the reproduced original-root boundary.

## Three observed root identities

| Source | Root represented | Evidentiary meaning |
| --- | --- | --- |
| SBE `0.4.60` worker trace and command result | `/work/runs/workspace-5d5294a3-6d1d-4fe4-9a36-c0e2b067414a/sbe` | Native durable `workspace_contract.logical_root` |
| API authoring-authority source | `/work/runs/{api_run_id}/sbe` | Path currently constructed for `SbeAuthoringRun.logical_workspace_path` |
| original run-wide checkpoint packet | `/work/deterministic-domain` | Deterministic job checkpoint; not used by the operator restore |

These identities are not canonically equivalent. SBE is correct to refuse an
authority generated from either non-native value when reading the copied
workspace. The API must establish which value it actually supplied during the
failed request before assigning the exact live cause.

## Reader boundary map

The public reader executes the relevant boundaries in this order:

1. relocation-authority shape, digest, capabilities, and time window;
2. assessment timestamp inside that window;
3. restored `run.json` native-run identity;
4. durable workspace-contract presence and relocated-root inequality;
5. original logical-root digest binding;
6. restored physical-root digest binding;
7. snapshot schema and preserved manifest logical root;
8. exact snapshot member inventory;
9. inner operator assessment, including exact terminal-result selection;
10. repeated authority, freshness, and snapshot validation after native reads;
11. relocated wrapper construction and API pair validation.

The generic API detail proves only that a `TypeError` or `ValueError` escaped
the reader/pair sequence. The absence of an SBE inner-assessment start event is
compatible with failure at step 5, because relocated snapshot validation runs
before `_read_operator_disposition_assessment()` begins its diagnostic phases.

## Provider-free controls

`test_hokusai_relocated_assessment_investigation_slice0.py` constructs a copied
provider-pending workspace with five known provider-local dependencies, no
provider callback, and no mutation capability.

- Native logical-root authority: returns
  `provider_pending_known_identity` / `permitted`.
- Deterministic-domain authority: refuses at original-root binding.
- Existing relocation suites remain green, including snapshot, terminal-result,
  authority-pair, and capability fences.

## Ownership and next evidence

The exact classification is an API identity-source defect, not an SBE reader
defect. API's job-bound join proves the deployed authority builder used the
API-run root rather than the native durable allocation root. A run-wide
latest-active checkpoint is not a substitute for that join; the earlier query
selected the deterministic job.

No R2 HEAD/GET, provider operation, workspace mutation, retry, or second
operator execution is needed or authorized. SBE implementation remains gated.
