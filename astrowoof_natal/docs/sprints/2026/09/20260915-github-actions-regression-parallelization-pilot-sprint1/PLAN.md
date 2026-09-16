# Plan — GitHub Actions regression parallelization pilot

## Objective

Create and measure a least-privilege GitHub Actions pilot that runs SBE's existing
provider-free regression coordinator on a clean hosted Linux runner, proves exact
inventory/outcome equivalence across justified parallel counts, and determines
whether hosted CI is reliable and materially faster enough to adopt.

## Success criteria

The pilot succeeds when it produces reviewable evidence for all of the following:

1. an exact, reproducible clean-runner installation of SBE and SPC 0.11.1;
2. manifest completeness on the hosted checkout;
3. identical successful test/outcome inventories for 1-, 2-, and 4-worker
   `parallel_safe` runs;
4. one successful whole-suite run using the best justified hosted count;
5. compact retained receipts and actionable failure logs;
6. zero provider, R2, Better Stack, Render, database, deployment, or QA-workspace
   operations; and
7. a documented adopt/manual-only/reject disposition based on timing, reliability,
   cost, and maintenance burden.

## Frozen fences

- Begin from branch point `b396da72`; do not merge the concurrent suspension work.
- Use GitHub-hosted Ubuntu and official `actions/checkout` / `actions/setup-python`
  releases pinned to reviewed major or immutable commit references.
- Workflow permissions default to `contents: read`; add no write permission.
- The first workflow trigger is `workflow_dispatch` only.
- Do not reference repository/environment secrets unless Gate A establishes that a
  private SPC source is unavoidable and the owner separately approves a narrow,
  read-only credential design.
- Never expose credentials to tests. Preserve and test the runner's sanitation.
- Do not change test classifications, frozen weights, runtime semantics, schemas,
  fixtures, or production logging to improve CI timing.
- Do not parallelize wheel builds, installed-wheel qualification, release receipts,
  tags, publication, deployment, or live qualification.
- Do not call the direct `unittest discover` fallback the authoritative CI result;
  use the checked-in coordinator and its receipts.
- Do not make the pilot a required check or add a pull-request trigger before the
  adoption gate.
- Add no new test module unless implementation introduces testable repository
  logic; if one is added, classify it in `test_suite_manifest.json` in the same
  change.
- Record `no Alloy impact`: this is execution infrastructure beneath unchanged
  native/editorial/lifecycle relationships. Reassess only if implementation reaches
  production semantics.

## Slice 0 — Clean-runner dependency and workflow contract

1. Download the exact SPC 0.11.1 wheel from its canonical GitHub Release using the
   ephemeral repository-scoped `${{ github.token }}` and the API-proven coordinates:
   - repository: `kevin2357/semantic-projection-core`;
   - tag: `semantic-projection-core-v0.11.1`;
   - filename: `semantic_projection_core-0.11.1-py3-none-any.whl`; and
   - SHA-256:
     `dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`.
2. Admit the wheel into a workflow-local directory only after exact SHA comparison.
   Install it with `pip --no-index --no-deps`, then verify installed version/origin
   and run `pip check`. Do not pass `${{ github.token }}` into the test steps or
   persistent environment.
3. Reject editable sibling checkout assumptions, floating branches, unverified
   downloads, broad personal tokens, and copied local wheels without provenance.
4. Freeze the workflow contract:
   - `workflow_dispatch` only;
   - `ubuntu-latest` or a more specific reviewed Ubuntu image;
   - one initial Python runtime, preferably 3.12 for timing, followed by a bounded
     3.11 compatibility cell only after the workflow mechanics pass;
   - `contents: read` permissions;
   - explicit job timeout;
   - branch-scoped concurrency with cancellation of superseded runs;
   - short receipt/log artifact retention; and
   - no secret-bearing environment at test execution.
5. Decide whether dependency caching is safe/useful. Cache only ordinary pip
   download content keyed by OS, Python, and lock inputs; never cache credentials,
   working directories, or test outputs.
6. Record the hosted-minutes ceiling for the first measurement run.

Acceptance:

