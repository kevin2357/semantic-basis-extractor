# Evidence Index

- Fresh QA run reached `await_external_authority` with
  `astrowoof.external_authority_request.v2` after supported provider
  reconciliation.
- API source fails closed for v2 rather than constructing a v1 grant.
- SBE temporal lifecycle handoff explicitly says v2 identity/joining is
  qualified while constrained v2 execution remains a separate compatibility
  decision.
- QA worker suspension is an operational containment measure, not authority to
  mutate or resume retained provider work.
- Detailed PLAN.md received joint approval and Slices 0–2 are implemented.
- Owner/API plan approval received. Slice 0 contract and lineage audit authorized;
  no provider or retained-workspace operation is authorized.
- Slice 0 public reproducer:
  `test_external_authority_v2_execution_gap.py`.
- Slice 0 audit:
  `SLICE 0 - CONTRACT LINEAGE AND APPLICABILITY AUDIT.md`.
- Expected native branch: ordinary v2 request, awaiting authority, ineligible now,
  no local work, no due retrieval subset, no `not_before`.
- Existing CLI outcome: typed parser refusal before state/provider work because the
  released external-authority executor is fixed to six-member v1 initial waves.
- Provider calls/retrievals/spend/retained-run mutation: **0**.
- Slice 1 proposal:
  `SLICE 1 - V2 GRANT AND DISPATCH CONTRACT PROPOSAL.md`.
- New packaged schemas: v2 grant and v2 passive dispatch result.
- New packaged fixture: `external-authority-v2/ordinary-action-set.v1.json`.
- Focused Slice 0–1 plus temporal lifecycle result: **33 tests passed** in the
  schema-enabled environment; the lean environment also passed with two expected
  optional-schema skips.
- Provider/network/credential/spend/native mutation/snapshot publication: **0**.
- API Slice 1 clarification is closed: every grant explicitly carries and validates
  `request_schema_version = astrowoof.external_authority_request.v2`; mutation
  coverage rejects cross-version substitution.
- Slice 2 review artifact:
  `SLICE 2 - ATOMIC INTENT FENCE REVIEW.md`.
- Slice 2 public implementation:
  `external_authority_v2_execution.py` and the packaged
  `external-authority-intent-result.v2.schema.json`.
- Focused Slice 0–2 plus temporal lifecycle result: **40 tests passed** with JSON
  Schema enabled.
- Failure injection proves byte-identical refusal before persistence and a complete
  but snapshot-invalid unit in the state/snapshot interruption window.
- Provider/network/credential/spend/retained-workspace operations: **0**.
- Next gate: API review before Slice 3 provider dispatch.
- Slice 3 review artifact:
  `SLICE 3 - PROVIDER DISPATCH REPLAY AND QUIESCENCE REVIEW.md`.
- New packaged result:
  `astrowoof.external_authority_provider_dispatch_result.v2`.
- Focused Slice 0–3 plus temporal lifecycle result: **50 tests passed** with JSON
  Schema enabled.
- Provider callback writer-release, per-ID durability, pre-entry resume, entered
  ambiguity, competing dispatcher, cursor recovery, duplicate identity, exact
  replay, reconciliation selection, and sink-failure cases all passed.
- Real provider/network/credential/spend/retained-workspace operations: **0**.
- Next gate: API review before Slice 4 route qualification.
- Slice 4 review artifact:
  `SLICE 4 - ROUTE AND HOLISTIC LIFECYCLE QUALIFICATION REVIEW.md`.
- Same-workspace exact and bounded traces each prove six initial creates, real 4+2
  reconciliation, v2 grant/intent/dispatch, durable identity, and reconciliation
  selection.
- All four ordinary Response stages pass on exact and bounded routes.
- Optional/ordinary v2 Batch refuses before mutation and provider work; existing
  initial exact/bounded Batch mechanisms remain passing and unchanged.
- Focused Slice 0–4 plus deployed/pending qualification result: **59 tests passed**.
- Real provider/network/credential/spend/retained-workspace operations: **0**.
- Next gate: API review before Slice 5 installed-wheel packaging and handoff.
- Slice 5 consumer handoff:
  `EXTERNAL AUTHORITY V2 EXECUTION CONSUMER HANDOFF.md`.
- Slice 5 readiness review:
  `SLICE 5 - PACKAGING AND RELEASE READINESS REVIEW.md`.
- New console boundaries: `astrowoof-external-authority-v2` and
  `astrowoof-external-authority-v2-qa`.
- Source v2 qualification receipt: pass, including exact/bounded 4+2, all four
  Response stages, next reconciliation selection, and deliberate Batch refusal.
- CLI source tests prove passive nonmutation, external-only output, constrained
  create, closed result, and zero-create exact replay.
- Real provider/network/credential/spend/retained-workspace operations: **0**.
- Two deterministic candidate builds are byte-identical at SHA-256
  `0e1d127c782a19f997eeb70b51ed615b58affc32435bd42542e3f24b289c621b`.
- Installed candidate import resolved inside the isolated virtual environment.
- `pip check`: pass.
- Generic installed-wheel smoke: pass.
- Installed provider-free v2 qualification: pass; receipt SHA-256
  `5eb7d1ef2fdbd7d1c0e9daae66ae665f667dc9bfc5ba2a83342cbbe8948ab950`.
- Complete suite execution: 655 tests exercised; 654 passed, 35 expected skips,
  and one Windows-only CRLF-versus-canonical-LF frozen-hash assertion failed.
  The test-only canonicalization correction passes its focused regression.
- Qualification receipt proves exact/bounded 4+2, all four ordinary interactive
  Response stages, reconciliation-only observation, and deliberate ordinary-Batch
  refusal.
- Real provider creates/retrievals, external network, credentials, spend, and
  retained-QA workspace access: **0**.
- No version bump, tag, or publication has occurred. Final API/owner release review
  remains the gate before a fresh-version rebuild from committed source.
- Final API/owner review: approved for `0.4.20` after duplicate-definition cleanup.
- Duplicate public command-result definitions and duplicate lexical predicate:
  removed; no contract or runtime behavior change.
- Post-cleanup fast source gate: **33 passed; 2 optional-schema skips**.
