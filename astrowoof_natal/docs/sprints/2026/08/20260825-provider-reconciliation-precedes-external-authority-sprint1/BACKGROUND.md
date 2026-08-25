# Provider Reconciliation Precedes External Authority — Background

Date: 2026-08-25  
Status: planning; no implementation, provider activity, or retained-run mutation

## Discovery

A fresh QA two-run cohort exposed a lifecycle ordering defect after all twelve
initial authoring requests had been submitted successfully. The API authority
records showed a mixture of `reported` and `provider_created` actions for each
initial six-member wave, while the OpenAI dashboard showed completed structured
responses for all twelve requests.

For one run, native trace evidence recorded a reconciliation cycle that returned
`execution_capacity_disposition: "await_external_authority"` and deferred the
worker for `external_authority.awaiting_compatible_grant` even though that same
workspace still had three `provider_created` dependencies. No later worker claim
reconciled those retained provider results. The other run exhibited the same
class of partial reconciliation.

This is not a provider-latency, API-spend, or external-authority-v2 admission
problem. It is an ordering problem inside lifecycle selection: already-created
provider work must be observed/reconciled before the lifecycle can request or
wait for authorization for a later action.

## Desired rule

For every eligible native cycle:

1. If any retained provider-created dependency is reconciliable, select the
   retrieval-only reconciliation path.
2. Only after no provider-created dependencies remain may the lifecycle expose
   an external-authority request for a not-yet-created action.
3. If retained lineage cannot be reconciled safely, return a typed refusal or
   review disposition rather than inventing a fresh wave or silently waiting.

The rule must apply to initial-wave members and ordinary authoring routes without
changing the meaning of provider reconciliation, external-authority bindings, or
single-writer custody.

## Boundaries

- Current QA cohort runs remain frozen. This sprint neither reconciles, retries,
  repairs, authorizes, or changes them.
- Provider I/O remains outside the single-writer mutation fence.
- The API remains the authority for external spend approval. SBE only reports the
  exact next required authority after retained provider work has been exhausted.
- The result must be provider-free reproducible with fake/stub provider facts.

