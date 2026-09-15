# Python 3.11 editorial contract-resource compatibility correction

## Purpose

Correct a live SBE compatibility defect in editorial runtime capture after the
0.4.62 native diagnostics localized two independent delivery witnesses to the
same source line.

This is an SBE-owned package/runtime correction. It is not an API observer,
workspace-identity, editorial-evidence, packet, transport, or Better Stack
defect.

## Trigger

The latest two-pup cohort ran SBE 0.4.62 on the Render worker. Both terminal
delivery captures completed every native phase through packet validation and
then raised `TypeError` during `typed_status_construction`.

The safe diagnostic frame was identical in both runs:

- module: `editorial_review_contracts.py`;
- function: `_resource_bytes`;
- line: `221`; and
- deterministic failure fingerprint: `667a621a320f2cc5`.

The implicated expression passes two descendants to the resource
`Traversable.joinpath(...)` operation:

```python
files("astrowoof_natal_authoring.resources").joinpath(
    CONTRACT_PREFIX, name,
).read_bytes()
```

Render provenance reports CPython 3.11.15. The recent installed-wheel/API host
qualification used CPython 3.12.14. SBE declares Python `>=3.11`, so the leading
hypothesis is an untested Python 3.11 API-compatibility defect: the live
`Traversable` implementation does not accept the multi-descendant call shape
accepted by the qualification runtime.

## Current interpretation

Confidence is high because two distinct native runs, workspace roots, API run
IDs, and exact result IDs reached the same phase, frame, line, exception class,
and fingerprint. The evidence rules out all earlier capture phases and points
to deterministic shared code rather than subject-specific data.

The expected narrow correction is to join one component at a time while
preserving the same packaged resource and bytes:

```python
return (
    files("astrowoof_natal_authoring.resources")
    .joinpath(CONTRACT_PREFIX)
    .joinpath(name)
    .read_bytes()
)
```

That hypothesis must be reproduced on Python 3.11 before implementation is
approved.

## Non-goals

- No provider, R2, Better Stack, API, queue, lifecycle, or workspace mutation.
- No change to editorial packet, projection, transport, artifact, or capture
  status schemas.
- No latest-result discovery or identity substitution.
- No change to capture eligibility, evidence collection, assembly, validation,
  or delivery behavior.
- No release, deployment, or live witness before later explicit gates.

