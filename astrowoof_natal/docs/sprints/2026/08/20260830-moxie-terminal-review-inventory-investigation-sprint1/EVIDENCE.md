# Evidence — Moxie terminal-review inventory investigation

## Current gate

Slices 0–6 are complete. Final `0.4.33` candidate qualification is recorded and
paused for final API/owner release review.

## Frozen supplied identities

- API run: `b39c8b14-d0c7-440a-b5b8-bd4bb0d85205`
- SBE job: `5f2757db-feb6-457e-8f76-e56f45e7eadf`
- Native run: `53bacbe893fa722a50a251111d9263a7c703da28c088b30fcdc9ff3798a8dea4`
- Checkpoint generation: `11`
- R2 storage object ID: `429d43b2-6dc0-4ad9-ac31-ee68c9d32878`
- Archive SHA-256: `aa6b472e3b865242f93c388a8664828a292ff05953e835211f90a70567132920`
- Inventory SHA-256: `88d6e44341ade8d21fccf3c2964f721e03f45e089a510c4859f3ca9f8bc61509`
- Provider version/ETag: `"43ecac806938556e1bf16e6b63952130"`

## Source contract evidence

- `build_terminal_action_dispositions()` projects every action from
  `state.spend_ledger.actions` in ledger order.
- Result v0.2 carries the ordered rows, their inventory digest, and custody
  subsets.
- `validate_terminal_review_result_v02_against_api_actions()` requires exact
  action-set equality plus native-run, binding, route-family, stage, and
  provider-operation joins.
- No terminal-review v0.2 field declares a legitimate smaller snapshot subset.

## Evidence limitation before access

The background has an R2 storage object ID, hashes, size, ETag, and logical path,
and API has now supplied the exact object key for the approved `HEAD` and `GET`.
The coordinate requirement is satisfied. Bucket listing and guessed keys remain
prohibited.

## Slice 0

- Contract map: `SLICE 0 - CONTRACT MAP AND EVIDENCE FREEZE.md`.
- Access manifest: `SLICE 0 - R2 ACCESS MANIFEST.json`.
- Result scope established from source: complete native spend ledger.
- API asserted inventory: six reported initial actions plus one provider-created
  creative retry.
- Remaining field-level join input: the six initial API IDs and complete seven
  immutable binding documents are not present in the supplied sprint evidence.
- R2 operations performed: zero.

## Activity

- R2 HEAD/GET: one/one, the complete approved allowance.
- R2 list/write/delete: zero.
- Provider calls/spend: zero.
- Retained workspace commands/mutation: zero.
- API database/job/lease/capacity mutation: zero.
- Source/schema/version/release changes: zero.

## Slice 1

- Access receipt: `SLICE 1 - READ-ONLY R2 ACCESS RECEIPT.json`.
- Offline restore receipt: `SLICE 1 - OFFLINE RESTORE RECEIPT.json`.
- Publication validation: `SLICE 1 - RETAINED PUBLICATION VALIDATION.json`.
- Findings: `SLICE 1 - RETAINED CHECKPOINT FINDINGS.md`.
- Native ledger/result action count: 8.
- API-authoritative action count supplied in background: 7.
- Recovered result: `nres_b68e9150988370d154aa3c06`, valid v0.2
  `review_required/local_work_progress_contradiction`.
- Extra leading native row: providerless `PREPARED` retry-3 action
  `paid_95b6252fedb1610b3be397d9`.
- Remote allowance remaining: no HEAD, GET, list, write, or delete.

## Slice 2

- Causal matrix: `SLICE 2 - MOXIE SANITIZED CAUSAL AND INVENTORY MATRIX.md`.
- Retry-2 provider completion: reconciliation cycle 60 at revision 59,
  `2026-08-30T18:51:02Z`.
- Retry-3 preparation: journal sequence 82, revision 67,
  `2026-08-30T18:51:34.076900Z`.
- Terminal invocation/result: journal sequences 83–85, revision 69, beginning
  `2026-08-30T18:51:35.422091Z`.
- Intervening retry-3 lifecycle/external-authority publication: none retained.
- Production seam: pass attempt 2 remained
  `AMBIGUOUS_PROVIDER_SUBMISSION` while the ledger carried completed provider
  evidence; ordinary resume prepared attempt 3, then the progress fence found
  the retry-2 semantic operation still advertised and sealed the contradiction.
