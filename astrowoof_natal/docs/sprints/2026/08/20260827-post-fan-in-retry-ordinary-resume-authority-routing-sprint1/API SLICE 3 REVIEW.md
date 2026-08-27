# API Slice 3 Review — Composed Post-Fan-In Runtime

Date: 2026-08-27  
Disposition: **approved for Slice 4, with an explicit fixture requirement**

## Runtime review

Slice 3 proves the required incident successor at the real public SBE boundary:

```text
not-due provider custody
  -> due retrieval-only reconciliation
  -> durable completed evidence
  -> one provider-free local fan-in operation
  -> consuming ordinary_resume
  -> fresh exact ordinary v2 request/grant/intent
  -> one provider detach
  -> exact replay with no second create
```

Most importantly, retained `DETACHED` initial-wave lineage no longer captures that
ordinary-resume route, while an actually active initial wave still requires the v1
aggregate grant. That is the right narrowly scoped correction.

I independently reran the focused Slice 1/3 contract and routing suite in the SBE
source runtime (`PYTHONPATH=astrowoof_natal/src`): 19 passed with one expected
optional-`jsonschema` skip. The broader 44-test composed qualification is recorded
in this Slice's evidence; its provider transport is scripted and it reports zero
external network/spend/retained-QA activity.

## Slice 4 fixture requirement

Yes: this is the right point to make the post-fan-in fixture a concrete remaining
deliverable of **this** sprint. Slice 3 is a convincing internal composed proof,
but it is not yet the reusable public, installed-wheel fixture required for the
API's joined one-slot qualification.

Slice 4's existing plan already calls for a sanitized SBE fixture/public
qualification component. Please make its contract explicit:

1. It must be public and provider-free, with a supported reader/validator and a
   stable receipt/digest identity.
2. It must materialize both the historical incident state and the corrected
   successor, including the exact evidence above: provider custody, retrieval,
   local fan-in, consumed operation, ordinary v2 authority, one dispatch, and
   replay non-duplication.
3. It must expose only public lifecycle/command/evidence projections—never raw
   `run.json`, private selectors, prompts, provider payloads, or retained QA data.
4. Its endpoint must be **delivery-ready**, not claim reader delivery. In other
   words, it must prove the corrected successor reaches the next supported
   non-local terminal/delivery disposition or a provider-pending custody state
   whose remaining work is explicitly modeled. Full reader delivery is an API
   persistence/delivery assertion and belongs in Sprint 54's joined fixture.
5. The API joined campaign should consume that fixture against the exact installed
   SBE wheel, add real persistence/scheduler/one-slot fairness, and then assert
   the API-owned terminal/delivery outcome. That lets us do one candidate release
   and one QA deployment rather than deploy an intermediate SBE wheel merely to
   continue provider-free qualification.

This is an additive qualification surface, not a lifecycle schema or authority
change. It should be part of Slice 4/5 acceptance before release, not deferred to
a subsequent SBE patch sprint.

No retained-cohort mutation, provider activity, deployment, or release is
authorized by this review.
