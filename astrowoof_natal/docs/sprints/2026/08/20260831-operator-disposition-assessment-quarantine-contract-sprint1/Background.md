# Operator disposition assessment and generic quarantine — companion sprint

## Why this exists

API Sprint 66 is designing a general operator-runner quarantine path for an arbitrary stuck run. The goal is deliberately narrower than terminalization: remove the run from ordinary scheduling and release only local API capacity/lease resources that can be proven safe to release, while preserving every potentially live provider, spend, workspace, checkpoint, receipt, and native-custody obligation.

The API cannot infer that safety from action records, receipts, a status label, or a raw workspace snapshot. It needs a versioned, read-only SBE assessment of the exact native checkpoint and its custody situation.

This sprint must create that public SBE boundary. It must not itself mutate any retained run, invoke a provider, release spend, deploy a worker, or create a release merely because this background document exists.

## Required public contract

Provide a closed, versioned artifact and root-level Python reader/validator:

`astrowoof.operator_disposition_assessment.v1`

For one exact native run/checkpoint, the assessment must bind at least:

- native run ID, route, lifecycle revision, snapshot/checkpoint identity, compatibility identity, and digest;
- one closed `native_custody_class`:
  `provider_free_quiescent`, `provider_pending_known_identity`,
  `completed_unadopted`, `native_local_work_ready`,
  `providerless_authority`, `submission_ambiguous`, `sealed_terminal`, or
  `unsupported_or_inconsistent`;
- explicit provider/local/authority assertions and bounded counts;
- only safe provider identity/status detail needed for diagnosis—no prompts, subject data, provider payloads, or secrets;
- a closed local-quarantine posture: `permitted`, `prohibited`, or `native_prior_action_required`;
- ordered supported next actions and a typed reason;
- canonical digest/integrity fields plus fixtures and provider-free qualification tests.

The assessment must be snapshot-bound. API needs to reject it if the exact bound native identity has changed.

## Intended semantics

1. It is inspection only: no provider I/O and no retained-workspace mutation.
2. `permitted` is native-only evidence that an ordinary local SBE authoring
   worker need not remain scheduled. API separately proves its exact job fence,
   lease/capacity ownership, and resource disposition under its writer lock. It
   never means API may cancel, mutate, or forget native/provider/spend custody.
3. Pending, ambiguous, or providerless-authority custody must remain preserved for a later named reconciliation/retirement path.
4. `completed_unadopted` must point to existing native fan-in/adoption semantics where valid; it is not permission to synthesize completion.
5. `sealed_terminal` supports ordinary terminal ingestion, not arbitrary API repair.
6. Unknown/inconsistent evidence has posture `prohibited`: it cannot authorize
   the real `quarantine_run` operation or assessment-based local capacity
   release. API may still record a request, refusal, or operator-audit event,
   but that diagnostic/audit record is not completed quarantine and must not
   manufacture native recovery or resource authority.
7. Leaving quarantine must require a later named action and fresh assessment; it must never happen automatically after a restart.

## Suggested slices

1. **Inventory and boundary freeze.** Inventory existing inspection/readers, lifecycle ownership, custody vocabulary, and cross-route cases. Pause for API review.
2. **Schema and reader.** Define the v1 schema, canonical digest, root-level builder/reader/validator, fixtures, and closed vocabularies. Pause for API review.
3. **Projection and qualification.** Implement custody/posture projection and provider-free tests for every class, especially rejected/ambiguous and completed-unadopted cases.
4. **Cross-route and ordering review.** Verify all relevant initial/retry/reconciliation/local/terminal routes. Pause for API review before release work.
5. **Release readiness.** Installed-wheel qualification, public handoff notes, and a release recommendation.

## Coordination with API Sprint 66

API may build non-semantic scaffolding in parallel: the `operator_quarantined` job state, audit/persistence shapes, diagnostics, and test doubles. API must not finalize assessment admission, custody interpretation, resource-release rules, or invoke a production quarantine command until this public contract is frozen and then released/consumed.

The intended API order, once an assessment is admitted, is: acquire exact job fence; persist the exact assessment/request; move the job to `operator_quarantined`; release only the target's non-active local lease/capacity; retain all provider/spend/workspace/checkpoint/artifact/receipt custody. A currently active ordinary worker lease must fail closed or require explicit policy—never be silently revoked.
