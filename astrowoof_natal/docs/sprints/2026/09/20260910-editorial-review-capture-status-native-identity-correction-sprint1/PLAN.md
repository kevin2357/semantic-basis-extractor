# Plan — editorial-review capture-status native identity correction

Status: Slice 0 plan approved by Kevin and API/Vafflemutt. Provider-free
discovery, implementation, and qualification are authorized within the frozen
safety boundary; release and external operations remain separately gated.

## Goal

Ensure every emitted runtime `editorial_review_capture_status.v1` carries exact,
durable native run, subject, and selected-result correlations and derives its
`capture_id` from the released semantic-manifest identity domain. Preserve the
closed schema, typed reasons/detail codes, deterministic behavior, and no-I/O
posture.

## Slice 0 — Identity-source and failure-boundary freeze

Trace every status-producing branch through `read_eligible_editorial_result`,
`collect_editorial_review_runtime_evidence`, and
`build_editorial_review_runtime_capture`.

For each branch, identify the validated source of:

- `native_run_id`;
- `subject_id`;
- `native_result_id`;
- `reason`; and
- `detail_code`.

Confirm that the caller-selected `result_id`, native result `result_id`, and
publication receipt `result_id` agree before emitting a status. Determine the
closed behavior when result/receipt identity is valid but a single durable
subject identity cannot be established. Do not infer subject identity from a
path, fixture sentinel, or unvalidated state.

Freeze whether the existing v1 schema and manifest formula are sufficient. The
default recommendation is to preserve both and derive `capture_id` exactly from
`native_run_id`, `native_result_id`, `reason`, and `detail_code`.

`subject_id` remains mandatory, validated status content but is deliberately
outside that frozen capture-ID domain. The same selected result with a subject
mismatch must emit no status. A hypothetical subject-only change must not be
accepted as defining a second legitimate capture ID.

### Review gate 0 — contract decision

Pause for Kevin and API/Vafflemutt review of the identity sources, exact-result
join, subject-unavailable behavior, and v1 preservation decision before code.

## Slice 1 — Separate fixture and runtime construction

- Replace runtime dependence on fixture sentinels with a public, provider-free
  constructor requiring explicit native correlations.
- Keep fixture convenience isolated and visibly fixture-only.
- Centralize the closed reason-to-detail-code mapping.
- Validate inputs and derive `capture_id` from the semantic manifest's declared
  domain.
- Preserve deterministic canonical construction and the closed v1 schema.

## Slice 2 — Thread exact correlations through runtime refusals

- Carry the exact validated result/view identity through every eligible,
  unsupported, incomplete, and contradictory branch.
- Ensure nested helpers cannot discard the selected result identity.
- Emit a status only when all required native correlations are durable and
  mutually consistent.
- Fail closed without fabricated native content when v1 cannot be populated.
- Preserve successful packet/projection/artifact output byte-for-byte unless a
  separately reviewed deterministic fixture digest necessarily changes.

## Slice 3 — Focused qualification and consumer review

Add provider-free regressions proving:

1. two distinct real-ish native inputs produce distinct correlations and
   capture IDs;
2. repeated identical input produces identical status bytes;
3. requested/result/receipt ID mismatch is rejected;
4. run and subject mismatches are rejected;
5. no runtime status contains fixture sentinels;
6. every reason/detail-code branch remains schema-valid;
7. `capture_id` matches the manifest formula and rejects a rehashed mutation;
8. successful exact-delivery and valid packet branches remain unchanged; and
9. construction performs no provider, network, subprocess, database, storage,
   lifecycle, or workspace mutation.

Run the focused editorial-review contract/runtime matrix, release-contract
guards affected by packaged resources, and a clean installed-wheel consumer
qualification. Submit the exact candidate to API/Vafflemutt for Slice 2C review.

### Review gate 3 — package/release decision

Pause after source and installed-candidate evidence. A version bump, commit,
push, tag, GitHub release, API sender, Better Stack write, deployment, provider
operation, or retained-run access requires its own explicit authorization.

## Slice 4 — Optional patch release

If jointly approved, freeze a fresh unreleased patch version (expected
`0.4.56`), select a proportionate regression gate from the final diff, perform
exact-commit reproducible-wheel qualification, obtain final consumer and owner
authorization, and follow the immutable publication playbook.

## Explicit exclusions

- API transport/sender implementation
- Better Stack, R2, database, or deployment work
- Provider calls or spend
- Latest-result discovery
- Lifecycle, eligibility, cleanup, retry, or recovery changes
- Capture schema redesign unless Slice 0 proves v1 cannot be honest
- New Alloy modeling
