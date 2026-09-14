# Closeout — Garamond / Quill Post-Rollout Observer Investigation

## Outcome

Investigation complete. The Garamond and Quill observation failures are
API-owned workspace-root identity defects, not SBE capture or transport
defects.

Both runs preserved their exact terminal result identity through API's bounded
publication retry and entered the observer. API then called SBE capture using
the outer checkpoint/run-label root instead of the native durable logical root
recorded in each workspace contract. SBE correctly failed closed during
snapshot validation.

The decisive paired control used each hash-verified retained archive twice:

- at API's supplied root, exact native reading failed during snapshot root
  validation;
- at the workspace's own durable root, exact reading and evidence collection
  returned `delivery`, followed by one packet, eight projections, and nine
  artifacts.

API reviewed and approved this classification. Its correction must persist and
carry the exact native durable workspace root alongside the exact checkpoint
and result identity through both initial terminal handling and publication
retry. It must not discover a latest workspace or derive a substitute root from
the API run ID.

## SBE disposition

No SBE runtime, package, schema, test-manifest, or Alloy change is required.
Stable-root validation remains strict and fail-closed. No release is opened by
this sprint.

All authorized external reads are exhausted. The disposable archives and
restores remain outside Git. No provider request, retry, native mutation,
publication, Better Stack write, lifecycle change, or QA-state change occurred
during investigation.
