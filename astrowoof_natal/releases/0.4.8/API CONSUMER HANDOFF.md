# SBE 0.4.8 API Consumer Handoff

At an initial-wave authorization boundary, use the supported public reader:

```python
from astrowoof_natal_authoring import read_initial_wave_authority_inputs

authority_inputs = read_initial_wave_authority_inputs(run_dir)
```

The returned `astrowoof.initial_authoring_wave_authority_inputs.v1` document is
snapshot-validated and contains the exact prepared wave plus its complete ordered
six-binding bundle. Persist the wrapper, both nested documents, and the wrapper
digest before reserving authority.

For each ordered member, copy `binding_bundle.ordered_members[i].binding` exactly
into one `astrowoof.provider_spend_authorization.v0.1` document. Atomically reserve
the full six-member set, construct the wave envelope from the returned prepared
wave, and resume only with the complete ordered authority set.

Both `prepared_wave.run_id` and `binding_bundle.run_id` identify
`SbeAuthoringRun.native_run_id`, not API `GenerationRun.id`.

The bundle is preparation evidence, not authorization or scheduling authority.
Lifecycle inspection/result/receipt remain authoritative for scheduling and
native progression. API continues to own cross-run reservations, quotas, circuit
breakers, entitlements, billing authority, and public product state.

See the detailed
[Initial Authoring Wave Consumer Handoff](../../docs/post_extraction_authoring/Initial%20Authoring%20Wave%20Consumer%20Handoff.md).
