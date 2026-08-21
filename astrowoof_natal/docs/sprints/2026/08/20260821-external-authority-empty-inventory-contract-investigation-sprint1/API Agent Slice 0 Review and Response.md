# API Agent Slice 0 Review and Response

Date: 2026-08-21
Disposition: approved to proceed
API review commit: `4b6a60d`

## Review conclusions

- The retained rejection does not prove an empty action inventory because its exact
  rejected lifecycle document was not retained.
- Normal exact and bounded inspection paths both produce coherent six-action
  external-authority requests.
- SBE lifecycle v0.5 has two proven contract gaps for
  `await_external_authority`: wrong `reason_code` and non-null `not_before` are
  currently accepted natively even though the API correctly refuses them.
- All five external-authority branch predicates should become explicit native
  invariants with structured, redacted predicate diagnostics.
- No API changes are required from this review.

## Implementation notes accepted by SBE

1. Slice 0's reuse of another test fixture remains test-only. Installed-wheel
   qualification will construct or consume packaged/public fixtures and will not
   import another source-tree test class.
2. Branch invariants are conditional on the command. A typed refusal with
   `command=none` continues to require an empty action inventory;
   `await_external_authority` requires a nonempty exact request inventory.

