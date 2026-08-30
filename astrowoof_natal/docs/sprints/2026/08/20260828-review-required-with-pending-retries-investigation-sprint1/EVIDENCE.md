# Sprint evidence

## Immutable publication evidence

- Tag: `astrowoof-natal-authoring-v0.4.29`.
- Tag target: `5f317b982241c2fdad3d322ba595429c33bb5ed8`.
- GitHub release ID: `379163756`.
- Published at: `2026-08-30T02:50:46Z`.
- Wheel asset ID: `536065695`.
- Published/downloaded wheel SHA-256:
  `25b35b74b35c65e4bce97f7050e5579d6f802aad944569954e50b7db054c2726`.
- Checksum asset ID: `536065692`.
- Checksum asset SHA-256:
  `d2e2a85e3fd2c5566ef58f6770ffb2e47a234822c079cff22c1aefe829c2eb60`.
- Download verification: pass.

## Slice 8 final release evidence

- Release version: `0.4.29`.
- Exact artifact source commit: `f6a045b`.
- Corrected full suite: 879 passed; 44 expected environment/opt-in skips.
- Deterministic wheel builds: byte-identical.
- Wheel SHA-256:
  `25b35b74b35c65e4bce97f7050e5579d6f802aad944569954e50b7db054c2726`.
- Installed generic release smoke: pass.
- Installed lifecycle smoke: pass.
- Installed retry-lineage receipt SHA-256:
  `70c3ffc1ce9181f8cbaa2e5afdfd7d953f927d0d09bcef90ac976e19afa4d575`.
- Installed terminal-review receipt SHA-256:
  `9eec36cd470243fcd8acff650ac8e16ab8795d469bf202144e3d53ad7f24d8c0`.
- Installed post-fan-in qualification: pass.
- Installed adversarial receipt SHA-256:
  `79eaa3dfc31d9e41fc0814a649751ad0d24df22c5b79bf47db1b24317cae3224`.
- SPC dependency/compatibility pin: `semantic-projection-core==0.11.1`.
- External provider/network/spend: 0/0/USD 0.
- Retained Pippin/Duchess/R2/API access or mutation during implementation and
  release qualification: 0.

The later release-lock commit changes documentation/evidence only. The wheel is
the exact artifact built from `f6a045b`.

## Slice 7 installed-wheel evidence

- Public console command: `astrowoof-retry-lineage-qa`.
- Packaged qualification schema:
  `retry-lineage-qualification.v1.schema.json`.
- Consumer handoff: `RETRY LINEAGE V0.8 API CONSUMER HANDOFF.md`.
- Consumer fixture manifest: `slice7-consumer-fixture-manifest.json`.
- Candidate wheel version: `0.4.28` (unreleased working candidate; a release
  would require a fresh version).
- Candidate wheel SHA-256:
  `255831b795a9403880f1fc67e8618e3711d9b6e67ea9108862a88f0515585cf6`.
- Installed qualification receipt SHA-256:
  `b845a3fc61069e3be7569d7f520cab5bb50d2bbaa1bfc26116628a13f985934d`.
- Installed public fixture and lifecycle-v0.8 validation: pass.
- Installed generic lifecycle smoke with required packaged-resource checks: pass.
- Source contract/runtime/qualification suite: 15 passed.
- Provider/network/create/retrieve/spend: 0/0/0/0/USD 0.
- Retained QA/R2/API access or mutation: 0.

Status: Slice 7 complete; paused at Voof-paws 6 joint-adoption review.

## Slice 6 qualification evidence

- Qualification contract:
  `astrowoof.retry_lineage_qualification.v1`.
- Receipt SHA-256:
  `b50eae7c9804cd4ab466e4f252db18561e7239045ba5220f0cf52b0acc025c13`.
- Fresh-root reproducibility: byte-identical receipt across two executions.
- Route cells: exact interactive and bounded interactive.
- Runtime progression per route:
  `provider_reconciliation_cycle` with one due retained action, followed by
  `none / retain_for_review / retry_lineage_conflict_requires_review` after
  custody settlement.
- Executed create-fence boundaries: prepared, authorized, call-entered,
  provider-identity-durable, and reported; forward create permitted in all
  cells: false.
- Focused qualification plus runtime/contract suite: 13 passed.
- Combined Slices 2–6 and adjacent retry/payload/post-fan-in suite: 31 passed.
- `git diff --check`: clean (Git emitted only line-ending conversion notices).
- External network/provider create/retrieve/spend: 0/0/0/USD 0.
- Retained Pippin/Duchess/R2/API mutation or access during implementation and
  qualification: 0.

