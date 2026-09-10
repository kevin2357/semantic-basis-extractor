# API technical approval — SBE 0.4.56 release lock

Status: technical approval granted for owner authorization to tag and publish
the exact qualified candidate.

## Verified release identity

- Required tag target: `a43067f580c5d4b727333a0eb54422191f73fa77`
- Candidate wheel:
  `astrowoof_natal_authoring-0.4.56-py3-none-any.whl`
- SHA-256:
  `31a82e5121a3a43c62843f7ee39e8359ecd8485245e6b35f555892a41f4ed551`
- Size: `1,379,722` bytes

API independently recalculated the SHA-256 for both release-lock wheel builds;
both matched the declared digest and byte size. The release-lock commit resolves
on `origin/main`; no tag points at it. The later documentation commit is not a
permitted tag target.

The reported full-suite, installed-wheel, public qualification, and four-cell
API consumer evidence is sufficient for this narrow corrective release. The
new public capture-status constructor/validator is compatible with API's
existing 0.4.55 consumer boundary and unblocks the later Slice 2C runtime-hook
qualification.

This approval does not authorize an API deployment, Better Stack write, or QA
cohort; it authorizes only SBE immutable tag/release publication under the
release playbook.