- exact dependency provenance, asset coordinates, and digest are documented;
- download, admission, and offline installation are separate workflow steps;
- the workflow permissions/triggers/runtime/timeout/retention contract is frozen;
- no unresolved secret or package-source ambiguity remains; and
- no workflow has been dispatched yet.

Status: complete. API's existing immutable-release intake pattern supplied the
exact SPC asset coordinates, and direct GitHub metadata confirms its published
release state, filename, size, and SHA-256. The manual-only, least-privilege,
30-hosted-minute pilot contract is frozen in `EVIDENCE.md`.

## Review Gate A — Feasibility and authority

Owner/API review confirms the SPC acquisition route, permissions, trigger, runtime,
minutes ceiling, and evidence-retention design. If exact dependency acquisition
requires materially broader authority than expected, stop rather than improvising.

Status: passed. No broader authority is required: the exact public release asset is
admitted with an ephemeral repository-scoped token limited to its download step;
the pilot has `contents: read` only and a 30 hosted-minute aggregate ceiling.

## Slice 1 — Manual smoke workflow

1. Add one clearly named workflow under `.github/workflows/`.
2. Checkout the exact triggering commit with persisted Git credentials disabled
   after checkout where practical.
3. Install the selected Python runtime and exact dependency set.
4. Print only safe provenance: OS/runner label, CPU count, Python/pip versions,
   installed package names/versions, and `pip check` outcome.
5. Run fast preflight controls before the expensive suite:
   - manifest load/completeness validation;
   - focused `test_test_suite_runner.py`; and
   - a sanitation assertion proving representative denied variables do not reach a
     child worker.
6. Run the complete already-classified `parallel_safe` inventory with
   `--parallel-only --workers 2` and write an explicit receipt under a
   workflow-owned results directory. The coordinator intentionally offers no
   parent-level subset selector; this preserves the real manifest/shard boundary
   that Slice 2 will measure.
7. Upload the receipt plus failure logs with `if: always()` and a short retention
   period. Exclude temporary workspaces, caches, source archives, and authored
   fixtures copied by tests.
8. Deliberately exercise one controlled failure on a temporary workflow revision or
   local workflow-equivalent invocation to prove that logs and reproduction commands
   survive a red run; do not leave the main pilot intentionally red.

Acceptance:

- the manual workflow starts on the intended commit;
- installation, manifest preflight, focused runner tests, and smoke pass;
- artifact upload occurs on success and failure without leaking secrets or large
  work roots; and
- the workflow has no external application operations.

Status: source implementation complete and locally validated. The workflow is
manual-only and was not schedulable from its feature branch: GitHub requires a
`workflow_dispatch` file to exist on the repository default branch before dispatch
for another ref. The initial authorized dispatch received HTTP 404 before any job
allocation, consuming zero hosted minutes. Its exact hosted dependency admission,
action execution, and artifact behavior remain unproven until an owner selects a
default-branch dispatcher or another explicit trigger design.

## Review Gate B — Smoke and artifact usability

Review the exact workflow diff and first run. Confirm permissions, package
provenance, logs, artifact contents, redaction, and reproduction commands before a
full measurement run.

Status: reached. Hosted runs prove exact SPC admission, Python 3.12 setup,
credential sanitation controls, complete two-worker execution, compact receipt
retention, and failure-only worker diagnostics. The 650-test smoke takes about
91 seconds, but it is red for two source-baseline digest mismatches and for a
metadata-only test setup condition. Do not begin parallel-count measurement until
owner review decides whether to admit a precisely pinned build-tool pair for local
SBE metadata and how to disposition the two SHA-baseline failures.

## Slice 2 — Hosted parallel-count experiment

1. On one hosted runner and one exact commit, execute the complete
   `parallel_safe` class sequentially at `--workers 1`, `2`, `4`, and an explicitly
   curiosity-only `16`, each with a unique `--work-root` and `--receipt`.
2. Preserve the same Python process environment and installed dependencies across
   all three cells so only worker count changes.
3. Compare and require exact equality of:
   - manifest SHA-256;
   - test count and skip count;
   - test inventory SHA-256;
   - outcome inventory SHA-256; and
   - successful group return codes.
