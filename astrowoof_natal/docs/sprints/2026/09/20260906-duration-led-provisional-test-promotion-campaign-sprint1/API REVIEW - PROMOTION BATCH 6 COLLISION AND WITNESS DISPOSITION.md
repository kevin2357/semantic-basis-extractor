# API review — promotion batch 6 collision and witness disposition

## Decision

**Approved for promotion:**

- `test_batch_negative_authorization.py`; and
- `test_external_authority_v2_intent_fence.py`.

Promote only those two modules, then run the repeated concurrent
actual-manifest stress proof before selecting Batch 7.

**Historical witness decision:** archive
`test_completed_retry_duplicate_submission_investigation_slice0.py` as
forensic characterization, rather than promoting it or retaining it in the
active regression suite.

## Collision evidence accepted

- Three two-copy repetitions produced 12/12 green secret-scrubbed worker
  receipts, with exact inventories of 18/0 and 17/0 tests/skips, empty stderr,
  and no failures or errors.
- The real tests retained their substantive boundaries: all-or-none denial,
  crash recovery, replay/nonmutation, ordered events, workspace-lock behavior,
  durable v2 intent, ambiguity fencing, provider-identity safety, and zero
  unintended provider calls.

## Witness disposition rationale

The held test deliberately proves an obsolete defect is reproducible by
restoring a frozen mixed checkpoint twice and observing two scripted creates.
It is useful historical explanation, but asserting that broken behavior in the
ordinary active suite is neither a present-tense product invariant nor enough
reason to pay its maintenance coupling cost.

The current regression chain supplies the meaningful replacement:

- Slice 2 proves the authorization route is a typed, nonmutating,
  provider-create-forbidden refusal; and
- Slice 2 also proves contradictory completed local progress seals an exact
  review result with `new_provider_create_permitted=false`.

Archive the original reproduction with a short provenance record and links to
those current invariants. Do not delete its history or silently recast it as a
success case. In the follow-up archival change, remove it from routine manifest
selection/discovery rather than leaving a `test_*.py` historical failure witness
to run accidentally. That archival move is separate from this two-module
promotion and must preserve an exact source/evidence pointer.

## Next boundary

After the narrow promotion, require the actual-manifest stress receipts to
match in test identities, outcomes, skips, manifest digest, and stderr posture.
No semantic-closure move, production/package change, or additional provisional
promotion is authorized here.
