# Gate D — 0.4.67 candidate wheel (superseded)

> Superseded by the `0.4.68` candidate after the safe workspace-inventory
> attestation and immutable legacy-compatibility correction. Do not use this
> wheel for Gate D.

## Candidate coordinates

This is a provider-free, local Gate D candidate only. It has not been tagged, published, deployed, admitted by API, or selected for provider-backed work.

| Field | Value |
| --- | --- |
| Artifact-source commit | `e8dbf322c9cb2ae627fba745ed9891b3abdaad50` |
| Distribution version | `0.4.67` |
| `SOURCE_DATE_EPOCH` | `1790979368` |
| Canonical filename | `astrowoof_natal_authoring-0.4.67-py3-none-any.whl` |
| Retained candidate | `C:\tmp\sbe-0.4.67-gate-d-e8dbf322\wheel-a\astrowoof_natal_authoring-0.4.67-py3-none-any.whl` |
| SHA-256 | `db416ff44f2521b35dba3a5e141c7449e8f8266d77cfad65f3d53c825bed5ba9` |
| Byte size | `1,429,143` |

Two independent no-dependency, no-build-isolation builds from a clean `git archive HEAD` source export were byte-identical. The second retained build is under `wheel-b` beside the candidate.

## Final candidate identities

| Contract item | SHA-256 / version |
| --- | --- |
| Processing-profile catalog | `560f91f3e7a1ae1b1c7b08c7d1f727c723309d0041f3b9d36ded192e5c41e6a3` |
| Axis-aware profile | `d75a2a6e122a17440ecbb2e3894a6ce45dd7dbe807dfb3c7d7a802603258dd72` |
| Compatibility profile | `5fe18f925770c8b967a9b32b4ca749bc31363c806b0a186b042387ed37882d0e` |
| Prompt-release catalog | `e48a2b1c474d31cb82295cefa40b2b32f338f29b3a1241eb2f6f941c828cf4cc` |
| Editorial prompt release | `astrowoof.authoring.editorial.v2`, version `2.0.0`, SHA `089942e352e92fa2ad2e80ad8a3a705ef7976aa2c64e9001f2b068c84bffa94f` |
| Editorial authoring brief | `8097cc2639212f82a0ff2b916baacd3d4f7bdaeca3cce22c0ada4d10db659bbc` |
| Editorial guiding lights | `ac1625fed0e6791b7c39c79610e104ba9a99ea720f4ecbe5cba55a8a070e7d08` |

The SBE-authoring descriptor is `fdff9eca02c85ca6c9ae7787b10febe53b3ce4e0b088e5964d3c62e4508eaca7`, requiring `astrowoof-natal-authoring==0.4.67` and `semantic-projection-core==0.11.1`. The deterministic-runtime descriptor is `df053cefa0e436d784c6b49cc3b74d1fe9b33d0f6c5a18576a408934cafa1fbb`, requiring `astrology-graph-foundry==0.8.1` and `semantic-projection-core==0.11.1`.

## Installed-wheel checks

The exact retained wheel was installed no-deps into an isolated local target outside the checkout. It resolved from that target, reported `0.4.67`, validated both catalogs and the axis-aware profile, and resolved both editorial v2 workspace assets with their recorded digests. The wheel has 323 members, contains the required catalogs and assets, and has no build, distribution, cache, or bytecode members.

Focused version/profile/runtime qualification passed: 31 tests, including profile/catalog validation, axis-policy override, v2-only workspace asset selection, SBE subprocess profile-reference threading, and suite-manifest coverage.

## Safe-attestation finding

The installed `resolve_sbe_authoring_binding()` safely returns the processing-profile ID and SHA-256, generation-manifest SHA-256, route, selection policy, SBE worker descriptor, and prompt-release ID/version/SHA-256.

It does **not** return the v2 `workspace_components` inventory. Per-stage authoring provenance returns selected provider-prompt component digests and a rendered-prompt digest, but not the static workspace-guidance inventory. Therefore the API request to compare editorial guidance component-inventory digests is not yet satisfied by runtime safe attestation.

This is a narrow Gate D contract gap, not a wheel-integrity defect. Before calling this candidate release-locked or using it for final joined Gate D acceptance, either SBE must add sanitized workspace-component inventory to the attestation or both repositories must explicitly narrow the joint comparison to fields presently emitted. No scope change is made by this evidence record.
