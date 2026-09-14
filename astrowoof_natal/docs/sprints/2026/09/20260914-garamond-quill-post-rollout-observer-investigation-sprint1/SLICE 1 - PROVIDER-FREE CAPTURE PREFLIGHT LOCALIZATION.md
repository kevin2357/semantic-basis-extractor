# Slice 1 — Provider-Free Capture/Preflight Localization

## Result

Slice 1 does not reproduce the Garamond/Quill failure from checked-in source
and fixtures. Both the accepted-polish SBE capture path and API's packet/status
preflight paths pass. The investigation therefore stops at the conditional
exact-workspace review gate in Slice 2.

## Safe phase map

| Phase | Provider-free result | Residual live possibility |
| --- | --- | --- |
| Exact result/receipt read and source join | Exact and ambiguity guards pass | A retained-workspace file or identity contradiction can raise before fallback |
| Runtime evidence collection | Six initial winners plus accepted polish passes | A live-only path, report, digest, action, or disposition shape can differ |
| Typed capture-status fallback | Exact unsupported status passes; ambiguous identity refuses | Fallback cannot lawfully describe a failure if run/subject/result identity itself is unproven |
| Packet/projection/artifact construction | Accepted-polish fixture succeeds | A retained artifact or optional-history shape can fail construction |
| API native-event envelope and request preflight | Packet and singleton status paths pass | A live packet's count, size, source, or event shape can differ |
| HTTP post | Not entered by the live outcome classification | Not the first demonstrated failure |

The source boundary matters. `build_editorial_review_runtime_capture()` calls
`collect_editorial_review_runtime_evidence()` before entering the guarded
packet-construction block. Exact read/source exceptions and some evidence-file
exceptions therefore escape directly. API currently catches those together
with envelope and preflight exceptions and emits the single public
`capture_or_preflight` outcome. Conversely, evidence conditions with proven
identity can return a typed `editorial_review_capture_status.v1`; exact-identity
ambiguity correctly raises instead of fabricating a status.

## Commands and outcomes

SBE focused provider-free gate:

```text
python -m unittest \
  ...test_runtime_evidence_collects_six_exact_pass_winners_read_only \
  ...test_runtime_status_uses_distinct_exact_native_correlations \
  ...test_runtime_status_refuses_selected_result_or_subject_ambiguity

Ran 3 tests in 0.327s — OK
```

API provider-free observer/preflight module:

```text
python -m pytest -p no:cacheprovider \
  tests/test_editorial_review_transport.py -q

15 passed in 0.52s
```

The API module covers deterministic packet preflight, artifact separation,
singleton capture-status preflight, successful packet observer dispatch,
successful typed-status dispatch, and fail-closed malformed/oversize inputs.

## Review gate

Provider-free evidence cannot choose between a live-shape SBE capture failure
and a live-shape API preflight failure. The smallest next step is Slice 2's
bounded reproduction against exact Garamond and Quill checkpoint coordinates.
That step remains unauthorized. It requires API to provide exact immutable
coordinates and the owner to authorize at most one conditional metadata read
and one bounded object read for each named checkpoint.

No runtime/package code was changed. No provider, R2, Render, Better Stack,
native mutation, retry, publication, or QA-state operation occurred.
