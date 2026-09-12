# Slice 0 — current-tree and moving-family intake

## Outcome

The Sprint 1 handoff remains internally coherent after rebasing this dedicated
worktree onto current `main` at `c5e6593`. The editorial-review packet family
is now frozen and is the only changed portion of the inherited provisional
tail. No active test is unclassified.

## Manifest reconciliation

| Classification | Sprint 1 handoff | Current | Explanation |
|---|---:|---:|---|
| `parallel_safe` | 78 | 81 | Three already-approved modules entered current `main`: terminal-review QA, terminal-review interruption, and Waffle/Scone finalization. |
| `provisional` | 18 | 18 | The exact inherited tail is unchanged. |
| `serial_only` | 36 | 37 | The operator-disposition reader was deliberately classified serial and logging-sensitive after the handoff. |
| `logging_sensitive` | — | 12 | Current protected-logging overlay; it includes the new operator-disposition reader. |

Current manifest SHA-256:
`a54d03a7a95ea1facce06cacaa363651dd1caf461e5bafb80e59adf4a69483ac`.

The focused runner/manifest guard passed 16 tests. It proves exact-once active
module classification, rejects omissions/duplicates, and retains worker secret
environment scrubbing.

## Changed provisional family

Diffing tests from the Batch 11 checkpoint `70f9780` to current `HEAD` found
exactly these changed provisional modules:

- `test_editorial_review_contract_foundation.py`
- `test_editorial_review_contract_fixtures.py`
- `test_editorial_review_contract_qualification.py`
- `test_editorial_review_runtime.py`

Their owning implementation/release sequence is frozen by commits `fffac7e`,
`0699538`, `979ac3f`, and `742e0fc`; they can now be considered together rather
than treated as a moving family.

## Current-source measurement

| Module | SHA-256 | Tests | Skips | Seconds |
|---|---|---:|---:|---:|
| `test_editorial_review_contract_fixtures.py` | `4ada58b8f47ab827683d1fa53bd487586f7293ef842475d72930195802a465a7` | 9 | 0 | 8.450852 |
| `test_editorial_review_contract_qualification.py` | `c19d0d3e187c1c155437bed6e6a7b81e5ac544aa7b14e50f6e84d5f6778f50e5` | 7 | 0 | 7.621098 |
| `test_editorial_review_contract_foundation.py` | `c5b39932b80146520d10a1b72106698ff8dfccc20667daef9c7920b335fc7676` | 12 | 1 | 2.274651 |
| `test_editorial_review_runtime.py` | `941eb5b41d8e02980f33b9f61ad4449c7ec81c0c42f4a39690795823b99a545c` | 11 | 0 | 2.123262 |

The family totals 39 tests, one expected optional-`jsonschema` skip, and
20.470863 seconds on this host. All modules passed. These current-source values
supersede no unrelated frozen weights.

## Slice decision

Use the four modules as one coherent Batch 12. This honors the earlier intake
decision, reviews shared contracts and runtime capture together, and captures
more useful duration than the remaining isolated subsecond tail. Duration
prioritizes this audit but does not establish collision safety.

No manifest classification, runtime/package behavior, or external system was
changed by Slice 0.
