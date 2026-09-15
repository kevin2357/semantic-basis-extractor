# Log — Python 3.11 editorial contract-resource compatibility

## 2026-09-15 — Sprint initialization

- Inspected only the latest local Render exports for the two named native runs.
- Left Better Stack exports untouched at the owner's direction.
- Joined the 0.4.62 phase diagnostics to the exact approved SBE source frame.
- Classified both witnesses as the same deterministic
  `typed_status_construction` / `_resource_bytes:221` `TypeError`.
- Identified the Python 3.11 versus 3.12 runtime difference and the
  multi-descendant `Traversable.joinpath(...)` call as the leading cause.
- Created this sprint's background, evidence register, log, and plan.
- Made no source, test, manifest, package, workspace, provider, API, or remote
  change.
- Paused at Review Gate A before reproduction or implementation.

## 2026-09-15 — API initial-plan review

- API approved the provider-free Slice 0 reproduction on real Python 3.11,
  with a Python 3.12 contrast and related-call-site inventory.
- API required proof that chained traversal returns byte-identical resource
  content and that missing or malformed resources remain failures.
- API confirmed no API contract, packet, lifecycle, transport, or Alloy change
  is indicated by the current evidence.
- Production source, version, package, release, deployment, and live witness
  remain unauthorized pending review of the reproduction.
