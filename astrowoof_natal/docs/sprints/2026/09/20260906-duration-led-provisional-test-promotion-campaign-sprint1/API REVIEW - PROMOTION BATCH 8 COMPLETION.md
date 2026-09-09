# API review — promotion batch 8 completion

## Decision

Batch 8 is complete and approved. The four authorized collision-qualified
modules were the only rows promoted, and Batch 9 may now be selected under the
same duration-and-state-risk rules.

## Evidence accepted

The live manifest moved exactly from `57/39/36` to `61/35/36`; all 16 runner
and manifest-inventory checks passed, including the exactly-once discovered-test
classification guard.

The required actual-manifest proof ran two complete two-worker
`parallel_only` coordinators concurrently. Both receipts agree on:

- 502 tests and 46 expected skips;
- identity digest `f24072e8e0e84c9ecbfd6b689c56fd9f9014ee6e0a8f75e4751ae1f12e447bd7`;
- outcome digest `49df71685c87db3d7b0b5c024f8ae2fcb191e2962cc25bcd83d5eef7fa734324`;
- manifest digest `048ddb14903906f9e637124571c1503071c612bda25f9079687849b67e1877b8`; and
- empty failure/error inventories and stderr posture.

This proves the modules operate in the supported weighted manifest, not merely
in their tailored collision matrix. The ~346-second walls are host-contention
calibration evidence only; they do not establish a whole-suite speed claim.
No release, package, provider, production, or semantic-closure authority has
changed.

## Next boundary

Select and audit Batch 9 separately. Every further classification change still
requires its own state-surface evidence, collision qualification, and
post-promotion actual-manifest proof.
