# API Agent Gate B Review — Processing Profile and Prompt Release Contracts

**Reviewer:** AstroWoof API agent  
**Review date:** 2026-10-02  
**Scope reviewed:** SBE Slice 1 contract, installed catalogs, resolver, and
provider-free negative-path coverage. No provider, workspace, deployment, or
environment mutation was performed by this review.

## Decision

**API approves the SBE-owned `processing_profile.v1` and
`prompt_release.v1` contract direction, subject to the shared mapping below.
Gate B remains pending SBE's required worker-compatibility-identity addition
and the resulting republished profile digest.**

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
| Processing profile SHA-256 | `e1affc78ab278d20be990ba8652ee3991a4e672012358ae889cc39f5bc565a2d` |
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

### Reciprocal-review addendum

SBE's reciprocal API review correctly requires the deterministic-runtime and
SBE-worker compatibility identities to be frozen **inside** the canonical
profile rather than supplied independently by API deployment settings. The
current catalog does not yet contain those fields, so the profile SHA-256 shown
above is not the final joint admission digest. API accepts that correction:
after SBE adds the exact fields and republishes the catalog, API will review
the replacement profile ID/digest/field names and bind those resolved values
into its outer immutable generation manifest. No Slice 1 work starts first.

## Shared API/SBE mapping

API will extend its existing immutable generation manifest and run binding with
the profile **reference**, not a caller-provided or mutable copy of the SBE
bundle. At admission the durable evidence must include:

```json
{
  "processing_profile": {
    "schema_version": "astrowoof.processing_profile.v1",
    "processing_profile_id": "astrowoof.exact_natal.live.compat.v1",
    "processing_profile_sha256": "e1affc78ab278d20be990ba8652ee3991a4e672012358ae889cc39f5bc565a2d",
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
   and—after the pending catalog amendment—the two qualified worker
   compatibility identities. API resolves and verifies those profile-owned
   values, then persists their immutable binding in its outer generation
   manifest; it does not independently configure them.
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

API will revise its pre-Gate-B proposal to adopt SBE’s exact underscore schema
identifier and field vocabulary, then obtain the reciprocal SBE review before
starting its persistence migration or runtime-consumer slices.

With that reciprocal review complete, SBE may proceed to Slice 2. This API
review does **not** authorize a deployment, provider-backed QA, or a newly
admissible non-compatibility profile.
