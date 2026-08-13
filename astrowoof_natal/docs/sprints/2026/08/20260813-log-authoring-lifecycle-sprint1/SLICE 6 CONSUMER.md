# Slice 6 Consumer Surface and Installed Qualification

Status: complete, 2026-08-13

Slice 6 publishes a dedicated `astrowoof-authoring-lifecycle` command for inspect,
provider-less denial, and closeout, plus `astrowoof-lifecycle-smoke` for provider-free
installed qualification. The equivalent Python functions remain supported.

Schemas, the event payload catalog, contract catalog, and seven lifecycle fixtures
are package resources. Consumers locate them via `resource_access`, never repository
paths.

The lifecycle smoke constructs a sanitized prepared-action workspace and exercises:

- exact read-only inspection;
- provider-less eligibility;
- durable negative authorization;
- fresh post-mutation inspection;
- closeout and byte-stable replay;
- denial and closeout events; and
- final complete snapshot validation.

The smoke has no provider client, API key, network requirement, or paid operation.
`--require-installed` rejects source-tree execution.

A temporary 0.2.2 qualification wheel was built and installed into a fresh venv
outside the repository. Its SHA-256 was
`29914a16f4c64075575cd5754796bc5bedef7c9573eea4f03db2c4dbd2dcc7fe`; this is
evidence for this source checkpoint only and is not a promoted, tagged, or pinnable
release artifact.

The complete consumer sequence and ownership boundary are documented in
`docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`.
