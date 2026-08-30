# Slice 3 — packaged qualification contract

## Classification

Additive qualification-only package surface. It is not lifecycle authority and
does not change production inspection, selection, custody, provider, or mutation
behavior.

## Public resources

1. `legacy-v05-local-work-upgrade-fixture.v1.json`
   - closed static scenario definitions and expected outcomes;
   - no workspace path or native private state;
   - cells: consistent/not-due, consistent/due, lineage-conflict-with-custody,
     and lineage-conflict-after-custody.
2. `legacy-v05-local-work-upgrade-bundle.v1.schema.json`
   - validates a dynamically generated provider-free bundle containing the
     complete public v0.5/v0.7/v0.8 documents for the consistent scenarios and
     the packaged public v0.8 conflict fixtures;
   - binds every document to its scenario and stable shared identities.
3. `legacy-v05-local-work-upgrade-qualification.v1.schema.json`
   - validates the concise reproducible installed qualification receipt.

## Public Python/CLI surface

- fixture, bundle-schema, and receipt-schema readers;
- strict Python bundle and receipt validators which do not depend on optional
  `jsonschema`;
- a bundle builder using SBE-owned provider-free workspace machinery and public
  lifecycle readers/validators;
- a qualification runner; and
- `astrowoof-legacy-local-work-upgrade-qa` with mutually exclusive
  `--fixture`, `--bundle`, `--bundle-schema`, and `--schema` output modes.

The command accepts no run directory, provider credential/identity, request,
grant, authorization, production input, or retained-workspace coordinate.

## Dynamic bundle versus reproducible receipt

Complete public lifecycle documents legitimately carry the temporary logical
workspace root and snapshot identity. The dynamic bundle therefore remains a
per-invocation public validation artifact and is not required to be byte-identical
across work directories.

The concise receipt excludes those ephemeral values. It records only:

- package name/version;
- fixture and both schema SHA-256 values;
- scenario names and declared selected outcomes;
- boolean stable-identity/document-validation assertions;
- provider create/retrieve/network/spend counts, all zero;
- privacy assertions; and
- its canonical receipt SHA-256.

Two clean installed runs must produce an identical receipt.

## Validator authority

The bundle validator delegates each full document to the released public v0.5,
v0.7, or v0.8 validator. It independently validates only:

- exact bundle shape and digest;
- stable run/revision/snapshot/logical-root equality across versions;
- fixture/scenario identity;
- the sole legacy dependency predicate;
- expected selected command/disposition/eligibility;
- exact local-operation source actions and retained custody IDs; and
- zero-I/O/privacy declarations.

It does not reproduce SBE action/binding/provider composition rules.

## Mutation matrix

Reject after recomputing outer digests when any of the following changes:

- run, revision, snapshot, root, route, or provider identity join;
- legacy dependency count/completed-evidence predicate;
- v0.7/v0.8 selected command or local operation;
- due subset/not-before/custody inventory;
- conflict classification or forward-dispatch assertion;
- fixture/schema/receipt hash;
- I/O or privacy assertion; or
- any missing/extra field.
