# Terminal Review Closeout Handoff Sprint 1 Evidence

## Planning evidence

- Incident source: `BACKGROUND.md`.
- Affected SBE release: `0.4.27`.
- Existing result schema: `astrowoof.native_execution_result.v0.1`.
- Existing receipt schema: `astrowoof.native_publication_receipt.v0.1`.
- Existing ordinary exact CLI source contains an intended
  publish-result-before-`SystemExit(2)` sequence.
- Retained QA trace reports no terminal publication events and leaves the prior
  result at `provider_pending`.
- Existing execution result includes action IDs and provider-operation projections,
  but Slice 0/1 must determine whether that is strict and complete enough for mixed
  custody settlement.
- External provider calls/spend performed during planning: 0.
- Retained QA workspace access/mutation during planning: 0.

Status: planning evidence only; no runtime conclusion or release recommendation.

## Slice 0 evidence

- Test module:
  `astrowoof_natal/tests/test_terminal_review_closeout_handoff_slice0.py`.
- Public exact ordinary-resume boundary: exercised through `closure.main()`.
- Already-review-required result: sealed before exit 2.
- Prior `provider_pending` result followed by mixed-custody `review_required`:
  two immutable ordered result identities; successor reader validation passed.
- Native publication event precedes the command-result envelope.
- Result v0.1 gap: provider-operation entries are not each strictly action-joined,
  and no complete per-action terminal disposition is projected.
- Read-only API source finding: ordinary resume does not immediately call sealed
  native transition ingestion; later `retain_for_review` deliberately bypasses
  terminal ingress.
- Focused plus adjacent suites: 29 passed in 7.580 seconds.
- External provider/network calls: 0.
- Provider creates/retrievals: 0/0.
- Spend: USD 0.
- Retained QA access/mutation: 0.

Status: Slice 0 complete; causal review pending before contract work.

## Slice 0 API review and retained-checkpoint preflight

- API review record: `API SLICE 0 REVIEW.md`.
- Review conclusion: current evidence points to an API ordinary-resume ingestion
  gap; retained checkpoint inspection is needed before making a claim about the
  exact live SBE publication bytes.
- QA database preflight established for both exact jobs:
  job failed/inactive; no active lease; local continuation false; capacity
  released; workspace registration retained.
- Duchess active checkpoint:
  generation 13; archive bytes 4,054,594; native lifecycle status
  `AWAITING_SPEND_AUTHORIZATION`; archive and inventory SHA-256 recorded in the
  protected database row.
- Pippin active checkpoint:
  generation 12; archive bytes 4,014,784; native lifecycle status
  `AWAITING_SPEND_AUTHORIZATION`; archive and inventory SHA-256 recorded in the
  protected database row.
- Read surfaces accessed: QA lifecycle/job/workspace/checkpoint database metadata;
  the two exact R2 checkpoint objects; checkpoint manifests; native result index;
  indexed sealed results and receipts; retained snapshot/basis identities; current
  snapshot identity; and native journal metadata/records.
- SSH result: Render instance discovery succeeded; authentication failed because
  no matching local private key or SSH-agent identity was available.
- R2 validation: both archive byte sizes and SHA-256 identities match the protected
  checkpoint rows; both manifest generations and complete inventory SHA-256 values
  match; all accessed members match their declared hashes.
- Duchess: 796 declared members, 11 sealed results, 98 native journal records.
  Latest sealed result is `ordinary_authoring / provider_pending /
  provider_operation_pending`, with 10 action IDs and eight provider projections.
- Pippin: 789 declared members, 10 sealed results, 95 native journal records.
  Latest sealed result is `ordinary_authoring / provider_pending /
  provider_operation_pending`, with 10 action IDs and eight provider projections.
- Neither result index contains a `review_required` outcome. Every indexed result
  has a digest-valid receipt joined to its result digest and retained snapshot
  identity.
- Sanitized report:
  `C:\tmp\sbe-terminal-review-retained-metadata.json`.
- Temporary checkpoint ZIPs, inspection script, and all four User-scoped R2
  credential variables were removed after inspection.
