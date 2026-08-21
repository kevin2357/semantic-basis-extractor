# Slice 2 — Native Validator and Classification Hardening

Date: 2026-08-21
Status: complete and approved

## Outcome

Lifecycle inspection v0.5 now enforces the approved external-authority command
conditionals in both its packaged JSON Schema and Python semantic validator.

No lifecycle version, public state, command, authority, provider behavior, or API
database contract changed.

## `await_external_authority`

Native validation now requires:

- ineligible branch;
- exact branch and capacity reason `spend_authorization_required`;
- capacity disposition `await_external_authority`;
- no locally ready work;
- null capacity and branch due times;
- nonempty ordered action IDs;
- a request object; and
- no refusal object.

Existing request validation and semantic joins continue to require 1–32 unique
actions, complete bindings/digests, exact run/observation identity, and exact branch
and request ordering.

## Typed refusal

When a refusal object exists, native validation now requires:

- command `none`;
- ineligible branch;
- reason `native_review_or_ambiguity`;
- empty action IDs and null branch due time;
- capacity `retain_for_review` with reason `native_review_required`;
- no locally ready work and null capacity due time; and
- no request object.

Thus empty action IDs remain valid for truthful non-runnable refusal and invalid for
external-authority admission.

## Failure behavior

Contradictory constructed lifecycle documents raise a deterministic validation
error containing a sorted set of closed failed-predicate names. They are not
recast as native refusals and cannot escape as public inspection bytes.

Request construction from an inadmissible but truthfully classifiable native state
continues to produce the existing typed refusal before final document validation.

## Schema parity

Conditional `if`/`then` rules were added only to `lifecycleInspectionV05`; the
shared v0.4 branch schema was not retroactively tightened. Cross-object equality
remains enforced semantically.

The schema mutation test covers both command tables. It is present but skipped by
the lean host interpreter when `jsonschema` is unavailable; JSON syntax and Python
compilation were separately verified. Installed-wheel/Linux qualification remains
a later sprint gate.

## Tests

- Contract/investigation/lifecycle group: 58 passed, 5 skipped.
- Initial-wave lineage fence: 7 passed.
- Provider-pending capacity: 29 passed.
- Total completed focused tests: 94 passed, 5 skipped.
- Python compilation: passed.
- Packaged lifecycle JSON parsing: passed.
- `git diff --check`: passed.

Provider calls: 0. Spend: USD 0. Retained QA workspace access: none.

## Gate

PASS. Every approved invalid command conditional is refused natively before public
return or provider-capable execution. Slice 3 structured observability remains
separate.