- Additional remote/provider/native/API mutation activity: zero.

## Slice 3

- Reproduction report: `SLICE 3 - PROVIDER-FREE REPRODUCTION.md`.
- Characterization: `tests/test_moxie_terminal_review_inventory_slice3.py`.
- Retained bad path: real top-level resume and local-work progress fence seal an
  eight-row `local_work_progress_contradiction`; seven-row API join refuses.
- Corrected ordering A: retry-2 result adopted, semantic operation consumed, no
  retry-3 action prepared.
- Corrected ordering B: retry-2 result adopted and rejected by deterministic QA,
  retry 3 prepared, successor selects its exact external-authority inventory.
- New/focused tests: 3/11 passed.
- Provider/network/spend activity: zero.
- Additional R2 access or retained workspace mutation: zero.
- Production runtime/schema/package changes: zero.

## Slice 4

- Classification/handoff: `SLICE 4 - FINDING CLASSIFICATION AND HANDOFF.md`.
- Primary correction: SBE exact-interactive completed-provider fan-in adoption
  must finish before successor retry selection.
- Public contract change required: no.
- Terminal-review projection or API strict-join weakening: prohibited.
- Runtime/source/schema/package changes: zero.
- Additional remote/provider/native/API mutation activity: zero.

## Slice 5

- Implementation record:
  `SLICE 5 - EXACT INTERACTIVE FAN-IN ADOPTION IMPLEMENTATION.md`.
- Runtime source: `src/astrowoof_natal_authoring/closure.py`.
- Provider-free matrix:
  `tests/test_moxie_terminal_review_inventory_slice3.py`.
- New/adjacent focused tests: 8/19 passed.
- Provider create/retrieve/network/spend: zero.
- Retained Moxie and R2 activity: zero.
- Public schema changes: zero.
- Exact interactive runtime source changed; packaging/version/release work has
  not begun.

## Slice 5A opening evidence

- Control-room issue: `kevin2357/astrowoof-api#7`.
- SBE-owned gap: `astrowoof-external-authority-v2` does not configure the
  standard logger or pass an event emitter into the v2 intent/dispatch runtime.
- Existing safe runtime event hooks include fence validation, intent commit,
  provider-create permission, provider identity, pending custody, and refusal.
- API-owned gap: reconciliation captures useful SBE stderr but does not retain
  or relay it; durable subprocess diagnostic retention is not claimed here.
- Public contract/schema/lifecycle changes expected: zero.

## Slice 5A completion evidence

- Implementation record: `SLICE 5A - V2 PUBLIC COMMAND OBSERVABILITY.md`.
- Runtime source:
  `src/astrowoof_natal_authoring/cli/external_authority_v2.py` and the existing
  request-selection event hook in `external_authority_v2_execution.py`.
- Tests: `test_external_authority_v2_cli.py`,
  `test_ambiguous_provider_submission_runtime.py`, and
  `test_moxie_terminal_review_inventory_slice3.py`.
- Focused matrix: 20 passed in 42.003 seconds.
- Privacy: API-key, prompt/payload, authorization-document, and protected error
  sentinels absent from emitted events/logs.
- Event-sink failure: authoritative refusal/result and zero-provider-I/O
  behavior unchanged.
- Compilation/diff hygiene: passed.
- Provider/network/spend and retained Moxie/R2 access: zero.
- Public schema/lifecycle/authority changes: zero.

## Slice 6

- Candidate record:
  `SLICE 6 - INSTALLED QUALIFICATION AND RELEASE CANDIDATE.md`.
- Final wheel SHA-256:
  `2559ba0e6edd07c27641d11933928457aae8e4a082c1158a74ca0c523cfd7313`.
- Deterministic builds: two, byte-identical.
- Installed dependency identity: SPC `0.11.1`; `pip check` passed.
- Installed commands passed: generic smoke, external-authority v2,
  adversarial lifecycle, post-fan-in retry, and terminal review.
- Full suite once: 925 tests / 1,068.115 seconds / 48 expected skips / one
  historical release-derived fixture mismatch.
- Focused correction: 17 passed, one expected optional-schema skip.
- Full suite repeated: no, per explicit owner direction.
- Final installed qualifications after rebuild: passed.
- Provider/network/spend and retained Moxie/R2 activity: zero.
