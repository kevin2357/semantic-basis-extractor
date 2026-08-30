# Slice 3 — API consumer handoff

## Status

Implemented and ready for API fixture/contract review. This is additive,
qualification-only package work; no production lifecycle/runtime behavior changed.

## Public surface

- Python:
  - `read_legacy_local_work_upgrade_fixture`
  - `read_legacy_local_work_upgrade_bundle_schema`
  - `read_legacy_local_work_upgrade_qualification_schema`
  - `build_legacy_local_work_upgrade_bundle`
  - `validate_legacy_local_work_upgrade_bundle`
  - `run_legacy_local_work_upgrade_qualification`
  - `validate_legacy_local_work_upgrade_qualification`
- CLI: `astrowoof-legacy-local-work-upgrade-qa`
- CLI modes: default receipt, `--fixture`, `--bundle`, `--bundle-schema`,
  `--schema`.

The CLI accepts no production input or provider/authority/workspace argument.

## Consumer rule

API should use the bundle only as provider-free fixture evidence. It should pass
the contained lifecycle documents to SBE's public validators and compare stable
shared identities. The bundle and qualification receipt are not scheduling,
provider, spend, or mutation authority.

The receipt is intentionally path-free and reproducible. The complete public
document bundle is invocation-specific because lifecycle documents truthfully
bind their temporary logical workspace and snapshot identity.

## Scenario outcomes

| Scenario | Expected outcome |
| --- | --- |
| consistent completed fan-in + unrelated not-due custody | exact `ordinary_resume`; custody retained; zero provider I/O |
| consistent due custody | `provider_reconciliation_cycle`; qualification performs zero GETs |
| lineage conflict with custody | reconciliation permitted, forward dispatch forbidden |
| lineage conflict after custody | typed `retain_for_review` |

## Current evidence

- New focused qualification tests after review hardening: 9 passed, 1 optional
  `jsonschema` check skipped.
- Combined legacy/v0.7/v0.8/qualification matrix: 36 passed, 1 optional
  `jsonschema` check skipped.
- The bundle validator derives the legacy seam from the complete embedded v0.5
  document and rejects recomputed-digest mutations to its local-source,
  custody/due, and conflict projections.
- Two fresh source-tree qualification invocations produced identical receipt
  SHA-256 `aaa8792054996520e9eb8d0f145b693c96b7de3f871b277f9e63d3f31bb790ea`.
- Receipt reports zero create, retrieval, external network, and spend.
- `git diff --check` is clean apart from informational Windows line-ending
  notices.

Installed-wheel qualification and version bump remain deliberately after this
API review gate.
