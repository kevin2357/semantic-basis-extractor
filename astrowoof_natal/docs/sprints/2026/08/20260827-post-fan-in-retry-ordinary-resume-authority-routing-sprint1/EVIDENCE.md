# Evidence — Post-Fan-In Retry Ordinary-Resume Authority Routing SBE Sprint 1

## Planning evidence

- Incident background: `Background.md`.
- Analysis: `SBE AGENT PRE-SPRINT HUDDLE.md`.
- Plan: `PLAN.md`.
- Current SBE release observed in incident: 0.4.26.
- Retained QA cohort: suspended and not accessed or mutated by SBE planning.
- External provider/network calls: 0.
- Provider spend: USD 0.
- Runtime/source/schema changes: none.

## Slice 0 evidence

- Findings: `SLICE 0 - INCIDENT REPRODUCTION AND CAUSAL FINDINGS.md`.
- Public runtime characterization:
  `tests/test_post_fan_in_retry_authority_routing_slice0.py`.
- Existing selector characterization retained:
  `tests/test_post_fan_in_retry_matrix_slice0.py`.
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 -v`.
- Result: 7 passed.
- Production source/schema changes: none.
- Retained QA access/mutation: none.
- External provider/network calls: 0.
- Provider create/retrieval calls: 0.
- Spend: USD 0.

- API review: `API SLICE 0 REVIEW.md`.
- API disposition: approved to begin Slice 1.

Status: Slice 0 approved; Slice 1 ready to begin.

## Slice 1 evidence

- Normative contract: `POST-FAN-IN ROUTING CONTRACT AND DECISION MATRIX.md`.
- Closed fixture:
  `fixtures/post-fan-in-authority-routing-matrix.v1.json`.
- Contract validator/mutation coverage:
  `tests/test_post_fan_in_authority_routing_contract_slice1.py`.
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_post_fan_in_authority_routing_contract_slice1 astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 astrowoof_natal.tests.test_post_fan_in_retry_contract_slice1 astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice3`.
- Result: 19 passed; 1 expected optional-schema skip.
- Runtime/source/schema changes: none.
- External provider/network calls: 0.
- Retained QA access/mutation: none.
- Spend: USD 0.

Status: Slice 1 complete; API contract review required before Slice 2.

- API review: `API SLICE 1 REVIEW.md`.
- API disposition: approved for Slice 2 runtime implementation.

## Slice 2 evidence

- Runtime source:
  - `src/astrowoof_natal_authoring/initial_wave.py`
  - `src/astrowoof_natal_authoring/closure.py`
  - `src/astrowoof_natal_authoring/bounded_lifecycle.py`
- Runtime tests:
  - `tests/test_post_fan_in_retry_authority_routing_slice0.py`
  - `tests/test_post_fan_in_retry_routing_runtime_slice2.py`
- Focused route/contract/post-fan-in result: 24 passed.
- Wider initial-wave/external-authority/bounded result: 77 passed.
- External provider/network calls: 0.
- Retained QA access/mutation: none.
- Spend: USD 0.

Status: Slice 2 complete; Slice 3 in progress.

## Slice 3 evidence

- Composed qualification:
  `tests/test_post_fan_in_retry_composed_runtime_slice3.py`.
- Narrative evidence:
  `SLICE 3 - COMPOSED RUNTIME AND FAILURE QUALIFICATION.md`.
- Focused composed/route/failure result: 44 passed.
- Prior wider initial-wave/external-authority/bounded result: 77 passed.
- External provider/network calls: 0.
- Scripted local exact-path retrievals: 1.
- Scripted local exact-path creates: 1.
- Duplicate creates on replay: 0.
- Retained QA access/mutation: none.
- Spend: USD 0.

Status: Slice 3 complete; API review required before Slice 4.

- API review: `API SLICE 3 REVIEW.md`.
- Independent focused result: 19 passed; 1 expected optional-schema skip.
- API disposition: approved for Slice 4 with a required public, provider-free,
  installed-wheel post-fan-in fixture and stable receipt identity.

Status: Slice 3 approved; Slice 4 may begin.

## Slice 4 SBE evidence

- Public fixture:
  `src/astrowoof_natal_authoring/resources/fixtures/post-fan-in-retry-routing.v1.json`.
- Closed receipt schema:
  `src/astrowoof_natal_authoring/resources/contracts/post-fan-in-retry-qualification.v1.schema.json`.
- Public runner/reader/validator:
  `src/astrowoof_natal_authoring/post_fan_in_retry_qa.py`.
