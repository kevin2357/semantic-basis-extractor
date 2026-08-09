# Slice 0 - Forensic Model and Reproduction

Status: complete; gate approval pending.

## Result

The retained 0.2.1 run was inspected read-only and reduced to a compact,
non-payload forensic model. Two deterministic synthetic regressions reproduce
the mechanisms necessary for the observed failure.

### Lost subject publication

`finalize_subjects()` obtains or assembles a subject record, calls
`polish_subject()`, and only afterward assigns that record into
`state["subjects"]`. The second-attempt `AwaitingSpendAuthorization` exception
escapes `polish_subject()` and bypasses the assignment.

The regression begins with a QA-warning deck, accepts an improving first polish
result, copies its deck and reports into the final paths, then raises the spend
pause on attempt 2. It proves:

- the final deck changed to the first polish result;
- attempt 1 is `POLISH_ACCEPTED` in the local record;
- attempt 2 is locally `SUBMITTED`; and
- persisted operator state still has no subject record.

This matches the retained run's empty `subjects` object despite its native
attempt-1 outputs and rewritten final files.

### Mixed-generation snapshot

`snapshot_inventory()` walks and hashes the workspace without a run-wide
quiescence lock. A controlled regression mutates three final files after their
old generation has been inventoried but before the later attempt subtree is
inventoried. The resulting snapshot contains old final identities and new
attempt identities, and immediately fails native snapshot validation.

The retained manifest has exactly that shape: its old final identities coexist
with matching new attempt-1 artifacts and the prepared attempt-2 request.
This proves SBE can publish a mixed-generation manifest when inventory overlaps
workspace mutation. It does not prove which two acceptance-worker lifetimes
overlapped; container/process timing evidence remains external. The initially
observed transient snapshot-write race and the stable mismatch are therefore
classified as the same missing-quiescence class, while lost subject publication
is a separate deterministic exception-ordering defect at the same boundary.

## Retained-run invariants

- Run schema: `astrowoof.semantic_closure_run.v0.9`.
- State revision: 60.
- Public/operator status: `AWAITING_SPEND_AUTHORIZATION`.
- Snapshot members: 876; no missing or additional authoritative members.
- Action 1: `REPORTED`, durable Response ID, 16,644 reported micro-USD.
- Action 2: `PREPARED`, no authorization in ledger, no provider identity, no
  consumption, and no reported usage.
- External action-2 authorization: exact binding match.
- Changed members: final deck, validation report, and lint report only.
- Each changed final member equals its retained attempt-1 counterpart.
- `spend-consumption.lock` is intentionally outside snapshot authority.

No provider operation, authorization consumption, repair, snapshot rewrite, or
acceptance-run mutation occurred.

## Frozen implementation boundary

Production work may touch:

- `astrowoof_natal_authoring/closure.py` for split persistence/checkpointing,
  subject ownership, run locking, boundary classification, and orchestration;
- `astrowoof_natal_authoring/spend.py` or packaged contracts only if a proven
  state/revision transition requires it;
- a narrowly scoped installed repair/inspection command and entry point;
- focused semantic-closure/spend/recovery tests; and
- the durable workspace, spend, runner, consumer, sprint, and release docs.

Extraction, scoring, selection, synthesis, production prompts, provider
disclosure, pricing, generation policy, QA rules, and delivery semantics remain
out of scope. Any need to change them requires a plan revision.

## Verification

- Lost-subject polish-boundary regression: pass (defect reproduced).
- Mixed-generation snapshot regression: pass (defect reproduced).
- Retained acceptance run: read-only.
- Provider requests and incremental spend: zero.
- `git diff --check`: pending final gate check.

Next action: approve the reproduced two-defect model and frozen implementation
boundary before Slice 1 changes production checkpoint orchestration.
