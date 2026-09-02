# API review of Slices 1–2

## Decision

Slices 1–2 are approved. Proceed to Slice 3's provider-free,
production-boundary reproductions. The remote read budget was consumed exactly
as authorized; no additional retained-QA access is approved or needed for this
next step.

## Confirmed findings

### Nori: confirmed combined seam

The checkpoint/result/receipt/journal join establishes two distinct facts:

1. SBE's v0.2 `review_required` result explicitly retained one polish action in
   `provider_reconciliation_required` custody and prohibited new provider
   creation. It was not a complete-custody native terminal.
2. API nevertheless mapped that result to the non-retryable terminal job reason
   `native.terminal.review_required` and performed terminal cleanup.

The second is an API result-ingestion/disposition defect. A future API patch
must consume the complete native result disposition—especially custody finality
and reconciliation inventory—not infer terminal resource cleanup from
`review_required` alone.

The SBE ordering candidate is also well-supported: polished work is advertised
before the first authoring-pass progress-seal boundary, while its actual
stage-specific consumer occurs later. Slice 3 should reproduce that exact
ordering with a completed polish response and no provider I/O.

### Biscuit: distinct candidate with an API containment gap

The retained checkpoint establishes completed, joined creative-retry evidence,
one advertised operation key, no consumed-key history, and an ambiguous
matching pass attempt. It does not prove the internal failed predicate, so the
planned production-boundary reproduction is necessary.

The API-side finding is nonetheless actionable as an invariant: it must not
continue to allocate the sole SBE slot indefinitely for a byte-identical basis
and unchanged semantic operation. The eventual API correction should be
generic—no progress is a typed containment/review condition, not a Biscuit
special case. It must preserve provider/spend custody and must not itself adopt,
deny, cancel, or recreate provider work.

## Slice 3 required controls

- Include Nori's completed-polish ordering case and a control in which the
  stage-specific polish consumer runs before progress is sealed.
- Include Biscuit's completed creative-retry evidence plus the exact
  ambiguous-attempt posture, and prove whether the public resume boundary
  publishes a changed successor or an unchanged semantic operation.
- Assert no provider create/retrieve/POST and no external storage mutation.
- Distinguish native result publication from the API's later disposition; do
  not simulate the API interpretation inside an SBE-only fixture.
- Preserve a legitimate provider-not-due control so the correction cannot turn
  genuine provider custody into spurious local work.

No retained-run recovery, runtime change, or release is authorized at this
gate.
