# Provider Reconciliation Precedes External Authority — Evidence

## Planning evidence

- Fresh QA cohort contained two six-member initial waves.
- OpenAI dashboard observation indicated all twelve submitted structured responses
  were available.
- API authoritative records retained mixed `reported` and `provider_created`
  action states for both waves.
- SBE trace evidence recorded a defer to external-authority wait with remaining
  provider-created dependencies.

These observations establish the selector-ordering question only. They are not a
license to mutate the cohort or to treat dashboard observations as lifecycle
authority.

## SBE planning assessment

- Current selector evidence indicates due reconciliation already precedes prepared
  authority.
- Candidate defect: prepared authority precedes scheduled/not-due provider custody
  and completed-provider evidence requiring local fan-in.
- This remains a hypothesis until Slice 0 reproduces it through public lifecycle
  and temporal inspection.
- Planning changed no runtime, schema, provider, spend, or retained workspace.

## Next-release compatibility baseline

- Project dependency: `semantic-projection-core==0.11.1`.
- Bounded admission runtime pin: SPC 0.11.1.
- Next release manifest requirement: exact SPC 0.11.1.
- Published 0.4.21 manifest remains unchanged and accurately records SPC 0.11.0.

## API plan approval

- Review: `API AGENT PLAN REVIEW.md`.
- Verdict: approved to begin provider-free Slice 0.
- Existing lifecycle v0.5/temporal v0.6 are the preferred compatibility target.
- No API code/schema change is expected if corrected inspection preserves existing
  command and `not_before` semantics.
- Runtime implementation remains unstarted pending Slice 0 API review.

## Slice 0 evidence

- Result: `results/SLICE 0 - PUBLIC SELECTOR AUDIT AND PRECEDENCE CONTRACT.md`.
- Reproducer:
  `astrowoof_natal/tests/test_provider_reconciliation_precedes_authority_slice0.py`.
- Focused result: 4 tests passed.
- Routes: exact Natal interactive and bounded Natal interactive.
- Public readers: lifecycle inspection v0.5 and temporal lifecycle v0.6.
- Observed current defect:
  - due provider custody + prepared → reconciliation (correct baseline);
  - not-due provider custody + prepared → authority (incorrect);
  - completed provider evidence + prepared → authority (incorrect).
- Secondary symptom: time-only not-due → due currently changes the v0.6 basis
  because the not-due branch embeds authority inventory and the due branch does not.
- Authoritative workspace hashes remained unchanged across every inspection.
- Provider POST/create/submit/retry/GET calls: 0.
- Authorization/grant consumption: 0.
- Frozen QA cohort access/mutation: 0.
- Source/schema/runtime changes: none.

## Slice 1 evidence

- API approval: `API AGENT SLICE 0 REVIEW.md`.
- Contract:
  `results/SLICE 1 - PRECEDENCE CONTRACT AND SEMANTIC VALIDATION.md`.
- Lifecycle v0.5 closed failures:
  - `retained_provider_custody_precedes_authority`;
  - `provider_fan_in_precedes_authority`.
- Temporal v0.6 independently refuses an authority request over retained custody,
  even when all digests are recomputed.
- Genuine authority-only observations retain a stable request digest across trusted
  observation time.
- Focused result: 28 tests passed; 1 optional `jsonschema` check skipped.
- Provider I/O, create, retrieval, authorization consumption, and frozen-QA access:
  0.
- Runtime selector change: none; current contradictory mixed branches fail closed
  pending Slice 2.

## Slice 2 evidence

- Shared selector now orders retained provider truth before prepared authority.
- Exact and bounded not-due mixed states select ineligible
  `provider_reconciliation_cycle` with native `not_before`.
- Exact and bounded due mixed states select only the first four native due members.
- Completed-provider evidence selects `ordinary_resume` before authority.
- Time-only not-due → due keeps one v0.6 checkpoint basis and absent authority
  inventory.
