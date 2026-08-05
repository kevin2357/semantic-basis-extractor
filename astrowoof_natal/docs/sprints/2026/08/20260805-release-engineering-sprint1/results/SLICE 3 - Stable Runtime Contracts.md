# Slice 3 — Stable Runtime Contracts

## Result

Slice 3 passed. Runtime boundaries that were previously encoded only in
directory conventions and evolving JSON objects now have named, versioned
contracts and documented compatibility behavior.

## Contract catalog

| Boundary | Version |
|---|---|
| Projected natal input | `astrowoof.projected_natal_input.v0.1` |
| Subject parameters | `astrowoof.subject_params.v0.1` |
| Operator run state | `astrowoof.semantic_closure_run.v0.7` |
| Public polling state | `astrowoof.semantic_closure_public_run.v0.1` |
| Authoring profile | `astrowoof.authoring_profile.v0.1` |
| Delivery manifest | `astrowoof.natal_delivery_manifest.v0.1` |

The installed package carries a machine-readable contract catalog. The full
consumer-facing description is maintained in `Runtime Contracts.md`.

## Input normalization

The preferred input supplies `astrowoof-input-manifest.json`, with one subject
ID and four relative projected-context paths per subject. Paths are contained
within the input root, must exist, and a subject's contexts must share one
directory. The historical filename-driven direct and multi-subject layouts
remain accepted and are explicitly labeled `legacy-directory-v0` after
normalization.

Historical unversioned `params.json` remains accepted. It is validated and
normalized to `astrowoof.subject_params.v0.1` before use.

## Run-state separation

`run.json` remains the durable operator and resume artifact. New runs now
record their normalized input contract and complete authoring profile.

Every state save also writes `public-run.json`. It contains only status,
timestamps, service level, aggregate pass progress, per-subject status, and
delivery readiness. It omits filesystem paths, provider configuration,
attempt evidence, request material, and internal QA details.

## Delivery boundary

Subject deliveries now contain five artifacts:

1. authored deck;
2. assembly report;
3. validation report;
4. lint report; and
5. versioned delivery manifest.

The manifest identifies artifact roles, subject, final status, operator-run
contract, and authoring profile. Hash and engine-provenance fields are
intentionally deferred to Slice 4.

## Compatibility verification

- operator-run v0.2–v0.6 migration remains supported;
- old projected-directory inputs normalize without user changes;
- old unversioned subject parameters normalize without user changes;
- source-tree entry points invoke the source extractor shim;
- installed entry points invoke the package module;
- explicit input manifests reject traversal and unsupported versions.

Focused tests: six passed.

End-to-end fake-provider proof:

- status: `DELIVERY_COMPLETE`;
- accepted passes: 6/6;
- cards: 50;
- summaries: 4;
- delivery members: 5;
- delivery manifest present: yes;
- public polling state present: yes.
