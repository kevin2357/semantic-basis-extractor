# AstroWoof Natal Authoring 0.4.50

SBE 0.4.50 adds bounded, non-authoritative decision-evidence trace summaries
at durable optional-stage classification, validation/lint consumption, and
native result publication boundaries.

## What changed

- New `native_stage_evidence_summary` traces expose stage/attempt/action/provider
  correlation, accepted/improved state, bounded counts, report presence, and
  typed error class/fingerprint without prompt or edit material.
- New `native_validation_evidence_summary` traces expose report identities,
  status/counts, and capped closed warning/acceptance/rejection code
  distributions without finding prose.
- New `native_publication_evidence_summary` traces join explicit result
  outcome/cause to result, receipt, invocation, checkpoint, snapshot, and
  bounded native evidence totals. Publication is not treated as terminality.
- The run reporter recognizes and places the new events and preserves their
  bounded code distributions.
- New provider-free installed command:
  `astrowoof-decision-evidence-observability-qa`.

## Compatibility

- Lifecycle, authority, custody, provider, editorial, and API disposition
  contracts are unchanged.
- Existing operational trace and run-report schemas remain readable.
- `semantic-projection-core==0.11.1` remains the supported dependency.
- The events are diagnostic only and never grant transition authority.

## Qualification

- Full repository suite: 1,061 passed, 3 expected skips.
- Two artifact-source builds were byte-identical.
- Installed generic release smoke, historical trace observability, run reporter,
  and decision-evidence observability qualifications passed.
- Provider creates/retrievals, external network calls, R2 access, and retained-QA
  mutation: zero.
