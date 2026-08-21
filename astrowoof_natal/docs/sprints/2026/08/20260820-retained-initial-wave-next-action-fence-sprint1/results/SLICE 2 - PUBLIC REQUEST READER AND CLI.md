# Slice 2 — Public Request Reader and CLI

Date: 2026-08-20
Status: complete

## Supported Python surface

The package root now exports:

- `build_external_authority_request(...)`;
- `validate_external_authority_request(...)`;
- `read_external_authority_request(run_dir)`; and
- `read_external_authority_schema()`.

`read_external_authority_request()` is the supported consumer boundary. It validates
the complete stable-path workspace snapshot, reads the exact native state, joins a
stored initial wave to the existing public binding bundle, constructs the closed
request, and then revalidates the snapshot and observation before returning. A
coherent writer update during the read fails closed rather than returning mixed
checkpoint evidence.

A stored initial-wave artifact is not sufficient by itself. The reader publishes an
`initial_wave_admission` request only when the stored wave is exactly
`AWAITING_SPEND_AUTHORIZATION` and each of its six ordered IDs resolves exactly once
in the durable ledger to a `PREPARED`, providerless, unconsumed action whose complete
binding equals the public binding-bundle member. Authorized, submitting,
provider-recorded, pending, reported, completed, missing, duplicated, or
binding-mismatched members return typed `request_unavailable` and no create-capable
request.

The request observation time is the snapshot-bound native `updated_at` (falling back
to `created_at` for compatible historical state), not reader wall-clock time.
Repeated reads of an unchanged checkpoint therefore return the same request digest.

For an initial wave, semantic member order is preserved. For an ordinary prepared
set, actions are ordered lexically by `action_id`. The public artifact contains only
complete spend bindings and route/wave identities; it excludes prompts, provider
payloads and responses, credentials, and protected subject fields.

Tests use the production-shaped revision relationship: actions are bound at their
preparation revision and inspected from the later persisted checkpoint. The action
revision may precede, but may never exceed, the request observation revision.

## Supported CLI

```text
astrowoof-external-authority --run-dir RUN_DIR [--output OUTSIDE_RUN]
astrowoof-external-authority --validate-request REQUEST.json
astrowoof-external-authority --schema
```

The run reader and validation operations are provider-free and perform no native
mutation. An output path equal to or beneath `RUN_DIR` is refused. Stdout always
contains the same validated JSON written to an allowed output path.

## Refusal behavior

The reader fails closed for:

- missing or changed snapshot members;
- restoration under the wrong logical absolute path;
- a run changing coherently during the read;
- missing or mismatched wave/binding-bundle evidence;
- empty ordinary prepared inventory;
- incomplete or stale public bindings;
- invalid ordering, membership, digest, or observation time; and
- unsupported/extra contract fields during standalone validation.

No provider call, authorization mutation, reservation decision, or lifecycle branch
selection occurs in this Slice 2 surface. Lifecycle v0.5 integration remains Slice 3
work after the approved public reader boundary.

## Qualification

- Focused public/request/legacy-wave suite: 36 tests passed on the host lean runtime;
  four proposal-only Draft 2020-12 tests skipped because `jsonschema` is absent.
- Slice 1 Linux QA schema suite previously passed all Draft 2020-12 cells.
- A wheel built offline with `--no-build-isolation` and installed into an isolated
  Python 3.11 environment.
- Installed `astrowoof-external-authority --schema` loaded the packaged v1 schema.
- Candidate wheel SHA-256 during this slice:
  `26edc7ec6118bec38ab8374cd34326075cae87db158d2ad660d76b9666839fc5`.
- Provider/network calls: 0. Spend: USD 0.
- Temporary qualification environments were removed after the check.