- External provider/network calls: 0 provider calls (Render control-plane and
  PostgreSQL metadata reads only).
- Provider creates/retrievals: 0/0.
- Workspace resume/reconciliation/repair/write/delete: 0/0/0/0/0.
- Spend: USD 0.

Status: retained metadata inspection complete. It proves a live-route native
publication gap alongside the independently identified API ingestion gap; Slice 1
contract work is authorized.

## Slice 1 evidence

- Contract proposal:
  `TERMINAL REVIEW AND MIXED CUSTODY CONTRACT PROPOSAL.md`.
- Public identity: `astrowoof.native_execution_result.v0.2`.
- Packaged schema:
  `resources/contracts/terminal-review-result-v0.2.schema.json`.
- Public Python surface:
  `build_terminal_action_dispositions`, `build_terminal_review_result_v02`,
  `validate_terminal_review_result_v02`,
  `validate_terminal_review_result_v02_against_receipt`, and
  `read_terminal_review_result_v02_schema`.
- Focused contract module:
  `astrowoof_natal/tests/test_terminal_review_contracts.py`.
- Verified mixed reported/provider-pending/providerless-authorized inventory,
  exact ledger ordering, canonical inventory digest, custody finality/subsets,
  false create permission, exact invocation/receipt join, schema packaging, and
  Python-only rejection of malformed and rehashed contradictions.
- Focused plus adjacent suites: 57 passed in 5.96 seconds.
- External provider/network calls: 0.
- Workspace mutation/resume/reconciliation/repair: 0/0/0/0.
- Spend: USD 0.

Status: Slice 1 complete; API schema/authority review required before Slice 2.

## Slice 1 API review correction evidence

- Review record: `API SLICE 1 REVIEW.md`.
- Duplicate public imports/exports and duplicate validator blocks: removed.
- Canonical receipt compatibility:
  `validate_native_publication_receipt()` validates the exact closed v0.1 receipt
  against historical result v0.1 or review-only result v0.2.
- API immutable action join:
  `validate_terminal_review_result_v02_against_api_actions()` recomputes each
  complete binding digest and joins native run, action, route, stage, and provider
  operation.
- Consumer-critical mutations covered: valid-looking wrong binding digest basis,
  wrong provider operation, wrong result schema, and mismatched result identity.
- Focused plus adjacent suites: 59 passed in 5.68 seconds.
- AST singular-definition check: pass.
- `git diff --check`: clean apart from Windows line-ending notices.

Status: API-approved for exact-interactive Slice 2 only.

## Slice 2 exact-interactive runtime evidence

- Runtime boundary: public `astrowoof-run-semantic-closure --resume`, exact Natal,
  interactive Responses only.
- Spend-boundary review derivation: fresh v0.7 inspection selects
  `none / retain_for_review` after state and snapshot persistence.
- Publication order: journal transition -> immutable v0.2 result -> full snapshot
  validation -> canonical immutable v0.1 receipt -> `native.result_published`
  event -> exact command-result envelope -> exit 2.
- Command-result schema:
  `astrowoof.terminal_review_command_result.v0.1`.
- Consumer join:
  `validate_terminal_review_command_result_against_publication()` proves the
  transported invocation, result, and receipt are the exact sealed publication.
- Mixed action evidence proves reported actions are terminally accounted and
  providerless authorized actions remain denial-only; new provider creation is
  false.
- Exact API binding validation remains a separate required consumer join through
  `validate_terminal_review_result_v02_against_api_actions()`.
- Focused test groups:
  - terminal-review/native-transition: 33 passed in 4.70 seconds;
  - post-fan-in contract/runtime: 14 passed in 3.62 seconds;
  - post-fan-in routing runtime: 9 passed in 15.46 seconds;
  - composed post-fan-in runtime: 7 passed in 17.91 seconds.
- Total focused/adjacent assertions: 63 passed.
- Singular-definition AST check: pass.
- `git diff --check`: clean apart from Windows line-ending notices.
- Provider creates/retrievals/network calls: 0/0/0.
- Spend: USD 0.
- Retained Pippin/Duchess access or mutation: 0.

Status: Slice 2 exact-interactive gate complete; API review required before
custody-only Slice 3.

