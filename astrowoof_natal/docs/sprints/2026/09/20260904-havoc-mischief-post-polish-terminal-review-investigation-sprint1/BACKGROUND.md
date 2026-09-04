# Havoc/Mischief post-polish terminal-review investigation

## Why this exists

The fresh QA pair completed the intended live pipeline cleanly through initial
fan-out, provider reconciliation, exact ordinary-v2 optional-stage authority,
polish-provider retrieval, and adoption. Both then reached the native terminal
state `FINAL_QA_FAILED` after their first polish attempt. The common outcome may
be a legitimate shared editorial rule, but it needs an evidence-led review
before anyone treats it as expected behavior or changes product policy.

This is an investigation sprint. It must not resume, reconcile, repair, mutate,
or access the provider. It must not treat an SBE log as custody authority.

## Frozen QA identities

| Dog | Reading ID | API run ID | Native run ID |
| --- | --- | --- | --- |
| Havoc von Hooligan | `76615c50-5996-470b-881d-420774fe8791` | `18d29fd9-2e74-4803-8de9-f65324c69a10` | `8fe16b99856c96c5a6fd67c59e9a9bd4f89199725101456a60ae3456ba410b7b` |
| Mischief McMuffin | `5caca45a-8b86-429d-be62-e79c3bab946b` | `273dbea7-50c8-4dee-b1ac-3f99e68be5ea` | `e41cee4362fc2ba3ce7fcfdcf633d99bc1762a66a05fb2d76424c6908a8b2ebb` |

Both runs used SBE `0.4.43` and SPC `0.11.1` in QA.

## Established facts

1. Each run completed six initial authoring actions and exactly one `polish`
   action; all seven are durably `reported` by API.
2. Both polish responses were retrieved and joined into the exact optional-stage
   consumer attempt (`completed_optional_provider_result_joined_for_adoption`).
3. Each native workspace transitioned to `FINAL_QA_FAILED` immediately after
   its polish result was adopted. The validation command returned code 1, while
   the lint command returned code 0 and logs recorded no warnings.
4. API run and SBE job are terminal `failed`; capacity is released and there
   are no active leases. There is no live provider custody or spend admission
   awaiting action.
5. The relevant native terminal publication was `review_required`; that records
   an editorial terminal review rather than a provider or transport failure.

## Already exported evidence

The following local artifacts were generated without workspace, provider, or
database mutation. They are convenience evidence only; source authority stays
with the frozen QA records and any subsequently supplied bounded checkpoint
packet.

- Raw cohort SBE log window:
  `C:\tmp\qa-havoc-mischief-run-report-20260904\sbe-worker-cohort-raw.log`
- Havoc filtered log and run-evolution report:
  `C:\tmp\qa-havoc-mischief-run-report-20260904\sbe-worker-havoc.log` and
  `C:\tmp\qa-havoc-mischief-run-report-20260904\havoc-report\`
- Mischief filtered log and run-evolution report:
  `C:\tmp\qa-havoc-mischief-run-report-20260904\sbe-worker-mischief.log` and
  `C:\tmp\qa-havoc-mischief-run-report-20260904\mischief-report\`

## Investigation question

For each dog, identify the authoritative editorial issue codes and the exact
final validation outcome before and after polish. Then determine whether the
shared `FINAL_QA_FAILED` outcome is:

- two legitimate independent editorial rejections;
- a shared fixture/prompt/product-policy effect that needs owner discussion; or
- a defect in validation, report interpretation, optional-stage adoption, or
terminal projection.

If checkpoint contents are necessary, ask API for an exact hash-verified,
read-only coordinate packet for only the final accepted checkpoint and the
named validation/acceptance artifacts. Do not list R2 or infer object paths.
