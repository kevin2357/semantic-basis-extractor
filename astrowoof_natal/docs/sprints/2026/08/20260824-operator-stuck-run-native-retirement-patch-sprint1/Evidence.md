# Evidence

Record contract fixtures, native-transition tests, packaged-release verification,
and the API handoff here.

## Planning evidence

- Repository branch: `main`.
- Starting release: immutable SBE 0.4.18.
- API source reviewed: API Sprint 38 stuck-run terminal retirement documents.
- Plan covers ownership, eligibility, refusal, dry-run, mutation, replay,
  interruption, packaging, and joint-QA gates.
- Runtime/source/schema changes: 0.
- Provider operations/network/credentials/spend: 0.
- Retained QA workspace access/mutation: 0.

## Slice 1 evidence

- Public Python surface:
  `build_operator_retirement_request`, `assess_operator_retirement`,
  `validate_operator_retirement_request`,
  `validate_operator_retirement_assessment`, and
  `read_operator_retirement_schema`.
- Public CLI: `astrowoof-operator-retirement schema|build-request|dry-run`.
- Contract SHA-256:
  `7ae51b5a85d2787861c28b033cab35bdf1201b656795a86674d8cdca73deb866`.
- Eligible request fixture SHA-256:
  `744cce7f2e41636b4c1e9761b971b9ee833ef839c11d58a49377192d7b00635d`.
- Eligible assessment fixture SHA-256:
  `95ab1e7191b6949919b70db8b16cdc1cf584e3721e17c03976a34a198606ef17`.
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_operator_retirement_contract
  astrowoof_natal.tests.test_lifecycle_inspection
  astrowoof_natal.tests.test_lifecycle_contracts
  astrowoof_natal.tests.test_native_transitions`.
- Result: 66 passed; one optional schema test skipped because the lean interpreter
  lacks `jsonschema`. Strict Python validation ran in every environment.
- Dry-run authoritative mutation: 0.
- Provider operations/network/credentials/spend: 0.
- Retained QA workspace access/mutation: 0.
- Status: Slice 1 complete; API review required before Slice 2.

## Slice 2 evidence

- Native transition schema SHA-256:
  `3b782f1b48dd3cbecf2f6c30a32b7a773b084bddf2ad7c2359d703dce6df6057`.
- Lifecycle schema SHA-256:
  `5290a9db3521e8c547672d773c403920fd17d5b9511ee17595be47c670ffcf51`.
- Applied execution proves status/cause, revision advance, complete snapshot,
  journal range, immutable native result, publication receipt, request/closure
  projection, and freshly derived false continuation assertions.
- Refused execution proves unchanged authoritative workspace bytes and no native
  publication.
- Focused retirement/lifecycle/native-transition result: 70 passed, two optional
  `jsonschema` checks skipped; strict Python validators ran.
- Provider I/O, credentials, retrievals, submissions, and spend: 0.
- Retained QA workspace access/mutation: 0.
- Status: Slice 2 complete; review before replay/failure-injection Slice 3.

## Slice 3 evidence

- Exact replay: same native result and receipt; zero changed authoritative bytes.
- Compatible later request: `already_retired`, separate current/original request
  digests, original native seal reused.
- Injected interruption points: after state persistence, after transition snapshot,
  after native publication, and during receipt publication.
- Safe recovery creates exactly one native result and one receipt.
- Unrelated workspace bytes prevent interrupted-state recovery.
- Concurrent second writer is excluded; exactly one transition/result exists.
- Failing typed-event sink does not affect status, seal, or provider behavior.
- Protected audit sentinel absent from captured events and logs.
- Execute-time revalidation race: a post-request `SUBMITTING` action yields
  `provider_ambiguity_present`, `not_retirement_quiescent`, and
  `stale_observation`; authoritative workspace bytes remain identical and no
  native result/receipt is published.
- Focused result: 79 passed, two optional `jsonschema` checks skipped.
- Provider I/O/network/credentials/spend: 0.
- Retained QA workspace access/mutation: 0.
- Status: Slice 3 complete; installed-wheel/API handoff Slice 4 is next.

## Slice 4 evidence

- Installed qualification command:
  `astrowoof-operator-retirement-qa --require-installed`.
- Candidate wheel SHA-256:
  `e084e085bf090a5358d934e37bc6aea435ae3448f96bc625e3746f5e77d6e2bc`.
- Qualification schema SHA-256:
  `97e4d84894e171204cc9aeb9a7a006cd98410bd9347d4338b2276500afb9fc7d`.
- Qualification receipt internal SHA-256:
  `e247fbb47f66a3a5876d500bb7bd0c41e82cbc42a0f214034193c61022903240`.
- Qualification receipt file SHA-256:
  `11d21558e908b4661250e3764e033ce720c51272f136c91ac09b6cef35a29a2b`.
- All eleven closed qualification checks passed.
- Focused result: 82 passed, three optional `jsonschema` checks skipped.
- Provider I/O/network/credentials/spend: 0.
- Retained QA workspace access/mutation: 0.
- Candidate uses version 0.4.18 solely for pre-release review. A fresh patch version
  and final committed-source wheel remain Slice 5 work.
- Status: Slice 4 complete; final API review required before release preparation.

## Slice 5 release-preparation evidence

- API Slice 4 approval: received; independent focused result 29 passed with three
  expected optional-schema skips.
- Release version: 0.4.19 (fresh immutable patch candidate).
- Complete source suite: 623 passed; 33 environment/opt-in skips.
- Artifact-source commit:
  `3151c4fc15d1436e0c250228c2069e4771be30da`.
- Fixed build epoch: `1787615331`.
- Two byte-identical 909960-byte wheels; SHA-256:
  `6ccc2a5ba859830e60f9139e4e52e9795602dff30569c1dbb6ba9579b2f38f79`.
- Generic installed release smoke: pass.
- Installed operator-retirement qualification: pass; receipt SHA-256:
  `37ff37dd42a0a5cc593ddf10bf645a456904d0f241ae11d5be74ab904f3c413f`.
- Provider I/O/network/credentials/spend: 0.
- Retained QA workspace access/mutation: 0.
- Immutable tag: `astrowoof-natal-authoring-v0.4.19` at
  `10dadc5e4d4f259a07643c2ccea869239a9902b7`; annotated tag object
  `9e7104cc87b030fb9e6f8fa3fcb92229af1aaa6e`.
- GitHub release: 376056805, published `2026-08-24T23:59:08Z`.
- GitHub-reported and independently downloaded wheel digests both match the
  qualified SHA-256 exactly.
- Status: Slice 5 and sprint complete; SBE 0.4.19 published and verified.
- Status: Slice 0 contract candidate complete; API review required before Slice 1.

## Slice 0 evidence

- Current code path: `lifecycle._local_dependencies()` maps
  `AWAITING_SPEND_AUTHORIZATION` to `retry_preparation` without consulting action
  cardinality; `_capacity_and_custody()` consequently selects local continuation.
- Sanitized provider-free characterization:
  `results/retirement-quiescence-characterization.json`.
- API-owned pre-invocation custody expectation:
  `results/api-custody-fence-expectation.json`.
- Contract proposal: `OPERATOR RETIREMENT CONTRACT PROPOSAL.md`.
- Runtime/source/schema changes: 0.
- Provider operations/network/credentials/spend: 0.
- Retained QA workspace access/mutation: 0.
