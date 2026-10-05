# Creating a prompt release

Use this procedure whenever anything sent to, or mounted for, the authoring
model changes. That includes system instructions, authoring briefs, style
guidance, evaluation guidance, and any other declared workspace asset.

## Create a closed asset set

1. Copy each changed asset to a new versioned package resource under
   `src/astrowoof_natal_authoring/resources/authoring/`. Do not overwrite an
   asset referenced by an earlier release.
2. Keep every asset UTF-8, LF-terminated, and free of carriage returns. SBE
   validates those byte rules before accepting a component digest.
3. Inventory every component used by each stage. `components` covers direct
   stage prompt material; `workspace_components` covers files copied into the
   authoring workspace. Do not rely on an undeclared ambient file.

## Register and bind

1. Add a new release object to
   `src/astrowoof_natal_authoring/resources/contracts/prompt-release-catalog.v1.json`.
2. Give it a new immutable release ID/version and component SHA-256 values.
   Define every stage's selected components and the intended profile IDs.
3. Calculate `release_sha256` using `prompt_release_sha256()`, then refresh the
   prompt catalog SHA-256. Run catalog validation to catch noncanonical order,
   invalid paths, duplicate components, or digest mismatch.
4. Create a new processing profile that references this exact release ID and
   digest. A new prompt release is not selectable by itself.
5. Update [../processing-profiles/CATALOG.md](../processing-profiles/CATALOG.md)
   and the profile documentation.

## Qualify safely

Run provider-free package and installed-wheel checks first. The safe attestation
and API manifest should retain only release/profile identifiers, release/profile
digests, and the workspace component logical names and SHA-256 values. Prompt
text, workspace paths, and component bytes do not belong in that boundary.

After the profile's wheel is released and admitted, use the selection runbook;
do not change a prior run's prompt identity to test the new one.
