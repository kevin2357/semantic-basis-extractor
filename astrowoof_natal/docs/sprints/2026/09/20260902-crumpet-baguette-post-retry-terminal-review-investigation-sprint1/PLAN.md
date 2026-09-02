# Sprint 1 — Post-retry terminal-review investigation

Status: Complete. SBE 0.4.39 is committed, immutably tagged, published, and
post-publication hash verified.

## Goal

Prove why fully reported six-initial/two-retry native workspaces reach
`FAILED_REQUIRES_REVIEW`, and distinguish intended editorial terminal review
from a general finalization-predicate defect.

## Slice 0 — Read-only checkpoint comparison

- Recover the two exact protected checkpoints with two HEADs/two GETs only.
- Validate each recovered object against its exact byte count, checkpoint
  SHA-256, inventory digest, archive-safety rules, native run identity, and
  expected restore root before interpreting native state.
- Join the API's six `initial:reported` and two `creative_retry:reported`
  actions to native pass/attempt evidence. Treat `reported` as durable provider
  completion evidence, not as proof that deterministic QA accepted the pass.
- For every pass, compare its final pass state, attempt count, initial and retry
  outcomes, deterministic-QA status/rejection reasons, retry feedback,
  accepted-workspace evidence, and any persisted transition into
  `FAILED_REQUIRES_REVIEW`.
- Compare pass requirements, retry lineage, result adoption, finalization
  prerequisites, and terminal publication payloads.
- Validate each sealed native-result v0.2 document, publication receipt, and
  terminal command-result envelope against the exact checkpoint/snapshot,
  cause code, and complete action-disposition inventory.
- Identify the exact source-level predicate which produces
  `authoring_passes_incomplete`, then identify the earlier native fact which
  made that predicate true.

### Voof-paws 1 — causal findings

Pause after the paired checkpoint comparison. Review whether the evidence
shows intended bounded-attempt exhaustion, incomplete retry adoption, a stale
pass-level transition, or a shared deterministic-QA predicate before designing
the provider-free reproduction.

## Slice 1 — Policy and evidence-contract freeze

- Determine whether both documents satisfy the documented terminal-review
  contract and whether that contract expresses an intended product decision.
- Record the successfully qualified orchestration span: fan-out, detached
  provider custody, reconciliation/fan-in, bounded creative retry, native
  terminal publication, API closeout, and resource release.
- Create a minimal provider-free reproducer from the approved Slice 0 evidence,
  not a synthetic recovery guess.
- Preserve a legitimate two-attempt exhaustion control if Slice 0 shows that
  terminal review can be the correct result.
- Record the owner decision: keep generating, validating, and persisting theme
  groups, but treat the currently unused/provisional distribution rules as
  advisories rather than pass-rejection authority.
- Freeze the hard/advisory partition:
  - malformed registries, invalid/duplicate identifiers or metadata, and
    assignments to unknown groups remain hard structural failures;
  - `theme_group_coverage`, `theme_group_balance`, and
    `cross_section_theme_mirroring` become deterministic advisories.
- Keep hard rejection codes and advisory codes structurally distinct. A pass
  with advisories and no hard issue is accepted; unknown issue codes may not be
  silently downgraded.
- Preserve advisory codes, affected claim IDs, and bounded messages in the
  durable pass-QA report and concise `✨🐶` diagnostics. Logs are explanatory;
  the retained report is the durable evidence.
- Decide and document the smallest honest pass-QA report schema evolution. Do
  not publish advisory codes through an old field whose name or semantics say
  rejection.
- Do not change the pass-6 provider prompt, retry geometry, API lifecycle
  contract, historical Crumpet/Baguette evidence, or retained workspaces.

### Voof-paws 2 — policy/schema freeze

Pause only if the report-shape change creates an API-visible compatibility
question. Otherwise proceed with the approved owner policy.

## Slice 2 — Advisory acceptance implementation

- Split deterministic pass findings into hard rejection and advisory classes at
  one acceptance boundary rather than scattering exceptions across callers.
- Accept a pass containing only theme-group distribution/mirroring advisories;
  persist the advisories and emit a sanitized summary without preparing a
  creative retry.
- Retain rejection for malformed registries, unknown assignments, and all
  unrelated existing hard acceptance failures.
- Add provider-free tests for each advisory code alone and in combination, each
  retained structural failure, mixed advisory + hard failure, unknown-code
  fail-closed behavior, and deterministic report replay.
- Add a production-shaped pass-6 regression derived from the sanitized Slice 0
  facts: the old hard-gate shape is accepted with advisories, while the original
  Crumpet/Baguette artifacts remain immutable historical evidence.
- Verify downstream closure treats accepted-with-advisories as accepted work,
  creates no retry, and remains eligible for ordinary finalization.

## Slice 3 — Run reporter release integration

- Adopt the already source-qualified deterministic run reporter from
  `20260831-run-evolution-matrix-reporter-mini-sprint1` without mixing its
  diagnostic semantics into pass acceptance.
- Package the closed run-report and qualification schemas, Python reader,
  provider-free qualification, and console commands:
  - `astrowoof-run-report` for local parse/render/build;
  - `astrowoof-run-report-qa` for deterministic installed-wheel qualification.
- Retain JSON, Markdown, self-contained HTML, and Mermaid renderers derived from
  one validated report artifact.
- Recheck privacy exclusions, malformed/unknown-line accounting, deterministic
  byte identity, interleaved-run partitioning, and robust no-progress candidate
  classification.
- State prominently that the reporter consumes exported logs only and is never
  lifecycle, custody, settlement, acceptance, or recovery authority.

## Slice 4 — Combined provider-free qualification and handoff

- Add a theme-policy qualification fixture proving advisory-only acceptance,
  durable advisory visibility, zero retry creation, and structural-failure
  rejection through the supported pass acceptance/runtime boundary.
- Run the reporter qualification from a clean installed wheel and render all
  advertised formats from a sanitized fixture in a fresh temporary directory.
- Prove both features are independent: reporter input cannot alter native state,
  and acceptance reports do not depend on reporter availability.
- Produce a concise consumer/operator handoff covering the advisory policy,
  retained evidence locations, reporter usage, privacy limits, and authority
  boundaries.
- Confirm zero provider/network/R2 activity and no retained QA access.

## Slice 5 — Versioned release preparation

- Bump to a fresh immutable patch version before release-bound tests or fixture
  hashes are finalized.
- Run focused pass-acceptance/closure regressions, the reporter suite, release
  smoke, and both installed-wheel qualifications.
- Select broad-suite depth proportionate to the final diff and record honestly
  what was and was not run; do not rerun a successful broad suite merely for a
  release-derived fixture version mismatch.
- Build twice from the committed source identity and require byte-identical
  wheels, clean install/`pip check`, exact wheel and qualification hashes,
  `git diff --check`, and an explicit final release approval before tag/publish.
