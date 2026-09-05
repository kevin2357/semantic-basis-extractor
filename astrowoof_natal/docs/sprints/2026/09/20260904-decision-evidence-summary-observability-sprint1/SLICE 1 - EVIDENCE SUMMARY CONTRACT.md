# Slice 1 — Evidence-summary contract

## Authority boundary

Every summary is diagnostic-only. It projects native state or a public artifact
only after the underlying value has been validated/classified. A trace cannot
authorize execution, recovery, settlement, delivery, or API resource release.

## Event vocabulary

### `native_stage_evidence_summary`

One classified optional-stage attempt/review:

- safe stage, subject, action, and provider correlation;
- attempt number and exact native attempt state;
- accepted/improved flags where the stage defines them;
- warning/error and edit/omission counts where known;
- report-presence flags;
- sanitized exception class/fingerprint; and
- semantic summary SHA-256.

The event never contains an editable field path, replacement, excerpt, prompt,
provider body, or report path.

### `native_validation_evidence_summary`

One exact validation/lint report pair consumed by finalization:

- explicit report presence;
- validation and lint status;
- error/warning counts;
- closed lint-warning, acceptance-state, and rejection-code distributions;
- semantic report digests; and
- semantic summary digest.

Unknown or absent evidence remains distinct from a present empty report.
Arbitrary messages/details are never projected.

### `native_publication_evidence_summary`

One completely sealed native publication:

- exact result schema, command kind, outcome, and cause;
- run/revision/result/receipt/invocation identities and digests;
- checkpoint-basis and snapshot digests;
- action/provider counts and state distributions;
- subject and optional-stage state distributions; and
- semantic summary digest.

Publication is not synonymous with terminality. Consumers must use the explicit
validated result contract and outcome/cause.

## Canonical semantics

- Scalars that do not match the existing safe-token grammar become `unknown`.
- SHA-256 fields must be lowercase 64-character hexadecimal or `unknown`.
- Code distributions are lexically ordered mappings with count and canonical
  SHA-256.
- Missing reports yield `present=false`, count fields `null`, status `unknown`,
  and digest `unknown`; present empty lists yield count zero.
- Large/native inventories remain counts/distributions or use the existing
  bounded prefix-plus-overflow contract.
- Every helper computes a canonical summary SHA-256 before logging.

## Failure and privacy behavior

Projection/logging exceptions are swallowed at the observability boundary and
cannot alter native state, provider I/O, output bytes, or exit code. Protected
sentinel coverage applies to edit material, report prose/details, workspace
paths, payloads, authorization documents, credentials, and provider bodies.
