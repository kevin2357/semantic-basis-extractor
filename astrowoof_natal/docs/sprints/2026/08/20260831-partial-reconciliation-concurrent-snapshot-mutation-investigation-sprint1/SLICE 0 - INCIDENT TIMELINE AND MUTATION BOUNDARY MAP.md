# Slice 0 — incident timeline and mutation-boundary map

## Decision

The Kardamom failure has a source-and-trace-supported causal mechanism in SBE
0.4.35. The available evidence identifies a live validation-boundary race and
does not implicate the restored predecessor checkpoint; without reading the
retained bytes, it does not categorically exclude every pre-existing workspace
defect. The first `390 / 390` line was not an added-file event.

SBE 0.4.35 made a worker-thread `save_state()` inspect the latest sealed native
result before persisting state. That inspection called
`read_native_transition_result()`, which revalidated the whole workspace
snapshot. At the same time, another approved pass worker was writing ordinary
request/response artifacts into the same workspace. The validation therefore
compared a quiescent predecessor manifest with a legitimately moving workspace.

This is a validation-at-the-wrong-boundary defect made observable by concurrent
fan-in. It is also a shared-workspace coordination warning: the worker lock
serialized state writes, but did not make pass-local filesystem production
quiescent for a whole-workspace reader.

## Frozen 11:54 UTC sequence

Run: `a120a14edaf523856444d3fb895b15340874efe258fe818b8bbb5d943b6e518f`

1. `11:54:02.192` — lifecycle selected one four-action reconciliation subset.
2. `11:54:02.197–02.208` — GETs began for actions `paid_7d5a…`,
   `paid_7d5f…`, `paid_9a0e…`, and `paid_dbf1…`.
3. `11:54:02.520–03.115` — all four retrieval calls returned. Native selection
   classified pass 3 (`paid_dbf1…`) and pass 5 (`paid_7d5a…`) as completed;
   passes 2 and 4 retained pending provider custody.
4. `11:54:03.488` — `author_pending_passes()` started pass 3 and pass 5 with
   `max_workers=2`.
5. Each worker entered its existing attempt and the OpenAI adapter wrote
   pass-local request evidence before consuming the already-reconciled result.
6. `11:54:04.386` — a worker-side `save_state()` followed the 0.4.35 sealed-
   result preservation lookup into `read_native_transition_result()` and then
   `validate_workspace_snapshot()`. Expected and actual inventories both had
   390 paths but differed in at least one existing member's bytes/digest.
7. `11:54:04.408` — pass 3's provider cost became durable, proving execution
   progressed into local reconciliation/accounting. This does not prove native
   pass-truth adoption or successor publication.
8. `11:54:04.611` — the next whole-workspace validation saw 420 actual paths
   against 390 expected. The +30 members have the cardinality and timing of one
   complete pass-local response tree. Historical logs do not contain the paths,
   so that exact path attribution remains a strong source-consistent inference,
   not retained-byte proof.
9. The `ValueError` escaped through `future.result()`, then through
   `run_bounded_authoring_reconciliation()` and the public CLI. No typed native
   result made the failure non-retryable or proved a safe replay.

The same pattern repeated as the workspace/checkpoint member count advanced
from 390 to 392 and then 422. Later cycles selected more completed members and
re-entered the same invalid boundary.

## Exact historical call path

The 0.4.35 traceback records:

```text
author_one_pass -> save_state
save_state -> read_native_transition_result
read_native_transition_result -> validate_workspace_snapshot
validate_workspace_snapshot -> ValueError
```

The top-level escape path records:

```text
closure.main
  -> reconcile_authoring_provider_cycle
  -> run_bounded_authoring_reconciliation
  -> author_pending_passes
  -> future.result
  -> author_one_pass
```

## Inventory classification

The provider-free Slice 0 recorder compares manifests by relative path and
classifies additions, removals, byte-count changes, and digest changes without
reading file contents into evidence.

- Equal-count mutation: changing `run.json` from revision 14 to revision 15
  preserves the path and byte count but changes its digest. Validation rejects
  it with no added or removed path.
- Added pass tree: a sibling writer adds 30 response members under one pass
  root. Validation rejects the resulting `N -> N+30` inventory and the recorder
  attributes all additions to that disjoint pass root.

This proves the two log shapes represent distinct mutation classes. It does
not claim that the retained QA workspace contains the transient 30 files; the
failed command never published them as a valid successor checkpoint.

## Current-main distinction

Commit `96980ab` (released in 0.4.36) removed the sealed-result lookup from
`save_state()`. Consequently, current worker-thread `save_state()` no longer
calls `read_native_transition_result()` or validates the whole workspace at
that point. This removes the exact 0.4.35 crash path.

That removal occurred inside the observability release and is not, by itself,
a sufficient closeout claim. Later slices must prove:

- terminal-review status preservation still occurs at the correct coordinator
  boundary;
- concurrent and serial fan-in yield the same complete native truth;
- no other whole-workspace reader runs while pass-local writers are active;
- interruption yields either typed non-retryable review or an affirmatively
  safe replay; and
- pending provider custody remains intact.

## R2 decision

No retained R2 read is requested at this paws point. The exact exception path
is present in the full trace, and the relevant transient local writes would not
necessarily exist in the last valid checkpoint. If later parity or provenance
work bottoms out, SBE will request a coordinate packet and new explicit owner
authorization before any `HEAD` or `GET`.

## Slice 0 conclusion

The causal class is sufficiently established to pause for review:

> SBE 0.4.35 performed a strict whole-workspace validation from worker-local
> persistence while sibling local fan-in was mutating the workspace. The first
> mismatch was existing-member mutation; the later mismatch was added pass-local
> output. The failure escaped untyped and was retried.

Slice 2 should now reproduce the real 0.4.35 call boundary and compare it with
current main before selecting a correction family. Slice 1 remains optional.
