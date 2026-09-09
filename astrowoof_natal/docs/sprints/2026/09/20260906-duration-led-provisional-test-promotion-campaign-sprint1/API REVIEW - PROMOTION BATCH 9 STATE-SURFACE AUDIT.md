# API review — promotion batch 9 state-surface audit

## Decision

Approved to run bounded collision qualification for exactly these five Batch 9
modules:

- `test_review_required_pending_retries_investigation_slice2.py`;
- `test_spend_enforcement.py`;
- `test_external_authority_empty_inventory_investigation.py`;
- `test_lifecycle_closeout.py`; and
- `test_checkpoint_repair.py`.

This remains collision-only approval; no manifest row changes until a separate
promotion review.

## Review

The adaptive five-module cohort is justified by its compact measured tail
(7.924 seconds) despite its 53 tests. Each module confines writes, locks,
backups, and recovery artifacts to caller-owned temporary roots. The
provider-facing cases either use instance-local transport doubles or stop at
the spend callback before transport, so their valuable exact-call/no-call
assertions remain meaningful without external activity.

The review-required compatibility witness, logger/event-sink failures,
interruption recovery, and checkpoint `dry-run`/apply/back-up boundaries are
all retained as substantive coverage, not bypassed for scheduling convenience.
Process-global imports, log capture, and patches restore locally; no shared
database, network, provider, cwd, repository-write, fixed-output, or ambient
credential surface was identified.

## Collision gate

Run three repetitions of two independent copies per exact module, in controlled
waves of at most six workers. Require exact per-copy inventories of 4, 18, 13,
10, and 8 tests with zero skips, failures, errors, unexpected successes, or
coordinator stderr. Pause for a separate promotion decision before any
manifest update or actual-manifest stress proof.