- CLI: `astrowoof-post-fan-in-retry-qa`.
- Tests: `tests/test_post_fan_in_retry_qa_slice4.py`.
- Focused result: 5 passed; 1 expected optional-`jsonschema` skip.
- Combined Slice 1–4 result: 25 passed; 1 expected optional-schema skip.
- Scripted local retrievals: 1.
- Scripted local creates: 1.
- Duplicate creates: 0.
- External network/provider calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.

Status: SBE Slice 4 component complete; API joined-campaign review pending.

- API review: `API SLICE 4 REVIEW.md`.
- Reproducibility defect: confirmed and corrected.
- Reproducibility assertion: two independent disposable workspaces produce equal
  phase evidence, endpoint evidence, receipt identity, and receipt value.
- Corrected focused result: 6 passed; 1 expected optional-schema skip.
- Corrected combined result: 26 passed; 1 expected optional-schema skip.

Status: Slice 4 correction complete; API re-review pending.

- API re-review: `API SLICE 4 RE-REVIEW.md`.
- Independent result: receipt, phase evidence, and endpoint evidence reproduce
  exactly across fresh workspaces.
- Disposition: approved for installed-wheel qualification.

Status: Slice 4 approved; Slice 5 in progress.

## Slice 5 SBE candidate evidence

- Candidate source commit: `e1a22ab`.
- Candidate version: `0.4.27`.
- Fixed build epoch: `1787844361`.
- Deterministic wheel A/B size: 1,048,593 bytes each.
- Deterministic wheel A/B SHA-256:
  `ae8da7a7ce64cd83e1a4444fb8a77587eafb1c1f5a7ff1cc3ac615dfb51e611a`.
- Exact installed SPC dependency: `semantic-projection-core==0.11.1`.
- Wheel inventory confirmed:
  - `astrowoof_natal_authoring/py.typed`;
  - `post-fan-in-retry-qualification.v1.schema.json`;
  - `post-fan-in-retry-routing.v1.json`; and
  - console entry point `astrowoof-post-fan-in-retry-qa`.
- Installed generic release smoke: passed with `--require-installed` from an
  external literal `site-packages` tree.
- Installed adversarial qualification: passed.
- Installed post-fan-in qualification: passed twice with byte-identical receipts.
- Installed post-fan-in receipt SHA-256:
  `0db488713ad4711f52431d0a65187d6103f7784e41cd9a2c1d192c5af7eee074`.
- Full source suite: 829 passed in 825.722 seconds; 40 expected skips.
- External provider/network calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.
- Platform status: Windows source/build/installed qualification complete; the
  API/Linux joined campaign against this exact candidate remains the next gate.

Status: SBE Slice 5 component complete; API/Linux candidate review required
before Slice 6 release preparation.

## API Slice 5 review and joined-campaign blocker

- Review: `API SLICE 5 REVIEW.md`.
- Independent installed-candidate disposition: approved for the API joined
  campaign; publication withheld.
- Approved pre-4A wheel SHA-256:
  `ae8da7a7ce64cd83e1a4444fb8a77587eafb1c1f5a7ff1cc3ac615dfb51e611a`.
- Blocker review: `API JOINED-CAMPAIGN BLOCKER REVIEW.md`.
- Blocker classification: public handoff incompleteness, not a runtime regression.
- Missing evidence: closed ordered lifecycle projections that API can validate and
  route through its real translator/persistence/scheduler services.
- Existing receipt status: valid reproducible SBE attestation, insufficient by
  itself as API campaign input.
- Safety totals remain: external provider/network calls 0, spend USD 0,
  retained-QA access/mutation none.

Status: corrective Slice 4A required. The pre-4A candidate is not approved for
publication or deployment; repeat Slice 5 after the packaged projection surface
is complete and reviewed.

## Corrective Slice 4A evidence

- Contract: `astrowoof.post_fan_in_retry_inspection_bundle.v1`.
- Schema: `post-fan-in-retry-inspection-bundle.v1.schema.json`.
- Public CLI selectors: `--inspection-bundle`, `--inspection-bundle-schema`.
- Ordered projections: all seven existing qualification phases, exact order.
- Reproducibility: exact bundle equality across fresh disposable workspaces.
- Semantic mutations: digest and closed phase semantics refuse changes.
- Privacy: no provider IDs/payloads, prompts, native paths/files, credentials,
  protected provenance, or retained-QA evidence.
- Focused result: 9 passed; 1 expected optional-schema skip.
- Adjacent regression result: 20 passed.
- External provider/network calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.

Status: Slice 4A implemented; API projection-bundle review required.

### API Slice 4A receipt-binding correction

- Review: `API SLICE 4A REVIEW.md`.
- Finding reproduced: a rehashed arbitrary receipt reference was previously
  accepted.
