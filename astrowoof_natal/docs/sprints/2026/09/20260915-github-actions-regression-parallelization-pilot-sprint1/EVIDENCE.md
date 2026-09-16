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

## Feasibility unknowns for Gate A

1. Exact clean-runner acquisition of SPC 0.11.1 is not yet established.
2. The compatible GitHub-hosted Ubuntu/Python combination is not yet exercised.
3. No workflow permissions, timeout, artifact, or concurrency policy exists.
4. Hosted 1/2/4-worker durations and exact digest equivalence are unmeasured.
5. The serial tail's hosted duration is unmeasured.

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
