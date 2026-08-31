# Evidence — final-QA review terminal bridge investigation

## Inputs

- `Background.md`
- `C:\Users\kevin\Downloads\sbe logs.txt`
- Current SBE `main` source after release `0.4.34`

Log SHA-256:
`ccb0a8ca81ff031cc931cb1c94e53b401c17662d4d9c49dd0b4208eca468d569`.

## Preliminary Glimmer timeline

| Time (UTC) | Evidence |
|---|---|
| 07:42:13.202 | Final assembly: `FINAL_QA_WARN`, 0 validation errors, 3 lint findings. |
| 07:42:13.299 | Polish action `paid_6ee…` prepared. |
| 07:42:13.299 | Run becomes `AWAITING_SPEND_AUTHORIZATION`. |
| 07:42:16.997 | Prior ordinary cycle aborts on non-append-only local-work history after publishing the authority checkpoint. |
| 07:42:53.201 | Exact ordinary-v2 request/grant fence validates. |
| 07:42:53.202 | Polish action authorized and consumed. |
| 07:42:53.203 | Persist changes run status to `FINAL_QA_REQUIRES_REVIEW`. |
| 07:42:54.919 | V2 executor records provider creation as permitted. |
| 07:42:56.914 | OpenAI Responses POST begins while outer status is review-terminal-looking. |
| 07:42:57.520 | Provider returns queued identity `resp_0adb…`. |
| 07:42:57.815 | Provider identity is durably recorded. |
| 07:42:59.107 | V2 command returns `detached_provider_pending`. |
| 07:43:34.001 | API rejects the following public temporal lifecycle as terminal. |

## Preliminary source join

- `persist_state()` increments revision and unconditionally calls
  `update_run_status()`.
- `update_run_status()` preserves/derives `FINAL_QA_REQUIRES_REVIEW` from the
  subject's `FINAL_QA_WARN` state but has no explicit ordinary action
  `AUTHORIZED`/`SUBMITTING`/provider-bound precedence representing active polish
  custody.
- The v2 executor validates the pre-intent inspection, authorizes and consumes
  the action, persists the candidate, then proceeds to provider I/O. It does not
  reassert that the post-intent checkpoint is nonterminal before call-entry.
- Public lifecycle code classifies `FINAL_QA_REQUIRES_REVIEW` as terminal.

These facts explain how a single command can produce a terminal-looking native
status and then create durable provider custody. The retained workspace is still
needed to establish the exact generation-18 action/intent/result/snapshot join.

## Predicate Paws comparison

Predicate Paws published an immutable `review_required` result and exact command
envelope after its final creative retry was rejected. API then completed typed
terminal closeout. This supports the existence of legitimate native review
terminals but does not make its cause identical to Glimmer's mixed-custody state.

## Slice 1 retained evidence

- Exact access counts: one `HEAD`, one `GET`, zero list/write/delete/provider
  operations.
- Final manifest SHA-256:
  `a066d66ae3fcce3624a4f14b875a168c394238a45b138ed6657344611d3b6681`.
- Archive SHA-256:
  `a53a6a916a530381af500121882a6dd40ce638af974fd261d1c26f09c3e37eb1`.
- Inventory SHA-256:
  `bda5e1bd10527ed454b636a0a1442284f1d39b5e4f43552bb6e086b675ee1717`.
- Strict restore: 1022 members; 22,723,480 uncompressed bytes; generation 18.
- Native revision 104 joins outer `FINAL_QA_REQUIRES_REVIEW` to live polish
  intent `PROVIDER_PENDING`, durable `resp_0adb…`, and zero retrieval attempts.
- The native-result index has no terminal-review result for Glimmer.

The detailed field-level record is in
`SLICE 1 - RETAINED CHECKPOINT FINDINGS.md`; the bounded remote-operation record
is in `SLICE 1 - READ-ONLY R2 ACCESS RECEIPT.json`.

## Slice 4 runtime evidence