Status: Slice 6 complete; paused at Voof-paws 5.

## Slices 4–5 runtime evidence

- Corrected production regression proves preparation, pre-authorization re-entry,
  authorization, and durable `SUBMITTING` intent retain exactly one action and
  byte-identical retry evidence with zero provider transport.
- Generic QA feedback regression proves attempt 2 remains the predecessor for
  incomplete attempt 3.
- Pippin/Duchess-shaped provider-free fixture selects reconciliation while one
  provider ID is retained, then selects typed review after that custody settles.
- Whole-ledger conflict preflight is nonmutating and blocks forward dispatch.
- Public lifecycle CLI emits validated v0.8 evidence from the real workspace.

## Slice 3 contract evidence

- `retry_lineage_contracts.py` is projection-only and not wired to runtime
  mutation.
- Packaged schema: `retry-lineage-contracts.v1.schema.json`.
- Complete lifecycle root schema: `temporal-lifecycle-contracts.v3.schema.json`;
  public reader: `read_lifecycle_inspection_v08_schema()`.
- Packaged complete example: `retry-lineage-mixed-custody.v0.8.json`, validated
  by `read_lifecycle_inspection_v08_fixture()`.
- Focused mutation coverage proves binding/request changes retain one attempt key
  and become conflict; rehashed malformed evidence fails; mixed custody preserves
  reconciliation; fabricated, missing, and provider-mismatched lineage members
  fail exact joins; and a rewritten review branch is refused.
- Retained QA workspaces and provider transports were not accessed.

## Pre-investigation evidence

- Incident background: `BACKGROUND.md`.
- Companion completed sprint:
  `../20260828-terminal-review-closeout-handoff-sprint1/`.
- Frozen API run IDs:
  - Pippin: `fbe8ada6-511d-469f-a9b6-31fe15835138`.
  - Duchess: `40783a32-e326-4605-8503-de8838152fc0`.
- Frozen native run IDs:
  - Pippin: `8fcce2334d4e717595cafe5af18bb6ee5d097270da362a6783a5fab2f5a8bb79`.
  - Duchess: `d436f2a008656d16bb8f1efbdb11342278ed808ad88acba3fdafef087d230268`.
- Prior controlled inspection established:
  - both retained archives and complete inventories are hash-valid;
  - latest sealed native results are `provider_pending`;
  - neither retained result index contains `review_required`;
  - no retained workspace mutation or provider operation was performed.
- SBE 0.4.28 separately corrected the exact-interactive terminal-result handoff.

## Historical pre-Slice-1 gate

No new retained bytes have been accessed for this investigation. No provider call,
retrieval, create, spend, workspace write, R2 write, recovery, or deployment has
occurred.

This section records the historical pre-Slice-1 posture only.

## Current gate

Slices 0–7 are complete. The active gate is Voof-paws 6: API review of the
installed-wheel public surface and joint provider-free adoption evidence before
release preparation.

## Slice 0 evidence

- Protocol: `SLICE 0 - EVIDENCE MAP AND READ-ONLY INSPECTION PROTOCOL.md`.
- Frozen manifest: `slice0-inspection-manifest.json`.
- Background SHA-256:
  `1e2253f3f2b3485bf41a5324f8e8e1ae4527a6fd397f06d7786a3d0dfce270cc`.
- Protocol SHA-256:
  `ad5ebf34973c2763f33d6d18e7062208591bd4c800b45ba5408200a32364e74b`.
- Frozen remote limits: two exact HEAD operations, two exact GET operations,
  zero list/write/copy/delete/provider operations.
- Credential presence during Slice 0: false.
- Retained R2 access: 0.
- Retained workspace/API/R2 mutation: 0.
- Provider create/retrieve/spend: 0/0/USD 0.

Status: Slice 0 complete; awaiting Voof-paws 1 review and exact protected
checkpoint authority before temporary R2 access.

## Voof-paws 1 API review

- API approved exactly two checkpoint HEADs and two GETs with no listing, writes,
  provider access, recovery, execution, or retained-state mutation.
- API requires actual checkpoint-contract and compatibility-identity values in
  the uncommitted authority input and their nonsecret identities in the receipt.
- Every causal claim must carry a compact provenance pointer: declared native
  relative path and member SHA-256, API row/action identity where applicable,
  evidence class (`direct`, `inferred`, `unknown`, or `contradictory`), and
  confidence level.
- Inspection remains blocked until the exact protected checkpoint-authority input
  is supplied; bucket credentials alone do not authorize object discovery.

