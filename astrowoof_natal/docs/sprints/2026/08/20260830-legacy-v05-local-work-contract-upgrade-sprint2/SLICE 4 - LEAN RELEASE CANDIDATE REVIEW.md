# Slice 4 — lean release candidate review

## Candidate identity

- Version: `0.4.32`
- Dependency identity: `semantic-projection-core==0.11.1`
- Wheel: `astrowoof_natal_authoring-0.4.32-py3-none-any.whl`
- Wheel SHA-256: `c45cd46ff4d7ffa98024b662c55f840e8f7cbea9682d32e97273f6e451493d6e`
- Two controlled builds are byte-identical.

## Installed qualification

- Clean installed SBE identity: `0.4.32`
- Clean installed SPC identity: `0.11.1`
- `pip check`: no broken requirements.
- Generic `astrowoof-release-smoke --require-installed`: pass.
- Generic-smoke packaged resource count: 137.
- Generic-smoke resource-set SHA-256:
  `c920d88cd7c3166c0a275908f615f1c373aa81a5c33261e4dc4f7e2b446b9fa9`.
- Two separate installed invocations of
  `astrowoof-legacy-local-work-upgrade-qa` emitted byte-identical receipts.
- Installed qualification receipt SHA-256:
  `2401cba4fbf18c21238b34508d28494ad23067033ecfbd072ed256455a9800b1`.
- Receipt package identity: `0.4.32`.
- Provider create, retrieval, external network, and spend counts: zero.

## Packaged resources

- Fixture SHA-256:
  `04802af621aea7e0e769fc6c3d4d844179dd681beb70ebd6e8d95a23faa1f8f6`.
- Bundle-schema SHA-256:
  `3680fa78f203fab3162de9ade3f87a45c31b194b63cb56faa43bf74bfcf92dd7`.
- Qualification-schema SHA-256:
  `1e2209dedfe6843829e6b933807c09c560acf2002f75683e6f0da72af9ec8fb1`.
- The candidate wheel contains all three resources and the qualification console
  entry point.

## Test evidence

- Release-shaped focused legacy/v0.7/v0.8/qualification matrix: 36 passed, one
  optional-schema skip.
- Qualification-specific suite within that matrix: 9 passed, one optional-schema
  skip.
- Recomputed-digest mutation coverage protects the embedded v0.5 seam, stable
  joins, local source-action projection, retained/due custody projection,
  lineage-conflict outcome, receipt outcome, and privacy assertions.
- `git diff --check` is clean apart from informational Windows line-ending
  notices.

## Scope audit and test posture

The candidate changes only qualification code, package exports, a console entry
point, closed fixture/schema resources, tests, version metadata, and sprint
documentation. It does not alter lifecycle selection, provider transport,
custody, authority, snapshot, journal, or native mutation code.

Accordingly, this candidate uses the API-approved lean package-only release gate.
The full runtime suite was deliberately not run; this record does not imply that
it passed. If the scope changes before publication, this classification and gate
are invalid.

No retained-QA workspace, provider credential, provider operation, deployment,
or paid work was accessed or performed.

## Gate

Candidate preparation is complete. Commit, tag, and publication remain paused
for explicit owner and final API release approval.
