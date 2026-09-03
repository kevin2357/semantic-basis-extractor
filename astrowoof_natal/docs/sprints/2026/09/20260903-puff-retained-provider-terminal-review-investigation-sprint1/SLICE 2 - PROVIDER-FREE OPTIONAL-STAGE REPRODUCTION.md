# Slice 2 — Provider-free optional-stage reproduction

## Status

Complete. Runtime implementation has not begun. This is the review gate before
changing native behavior.

## Production-boundary reproduction

`test_optional_stage_completed_evidence_adoption_slice2.py` starts from the
existing production-shaped exact-interactive workspace and invokes the real
`closure.main()` resume command. The fixture contains:

- one ordinary-v2 polish action in `WAITING`;
- one exact durable provider response identity;
- `provider_reconciliation.last_outcome = completed`;
- the corresponding snapshot-owned reconciliation response artifact;
- one exact subject polish attempt still in `SUBMITTED`; and
- no attempt-local `openai-background-response.json` marker.

Provider transport is forbidden. The desired assertion is presently marked
`expectedFailure`: the command leaves the paid action `WAITING` instead of
reporting it, because `polish_subject()` re-enters `SpendController.callbacks()`
before any adapter joins the completed response to the stored attempt.

This is Puff's native seam. It is not an API custody or scheduling inference.
The existing ambiguity and terminal-review fences correctly prevent a second
provider create and contain the unresolved evidence.

## Route inventory

| Stage | Exact ordinary-v2 topology | Current evidence | Repair scope decision |
|---|---|---|---|
| `polish` | Stored `SUBMITTED` attempt, ordinary-v2 action, completed reconciliation artifact, `complete_json()` re-entry | Real `closure.main()` expected-failure reproducer | In scope; mandatory first repair |
| `qualitative_critic` | Stored `CRITIC_SUBMITTED` review, ordinary-v2 action, same `complete_json()` adapter | Runtime characterization reaches the exact critic spend callback and ambiguity path | In scope only through an exact stage-aware join; must not borrow polish attempt assumptions |
| `qualitative_candidate` | Stored `CANDIDATE_SUBMITTED` review, ordinary-v2 action, same `complete_json()` adapter | Runtime characterization reaches the exact candidate spend callback and ambiguity path | In scope only through an exact stage-aware join; must preserve critic-artifact predecessor binding |
| creative retry / initial authoring | Pass-attempt topology | Existing `prepare_completed_exact_attempt_for_adoption()` | Control; do not redesign |
| bounded | Separate bounded provider and lifecycle machinery | Not characterized as sharing this seam | Excluded |
| Batch | Different submission/result topology | Not characterized as sharing this seam | Excluded |

The critic/candidate tests are characterization tests, not claims that their
stored consumer records are interchangeable with polish. They prove that the
same unsafe ordering exists at the consumer boundary; the exact join must still
honor each stage's own persisted lineage.

## Frozen implementation boundary

The narrow repair should run before optional-stage consumer submission and
must:

1. locate exactly one completed ordinary-v2 action for the expected stage and
   route;
2. validate native run identity, action binding, provider response identity,
   completed reconciliation state, and response artifact identity;
3. join it to exactly one compatible stored in-progress consumer attempt;
4. materialize only the private attempt-local response marker needed by the
   existing `OpenAIResponsesProvider.complete_json()` adoption path;
5. make no provider request and grant no authority;
6. refuse or retain custody on missing, duplicate, malformed, mismatched, or
   conflicting evidence; and
7. remain idempotent when the exact marker/attempt join already exists.

Only after the existing consumer validates/parses the response and records its
normal deterministic outcome may the paid action become `REPORTED`, the v2
intent retire, and the local-work operation key be consumed.

## Focused test result

Command:

```text
python -m unittest -v astrowoof_natal.tests.test_optional_stage_completed_evidence_adoption_slice2
```

Result:

```text
Ran 3 tests in 6.009s
OK (expected failures=1)
```

- one intentional expected failure: real Puff-shaped polish resume;
- two passing topology characterizations: qualitative critic and candidate;
- zero provider calls;
- zero retained-workspace access;
- zero runtime-source changes.

The expected-failure marker is temporary test scaffolding. Implementing the
repair must turn it into an ordinary passing regression rather than silently
leaving an unexpected-success annotation.
