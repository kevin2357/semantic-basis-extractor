# Slice 2 — Public Joined Authority Inputs

Status: complete; AstroWoof API approved

## Outcome

The supported public boundary now returns the exact run-specific prepared wave and
complete binding bundle together from one snapshot-validating operation:

```python
read_initial_wave_authority_inputs(run_dir)
```

Its return contract is
`astrowoof.initial_authoring_wave_authority_inputs.v1`. SBE validates the complete
workspace snapshot, prepared wave, binding bundle, every binding/action digest, the
ordered join, and the wrapper digest before returning either document.

The provider-free CLI equivalent is:

```text
astrowoof-initial-wave-contract --initial-wave-inputs --run-dir <run>
```

`--output` is supported only outside the inspected run workspace.

## Packaged public surface

- Root builders/validators/readers for bundle and joined authority inputs.
- Strict bundle and authority-inputs JSON Schemas.
- Canonical exact and bounded binding-bundle fixtures.
- Contract-catalog and installed lifecycle-smoke enumeration.
- Updated Initial Authoring Wave and Spend Authorization consumer handoffs.
- Installed qualification driver for exact and bounded run-specific reader/CLI.

## Safety behavior

- Snapshot invalid, artifact absent, unsupported/extra fields, changed digest,
  cross-wave mismatch, or unsafe output fails closed.
- The reader performs SBE-owned native lookup internally; API reads no `run.json`,
  request packet, prompt file, legacy request projection, or logs.
- Returned content contains binding identity/commercial limits but no prompt,
  request body, output schema, subject data, protected provenance, provider identity,
  or API reservation identity.
- The pair is preparation evidence only. It grants no spend or provider authority.

## Tests and qualification

- Public/reader/CLI, bundle, release-contract, native-transition, and bounded
  contract suite: 61 passed in 3.864 seconds.
- Strict bundle and joined-schema validation with resolved references: pass in
  offline Linux `jsonschema` environment.
- Installed Windows candidate: `pip check`, root exports, both new schemas, exact
  fixture, CLI schema export, lifecycle smoke, and exact/bounded run-specific
  reader/CLI round trips passed.
- Qualification-only 0.4.7-named wheel: 828,375 bytes, 118 entries, 71 resources,
  no tests/bytecode; SHA-256
  `15068ee064654226a7c05a37cddce18cc0e0ecb28c27b54e7824b1e8f46fd78a`.
  It is not publishable because 0.4.7 is immutable.
- Provider operations / spend: 0 / USD 0.

## API review request

Please confirm API Slice 3 can:

1. call the joined reader/CLI without private workspace parsing;
2. persist both returned documents and wrapper digest;
3. bind both native run IDs to `SbeAuthoringRun.native_run_id`;
4. atomically reserve the six ordered bindings;
5. create the six ordinary authorization documents by exact binding copy; and
6. call `build_wave_authorization(prepared_wave, documents, ...)`.

API approved all six points without requesting a contract change.
