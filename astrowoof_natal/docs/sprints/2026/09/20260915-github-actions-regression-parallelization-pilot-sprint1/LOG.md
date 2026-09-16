# Log — GitHub Actions regression parallelization pilot

## 2026-09-15 — Sprint initialization

- Preserved the active repository checkout and created
  `codex/github-actions-regression-pilot` directly from `origin/main`.
- Pushed the empty branch and attached it to a dedicated worktree under `C:\tmp`.
- Confirmed the pilot starts at `b396da72` with a clean working tree.
- Confirmed no existing `.github/` automation exists at the branch point.
- Read the test-suite runner, manifest, runner documentation, package metadata, and
  prior duration-led promotion evidence.
- Counted all 139 discovered modules and confirmed exact manifest completeness: 82
  parallel-safe, 19 provisional, and 38 serial-only.
- Identified clean-runner acquisition of pinned SPC 0.11.1 as the first unresolved
  feasibility boundary.
- Chose a manual-only, secret-free, least-privilege pilot before any automatic PR
  trigger or required-check proposal.
- Created the detailed background, evidence register, plan, log, and results index.
- No workflow, runtime source, test, manifest, package, release, or repository
  settings change has occurred.

## 2026-09-16 — SPC acquisition boundary resolved

- API reported its existing image-publication pattern: use ephemeral
  repository-scoped `${{ github.token }}` to download the exact SPC 0.11.1 GitHub
  Release wheel, verify the qualified SHA, copy only admitted bytes into the local
  wheelhouse, verify again at the installation boundary, and install with
  `pip --no-index --no-deps`.
- Independently confirmed the canonical filename, release tag, and SHA-256 in API
  package metadata, worker-image workflows, deterministic runtime lock, and
  operations documentation.
- Froze the exact SPC wheel SHA-256 as
  `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`.
- Removed private-index, editable-checkout, and long-lived-token designs from the
  pilot path.
- Gate A now needs review only of the workflow controls and first-run minutes
  ceiling; dependency provenance is no longer ambiguous.

## 2026-09-16 — Slice 0 / Gate A complete

- Read GitHub Release metadata directly. The exact SPC release is published, not
  draft/prerelease, and exposes the 161,706-byte canonical wheel with the qualified
  SHA-256.
- Froze the manual-only hosted-pilot contract: `contents: read`, no persisted Git
  credential, `ubuntu-latest`, Python 3.12 timing cell, 30-minute job timeout,
  30 hosted-minute aggregate first-run ceiling, branch-scoped cancellation, and
  seven-day compact-artifact retention.
- Froze the dependency path as a separate download, SHA-admission, offline local
  install, installed-version/origin check, and `pip check`; the token exists only
  in the download step and never reaches the test environment.
- Confirmed no secret, repository-write, provider, R2, Better Stack, Render,
  database, QA-workspace, release, or deployment authority is required.
- Slice 0 complete. The next boundary is the reviewed manual smoke workflow in
  Slice 1; no `.github` file or hosted run has been created yet.

## Next action

Proceed to Slice 1 only after this Slice 0 evidence is committed and pushed.

## 2026-09-16 — Slice 1 source implementation

- Added `manual-regression-parallelization-pilot.yml` as the repository's first
  SBE GitHub Actions workflow.
- Kept it manual-only and least-privilege; the checkout credential is not persisted
  and the ephemeral release-download token exists only in that one step.
- Preserved exact SPC SHA admission before its offline local install, then recorded
  Python, installed-package, and `pip check` provenance in compact evidence.
- Corrected the inherited plan language: `--parallel-only` intentionally runs every
  classified parallel-safe module, so the smoke is the complete 82-module two-worker
  group rather than a synthetic subset.
- Added manifest/control-test preflight and a two-worker real coordinator smoke.
- Upload scope is `.ci-results` only with seven-day retention and `if: always()`;
  owned work roots and pip cache are not uploaded.
- Locally validated manifest completeness and all 16 existing runner-control tests.
- No hosted workflow run has started. Commit/push is the next boundary; manual
  dispatch remains separately owner-controlled.

## 2026-09-16 — Manual dispatch platform refusal

- Owner authorized the first manual dispatch from
  `codex/github-actions-regression-pilot`.
- GitHub refused before scheduling with HTTP 404 because the workflow file is not
  present on the repository default branch.
- No hosted runner, dependency download, test, artifact, provider operation, or
  application-service operation occurred. The full 30 hosted-minute budget remains
  unconsumed.
- Do not retry the same API call. GitHub requires a default-branch dispatcher, so
  a distinct owner decision is required before Slice 1 can proceed.
