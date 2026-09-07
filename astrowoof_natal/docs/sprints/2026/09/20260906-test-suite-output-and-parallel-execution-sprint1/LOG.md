# Log — quiet tests and safe parallel execution

## 2026-09-06 — Slices 0–1

- Adopted the owner decision to suppress routine console sparkle-dog output via
  a test-only log-level boundary; production and sink behavior stays unchanged.
- Mapped CLI/root logging configuration and identified the protected
  observability modules.
- Measured a representative CLI test at INFO and with test-only INFO
  suppression.
- Classified the current 129 test modules conservatively: 38 parallel-safe,
  55 provisional, and 36 serial-only. The 129th is the Slice 3 runner test.
- Found a hidden import-order dependency: direct module shards require explicit
  `PYTHONPATH=astrowoof_natal/src`.
- Ran the same 39-module safe-candidate inventory with one, two, and four
  processes. All corrected runs agreed on 239 tests, 41 skips, and success.
- Recommended two deterministic weighted workers for the first supported
  prototype; four round-robin workers were badly imbalanced.
- Made no production logging, test-runner, CI, or release-playbook change.

## 2026-09-06 — Slices 2–3

- Added a runner-only quiet bootstrap and protected logging-sensitive group.
- Corrected one classification after an honest quiet-run failure:
  decision-evidence observability moved from parallel-safe to protected serial.
- Added the executable classification manifest and deterministic coordinator.
- Measured and checked in 38 per-module duration weights.
- Passed the weighted two-worker subset in 46.498 seconds with balanced shard
  completion and an exact identity digest.
- Compared pytest-xdist 3.8.0 on the same module set; it passed in 57.384
  seconds but added cache/isolation and reporting complexity, so it was not
  adopted.
- Paused before Slice 4 and made no CI/default/release-process change.
- Incorporated API review corrections: deny all inherited `ASTROWOOF_*`
  variables, prove named secrets absent in a child process, and reconcile the
  current narrative inventory to 129 modules.
- Repassed the 236-test approved subset under the stricter sanitizer in 43.614
  seconds with the same test-identity digest.
- Slice 4's first 1,114-test broad gate found one remaining INFO-sensitive
  assertion in the quiet serial tail. Reclassified the already-serial external
  authority execution module as protected/unquiet without weakening its test.

## 2026-09-07 — Slice 4 complete

- Added exact outcome inventories to the aggregate receipt and covered them
  with the runner's tenth focused regression.
- Completed the authoritative final pair over 1,115 tests and 58 skips.
- One-worker and two-worker test and outcome digests match exactly; both runs
  passed without failures, errors, or unexpected successes.
- The two-worker run took 1,091.085 seconds versus 964.806 seconds for one
  worker. The current safe set is too small and the serial tail too dominant to
  provide a whole-suite speedup on this laptop.
- Verified owned group-result roots, unchanged package/release surfaces, no
  orphan Python test processes, and no external-system activity.
- Retained the deterministic runner as a strong growth framework and created a
  separate duration-led provisional-promotion campaign rather than expanding
  this already-large sprint.
- Paused at Voof-paws 2 before CI/default or release-playbook adoption.

## 2026-09-07 — Slice 5 adoption decision

- Adopted the deterministic runner and checked-in manifest as the supported
  broad-confidence framework.
- Set one worker as the supported default; two-worker execution remains an
  experimental profile until duration-led promotion or different hardware
  proves a repeatable gain.
- Retained direct unittest discovery as the universal diagnostic fallback.
- Added a maintainer-facing runner guide and updated the release playbook.
- Strengthened fail-closed manifest regressions for new unclassified modules,
  duplicate classifications, stale/nonexistent entries, and the one-worker
  default.
- No CI workflow exists in this repository today; future CI adoption must use
  this same manifest/coordinator rather than reimplement sharding in YAML.

## 2026-09-07 — Slice 6 closeout

- Ran the newly documented broad-confidence command without `--workers`.
- Receipt confirmed the adopted one-worker default and a green 1,118-test,
  58-skip inventory in 1,122.983334 seconds.
- Recorded exact test and outcome digests in the closeout evidence.
- Confirmed that the sprint changes test/process tooling, tests, and
  documentation only; no package version or release is warranted.
- Closed the sprint and handed further parallel-set expansion to the separate
  duration-led provisional-promotion campaign.
