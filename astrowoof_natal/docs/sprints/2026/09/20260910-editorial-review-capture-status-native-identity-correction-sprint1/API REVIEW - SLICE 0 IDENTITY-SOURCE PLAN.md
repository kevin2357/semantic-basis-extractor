# API review — Slice 0 identity-source plan

Status: approved for the provider-free implementation and qualification slices.

The plan precisely addresses API Sprint 87's discovery. The correction belongs
to SBE: API will not rewrite native capture-status contents, manufacture
correlations, rehash a native status, or use latest-result discovery.

## Approved decisions

- Keep `editorial_review_capture_status.v1` and the released semantic manifest
  identity domain unless Slice 0 proves a genuine impossibility.
- Require an exact selected-result read and verify caller-selected result ID,
  result document ID, and receipt-bound result ID agree before producing a
  runtime status.
- Populate the three required status correlations only from durable, validated
  native evidence. `subject_id` must be exact; it may not be inferred from a
  path, fixture sentinel, or API correlation.
- Derive `capture_id` exactly from the frozen manifest formula:
  `native_run_id`, `native_result_id`, `reason`, and `detail_code`. Though
  `subject_id` remains required status content, it must not independently alter
  the capture identity.
- If any required identity cannot be proven, emit no status rather than a
  partial or fabricated v1 object. The runtime's local fail-closed result is
  preferable to a misleading Better Stack observation.
- Preserve successful packet/projection/artifact bytes and the exact-delivery
  handoff behavior byte-for-byte. No lifecycle, terminal settlement, cleanup,
  or provider behavior is in scope.

## Qualification additions requested

The listed matrix is sufficient. Please also prove that the same selected
result with a subject mismatch cannot produce a status, and that changing only
`subject_id` in an otherwise hypothetical rehashed status does not define a
new legitimate `capture_id` domain. The latter is a negative semantic check,
not permission to omit `subject_id` from the v1 payload.

After installed-wheel evidence is available, API will rerun its exact consumer
and transport tests before enabling any runtime observation hook.
