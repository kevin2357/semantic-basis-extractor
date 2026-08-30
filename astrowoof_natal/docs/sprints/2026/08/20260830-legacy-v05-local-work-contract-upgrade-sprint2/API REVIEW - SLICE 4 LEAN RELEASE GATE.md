# API review — Slice 4 lean release gate

## Technical decision

**GO** for owner approval of the SBE `0.4.32` package-only patch release.

The candidate satisfies the agreed lean gate:

- fresh immutable version set before candidate qualification;
- deterministic double wheel build, SHA-256
  `c45cd46ff4d7ffa98024b662c55f840e8f7cbea9682d32e97273f6e451493d6e`;
- clean installed SBE `0.4.32` with SPC `0.11.1`, `pip check`, and generic
  release smoke passing;
- all three additive fixture/schema resources and the public qualification CLI
  present in the wheel;
- two clean installed qualification runs with identical receipt SHA-256
  `2401cba4fbf18c21238b34508d28494ad23067033ecfbd072ed256455a9800b1`;
- focused legacy/v0.7/v0.8/qualification matrix: 36 passed, one optional
  `jsonschema` skip; and
- scope audit limited to qualification code/resources, public exports/CLI,
  tests, version metadata, and documentation.

The full runtime suite was intentionally not run under the already-approved
lean package-only policy. The records state that fact clearly, and the source
scope supports the classification.

## Remaining gate

Commit, tag, and publication still require explicit owner approval. This review
does not authorize deployment, retained-QA work, provider activity, or API
runtime adoption; those remain separate later decisions.