- `update_run_status()` now gives precedence to ambiguity and provider custody
  before preserving a final-QA review state or selecting a different prepared,
  authorized, or budget-blocked action.
- `dispatch_external_authority_v2_intent()` revalidates under the native writer
  after intent durability and before provider call-entry.
- A contradictory terminal post-intent checkpoint returns the closed v4
  `pre_provider_refusal` result with:
  - `reason = post_intent_lifecycle_contradiction`;
  - `provider_io = not_attempted`;
  - `grant_disposition = refused`; and
  - the complete ordered refused-action inventory.
- The public command wraps that refusal in command-result v3; normal dispatch
  continues to use command-result v2 without widening its frozen shape.
- The immutable refusal history survives replay. The refused grant cannot be
  reused, and a newly exported request plus fresh grant can establish a later
  intent.
- Provider-pending polish remains nonterminal and reconciliation-selected;
  providerless authorized polish remains nonterminal; call-entry ambiguity
  remains ambiguity; no-custody final-QA warning remains terminal.
- Mixed inventories prove provider custody plus a different prepared or
  budget-blocked action selects reconciliation; after custody clears, the
  remaining fact regains its ordinary projection.
- Focused matrix: 123 passed, 5 expected optional-schema skips.
- External network/provider calls and spend: zero. The tests use only scripted
  adapters; the post-intent refusal cases prove zero scripted creates.

## Current gate

Slice 2 freezes the evidence-backed causal and contract decision in
`SLICE 2 - CAUSAL MATRIX AND CONTRACT FREEZE.md`.

Slice 3 freezes the executable counterexample in
`SLICE 3 - PROVIDER-FREE PRODUCTION-BOUNDARY REPRODUCTION.md` and
`tests/test_final_qa_mixed_custody_slice3.py`.

Current focused result: 123 passed, 5 expected optional-schema skips. External
provider calls and spend: zero. Scripted local create count in the original
public CLI counterexample: one; corrected post-intent refusal create count:
zero.

Slice 5 packages the provider-free public receipt and consumer handoff. Source
matrix: 131 passed, 6 expected optional-schema skips. Installed wheel:
`6690df42a4d35c99b93bb4118ed62f1f2dad56c9c07f05209f4439bb2ebc0fa6`.
Stable receipt:
`99ef5eccde34a370fb918d5cb6361244131b44e007029293c229ae4878704adf`.

Paused at Voof-paws 6. Generation 17 access is not needed. No retained-run
recovery/mutation, external network, real provider work, or spend occurred.

## Slice 6 release-candidate evidence

- Version frozen before broad testing: 0.4.35.
- Broad suite: 945 tests run; 49 expected skips; 3 boundary-expectation
  failures. No full-suite repetition after correction.
- Directly affected post-correction matrix: 31 passed.
- Final deterministic wheel SHA-256:
  `830a4cd9288628c399a79f9d255edbb49caa5ab608046af6f12cfec8bbe34cfb`
  (two byte-identical builds).
- Final installed mixed-custody receipt SHA-256:
  `a9123f0d8f09d66083209db2573f99937f63c95917ef11e989fcb2d1f6e59599`
  (two identical runs).
- Installed `pip check`, generic release smoke, terminal-review qualification,
  JSON Schema validation, and Python semantic validation: pass.
- Final candidate external provider/network calls, spend, R2 access, and
  retained-run access: zero.

Final gate complete: API and owner approved release; SBE `0.4.35` is published.

## Publication evidence

- Source commit: `e73b057e`.
- Tag: `astrowoof-natal-authoring-v0.4.35`.
- Release:
  `https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.4.35`.
- Public asset: `astrowoof_natal_authoring-0.4.35-py3-none-any.whl`.
- Size: `1136408` bytes.
- GitHub asset digest and downloaded SHA-256:
  `830a4cd9288628c399a79f9d255edbb49caa5ab608046af6f12cfec8bbe34cfb`.
- Release is public, non-draft, and non-prerelease.
