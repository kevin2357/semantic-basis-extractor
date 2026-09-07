# Slice 3 — promotion batch 2

## Cohort

The next three remaining duration leaders formed one bounded cohort:

- `test_happy_path_qa_slice4b.py` — frozen isolated weight 44.831 seconds;
- `test_adversarial_qa.py` — 24.845 seconds; and
- `test_legacy_local_work_upgrade_qa.py` — 20.393 seconds.

Together they accounted for 89.9 seconds of the original provisional tail.

## State-surface decision

All three use owned temporary output roots and provider-free qualification
surfaces. None writes repository/package artifacts, mutates ambient environment
or working directory, opens a database/listening port, or possesses real
provider authority.

The cohort deliberately covers distinct isolation risks:

- happy-path repeatedly builds production-shaped temporary workspaces;
- adversarial qualification caches one process-local, read-only receipt at
  class setup; and
- legacy upgrade invokes a child package CLI, whose environment and outputs
  remain inside the runner worker's sanitized boundary.

No repair or semantic change was needed.

## Collision evidence

Three repetitions launched two independent copies of every module together—six
worker processes per repetition. Every worker passed:

| Module | Result per copy | Repetition durations (seconds) |
|---|---|---|
| happy path | 6 tests, 1 optional-schema skip | 53.96/53.17; 60.36/60.99; 62.35/62.47 |
| adversarial | 5 tests, 0 skips | 30.34/30.10; 37.64/37.24; 40.95/40.68 |
| legacy upgrade | 9 tests, 1 optional-schema skip | 22.96/22.47; 31.43/31.76; 28.47/28.33 |

There were no failures, errors, identity changes, provider calls, or leaked
shared artifacts.

## Promoted-manifest proof

After promotion, two complete two-worker `parallel_only` executions ran
concurrently as a four-process stress case. Both passed:

- 301 tests, 42 skips;
- identity digest
  `9108c5ce651120c48b7e16b9029b798e26e1e17b002214e1b2e6ef026a4112e0`;
- outcome digest
  `ec7f2e1eb7a7e5426e4208a384de72fdbdd746552f532a0115592158e17f745f`;
- wall times 275.520 and 275.380 seconds.

The manifest is now 43 `parallel_safe`, 50 `provisional`, and 36
`serial_only`. Semantic closure remains unchanged and serial.

## Next boundary

Pause for review of promotion batch 2 before selecting another cohort. The next
duration leaders are composed runtime/qualification modules and require their
own state-surface audit rather than inheriting this decision.
