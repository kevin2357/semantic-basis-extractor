# Slice 0 — Diffie bounded follow-up

## Disposition

Hellman and Diffie are separate causal branches.

- Hellman is closed sufficiently for the API terminal-result-first correction.
- Diffie's exact rejected lifecycle document was not retained in the active
  checkpoint, API sprint evidence, or repository log extracts. Its live failure
  therefore cannot be reconstructed byte-for-byte from current evidence.
- No SBE runtime or schema change is justified solely by Diffie's historical
  error.

## Retained facts

Diffie generation 8 is a complete, snapshot-valid checkpoint sealed before the
later API error. It contains two creative-retry actions with durable provider
identities and pending reconciliation evidence. Its lifecycle evidence selects
provider reconciliation as not due and releases capacity until the native due
time. That document is coherent and is not the document rejected later by API.

The later API error records only the closed exception category and message:

```text
SbeProviderContractError: SBE ordinary resume branch evidence is incomplete
```

It does not retain the lifecycle bytes or the individual failed predicate.

## Render log correlation

The owner-supplied SBE-worker export covers `08:21:06Z` through `09:10:20Z` and
does include Diffie's failing interval. It establishes:

- generation 8 was accepted at `08:55:01.340Z` after a quiescent, not-due
  provider-reconciliation cycle;
- its API projection reported `local_continuation_required=false` and two
  provider-local dependencies;
- API claimed attempt 7 at `08:56:45.629Z` and entered
  `_advance_bounded_reconciliation`;
- validation failed at `08:56:52.347Z` inside
  `SbeBoundedReconciliationService.validate()` while validating the result's
  embedded lifecycle inspection; and
- no new checkpoint was accepted for Diffie after generation 8.

No `✨🐶` lifecycle line or command-result bytes from the reconciliation
subprocess were streamed between claim and failure. The wrapper captured that
document in-process and reduced the failure to the generic strict-consumer
message. Thus the log proves the rejected document was a newly returned
reconciliation inspection, not generation 8, but still cannot expose its exact
failed predicate.

The separately exported HTTP API service log contains deployment and health
traffic only. The relevant validator ran inside the SBE queue-worker service, so
that export adds no invocation evidence.

## Source-compatible strict-consumer seam

The API v0.5 consumer requires every `ordinary_resume` projection to carry a
nonzero `local_dependency_count`. SBE's v0.5 projection can legitimately select
ordinary local fan-in while another provider-bound retry remains pending. In that
mixed state:

- completed provider evidence makes deterministic local fan-in runnable;
- the still-pending provider identity keeps `local_dependencies` empty because
  assembly/retry dependencies remain gated on provider custody;
- v0.5 selects `ordinary_resume / local_work_ready`; and
- v0.7/v0.8 supplies the explicit local-work operation that identifies what may
  be consumed.

`test_completed_retry_beside_pending_retry_has_local_work_but_no_dependency`
freezes this shape provider-free. It explains a concrete way the API's strict
v0.5 ordinary-resume predicate can reject a valid SBE projection. It is a
source-compatible Diffie hypothesis, not a claim that Diffie's missing live
document had identical bytes.

## Consumer implication

The API must not infer local work from v0.5 dependency count once the native run
requires the newer local-work contract. It should consume the newest supported
closed lifecycle projection and its explicit local-work inventory, or fail closed
with retained evidence if only an older/incomplete document is available.

This is compatible with the Hellman correction: a sealed terminal result still
wins before any lifecycle scheduling. Diffie's branch concerns strict lifecycle
version/predicate consumption only when no winning sealed result exists.

## Evidence limit and next request

To classify the historical Diffie invocation conclusively, API would need to
provide one of:

1. the exact rejected lifecycle document and its invocation/result identity; or
2. a sanitized predicate projection containing every field used by the strict
   ordinary-resume validator.

Absent that evidence, the exact historical predicate remains `unavailable`. The
bounded follow-up has exhausted the retained checkpoint, Render worker/API logs,
current API sprint records, public SBE source, and provider-free characterization
without inventing a live fact. The evidence nevertheless narrows the failure to
the embedded post-reconciliation lifecycle document and makes the mixed
completed/pending v0.5 compatibility seam the leading source-consistent cause.

## Safety record

- No additional R2 access occurred.
- No retained workspace was restored or mutated.
- No provider call, retrieval, cancellation, or spend occurred.
- QA SBE remained suspended.
