# Slice 0 — Frozen Trace Reconstruction and Coordinate Request

## Outcome

The frozen traces establish one shared first-polish boundary and two distinct
observable failures. They do not prove whether either sealed native result
carried the exact authority request API needed. Ownership therefore remains
open pending two bounded immutable-object inspections.

No storage read, provider I/O, workspace recovery, mutation, or runtime change
was performed.

## Source boundary

This reconstruction uses the supplied API facts plus the unfiltered worker log
and contiguous Better Stack cohort listed in `EVIDENCE.md`. Log events are
diagnostic evidence of ordering; they are not substitutes for sealed result,
receipt, request, action, or binding objects.

## Side-by-side evidence matrix

| Boundary | Ada Brioche | Aldus Croissant |
| --- | --- | --- |
| API run | `cf631433-b898-4214-8c2d-e2b6e37a7d0b` | `b2879540-54af-462f-8973-5f2f98b8c078` |
| Native run | `26974e4422013a2fcc2bc9f6ec1bbf93401f7d0dd87926b5a530525f3e19c49c` | `65b7940ea2b54120db19291a64bdb84a5f81bce56cd190cc105c61a3f952f63d` |
| Pre-polish paid history | six initial actions `REPORTED` | six initial plus one creative retry `REPORTED` |
| Final-QA observation | `FINAL_QA_FAILED`; one validation error; three lint findings | `FINAL_QA_FAILED`; one validation error; three lint findings |
| First polish action | `paid_67c8a2afd008a6fdf317c1b0`, `PREPARED`, 617385 micro-USD | `paid_470896db6a2cf2312864dccd`, `PREPARED`, 617021 micro-USD |
| Inventory transition | six reported → six reported plus one prepared polish | seven reported → seven reported plus one prepared polish |
| Native state | `AWAITING_SPEND_AUTHORIZATION`, revision 54 | `AWAITING_SPEND_AUTHORIZATION`, revisions 76–78 |
| Diagnostic request posture | `v2_intent_present=False`; no trace-level grantable request proven | `authorization.awaiting` and `spend_boundary_handoff` emitted; sealed request still unproven |
| First relevant publication | provider reconciliation, native-result v0.1, `awaiting_external_authority`, cause `spend_authorization_required` | ordinary authoring, native-result v0.2, `review_required`, cause `native_lifecycle_review_required` |
| Published result / receipt | `nres_3b5ee9a244262af1e415e112` / `nreceipt_83bab5d85dda4de42f748eaf` | `nres_e41bbf89a77e50f6b5c87a06` / `nreceipt_de8f55540f2b4ded4f9f899b` |
| Enclosing command outcome | provider-reconciliation result v0.2 becomes `review_required` | terminal-review command v0.1 says `review_required` |
| API terminal observation | closeout `review-required`; job failure `native.review.requires_review` | cycle first reports `terminal_closed`, then fails `sbe.contract.provider_lifecycle` because `SBE terminal review API action inventory changed` |
| Final accepted SBE checkpoint | generation 6, `5caed3f7-c668-4946-bc95-df387faaff82` | generation 11, `25f30ea7-dbe3-4d79-8c2a-f1e130b8f0b0` |

## What the traces decide

1. The failure is not a general initial fan-in or provider-custody failure.
   All preceding paid actions have reported evidence and provider custody is
   zero at the first-polish boundary.
2. Both runs legitimately enter polish because whole-deck final QA fails with
   the same counts. Preparing a polish action is therefore expected state
   evolution, not by itself terminal evidence.
3. Ada does not expose a trace-proven external-authority-v2 intent. Her native
   publication says `awaiting_external_authority`, but the enclosing command
   converts that posture to `review_required`.
4. Aldus emits the expected spend-boundary signals, but that still does not
   prove the sealed v0.2 result includes a valid exact request. His later API
   failure specifically compares terminal-review action inventories after the
   expected seven-to-eight mutation.
5. The two endings may be manifestations of one unstable handoff boundary, or
   two defects: an Ada publication/request gap and an Aldus terminal-review
   snapshot-ordering gap. The traces cannot safely choose between them.

## Exact questions for immutable inspection

For each run, inspection must answer:

- Does the named sealed result join exactly to its receipt and invocation?
- Does it identify the exact prepared polish action and subject?
- Does it contain an external-authority request or refusal? If present, does
  that object join exactly to the paid action and authorization binding?
- Is the request structurally consumable by API, including its digest and
  action inventory, or is the awaiting-authority meaning present only in the
  outcome/cause fields?
- What action inventory did terminal review take as its before/after basis?
- For Aldus, is the seven-to-eight change inside ordinary authoring the only
  inventory change, and should terminal review have treated it as expected
  local work rather than terminal settlement?

## Smallest coordinate request

Please provide two closed protected-checkpoint coordinate packets, one for each
final accepted SBE checkpoint below. Coordinates alone authorize no storage
operation.

### Ada

- API run: `cf631433-b898-4214-8c2d-e2b6e37a7d0b`
- native run: `26974e4422013a2fcc2bc9f6ec1bbf93401f7d0dd87926b5a530525f3e19c49c`
- SBE job: `290799eb-fd83-4152-ae21-1474ec96f7ee`
- checkpoint: `5caed3f7-c668-4946-bc95-df387faaff82`
- generation: 6
- expected result: `nres_3b5ee9a244262af1e415e112`
- expected receipt: `nreceipt_83bab5d85dda4de42f748eaf`

### Aldus

- API run: `b2879540-54af-462f-8973-5f2f98b8c078`
- native run: `65b7940ea2b54120db19291a64bdb84a5f81bce56cd190cc105c61a3f952f63d`
- SBE job: `f0c2c775-59b6-4284-9e0e-f49b53f9435d`
- checkpoint: `25f30ea7-dbe3-4d79-8c2a-f1e130b8f0b0`
- generation: 11
- expected result: `nres_e41bbf89a77e50f6b5c87a06`
- expected receipt: `nreceipt_de8f55540f2b4ded4f9f899b`

Each packet should use the established
`astrowoof.protected_checkpoint_coordinate.v1` shape and include API/native/job/
checkpoint identities, generation and stage, exact bucket/object/version/ETag,
byte size, archive and inventory hashes, logical-root and snapshot identities,
native revision/status, SBE/SPC releases, and the expected invocation/result/
receipt identities and hashes. Please publish each packet's SHA-256 beside it
and state that it addresses the named accepted checkpoint after the relevant
first-polish publication.

## Proposed Slice 1 access boundary

After owner review, request separate authorization for exactly one conditional
`HEAD` and one bounded conditional `GET` per named object. Validate coordinates
and safe archive structure, then extract only snapshot/journal indexes, the
named sealed result and receipt, the named polish paid-action record, final-QA
state, and any exact request/refusal/binding records needed for the questions
above. No recovery, resume, reconciliation, provider call, spend decision, or
workspace mutation is requested.

## Slice disposition

Slice 0 is complete. Slice 1 is blocked only on API supplying the two coordinate
packets and the owner separately authorizing the bounded reads.
