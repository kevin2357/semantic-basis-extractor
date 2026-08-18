# AstroWoof Natal Authoring 0.4.8 Release

Status: release candidate; publication pending

## Summary

SBE 0.4.8 closes the public authority boundary introduced with Initial Authoring
Wave v1. A supported snapshot-validating reader and CLI now return the exact
prepared wave together with a closed, content-addressed bundle containing all six
complete ordered spend bindings.

The API can therefore reserve and authorize the six-member interactive wave
without reading private `run.json`, packet files, logs, or undocumented native
artifacts. Exact and bounded interactive routes use the same public operation.

This additive patch does not change lifecycle states, transition-oracle
vocabulary, editorial topology, prompts, provider transport, Batch cardinality,
or API/SBE authority ownership.

## Public additions

- `read_initial_wave_authority_inputs(run_dir)`;
- `validate_initial_wave_authority_inputs(document)`;
- `build_initial_wave_authority_inputs(prepared_wave, binding_bundle)`;
- `astrowoof-initial-wave-contract --initial-wave-inputs --run-dir ...`;
- `astrowoof.initial_authoring_wave_binding_bundle.v1`; and
- `astrowoof.initial_authoring_wave_authority_inputs.v1`.

The exact artifact identity and post-publication verification will be recorded in
`release-manifest.json` after the versioned source boundary is rebuilt.
