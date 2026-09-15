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

## Slice 0 reproduction evidence

Official container identities used:

- `python:3.11.15-slim`, image digest
  `sha256:90744cff8f32887f075c47d747a173ff333e9e98801667af93c357fa9f5e28ff`;
- `python:3.12.14-slim`, image digest
  `sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea`.

The read-only probe confirmed:

- Python 3.11 `joinpath` signature: `(self, child)`;
- Python 3.12 `joinpath` signature: `(self, *descendants)`;
- current two-descendant helper: `TypeError` on 3.11, success on 3.12;
- chained traversal on both: 11,604 bytes, SHA-256
  `306fcf0e55c56f5fe48b18eaced64dbb3338ab783a5722a801f7759af96e52e5`;
- direct, chained, and successful current-helper bytes are identical;
- missing resource: `FileNotFoundError` on both; and
- malformed JSON: `ValueError` on both.

An AST inventory found ten explicit multi-argument calls and one additional
starred-component call across seven source modules. See the Slice 0 report for
classification.

## Evidence limits

The live diagnostics intentionally omit exception prose and unsafe path/content
material. Provider-free reproduction now confirms the exception class and
runtime boundary without needing that prose. No live workspace was read.
