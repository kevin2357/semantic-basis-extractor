# Slice 0 — In-process logging and restore-path reproduction

## Result

Slice 0 found a provider-free reproduction that closely matches the live assessment refusal and confirmed that normal SBE sparkle logging works in-process once its existing handler is explicitly configured.

No live workspace, provider, database, or object-storage access was used.

## Leading assessment-failure candidate

The API operator runner restores a checkpoint beneath its request-specific workspace:

```text
<operator-runner-root>/<operator-request-id>/sbe
```

SBE's public assessment reader resolves that directory and immediately calls `validate_workspace_snapshot(root, state)`. The native workspace contract requires `root` to equal the original `workspace_contract.logical_root` exactly.

A provider-free experiment materialized a valid provider-pending workspace, wrote its snapshot at its original path, copied the exact files to a request-specific `.../request-id/sbe` path, and invoked the public reader there. It failed with:

```text
ValueError: Run workspace must be restored at its original logical absolute path:
expected '<temporary>/original', got '<temporary>/request-id/sbe'
```

The same reader against the original path returned a valid `permitted` assessment.

This is the strongest current explanation for Baskerville's `disposition_assessment_unavailable`: restoration can be byte-exact while still violating SBE's stable logical absolute-path contract. The exact persisted live exception detail has not been read, so the live cause remains a high-confidence candidate rather than a completed identity proof.

## Why existing tests missed it

The API operator-runner tests inject both:

- a fake restore callback; and
- a fake permitted/prohibited assessment reader.

They prove request fencing and disposition semantics but never join API's real request-specific restore path to SBE's real public reader. SBE reader tests invoke the reader at the original materialization path. Each side passes independently while the cross-package path contract fails.

## Existing logging experiment

SBE's normal `configure_logging()` was installed into an in-memory stderr-equivalent stream before an in-process reader call.

Observed on a successful assessment:

- 7 structured records;
- every record validated/rendered as `astrowoof.sbe_worker_log.v1`;
- existing `workspace_fingerprint`, `native_state_summary`, and lifecycle `application_message` events were captured; and
- records came from the normal closure and lifecycle loggers.

Observed on the relocated-path failure:

- 0 records;
- failure occurs before an existing log statement; and
- the raw `ValueError` contains absolute paths and therefore should not simply be logged verbatim.

This establishes that no callback is presently justified. The existing formatter works for in-process SBE calls. The remaining requirements are:

1. deliberately configure/carry the existing SBE handler in the operator-runner host;
2. add bounded assessment entry/failure/completion events before the current early failure boundaries; and
3. sanitize the failure into closed phase/reason fields rather than exposing paths.

## Assessment phase/failure inventory

| Phase | Representative failure | Existing useful log before failure? | Candidate bounded reason |
| --- | --- | --- | --- |
| resolve/load | missing or invalid `run.json` | no | `native_state_unavailable` |
| initial snapshot validation | stable root mismatch, missing manifest, changed inventory | no for root/manifest; one error for changed inventory | `workspace_path_mismatch`, `snapshot_unavailable`, `snapshot_changed` |
| timestamp normalization | missing or timezone-naive `updated_at` | some earlier lifecycle-independent records may exist only after validation | `observation_time_invalid` |
| read-only fence | lock absent or unavailable | lifecycle can describe unestablished access | normally classification evidence, not an exception |
| retry-lineage inspection | later contract cannot represent historical evidence | existing lifecycle logs may exist | `legacy_lifecycle_fallback` when fallback succeeds |
| v0.5 fallback | both current and fallback inspection fail | inconsistent | `lifecycle_inspection_unavailable` |
| lifecycle normalization | unsupported lifecycle schema/evidence | preceding inspection-dependent | `lifecycle_evidence_unsupported` |
| terminal evidence | malformed or contradictory exact terminal evidence | inconsistent | `terminal_evidence_invalid` |
| custody classification | unsupported/contradictory facts | some lifecycle summaries exist | `custody_classification_unavailable` |
| final snapshot validation | workspace changed while assessed | yes | `snapshot_changed_during_assessment` |
| assessment construction | output violates closed assessment schema | preceding native facts exist | `assessment_contract_invalid` |

The matrix is diagnostic only. It must not convert unsupported or contradictory native states into quarantine permission.

## Contract ruling

- Continue with existing SBE sparkle logging.
- Do not add an observation callback in this sprint unless a later concrete host limitation invalidates this experiment.
- Keep API request/job/lease correlation in API-owned events; SBE logs native run/state/digest evidence it can prove.
- Treat stable-path restoration as a functional cross-package issue adjacent to observability. Logging alone would reveal it but would not make assessed quarantine work.

## Next review questions

1. Should API restore the checkpoint at its recorded logical restore path, or should SBE gain a separately designed read-only relocation contract?
2. Can the operator runner safely configure SBE's existing stderr handler once at process startup without disturbing API JSONL stdout?
3. Which bounded assessment events and reason codes belong in the existing closed worker-log catalog?
4. Should the cross-package real-restore/real-reader regression live in API, SBE qualification, or both?

