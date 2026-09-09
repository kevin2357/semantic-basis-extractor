# API review — promotion batch 9 completion

## Decision

Batch 9 is complete and approved. The five authorized modules were the only
manifest changes, and Batch 10 may be selected for its own separate audit.

## Evidence accepted

The live manifest moved exactly from `61/35/36` to `66/30/36`; all 16 runner
and manifest-inventory regressions passed, including exactly-once discovery.

The required actual-manifest proof ran two complete two-worker
`parallel_only` coordinators concurrently. Both receipts agree on:

- 555 tests and 46 expected skips;
- identity digest `b876ea3a8be28ded68a72821e640471463498e16eea98d4dcf6019fb5dd361d9`;
- outcome digest `7f193d0bee9bd497f0dc1ca4d3335dd820ed273375ab6bdbbcaee0c594ba0527`;
- manifest digest `a3c63c65abaea59e1918f166a390ed433620fc57d58a9e212e2360ef6c32deb9`; and
- empty failure/error and stderr posture.

That is sufficient evidence that the five modules compose in the live weighted
manifest. The approximately 337-second wall times remain host-contention
calibration only, not a whole-suite performance conclusion. No package,
provider, production, release, or semantic-closure authority changed.

## Next boundary

Batch 10 must receive its own state-surface audit, bounded collision evidence,
promotion decision, and post-promotion actual-manifest proof.
