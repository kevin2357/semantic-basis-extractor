# Log — Muffin Local-Resume Quiescent-Loop Investigation Sprint 1

## 2026-08-25 — Background reviewed and plan drafted

- Read the API-provided retained-cohort background.
- Inspected SBE v0.7 local-work selection/consumption and the API's current v0.7
  scheduling adapter.
- Identified the leading native gap: released qualification proves the contract
  around an injected successful mutation but not that the real ordinary-resume
  executor performs that mutation.
- Distinguished historical API `provider_created` lineage from current SBE
  provider-retrieval custody.
- Drafted the production-path reproducer, contract freeze, native correction,
  no-spin enforcement, installed qualification replacement, API handoff, and
  release gates.
- No source/schema/runtime/test/release/provider/retained-QA mutation has begun.

Current gate: owner/API review before Slice 0.

## 2026-08-25 — API wrapper diagnosis accepted; sprint closed

- API review identified the exact lossy translation:
  `local_continuation_required = not inspection.release_until_due`.
- Confirmed that this collapses typed `retain_for_review` and
  `unsupported_retain_capacity` outcomes into false local continuation.
- Accepted SBE 0.4.25's v0.7 contract as released; no native implementation or
  patch release is required on current evidence.
- Transferred the runtime correction and starvation regression to the API sprint.
- Kept expired-lease reaping/reset-precondition work API-owned and separate.
- Retained the original SBE investigation plan as contingency/audit material.

Final gate: closed before Slice 0; reopen only if API qualification produces
evidence of a distinct SBE-native defect.
