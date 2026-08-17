# Slice 0 Baseline

Date: 2026-08-16  
Status: complete; awaiting gate review  
Provider operations: 0  
Paid spend: `$0`

## Outcome

The two deferred routes already possess the durable native evidence needed for a
parity implementation. Exact Batch correctly fails closed in SBE 0.4.3. A real
bounded run, however, exposed a route-classification defect: it accidentally
inherits exact-interactive scheduling eligibility before a bounded reconciliation
adapter exists. Both routes can resume their known provider identity without
creating replacement work through their existing blocking route logic.

## Exact-Natal Batch inventory

One Batch round is the provider operation and may contain several paid action
members.

| Boundary | Durable native evidence | Current resume behavior |
|---|---|---|
| Prepared | Batch input JSONL, request membership, model, route, round number | May upload the input File |
| Uploaded | `input_file_id`, input bytes and membership | May create the Batch; not safe provider-pending custody yet |
| Submitted | `batch_id`, status, paid-action provider identity | Retrieves the same Batch ID |
| Terminal object | Batch status, request counts, output/error File IDs | Downloads declared files |
| Ingested | Exact `custom_id` mapping, raw Responses, per-pass metadata/QA | Continues retry/final local work |

The baseline creates a real scripted Batch round through the existing production
function, persists `batch_test`, validates a complete snapshot, and inspects the
workspace without mutation. Inspection reports:

- capacity: `unsupported_retain_capacity`;
- custody: `unsupported` with the exact paid action ID retained; and
- reason: missing supported reconciliation timing for a Batch action.

The subsequent resume performs one `retrieve_batch(batch_test)` and performs no
additional input upload or Batch creation. This freezes the known-ID/no-resubmit
property before parity changes.

Important seam: a durable input File ID without a durable Batch ID is not the same
as provider-pending paid work. The existing path can re-enter Batch creation from
that state. Slice 1 must classify it as local continuation or ambiguity based on
the actual provider boundary; it must not advertise retrieval-only capacity
release.

## Bounded-Natal interactive inventory

The bounded route persists:

- exact paid-action binding and authorization/consumption evidence;
- durable Response ID and provider kind;
- bounded stage/attempt route;
- minimized authoring packet and immutable claim authority;
- route-local provider-result artifacts;
- validation, cards, disposition, optional-stage progress, and delivery; and
- one complete workspace snapshot at interruption boundaries.

The baseline interrupts immediately after `provider_created()` records a Response
ID. The snapshot is complete, lifecycle inspection is nonmutating, and the exact
action remains visible. Contrary to the intended 0.4.3 classification, inspection
reports `continue_local_cycle` with `known_operations_pending` custody.

Cause: bounded runs use the shared
`astrowoof.semantic_closure_run.v0.9` `schema_version` and identify themselves with
`route_contract: astrowoof.bounded_natal.authoring_run.v1`. The capacity predicate
checks the shared schema, interactive service level, and stage, but not
`route_contract`. An older negative test changed `schema_version` to the bounded
contract string, which is not the shape produced by `create_bounded_run()` and
therefore did not protect the real boundary.

This is unsafe classification, not evidence that exact reconciliation already
supports bounded continuation. Slice 2 must bind route eligibility explicitly;
until the bounded adapter lands, real bounded work must fail closed rather than
entering the exact adapter.

Normal bounded resume then calls the provider's `resume()` once with the same
Response ID, creates no second submission, exhausts local authoring/validation,
and reaches `DELIVERY_COMPLETE`.

## Current state-transition summary

| Route/mechanism | Known identity | 0.4.3 inspection | Existing same-ID continuation | Sprint target |
|---|---|---|---|---|
| Exact interactive Response | Response ID | `release_until_due` or due local cycle | GET/cached evidence | Regression baseline |
| Exact Batch | Batch ID | `unsupported_retain_capacity` | Batch retrieve/download/ingest | Bounded parity |
| Bounded interactive | Response ID | **Incorrectly inherits** `continue_local_cycle`/release timing | bounded `resume()`/validate/continue | Correct route binding plus bounded parity |
| Bounded Batch | none; adapter rejects construction | fail closed | none | Remain deferred |

## Native authority versus observation

Native authority consists of `run.json`, paid-action bindings and state,
provider IDs, Batch round membership/artifacts, bounded route artifacts, and the
complete workspace snapshot. Lifecycle capacity/custody projections and execution
events are derived consumer observations. API queue slots, PostgreSQL state,
reservations, and dollar exposure remain API authority.

## Evidence

Focused command:

```text
python -m unittest astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_batch_authorization_digest_survives_persisted_resume astrowoof_natal.tests.test_bounded_lifecycle.TestBoundedLifecycle.test_interrupted_submission_reconciles_durable_id_without_resubmit astrowoof_natal.tests.test_bounded_provider
```

Result: 6 focused tests passed in 6.237 seconds. The complete repository suite
passed all 339 tests in 141.686 seconds. No network-capable transport, API key, or
provider endpoint was used.

## Slice 0 conclusion

No pipeline rewrite is warranted. Slice 1 should define a shared lifecycle meaning
with two route-specific adapters:

- one Batch-round retrieval/download/ingestion adapter; and
- one bounded interactive Response retrieval/cache/continuation adapter.

Both must preserve the baseline no-resubmission evidence and keep uploaded-only
Batch state plus bounded Batch fail closed. Route-contract discrimination must be
fixed before exposing the generalized dispatcher.
