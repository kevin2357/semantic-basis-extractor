# Background — GitHub Actions regression parallelization pilot

## Motivation

SBE now has a checked-in, fail-closed test-suite manifest and a deterministic
subprocess coordinator. Local qualification has proven that the classified
`parallel_safe` modules can execute concurrently with isolated temporary, cache,
output, and result roots. The supported broad-confidence default nevertheless
remains one worker because two workers were slower on the qualifying Windows
laptop while the provisional and serial tail dominated elapsed time.

That local result does not answer whether a GitHub-hosted Linux runner has a
different useful concurrency point. This sprint is a bounded experiment to answer
that question with exact runner receipts rather than adopting CI by intuition.

The pilot is intentionally separate from the active cooperative-suspension branch:

- branch: `codex/github-actions-regression-pilot`;
- branch point: `b396da72` from `origin/main`;
- worktree: `C:\tmp\semantic-basis-extractor-github-actions-regression-pilot`; and
- the ordinary repository checkout remains on its existing suspension branch.

## Existing test infrastructure

`astrowoof_natal/scripts/run_test_suite.py` already provides the mechanics that a
hosted workflow should reuse:

- manifest completeness validation for every immediate `test_*.py` module;
- deterministic duration-weighted assignment of `parallel_safe` modules;
- subprocess isolation and unique owned roots per group;
- removal of inherited AstroWoof, AWS, Cloudflare, Render, database, and OpenAI
  credentials;
- protected unquiet execution for logging-sensitive tests;
- exact collected-test and outcome inventory digests;
- retained group logs, commands, durations, and a versioned receipt; and
- a serial tail containing provisional and serial-authority modules.

At the branch point, the manifest classifies all 139 discovered test modules:

| Classification | Modules |
| --- | ---: |
| `parallel_safe` | 82 |
| `provisional` | 19 |
| `serial_only` | 38 |
| logging-sensitive subset | 13 |

The frozen parallel weights sum to 641.483232 seconds. They are scheduling hints
from previous environments, not a promise about hosted-runner duration.

## Current automation surface

The repository has no checked-in `.github/` workflow at this branch point. The
pilot therefore introduces a repository automation surface, even if it changes no
production Python. The workflow must be reviewed and committed like code.

The package declares Python `>=3.11` and pins
`semantic-projection-core==0.11.1`. API's existing image-publication workflow
already establishes the clean-runner source for that companion dependency: the
canonical GitHub Release asset
`semantic_projection_core-0.11.1-py3-none-any.whl` from tag
`semantic-projection-core-v0.11.1`. Its qualified SHA-256 is
`dc345cd3253de333a5428e4fc7e24816447a065215ef288ba76527960a7da612`.

The API workflow downloads that exact asset with the ephemeral repository-scoped
`${{ github.token }}`, admits it only after SHA verification, and installs it
offline with `pip --no-index --no-deps`. The SBE pilot should reproduce that
already-qualified intake pattern rather than inherit local wheels or sibling
worktrees. It must not substitute an editable checkout, floating branch, unpinned
package, or credential-bearing private index.

## Questions this pilot should answer

1. Can a clean hosted Ubuntu runner install the exact declared source tree and SPC
   dependency without exposing broad credentials?
2. Does the manifest validate unchanged in Linux with no unclassified module?
3. Do 1-, 2-, and 4-worker runs of the same 82-module `parallel_safe` inventory
   produce identical test and outcome digests?
4. Which worker count minimizes hosted wall time on repeated evidence rather than
   one noisy sample?
5. How much of whole-suite wall time remains in the serial tail after choosing the
   best hosted parallel count?
6. Are failure logs, group receipts, and exact reproduction commands useful when
   collected as GitHub Actions artifacts?
7. Is the speed/reliability result good enough to justify an automatic pull-request
   gate, or should the workflow remain manual/diagnostic?

## Safety and authority boundary

This sprint is provider-free and must not receive or use production secrets. The
workflow may install declared build/test dependencies and may upload its own test
receipts and logs to the GitHub Actions run. It may not:

- call OpenAI or another paid provider;
- access R2, Better Stack, Render, a database, GHCR deployment credentials, or QA
  workspaces;
- build, tag, publish, deploy, or attest a release candidate;
- mutate the test classification merely to improve timing;
- grant write permissions to repository contents, packages, issues, or actions;
- treat a green hosted run as installed-wheel or release-pair qualification; or
- make a first-pass experimental workflow a required branch-protection check.

GitHub Actions network access during checkout and dependency installation is
expected. The test command itself remains provider-free through the existing
runner's environment sanitation and should not depend on external application
services.

## Cost and retention posture

The pilot should minimize hosted minutes and artifact volume:

- start with manual `workflow_dispatch` only;
- use one hosted runner for the 1/2/4 parallel-only comparison so machine class and
  setup overhead are shared;
- run the whole suite once at the selected count rather than three times;
- upload compact receipts and failure logs, not entire temporary workspaces;
- apply an explicit job timeout and short artifact retention; and
- cancel superseded runs on the same branch.

Any later scheduled or pull-request trigger is a separate adoption decision.

## Expected implementation surface

The likely pilot is one workflow file plus sprint evidence. A tiny repository-only
helper is acceptable only if YAML cannot safely compare receipts or collect the
desired summary. Production package code, schemas, fixtures, the manifest, and the
test runner should remain unchanged unless the hosted environment exposes a real,
separately reviewed defect.

## Prior evidence and claim limits

The duration-led promotion campaigns established module-level isolation and exact
concurrent inventory equivalence. This sprint does not reopen those classifications.
It evaluates a new execution environment and orchestration layer.

A successful pilot proves only that the tested commit passed on the selected GitHub
hosted image and Python version with the recorded dependency identities. It does not
prove Windows equivalence, deterministic wheels, installed-release behavior, live
provider behavior, or future hosted-runner performance.