## Slice 3 exact-interactive custody evidence

- API review record: `API SLICE 2 REVIEW.md`.
- Public-command three-class witness:
  - reported action -> `terminally_accounted`;
  - durable WAITING Response -> `provider_reconciliation_only`;
  - providerless AUTHORIZED action -> `providerless_denial_only`.
- Sealed result finality: `mixed_resolution_required`.
- Exact ordered reconciliation inventory: one durable provider action.
- Exact ordered providerless-denial inventory: one unused authorized action.
- New provider create permission: false.
- Command result joins its exact v0.2 result and canonical v0.1 receipt.
- Public reconciliation command transport:
  one scripted GET for the exact durable Response ID; no request payload; no POST.
- Completed review-custody response handling:
  usage/cost availability is recorded on the native paid action, the action becomes
  `REPORTED`, and editorial response content is not passed to authoring or
  finalization.
- Providerless denial:
  exact observation/binding request applied through the existing public operation;
  no provider interface is accepted or reachable.
- Closeout after both operations:
  terminal true; provider continuation false; local continuation false.
- Focused/adjacent suites: 120 passed in 19.47 seconds.
- Provider GET/POST/create/retry: 1/0/0/0, all provider-free scripted transport.
- External network/provider calls and spend: 0 / USD 0.
- Retained Pippin/Duchess access or mutation: 0.

Status: Slice 3 complete; API review required before interruption/replay Slice 4.

## Slice 4 interruption, replay, and lineage evidence

- API review record: `API SLICE 3 REVIEW.md`.
- Failure cuts exercised independently:
  `after_journal_appended`, `after_result_written`, `after_snapshot_written`,
  `after_snapshot_validated`, and `after_receipt_published`.
- Every cut converges on one validated v0.2 result and canonical v0.1 receipt.
- A fully appended but unsealed invocation tail is recognized only by its exact
  three-record close, one invocation identity, route/revision join, and matching
  review outcome/cause.
- Exact replay requires unchanged native revision, route, command, review cause,
  and complete ordered action-inventory digest.
- Concurrent finalization: one successful writer, one typed filesystem-lock
  refusal, one result in the index; later replay returns that result.
- Successor continuity:
  - original v0.2 result bytes unchanged and independently readable;
  - successor command kind is `provider_reconciliation`;
  - successor outcome remains `review_required`;
  - successor journal starts at predecessor end sequence + 1;
  - both results retain independently validating receipts.
- Status monotonicity regression proves custody-only persistence cannot turn
  `FAILED_REQUIRES_REVIEW` back into provider-pending or authoring.
- Failing execution-event sink does not alter publication.
- Protected sentinel is absent from result, receipt, and bounded journal exports.
- Focused/adjacent suites: 124 passed in 28.27 seconds.
- Broad `test_semantic_closure.py`: 93 passed in 193.48 seconds; one existing
  `PytestReturnNotNoneWarning` for `test_spend_policy`.
- Provider/network calls and spend: 0 / USD 0.
- Retained Pippin/Duchess access or mutation: 0.

Status: Slice 4 complete; API review required before installed/package fixtures.

## Slice 5 installed-wheel evidence

- Public command: `astrowoof-terminal-review-qa`.
- Public Python surface:
  `run_terminal_review_qualification()`,
  `validate_terminal_review_qualification()`, and
  `read_terminal_review_qualification_schema()`.
- Packaged schema: `astrowoof.terminal_review_qualification.v1`.
- Packaged fixture:
  `resources/fixtures/lifecycle/terminal-review-qualification.v1.json`.
- Receipt SHA-256:
  `b6341100d54b0147dbf138d3a1a54043453057a8e23927afbcac6fb451337572`.
- Candidate wheel:
  `astrowoof_natal_authoring-0.4.27-py3-none-any.whl`.
- Candidate wheel SHA-256:
  `c71dcc6ed6ba9d5af7defb1125f3515ff9fa95729f7c29cf0ba6086d142eacd2`.
- Imported runtime:
  `.tmp-terminal-review-slice5/venv/Lib/site-packages/astrowoof_natal_authoring`.
