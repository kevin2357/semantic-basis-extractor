# Evidence — editorial-review capture-status native identity correction

Status: discovery evidence only; implementation and qualification have not
started.

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

- branch-by-branch identity-source matrix;
- frozen subject-unavailable behavior;
- focused regression receipt;
- installed-wheel consumer evidence; and
- API/Vafflemutt review.

