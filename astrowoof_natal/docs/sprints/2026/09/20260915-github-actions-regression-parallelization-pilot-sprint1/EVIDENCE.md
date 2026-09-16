# Evidence — GitHub Actions regression parallelization pilot

## Initial repository inventory

- Branch: `codex/github-actions-regression-pilot`
- Branch point: `b396da72`
- Dedicated worktree:
  `C:\tmp\semantic-basis-extractor-github-actions-regression-pilot`
- Existing `.github/` directory: absent
- Package minimum Python: `>=3.11`
- Exact declared companion dependency: `semantic-projection-core==0.11.1`
- Supported broad-confidence command:
  `python astrowoof_natal/scripts/run_test_suite.py`
- Manifest schema: `astrowoof.test-suite-manifest.v1`
- Run receipt schema: `astrowoof.test-suite-run.v1`

## Frozen manifest baseline

| Evidence | Value |
| --- | ---: |
| Discovered `test_*.py` modules | 139 |
| `parallel_safe` | 82 |
| `provisional` | 19 |
| `serial_only` | 38 |
| logging-sensitive subset | 13 |
| summed frozen parallel weight | 641.483232 seconds |

The classifications are inputs to this sprint, not optimization candidates.

## Existing runner controls

Source inspection confirms that the coordinator:

- validates discovered modules against the manifest before execution;
- refuses duplicate, missing, stale, and unsupported classifications;
- assigns parallel work by frozen duration and stable module-name tie-break;
- launches independent subprocesses with unique temporary/cache/output roots;
- removes `DATABASE_URL`, `OPENAI_API_KEY`, `RENDER_API_KEY`, and all inherited
  `ASTROWOOF_`, `AWS_`, `CLOUDFLARE_`, and `RENDER_` variables;
- preserves a distinct unquiet serial group for logging-sensitive modules; and
- records test count, skip count, inventory digest, outcome digest, per-group
  commands, durations, stdout, stderr, and return codes.

## SPC clean-runner acquisition evidence

API uses a versioned GitHub Release wheel rather than Git checkout:

- repository: `kevin2357/semantic-projection-core`;
- release tag: `semantic-projection-core-v0.11.1`;
- asset: `semantic_projection_core-0.11.1-py3-none-any.whl`;
- SHA-256:
  `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`;
- download authority: ephemeral repository-scoped `${{ github.token }}`;
- admission: exact SHA comparison before use; and
- installation: `pip --no-index --no-deps` from the admitted local wheel.

Independent repository evidence agrees:

- API `pyproject.toml` embeds the same release URL and SHA-256 fragment;
- `docker/deterministic-domain-worker/requirements.lock` records the same version
  and hash;
- `.github/workflows/publish-worker-images.yml` downloads the exact tag/filename
  and verifies the same digest; and
- the operations field guide names the same canonical wheel identity.

This resolves the package-source ambiguity without a long-lived secret, sibling
checkout, or floating dependency. The pilot will not rely on the remote download
alone: it must hash the admitted file before installation.

Direct read-only GitHub Release metadata verification on 2026-09-16 confirmed:

| Field | Verified value |
| --- | --- |
| Release state | published; neither draft nor prerelease |
| Tag | `semantic-projection-core-v0.11.1` |
| Wheel filename | `semantic_projection_core-0.11.1-py3-none-any.whl` |
| Wheel size | 161,706 bytes |
| Release API digest | `sha256:dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612` |
| Additional asset | `SHA256SUMS.txt` |

The release metadata digest agrees with the qualified API runtime lock and the
planned local admission check.

## Frozen Gate A workflow contract

| Control | Pilot decision |
| --- | --- |
| Trigger | `workflow_dispatch` only |
| Runner | `ubuntu-latest` |
| Timing Python | 3.12; a later bounded 3.11 smoke is optional |
| Permissions | `contents: read` only |
| Git credential persistence | disabled after checkout |
| SPC download | `gh release download` with ephemeral `GH_TOKEN=${{ github.token }}` only in the download step |
| SPC admission/install | exact SHA check, then local `pip --no-index --no-deps` install |
| Job timeout | 30 minutes |
| Aggregate first-measurement budget | 30 hosted minutes maximum |
| Concurrency | branch-scoped; cancel superseded pilot runs |
| Artifact retention | 7 days; compact receipts and failure logs only |
| Application/provider operations | zero expected and permitted |

