# Evidence — editorial-review capture-status native identity correction

Status: Slice 0 contract decision and Slices 1–2 source qualification complete;
installed-wheel and API consumer evidence remain pending.

## Confirmed source facts

- Public runtime entry point:
  `build_editorial_review_runtime_capture(run_dir, result_id)`.
- Runtime refusal construction delegates to
  `build_editorial_review_capture_status(reason)`.
- That helper currently supplies three fixed fixture correlation strings.
- Capture-status v1 requires `native_run_id`, `subject_id`, and
  `native_result_id`.
- Semantic contract v5 declares capture identity inputs as `native_run_id`,
  `native_result_id`, `reason`, and `detail_code`.
- Existing fixture coverage proves closed schema shape and reason vocabulary,
  but does not prove runtime correlation authenticity, cross-input identity
  separation, or agreement with the manifest derivation domain.

## Current disposition

The API finding is substantiated. SBE should provide the narrow public
correction after Review Gate 0. API should remain paused on emitting the
no-packet branch and must not rewrite native content or identity.

## Pending evidence

- installed-wheel consumer evidence; and
- API/Vafflemutt review.

## Slice 0 evidence

- Completed the branch-by-branch identity-source matrix in
  `SLICE 0 - IDENTITY SOURCE AND FAILURE BOUNDARY.md`.
- Confirmed the selected result ID needs an explicit caller/result/receipt
  equality check before status emission.
- Froze subject-unavailable behavior as no status: zero subjects, multiple
  subjects, or a run mismatch cannot populate v1 honestly.
- Confirmed an unsupported service level may emit `ineligible_route` only when
  exactly one subject is otherwise proven.
- Confirmed subject-only mutation cannot be authenticated by `capture_id` and
  therefore requires validation against exact native source evidence.
- Recommended preserving capture-status v1 and semantic contract v5.

## Slices 1–2 evidence

- Runtime construction now requires explicit real correlations and validates
  them against the exact selected result, receipt, run, and sole subject.
- Fixture-only sentinels are isolated from the runtime constructor.
- Subject identity remains required but outside the frozen capture-ID formula.
- Focused source and adjacent regression gates passed as recorded under
  `results/SLICE 1-2 SOURCE QUALIFICATION.md`.
- Successful packet and exact-delivery paths remain covered and green.
- API's existing five-test intake guard passes unchanged against the source
  overlay, including its backwards-compatible synthetic status helper call.
