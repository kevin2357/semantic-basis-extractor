# API Slice 4 Review

## Decision

The installed-wheel qualification design is approved, with one small correction
required before its final receipt/rebuild and any release decision.

The candidate evidence is otherwise strong: the wheel inventory contains the
fixture JSON, both schemas, and the console entry point; the installed command
ran outside the source checkout; and all reported provider/network/spend counters
are zero.

## Required correction: identify both packaged schemas truthfully

The receipt field named `fixture_schema_sha256` currently hashes
`duplicate-submission-fence-qualification.v1.schema.json`, not
`duplicate-submission-fence-fixtures.v1.schema.json`.

That leaves the fixture-bundle schema present only as an inventory assertion,
despite the receipt field's name implying it binds that schema. Please replace
the ambiguous single field with two closed receipt fields:

```text
fixture_bundle_schema_sha256
qualification_schema_sha256
```

The provider-free installed command must read and hash both packaged resources;
the strict Python validator, JSON Schema, source tests, and installed-wheel
receipt should require both exact values. This is an additive pre-release
correction—there is no compatibility concern for the unpublished candidate.

## Remaining release gate

After that correction, rebuild from the final source with a fresh immutable
package version. The present candidate correctly records version `0.4.29`, which
is already published and therefore must not be the released artifact version.

No API consumer work, retained-QA recovery, provider activity, or spend is
authorized by this review.

## Correction re-review — approved

The correction is incorporated correctly. The receipt now has separate,
strictly validated identities for both:

- `fixture_bundle_schema_sha256`; and
- `qualification_schema_sha256`.

The rebuilt isolated-wheel receipt binds both values, and the focused Slice 4
source test passes (three tests, one expected optional-schema skip). This clears
the Slice 4 technical review gate. The remaining release requirement is only to
build and publish from the final source under a new immutable version rather
than the already-published `0.4.29` candidate version.
