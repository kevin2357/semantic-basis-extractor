# Slice 1 — promotion Batch 12 collision qualification

## Result

The complete four-module editorial-review cohort passed the approved bounded
collision matrix. This evidence supports a separate promotion decision; it does
not change the live 81/18/37 manifest.

## Matrix

Three repetitions ran two independent copies of every candidate in controlled
waves capped at six simultaneous child processes. All 24 secret-scrubbed
worker receipts passed.

| Module | Exact outcome in every copy | Worker-duration range | Identity SHA-256 | Outcome SHA-256 |
|---|---|---:|---|---|
| `test_editorial_review_contract_fixtures.py` | 9 tests, 0 skips | 4.371148–18.075944 s | `5ab18f953960fc986d655fefeaa933c65680fc994a736152330a6412d2400968` | `cb054ccb61abf95c144efd0a67f5ad934a68acaec364ec62301f318748250d73` |
| `test_editorial_review_contract_qualification.py` | 7 tests, 0 skips | 6.757368–7.418983 s | `bf926a39ca58bc02ef282a53fbd6726ee9fca0caeb9379e16026c526b297b0fc` | `288e2cad9ede90ac6c79054eb9ce91defef6ec1d8f7573588ee23e3578d43628` |
| `test_editorial_review_contract_foundation.py` | 12 tests, 1 skip | 0.236742–0.354286 s | `e9387acb4e6e8e54a0d645892818a11e3d3bffa51e7b5784e42ae3b42e5b3701` | `4570e52afbf51569eec56f504fccdcacd6212ae573aa8344741b24e3fe6d397e` |
| `test_editorial_review_runtime.py` | 11 tests, 0 skips | 0.514689–0.706633 s | `c87d4a6646494aedb987ae18cf7359240826a83f311b272a6e963a63e53f9018` | `4267ef3d0f39827478468ab1b5b462ff2263ae55f705c70ad9e045f5767f0fd9` |

Each module had one identity inventory and one outcome inventory across all six
copies. The sole skip was exactly
`TestEditorialReviewContractFoundation.test_optional_jsonschema_accepts_every_schema_document`.
There were zero failures, errors, expected failures, unexpected successes, or
additional skips.

## Isolation observations

- Every coordinator exited zero and emitted zero stdout/stderr bytes.
- No failed-worker stdout/stderr logs were materialized beneath the owned work
  roots.
- All 144 temporary evidence files remained beneath the single explicitly
  owned collision root; the repository stayed byte-clean.
- No Python process whose command line referenced Batch 12 or the editorial
  modules remained after the matrix.
- The qualification module's own provider-free guard continued to prohibit
  sockets and subprocess creation. Fixture child interpreters remained local,
  isolated, and digest-only.

Raw measurement receipts and child-worker receipts are retained at
`C:\tmp\sbe-batch12-collision-20260912` pending the promotion review. They are
diagnostic evidence, not repository or release artifacts.

## Next boundary

Pause for the separate promotion decision. If approved, move only these four
modules from `provisional` to `parallel_safe`, update their measured weights,
run runner/manifest guards, and then run repeated concurrent actual-manifest
stress proof before completion approval.

No other provisional promotion, semantic-closure movement, production/package
change, provider/external activity, or release work is authorized here.
