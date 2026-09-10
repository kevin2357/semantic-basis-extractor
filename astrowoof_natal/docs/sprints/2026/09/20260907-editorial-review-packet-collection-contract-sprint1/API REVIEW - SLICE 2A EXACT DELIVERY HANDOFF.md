# API review — Slice 2A exact delivery handoff

## Decision

The proposed `astrowoof.terminal_delivery_command_result.v0.1` is the right
narrow bridge for API Slice 2A.  It repairs the precise fresh-delivery gap
without granting API a latest-result lookup, mutable-state inference, or any
new native lifecycle authority.

The envelope is correctly closed to eight fields and identifies one exact
same-call publication:

- successful `delivery_complete` and `exit_code=0`;
- native invocation ID, result ID, and result digest; and
- receipt ID and receipt digest.

The builder first validates the native v0.1 delivery result against its
publication receipt, rejects non-delivery outcomes, and the public reader
rebuilds the canonical envelope to prove an exact publication join.  The CLI
change is also correctly fenced to `--events-stdout-jsonl` successful-delivery
output; normal human/plain JSON output retains mutable run state.  I confirmed
there is no result-index/latest-result read, added provider work, workspace
mutation, custody transition, or editorial capture in this path.

API may consume this only as a typed structured-subprocess handoff.  It must
accept exactly one such handoff, validate it with the installed public SBE
validator, carry only the exact `result_id` into
`SbeCycleResult.sealed_terminal_result_id`, and let existing native ingress
perform its exact-result/receipt validation before editorial capture.  Missing,
multiple, conflicting, malformed, or publication-mismatched handoffs remain
fail-closed.  The handoff itself is evidence, not transition authority.

## Verification performed

- Inspected the closed JSON schema, builder, exact-publication validator,
  catalog/export surface, and the `closure.py` structured-output branch.
- Ran the focused terminal-review contract module from source:
  `15 passed`.
- Ran `git diff --check` across the changed public contract, CLI, catalog,
  exports, and focused test files: no whitespace errors.

## Required small correction before package qualification

`tests/test_terminal_review_contracts.py` currently ends with three stray,
unreachable name expressions after `unittest.main()`:

```python
read_terminal_delivery_command_result_schema,
validate_terminal_delivery_command_result,
validate_terminal_delivery_command_result_against_publication,
```

They appear to be duplicated import remnants.  They do not affect discovery
execution (the focused module passed), but please remove them rather than
release dead test-source statements.

After that cleanup, API grants technical approval to proceed through the
ordinary fresh package/release qualification gate.  The gate should retain the
existing exact-publication mutation coverage, demonstrate structured JSONL
delivery emits this handoff while legacy CLI output does not change, and repeat
the installed-wheel API-consumer qualification before API Slice 2B/2C begins.
