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
- Runtime implementation remains unstarted pending owner authorization.
