# Slice 1 — Exact Retained Binding Join Finding

## Authorized acquisition

The owner authorized exactly one conditional HEAD and one bounded GET for each
named checkpoint. Those four operations were performed and the budget is now
consumed. No listing, alternate-key discovery, write, delete, provider call, or
retained-run mutation occurred.

| Witness | HEAD | GET | Archive identity | Inventory identity |
| --- | ---: | ---: | --- | --- |
| A | 1 | 1 | 4,719,373 bytes; `e09545cb...ef454` | 922 workspace members; `7864a9bf...a295d` |
| B | 1 | 1 | 5,098,057 bytes; `1d20a6e2...b10e7` | 934 workspace members; `d034d78f...639d3` |

Both archives were safely extracted outside Git after duplicate-name,
traversal, link, member-set, byte-size, per-member digest, and canonical
inventory verification. Offline public-reader execution used network-disabled,
read-only containers mounted at each receipt's original logical root.

## Exact joins that pass

For both witnesses:

- the exact native reader accepts the selected result and receipt;
- result, receipt, and restored state carry the same native run;
- `post_checkpoint.native_state_revision` equals durable `state_revision`;
- result and receipt checkpoint-basis digests agree;
- result release equals the recorded runtime release;
- disposition count equals ledger action count;
- disposition action IDs equal ledger action IDs exactly; and
- the retained initial assembled deck exists and matches its recorded digest.

Witness A has seven ledger actions and seven dispositions. Witness B has eight
of each. The current public collector reproduces
`contradictory_native_evidence` for both exact result IDs.

## Three-way digest result

Every one of the fifteen action comparisons has the same outcome:

| Comparison | Witness A | Witness B |
| --- | ---: | ---: |
| sealed disposition equals producer projection | 7/7 | 8/8 |
| sealed disposition equals complete ledger binding | 0/7 | 0/8 |

Every complete ledger binding has the same four fields outside the sealed
terminal projection: `model`, `prepared_state_revision`, `run_id`, and
`service_level`.

The first pass attempt therefore reaches the review-only membership check with
an action ID that exists but a digest recomputed over a larger object than the
producer sealed. Capture returns `native_join_conflict` before packet assembly.
No optional-stage or artifact-only defect is needed to explain either witness.

## Gate B ruling

The live cause is established independently in both retained workspaces. The
v0.2 result is internally correct according to its producer contract; the
editorial capture consumer recomputes that contract identity from the wrong
digest domain.

