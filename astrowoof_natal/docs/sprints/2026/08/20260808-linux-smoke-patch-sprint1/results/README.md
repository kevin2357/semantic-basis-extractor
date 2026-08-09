# Sprint Results

Status: Slice 2 exact artifact qualification complete; gate approval pending.

- `SLICE 0 - Reproduction and Patch Boundary.md`: immutable baseline,
  normalized collision, platform ordering proof, cleanup masking, and exact
  patch boundary.
- `slice0-linux-reproduction.json`: compact machine-readable diagnostic
  evidence.
- `SLICE 1 - Deterministic Fake and Smoke Correction.md`: narrow source diff,
  normalization-safe fake output, structured failure, and regression results.
- `slice1-correction.json`: compact implementation and test evidence.
- `SLICE 2 - Exact Patch Artifact Qualification.md`: reproducible wheel audit,
  exact installed-wheel Windows/Linux results, and retained upstream identity.
- `slice2-artifact-qualification.json`: compact machine-readable artifact and
  cross-platform qualification evidence.

This directory will contain compact, independently reviewable evidence for the
Linux reproduction, narrow fake/smoke correction, exact 0.2.1 Windows/Linux
artifact qualification, and any separately authorized publication.

Large Docker workspaces, wheel builds, virtual environments, and raw acceptance
artifacts remain outside Git.
