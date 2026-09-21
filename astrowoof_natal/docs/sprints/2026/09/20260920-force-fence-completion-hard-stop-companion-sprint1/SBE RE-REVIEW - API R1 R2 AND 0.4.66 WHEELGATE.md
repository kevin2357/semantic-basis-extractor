# SBE Re-review — API R1/R2 and 0.4.66 wheelgate

## Decision

**R1 is approved. R2 needs one narrow API-only correction before Joint Slice
3.** The correction does not change SBE's public suspension contract, schema,
runtime, package contents, or release identity. The immutable `0.4.66` wheel
remains the required joined-replay target once R2 is corrected.

## Evidence reviewed

- API response to the earlier SBE review.
- API implementation commit `29ce05f59534914b4c31cd291c6501895438ddd4`.
- API plan/status update `114808d`.
- SBE `0.4.66` release record: tag
  `astrowoof-natal-authoring-v0.4.66` at
  `a9cb1745da5604869591efd9120e1bd8de76c2f7`; wheel
  `astrowoof_natal_authoring-0.4.66-py3-none-any.whl`, 1,406,483 bytes,
  SHA-256
  `ec30e79780b7a4ffc47510ec25f5b6cb3b09639a8b6a2ec6b2def0661f871daf`.

No provider, workspace, R2, live-worker, allocation, or deployment action was
performed for this review.

## R1 — actual argv binding

Approved. The new provider-free regression intercepts the exact argv supplied
to `Popen`, canonically hashes `{"argv": [...]}`, and compares it to the
persisted prelaunch digest. It includes the time-bound and control-path
arguments that make the reconciliation invocation distinct. The paired
completion test refuses a mismatching argv digest before allocation release.

This is the correct split of responsibility: API proves what it launched; SBE
continues to validate the closed request/result/receipt/command chain that
agrees with the sealed command digest. No native latest-result discovery is
introduced.

## R2 — direct-child exit receipt

The new `DirectChildExitReceipt` is the right primitive. It is produced only
after the reconciliation child has returned a native-suspension command result
and carries a PID, permitted return code, UTC observation time, argv digest,
and explicit `direct_child_exit` scope. The completion adapter also correctly
keeps the API database invocation record ID separate from SBE's sealed
`supervision_invocation_id`.

One contradiction remains. The cooperative completion evidence still writes
`child_process_group_alive: false`, and the generic finalizer still requires
that field for finalization. API explicitly does **not** create or manage a
reconciliation process group, so that field is neither direct-child evidence
nor a fact this route can establish. Leaving it in the successful path turns a
direct-child proof into a silent process-group assertion.

### Required correction before the joined replay

For the `provider_reconciliation` cooperative route:

1. Remove the process-group field from the persisted direct-child evidence and
   do not make its value a finalization prerequisite for that proof scope.
2. Have the finalizer select and validate the direct-child proof shape
   explicitly: exact `proof_scope`, direct-child exit receipt, persisted
   invocation and envelope identities, and exact named SBE handoff. Do not
   accept a legacy process-group boolean as a substitute.
3. Add provider-free coverage that the direct-child route succeeds without a
   process-group claim, while missing, malformed, or substituted direct
   receipts and an attempted legacy-only proof fail closed without releasing
   the target allocation.

`parent_exit_observed` may remain as a concise statement of the parent fact;
it must be backed by the direct-child receipt rather than broadened into a
process-group claim.

## Wheel conclusion

No new SBE candidate wheel is warranted. The remaining defect is confined to
API completion-proof interpretation and persistence; SBE `0.4.66` remains the
already-published, SHA-pinned public producer to install for Joint Slice 3.
After the narrow API correction, install only the exact wheel above and run the
provider-free joined replay plus its negative cases. A local rebuild, a newer
wheel, or a latest-result substitute would invalidate that gate.
