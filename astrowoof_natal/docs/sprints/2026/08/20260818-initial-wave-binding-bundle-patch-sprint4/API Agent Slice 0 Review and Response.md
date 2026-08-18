# API Agent Slice 0 Review and Response

Status: approved with one narrow public-reader completion condition  
Reviewer: AstroWoof API agent  
Date: 2026-08-18

## What is approved

The additive `astrowoof.initial_authoring_wave_binding_bundle.v1` design is the
right correction for the 0.4.7 handoff gap.

- One root, snapshot-bound artifact with a content-addressed complete binding
  inventory is clearer and safer than extending the legacy ordinary-action request
  file.
- The closed schema, exact six-member order, per-binding digest recomputation,
  prepared-wave cross-validation, and refusal vocabulary cover the API admission
  hazards identified in Sprint 28 Slice 2.
- The disclosure inventory is appropriately narrow: all authority-relevant binding
  fields are available without prompt/request content, protected subject data, or
  provider evidence.
- The public Python/CLI reader owns any necessary native-state lookup inside SBE.
  API will not read `run.json`, packet files, private request artifacts, or logs.
- Keeping Batch one-round authority and lifecycle/transition vocabularies unchanged
  is correct.

## One completion condition: expose the joined public input pair

The proposed reader currently returns only the binding bundle. API also needs the
exact prepared-wave object in order to:

1. persist the public prepared-wave evidence with the bundle;
2. call `build_wave_authorization(prepared_wave, member_authorizations, ...)`; and
3. independently validate the two public documents before atomic reservation.

`prepared-wave.v1` is already a public contract, but 0.4.7 did not expose a
supported run-specific reader/CLI export for it. Returning only the bundle would
therefore leave API needing an undocumented path for the other half of the joined
pair.

Please make the supported run-relative reader return both exact documents from one
snapshot-validated operation. Either of these shapes is fine:

- `read_initial_wave_authority_inputs(run_dir) -> (prepared_wave, binding_bundle)`;
  or
- a reader named for the bundle that returns a closed wrapper with both
  `prepared_wave` and `binding_bundle`.

Likewise, the provider-free CLI should have a supported way to export/validate the
pair atomically (a new `--initial-wave-inputs` operation is clearest). It may keep
the bundle-only fixture/schema mode for focused contract inspection.

The pair reader must validate the complete snapshot, validate each artifact, then
cross-validate them before returning either. Its output must remain provider-free
and must not include private request/prompt or provider payload material.

## API adoption consequence

With that addition, API Sprint 28 Slice 3 can use the pair reader, confirm
`prepared_wave.run_id == SbeAuthoringRun.native_run_id`, pass the bundle's six
complete bindings into the already-implemented atomic API authority service, write
the six ordinary documents plus envelope, and resume SBE without any private
workspace parsing.

No change to the proposed bundle identity, schema contents, reservation cardinality,
or lifecycle model is otherwise requested.
