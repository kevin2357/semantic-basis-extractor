# Slice 0 — Contract Freeze and API Review

Status: complete; awaiting Kevin/API review

## Outcome

The gap is confirmed and the additive binding-bundle v1 contract is frozen for
review. Both route implementations already construct authoritative complete
bindings before building their prepared-wave projection, so runtime publication can
reuse native facts without reverse engineering or changing provider requests.

## Route inventory

| Route | Complete binding source | Prepared wave | Required correction |
|---|---|---|---|
| Exact interactive | `action_binding()` then `prepare_action()` in exact initial-wave preparation | `build_initial_wave()` | publish ordered binding bundle before checkpoint |
| Bounded interactive | same spend binding/ledger primitives in bounded preparation | same wave builder with bounded route contract | same publication rule |
| Exact Batch | one round binding | not a six-action interactive wave | unchanged |
| Bounded Batch | one round binding | not a six-action interactive wave | unchanged |

## Consistency truth table

| Condition | Result | Provider creates / consumption |
|---|---|---:|
| Bundle and wave valid; six exact bindings agree | accept for API reservation construction | 0 at read boundary |
| Bundle absent | `binding_bundle_missing` | 0 |
| Unsupported/extra field | `unsupported_contract` | 0 |
| Bundle or binding digest changed | `digest_mismatch` | 0 |
| Wave ID/digest or route/run/profile differs | `wave_mismatch` | 0 |
| Reordered/missing/duplicate/unknown action | `member_inventory_mismatch` | 0 |
| Any full binding differs from prepared projection | `binding_mismatch` | 0 |
| Prepared revision no longer matches checkpoint | `stale_preparation_basis` | 0 |
| Snapshot incomplete/changed | `snapshot_invalid` | 0 |
| CLI output resolves inside workspace | `unsafe_output_path` | 0 |

At resume, existing complete-wave preflight independently revalidates all six
ordinary authorizations and the wave-level authorization before consuming any
authority or creating provider work.

## Decisions for API review

1. Use one root `initial-authoring-wave-binding-bundle.json`, included in the
   authoritative snapshot.
2. Keep bundle v1 additive; do not mutate prepared-wave v1.
3. Expose a snapshot-validating `run_dir` reader as the production interface.
4. Do not offer arbitrary file paths as the production reader boundary.
5. Do not synthesize missing bundles for legacy workspaces.
6. Keep ordinary non-wave `spend-authorization-requests.json` behavior unchanged.
7. Add no lifecycle/oracle states; the bundle is preparation evidence only.
8. Preserve one Batch action/reservation per round; bundle v1 is interactive only.

## API review completion condition incorporated

API approved the bundle contract subject to one necessary completion: the supported
snapshot-validating worker operation must return both public inputs atomically.
The contract now freezes
`astrowoof.initial_authoring_wave_authority_inputs.v1`, containing the exact
run-specific `prepared_wave` and `binding_bundle` plus a canonical pair digest.
The reader validates the snapshot, each document, and their join before returning
either. The CLI operation is `--initial-wave-inputs`.

## Evidence

- Proposal schema is strict Draft 2020-12 with `additionalProperties: false` at
  every object level.
- Exact and bounded representative in-memory fixtures validate against that schema
  and freeze distinct wave/bundle identities.
- Proposal/current-wave suite: 18 passed without skips in offline Linux with
  `jsonschema`; base Windows environment passed 16 with two expected optional
  schema-library skips.
- Every fact needed for an ordinary authorization binding is present without prompt
  or provider request payload.
- Exact and bounded use the same canonical spend-binding primitive and wave builder.
- Provider operations / spend: 0 / USD 0.
