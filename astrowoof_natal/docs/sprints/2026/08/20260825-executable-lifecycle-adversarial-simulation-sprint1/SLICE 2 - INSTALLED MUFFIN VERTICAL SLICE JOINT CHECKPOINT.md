# Slice 2 — Installed Muffin Vertical Slice Joint Checkpoint

Status: SBE installed/runtime half complete; paused for the API scheduler/capacity
half of the joint vertical-slice review.

## What SBE now provides

The qualification-only installed package exports:

- `materialize_review_no_action_workspace(root)`
- `inspect_review_no_action_workspace(run_dir)`
- `build_review_no_action_runtime_trace(inspection, api_translation=...)`

The materializer directly writes one fixed, deliberately sanitized exact-Natal
`run.json`, then uses SBE's production `public_run_state()` and complete
workspace-snapshot writer. It is a narrowly labeled historical-fixture constructor,
not a production-state builder or generic native editor. It contains
no subject, prompt, provider request/response payload, provider identity, credential,
or spend-capable transport.

The inspector obtains SBE's native single-writer lock and invokes the real
`inspect_post_fan_in_lifecycle()` production boundary. It validates the resulting
v0.7 document and refuses unless it reaches exactly:

- `selected_command = none`
- `capacity_disposition = retain_for_review`
- `local_work_ready_now = false`
- empty local-work operations
- complete, authoritative snapshot observation under established native exclusion

The trace builder takes those same validated lifecycle bytes and creates either:

- the historical lossy API fixture projection, classified `stutter`, retaining its
  lease/capacity and carrying a competing-run starvation witness; or
- the corrected API fixture projection, classified `productive`, releasing its
  modeled lease/capacity.

The native public evidence and digest are identical between the two projections.
Only the explicitly API-owned qualification state changes. SBE does not claim that
the modeled API fixture is deployed database authority.

## API fixture projections—not production proof

The historical and corrected API states in SBE's trace are controlled qualification
inputs. They demonstrate the distinction the composed harness must test, but they do
not prove how the API's production translator, database, lease service, capacity
service, or scheduler behaves.

An ad-hoc cross-repository invocation observed the current API validator/mapper
produce `terminal_closed` and `local_continuation_required=false`, but SBE does not
claim that uncommitted observation as authoritative qualification evidence. API
Sprint 52 must publish its own reproducible committed test/receipt.

## Remaining joint gate

The API companion must now run this installed SBE surface first through its real
`SbeLocalWorkLifecycleService` and `ProductionSbeCycleEngine`, and then through its
lease/capacity/scheduler harness with two runs and one slot, proving:

1. the historical translation retains the slot and witnesses the Muffin loop;
2. the corrected production translation releases the slot; and
3. the continuously eligible second run is then claimable/progresses.

SBE should not broaden the route matrix until that composed assertion is reviewed.

## Safety and qualification

- Installed candidate wheel SHA-256:
  `d167cbb005d72cf6dc19e223beaa702ccd4207fa5a57d1949a0dc0d1c3103e26`
- External network calls: 0
- Provider creates/retrievals: 0 / 0
- Spend: USD 0
- Retained QA access/mutation: 0
- Source-tree/test-helper imports in installed reproduction: 0