- Correction: public validation reconstructs and validates the canonical receipt,
  then requires exact receipt-identity equality.
- Requested fully rehashed wrong-receipt mutation: refused.
- Focused result: 10 passed; 1 expected optional-schema skip.
- Adjacent regression result: 20 passed.
- Provider/network/spend/retained-QA totals remain zero.

Status: Slice 4A correction complete; fresh candidate build and installed
qualification required.

## Fresh post-4A candidate evidence

- Artifact source commit: `9205235`.
- Version: `0.4.27` (unpublished).
- Fixed build epoch: `1787872684`.
- Deterministic wheel size: 1,051,330 bytes.
- Deterministic wheel SHA-256:
  `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`.
- Exact installed dependency: `semantic-projection-core==0.11.1`.
- Installed qualification receipt SHA-256:
  `982f8e3044c7e20a9324d44c61867af5e1787d2d996289ad7fe57aff19e6f2b9`.
- Installed projection bundle SHA-256:
  `75247d8652698e122c46fc79480bbf5b73fd0671b8cb38cb6aa5671eaab2a8a4`.
- Receipt/bundle join: exact match, validated by installed public API.
- Installed adversarial qualification: passed.
- Generic installed release smoke: `DELIVERY_COMPLETE`; cleanup complete.
- External provider/network calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.

Status: fresh post-4A candidate qualified on Windows. API joined campaign must use
the exact wheel digest above; publication and deployment remain withheld.

- API Slice 4A re-review: approved.
- Independent focused result: 10 passed; 1 expected optional-schema skip.
- Joined-campaign pin: replacement wheel SHA-256
  `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`.
- Version-only selection is unsafe because the superseded candidate also carries
  unpublished version `0.4.27`.

Status: awaiting API/Linux joined-campaign evidence; no publication, deployment,
provider work, spending, or retained-QA recovery authorized.

## Slice 5 re-review and Slice 4B request

- API Slice 5 re-review: post-4A candidate independently approved for the joined
  campaign, with publication still withheld.
- Slice 4B request: two representative public real-engine happy-path witnesses.
- Witness scope: exact interactive Response route; existing lifecycle and authority
  contracts only.
- Broad permutation ownership remains with the generated API simulator.
- Downstream-stage identity requires production-path characterization before freeze.
- Post-4A candidate status: valid historical qualification evidence, superseded as
  final campaign input once 4B changes are committed.
- Safety posture remains provider-free, zero-spend, and no retained-QA access.

Status: Slice 4B planned; API review required after both witness artifacts pass.

## Slice 4B characterization evidence

- Route/mechanism: exact Natal / interactive Response.
- Provider-bound retry actions: 2.
- Completion order: later action completed while earlier action remained pending.
- Reconciliation outcome: `progressed_local`.
- Capacity: `continue_local_cycle`, reason `local_work_ready`.
- Incorrect selected command: `none`, reason `terminal_or_no_continuation`.
- Root cause: execution-branch selection requires an older dependency projection
  even though validated custody already proves completed evidence.
- Proposed correction: select `ordinary_resume` for completed provider evidence;
  require v0.7 concrete local work; retain all other provider custody.
- Authority topology: distinct action/binding/grant members, potentially one
  aggregate ordinary-v2 request after both results are consumed.
- External provider/network calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.

Status: API interpretation requested before implementation freeze.

- API interpretation: approved aggregate ordinary-v2 action-set with distinct
  exact members.
- Mixed-custody selector correction: implemented.
- Regression: later action completed, earlier action pending, selected command
  `ordinary_resume`, one exact completed-evidence local operation, both custody
  action IDs retained.

Status: selector correction complete; public happy-path witnesses in progress.

## Slice 4B public witness evidence

Implemented public artifacts:

- `astrowoof.ordinary_v2_happy_path_qualification.v1`
- `astrowoof.ordinary_v2_happy_path_bundle.v1`
- `astrowoof.ordinary_v2_happy_path_fixture.v1`
- `astrowoof-ordinary-v2-happy-path-qa`

Observed source-tree receipt:

- status: `pass`
- witnesses: `two_retries_out_of_order`,
  `retry_then_qualitative_critic`
- scripted retrieval observations: 4
- scripted creates: 3
- duplicate creates: 0
- duplicate local consumptions: 0
- external network calls: 0
- provider spend: USD 0
- receipt SHA-256:
  `fe794bc6f1afeaf18971b6298c6bcb41d10d5b5ec5965fdc05d26c470859ba61`

Installed-wheel qualification:

