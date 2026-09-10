# API approval — Slice 0 identity source and failure boundary

Status: approved for Slice 1–3 provider-free implementation and qualification.

The completed decision record correctly resolves API Sprint 87's capture-status
finding.

- Preserve capture-status v1 and semantic-contract v5 unchanged.
- Keep the exact `capture_id` domain to native run ID, native result ID,
  reason, and detail code only.
- Require `subject_id` as authenticated native payload content, but do not
  introduce it as a new identity input.
- The caller-selected/result-document/receipt-bound result-ID equality check is
  an appropriately narrow local consumer guard. It must precede every emitted
  status and does not justify changing the general native exact reader.
- The branch matrix correctly fails closed for malformed/unsealed evidence,
  unsupported receipt, state/run mismatch, and zero/multiple subjects. The
  service-level case is correctly split: only an otherwise proven single-subject
  workspace can yield `ineligible_route`.
- A subject-only rehash remains schema-shaped but is illegitimate without the
  exact-source join. The planned runtime join validator is therefore required,
  not redundant.

No API transport, terminal semantics, lifecycle, custody, cleanup, or Better
Stack authority changes are implied. `No Alloy impact` is correct.
