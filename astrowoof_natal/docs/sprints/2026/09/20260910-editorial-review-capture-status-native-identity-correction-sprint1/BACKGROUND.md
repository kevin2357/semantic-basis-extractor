# Background — editorial-review capture-status native identity correction

## Why this mini-sprint exists

AstroWoof API Sprint 87 Slice 2C discovered a released SBE `0.4.55` producer
defect in the typed no-packet branch of
`build_editorial_review_runtime_capture(run_dir, result_id)`.

The runtime currently delegates refusal construction to the fixture-oriented
`build_editorial_review_capture_status(reason)` helper. That helper inserts the
literal fixture correlations `native-capture-status-fixture`,
`subject-capture-status-fixture`, and `result-capture-status-fixture`. Real
unsupported or incomplete runs can therefore emit non-real correlations and
share a capture identity merely because they share a reason.

The helper also derives its ID from all three correlation values, while the
released semantic manifest defines `capture_id` from `native_run_id`,
`native_result_id`, `reason`, and `detail_code`. The correction must reconcile
runtime construction with that declared identity domain rather than silently
creating a new formula.

## Companion discovery

[API Slice 2C capture-status runtime discovery](<C:/dev/github/astrowoof-api/docs/sprints/2026/09/20260907-editorial-review-evidence-retention-companion-sprint87/API SLICE 2C CAPTURE STATUS RUNTIME DISCOVERY.md>)

## Released baseline

- SBE package: `astrowoof-natal-authoring` `0.4.55`
- Release tag: `astrowoof-natal-authoring-v0.4.55`
- Release-lock commit: `22b31476d526ecba0303d511efc0f9b3e507f000`
- Capture schema: `editorial_review_capture_status.v1`
- Semantic contract: `editorial_review_semantic_contract.v5`

The successful exact-delivery handoff remains valid and is outside this defect.

## Frozen safety boundary

- SBE owns capture-status native content and identity; API must not repair,
  enrich, suppress, or rehash it.
- Construction remains provider-free, network-free, storage-transport-free,
  read-only, deterministic, and bound to the caller-selected exact result ID.
- No latest-result discovery is allowed.
- No placeholder, filename inference, or caller-invented subject identity may
  stand in for durable native evidence.
- If all v1-required correlations cannot be established honestly, the runtime
  must fail closed rather than emit a fabricated v1 status.
- The patch must not alter native eligibility, terminal settlement, delivery,
  lifecycle state, workspace contents, or API observation authority.

## Alloy impact assessment

`No Alloy impact.` The defect concerns concrete runtime correlation population
and deterministic ID derivation. It does not change chronology, pass/retry or
assembly relationships, deck transitions, ownership, selection/delivery,
projection membership, artifact scope, provider-Response uniqueness, or API
observation authority. Schemas, semantic-manifest checks, fixtures, mutations,
and runtime/consumer regressions are the faithful enforcement boundary.

