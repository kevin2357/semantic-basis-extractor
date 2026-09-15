# Evidence — Python 3.11 editorial contract-resource compatibility

## Evidence boundary

This initial classification uses only the local Render exports supplied by the
owner. Better Stack exports were deliberately left untouched. No provider,
network, R2, API, workspace, or runtime mutation occurred.

## External Render exports

The source files remain outside Git in `C:\tmp`:

| File | Bytes |
| --- | ---: |
| `sbe-worker-render-logs-20260915-mdt-0635-0640.txt` | 365,918 |
| `sbe-worker-render-logs-20260915-mdt-0640-0645.txt` | 1,083,007 |
| `sbe-worker-render-logs-20260915-mdt-0645-0650.txt` | 876,156 |
| `sbe-worker-render-logs-20260915-mdt-0650-0655.txt` | 553,920 |
| `sbe-worker-render-logs-20260915-mdt-0655-0700.txt` | 0 |

The nonempty files cover the cohort's relevant UTC interval. The final export
is empty and supplies no evidence.

## Witness matrix

| Field | Witness 1 | Witness 2 |
| --- | --- | --- |
| Native run ID | `08ecc2f5b68600101494c40c9404d8a31b5b9ea1cd98e3b89b5b259e5fb635a0` | `68e05b7d64a906d3862184a7079d52f7c791869e3a584cc501fe68c82e6d3c49` |
| API run ID | `4a7d55c4-82c2-4f80-8df4-9af01d9f22fb` | `2cc7f2f0-63ae-4224-b3f7-118a0cc08d59` |
| Exact result ID | `nres_c164c39bf9b4c94429a3a9d5` | `nres_771b6685241930a90a9bfa18` |
| Route | `delivery` | `delivery` |
| Root SHA-256 | `2ac8d6bcb31d83d110e8366216e48ba14a05c9b44203bc20d62566662aa5f7d6` | `76bfc9f82e7c5409bb6ed4356fb7da0f56d55580982faf6830b4ec22d2c7fb16` |
| Failed phase | `typed_status_construction` | `typed_status_construction` |
| Exception class | `TypeError` | `TypeError` |
| Safe frame | `editorial_review_contracts.py::_resource_bytes:221` | `editorial_review_contracts.py::_resource_bytes:221` |
| Fingerprint | `667a621a320f2cc5` | `667a621a320f2cc5` |

## Proven successful phases

For both witnesses, SBE 0.4.62 reported successful completion of:

1. `root_normalization`;
2. `exact_result_reader`;
3. `eligibility_classification` with branch `delivery`;
4. `exact_source_proof`;
5. `pre_assembly_evidence_collection`;
6. `guarded_packet_assembly`; and
7. `packet_validation`.

The next phase, `typed_status_construction`, failed. Therefore these exports do
not support changing roots, readers, source proof, evidence collection, packet
assembly, or packet validation.

## Source and runtime join

- Exact source location:
  `astrowoof_natal/src/astrowoof_natal_authoring/editorial_review_contracts.py:221`.
- Live SBE release: `0.4.62`.
- Live Render Python: `3.11.15`.
- Recent local/API installed-wheel qualification Python: `3.12.14`.
- Declared package floor: Python `>=3.11`.

This join makes Python 3.11 resource traversal the primary reproduction target,
not merely a speculative secondary check.

## Evidence limits

The diagnostics intentionally omit exception prose and unsafe path/content
material. They prove the phase and approved SBE frame, but the exact Python
error text remains unobserved. A provider-free Python 3.11 reproduction is
required before freezing the correction.

