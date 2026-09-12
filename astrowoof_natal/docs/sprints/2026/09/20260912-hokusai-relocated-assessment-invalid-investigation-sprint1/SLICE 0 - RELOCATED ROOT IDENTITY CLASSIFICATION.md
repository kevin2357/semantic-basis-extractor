# Slice 0 — Relocated root identity classification

## Result

Provider-free reproduction identifies SBE's original-logical-root binding as
the exact compatible failure phase. The released `0.4.60` reader accepts a
relocated, byte-stable, provider-pending workspace when relocation authority
hashes the logical root preserved by `run.json.workspace_contract`. The same
workspace is refused with `Original logical root does not match relocation
authority` when authority instead hashes `/work/deterministic-domain`.

This establishes a closed causal class, not the exact live exception. The live
authority document and the exact checkpoint returned to the operator runner
were not persisted in the supplied evidence. No storage read is required to
resolve that remaining API metadata join.

## Three observed root identities

| Source | Root represented | Evidentiary meaning |
| --- | --- | --- |
| SBE `0.4.60` worker trace and command result | `/work/runs/workspace-5d5294a3-6d1d-4fe4-9a36-c0e2b067414a/sbe` | Native durable `workspace_contract.logical_root` |
| API authoring-authority source | `/work/runs/{api_run_id}/sbe` | Path currently constructed for `SbeAuthoringRun.logical_workspace_path` |
| supplied run-wide checkpoint packet | `/work/deterministic-domain` | A catalogued active checkpoint path whose exact SBE-job relationship is not established |

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

The leading classification is an API identity-source/join problem, not an SBE
reader defect. Before any correction design, API should return the exact
checkpoint selected by `restore_latest(job_id=3c1dc0cd-3169-4542-8f9b-40305d8dcf3b)`
and the exact `SbeAuthoringRun.logical_workspace_path` used to construct request
`e80e824c-fe88-4753-9f55-d2ff42aeb1c0`'s authority. A run-wide latest-active
checkpoint is not a substitute for that join.

No R2 HEAD/GET, provider operation, workspace mutation, retry, or second
operator execution is needed or authorized. SBE implementation remains gated.

