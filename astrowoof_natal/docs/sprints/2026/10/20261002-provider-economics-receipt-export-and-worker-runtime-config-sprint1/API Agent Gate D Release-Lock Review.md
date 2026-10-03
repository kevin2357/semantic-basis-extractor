# API Agent Gate D release-lock review

**Decision:** approved for SBE `0.4.68` tag and publication.

## Reviewed coordinates

- Artifact source: `0f6979fba6674785bf188d5c1d7561e127205a73`
- Release lock: `ed4b8643`
- Wheel: `astrowoof_natal_authoring-0.4.68-py3-none-any.whl`
- Final SHA-256:
  `d9636e5eadc302681040f2a732a3755f2db689e66bc18e3cfac8ea27b4c2b215`
- Profile catalog:
  `d5306dd374e123b6b8339581520a50ea64a0b317dcc18719e4329d5a09cb33e5`
- Axis-aware profile:
  `astrowoof.exact_natal.live.axisawaresbe.v1` /
  `da9f8dbd50421e0b556ee71cdd0b2ca54baebbc91ef2eb7f1137fa836488ff63`

## Independent release-lock check

The prior provider-free candidate archive (`9840101a…`) and the release-lock
archive have different whole-wheel hashes, as expected after the release-lock
archive build epoch changed. Their 323 ZIP members have the same names and
identical uncompressed SHA-256 content hashes. The only source-tree delta from
the artifact commit through `ed4b8643` is Gate-D documentation. Therefore the
final `d963…` hash is the correct immutable release coordinate.

API has changed its QA-only candidate pin and local deterministic qualification
recipe to the final hash. It rebuilt an isolated local deterministic image from
the release-lock wheel, verified the SHA in the Docker build, and reran the
joined provider-free matrix against the exact installed release-lock artifact.

Result: **94 passed**, including real API handoff, installed SBE resolver,
installed semantic-closure CLI with contradictory legacy-policy input,
network-isolated deterministic execution, and digest-mismatch refusals. Ruff,
JSON validation, and diff checks passed. No image push, deployment, profile
activation, database mutation, or provider action occurred.

## Boundary retained

Approval is for SBE tagging/publishing the immutable package. It does not
activate the new profile in QA, deploy a worker context, or authorize any
provider-backed run. Historical compat remains routed to its matching `0.4.66`
context rather than the new release.
