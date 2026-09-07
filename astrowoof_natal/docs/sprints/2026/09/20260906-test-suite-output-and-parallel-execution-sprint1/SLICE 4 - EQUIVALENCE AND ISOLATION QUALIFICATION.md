# Slice 4 — equivalence and isolation qualification

## Result

Slice 4 is complete and ready for Voof-paws 2.

The deterministic runner proved exact one-worker/two-worker behavioral
equivalence over the complete current suite. It did not prove a whole-suite
speed advantage on this laptop: the final two-worker invocation was 126.279
seconds slower than the final one-worker invocation. The runner is therefore a
sound framework for controlled growth, but its present conservative manifest
should not be represented as a performance improvement.

## Authoritative final pair

Both invocations used the same checked-in manifest and final runner behavior,
including exact outcome inventories.

| Mode | Tests | Skips | Wall time | Success |
|---|---:|---:|---:|---|
| Two workers | 1,115 | 58 | 1,091.085 s | yes |
| One worker | 1,115 | 58 | 964.806 s | yes |

Exact shared identities:

- test inventory SHA-256:
  `fd9b735381548e2bab7d732aa1a500b87cfe0008873583952f9b7edd8aefd146`
- outcome inventory SHA-256:
  `4f018b127dec7d3c305ec3372a80224d5ab33a3a2707de75a3db6ca247b0f303`
- failures: none;
- errors: none;
- unexpected successes: none; and
- skip count and exact skipped identities: equivalent through the outcome
  digest.

The one-test increase from earlier 1,114-test characterization is the runner's
new exact-outcome-inventory regression. Both final modes collected that same
1,115-test inventory.

## Group timing

Two-worker invocation:

| Group | Tests | Skips | Duration |
|---|---:|---:|---:|
| `parallel-1` | 136 | 22 | 60.186 s |
| `parallel-2` | 100 | 18 | 52.935 s |
| `serial-quiet` | 779 | 14 | 984.875 s |
| `serial-observability` | 100 | 4 | 45.006 s |

One-worker invocation:

| Group | Tests | Skips | Duration |
|---|---:|---:|---:|
| `parallel-1` | 236 | 40 | 72.097 s |
| `serial-quiet` | 779 | 14 | 853.252 s |
| `serial-observability` | 100 | 4 | 38.654 s |

The 38 approved parallel modules are too small a fraction of the complete
suite to offset process/resource overhead and variation in the dominant serial
tail. More workers are not the immediate remedy. A separate duration-led
provisional-promotion campaign now records the proposed path to a materially
larger safe set and future distributed CI profiles.

## Isolation and safety

- Every two-worker group wrote its result beneath its uniquely named owned root
  in `.tmp-test-suite-final-parallel-reboot`.
- The corresponding one-worker groups wrote beneath the separate
  `.tmp-test-suite-final-serial-reboot` root.
- No group result path crossed into another group's root.
- No package source, packaged resource/schema/fixture, `pyproject.toml`, build,
  distribution, or release-receipt surface was modified by either invocation.
- The runner strips inherited AstroWoof and named external-service credentials;
  its direct child-process sanitation regression passed.
- No provider, R2, Render, QA, retained-workspace, package publication, or
  release action occurred.
- No Python runner/test process remained after completion.
- Protected logging tests ran in the explicit unquiet
  `serial-observability` group; routine tests retained the runner-only quiet
  posture.

## Failure qualification

The earlier deterministic injection runs remain valid against both weighted
parallel groups:

- injected `parallel-1`: aggregate failed, 237 tests/40 skips, one exact
  synthetic failure, reproduction command retained;
- injected `parallel-2`: aggregate failed, 237 tests/40 skips, one exact
  synthetic failure, reproduction command retained.

The aggregate did not flatten either failure into an exit-code-only result.
Each failed group retained its full module command and exact failure identity.

## Final mechanical checks

- focused runner suite: 10 passed;
- `git diff --check`: clean at the Slice 4 gate;
- complete final one-worker and two-worker receipts: present and successful;
- orphan Python test processes: none; and
- installed/runtime package behavior: unchanged.

## Decision requested at Voof-paws 2

Approve the runner and manifest as a trustworthy test framework, while
recording that the present two-worker configuration is not yet the faster
whole-suite default on this laptop. CI/default adoption should distinguish:

1. adopting the deterministic framework and its safety controls; from
2. claiming or requiring parallel execution as a current performance win.

The follow-up promotion campaign can expand the safe set before the project
chooses a default worker profile. No package release is implicated by Slice 4.