- Focused result: 70 tests passed; 1 optional schema check skipped.
- Provider create/retrieval, authorization consumption, and frozen-QA access: 0.

## Slice 3 evidence

- Installed qualification surface: `astrowoof-provider-pending-qa`.
- One workspace owns six provider identities plus one later prepared action.
- Retrieval cardinality: first cycle 4; second cycle 2; unique total 6.
- Prepared authority before completion/fan-in: absent.
- Second-cycle completed-evidence branch: `ordinary_resume`.
- Post-fan-in branch: `await_external_authority`, containing only the prepared ID.
- Provider transport is scripted and local; external network/spend: 0.
- Focused result: 34 tests passed.

## Slice 4 evidence

- Route matrix:
  - exact Natal interactive Response: pass;
  - bounded Natal interactive Response: pass;
  - exact Natal Batch: pass;
  - bounded Natal Batch: pass.
- Batch authority remains one provider action/round; no member-level reservation
  authority was introduced.
- Supported interactive stage matrix: initial, retry, polish, critic, candidate.
- Ordinary optional-stage Batch dispatch remains explicitly unsupported/refused.
- Focused result: 13 tests passed.
- Provider/network/spend and frozen-QA access: 0.

## Slice 5 evidence

- Handoff: `PROVIDER CUSTODY PRECEDENCE API HANDOFF.md`.
- Installed command: `astrowoof-provider-pending-qa`.
- Candidate wheel SHA-256:
  `730315cbbd4cd78fbc592c74e3d7021c8aad7b0cddf8d0ee07fa03418a9b55fb`.
- SPC 0.11.1 wheel SHA-256:
  `fd8b9be60c91f7f102164c45fcf2f89c814f808b334b3c08136f683f1c2b8b5b`.
- Receipt SHA-256:
  `271743902a49eb16ea1be23c3d44f86dc9b15cb877fb6f30e2ca7a61bfc63741`.
- Receipt status: pass; create count 6; retrieval count 6; retrieval waves 4+2.
- Post-fan-in authority inventory: exactly one later prepared action.
- External network/provider/spend/frozen-QA activity: 0.

## Slice 6 evidence

- Artifact source commit: `f68c7ac0d161f8bac81a72e01824d18d7627a88f`.
- Full source suite: 700 passed; 36 expected skips.
- Reproducible build epoch: `1787649544`.
- Candidate A/B wheel bytes: 970685 each.
- Candidate A/B SHA-256:
  `5ead8d317d81bbcc5c38132c3b81d2ca380911088f4b8c6866dc3f333003f47d`.
- Exact installed SPC: 0.11.1; qualified local wheel SHA-256
  `fd8b9be60c91f7f102164c45fcf2f89c814f808b334b3c08136f683f1c2b8b5b`.
- Installed `pip check`: pass.
- Installed `astrowoof-provider-pending-qa`: pass.
- Installed `astrowoof-release-smoke --require-installed`: pass.
- Resource count: 102; resource-set SHA-256
  `7bb74f04a466cfa5d28c248e3c411f97c61221770a3eba1556544710d6c0775c`.
- External provider/network calls, spend, and frozen-QA access/mutation: 0.
- Fresh API/worker release-pair qualification remains required before paid QA.

## Publication evidence

- Immutable tag: `astrowoof-natal-authoring-v0.4.22`.
- Tag commit: `de28857172fb7c0b981ff716b34eaade80c5ba70`.
- Annotated tag object: `0ce01c82173b5ee7ddfd8c9a9c4f52cb75f7a6dd`.
- GitHub release ID: 376291418.
- Published at: `2026-08-25T09:37:57Z`.
- Wheel asset ID: 528966202; checksum asset ID: 528966203.
- GitHub-reported and independently downloaded wheel SHA-256:
  `5ead8d317d81bbcc5c38132c3b81d2ca380911088f4b8c6866dc3f333003f47d`.
- Published bytes: 970685; draft: false; prerelease: false.
