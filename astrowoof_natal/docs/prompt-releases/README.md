# Prompt releases

A prompt release is the closed, versioned collection of authoring instructions
used by SBE. It is not merely an OpenAI system prompt.

For current editorial releases, the component inventory includes:

- the `system_authoring` prompt supplied to initial, retry, polish, and critic
  stages; and
- workspace guidance copied into the authoring workspace, currently the
  authoring brief and guiding lights.

Each component has a logical component ID, a package resource path, and a
SHA-256 of canonical UTF-8, LF-terminated bytes. The prompt-release SHA-256 is
the canonical digest of the full release object and its inventory. SBE's safe
binding attestation can therefore identify the release and component hashes
without disclosing prompt text or workspace bytes.

## Why this is separate from a processing profile

A processing profile binds exactly one prompt release alongside route and runtime
settings. That lets one prompt revision be qualified as part of a specific
profile without mutating prior profiles or their recovery paths.

Do not edit a resource already referenced by a released prompt release. Copy it
to a new versioned resource, create a new release object, digest it, and bind a
new processing profile. The old release and resource remain installed for runs
that already persisted their identity.

See [../operations/creating-prompt-release.md](../operations/creating-prompt-release.md)
for the operator/developer workflow.