The aggregate budget includes all jobs for the initial workflow revision. If the
smoke plus 1/2/4-worker comparison cannot finish inside it, do not begin the
whole-suite confirmation; retain what is safe, record the shortfall, and return to
review.

## Slice 1 source evidence

`/.github/workflows/manual-regression-parallelization-pilot.yml` now implements
the Gate A contract without dispatching a hosted run:

- manual `workflow_dispatch` trigger only;
- `contents: read` permission only;
- branch/ref-scoped cancellation and a 30-minute job timeout;
- exact SHA-admitted SPC download, then separate local offline install;
- ephemeral `GH_TOKEN` only in the release-download step;
- checkout with `persist-credentials: false`;
- Python 3.12 provenance plus `pip check` capture;
- manifest validation and all 16 existing test-suite-runner control tests;
- the complete 82-module `parallel_safe` class at two workers; and
- seven-day upload of `.ci-results` only, on both success and failure.

No workflow dispatch, repository setting change, secret use outside the ephemeral
download step, provider operation, or application-service operation has occurred.

Local source-path validation completed with the bundled Python runtime:

| Check | Result |
| --- | --- |
| Manifest validation | `manifest=valid` |
| `test_test_suite_runner` | 16 passed |
| `git diff --check` | passed |

The local check validates runner syntax and controls. It does not attest hosted
action resolution, the clean dependency installation, or GitHub artifact upload;
those remain the first manual dispatch's purpose.

## Slice 1 dispatch attempt

On 2026-09-16, an authorized manual dispatch requested
`manual-regression-parallelization-pilot.yml` at
`codex/github-actions-regression-pilot`. GitHub returned:

```text
HTTP 404: workflow manual-regression-parallelization-pilot.yml not found on the default branch
```

GitHub Actions requires a `workflow_dispatch` workflow to exist on the repository
default branch before it can be dispatched for another ref. This was an API-level
refusal before job allocation: no hosted runner started, no dependency was
downloaded, no artifact was created, and zero hosted minutes were consumed.

The workflow source remains correct on the pilot branch, but a separate owner
decision is now required to make a manual-only dispatcher reachable from the
default branch or to choose a different explicitly authorized trigger design.

## First hosted smoke — mechanical setup correction

Run `35063312210` was the first scheduled hosted witness after the dispatcher
reached the default branch. It proved the following before failure:

- exact pilot commit checkout (`12df955c`);
- Python 3.12.14 setup;
- public SPC Release download and exact SHA admission;
- offline local SPC wheel installation;
- installation of `jsonschema==4.26.0` and transitive public test dependencies;
- successful `pip check`; and
- no provider, R2, Better Stack, Render, database, or other application operation.

The failure was a CI provenance-print typo after `pip check`:

```text
ModuleNotFoundError: No module named 'semantic_projection_core'
```

The package distribution name is `semantic-projection-core`; its documented and
source-used import package is `semantic_projection`. This is not an SPC installation
failure. The workflow now imports `semantic_projection` while still obtaining the
distribution version through `importlib.metadata`.

Because `.ci-results` had been created later in the same step, the early exception
also left no directory for the `if: always()` artifact action. The correction creates
the compact evidence root before any installation command. No test, runner smoke,
or artifact-upload behavior was exercised in this failed attempt.

## Remaining feasibility questions for Gate A

1. The compatible GitHub-hosted Ubuntu/Python combination is not yet exercised.
2. Hosted 1/2/4-worker durations and exact digest equivalence are unmeasured.
3. The serial tail's hosted duration is unmeasured.

## Evidence to retain from implementation

For each workflow revision/run, record:

- workflow commit and run URL/ID;
- runner image label and available CPU count;
- Python and pip versions;
- exact installed SBE/SPC versions and `pip check` result;
- workflow permissions and whether any secret context was referenced;
- manifest SHA-256;
- 1/2/4-worker parallel-only receipt summaries;
- exact test and outcome inventory digest comparison;
- selected whole-suite worker count and receipt;
- setup, parallel-only, serial-tail, and total wall times when available;
- artifact names, hashes or sizes, and retention policy;
- provider/external-service operation count, expected to be zero; and
- any cancellation, timeout, retry, or infrastructure failure separately from test
  failures.

No hosted evidence exists yet. This register will be updated from immutable Actions
run output rather than recollection.
