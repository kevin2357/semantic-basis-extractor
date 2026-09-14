# Evidence

## Raw export identities

| Window | Bytes | SHA-256 |
| --- | ---: | --- |
| `18:15–18:30Z` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `18:30–18:45Z` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `18:45–19:00Z` | 717,649 | `6c9b9ecd3512fd01f70b07900621eb53552345a2ae49e89e156aa80c333646aa` |
| `19:00–19:15Z` | 1,715,593 | `0a0485a530ebd8fb6179e01c4588b3bbcbeef2d65728b2a5f809abf60ee1c934` |

## Corrected observer evidence

- Garamond SBE emitted invocation `ninv_282f6a5d9b754eeaba685f1a`, result
  `nres_8a0f803d144b9430fe945e6c`, and receipt
  `nreceipt_bc0a2a6938486fa73bc126f4`. After one publication retry, API emitted
  `editorial.observation.completed` for that exact result at
  `2026-09-14T19:06:09.708Z`.
- Quill SBE emitted invocation `ninv_79ff79fcaf4a4994b2b178aa`, result
  `nres_52b2b0fb130ed0fdca2dcbeb`, and receipt
  `nreceipt_fd7df83ce6c7bfbc9425685e`. After one publication retry, API emitted
  `editorial.observation.completed` for that exact result at
  `2026-09-14T19:10:15.699Z`.
- Both observer outcomes were identical: `branch=unavailable`,
  `failure_kind=capture_or_preflight`, `editorial_delivered=false`, and
  `artifact_count=0`.

The exact handoff and Sprint 96 carry-forward succeeded. The failure precedes
HTTP outcome classification and lies inside local capture construction or API
request preflight.

## Provider-free localization

- SBE's checked-in runtime fixture containing six accepted initial passes and
  accepted polish completed capture successfully. The exact-correlation and
  fail-closed ambiguity cases also passed: `3 passed`.
- API's complete editorial transport module passed provider-free: `15 passed`.
  This includes successful packet preflight, singleton typed capture-status
  preflight, successful observer packet dispatch, and successful observer
  capture-status dispatch.
- Source tracing shows that exact native-result reading and most runtime
  evidence collection occur before packet construction's guarded fallback.
  Errors there can escape to API's broad `capture_or_preflight` classification.
  A typed fallback can also fail closed while proving exact result, run, or
  subject identity; those cases are intentionally distinct from a successful
  unsupported capture-status result.

No provider, R2, Render, Better Stack, native mutation, or QA-state operation
was used. The retained Garamond/Quill workspace shape is now the smallest
unexamined input capable of separating primary SBE capture failure from a
shape-specific API preflight failure.
