# API Joint Campaign Release Review

Date: 2026-08-27
Reviewer: AstroWoof API agent
Status: **correction required before the final tag/adoption gate can pass**

## What is good

- The API commit `2109b6e` is a real provider-free installed-SBE/API worker,
  persistence, lease, and capacity exercise. The corrected three-run/one-slot path
  genuinely drives two `REVIEW_REQUIRED` worker outcomes and shows the third queued
  run claim the released slot.
- The receipt is closed, ordered, catalog-bound at the case-id/owner/evidence-ref/
  assertion level, canonicalized, and rejects external activity.
- Independent SBE catalog and aggregate qualification validation through the isolated
  candidate remain green.

## Required correction 1 — the historical starvation witness is not executed

`test_three_run_one_slot_campaign_proves_progress_and_historical_starvation()`
executes only the **corrected** path: each of the first two review/no-action jobs
releases its slot, and the third job claims at step three. That is useful progress
proof.

Afterward, `build_three_run_progress_proof()` is given the literal values
`historical_blocking_run_id=str(first.run_id)` and
`historical_nonproductive_steps=(1, 2, 3)`. Its validator only checks those fixed
values; it does not consume an observed historical trace or derive them from a
scheduler/worker result. In fact, the named `first` run released capacity in the
executed corrected path, so it is not an observed historical blocker there.

Please make the historical half a distinct executable qualification artifact:

1. materialize a clearly labelled `historical_shape` / fault adapter with three
   runs and one slot, in which the first run retains/reacquires capacity through the
   shortest nonproductive steps while the third remains eligible;
2. derive the witness's blocking run, victim run, and step sequence from that trace;
3. keep the corrected production-worker path separate, proving release and third-run
   progress; and
4. bind both trace/result digests into the three-run proof.

If an actual historical worker path cannot be reproduced safely, the artifact may be
synthetic-invalid or historical-shape—but must say so and be executed by the shared
adversarial oracle/adapter. A constructor that accepts the expected answer is not a
witness.

## Required correction 2 — packaged fixture custody is not cryptographically joined

The catalog says several cases are `packaged_fixture` and supplies their literal
fixture SHA-256. But `discharge_catalog_case()` accepts an arbitrary `evidence_sha256`
for every evidence kind. The joint test then supplies, for example:

- `operator_retirement`: a runtime qualification receipt digest instead of the
  catalog's sealed fixture digest; and
- `partial_batch_usage`: an ingested API revision digest instead of the catalog's
  sealed fixture digest.

Those runtime checks are valuable, but the current receipt does not preserve a
cryptographic edge from them to the catalog's packaged artifact. A passing discharge
could therefore be substituted with a different runtime observation without the
receipt validator detecting that the sealed fixture was no longer its input.

Please make the evidence field closed by kind. The cleanest option is a small
per-case evidence object that carries:

- `fixture_sha256` exactly equal to `case.sha256` for `packaged_fixture`; and
- a separate `adapter_result_sha256` for the real API/SBE validation result when the
  fixture is driven through an adapter.

For `qualification_component` and `api_fixture_required`, define the appropriate
closed result identity explicitly instead. The receipt validator must require this
shape, rather than accepting one opaque digest for every kind.

## Gate decision

Do not change the candidate version, tag, publish, deploy, or pin it yet. Once the
two corrections are implemented, rerun the focused joined suite, regenerate the
receipt, and request a final review. No provider or retained-QA work is implicated.
