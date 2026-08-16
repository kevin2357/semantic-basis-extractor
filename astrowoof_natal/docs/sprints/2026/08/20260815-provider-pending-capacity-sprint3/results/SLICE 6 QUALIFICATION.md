# Slice 6: Cross-Platform and Parallel Qualification

Status: qualification complete; pending Kevin's Slice 6 gate review.

## Native parallel cohort

Three independent exact-interactive workspaces were materialized with durable
provider IDs, authorizations, consumption evidence, reconciliation timing, and
complete snapshots. Aster and Bramble ran bounded pending cycles concurrently.
Both returned `detached_provider_pending` and fresh `release_until_due`
checkpoints. Clover remained independently inspectable and immediately runnable.

The cohort proves SBE has no resident-process or cross-run native dependency:
pending workspaces preserve their exact provider IDs and consumer-authority
references while unrelated native work remains runnable. It does not claim to
exercise the API's PostgreSQL capacity allocator; that remains the companion API
gate.

## Installed-wheel qualification

A local 0.4.2 qualification wheel was built from the Slice 6 tree and installed
with exact SPC 0.11.0 into clean environments:

- Windows Python 3.11.9: `pip check`, installed lifecycle smoke, and installed CLI
  bounded-mode discovery passed;
- Linux `python:3.11-slim`: clean install, `pip check`, installed lifecycle smoke,
  and installed CLI bounded-mode discovery passed.

The wheel contains `py.typed`, the lifecycle contract schema, reconciliation
policy/fixture resources, and 88 total members. Two builds using the same frozen
`SOURCE_DATE_EPOCH` were byte-identical:

```text
SHA-256 2db4602132531c5842aca649ce2bdc453cb0923e821ee6a4d08f98da770ab1c5
```

This is qualification evidence only, not a release artifact or published hash.

## Regression gate

The complete repository suite passed all 339 tests in 158.959 seconds. The added
parallel-cohort test passed independently in 0.292 seconds.

Provider operations: 0. Paid spend: `$0`. API key used: no. No version bump, tag,
publication, or API capacity-allocation claim occurred.
