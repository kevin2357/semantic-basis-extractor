# Slice 3 — Profile-bound prompt execution

**Status:** SBE exact-Natal/live compatibility path implemented and provider-free qualified; ready for the joined Gate C replay.

## Executable prompt selection

For a profile-aware semantic-closure invocation, SBE now resolves the installed
prompt release named by the already validated processing profile for the
ordinary `initial` and `retry` authoring stages.  The provider receives the
resolved installed text rather than an implicit hard-coded selection.

The compatibility asset has canonical LF-terminated package bytes for its
digest.  Its rendered system message deliberately removes only that final
asset terminator, preserving the exact pre-registry request text.  The focused
regression proves this byte-level compatibility.

Each provider instance created at the ordinary closure command boundary carries
safe release provenance by stage: release ID/version/digest, selected component
IDs and digests, and the rendered system-message digest.  Ordinary and retry
attempt metadata include that safe provenance; neither logs nor public results
gain prompt text, workspace contents, provider responses, or credentials.

The same command factory supplies the profile-bound configuration to ordinary,
polish, critic, and qualitative providers.  This first compatibility release
contains only the historical authoring system component, so it does not
redefine the distinct bounded or authority-only prompt assemblies.  Those
routes remain unsupported by this exact-Natal/live profile and cannot infer
coverage from it.

## Evidence

The focused provider-free profile tests now total **11 passing tests**.  They
cover package/catalog identity, role-package compatibility, all-or-none
handoff, replacement of contradictory CLI flags, initial/retry prompt-stage
provenance, and byte-equivalence of the compatibility system text.  The new
test remains listed in `tests/test_suite_manifest.json`.

## Gate C handoff

SBE is ready for the API-owned half to persist and pass the four-reference
handoff.  Gate C must run the exact installed SBE wheel against that API
envelope and verify the same profile digest, generation-manifest digest,
worker descriptor digest, and safe prompt-release attestation across creation
and resume/terminal evidence.  Wrong/missing IDs or digests must refuse before
provider submission.