- Installed command result: pass.
- Installed lifecycle smoke with `--require-installed`: pass.
- Focused terminal-review source gate: 21 passed, 3 optional-schema skips.
- Schema-enabled qualification gate: 5 passed with `jsonschema` 4.26.0.
- Public terminal-review sequence:
  exit 2 after validated receipt; one scripted GET; POST/create/retry 0; exact
  providerless denial applied; closeout terminal with no provider/local
  continuation.
- Compatibility and continuity:
  historical v0.1 readable; refused as v0.2; receipt mutation refused; original
  v0.2 result immutable; successor journal contiguous and remains
  `review_required`.
- Receipt reproducibility across fresh private temporary workspaces: byte-identical.
- Protected sentinel in receipt/public evidence: absent.
- Retained Pippin/Duchess access or mutation: 0.
- External network/provider calls and spend: 0 / USD 0.

Status: Slice 5 complete; API fixture/consumer review required before Slice 6.

### API review correction evidence

- Exact deterministic action inventories enforced by the Python validator.
- `successor_outcome=review_required` enforced.
- `providerless_denial_outcome=applied` enforced.
- Recomputed-digest mutations of all five semantic fields: refused.
- Installed-wheel rehashed mutation probe: refused.
- Replacement candidate wheel SHA-256:
  `c71dcc6ed6ba9d5af7defb1125f3515ff9fa95729f7c29cf0ba6086d142eacd2`.
- Qualification receipt remains:
  `b6341100d54b0147dbf138d3a1a54043453057a8e23927afbcac6fb451337572`.

Status: correction complete; API re-review required before Slice 6.

## Slice 6 release-candidate evidence

- Candidate version: 0.4.28.
- Artifact source commit:
  `25e0be9ce670b3643f47f6cdd0a71de7d00ad11e`.
- Fixed build epoch: `1787911516`.
- Strict-schema broad source suite: 860 passed, 3 expected skips, 750.136 seconds.
- Schema mismatch found by the first broad run: post-fan-in inspection-bundle
  operation key expected bare SHA-256 while public runtime identity was
  `work_<24 hex>`.
- Corrected focused gate: 15 passed.
- Candidate A/B wheel bytes: 1,077,913 / 1,077,913.
- Candidate A/B SHA-256:
  `365ab0bc63a03e2c9c06638631b5e47c78ce494331f014741472a3e59fa58fb4`.
- Byte reproducibility: pass.
- Installed runtime path: isolated `site-packages` under
  `.release-0.4.28-installed`.
- Installed generic release smoke: pass.
- Installed lifecycle smoke: pass.
- Installed terminal-review qualification: pass; receipt
  `6289962655c36e4c2cab5828c30499a75155094c0437898c7f68fdf4e0afeb6d`.
- Installed post-fan-in qualification: pass; receipt
  `9085c0a83d615c24163e6268c8ed89fac14a89dce2843ec61bdab8ab51e630f1`.
- Installed adversarial qualification: pass; receipt
  `3f1ee272e9724898acdfa4dff2fa82edbc16cbc144507ed22e351e9956c26e76`.
- Exact dependency: `semantic-projection-core==0.11.1`.
- External provider/network calls and spend: 0 / USD 0.
- Retained Pippin/Duchess access or mutation: 0.
- `git diff --check`: pass after review-record whitespace normalization.

Status: release candidate qualified; final API and owner review approved immutable
tag and publication as SBE 0.4.28.

## Immutable publication evidence

- Tag: `astrowoof-natal-authoring-v0.4.28`.
- Tag target: `b61ea7dcdba1c8769833c46c785db974c88d3c77`.
- GitHub release ID: `378409256`.
- Published at: `2026-08-28T10:23:09Z`.
- Wheel asset ID: `533629996`.
- Published/downloaded wheel SHA-256:
  `365ab0bc63a03e2c9c06638631b5e47c78ce494331f014741472a3e59fa58fb4`.
- Checksum asset ID: `533629994`.
- Checksum asset SHA-256:
  `19e0dba92bd94ae162b6bef942e959adff70338a05034f93f06d7ce4928b2352`.
- Download verification: pass.
