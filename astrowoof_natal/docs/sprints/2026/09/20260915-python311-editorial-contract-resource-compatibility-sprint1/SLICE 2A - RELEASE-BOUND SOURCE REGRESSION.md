# Slice 2A — Release-bound source regression

## Outcome

The frozen SBE 0.4.63 source tree passes the two-runtime focused editorial
capture matrix and the manifest-controlled full repository suite. It is ready
to become the committed artifact-source identity before wheel construction.

## Identity freeze

- Fresh distribution version: `0.4.63`.
- Required eventual tag: `astrowoof-natal-authoring-v0.4.63`.
- Local tag and GitHub release identity were confirmed unused.
- Version was updated before either release-bound suite.
- No non-sprint version-derived fixture or test expectation required an update.

## Focused matrix

The focused matrix includes contract resource readers, both editorial fixture
worlds, qualification, public delivery/review capture, typed-status
construction, and native diagnostics.

- CPython 3.11.15: 45 tests, 1 optional skip, zero failures.
- CPython 3.12.14: 45 tests, 1 optional skip, zero failures.

The Python 3.11 run used the official `python:3.11.15-slim` container with the
repository mounted read-only. No installed candidate existed yet.

## Full manifest gate

Command:

```text
python astrowoof_natal/scripts/run_test_suite.py
```

Result:

- interpreter: CPython 3.12.14;
- tests: 1,200;
- expected skips: 60;
- failures: 0;
- wall time: 1,133.50017 seconds; and
- test inventory SHA-256:
  `3831ed792e633b43128e611e93738d8da0af9a0ed4b22f192faa853828ce9b9e`.

The exact coordinator receipt was emitted under the process-owned system temp
directory. Its compact durable fields are retained in
`results/slice2-source-regression.json`.

## Safety and model ruling

- Provider operations: zero.
- Application network operations: zero.
- R2/Better Stack operations: zero.
- Authoritative workspace mutations: zero.
- Alloy impact: none; resource traversal compatibility changes no modeled
  lifecycle, authority, custody, selection, packet, or transition semantics.

## Next boundary

Commit this exact tested artifact source, inspect tracked/untracked package
inputs, then build twice from a clean committed export at one recorded
`SOURCE_DATE_EPOCH`. No tag or publication is authorized.

