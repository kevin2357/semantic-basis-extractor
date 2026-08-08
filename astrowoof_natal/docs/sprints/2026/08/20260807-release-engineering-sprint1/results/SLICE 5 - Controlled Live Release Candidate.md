# Slice 5 - Controlled Live Release Candidate

Status: safe controlled stop; corrective change and gate result await approval.

## Approved live profile

The user authorized Ella through OpenAI Batch with all three optional stages
enabled, a USD 5.00 run ceiling, USD 1.00 ceilings for initial authoring,
creative retry, polish, qualitative critic, and qualitative candidate, and
generation-profile-driven skipping for optional stages that exhaust budget.
No dollar values from design examples were treated as defaults.

The input used UUID source identity
`e11a0000-0000-4000-8000-000000000001` with installed AGF 0.6 / SPC 0.10
compatibility. Provider payloads were scanned before authorization for exact
birth date/datetime, coordinates, location, and protected field names.

## Execution result

- The exact installed candidate prepared and authorized one initial Batch
  action for a conservative USD 0.540033 commitment.
- Detach/resume and polling reused Batch
  `batch_6a76ab49fbe88190a0bc64caa74e004e`; they created no new commitment.
- OpenAI reported 254,272 input tokens (254,254 cached), 83,553 output tokens,
  1,228 reasoning tokens, and estimated spend of USD 0.263381.
- One pass was accepted. Five passes required creative retry.
- The retry round's conservative commitment was USD 1.125082, exceeding the
  approved USD 1.00 creative-retry ceiling. It was not authorized or submitted.
- The durable terminal operator state is `BUDGET_EXHAUSTED`. The ledger has two
  actions and exactly one provider operation.

Optional stages were enabled but were not reached because creative retry is a
mandatory production stage and hard exhaustion stops the run. Earlier blocked
discovery runs exercised polish and critic and exposed the candidate disclosure
defect; those runs are not claimed as final qualification.

## Corrective finding

The live boundary revealed that an over-ceiling action was initially left
`PREPARED`/`AWAITING_SPEND_AUTHORIZATION` until an authorization attempt.
The candidate now classifies ceiling failure during preparation, reclassifies
persisted prepared actions on resume, and durably writes both ledger and public
`BUDGET_EXHAUSTED` state before raising. Mandatory exhaustion and optional skip
remain distinct.

The complete suite passes 144 tests. Two fixed-epoch final builds are
byte-identical at 623,777 bytes with SHA-256
`312bdf1dba73c80111aeaa95280c4e64f7078dcf17ca0fea91d0105e3f8a7030`.
That exact wheel passed clean-installed deterministic release smoke.

## Gate

The spend safety behavior passed under the user-approved policy, but the live
run did not reach delivery. Proceeding requires explicit approval of the
corrective change and either acceptance of this bounded hard-exhaustion result
for Slice 5 or a separately approved retry ceiling for another live run.
