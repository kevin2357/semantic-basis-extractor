# Provider Reconciliation Precedes External Authority — Evidence

## Planning evidence

- Fresh QA cohort contained two six-member initial waves.
- OpenAI dashboard observation indicated all twelve submitted structured responses
  were available.
- API authoritative records retained mixed `reported` and `provider_created`
  action states for both waves.
- SBE trace evidence recorded a defer to external-authority wait with remaining
  provider-created dependencies.

These observations establish the selector-ordering question only. They are not a
license to mutate the cohort or to treat dashboard observations as lifecycle
authority.

## SBE planning assessment

- Current selector evidence indicates due reconciliation already precedes prepared
  authority.
- Candidate defect: prepared authority precedes scheduled/not-due provider custody
  and completed-provider evidence requiring local fan-in.
- This remains a hypothesis until Slice 0 reproduces it through public lifecycle
  and temporal inspection.
- Planning changed no runtime, schema, provider, spend, or retained workspace.

## Next-release compatibility baseline

- Project dependency: `semantic-projection-core==0.11.1`.
- Bounded admission runtime pin: SPC 0.11.1.
- Next release manifest requirement: exact SPC 0.11.1.
- Published 0.4.21 manifest remains unchanged and accurately records SPC 0.11.0.

## API plan approval

- Review: `API AGENT PLAN REVIEW.md`.
- Verdict: approved to begin provider-free Slice 0.
- Existing lifecycle v0.5/temporal v0.6 are the preferred compatibility target.
- No API code/schema change is expected if corrected inspection preserves existing
  command and `not_before` semantics.
- Runtime implementation remains unstarted pending Slice 0 API review.

## Slice 0 evidence

- Result: `results/SLICE 0 - PUBLIC SELECTOR AUDIT AND PRECEDENCE CONTRACT.md`.
- Reproducer:
  `astrowoof_natal/tests/test_provider_reconciliation_precedes_authority_slice0.py`.
- Focused result: 4 tests passed.
- Routes: exact Natal interactive and bounded Natal interactive.
- Public readers: lifecycle inspection v0.5 and temporal lifecycle v0.6.
- Observed current defect:
  - due provider custody + prepared → reconciliation (correct baseline);
  - not-due provider custody + prepared → authority (incorrect);
  - completed provider evidence + prepared → authority (incorrect).
- Secondary symptom: time-only not-due → due currently changes the v0.6 basis
  because the not-due branch embeds authority inventory and the due branch does not.
- Authoritative workspace hashes remained unchanged across every inspection.
- Provider POST/create/submit/retry/GET calls: 0.
- Authorization/grant consumption: 0.
- Frozen QA cohort access/mutation: 0.
- Source/schema/runtime changes: none.

## Slice 1 evidence

- API approval: `API AGENT SLICE 0 REVIEW.md`.
- Contract:
  `results/SLICE 1 - PRECEDENCE CONTRACT AND SEMANTIC VALIDATION.md`.
- Lifecycle v0.5 closed failures:
  - `retained_provider_custody_precedes_authority`;
  - `provider_fan_in_precedes_authority`.
- Temporal v0.6 independently refuses an authority request over retained custody,
  even when all digests are recomputed.
- Genuine authority-only observations retain a stable request digest across trusted
  observation time.
- Focused result: 28 tests passed; 1 optional `jsonschema` check skipped.
- Provider I/O, create, retrieval, authorization consumption, and frozen-QA access:
  0.
- Runtime selector change: none; current contradictory mixed branches fail closed
  pending Slice 2.

## Slice 2 evidence

- Shared selector now orders retained provider truth before prepared authority.
- Exact and bounded not-due mixed states select ineligible
  `provider_reconciliation_cycle` with native `not_before`.
- Exact and bounded due mixed states select only the first four native due members.
- Completed-provider evidence selects `ordinary_resume` before authority.
- Time-only not-due → due keeps one v0.6 checkpoint basis and absent authority
  inventory.
- Focused result: 70 tests passed; 1 optional schema check skipped.
- Provider create/retrieval, authorization consumption, and frozen-QA access: 0.

## Slice 3 evidence

- Installed qualification surface: `astrowoof-provider-pending-qa`.
- One workspace owns six provider identities plus one later prepared action.
- Retrieval cardinality: first cycle 4; second cycle 2; unique total 6.
- Prepared authority before completion/fan-in: absent.
- Second-cycle completed-evidence branch: `ordinary_resume`.
- Post-fan-in branch: `await_external_authority`, containing only the prepared ID.
- Provider transport is scripted and local; external network/spend: 0.
- Focused result: 34 tests passed.

## Slice 4 evidence

- Route matrix:
  - exact Natal interactive Response: pass;
  - bounded Natal interactive Response: pass;
  - exact Natal Batch: pass;
  - bounded Natal Batch: pass.
- Batch authority remains one provider action/round; no member-level reservation
  authority was introduced.
- Supported interactive stage matrix: initial, retry, polish, critic, candidate.
- Ordinary optional-stage Batch dispatch remains explicitly unsupported/refused.
- Focused result: 13 tests passed.
- Provider/network/spend and frozen-QA access: 0.
