# API Slice 2 Review — Packaged Prepared-Polish Qualification

## Decision

**Conditionally approved.** The provider-free command, receipt validator, and
neighboring custody/terminal matrix establish the right public consumer surface.
Please make the small packaged-schema correction below before beginning Slice 3
installed-wheel/release qualification.

## Confirmed

- `astrowoof-polish-authority-handoff-qa` executes the production lifecycle and
  temporal-reader boundaries from a temporary workspace, not a parallel request
  builder.
- Its positive case emits exactly one ordinary-v2 action (`paid_...`) and proves
  the branch is `await_external_authority`.
- The no-polish, mismatched subject/action, stale, unrelated stage, Batch, and
  sealed-terminal cases all remain no-request/non-dispatching.
- The receipt is integrity protected, declares provider-free / zero-network /
  zero-create / zero-spend behavior, and rejects a rehashed semantic mutation in
  the Python public validator.
- The public console entry point is registered in the package metadata.

I ran locally with `PYTHONPATH=astrowoof_natal/src`:

```text
python -m unittest \
  astrowoof_natal.tests.test_polish_authority_handoff_qa \
  astrowoof_natal.tests.test_polish_authority_handoff_slice0 \
  astrowoof_natal.tests.test_terminal_dominance_slice1 -v

Ran 12 tests in 0.666s — OK
```

## Required small correction

The Python `validate_polish_authority_handoff_qualification()` function correctly
freezes the exact `checks` keys and `negative_cases` values. The packaged JSON
Schema, however, permits any four true check names and any six unique string
negative cases. Tighten the schema to declare those exact names/values too (for
example, fixed object properties plus `required` for `checks`, and an exact
array shape for `negative_cases`).

That makes the stated *closed packaged schema* true for a schema-only consumer,
instead of relying on a consumer also invoking the Python validator. It is
additive contract hardening only; it does not change the native lifecycle or
broaden the prepared-polish exception.

## Slice 3 gate after correction

Once the schema and its direct negative validation test are updated, the
installed-wheel qualification may proceed. API can consume the receipt as a
release-pair qualification artifact; it still must obtain real continuation
authority exclusively from the native ordinary-v2 request at runtime.
