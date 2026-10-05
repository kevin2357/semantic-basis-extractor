# Creating a processing profile

Use this procedure for a new semantic runtime recipe: for example bounded
instead of exact birth time, batch instead of live execution, an axis-aware
selection policy, a different SBE model/attempt policy, or a new prompt release.

## Before editing

1. Decide whether the desired change belongs in a prompt release, a processing
   profile, or both. A prompt/guidance-byte change always needs a new prompt
   release; a profile binding or flag change always needs a new profile.
2. Choose a new immutable profile ID and version. Never reuse an existing ID
   with altered JSON or a new digest.
3. Identify compatible deterministic-runtime and SBE-authoring package
   descriptors. These are package requirements, not image tags or deployment
   IDs.

## Package work

1. Add the new profile to
   `src/astrowoof_natal_authoring/resources/contracts/processing-profile-catalog.v1.json`.
2. Bind its exact `prompt_release.release_id` and `prompt_release.release_sha256`.
3. Set route, selection policy, deterministic fragment, SBE fragment, and both
   worker compatibility descriptors deliberately. The schema rejects unknown,
   missing, or noncanonical fields.
4. Compute the profile SHA-256 over canonical JSON with `profile_sha256`
   omitted, then recompute the catalog SHA-256 with `catalog_sha256` omitted.
   Use `processing_profile_sha256()` and the package validation tests rather
   than hand-rolling a serializer.
5. Update [../processing-profiles/CATALOG.md](../processing-profiles/CATALOG.md).

## Qualification and release

1. Add focused provider-free tests for the new profile and its rejection
   boundaries: wrong digest, wrong route/environment, missing prompt release,
   and incompatible package descriptor as applicable.
2. Build an isolated candidate wheel. Run the installed-wheel, API/SBE joined
   replay for the exact profile identity. A source-tree-only pass is not enough.
3. Obtain the required cross-repository review and record the wheel filename,
   SHA-256, byte size, catalog digest, profile digest, prompt-release digest,
   and package descriptors.
4. Follow the [Maintainer Release Playbook](../post_extraction_authoring/Maintainer%20Release%20Playbook.md)
   for immutable tag/publication. A new profile normally requires a new SBE
   wheel because the package-installed catalog changed.

## After publication

API must admit the exact profile identity and create or verify a compatible
worker-release context for both worker roles. Do not activate it merely because
the wheel exists. Activate it through the API control-plane workflow and retain
older contexts while any admitted runs may still need them for continuation or
recovery.
