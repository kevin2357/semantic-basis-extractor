# Slice 3 — promotion batch 7 collision qualification

## Result

The complete three-module cohort passed the approved bounded collision matrix.
This is evidence for a separate promotion decision; it does not change the live
54/41/36 manifest.

## Matrix

Three repetitions launched two independent copies of every candidate together,
for six worker processes per repetition and 18 successful receipts total.

| Module | Exact outcome in every copy | Worker-duration range |
|---|---|---:|
| `test_sbe_v03.py` | 52 tests, 0 skips | 4.907–5.787 s |
| `test_negative_authorization.py` | 20 tests, 0 skips | 4.570–5.973 s |
| `test_operator_retirement_contract.py` | 26 tests, 2 optional-schema skips | 4.408–5.923 s |

Every copy used the supported secret-scrubbed provisional-measurement route,
an independent work root, and an independent receipt. All 18 workers passed
with empty stderr and no failures or errors.

Because the real modules ran, the result retains their substantive assertions:

- SBE v0.3 packet compilation, deterministic selection, validation/lint,
  workspace/archive round trips, package discovery, and child CLI behavior;
- typed negative authorization, stale/race precedence, byte-level refusal
  nonmutation, reconciliation recovery, replay, and zero provider work; and
- operator-retirement schema/assessment, atomic publication, interruption
  repair, single-writer exclusion, replay, and protected-sentinel isolation.

## Next boundary

Pause for the separate promotion decision. If approved, move only these three
modules to `parallel_safe`, run the runner inventory checks, and then run the
repeated concurrent actual-manifest stress proof. No semantic-closure movement,
production/package change, or later provisional promotion is authorized here.
