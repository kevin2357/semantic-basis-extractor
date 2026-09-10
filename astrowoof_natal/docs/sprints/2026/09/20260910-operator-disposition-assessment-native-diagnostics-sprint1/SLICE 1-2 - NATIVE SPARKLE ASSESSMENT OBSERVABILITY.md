# Slice 1–2 — Native sparkle assessment observability

## Result

SBE's existing structured application logger now observes the in-process operator-disposition assessment without adding a callback, changing the assessment schema, or changing native behavior.

## Added closed events

- `operator_disposition_assessment_started`
  - records the bounded entry phase before workspace state is loaded;
- `operator_disposition_assessment_completed`
  - records custody class, quarantine posture, reason code, state revision, lifecycle schema, and assessment digest; and
- `operator_disposition_assessment_failed`
  - records bounded phase, reason code, error class, and a stable diagnostic fingerprint without raw exception prose.

All records use `astrowoof.sbe_worker_log.v1` and the existing closed event catalog.

## Workspace fingerprint use

After `run.json` is loaded but before stable-path validation, the reader emits the existing `workspace_fingerprint` projection with `validation_outcome=assessment_preflight`.

This preserves useful identity on the early failure that likely affected Baskerville:

- native run/state identity when present;
- expected logical-root digest rather than path;
- snapshot digest and member count;
- checkpoint identity/digest when present;
- SBE/SPC release identity; and
- aggregate fingerprint digest.

The relocated-workspace regression proves neither the original nor restored absolute path appears in the fingerprint or failure record.

A second failure regression injects a lifecycle-inspection `OSError` containing
private prose and a path. The emitted failure remains bounded to phase
`lifecycle_inspection`, reason `lifecycle_inspection_unavailable`, exception
class, and stable fingerprint; neither exception prose nor path is emitted.

## Failure phases

The reader tracks only a closed set of diagnostic phases:

- `workspace_state_load`;
- `initial_snapshot_validation`;
- `observation_time_normalization`;
- `lifecycle_inspection`;
- `lifecycle_normalization`;
- `terminal_evidence_resolution`;
- `custody_classification`;
- `final_snapshot_validation`; and
- `assessment_construction`.

Exceptions are re-raised unchanged after best-effort logging. Assessment permission, provider behavior, workspace mutation, and public return documents are unchanged.

## Qualification

- assessment reader, assessment contract, and trace observability: 33 tests passed, 1 skipped;
- application logging, structured logging contract, suite manifest, and cross-route assessment: 34 tests passed;
- total focused results: 67 passed, 1 skipped; and
- `git diff --check` passed apart from informational Windows line-ending warnings.

## Remaining consumer seam

The API operator runner must explicitly configure or carry SBE's existing
structured stderr handler in its in-process host. Its installed-wheel gate must
exercise normal `force=False` initialization alongside API stdout events;
SBE's `force=True` test proves formatter correctness but not host coexistence.
That is API-owned integration and does not require another SBE diagnostic
transport.

The separate stable-path restoration mismatch remains a functional issue. These logs diagnose it; they intentionally do not relax or repair the native workspace contract.