- candidate wheel version: `0.4.27` (unpublished replacement build)
- candidate wheel SHA-256:
  `8c5ff0b00174f637b2f1485148dd7c8577ef6f6e6cb391137927fe8d657004f5`
- exact SPC dependency: `semantic-projection-core==0.11.1`
- two fresh installed CLI runs produced byte-identical receipt files
- receipt-file SHA-256:
  `31c46af0692d20b8dcecb118b52349b5c5bf5dcde1955e1b9cf37ada710c7588`
- installed bundle export and canonical receipt join: passed

The first witness proves custody-first out-of-order completion and one aggregate
two-member ordinary-v2 successor request. The second proves a creative retry can
advance to a distinct enabled qualitative-critic action prepared by the production
spend callback. Both end provider pending and replay exactly.

Status: Slice 4B implementation and source qualification complete; API contract
review pending before installed-wheel/release qualification.

## Slice 4B API review correction

API correctly identified that precursor acceptance/successor facts are installed
by the private deterministic fixture. The public evidence is now explicitly and
machine-readably scoped to `post_fan_in_selector_authority_and_replay`. Each
witness carries its exact fixture-installed precursor inventory. Documentation no
longer describes the artifacts as end-to-end real-engine witnesses.

Refreshed evidence-scope qualification:

- focused tests: 7 passed, 1 expected optional-schema skip
- installed wheel SHA-256:
  `8c5ff0b00174f637b2f1485148dd7c8577ef6f6e6cb391137927fe8d657004f5`
- two installed CLI receipts: byte-identical
- receipt identity:
  `fe794bc6f1afeaf18971b6298c6bcb41d10d5b5ec5965fdc05d26c470859ba61`
- receipt-file SHA-256:
  `31c46af0692d20b8dcecb118b52349b5c5bf5dcde1955e1b9cf37ada710c7588`
- external provider/network calls: 0
- spend: USD 0

Status: evidence-scope correction and refreshed installed qualification complete;
API re-review pending.

## Slice 4B API re-review

API approved the corrected evidence scope and authorized fresh installed-wheel and
release qualification. No runtime, schema, or fixture correction remains open.

Status: Slice 4B complete; Slice 5 committed-source qualification is next.

## Slice 5 broad-gate correction

The first broad-suite attempt correctly refused a contradictory lifecycle shape:
completed evidence had asserted local continuation while another provider action
was due. No provider or retained-QA work was involved. The selector now permits
completed-evidence local fan-in only when retained custody is not due and the run
is nonterminal.

Focused regression after correction: 3 passed, 1 expected optional-schema skip.

Status: corrected source must be committed before final candidate qualification.

## Final post-4B candidate evidence

- Artifact source commit: `adbbc70`.
- Version: `0.4.27` (unpublished).
- Fixed build epoch: `1787874000`.
- Deterministic A/B wheel size: 1,060,420 bytes.
- Deterministic A/B wheel SHA-256:
  `210ed3c98bcc84c2cfe9e9669edebaa56a1780bc1bb8057e61c0fffbd0c4c276`.
- Exact installed dependency: `semantic-projection-core==0.11.1`.
- Generic installed release smoke: passed, `DELIVERY_COMPLETE`.
- Installed adversarial qualification: passed.
- Installed post-fan-in retry qualification: passed.
- Installed scoped ordinary-v2 happy-path qualification and bundle: passed.
- Installed happy-path receipt identity:
  `fe794bc6f1afeaf18971b6298c6bcb41d10d5b5ec5965fdc05d26c470859ba61`.
- Two installed receipt files: byte-identical.
- Receipt-file SHA-256:
  `31c46af0692d20b8dcecb118b52349b5c5bf5dcde1955e1b9cf37ada710c7588`.
- Full source suite: 839 passed, 41 expected skips, 833.803 seconds.
- External provider/network calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.

Status: SBE Slice 5 complete. API joined-campaign qualification must pin the exact
wheel digest above before Slice 6 release review.

## API final candidate review

- Review: `API SLICE 5 FINAL CANDIDATE REVIEW.md`.
- Exact candidate consumed: source `adbbc70`, wheel SHA-256 `210ed3c9…c276`.
- API focused campaign: 10 passed.
- API commit: `abcc024`.
- External provider/network calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.
- Disposition: approved for SBE release.

Status: Slice 6 release preparation complete; owner tag/publication authorization
pending.

## Slice 6 final approval

- API final release review: unconditional go.
- API release-pair tests: 23 passed.
- API commit: `8dc7ede`.
- Owner authorization: granted.
- Review checkpoint: `db736e7e8ced31f85f5b1f9d6a8f2746f1ae1dcf`.

Status: tag and publication authorized; release lock and post-publication evidence
pending.