4. Record coordinator wall time and per-shard wall time. Keep setup time separate.
5. If one count fails or digests differ, stop before whole-suite execution and use
   retained group commands to reproduce the discrepancy.
6. Treat a single fastest observation as provisional. If the leading count is only
   marginally faster or results are noisy, repeat only the leading pair within the
   approved minutes ceiling.
7. Select only among worker counts `1`, `2`, and `4` when a count is both equivalent
   and materially useful. Record `16` for curiosity/performance characterization
   only; it cannot become the recommended count in this pilot. Otherwise retain one
   worker.

Acceptance:

- all compared counts are green and digest-identical;
- timing and runner characteristics are retained;
- the selected count has a stated evidence-based rationale; and
- no module classification has changed.

## Review Gate C — Parallel-count selection

Review exact receipt equivalence, timing variability, hosted minutes consumed, and
the proposed count. Approve one whole-suite confirmation or stop the pilot as not
beneficial.

Status: passed. On run `35067134359`, all worker counts were receipt-equivalent:
1=184.096436s, 2=104.275341s, 4=79.058307s, and curiosity-only 16=81.548776s.
Four is materially faster than the eligible alternatives; 16 is slower and excluded
from selection. Proceed with one four-worker full-suite confirmation.

## Slice 3 — Whole-suite hosted confirmation

1. Run the full coordinator once using the selected count, preserving the
   provisional and serial groups exactly as implemented.
2. Require manifest completeness, successful group return codes, exact inventory
   receipt generation, and zero denied credential variables in worker environments.
3. Retain the compact full receipt and only failure/debug logs needed for
   reproduction.
4. Compare test/skip inventory against the current accepted local broad-suite
   baseline where a same-commit baseline exists. Explain platform-dependent optional
   skips rather than forcing digest equality across unlike platforms.
5. Optionally run one bounded Python 3.11 smoke/compatibility cell if Gate A approved
   it; do not multiply the full suite across versions in this pilot.

Acceptance:

- one full hosted suite passes from a clean checkout;
- receipts and logs are sufficient to reproduce any group;
- wall-time composition shows parallel prefix versus serial tail; and
- the result is explicitly non-release-authoritative.

## Review Gate D — Adoption disposition

Choose and document exactly one disposition:

1. **Adopt as PR gate:** only if reliable, materially useful, maintainable, and
   appropriately bounded. Add a separate reviewed pull-request trigger and branch
   protection outside this experimental slice.
2. **Retain manual diagnostic:** useful for release investigations or occasional
   Linux regression evidence, but not worth every-PR minutes.
3. **Reject/remove:** hosted setup, dependency authority, runtime, flakiness, or cost
   outweighs the benefit. Preserve sprint evidence and remove the workflow.

No disposition silently replaces local broad-suite, installed-wheel, API consumer,
or release-lock qualification.

## Slice 4 — Documentation and closeout

1. Update `Test Suite Runner.md` only with behavior actually proven by hosted runs.
2. Record workflow commit/run identities, receipts, timings, artifact retention,
   provider-operation count, and final disposition in `EVIDENCE.md`.
3. Record any workflow maintenance assumptions, especially action versions and SPC
   acquisition.
4. Run focused workflow/helper tests, manifest validation, Markdown/diff checks,
   and a final clean-tree review.
5. Commit at reviewable boundaries and push the branch. Do not merge or alter
   repository settings without separate owner direction.

## Expected artifacts

- `.github/workflows/<reviewed-pilot-name>.yml`;
- versioned test-suite receipts from hosted runs;
- compact uploaded GitHub Actions artifact(s);
- sprint `BACKGROUND.md`, `PLAN.md`, `LOG.md`, `EVIDENCE.md`, and `results/` index;
- optional tiny repository-only comparison helper with focused tests; and
- final adoption/manual-only/rejection decision.

## Current status

Slice 3 found one pre-existing cross-platform release-contract assertion: its
300 KiB fixture floor is satisfied only after Windows CRLF expansion, while the
smallest canonical-LF fixture is 299,878 bytes on Linux. Correct that coarse
truncation guard, rerun one final four-worker whole suite, then proceed to Gate D.
The manual-only pilot remains provider-free and has no application I/O.
