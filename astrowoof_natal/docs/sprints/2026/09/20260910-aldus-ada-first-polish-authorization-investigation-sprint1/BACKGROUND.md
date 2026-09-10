# Aldus/Ada First-Polish Authorization Investigation — Background

## Purpose

Two fresh, independent QA authoring runs under the coherent API/SBE `0.4.57`
rollout reached the same post-fan-in/final-QA boundary and failed to continue
through first polish. The immediate task is to reconstruct the exact native
facts, distinguish an expected editorial terminal from an invalid
authorization/terminal-review transition, and identify the narrowest owner.

This is an investigation only. Do not resume, reconcile, repair, recover,
submit provider work, mutate a retained workspace, or make a runtime change
until the cross-repository evidence establishes a cause.

## Frozen cohort and joins

| Pup | API reading | API generation run | Native run |
| --- | --- | --- | --- |
| Aldus Croissant | `68f92211-8be9-4539-8f4d-1e8dae6ffaea` | `b2879540-54af-462f-8973-5f2f98b8c078` | `65b7940ea2b54120db19291a64bdb84a5f81bce56cd190cc105c61a3f952f63d` |
| Ada Brioche | `d03d47e1-21b5-47ea-a672-edcc598ec8f8` | `cf631433-b898-4214-8c2d-e2b6e37a7d0b` | `26974e4422013a2fcc2bc9f6ec1bbf93401f7d0dd87926b5a530525f3e19c49c` |

The cohort was explicitly authorized at USD `50/run`, `100/cohort`, `150`
rolling 24-hour, `49` for each initial/creative-retry/polish/critic stage, and
`0` qualitative candidate. The QA profile and workers had just passed the
scripted full-fleet attestation/provider-free rollout.

## Authoritative API facts

At the last read-only inspection both API runs are terminal `failed` and hold
no active execution capacity.

### Ada

- deterministic work succeeded;
- six initial paid actions are recorded `reported`;
- the SBE job failed at attempt `5/64` with
  `failure_classification=native_review_required` and
  `failure_reason_code=native.review.requires_review`;
- no API lifecycle-closeout row was found in the immediate terminal query.

### Aldus

- six initial actions and one creative retry are recorded `reported`;
- his final API state is also terminal `failed`, with no active capacity;
- the preceding API lifecycle inspection had
  `execution_capacity_disposition=continue_local_cycle`,
  `execution_capacity_reason_code=local_work_ready`, and
  `provider_custody_state=completed_evidence_pending_local_work`.

The API facts establish custody and terminalization, but do not alone establish
why native selected review rather than a normal first-polish continuation.

## SBE trace facts (non-authoritative, but diagnostic)

The current SBE worker snapshot was saved without filtering at:

`C:\tmp\sbe-pair-aldus-ada-live-check.log`

It contains both native IDs above. It is a convenience diagnostic artifact, not
an immutable checkpoint.

### Ada's latest relevant native evidence

- state: `AWAITING_SPEND_AUTHORIZATION`, revision `54`;
- action inventory: six initial `REPORTED`, one polish `PREPARED`;
- native summary: `subject_states=FINAL_QA_FAILED:1`,
  `optional_stage_states=SUBMITTED:1`, and zero provider custody;
- publication outcome: `awaiting_external_authority`, cause
  `spend_authorization_required`;
- SBE closure-level result: `review_required`.

### Aldus's latest relevant native evidence

- state: `AWAITING_SPEND_AUTHORIZATION`, revision `78`;
- action inventory: six initial `REPORTED`, one creative retry `REPORTED`, and
  one further optional action `PREPARED`;
- native summary: `subject_states=FINAL_QA_FAILED:1`,
  `optional_stage_states=SUBMITTED:1`, and zero provider custody;
- ordinary-authoring publication outcome: `review_required`, cause
  `native_lifecycle_review_required`;
- terminal-review command result also says `review_required`; SBE worker logged
  `terminal_closed` after checkpoint generation `11`.

## Initial hypothesis (explicitly rebuttable)

The pair suggests a seam at the first optional polish action after a native
whole-deck final-QA failure, not a general provider/fan-in problem:

1. initial work (and Aldus's creative retry) reaches reported evidence;
2. native materializes `FINAL_QA_FAILED` and an exact first polish action;
3. native observes a submitted/prepared optional stage but transitions to
   spend-authorization/review posture rather than receiving the expected API
   grant-or-denial ingestion; and
4. API ultimately turns that review posture into `native.review.requires_review`.

This is **not yet a causal conclusion**. In particular, determine whether the
native output actually contained a valid exact authority request, whether the
API owned an expected grant/denial decision, and whether terminal review was
already semantically required by the frozen native evidence.

## Boundaries

- QA workspaces are retained only for read-only, owner-authorized exact-object
  inspection after a coordinate packet is supplied.
- Do not infer a missing API grant from a trace line alone.
- Do not access providers or make any spend decision.
- Preserve the distinction between a correct editorial terminal outcome and a
  failed handoff which merely happens to occur after final QA.
