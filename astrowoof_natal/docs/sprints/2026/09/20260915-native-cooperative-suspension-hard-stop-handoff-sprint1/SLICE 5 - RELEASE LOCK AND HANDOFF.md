# Slice 5 — Release Lock and Handoff

## Release identity

| Evidence | Value |
| --- | --- |
| Distribution | `astrowoof-natal-authoring` |
| Version | `0.4.66` |
| Tag to create after approval | `astrowoof-natal-authoring-v0.4.66` |
| Artifact-source commit | `3907602c` |
| `SOURCE_DATE_EPOCH` | `1789534964` |
| Expected wheel | `astrowoof_natal_authoring-0.4.66-py3-none-any.whl` |
| Expected wheel SHA-256 | `ec30e79780b7a4ffc47510ec25f5b6cb3b09639a8b6a2ec6b2def0661f871daf` |
| Expected wheel size | `1,406,483` bytes |
| API joined revision | `613c0e01a7d473bf1aa0009e7902c23c98f6e093` |

The release-lock commit is the commit containing this record. The immutable tag
must target that commit, not the earlier artifact-source commit. The same
recorded epoch is retained because no package-affecting content changed after
the already-qualified 0.4.66 artifact build.

## Regression gate

The broad/full gate is required because this release changes shared v2
orchestration, reconciliation, native writer locking, and a cross-repository
public contract.

- Focused suspension/v2/manifest matrix: 74 passed, zero failures.
- Full checked-in manifest coordinator, one worker: 1,229 tests, three expected
  skips, zero failures, 1,308.851010 seconds.
- Full-suite inventory SHA-256:
  `ae272ce3009640bad4259db697e1c00bb92bfcdbf2ac754a59b87f1cc60591f0`.

The manifest initially refused to start because the three new suspension test
modules were unclassified. They were conservatively classified as
`provisional`; the focused gate was repeated before the successful full run.
No product behavior or test implementation changed after the full run.

## Installed and joined gates to repeat from this lock

1. Build twice from a clean export of the release-lock commit using the exact
   recorded epoch; require identical wheel names, sizes, inventories, and
   hashes.
2. Install that exact wheel into a clean environment; require `pip check`,
   installed version/import provenance, packaged contract/schema/fixture
   availability, and the public native-suspension qualification.
3. Repeat the joined API/SBE provider-free qualification against API revision
   `613c0e0`, including exact child-restart replay.
4. Preserve zero provider calls, spend, R2 access, live process termination,
   and API resource release.

## Operational boundary

This release supports exact interactive ordinary-v2 cooperative suspension at
the documented writer-locked safe points. Initial-wave fan-out, Batch, and
bounded routes remain unsupported. Parent-crash handling, exact child-death and
PID-reuse proof, worker-execution capacity reclamation, and later operator
assessment remain API-owned follow-up work. Neither the force fence nor the
native suspension result grants complete resource/custody release.

Tag creation and publication remain blocked on final technical review and the
owner's explicit authorization.
