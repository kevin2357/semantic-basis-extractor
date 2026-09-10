# Evidence — editorial-review capture-status native identity correction

Status: Slices 0–3 complete through exact release-lock qualification; final
API/Vafflemutt pre-tag review and explicit tag/publication authorization remain.

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

- final API/Vafflemutt pre-tag review; and
- explicit owner authorization for the immutable tag and GitHub publication.

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

## Slice 3 evidence

- Frozen candidate version `0.4.56` before package qualification.
- Two fixed-epoch candidate wheels were byte-identical at 1,376,426 bytes and
  SHA-256 `56be2706c792014468081fdf0fab8d101bf250141e97f349ba4e921d9d0abe82`.
- Clean installation used SPC `0.11.1`, jsonschema `4.26.0`, and tzdata
  `2026.3`; `pip check` was clean and imports resolved from `site-packages`.
- All 27 focused installed tests passed without skips.
- Four API functional consumer cells passed against the installed candidate and
  an independent version assertion confirmed `0.4.56`.

## Exact release-lock evidence

- Release-lock commit:
  `a43067f580c5d4b727333a0eb54422191f73fa77`.
- Recorded `SOURCE_DATE_EPOCH`: `1789031187`, the release-lock commit time.
- The checked-in coordinator's broad/full gate passed 1,161 tests with 60
  expected skips in 975.036 seconds. Its classified test-inventory SHA-256 was
  `888609c217425c0afc20f1ffef5feaf436cc3779def38c7c8aa1f065767d1740`.
- Two clean committed-source exports produced byte-identical wheels with 307
  identical members, no forbidden cache/bytecode/build/private members, size
  1,379,722 bytes, and SHA-256
  `31a82e5121a3a43c62843f7ee39e8359ecd8485245e6b35f555892a41f4ed551`.
- A fresh exact-wheel environment passed `pip check`, resolved SBE from
  `site-packages`, exposed version `0.4.56` and both new public symbols, passed
  all 27 focused tests, installed `astrowoof-release-smoke
  --require-installed`, installed `astrowoof-editorial-review-qa`, four API
  functional consumer cells, and the independent API-side version assertion.
- API's checked-in released-baseline assertion remains `0.4.55` by design and
  was not rewritten before publication approval.
