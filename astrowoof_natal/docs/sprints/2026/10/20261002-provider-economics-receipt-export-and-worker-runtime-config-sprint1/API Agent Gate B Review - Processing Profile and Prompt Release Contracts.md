# API Agent Gate B Review — Processing Profile and Prompt Release Contracts

**Reviewer:** AstroWoof API agent  
**Review date:** 2026-10-02  
**Scope reviewed:** SBE Slice 1 contract, installed catalogs, resolver, and
provider-free negative-path coverage. No provider, workspace, deployment, or
environment mutation was performed by this review.

## Decision

**API approves the SBE-owned `processing_profile.v1` and
`prompt_release.v1` contracts for Gate B. Slice 1β resolves the remaining
worker-compatibility concern with the correct two-layer model.**

The SBE implementation is appropriately closed and provider-free at this
stage. It validates strict canonical JSON and self-digests, refuses malformed
or uninstalled values, keeps package assets LF/UTF-8 canonical, and does not
yet alter an existing worker command or provider construction path. That is the
right boundary for this gate.

The approved initial compatibility tuple is:

| API-preserved fact | Approved SBE value |
| --- | --- |
| Profile schema | `astrowoof.processing_profile.v1` |
| Processing profile ID | `astrowoof.exact_natal.live.compat.v1` |
| Processing profile SHA-256 | `28a92d24dbbc10597c11c5bca0309ee9ea7aad5168069138f5e76dd90e32bf7a` |
| Profile version | `1.0.0` |
| Route family / contract | `exact_natal` / `astrowoof.semantic_closure_run.v0.9` |
| Execution mode | `live` |
| Selection policy | `legacy_atomic.v1` |
| Prompt release ID / SHA-256 | `astrowoof.authoring.compat.v1` / `51e58cb41cf4a317b4fa37e77e18f57567bd4976b56d6e9fa788154b4c1e3d5c` |
| Prompt release version | `1.0.0` |
| Prompt component / SHA-256 | `system_authoring` / `2ec0738497756b09887e921273371b4f99108378b9197ce9b065beeacd453a71` |

`qa` and `production` are the only environments approved by the installed
catalog for this initial tuple. Bounded, batch, and `axis_aware` combinations
remain unsupported and must refuse; neither repository may infer their support
from the presence of a general catalog schema.

### Slice 1β compatibility closure

The republished profile adds closed, digest-validated package-requirement
descriptors under `worker_compatibility`:

| Worker role | Descriptor SHA-256 |
| --- | --- |
| `deterministic_runtime` | `df053cefa0e436d784c6b49cc3b74d1fe9b33d0f6c5a18576a408934cafa1fbb` |
| `sbe_authoring` | `ed51592f2d32ec803054ec0353c7ac5dfac336475c43c6992404a9449559e581` |

This is the correct interpretation of a profile-owned compatibility identity:
it attests the semantic package requirements and is covered by the final
profile digest. API's existing environment-specific deployed-worker identity
remains an outer generation-manifest/image-rollout fence. A worker must verify
both layers; neither is an alternative to the other.

## Shared API/SBE mapping

API will extend its existing immutable generation manifest and run binding with
the profile **reference**, not a caller-provided or mutable copy of the SBE
bundle. At admission the durable evidence must include:

```json
{
  "processing_profile": {
    "schema_version": "astrowoof.processing_profile.v1",
    "processing_profile_id": "astrowoof.exact_natal.live.compat.v1",
    "processing_profile_sha256": "28a92d24dbbc10597c11c5bca0309ee9ea7aad5168069138f5e76dd90e32bf7a",
    "profile_version": "1.0.0",
    "route": {
      "family": "exact_natal",
      "execution_mode": "live",
      "sbe_contract": "astrowoof.semantic_closure_run.v0.9"
    },
    "selection_policy": "legacy_atomic.v1",
    "prompt_release": {
      "release_id": "astrowoof.authoring.compat.v1",
      "release_sha256": "51e58cb41cf4a317b4fa37e77e18f57567bd4976b56d6e9fa788154b4c1e3d5c"
    }
  }
}
```

The complete API `GenerationProfile.manifest_sha256` remains a separate
immutable digest of the whole generation manifest. It is not interchangeable
with the SBE profile's self-digest above.

The prompt release’s semantic version is safe provenance and should be emitted
by SBE’s validated installed-release attestation and retained by API in
action-level provenance. It need not be duplicated in the profile’s
`prompt_release` reference, whose exact approved schema is ID plus SHA-256.

## Boundary clarifications agreed by API

1. `route.execution_mode = live` is not the same dimension as
   `sbe.provider_service_level = interactive`. API will preserve both where
   needed and will not rename either to make them appear synonymous.
2. SBE’s profile bundle owns semantic/runtime choices, prompt-release binding,
   and role-specific package compatibility descriptors. API resolves and
   verifies those profile-owned values, then persists their immutable binding
   in its outer generation manifest. API separately persists the
   environment-specific deployed-worker identity used to fence the selected
   image; it does not independently configure profile semantics.
3. API-to-worker launch input remains ID, expected profile SHA-256, full API
   manifest SHA-256, route family, and worker role—not arbitrary profile JSON,
   prompt text, environment values, secret references, grants, workspace
   paths, or user-supplied overrides.
4. SBE safe return evidence should contain profile ID, profile SHA-256, profile
   version, route tuple, selection policy, prompt release ID/SHA-256/version,
   installed worker compatibility identity, and worker role. It must exclude
   prompt text, rendered request text, user content, provider response text,
   secret material, and paths. Action-level component inventory and rendered
   request digests remain Slice 3 provenance work.
5. Retry, polish, resume, reconciliation, detached continuation, and recovery
   must reuse the persisted profile binding. A current catalog default may not
   replace it. Legacy workspaces remain on their existing recovery reader path
   without synthetic profile or prompt provenance.

## Review evidence

- `processing_profiles.py` uses closed exact-key schemas, duplicate-key and
  non-finite-value rejection, canonical JSON serialization, self-digest
  validation, catalog cross-reference validation, and canonical prompt-asset
  bytes.
- The installed catalogs exactly bind the approved profile to the approved
  prompt release and constrain both to `qa` and `production`.
- The resolver checks that the referenced release is installed and mutually
  allows the profile and route.
- Slice 1's stated negative coverage is consistent with the implementation
  boundary: it is provider-free and does not yet touch command launch,
  workspace, or provider construction.

## Follow-up for the API repository

API has revised its pre-Gate-B proposal to adopt SBE’s exact underscore schema
identifier, the final profile digest, and the two-layer compatibility model.

With reciprocal review complete, SBE may proceed to Slice 2. This API
review does **not** authorize a deployment, provider-backed QA, or a newly
admissible non-compatibility profile.
