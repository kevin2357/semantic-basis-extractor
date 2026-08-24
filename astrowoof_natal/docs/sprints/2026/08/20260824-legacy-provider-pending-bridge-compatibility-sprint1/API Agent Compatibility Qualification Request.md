# API Agent Compatibility Qualification Request — Legacy Provider-Pending Bridge

Date: 2026-08-24
Status: request only; no implementation or provider activity

## Target historical shape

The API has one fresh QA run which created exactly one six-member initial
authoring wave under the v0.5-era lifecycle boundary, then failed before a
supported reconciliation claim could run:

- API run: `ce525bea-fc47-4666-93ff-f45e18dd553b`.
- SBE job: `b469adb8-281a-4153-a7b0-dc3b80f0390d`.
- Original authoring profile: `astrowoof.qa.sbe0415-external-authority.v2`.
- Latest native checkpoint status: `WAITING_FOR_RESPONSE`.
- Six provider operation identities exist; no result was durably reconciled.
- The job failed after two old contract attempts. It is not an exhausted retry
  or existing continuation-window recovery shape.

Current API worker code correctly isolates such pre-v1-initial-wave retained
workspaces rather than silently treating them as current temporal v0.6 state.

## Requested SBE qualification

Please determine, provider-free and against a frozen v0.5-like fixture, whether
the released SBE `0.4.16` public command below is a supported compatibility
operation:

```text
astrowoof-authoring-lifecycle --run-dir RUN \
  --resume --provider-reconciliation-cycle \
  --observed-at <canonical UTC instant>
```

The fixture should have known initial provider identities but no completed
provider output. The provider adapter must be a fake that proves:

1. no create/submit/retry operation can occur;
2. only bounded GET/retrieval is attempted;
3. no spend authorization, initial-wave authorization, external-authority
   request, or external-authority grant is accepted by this command;
4. its output is a sealed, valid public reconciliation result that the current
   API can ingest; and
5. unchanged/repeated provider-pending evidence retains a safe typed outcome.

## API bridge contingent on success

If the qualification passes, API Sprint 37 will add a dry-run-first audited
operator record for this exact historical target. It grants one worker claim
whose only permitted command is the reconciliation command above. It does not
reprofile the run, create authorization, infer v0.6 evidence, or mutate
provider state. Any new v0.6 temporal observation is persisted only after the
native command produces it.

If the qualification does not pass, please identify the smallest public SBE
compatibility addition required. We will not use private workspace mutation or
an ordinary resume as a substitute.

## Decision requested

Please respond with one of:

1. **Supported now:** fixture/command evidence sufficient for API bridge work.
2. **Supported with a narrow SBE patch:** describe the public contract and
fixture required.
3. **Unsupported/review-only:** explain the conflicting frozen invariants so
the API can terminally retain Aster without inventing recovery authority.
