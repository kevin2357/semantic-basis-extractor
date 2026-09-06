# Log

## 2026-08-31 — planning

- Read `Background.md` and the full concatenated Render export at
  `C:\tmp\sbe_worker_logs.txt`.
- Created the investigation plan with review pauses before contract and runtime
  work.
- Recorded API's pre-Slice 0 review and tightened the R2, failure-result, and
  semantic-parity requirements.

## 2026-08-31 — Slice 0

- Parsed the concatenated JSON export with a streaming JSON decoder; no log
  rewriting was required.
- Joined the 11:54 retrieval/action/pass sequence to the SBE 0.4.35 traceback.
- Compared tag `astrowoof-natal-authoring-v0.4.35` with current `main`.
- Identified the historical worker-local path:
  `save_state -> read_native_transition_result -> validate_workspace_snapshot`.
- Confirmed that commit `96980ab` removed that lookup from `save_state()` in
  0.4.36; recorded it as a current-main distinction, not yet as a qualified fix.
- Added a provider-free, content-free inventory-delta characterization for
  equal-cardinality digest mutation and a 30-member sibling pass tree.
- Decided not to request retained R2 access at this point because the traceback
  establishes the validator boundary and the transient writes may not exist in
  the last valid checkpoint.

### Paws point 1

API approved the causal class and the no-R2 decision. Its two precision
corrections were incorporated: restored-checkpoint innocence is not claimed
without retained-byte inspection, and reported-cost persistence proves local
reconciliation/accounting progress rather than native adoption. Slice 2 must
compare the real historical boundary on 0.4.35 with 0.4.36/current main.

No provider, R2, retained-workspace, runtime, release, or deployment activity
occurred.

## 2026-08-31 — Slice 2 preliminary wheel comparison

- Installed immutable 0.4.35 and 0.4.36 wheel artifacts into separate local
  targets without dependency or network activity.
- Ran one identical production-boundary fixture against both wheels.
- 0.4.35 reproduced the expected worker-side whole-workspace validation error.
- 0.4.36 completed worker persistence, coordinator snapshot publication, and
  exact immutable review-result replay.
- Added a real `author_pending_passes()` serial/concurrent comparison. Both
  wheels produced identical normalized pass/attempt/QA/file/action truth; the
  concurrent run demonstrated actual overlap.
- Recorded this as decisive for the immediate crash path, while retaining the
  mixed provider-custody reconciliation and interruption matrix as the
  remaining Slice 2 gate.
- Added a real mixed-custody boundary with two durable completed response
  artifacts, two pending actions, a sealed review predecessor, and a
  reconciliation-only controller. The 0.4.35 wheel failed at worker-local
  validation; 0.4.36 adopted both completed passes concurrently, retained both
  pending actions, made zero transport calls, validated the successor snapshot,
  and reopened the exact predecessor.
- Reached Paws point 2. The remaining question is interruption classification
  and typed safe-replay versus review evidence, not reproduction.

## 2026-08-31 — closeout decision

- Owner/API review accepted 0.4.36's removal of implicit sealed-result
  discovery as the narrow Kardamom correction.
- No additional runtime patch or release is needed for this sprint.
- Retained the characterization and wheel-battle tests as regression evidence.
- Deferred quarantine/interruption contract work to the immediately following
  sprint rather than widening this completed investigation.
