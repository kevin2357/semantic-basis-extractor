# Evidence index

- SBE assessment: `Diffie-Hellman Key Exchange - SBE Agent Notes on
  Diffie-shaped seam.md` in API Sprint 58.
- Retained evidence ceiling and public lifecycle availability work: SBE sprint
  `20260830-retry-external-authority-v2-dispatch-handoff-sprint1`.

This sprint will first inventory the provider-free public fixture and reader
evidence already released in 0.4.31. It will add package material only if the
joint contract freeze proves that evidence insufficient.

## Slice 1

- Contract inventory and exact predicate:
  `SLICE 1 - PUBLIC CONTRACT INVENTORY AND UPGRADE PREDICATE.md`
- Source-compatible v0.5 characterization:
  `astrowoof_natal/tests/test_retry_external_authority_v2_handoff_slice0.py`
- v0.7 runtime and progress evidence:
  `astrowoof_natal/tests/test_post_fan_in_retry_runtime_slice2.py`
- v0.8 lineage/custody contract and runtime evidence:
  `astrowoof_natal/tests/test_retry_lineage_contract_slice3.py` and
  `astrowoof_natal/tests/test_retry_lineage_runtime_slice4_5.py`
- Released package version under inventory: `0.4.31`.
- Focused provider-free gate: 26 tests passed across the legacy handoff
  characterization, v0.7 runtime/progress, and v0.8 lineage contract/runtime
  suites.
- Provider calls, retained-QA reads/mutations, and source/package changes during
  Slice 1: zero.

## Slice 2

- Same-checkpoint witness and precedence finding:
  `SLICE 2 - SAME-CHECKPOINT WITNESS AND PRECEDENCE FINDING.md`
- Regression:
  `test_legacy_upgrade_witness_joins_v05_v07_v08_on_one_checkpoint` in
  `astrowoof_natal/tests/test_retry_external_authority_v2_handoff_slice0.py`.
- Focused legacy/v0.7/v0.8 matrix: 27 tests passed.
- Provider transport calls and retained-QA access/mutation: zero.
- Runtime/schema/package-resource changes: zero; test and sprint evidence only.

## Slice 3 activation

- API review/request:
  `API REVIEW - SLICE 2 SAME-CHECKPOINT WITNESS.md`.
- Approved scope: additive packaged public fixture, strict validator/schema,
  qualification CLI, concise receipt, tests, and package metadata only.
- Provisional release class: lean package-only patch; full runtime suite omitted
  only if the final scope audit proves no production runtime change.

## Slice 3 implementation

- Contract: `SLICE 3 - PACKAGED QUALIFICATION CONTRACT.md`.
- Consumer handoff: `SLICE 3 - API CONSUMER HANDOFF.md`.
- Source: `astrowoof_natal_authoring/legacy_local_work_upgrade_qa.py`.
- Packaged fixture/schemas: `resources/fixtures/legacy-v05-local-work-upgrade-*`
  and `resources/contracts/legacy-v05-local-work-upgrade-*`.
- Focused suite after API-review hardening: 9 passed, 1 optional-schema skip.
- Combined legacy/v0.7/v0.8/qualification matrix: 36 passed, 1 optional-schema
  skip.
- Rehashed mutation coverage derives and protects the embedded v0.5 seam,
  local source-action projection, retained/due custody projection, and conflict
  outcome.
- Reproducible source-tree receipt SHA-256:
  `aaa8792054996520e9eb8d0f145b693c96b7de3f871b277f9e63d3f31bb790ea`.
- Provider create/retrieve/network/spend: zero.
- Production runtime semantic changes: zero.

## Slice 4 lean release candidate

- Candidate version: `0.4.32`.
- Deterministic wheel SHA-256:
  `c45cd46ff4d7ffa98024b662c55f840e8f7cbea9682d32e97273f6e451493d6e`.
- Installed SBE/SPC identity: `0.4.32` / `0.11.1`.
- Installed `pip check`: pass.
- Installed generic release smoke: pass.
- Installed qualification receipt SHA-256, reproduced twice:
  `2401cba4fbf18c21238b34508d28494ad23067033ecfbd072ed256455a9800b1`.
- Release-shaped focused matrix: 36 passed, 1 optional-schema skip.
- Full runtime suite: deliberately not run under the approved package-only lean
  gate; no full-suite pass is claimed.
- Provider create/retrieve/network/spend and retained-QA access: zero.
- Candidate review: `SLICE 4 - LEAN RELEASE CANDIDATE REVIEW.md`.

## Publication

- Release source: `d6515af87591e60836c4992415665d07401d29e4`.
- Tag: `astrowoof-natal-authoring-v0.4.32`.
- Published wheel SHA-256, independently downloaded and verified:
  `c45cd46ff4d7ffa98024b662c55f840e8f7cbea9682d32e97273f6e451493d6e`.
- Publication record: `POST-RELEASE - 0.4.32 PUBLICATION EVIDENCE.md`.
