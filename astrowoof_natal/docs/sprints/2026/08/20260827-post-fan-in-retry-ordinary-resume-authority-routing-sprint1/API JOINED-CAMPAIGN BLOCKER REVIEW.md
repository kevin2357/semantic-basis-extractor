# API Joined-Campaign Blocker Review

Date: 2026-08-27  
Disposition: **add corrective Slice 4A before release preparation resumes**

## Finding

The new `astrowoof-post-fan-in-retry-qa` fixture is a good closed,
provider-free qualification receipt. It proves the incident successor and is
reproducible. Its public receipt deliberately exposes only ordered phase names
and evidence hashes, however.

That is sufficient to attest that SBE's own qualification passed. It is not
sufficient for the planned API joined campaign: API cannot route opaque hashes
through its real lifecycle translator, persistence, scheduler, lease, and
capacity services. Reconstructing the corresponding native facts from private
workspace state would violate the SBE/API ownership boundary.

This is an incompleteness in the intended Slice 4 handoff surface, not a new
runtime defect and not a reason to split this into a separate incident sprint.

## Required corrective Slice 4A

Publish a sanitized, closed, provider-free **ordered inspection-projection
bundle** for the existing seven post-fan-in qualification phases:

```text
provider_not_due
provider_retrieval
local_fan_in
local_operation_consumed
ordinary_v2_authority
one_dispatch
exact_replay
```

Each projection must expose the exact public lifecycle facts API needs to
validate, persist, and schedule the phase through existing API services:

- stable scenario/run identity and route/mechanism;
- selected command, capacity disposition/reason, eligibility, and `not_before`;
- public provider-custody classification and ordered action IDs;
- public local-operation inventory and consumption identity/count as applicable;
- external-authority state and ordered action IDs as applicable; and
- a stable phase/bundle digest binding it to the existing fixture and receipt.

## Boundary requirements

- Provide a supported public reader and strict validator, with installed-wheel
  fixtures/tests.
- The bundle must be reproducible across disposable workspaces and bind to the
  existing fixture identity/phase order.
- Do not expose raw `run.json`, workspace paths, snapshots, prompts, provider
  payloads, provider IDs, credentials, protected provenance, or retained-QA data.
- API consumes validated projections; it does not select an SBE command, invent
  local work, reconstruct native state, or receive authority to mutate SBE.
- Keep the current runtime correction and v1/v2 authority boundaries unchanged.
- Preserve provider-free, zero-spend, zero-retained-QA qualification.

## Resulting release sequence

1. SBE completes Slice 4A and pauses for API review.
2. API runs Sprint 54's real translation/persistence/one-slot campaign against
   the exact installed candidate.
3. If that campaign passes, SBE resumes its existing Slice 5/6 publication path;
   then API deploys the single released candidate once to QA.

No provider work, retained-QA recovery, deployment, or release is authorized by
this review.
