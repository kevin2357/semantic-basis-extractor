# Selecting a processing profile

This is the deployment/control-plane procedure. It intentionally does not edit
SBE catalogs or prompt files.

## Preconditions

Before selection, verify that:

1. The desired profile ID and SHA-256 are present in the published SBE wheel.
2. Its referenced prompt release and component inventory validate in that same
   installed wheel.
3. API has admitted the exact immutable profile identity and has a compatible
   worker-release context for the deterministic-runtime and SBE-authoring roles.
4. The intended environment is listed in both the profile and prompt-release
   allowlists.

## Select for new runs

Use the API operator control plane to atomically set the active
profile/context pair for the target environment. Record the selection event and
read back the selected profile ID/digest, prompt-release ID/digest, and both
worker-route identities.

Do not infer a profile from a Docker image tag, and do not route a profile to a
worker context that merely looks newer. The profile's descriptors and the
context's immutable role routes must match.

## Recovery and rollback

- Existing runs keep their persisted profile and worker-release-context identity.
  They must resume there even after a different profile becomes active.
- Rollback means selecting a previously admitted profile/context pair for new
  runs. It does not rewrite manifests or reclassify existing runs.
- Retire a context only after the API inventory proves that no retained or live
  run can require it. In particular, keep historical contexts such as the
  `compat.v1` / SBE `0.4.66` bundle while recovery remains possible.

## Evidence to retain

For each activation or rollback, retain the operator identity, UTC time,
environment, old and new profile/context identity, package/image route
readbacks, and the admission/attestation result. Never include prompt text,
workspace paths, provider credentials, or raw deck content in this control-plane
evidence.
