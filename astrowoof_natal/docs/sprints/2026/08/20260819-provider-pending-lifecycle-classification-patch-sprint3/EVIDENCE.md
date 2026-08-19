# Provider-Pending Lifecycle Classification Patch Sprint 3 Evidence

Status: implementation complete; provider-free qualification passing.

## Implemented evidence

- Current schema: `astrowoof.authoring_lifecycle_inspection.v0.4`.
- Historical v0.3 fixture and schema remain packaged without reinterpretation.
- Provider-only waiting projects no local dependency and selects the reconciliation
  branch before and after due time.
- Due branch action IDs equal SBE's `provider_custody.next_due_action_ids` and are
  capped at four. They are diagnostic native selection, not API member authority.
- `validate_lifecycle_inspection_v04()` rejects contradictory continuation,
  capacity, timing, and action-subset projections.
- Packaged fixture: `fixtures/lifecycle/inspection.v0.4.json`.
- Installed command: `astrowoof-provider-pending-qa`.
- Qualification receipt contract:
  `astrowoof.provider_pending_lifecycle_qualification.v1`.
- Candidate wheel: `astrowoof_natal_authoring-0.4.13-py3-none-any.whl`.
- Candidate wheel SHA-256:
  `0e3ecc41e6752ce050aa55ce2d5fc5b4b8453f19d4e7032e7abadf420f57dcb4`.
- Installed qualification receipt SHA-256:
  `b77614fb4aebe641fc10d347a9ebc1e3d1133a573b51b9dcfc205cf3763e1576`.
- Provider-free qualification proves six unique creates, not-due release, direct
  due selection, bounded four-then-two retrieval, six durable response artifacts,
  no duplicate create/retrieval, and contradiction refusal.

## API review

- Outcome: approved.
- API review commit: `4455acc`.
- Accepted corrections: provider reconciliation is not ordinary local
  continuation; an already-due first inspection selects reconciliation directly.
- Accepted selection boundary: SBE owns the bounded next-action subset (maximum
  four). API consumes the branch and invokes the run-level command without member
  selection or reconstruction.

## Current native evidence

- `_local_dependencies()` maps `WAITING_FOR_RESPONSE` to the dependency kind
  `provider_result_reconciliation`.
- `inspect_lifecycle()` currently sets `local_continuation_remains` from
  `bool(local_dependencies)`, so a provider-only wait becomes local continuation.
- `_capacity_and_custody()` correctly discovers durable provider-bound actions,
  validates per-action reconciliation timing, and emits complete provider custody.
- Before due, capacity is `release_until_due`.
- At/after due, capacity is `continue_local_cycle` with generic
  `reason_code=local_work_ready`; v0.3 has no closed supported-command field.
- Existing tests freeze the now-problematic provider-only value
  `local_continuation_remains=true` and therefore require intentional revision.

## Current API evidence

- API selection currently enters reconciliation only when its latest persisted
  inspection has `execution_capacity_disposition=release_until_due` and a non-null
  `resume_not_before`.
- If the first post-wave inspection is already due, the native generic local-cycle
  tuple does not satisfy that predicate, so ordinary resume can be selected.
- The API validator already rejects one contradictory no-local-readiness/pending-
  custody tuple, but the public SBE contract still needs an affirmative typed branch.

## Safety

- Retained QA cohort accessed: no.
- Provider creates/retrievals: 0 / 0.
- Spend: USD 0.
- Repository changes: documentation only.
