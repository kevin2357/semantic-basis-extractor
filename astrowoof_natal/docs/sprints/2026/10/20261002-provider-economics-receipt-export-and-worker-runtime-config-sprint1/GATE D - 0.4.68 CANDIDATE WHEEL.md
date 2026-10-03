# Gate D — 0.4.68 candidate wheel

## Candidate coordinates

This retained candidate is provider-free only. It is not tagged, published,
deployed, or admitted by API.

| Field | Value |
| --- | --- |
| Artifact-source commit | `0f6979fba6674785bf188d5c1d7561e127205a73` |
| Release-lock/tag commit | `ed4b8643` |
| Distribution version | `0.4.68` |
| `SOURCE_DATE_EPOCH` | `1790984940` |
| Filename | `astrowoof_natal_authoring-0.4.68-py3-none-any.whl` |
| Retained wheel | `C:\tmp\sbe-0.4.68-release-lock-ed4b8643\wheel-a\astrowoof_natal_authoring-0.4.68-py3-none-any.whl` |
| SHA-256 | `d9636e5eadc302681040f2a732a3755f2db689e66bc18e3cfac8ea27b4c2b215` |
| Byte size | `1,429,258` |

Two clean archive builds were byte-identical. The second retained copy is in
the sibling `wheel-b` directory.

The exact retained wheel was installed into an isolated environment outside the
checkout. It resolved from `site-packages` as version `0.4.68`; `pip check`
passed after installing the declared transitive `jsonschema` requirement of
SPC `0.11.1`; and `astrowoof-release-smoke --require-installed` passed.

## Final candidate contract identities

- Processing-profile catalog:
  `d5306dd374e123b6b8339581520a50ea64a0b317dcc18719e4329d5a09cb33e5`
- Axis-aware profile `astrowoof.exact_natal.live.axisawaresbe.v1`:
  `da9f8dbd50421e0b556ee71cdd0b2ca54baebbc91ef2eb7f1137fa836488ff63`
- Historical compatibility profile `astrowoof.exact_natal.live.compat.v1`:
  `28a92d24dbbc10597c11c5bca0309ee9ea7aad5168069138f5e76dd90e32bf7a`
- Prompt-release catalog:
  `e48a2b1c474d31cb82295cefa40b2b32f338f29b3a1241eb2f6f941c828cf4cc`
- Editorial release: `astrowoof.authoring.editorial.v2`, version `2.0.0`,
  SHA `089942e352e92fa2ad2e80ad8a3a705ef7976aa2c64e9001f2b068c84bffa94f`.

The axis-aware SBE descriptor is
`e856d876e2d1ff6c234ca9624cd367602d1363519be7e0102c39b67b1ce64585`:
`astrowoof-natal-authoring==0.4.68` and
`semantic-projection-core==0.11.1`. The deterministic descriptor remains
`df053cefa0e436d784c6b49cc3b74d1fe9b33d0f6c5a18576a408934cafa1fbb`.

## Custody and attestation result

`compat.v1` is restored byte-for-byte to its finalized `0.4.66` profile
identity and retains its `0.4.66` SBE package requirement. The installed
`0.4.68` wheel consequently refuses to bind it with `required SBE distribution
version mismatch`; it cannot impersonate the legacy worker. Recovery must
route that persisted profile to its matching `0.4.66` worker context.

The new axis-aware binding safely attests, under `prompt_release`, the release
ID, semantic version, SHA-256, and sorted static workspace inventory:

```json
[
  {"logical_name":"AUTHORING BRIEF.md","sha256":"8097cc2639212f82a0ff2b916baacd3d4f7bdaeca3cce22c0ada4d10db659bbc"},
  {"logical_name":"GUIDING LIGHTS.md","sha256":"ac1625fed0e6791b7c39c79610e104ba9a99ea720f4ecbe5cba55a8a070e7d08"}
]
```

No paths, prompt prose, asset bytes, provider data, or credentials are in the
attestation. Focused provider-free qualification passed 32 tests. The exact
wheel installed outside the checkout, resolved from that installation, exposed
the expected safe binding, and contained all required assets with no generated
or cache members.

## Broad-suite qualification note

The one manifest-driven broad suite was run once for this candidate. Its first
pass exposed a local Windows checkout issue, not a package or test defect: the
versioned `provider-economics/mutation-corpus.v1.json` fixture had materialized
with CRLF bytes even though Git stores its required LF bytes. The existing
mutation-corpus digest assertion correctly refused that drift. Restoring the
single checked-out fixture to its committed LF bytes made the targeted test
pass without changing the test or fixture. This is recorded as a local
checkout-normalization snafu; final release builds remain archive-based and
therefore consume the committed canonical LF bytes.

## Publication verification

Published as [astrowoof-natal-authoring-v0.4.68](https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.68)
at `2026-10-03T00:03:55Z` (release ID `RE_kwDOToQdE84X-ZYv`). The uploaded
wheel asset `RA_kwDOToQdE84kKlOr` is 1,429,258 bytes and GitHub reports
`sha256:d9636e5eadc302681040f2a732a3755f2db689e66bc18e3cfac8ea27b4c2b215`.
Both published assets were freshly downloaded to a separate directory. The
downloaded wheel SHA-256 and `SHA256SUMS.txt` entry match the qualified value
exactly. The annotated tag's remote peeled target remains
`ed4b8643384c544ec04fc239c1e4e4a2562dd07e`.

## Remaining Gate D work

API must admit the exact axis profile and its worker-release/pool identity,
retain the historical compat mapping unchanged, and compare this sanitized
inventory alongside the existing prompt/profile/role identities in the joined
provider-free replay. No current-image substitution is permitted for a
persisted legacy run.