Status: Voof-paws 1 approved; awaiting exact protected checkpoint authority and
temporary R2 credentials for Slice 1.

## Slice 1 failed-attempt evidence

- Protected authority input validation: pass.
- Authority SHA-256:
  `1a21adf1b125304e9a1baa7ded358e32eb7f564b2c4489b812e79289462dcbf1`.
- First exact R2 HEAD: identity/metadata checks passed.
- First exact R2 GET: byte count and archive SHA-256 checks passed.
- Local inventory validation: stopped on an inspection-script canonicalization
  defect (missing newline in the inventory digest preimage).
- Persisted retained archive bytes: 0.
- Second checkpoint remote access: 0.
- Remote counts: HEAD 1; GET 1; list/write/copy/delete 0.
- Provider create/retrieve/spend: 0/0/USD 0.
- Retained workspace/API/R2 mutation: 0.
- Corrected validator production-format local test: pass.

Status: Slice 1 remains incomplete and stopped. No conclusion about historical
retry/review behavior is drawn from the failed attempt.

## Slice 1 retry refusal evidence

- Retry authorization: explicit owner/API approval.
- First exact HEAD and archive byte/SHA identity: pass.
- Complete manifest inventory digest after canonicalization correction: pass.
- Logical-root join against protected API authority: refused.
- Persisted archive bytes: 0 (pre-hardening tool behavior).
- Duchess retry access: 0.
- Retry remote counts: HEAD 1; GET 1; list/write/copy/delete 0.
- Cumulative remote counts: HEAD 2; GET 2; list/write/copy/delete 0.
- Provider create/retrieve/spend and retained mutation: 0/0/USD 0/0.
- No path mismatch was normalized, ignored, or treated as historical truth.

Status: Slice 1 remains incomplete. The evidence-preserving tool correction is
locally ready; another remote attempt is not implied by this record.

## Slice 1 completed inspection evidence

- Final fetch receipt: `slice1-read-only-inspection-receipt.json`.
- Final remote operations: HEAD 2; GET 2; list/write/copy/delete 0.
- Cumulative remote operations including the two stopped local-validator
  attempts: HEAD 4; GET 4; list/write/copy/delete 0.
- External provider create/retrieve/spend: 0/0/USD 0.
- Retained workspace/API/R2 mutation: 0.
- Local fetch receipt SHA-256:
  `115ba42b599fd6e41f0d288419e735ddf587d7a2923af60f3d8ffbe8a392a965`.
- Pippin archive SHA-256:
  `7730fb4cb37cfd28a2d1b7c9f845aa0051504dae29e893fdf6b4578b67216e8f`.
- Duchess archive SHA-256:
  `a2dcf2eb71aff3b0dd1df3dc7bc0c680527cf319fe55aa1df54b83ef1efeb9ea`.
- Sanitized causal timeline:
  `SLICE 1 - SANITIZED RETAINED PROVENANCE TIMELINE.md`.
- Machine-readable lineage inventory: `slice1-sanitized-lineage.json`.

Status: Slice 1 complete; Voof-paws 2 review pending. The exact later API review
decision is explained by current public mapper/source behavior, but the native
checkpoint itself remains nonterminal and provider-pending.

## Owner policy evidence

- Product-policy record: `OWNER POLICY NOTE - THEME GROUP QA POSTURE.md`.
- Historical issue code in both retained attempt-1 and attempt-2 reports:
  `theme_group_coverage`.
- Current code distinguishes structural registry validity, coverage, balance,
  minimum group size, and cross-section mirroring.
- Theme-group policy is explicitly non-driving for this investigation. No runtime
  policy change has been made or added to the sprint plan.

## Slice 2 causal reproduction evidence

- Narrative: `SLICE 2 - PROVIDER-FREE CAUSAL REPRODUCTION.md`.
- Closed causal matrix: `slice2-causal-matrix.json`.
- Focused regression:
  `tests/test_review_required_pending_retries_investigation_slice2.py`.
- Runtime reproduction: authorized and prepared actions with one route and two
  request digests produced through the real retry loop.
- Public projection reproduction: base provider-reconciliation selection replaced
  by v0.7 `retain_for_review` despite retained provider custody.
- Failure-modality comparison: historical and generic QA rejection projections
  are identical.
- Qualification: 12 passed.
- Provider/network/create/retrieve/spend: 0/0/0/0/USD 0.
- Retained QA workspace/R2/API mutation: 0/0/0.

Status: Slice 2 complete; Voof-paws 3 investigation-conclusion review pending.
