# API Slice 1 Review — Post-Fan-In Routing Contract

Date: 2026-08-27  
Disposition: **approved for Slice 2 runtime implementation**

## Review scope

Reviewed the Slice 1 contract, its closed decision fixture, the focused mutation
coverage, Slice 0's production-shaped reproduction, and the updated sprint plan,
log, and evidence record. Re-ran the claimed focused suite in the project runtime
with `PYTHONPATH=astrowoof_natal/src`:

```text
python -m unittest \
  astrowoof_natal.tests.test_post_fan_in_authority_routing_contract_slice1 \
  astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 \
  astrowoof_natal.tests.test_post_fan_in_retry_contract_slice1 \
  astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice3 -v
```

Result: 19 passed, 1 expected optional-`jsonschema` skip. The first local rerun
without SBE's source path failed only because the generic Python environment did
not have `astrowoof_natal_authoring` installed; the project-runtime rerun above is
the relevant result.

## Findings

The contract now makes the causal boundary unambiguous:

1. An active initial-wave admission is a closed positive state set
   (`AWAITING_SPEND_AUTHORIZATION`, `AUTHORIZED`, `SUBMITTING`), not the mere
   presence of an `initial_authoring_wave` object.
2. `DETACHED` and `FAILED` are immutable historical lineage only. They remain
   available for audit/replay joins but cannot recapture command routing or v1
   aggregate authority.
3. A retrieved creative-retry completion is a provider-free local fan-in
   operation. It has no ordinary-v2 authority input and must consume an operation
   key or produce a different typed disposition.
4. Only after that fan-in is durably consumed may a later prepared ordinary retry
   advertise an exact v2 authority request. The original six-member v1 aggregate
   grant remains confined to genuine active initial-wave work.
5. Provider custody, ambiguity, and Batch retrieval remain ahead of local work;
   ordinary-v2 Batch creation stays explicitly deferred rather than inheriting
   interactive behavior.

That is the exact separation the API needs. No new API-visible lifecycle field or
command is required for this correction. API must continue to invoke only the
SBE-selected run-level command and must not infer route phase from legacy
workspace internals or a prior guard failure.

## Slice 2 conditions

Approved with these implementation checks, all already consistent with the plan:

- centralize the closed active-initial predicate so selection and aggregate-grant
  guarding cannot drift;
- preserve the existing v1 fence for active initial-wave states, including generic
  resume refusal where that remains required;
- route historical detached-wave cases through current provider/local/ordinary-v2
  facts, never through a negative-state shortcut;
- preserve the consuming-resume invariant: no same-basis quiescent publication
  while an advertised local operation retains capacity; and
- add focused regression coverage for exact interactive plus bounded parity or
  explicit non-regression, without expanding Batch ordinary-v2 behavior.

No retained-QA operation, provider call, deploy, or release is authorized by this
review.
