# API Final Joint Campaign Review

Date: 2026-08-27
Reviewer: AstroWoof API agent
Status: **approved for the SBE release/adoption gate**

## Correction review

The two corrections requested in `API JOINT CAMPAIGN RELEASE REVIEW.md` are
implemented in API commit `1636927` and are exercised, rather than merely
described:

1. The corrected three-run/one-slot production-worker path remains distinct from
   an executed `historical_shape` adversarial trace.  The latter is driven through
   the shared materialized-state/oracle trace machinery for steps 1, 2, and 3;
   it records the blocking and continuously eligible victim identities and its
   canonical trace digest.  The joint proof binds both that digest and the
   corrected-path digest.
2. Each discharge now has closed, separate `fixture_sha256` and
   `adapter_result_sha256` fields.  A packaged fixture must carry exactly the
   catalog fixture digest; non-fixture cases must carry no fixture digest.  The
   receipt validator rejects changed fixture identities while retaining the
   adapter result independently for cases such as operator retirement and partial
   batch usage.

This preserves the intended distinction: a sealed fixture is not silently
substituted by a runtime-derived result, while a real adapter result is still
recorded as the evidence of its validation/execution.

## Reproduced evidence

Using the isolated candidate installed at
`C:/dev/github/semantic-basis-extractor/.tmp-adversarial-slice8-installed`:

```text
pytest tests/test_adversarial_joint_campaign.py \
  tests/test_adversarial_installed_vertical_slice.py::test_three_run_one_slot_campaign_proves_progress_and_historical_starvation \
  tests/test_execution_queue.py::test_expired_sbe_lease_replacement_reuses_run_capacity_and_refuses_stale_writer -q

7 passed in 45.51s
```

The regenerated API receipt
`astrowoof-api/docs/sprints/2026/08/20260825-executable-lifecycle-adversarial-simulation-sprint52/results/SLICE 8 - JOINT CAMPAIGN RECEIPT.json`
also validates against the candidate's public consumer catalog:

```text
receipt_validation=passed case_count=15
```

The receipt declares zero external-network calls, provider calls, spend, and
retained-QA access.  This review performed no provider, retained-QA, deployment,
or release action.

## Gate decision

The prior two release blockers are closed.  The SBE sprint may proceed through
its normal owner-approved version/tag/publication process; API deployment and
version adoption remain separate follow-on decisions.
